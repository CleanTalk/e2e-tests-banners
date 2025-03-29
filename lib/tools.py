import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from inc.options import *
from lib.browser_init import driver as browser_driver


# Set key
def set_key(key = '', driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver

    if driver.current_url != settings_page:
        print("[LOG] Reload page")
        driver.get(settings_page)

    locator = (By.ID, "apbct_setting_apikey")
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located(locator))
    align_center('apbct_setting_apikey', driver)
    driver.find_element(By.ID, 'apbct_setting_apikey').clear()
    put_key = driver.find_element(By.ID, 'apbct_setting_apikey')
    put_key.send_keys(key)

    align_center('apbct_settings__main_save_button', driver)
    driver.find_element(By.ID, 'apbct_settings__main_save_button').click()

    time.sleep(30)


# Get page source code
def get_page_source(driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver
    code = driver.find_element(By.XPATH, '/html/body')
    return code.get_attribute("outerHTML")


# Move browser view to the element
def align_center(form_element, driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver
    element1 = driver.find_element(By.ID, form_element)
    desired_y = (element1.size['height'] / 2) + element1.location['y']
    current_y = (driver.execute_script('return window.innerHeight') / 2) + driver.execute_script('return window.pageYOffset')
    scroll_y_by = desired_y - current_y 
    driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)


# Complete deactivation, to flush flags in DB
def complete_deactivation(driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver

    print("---=== Complete deactivation ===---")

    try:
        print("[LOG] Set regular key")
        set_key(regular_acc_key, driver)

        print("[LOG] Set complete deactivation")
        align_center('apbct_setting_data__email_decoder', driver)
        driver.find_element(By.CSS_SELECTOR, '#ct_adv_showhide > a').click()
        align_center('apbct_setting_misc__complete_deactivation', driver)
        driver.find_element(By.ID, 'apbct_setting_misc__complete_deactivation').click()
        driver.find_element(By.CSS_SELECTOR, '#apbct_settings__button_section > button').click()    

        driver.get(plugins_page)
        print("[LOG] Deactivate plugin")
        deactivation_button = driver.find_element(By.ID, 'deactivate-cleantalk-spam-protect')
        if deactivation_button:
            align_center('deactivate-cleantalk-spam-protect', driver)
            source_code = deactivation_button.get_attribute("innerHTML")
            deactivation_button.click()
            time.sleep(3)

        activation_button = driver.find_element(By.ID, 'activate-cleantalk-spam-protect')
        if activation_button:
            print("[LOG] Activate plugin")
            align_center("activate-cleantalk-spam-protect", driver)
            activation_button.click()
            time.sleep(3)
        
        print("[LOG] Save regular key")
        set_key(regular_acc_key, driver)
    except Exception as e:
        print(f"[ERROR] {e}")

    print("---=== Complete deactivation completed ===---\n")
