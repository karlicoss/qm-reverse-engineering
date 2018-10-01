#!/usr/bin/env python3

import sys
from typing import Dict

from kython.scrape import get_chrome_driver

from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore

def get_qm_driver():
    driver = get_chrome_driver(
        headless=False,
        profile_dir='/tmp/qm-chrome-profile',
    )
    # err, okay, apparently it is necessary to log onto training session..
    driver.get('http://www.quantified-mind.com/lab/take_tests/6156220076392448')
    driver.implicitly_wait(2)
    cont_button = driver.find_element_by_xpath('//*[@id="mental-variables-form"]/input')
    cont_button.click()
    driver.implicitly_wait(2)
    return driver

driver = None

def run_sim(test_url: str, script_getter, params: Dict):
    global driver
    if driver is None:
        driver = get_qm_driver()
    driver.get(test_url)
    # TODO eh, not much point passing params, is there?
    driver.execute_script(script_getter(**params))
    start_button = driver.find_element_by_xpath('//*[@id="start_button"]')
    start_button.click()
    result_sel = 'body > div.container > div.row > div.test_left.span9.test_finished > div.test_content > table > tbody > tr > td:nth-child(2)'
    results = WebDriverWait(driver, 200).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, result_sel))
    )
    return results.text

def run_test(test_url, script_getter, results, delays, errors):
    global driver
    def has_result(delay, errors):
        ll = [x for x in results if x['delay'] == delay and x['errors'] == errors]
        return len(ll) > 0

    for delay in delays:
        for errcount in errors:
            if has_result(delay, errcount):
                continue
            while True:
                try:
                    res = run_sim(
                        test_url,
                        script_getter=script_getter,
                        params=dict(
                            delay=delay,
                            errors=errcount,
                            variation=10,
                        )
                    )
                    sys.stdout.write(f"{{ 'delay': {delay:4}, 'errors': {errcount:3}, ")
                    sys.stdout.flush()
                    sys.stdout.write(f"'res': '{res}' }},\n")
                    break
                except Exception as e:
                    print("# GETTING NEW DRIVER!")
                    if driver is not None:
                        driver.quit() # just in case...
                        driver = None

def run_simple_reaction():
    from js_scripts import get_simple_reaction_script
    from results import results_simple_reaction
    run_test(
        'http://www.quantified-mind.com/tests/simple_reaction_time/practice',
        get_simple_reaction_script,
        results_simple_reaction,
        delays=[
                       20,  30,  40,  50,  60,  70,  80,  90,
            100, 110, 120, 130, 140, 150, 160, 170, 180, 190,
            200, 210, 220, 230, 240, 250, 260, 270, 280, 290,
            300, 310, 320, 330, 340, 350, 360, 370, 380, 390,
            400, 410, 420, 430, 440, 450, 460, 470, 480, 490,
            500, 510, 520, 530, 540, 550, 560, 570, 580, 590,
            600, 610, 620, 630, 640, 650, 660, 670, 680, 690,
        ],
        errors=[
                0,
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                17, 18, 19,
        ],
    )

def run_visual_matching():
    from js_scripts import get_visual_matching_script
    from results import results_visual_matching
    run_test(
        "http://www.quantified-mind.com/tests/feature_match/practice",
        get_visual_matching_script,
        results_visual_matching,
        delays=[
            # ok, so my delay was 742 on average... so let's do from 20 to 1000 in steps of 20?
            *range(20, 1200, 20),
            *range(30, 1200, 20),
        ],
        errors=[
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
        ],
    )

# run_simple_reaction()
run_visual_matching()

# ok, so it's possible to get pretty high score on matching by answering some correctly and others on random just to shift time enough
# although I have to admit, it takes a while to do that
# TODO ah, looks like it computes reaction time among correct answers? well that makes it a bit harder...
# ok, so on the one hand I'm barely performing better than random
# on the other hand it seems to be pretty hard
# yup! I can beat it with strategy like 'guess few correctly and then press so reach 400ms average'
# ok, so what? that would be quite hard without immediate feedback. but still, pretty weird.
