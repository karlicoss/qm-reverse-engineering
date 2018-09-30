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

# driver.get('http://www.quantified-mind.com/')
# driver.get('http://www.quantified-mind.com/lab/take_tests/6156220076392448')
# driver.implicitly_wait(2)
# cont_button = driver.find_element_by_xpath('//*[@id="mental-variables-form"]/input')
# cont_button.click()
# driver.implicitly_wait(2)

from js_scripts import get_script
# http://www.quantified-mind.com/tests/feature_match/practice
def run_test(test_url: str, params: Dict):
    driver.get(test_url)
    driver.execute_script(get_script(**params))
    start_button = driver.find_element_by_xpath('//*[@id="start_button"]')
    start_button.click()
    result_sel = 'body > div.container > div.row > div.test_left.span9.test_finished > div.test_content > table > tbody > tr > td:nth-child(2)'
    results = WebDriverWait(driver, 200).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, result_sel))
    )
    return results.text

def run_simple_reaction():
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
                        'http://www.quantified-mind.com/tests/simple_reaction_time/practice',
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


run_simple_reaction()
