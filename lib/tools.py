import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from lib.browser_init import driver as browser_driver

import MySQLdb
from MySQLdb import Error
import phpserialize
import config

# Set key
def set_key(key = '', driver_instance=None):
    driver = driver_instance if driver_instance is not None else browser_driver

    ensure_plugin_activated(driver)

    if driver.current_url != config.BANNERS_TESTS_SETTINGS_URL:
        print("[LOG] Reload page")
        driver.get(config.BANNERS_TESTS_SETTINGS_URL)

    print(f"🔑 Setting key: {mask_string(key)}")

    if set_key_via_database(key):
        print("✅ Key set via database")
        set_key_is_ok_via_database()

        driver.refresh()
        time.sleep(3)
    else:
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

def ensure_plugin_activated(driver):
    driver.get(config.BANNERS_TESTS_PLUGINS_URL)
    try:
        # Locate CleanTalk plugin row by its data-slug attribute
        plugin_row = WebDriverWait(driver, config.BANNERS_TESTS_REGULAR_TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, '//tr[contains(@data-slug, "security-malware-firewall")]'))
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
        raise Exception(f"Plugin activation failed: {e}. Is SPBCT installed?")

def remove_dismissed_flags():
    try:
        db_config = {
            'host': config.BANNERS_TESTS_DB_HOST,
            'database': config.BANNERS_TESTS_DB_NAME,
            'user': config.BANNERS_TESTS_DB_USER,
            'password': config.BANNERS_TESTS_DB_PASSWORD,
            'port': int(config.BANNERS_TESTS_DB_PORT),
            'charset': 'utf8mb4'
        }

        connection = MySQLdb.connect(**db_config)
        with connection.cursor() as cursor:
            select_query = """
            SELECT option_value
            FROM wp_options
            WHERE option_name = 'spbc_data'
            """

            cursor.execute(select_query)
            result = cursor.fetchone()

            if not result:
                print("❌ spbc_data not found in database")
                return False

            current_data = result[0]

            updated_data = update_key_in_settings(current_data, 'dismissed_banners', [])

            if current_data != updated_data:
                print(f"✅ Data updated: dismissed_banners has been updated")
            else:
                print(f"ℹ️ No changes: dismissed_banners not modified")

            update_query = """
            UPDATE wp_options
            SET option_value = %s
            WHERE option_name = 'spbc_data'
            """

            cursor.execute(update_query, (updated_data,))
            connection.commit()

            delete_query = """
            DELETE FROM wp_options
            WHERE option_name LIKE 'spbc_empty_key\\_%'
            OR option_name LIKE 'spbc_review\\_%'
            OR option_name LIKE 'spbc_trial\\_%'
            OR option_name LIKE 'spbc_renew\\_%'
            """

            cursor.execute(delete_query)
            connection.commit()

            print(f"✅ Dismissed flags reset successfully!")

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
        db_config = {
            'host': config.BANNERS_TESTS_DB_HOST,
            'database': config.BANNERS_TESTS_DB_NAME,
            'user': config.BANNERS_TESTS_DB_USER,
            'password': config.BANNERS_TESTS_DB_PASSWORD,
            'port': int(config.BANNERS_TESTS_DB_PORT),
            'charset': 'utf8mb4'
        }

        connection = MySQLdb.connect(**db_config)
        with connection.cursor() as cursor:
            select_query = """
            SELECT option_value
            FROM wp_options
            WHERE option_name = 'spbc_settings'
            """

            cursor.execute(select_query)
            result = cursor.fetchone()

            if not result:
                print("❌ spbc_settings not found in database")
                return False

            current_settings = result[0]

            updated_settings = update_key_in_settings(current_settings, 'spbc_key', key_value)

            update_query = """
            UPDATE wp_options
            SET option_value = %s
            WHERE option_name = 'spbc_settings'
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

def set_key_is_ok_via_database():
    try:
        db_config = {
            'host': config.BANNERS_TESTS_DB_HOST,
            'database': config.BANNERS_TESTS_DB_NAME,
            'user': config.BANNERS_TESTS_DB_USER,
            'password': config.BANNERS_TESTS_DB_PASSWORD,
            'port': int(config.BANNERS_TESTS_DB_PORT),
            'charset': 'utf8mb4'
        }

        connection = MySQLdb.connect(**db_config)
        with connection.cursor() as cursor:
            select_query = """
            SELECT option_value
            FROM wp_options
            WHERE option_name = 'spbc_data'
            """

            cursor.execute(select_query)
            result = cursor.fetchone()

            if not result:
                print("❌ cleantalk_data not found in database")
                return False

            current_data = result[0]

            updated_data = update_key_in_settings(current_data, 'key_is_ok', 1)

            update_query = """
            UPDATE wp_options
            SET option_value = %s
            WHERE option_name = 'spbc_data'
            """

            cursor.execute(update_query, (updated_data,))
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

def set_notice_via_database(notice_name, notice_value):
    try:
        db_config = {
            'host': config.BANNERS_TESTS_DB_HOST,
            'database': config.BANNERS_TESTS_DB_NAME,
            'user': config.BANNERS_TESTS_DB_USER,
            'password': config.BANNERS_TESTS_DB_PASSWORD,
            'port': int(config.BANNERS_TESTS_DB_PORT),
            'charset': 'utf8mb4'
        }

        connection = MySQLdb.connect(**db_config)
        with connection.cursor() as cursor:
            select_query = """
            SELECT option_value
            FROM wp_options
            WHERE option_name = 'spbc_data'
            """

            cursor.execute(select_query)
            result = cursor.fetchone()

            if not result:
                print("❌ cleantalk_data not found in database")
                return False

            current_data = result[0]

            updated_data = update_key_in_settings(current_data, notice_name, notice_value)

            update_query = """
            UPDATE wp_options
            SET option_value = %s
            WHERE option_name = 'spbc_data'
            """

            cursor.execute(update_query, (updated_data,))
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

def update_key_in_settings(settings_serialized, key, value):
    try:
        def object_hook(obj, additional_arg=None):
            if hasattr(obj, '__PHP_Incomplete_Class_Name'):
                result = {}
                for prop_key, prop_value in obj.items():
                    if not prop_key.startswith('__PHP_Incomplete_Class'):
                        clean_key = prop_key.split('\x00')[-1] if '\x00' in prop_key else prop_key
                        result[clean_key] = prop_value
                return result
            return obj

        settings_dict = phpserialize.loads(
            settings_serialized.encode('utf-8'),
            object_hook=object_hook,
            decode_strings=True
        )

        if isinstance(settings_dict, dict):
            settings_dict[key] = value
        else:
            return settings_serialized

        return phpserialize.dumps(settings_dict).decode('utf-8')

    except Exception as e:
        print(f"❌ Error: {e}")
        return settings_serialized

def wait_for_synchronization(driver, timeout=60):
    print("⏳ Waiting for synchronization...")

    start_time = time.time()

    try:
        sync_button = driver.find_element(By.ID, 'spbc_button__sync_regular')

        if sync_button.get_attribute('disabled'):
            print("⚠️ Sync button is disabled, cannot click")
            return False

        print("🖱️ Clicking sync button...")
        sync_button.click()
        time.sleep(2)

        print("⏳ Waiting for sync to start...")
        sync_start_time = time.time()
        while time.time() - sync_start_time < timeout:
            sync_button = driver.find_element(By.ID, 'spbc_button__sync_regular')
            if sync_button.get_attribute('disabled'):
                print("🔄 Synchronization started")
                break
            time.sleep(1)
        else:
            print("⏰ Timeout waiting for sync to start")
            return False

        print("⏳ Waiting for sync to complete...")
        while time.time() - start_time < timeout:
            sync_button = driver.find_element(By.ID, 'spbc_button__sync_regular')

            if not sync_button.get_attribute('disabled'):
                print("✅ Synchronization completed successfully")
                return True

            time.sleep(2)

    except NoSuchElementException:
        print("❌ Sync button not found")
        return False

    except Exception as e:
        print(f"❌ Sync error: {e}")
        return False

    print("⏰ Synchronization timeout")
    return False

def mask_string(input_string):
    if not input_string:
        return "empty"
    return "*" * 16 + input_string[-2:]
