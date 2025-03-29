from lib.browser_init import driver as browser_driver
from inc.options import *
from inc.banners_consts import *
from lib.tools import *
from lib.stage_functions import *


def check_empty_key(driver_instance=None): 
    driver = driver_instance if driver_instance is not None else browser_driver
    
    print("---=== Test banner with empty key ===---")
    try:
        set_key('', driver)

        check_banner_on_settings_page(banner_key_empty, banner_key_empty_text, driver)
        check_banner_on_main_page(banner_key_empty, banner_key_empty_text, driver)
        close_banner_on_main_page(banner_key_empty, driver)
        check_banner_on_main_page_not_exists(banner_key_empty, driver)
    except Exception as e:
        print(f"[ERROR] {e}")

    print("---=== Test banner with empty key completed ===---\n")
