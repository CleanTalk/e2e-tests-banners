from lib.browser_init import driver as browser_driver
from lib.tools import *
from inc.banners_consts import *
from lib.stage_functions import *

import config


def check_trial_key_expired(driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver

    print("---=== Test banner with trial key ===---")
    if not prepare_banner_stage(
        config.BANNERS_TESTS_API_KEY_TRIAL_EXPIRED,
        {'key_is_ok': 1, 'notice_trial': 1, 'notice_renew': 0, 'notice_review': 0, 'notice_show': 1},
        'injecttrialkey01',
        driver
    ):
        print("---=== Test banner with trial key failed to set key ===---\n")
        return 1

    check_banner_on_settings_page_res = check_banner_on_settings_page(
        banner_trial_settings, banner_trial_settings_text, driver
    )
    check_banner_on_main_page_res = check_banner_on_main_page(
        banner_trial_dashboard, banner_trial_dashboard_text, driver
    )
    close_banner_on_main_page_res = close_banner_on_main_page(banner_trial_dashboard, driver)
    check_banner_on_main_page_not_exists_res = check_banner_on_main_page_not_exists(
        banner_trial_dashboard, driver
    )

    check_other_banners_on_main_page_res = check_other_banners_on_main_page(driver)
    check_banner_on_settings_page_res = check_banner_on_settings_page(
        banner_trial_settings, banner_trial_settings_text, driver
    )

    print("---=== Test banner with trial key completed ===---\n")

    return (
        check_banner_on_settings_page_res or
        check_banner_on_main_page_res or
        close_banner_on_main_page_res or
        check_banner_on_main_page_not_exists_res or
        check_other_banners_on_main_page_res or
        check_banner_on_settings_page_res
    )
