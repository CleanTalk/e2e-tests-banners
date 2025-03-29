from lib.browser_init import driver as browser_driver
from inc.options import *
from inc.banners_consts import *
from lib.tools import *
from lib.stage_functions import *


def check_review_key(driver_instance=None): 
    driver = driver_instance if driver_instance is not None else browser_driver
    
    print("---=== Test banner with review ===---")
    set_key(review_key, driver)

    check_banner_on_settings_page(banner_review, banner_review_text, driver)
    check_banner_on_main_page(banner_review, banner_review_text, driver)
    close_banner_on_main_page(banner_review, driver)
    check_banner_on_main_page_not_exists(banner_review, driver)

    check_other_banners_on_main_page(driver)
    check_other_banners_on_settings_page(driver)

    print("---=== Test banner with review completed ===---\n")
        