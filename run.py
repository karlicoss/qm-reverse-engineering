#!/usr/bin/env python3

import sys

from kython.scrape import get_chrome_driver

from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore

driver = get_chrome_driver(
    headless=False,
    profile_dir='/tmp/qm-chrome-profile',
)

# driver.get('http://www.quantified-mind.com/')
driver.get('http://www.quantified-mind.com/lab/take_tests/6156220076392448')

driver.implicitly_wait(2)

cont_button = driver.find_element_by_xpath('//*[@id="mental-variables-form"]/input')
cont_button.click()

driver.implicitly_wait(2)


def get_script(delay, variation, errors):
    return f"""
    var delay = {delay};
    var variation = {variation};
    var errors = {errors};
""" + """
    var count = 0;

    const press_space = del => {
        var press_down = new KeyboardEvent('keydown',{'keyCode':32,'which':32});
        setTimeout(
            () => document.dispatchEvent(press_down),
            del,
        );
    };

    const callback = event => {
        console.log(event);
        if (count % 2 == 1) {
            var del = errors > 0 ? 0 : delay + (Math.random() * variation - variation / 2);
            errors -= 1;

            // var x = document.getElementById("simple_reaction_time_stimulus");
            console.log("clicked!");
            press_space(del);
        }
        count += 1;
    };

    var e = document.getElementById('simple_reaction_time_stimulus');
    var observer = new MutationObserver(callback);
    // TODO ok I need odd ones
    observer.observe(e, {
        attributes: true,
        attributeFilter: ['class'],
        childList: false,
        characterData: false
    });
    """

def run_test(delay: int, variation: int = 10, errors: int = 0):
    driver.get('http://www.quantified-mind.com/tests/simple_reaction_time/practice')
    driver.execute_script(get_script(delay, variation, errors))
    start_button = driver.find_element_by_xpath('//*[@id="start_button"]')
    start_button.click()
    result_sel = 'body > div.container > div.row > div.test_left.span9.test_finished > div.test_content > table > tbody > tr > td:nth-child(2)'
    results = WebDriverWait(driver, 200).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, result_sel))
    )
    return results.text



for delay in [20, 50, 100, 200, 400]:
    sys.stdout.write(f"Running for delay {delay:5}... ")
    res = run_test(delay)
    sys.stdout.write(res + "\n")

