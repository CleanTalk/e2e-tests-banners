from lib.browser_init import driver as browser_driver
from inc.banners_consts import *
from lib.tools import *
from lib.stage_functions import *

import config


def check_paid_expired(driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver

    print("---=== Test banner with paid and expired key ===---")
    if not prepare_banner_stage(
        config.BANNERS_TESTS_API_KEY_PAID_EXPIRED,
        {'key_is_ok': 1, 'notice_trial': 0, 'notice_renew': 1, 'notice_review': 0, 'notice_show': 1},
        'injectrenewkey01',
        driver
    ):
        print("---=== Test banner with paid and expired key failed to set key ===---\n")
        return 1

    check_banner_on_settings_page_res = check_banner_on_settings_page(
        banner_renew_settings, banner_renew_settings_text, driver
    )
    check_banner_on_main_page_res = check_banner_on_main_page(
        banner_renew_dashboard, banner_renew_dashboard_text, driver
    )
    close_banner_on_main_page_res = close_banner_on_main_page(banner_renew_dashboard, driver)
    check_banner_on_main_page_not_exists_res = check_banner_on_main_page_not_exists(
        banner_renew_dashboard, driver
    )

    check_other_banners_on_main_page_res = check_other_banners_on_main_page(driver)
    check_banner_on_settings_page_res = check_banner_on_settings_page(
        banner_renew_settings, banner_renew_settings_text, driver
    )

    print("---=== Test banner with paid and expired key completed ===---\n")

    return (
        check_banner_on_settings_page_res or
        check_banner_on_main_page_res or
        close_banner_on_main_page_res or
        check_banner_on_main_page_not_exists_res or
        check_other_banners_on_main_page_res or
        check_banner_on_settings_page_res
    )
