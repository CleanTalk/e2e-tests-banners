import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from lib.tools import get_page_source
from lib.browser_init import driver as browser_driver

import config

def _pause():
    if config.BANNERS_TESTS_STEP_PAUSE > 0:
        time.sleep(config.BANNERS_TESTS_STEP_PAUSE)

def log_cleantalk_banner_ids(driver):
    notices = driver.find_elements(By.CSS_SELECTOR, '[id^="cleantalk_"]')
    ids = [item.get_attribute('id') for item in notices]
    print(f"[LOG] CleanTalk banner ids on page: {ids}")

def check_banner_on_settings_page(banner_id, banner_text, driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver

    driver.get(config.BANNERS_TESTS_SETTINGS_URL)
    _pause()

    try:
        WebDriverWait(driver, config.BANNERS_TESTS_REGULAR_TIMEOUT).until(
            EC.presence_of_element_located((By.ID, banner_id))
        )
        print(f"[OK] Banner [{banner_id}] is on settings page")
        if banner_text in get_page_source(driver):
            print(f"[OK] Banner [{banner_id}] text is correct on settings page")
            return 0
        print(f"[ALARM] Banner [{banner_id}] text is incorrect on settings page!!!")
        return 1
    except (NoSuchElementException, TimeoutException):
        print(f"[ALARM] Banner [{banner_id}] is not on settings page!!!")
        log_cleantalk_banner_ids(driver)
        return 1


def check_banner_on_main_page(banner_id, banner_text, driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver

    driver.get(config.BANNERS_TESTS_URL + '/wp-admin/index.php')
    _pause()

    try:
        WebDriverWait(driver, config.BANNERS_TESTS_REGULAR_TIMEOUT).until(
            EC.presence_of_element_located((By.ID, banner_id))
        )
        print(f"[OK] Banner [{banner_id}] is on main page")
        if banner_text in get_page_source(driver):
            print(f"[OK] Banner [{banner_id}] text is correct on main page")
            return 0
        print(f"[ALARM] Banner [{banner_id}] text is incorrect on main page!!!")
        return 1
    except (NoSuchElementException, TimeoutException):
        print(f"[ALARM] Banner [{banner_id}] is not on main page!!!")
        log_cleantalk_banner_ids(driver)
        return 1


def close_banner_on_main_page(banner_id, driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver
    try:
        print("[LOG] Closing banner on main page")
        close_banner = WebDriverWait(driver, config.BANNERS_TESTS_REGULAR_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'#{banner_id} button.notice-dismiss'))
        )
        close_banner.click()
        time.sleep(max(2, config.BANNERS_TESTS_STEP_PAUSE))
        driver.refresh()
        _pause()

        try:
            driver.find_element(By.ID, banner_id)
            print(f"[ALARM] Banner [{banner_id}] is not closed!")
            return 1
        except NoSuchElementException:
            print(f"[OK] Banner [{banner_id}] is not on main page, all is OK!")
            return 0
    except Exception as exc:
        print(f"[ALARM] Banner [{banner_id}] is not on main page, nothing to close!!! ({exc})")
        log_cleantalk_banner_ids(driver)
        return 1


def check_banner_on_main_page_not_exists(banner_id, driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver

    driver.get(config.BANNERS_TESTS_URL + '/wp-admin/index.php')
    _pause()

    try:
        driver.find_element(By.ID, banner_id)
        print(f"[ALARM] Banner [{banner_id}] is on main page!!!")
        return 1
    except NoSuchElementException:
        print(f"[OK] Banner [{banner_id}] is not on main page")
        return 0


def check_banner_on_settings_page_not_exists(banner_id, driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver
    driver.get(config.BANNERS_TESTS_SETTINGS_URL)
    _pause()

    try:
        driver.find_element(By.ID, banner_id)
        print(f"[ALARM] Banner [{banner_id}] is on settings page!!!")
        return 1
    except NoSuchElementException:
        print(f"[OK] Banner [{banner_id}] is not on settings page")
        return 0


def _visible_apbct_notices(driver):
    notices = driver.find_elements(By.CSS_SELECTOR, '.apbct-notice')
    return [item for item in notices if item.is_displayed()]


def check_other_banners_on_main_page(driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver

    print("[LOG] Checking other banners on main page")
    driver.get(config.BANNERS_TESTS_URL + '/wp-admin/index.php')
    time.sleep(max(2, config.BANNERS_TESTS_STEP_PAUSE))
    driver.refresh()
    _pause()

    extras = _visible_apbct_notices(driver)
    if extras:
        print('[ALARM] There is an extra banner on main page')
        log_cleantalk_banner_ids(driver)
        return 1
    print('[OK] There are no extra banners on main page')
    return 0


def check_other_banners_on_settings_page(driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver

    print("[LOG] Checking other banners on settings page")
    driver.get(config.BANNERS_TESTS_SETTINGS_URL)
    time.sleep(max(2, config.BANNERS_TESTS_STEP_PAUSE))
    driver.refresh()
    _pause()

    extras = _visible_apbct_notices(driver)
    if extras:
        print('[ALARM] There is an extra banner on settings page')
        log_cleantalk_banner_ids(driver)
        return 1
    print('[OK] There are no extra banners on settings page')
    return 0
