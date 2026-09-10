import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from lib.browser_init import driver as browser_driver

import MySQLdb
from MySQLdb import Error
import phpserialize
import config

# Set key
def set_key(key='', driver_instance=None, skip_sync=False):
    driver = driver_instance if driver_instance is not None else browser_driver

    skip_activation_redirect()
    ensure_plugin_activated(driver)

    if 'signup_wizard=1' in driver.current_url or driver.current_url != config.BANNERS_TESTS_SETTINGS_URL:
        print("[LOG] Reload page")
        driver.get(config.BANNERS_TESTS_SETTINGS_URL)

    print(f"🔑 Setting key: {mask_string(key)}")

    if set_key_via_database(key):
        print("✅ Key set via database")
        # Drop leftover trial/renew flags so the settings wrap (and Sync) stay visible.
        # Sequential stages otherwise inherit the previous key's fullpage banner.
        set_data_flags_via_database({
            'key_is_ok': 1,
            'notice_trial': 0,
            'notice_renew': 0,
            'notice_review': 0,
            'notice_show': 0,
        })

        driver.refresh()
        time.sleep(3)

        if key and not skip_sync:
            if wait_for_synchronization(driver):
                print("✅ Key synchronization completed")
                return True
            print("❌ Key synchronization failed")
            return False
        return True
    print("❌ Failed to set key via database")
    return False


# Get page source code
def get_page_source(driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver
    code = driver.find_element(By.XPATH, '/html/body')
    return code.get_attribute("outerHTML")


# Move browser view to the element
def align_center(form_element, driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver
    element1 = driver.find_element(By.ID, form_element)
    desired_y = (element1.size['height'] / 2) + element1.location['y']
    current_y = (driver.execute_script('return window.innerHeight') / 2) + driver.execute_script('return window.pageYOffset')
    scroll_y_by = desired_y - current_y
    driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)

def skip_activation_redirect():
    try:
        connection = _db_connect()
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM wp_options WHERE option_name = 'ct_plugin_do_activation_redirect'"
            )
            connection.commit()
        return True
    except Exception as e:
        print(f"❌ Failed to skip activation redirect: {e}")
        return False
    finally:
        try:
            connection.close()
        except Exception:
            pass


def ensure_plugin_activated(driver):
    skip_activation_redirect()
    driver.get(config.BANNERS_TESTS_PLUGINS_URL)
    if 'signup_wizard=1' in driver.current_url:
        driver.get(config.BANNERS_TESTS_PLUGINS_URL)
    try:
        # Locate CleanTalk plugin row by its data-slug attribute
        plugin_row = WebDriverWait(driver, config.BANNERS_TESTS_REGULAR_TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, '//tr[contains(@data-slug, "cleantalk-spam-protect")]'))
        )

        # Check if plugin is inactive
        if "Activate" in plugin_row.text:
            # Click "Activate" link (supports multilingual UI)
            activate_button = plugin_row.find_element(
                By.XPATH,
                './/a[contains(@href, "action=activate") and (contains(text(), "Activate") or contains(text(), "Активировать"))]'
            )
            activate_button.click()

            # Wait for success notification
            WebDriverWait(driver, config.BANNERS_TESTS_REGULAR_TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "notice-success")]'))
            )
            print("[OK] Plugin activated successfully.")
        else:
            print("[INFO] Plugin already active.")

    except Exception as e:
        raise Exception(f"Plugin activation failed: {e}. Is CleanTalk installed?")

def _db_connect():
    return MySQLdb.connect(
        host=config.BANNERS_TESTS_DB_HOST,
        database=config.BANNERS_TESTS_DB_NAME,
        user=config.BANNERS_TESTS_DB_USER,
        password=config.BANNERS_TESTS_DB_PASSWORD,
        port=int(config.BANNERS_TESTS_DB_PORT),
        charset='utf8mb4'
    )


def remove_dismissed_flags():
    try:
        connection = _db_connect()
        with connection.cursor() as cursor:
            delete_query = """
            DELETE FROM wp_options
            WHERE option_name LIKE 'cleantalk\\_%\\_dismissed'
            OR option_name LIKE 'cleantalk%dismissed'
            """

            cursor.execute(delete_query)
            deleted_count = cursor.rowcount
            connection.commit()

            if deleted_count > 0:
                print(f"✅ Successfully removed {deleted_count} dismissed options")
            else:
                print("✅ No cleantalk_*_dismissed options found")

            return True

    except Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        if connection:
            connection.close()

def set_key_via_database(key_value):
    try:
        connection = _db_connect()
        with connection.cursor() as cursor:
            select_query = """
            SELECT option_value
            FROM wp_options
            WHERE option_name = 'cleantalk_settings'
            """

            cursor.execute(select_query)
            result = cursor.fetchone()

            if not result:
                print("❌ cleantalk_settings not found in database")
                return False

            current_settings = result[0]

            updated_settings = update_key_in_settings(current_settings, 'apikey', key_value)

            update_query = """
            UPDATE wp_options
            SET option_value = %s
            WHERE option_name = 'cleantalk_settings'
            """

            cursor.execute(update_query, (updated_settings,))
            connection.commit()

            return True

    except Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        if connection:
            connection.close()

def set_data_flags_via_database(flags):
    try:
        connection = _db_connect()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT option_value FROM wp_options WHERE option_name = 'cleantalk_data'"
            )
            result = cursor.fetchone()

            if not result:
                print("❌ cleantalk_data not found in database")
                return False

            updated_data = result[0]
            for key, value in flags.items():
                updated_data = update_key_in_settings(updated_data, key, value)

            cursor.execute(
                "UPDATE wp_options SET option_value = %s WHERE option_name = 'cleantalk_data'",
                (updated_data,)
            )
            connection.commit()
            print(f"✅ Data flags set: {flags}")
            return True
    except Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        try:
            connection.close()
        except Exception:
            pass


def set_key_is_ok_via_database():
    return set_data_flags_via_database({'key_is_ok': 1})

def update_key_in_settings(settings_serialized, key, value):
    try:
        settings_dict = phpserialize.loads(settings_serialized.encode('utf-8'), decode_strings=True)

        if isinstance(settings_dict, dict):
            settings_dict[key] = value
        else:
            return settings_serialized

        updated_settings = phpserialize.dumps(settings_dict).decode('utf-8')

        return updated_settings

    except Exception as e:
        print(f"❌ Error processing settings with phpserialize: {e}")

def wait_for_synchronization(driver, timeout=60):
    print("⏳ Waiting for synchronization...")

    start_time = time.time()

    try:
        sync_button = WebDriverWait(driver, config.BANNERS_TESTS_REGULAR_TIMEOUT).until(
            EC.presence_of_element_located((By.ID, 'apbct_button__sync'))
        )

        if sync_button.get_attribute('disabled'):
            print("⚠️ Sync button is disabled, cannot click")
            return False

        print("🖱️ Clicking sync button...")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sync_button)
        try:
            sync_button.click()
        except Exception:
            driver.execute_script("arguments[0].click();", sync_button)
        time.sleep(2)

        print("⏳ Waiting for sync to start...")
        sync_start_time = time.time()
        while time.time() - sync_start_time < timeout:
            try:
                sync_button = driver.find_element(By.ID, 'apbct_button__sync')
            except NoSuchElementException:
                print("✅ Sync button gone after click (fullpage banner replaced settings)")
                return True
            if sync_button.get_attribute('disabled'):
                print("🔄 Synchronization started")
                break
            time.sleep(1)
        else:
            print("⏰ Timeout waiting for sync to start")
            return False

        print("⏳ Waiting for sync to complete...")
        while time.time() - start_time < timeout:
            try:
                sync_button = driver.find_element(By.ID, 'apbct_button__sync')
            except NoSuchElementException:
                print("✅ Synchronization completed (settings replaced by banner)")
                return True

            if not sync_button.get_attribute('disabled'):
                print("✅ Synchronization completed successfully")
                wait_for_post_sync_reload(driver, sync_button)
                return True

            time.sleep(2)

    except NoSuchElementException:
        print("❌ Sync button not found")
        return False
    except TimeoutException:
        print("❌ Sync button not found")
        return False
    except Exception as e:
        print(f"❌ Sync error: {e}")
        return False

    print("⏰ Synchronization timeout")
    return False


def wait_for_post_sync_reload(driver, sync_button, timeout=15):
    """The plugin reloads settings when sync returns {reload: true}. Wait that out."""
    print("⏳ Waiting for post-sync page reload...")
    try:
        WebDriverWait(driver, timeout).until(EC.staleness_of(sync_button))
        print("✅ Settings page reloaded after sync")
    except TimeoutException:
        print("[LOG] No post-sync reload")
        return
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
    except TimeoutException:
        pass


def _flag_int(value):
    if value is True:
        return 1
    if value is False:
        return 0
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def get_data_flags_via_database(keys):
    connection = None
    try:
        connection = _db_connect()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT option_value FROM wp_options WHERE option_name = 'cleantalk_data'"
            )
            result = cursor.fetchone()
        if not result:
            return None
        data = phpserialize.loads(result[0].encode('utf-8'), decode_strings=True)
        if not isinstance(data, dict):
            return None
        return {key: _flag_int(data.get(key)) for key in keys}
    except Exception as e:
        print(f"❌ Failed to read data flags: {e}")
        return None
    finally:
        try:
            if connection:
                connection.close()
        except Exception:
            pass


def wait_until_data_flags(expected, timeout=30):
    """Wait until cloud sync has written the expected notice flags to the DB."""
    print(f"⏳ Waiting for cloud flags in DB: {expected}")
    start_time = time.time()
    last = None
    while time.time() - start_time < timeout:
        last = get_data_flags_via_database(expected.keys())
        if last is not None and all(_flag_int(last.get(key)) == _flag_int(value) for key, value in expected.items()):
            print(f"✅ Cloud flags in DB: {last}")
            return True
        time.sleep(1)
    print(f"[ALARM] Timed out waiting for flags {expected}, last={last}")
    return False

def mask_string(input_string):
    if not input_string:
        return "empty"
    return "*" * 16 + input_string[-2:]


def is_usable_api_key(api_key):
    if not api_key or not str(api_key).strip():
        return False
    return str(api_key).strip().upper() not in (
        'YOUR_API_KEY',
        'CHANGE_ME',
        'TODO',
        'XXX',
        'NONE',
    )


def prepare_banner_stage(api_key, inject_flags, dummy_key, driver):
    """Use a real key + cloud sync, or inject notice flags for a local headed run."""
    skip_activation_redirect()
    remove_dismissed_flags()

    if is_usable_api_key(api_key):
        if not set_key(api_key, driver):
            return False
        return wait_until_data_flags(inject_flags)

    if config.BANNERS_TESTS_INJECT_NOTICES == 'yes':
        print(f"[LOG] No API key, injecting notices {inject_flags}")
        if not set_key(dummy_key, driver, skip_sync=True):
            return False
        return set_data_flags_via_database(inject_flags)

    print("[ALARM] API key is empty and BANNERS_TESTS_INJECT_NOTICES is not enabled")
    return False
