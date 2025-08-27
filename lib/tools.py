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

        driver.refresh()
        time.sleep(3)

        if key:
            if wait_for_synchronization(driver):
                print("✅ Key synchronization completed")
                return True
            else:
                print("❌ Key synchronization failed")
                return False
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

def remove_dismissed_flags():
    print(config.BANNERS_TESTS_DB_HOST)
    print(config.BANNERS_TESTS_DB_NAME)
    print(config.BANNERS_TESTS_DB_USER)
    print(config.BANNERS_TESTS_DB_PASSWORD)
    print(config.BANNERS_TESTS_DB_PORT)
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
        sync_button = driver.find_element(By.ID, 'apbct_button__sync')

        if sync_button.get_attribute('disabled'):
            print("⚠️ Sync button is disabled, cannot click")
            return False

        print("🖱️ Clicking sync button...")
        sync_button.click()
        time.sleep(2)

        print("⏳ Waiting for sync to start...")
        sync_start_time = time.time()
        while time.time() - sync_start_time < timeout:
            sync_button = driver.find_element(By.ID, 'apbct_button__sync')
            if sync_button.get_attribute('disabled'):
                print("🔄 Synchronization started")
                break
            time.sleep(1)
        else:
            print("⏰ Timeout waiting for sync to start")
            return False

        print("⏳ Waiting for sync to complete...")
        while time.time() - start_time < timeout:
            sync_button = driver.find_element(By.ID, 'apbct_button__sync')

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
