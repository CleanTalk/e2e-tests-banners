# constants
from inc.banners_consts import *

# tools
from lib.tools import *

# browser
from lib.browser_init import browser_init

# stages
from lib.stages.auth import auth_admin
from lib.stages.check_empty_key import check_empty_key
from lib.stages.check_review_key import check_review_key
from lib.stages.check_trial_key_expired import check_trial_key_expired
from lib.stages.check_paid_expired import check_paid_expired

def __main__():

    driver = browser_init()

    auth_admin(driver)

    remove_dismissed_flags()

    #1
    check_empty_key_result = check_empty_key(driver) # empty key

    #2
    check_review_key_result = check_review_key(driver) # review key

    #3
    check_trial_key_expired_result = check_trial_key_expired(driver) # trial key expired

    #4
    check_paid_expired_result = check_paid_expired(driver) # paid and expired key

    print("Check completed")
    driver.quit()

    return(
        check_empty_key_result or
        check_review_key_result or
        check_trial_key_expired_result or
        check_paid_expired_result
    )

if __name__ == "__main__":
    __main__()
