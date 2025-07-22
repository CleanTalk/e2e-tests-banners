from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lib.browser_init import driver as browser_driver

import config

# Authorization in admin panel
def auth_admin(driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver

    driver.get(config.BANNERS_TESTS_URL + '/wp-login.php')
    locator = (By.ID, "wp-submit")
    element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located(locator))
    user_login = driver.find_element(By.ID, 'user_login')
    user_login.send_keys(config.BANNERS_TESTS_AUTH_LOGIN)

    user_pass = driver.find_element(By.ID, 'user_pass')
    user_pass.send_keys(config.BANNERS_TESTS_AUTH_PASS)

    send_auth = driver.find_element(By.ID, 'wp-submit')
    send_auth.click()
