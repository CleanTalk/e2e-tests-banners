from lib.browser_init import driver as browser_driver
from lib.tools import *
from inc.banners_consts import *
from lib.stage_functions import *

# проверка триального ключа
def check_trial_key_expired(driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver

    print("---=== Test banner with trial key ===---")
    set_key(trial_key_expired, driver)

    check_banner_on_settings_page(banner_trial_key_expired, banner_trial_key_expired_text, driver)
    check_banner_on_main_page(banner_trial_key_expired, banner_trial_key_expired_text, driver)
    close_banner_on_main_page(banner_trial_key_expired, driver)
    check_banner_on_main_page_not_exists(banner_trial_key_expired, driver)

    check_other_banners_on_main_page(driver)
    check_banner_on_settings_page(banner_trial_key_expired, banner_trial_key_expired_text, driver)

    print("---=== Test banner with trial key completed ===---\n")
