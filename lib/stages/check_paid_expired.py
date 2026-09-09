from lib.browser_init import driver as browser_driver
from inc.banners_consts import *
from lib.tools import *
from lib.stage_functions import *

import config

def check_paid_expired(driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver

    print("---=== Test banner with paid and expired key ===---")
    set_notice_via_database('notice_show', 1)
    set_notice_via_database('notice_renew', 1)

    check_banner_on_settings_page_res = check_banner_on_settings_page(banner_paid_expired, banner_paid_expired_text, driver)
    check_banner_on_main_page_res = check_banner_on_main_page(banner_paid_expired, banner_paid_expired_text, driver)
    close_banner_on_main_page_res = close_banner_on_main_page(banner_paid_expired, driver)
    check_banner_on_main_page_not_exists_res = check_banner_on_main_page_not_exists(banner_paid_expired, driver)

    check_other_banners_on_main_page_res = check_other_banners_on_main_page(driver)
    check_banner_on_settings_page_res = check_banner_on_settings_page(banner_paid_expired, banner_paid_expired_text, driver)

    set_notice_via_database('notice_show', 0)
    set_notice_via_database('notice_renew', 0)
    print("---=== Test banner with paid and expired key completed ===---\n")

    return(
        check_banner_on_settings_page_res or
        check_banner_on_main_page_res or
        close_banner_on_main_page_res or
        check_banner_on_main_page_not_exists_res or
        check_other_banners_on_main_page_res or
        check_banner_on_settings_page_res
    )
