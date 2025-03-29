from lib.browser_init import driver as browser_driver
from inc.options import *
from inc.banners_consts import *
from lib.tools import *
from lib.stage_functions import *

def days25_paid_key_5sites(driver_instance=None): 
    driver = driver_instance if driver_instance is not None else browser_driver

    print("---=== Test banner with paid and 25 days to end and 5 sites, no banner ===---")
    set_key(days25_paid_key_sites5, driver)

    check_banner_on_settings_page_not_exists(banner_days25_paid_key_5sites, driver)
    check_banner_on_main_page_not_exists(banner_days25_paid_key_5sites, driver)

    print("---=== Test banner with paid and 25 days to end and 5 sites, no banner completed ===---\n")
