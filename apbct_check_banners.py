# constants
from inc.options import *
from inc.banners_consts import *

# tools
from lib.tools import *
from lib.helper import *

# browser
from lib.browser_init import browser_init

# stages
from lib.stages.auth import auth_demo3
from lib.stages.check_empty_key import check_empty_key
from lib.stages.check_review_key import check_review_key
from lib.stages.check_trial_key_expired import check_trial_key_expired
from lib.stages.check_days25_paid_key import check_days25_paid_key
from lib.stages.check_paid_expired import check_paid_expired
from lib.stages.check_days2_paid_key import check_days2_paid_key
from lib.stages.days25_paid_key_5sites import days25_paid_key_5sites
from lib.stages.check_review_key_sites5 import check_review_key_sites5
from lib.stages.check_2days_to_end_trial import check_2days_to_end_trial


def __main__():
    helper()
    driver = browser_init()

    auth_demo3(driver)
    complete_deactivation(driver)

    check_empty_key(driver) # empty key
    check_review_key(driver) # review key
    check_trial_key_expired(driver) # trial key expired
    check_days25_paid_key(driver) # 25 days to end of paid key
    complete_deactivation(driver)

    check_2days_to_end_trial(driver) # 2 days to end of trial
    check_paid_expired(driver) # paid and expired key
    complete_deactivation(driver)

    check_days2_paid_key(driver) # paid and 2 days to end
    complete_deactivation(driver)

    days25_paid_key_5sites(driver) # paid and 25 days to end, 5 sites, banner should not be (check renew)
    check_review_key_sites5(driver) # paid and 25 days to end, 5 sites, banner should not be (check renew)
    complete_deactivation(driver)

    print("Check completed")
    driver.quit()


if __name__ == "__main__":
    __main__()
