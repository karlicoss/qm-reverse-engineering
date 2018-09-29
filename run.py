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
    const delay = {delay};
    const variation = {variation};
    const errors = {errors};
""" + """
    var count = 0;
    var err_count = 0;

    const press_space = del => {
        var press_down = new KeyboardEvent('keydown',{'keyCode':32,'which':32});
        setTimeout(
            () => document.dispatchEvent(press_down),
            del,
        );
    };

    const callback = event => {
        console.log(event);

        const is_green = count % 2 == 1;

        var del;
        if (err_count < errors) {
            // TODO assert !is_green?
            del = 5;
            count += 2; // mmm...
            err_count += 1;
            console.log("pressing error!")
        } else {
            count += 1;
            if (is_green) {
                del = delay + (Math.random() * variation - variation / 2);
                console.log("pressing green!");
            } else {
                return;
            }
        }
        press_space(del);
    };

    const e = document.getElementById('simple_reaction_time_stimulus');
    const observer = new MutationObserver(callback);
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


from results import results

def has_result(delay, errors):
    ll = [x for x in results if x['delay'] == delay and x['errors'] == errors]
    return len(ll) > 0

for delay in [
        20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190,
        200, 210, 220, 230, 240, 250,
        260, 270, 280, 290,
        300, 350, 400,
]:
    for errors in [
            0, 1, 2, 3, # 4, 5, 6, 7, 8, 9, 10,
    ]:
        # TODO be careful about it...
        if has_result(delay, errors):
            # print("SKIPPING", delay, errors)
            pass
            # continue
        while True:
            try:
                res = run_test(delay=delay, errors=errors)
                sys.stdout.write(f"{{ 'delay': {delay:4}, 'errors': {errors:3}, ")
                sys.stdout.flush()
                sys.stdout.write(f"'res': '{res}' }},\n")
                break
            except Exception as e:
                pass # try again
