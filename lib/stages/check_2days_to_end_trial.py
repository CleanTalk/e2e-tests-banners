from lib.browser_init import driver as browser_driver
from lib.browser_init import driver as browser_driver
from inc.options import *
from inc.banners_consts import *
from lib.tools import *
from lib.stage_functions import *

def check_2days_to_end_trial(driver_instance=None): 
    driver = driver_instance if driver_instance is not None else browser_driver
    
    print("---=== Test banner with 2 days to end trial ===---")
    set_key(two_days_to_end_trial, driver)

    check_banner_on_settings_page(banner_2days_to_end_trial, banner_2days_to_end_trial_text, driver)
    check_banner_on_main_page(banner_2days_to_end_trial, banner_2days_to_end_trial_text, driver)
    close_banner_on_main_page(banner_2days_to_end_trial, driver)
    check_banner_on_main_page_not_exists(banner_2days_to_end_trial, driver)

    check_other_banners_on_main_page(driver)
    check_banner_on_settings_page(banner_2days_to_end_trial, banner_2days_to_end_trial_text, driver)

    print("---=== Test banner with 2 days to end trial completed ===---\n")
