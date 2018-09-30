#!/usr/bin/env python3

import sys
from typing import Dict

from kython.scrape import get_chrome_driver

from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore

driver = get_chrome_driver(
    headless=False,
    profile_dir='/tmp/qm-chrome-profile',
)


def run_test(test_url: str, script_getter, params: Dict):
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

def run_simple_reaction():
    from js_scripts import get_simple_reaction_script
    TEST_URL = 'http://www.quantified-mind.com/tests/simple_reaction_time/practice'

    from results import results
    def has_result(delay, errors):
        ll = [x for x in results if x['delay'] == delay and x['errors'] == errors]
        return len(ll) > 0

    for delay in [
                       20,  30,  40,  50,  60,  70,  80,  90,
            100, 110, 120, 130, 140, 150, 160, 170, 180, 190,
            200, 210, 220, 230, 240, 250, 260, 270, 280, 290,
            300, 310, 320, 330, 340, 350, 360, 370, 380, 390,
            400, 410, 420, 430, 440, 450, 460, 470, 480, 490,
            500, 510, 520, 530, 540, 550, 560, 570, 580, 590,
            600, 610, 620, 630, 640, 650, 660, 670, 680, 690,
    ]:
        for errors in [
                0,
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                17, 18, 19,
        ]:
            # if has_result(delay, errors):
            #     continue
            while True:
                try:
                    res = run_test(
                        TEST_URL,
                        script_getter=get_simple_reaction_script,
                        params=dict(
                            delay=delay,
                            errors=errors,
                            variation=10,
                        )
                    )
                    sys.stdout.write(f"{{ 'delay': {delay:4}, 'errors': {errors:3}, ")
                    sys.stdout.flush()
                    sys.stdout.write(f"'res': '{res}' }},\n")
                    break
                except Exception as e:
                    print(e)
                    pass # try again

def run_visual_matching():
    from js_scripts import get_visual_matching_script
    TEST_URL = "http://www.quantified-mind.com/tests/feature_match/practice"
    for delay in [
            # ok, so my delay was 742 on average... so let's do from 20 to 1000 in steps of 20?
            *range(20, 1200, 20),
            *range(30, 1200, 20),
    ]:
        for errors in [
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
        ]:
            res = run_test(
                TEST_URL,
                script_getter=get_visual_matching_script,
                params=dict(
                    delay=delay,
                    errors=errors,
                    variation=10,
                )
            )
            sys.stdout.write(f"{{ 'delay': {delay:4}, 'errors': {errors:3}, ")
            sys.stdout.flush()
            sys.stdout.write(f"'res': '{res}' }},\n")


# run_simple_reaction()


run_visual_matching()
