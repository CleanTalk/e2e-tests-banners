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

    set_notice_via_database('notice_show', 0)
    set_notice_via_database('notice_review', 0)
    set_notice_via_database('notice_trial', 0)
    set_notice_via_database('notice_renew', 0)

    #1
    check_empty_key_result = check_empty_key(driver) # empty key
    remove_dismissed_flags()

    set_key(config.BANNERS_TESTS_API_KEY_REGULAR, driver)

    #2
    check_review_key_result = check_review_key(driver) # review key
    remove_dismissed_flags()

    #3
    check_trial_key_expired_result = check_trial_key_expired(driver) # trial key expired
    remove_dismissed_flags()

    #4
    check_paid_expired_result = check_paid_expired(driver) # paid and expired key
    remove_dismissed_flags()

    print("Check completed\n")
    driver.quit()

    print("Check results:\n")
    print("check_empty_key_result: {check_empty_key_result}\n")
    print("check_review_key_result: {check_review_key_result}\n")
    print("check_trial_key_expired_result: {check_trial_key_expired_result}\n")
    print("check_paid_expired_result: {check_paid_expired_result}\n")

    return(
        check_empty_key_result or
        check_review_key_result or
        check_trial_key_expired_result or
        check_paid_expired_result
    )

if __name__ == "__main__":
    __main__()
