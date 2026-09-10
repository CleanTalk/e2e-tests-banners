from dotenv import load_dotenv
import os

load_dotenv()

def _env_flag(name, default='no'):
    value = os.getenv(name, default)
    return 'yes' if str(value).strip().lower() in ('1', 'yes', 'true', 'on') else 'no'

# Database settings
BANNERS_TESTS_DB_HOST = os.getenv('BANNERS_TESTS_DB_HOST', '127.0.0.1')
BANNERS_TESTS_DB_NAME = os.getenv('BANNERS_TESTS_DB_NAME', 'wordpress')
BANNERS_TESTS_DB_USER = os.getenv('BANNERS_TESTS_DB_USER', 'wordpress')
BANNERS_TESTS_DB_PASSWORD = os.getenv('BANNERS_TESTS_DB_PASSWORD', 'wordpress')
BANNERS_TESTS_DB_PORT = os.getenv('BANNERS_TESTS_DB_PORT', '3306')

BANNERS_TESTS_HEADLESS = _env_flag('BANNERS_TESTS_HEADLESS', 'yes')
BANNERS_TESTS_JS_ON = _env_flag('BANNERS_TESTS_JS_ON', 'yes')
BANNERS_TESTS_REGULAR_TIMEOUT = int(os.getenv('BANNERS_TESTS_REGULAR_TIMEOUT', 10))
BANNERS_TESTS_STEP_PAUSE = float(os.getenv(
    'BANNERS_TESTS_STEP_PAUSE',
    '1.5' if _env_flag('BANNERS_TESTS_HEADLESS', 'yes') == 'no' else '0'
))
# Local-only: show trial/review/renew banners from DB flags when API keys are empty.
# Do not set this in CI — missing secrets must fail the keyed stages.
BANNERS_TESTS_INJECT_NOTICES = _env_flag('BANNERS_TESTS_INJECT_NOTICES', 'no')

BANNERS_TESTS_URL = os.getenv('BANNERS_TESTS_URL', 'http://localhost:8080').rstrip('/')
BANNERS_TESTS_AUTH_LOGIN = os.getenv('BANNERS_TESTS_AUTH_LOGIN', 'admin')
BANNERS_TESTS_AUTH_PASS = os.getenv('BANNERS_TESTS_AUTH_PASS', 'password')
BANNERS_TESTS_SETTINGS_URL = BANNERS_TESTS_URL + '/wp-admin/options-general.php?page=cleantalk'
BANNERS_TESTS_PLUGINS_URL = BANNERS_TESTS_URL + '/wp-admin/plugins.php'

BANNERS_TESTS_API_KEY_REGULAR = os.getenv('BANNERS_TESTS_API_KEY_REGULAR', '')
BANNERS_TESTS_API_KEY_REVIEW = os.getenv('BANNERS_TESTS_API_KEY_REVIEW', '')
BANNERS_TESTS_API_KEY_TRIAL_EXPIRED = os.getenv('BANNERS_TESTS_API_KEY_TRIAL_EXPIRED', '')
BANNERS_TESTS_API_KEY_PAID_EXPIRED = os.getenv('BANNERS_TESTS_API_KEY_PAID_EXPIRED', '')
