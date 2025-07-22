from datetime import datetime, timedelta

from inc.banners_consts import *

def helper():
    # Get current date
    current_date = datetime.now()
    print(current_date.strftime("%d.%m.%Y %H:%M:%S"))

    # Calculate key dates
    days25_paid_key_date = current_date + timedelta(days=25)
    two_days_to_end_trial_date = current_date + timedelta(days=2)
    days2_paid_key_date = current_date + timedelta(days=2)
    days25_paid_key_5sites_date = current_date + timedelta(days=25)

    # Format and output new date in format dd.mm.yyyy
    days25_paid_key_date = days25_paid_key_date.strftime("%d.%m.%Y")
    two_days_to_end_trial_date = two_days_to_end_trial_date.strftime("%d.%m.%Y")
    days2_paid_key_date = days2_paid_key_date.strftime("%d.%m.%Y")
    days25_paid_key_5sites_date = days25_paid_key_5sites_date.strftime("%d.%m.%Y")

    print(f"Set key {days25_paid_key_sites5} expiration date: {days25_paid_key_5sites_date}\n", f"https://cleantalk.org/noc/profile?user_id={days25_paid_key_sites5_user_id} \n")
    print(f"Set key {days25_paid_key} expiration date: {days25_paid_key_date}\n", f"https://cleantalk.org/noc/profile?user_id={days25_paid_key_user_id}\n")
    print(f"Set key {two_days_to_end_trial} expiration date: {two_days_to_end_trial_date}\n", f"https://cleantalk.org/noc/profile?user_id={two_days_to_end_trial_user_id}\n")
    print(f"Set key {two_days_to_end_paid} expiration date: {days2_paid_key_date}\n", f"https://cleantalk.org/noc/profile?user_id={two_days_to_end_paid_user_id}\n")

    print("\nChanges will be applied to the servers in 15 minutes !!!")
    print("\nDid you check the key expiration dates?! Otherwise, the tests may be incorrect. If yes, press Enter")
    input()
