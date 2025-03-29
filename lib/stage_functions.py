import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from lib.tools import get_page_source
from lib.browser_init import driver as browser_driver
from inc.options import settings_page


def check_banner_on_settings_page(banner_id, banner_text, driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver

    driver.get(settings_page)

    try:
        element = driver.find_element(By.ID, banner_id)
        print(f"[OK] Banner [{banner_id}] is on settings page")
        if banner_text in get_page_source(driver):
            print(f"[OK] Banner [{banner_id}] text is correct on settings page")
        else:
            print(f"[ALARM] Banner [{banner_id}] text is incorrect on settings page!!!")
            return
    except NoSuchElementException:
        print(f"[ALARM] Banner [{banner_id}] is not on settings page!!!")
        return


def check_banner_on_main_page(banner_id, banner_text, driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver

    driver.find_element(By.XPATH, '//*[@id="menu-dashboard"]/a/div[3]').click()
    time.sleep(3)

    try:
        element = driver.find_element(By.ID, banner_id)
        print(f"[OK] Banner [{banner_id}] is on main page")
        if banner_text in get_page_source(driver):
            print(f"[OK] Banner [{banner_id}] text is correct on main page")
        else:
            print(f"[ALARM] Banner [{banner_id}] text is incorrect on main page!!!")
            return
    except NoSuchElementException:
        print(f"[ALARM] Banner [{banner_id}] is not on main page!!!")
        return


def close_banner_on_main_page(banner_id, driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver
    try:
        print("[LOG] Closing banner on main page")
        close_banner = driver.find_element(By.CSS_SELECTOR, f'#{banner_id} > button')

        if close_banner:
            close_banner.click()
            
            time.sleep(3)
            driver.refresh()
            time.sleep(3) 

            try:
                empty_banner_element = driver.find_element(By.ID, banner_id)

                if empty_banner_element:
                    print(f"[ALARM] Banner [{banner_id}] is not closed!")
                    return
                else:
                    print(f"[OK] Banner [{banner_id}] is not on main page")

            except:
                print(f"[OK] Banner [{banner_id}] is not on main page, all is OK!")
    except:
        print(f"[ALARM] Banner [{banner_id}] is not on main page, nothing to close!!!")
        return


def check_banner_on_main_page_not_exists(banner_id, driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver

    driver.find_element(By.XPATH, '//*[@id="menu-dashboard"]/a/div[3]').click()
    time.sleep(3)

    try:
        driver.find_element(By.ID, banner_id)
        print(f"[ALARM] Banner [{banner_id}] is on main page!!!")
        return
    except NoSuchElementException:
        print(f"[OK] Banner [{banner_id}] is not on main page")
        return


def check_banner_on_settings_page_not_exists(banner_id, driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver
    driver.get(settings_page)

    try:
        driver.find_element(By.ID, banner_id)
        print(f"[ALARM] Banner [{banner_id}] is on settings page!!!")
        return
    except NoSuchElementException:
        print(f"[OK] Banner [{banner_id}] is not on settings page")
        return


def check_other_banners_on_main_page(driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver

    print("[LOG] Checking other banners on main page")
    driver.find_element(By.XPATH, '//*[@id="menu-dashboard"]/a/div[3]').click()
    time.sleep(3)
    driver.refresh()
    time.sleep(3)

    if ("apbct-notice" in get_page_source(driver) and
        '<h3>Help others to fight spam – leave your feedback!</h3>' not in get_page_source(driver)):
        print('[ALARM] There is an extra banner on main page')
    else:
        print('[OK] There are no extra banners on main page')


def check_other_banners_on_settings_page(driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver

    print("[LOG] Checking other banners on settings page")
    driver.get(settings_page)
    time.sleep(3)
    driver.refresh()
    time.sleep(3)

    if ("apbct-notice" in get_page_source(driver) and
        '<h3>Help others to fight spam – leave your feedback!</h3>' not in get_page_source(driver)):
        print('[ALARM] There is an extra banner on settings page')
    else:
        print('[OK] There are no extra banners on settings page')
