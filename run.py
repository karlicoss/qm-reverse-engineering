#!/usr/bin/env python3

import sys
import time
from typing import Dict, List
import json
from pathlib import Path

from selenium.webdriver import Chrome # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore


def get_driver(executable_path='/usr/lib/chromium-browser/chromedriver', profile_dir='/tmp/qm-chrome-profile'):
    opts = Options()
    opts.add_argument(f'--user-data-dir={profile_dir}')
    driver = Chrome(executable_path=executable_path, chrome_options=opts)
    return driver


class Runner:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self._driver = None

    def _reset(self):
        if self._driver is not None:
            self._driver.quit()
            self._driver = None

    @property
    def driver(self):
        if self._driver is None:
            self._driver = get_driver(**self.kwargs)
        return self._driver

    def run_sim(self, test_url: str, js_script: str):
        exc = None
        res = None
        for attempt in range(10):
            try:
                driver = self.driver
                driver.get('http://www.quantified-mind.com/')

                while len(driver.find_elements_by_link_text('Log out')) == 0:
                    print("Waiting for you to log in...")
                    time.sleep(1)

                ## first, we have to intiate any training session
                driver.get('http://www.quantified-mind.com/experiment/coffee') # default test pack, so everyone should have it
                driver.find_element_by_link_text('Take tests').click()
                driver.find_element_by_xpath('//option[@value=1]').click()
                driver.find_element_by_xpath('//*[@id="mental-variables-form"]/input').click()
                ##

                driver.get(test_url)
                driver.execute_script(js_script)
                start_button = driver.find_element_by_xpath('//*[@id="start_button"]')
                start_button.click()
                result_sel = 'body > div.container > div.row > div.test_left.span9.test_finished > div.test_content > table > tbody > tr > td:nth-child(2)'
                results = WebDriverWait(driver, 200).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, result_sel))
                )
                return results.text
            except Exception as e:
                exc = e
                print(f"{e}: getting new driver... (attempt {attempt})")
                time.sleep(5)
                self._reset()
        else:
            assert exc is not None
            raise exc

def has_result(state, params):
    if not state.exists():
        return False
    j = json.loads(state.read_text())
    return any(params == key for key, value in j)

def add_result(state, params, result):
    if not state.exists():
        j = []
    else:
        j = json.loads(state.read_text())
    j.append((params, result))
    with state.open('w') as fo:
        json.dump(j, fo, indent=1, sort_keys=True, ensure_ascii=False)


def run_test(test_url, js_script_template: str, delays: List, errors: List, state_file: str, **kwargs):
    state = Path(state_file)
    runner = Runner(**kwargs)

    for delay in delays:
        for errcount in errors:
            params = dict(
                delay=delay,
                errors=errcount,
                variation=10, # TODO better name?
            )
            print(f"{test_url}: {params}: ", end='')
            if has_result(state, params):
                print("already present, skipping")
                continue
            else:
                print("running...")

            js_script = js_script_template.format(**params)
            res = runner.run_sim(test_url, js_script)
            print(f'  result: {res}')

            add_result(state, params, res)

# ok, so it's possible to get pretty high score on matching by answering some correctly and others on random just to shift time enough
# although I have to admit, it takes a while to do that
# TODO ah, looks like it computes reaction time among correct answers? well that makes it a bit harder...
# ok, so on the one hand I'm barely performing better than random
# on the other hand it seems to be pretty hard
# yup! I can beat it with strategy like 'guess few correctly and then press so reach 400ms average'
# ok, so what? that would be quite hard without immediate feedback. but still, pretty weird.
