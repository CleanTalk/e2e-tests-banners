# Cleantalk auto e2e banners check

Selenium checks Anti-Spam admin banners against a live WordPress with the plugin installed.

## How to use

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in DB / WP / API keys
3. Run:

```bash
python apbct_check_banners.py
```

CI (`CleanTalk/wordpress-antispam` workflow) uses this action at `@master` and real `BANNERS_TESTS_API_KEY_*` secrets.

## Run in a visible browser

Firefox window, 1.5s pause on each check so you can see the banners:

```bash
./run-headed.sh
```

Or:

```bash
export BANNERS_TESTS_HEADLESS=no
export BANNERS_TESTS_STEP_PAUSE=1.5
python apbct_check_banners.py
```

Needs Firefox and geckodriver on PATH.

Without the GitHub API-key secrets you can still see trial / review / renew UI (flags are written to `cleantalk_data`, no cloud sync):

```bash
export BANNERS_TESTS_INJECT_NOTICES=yes
./run-headed.sh
```

Do **not** set `BANNERS_TESTS_INJECT_NOTICES` in CI — missing secrets must fail the keyed stages.

## Local WordPress (optional)

From this repo, with the plugin checkout mounted:

```bash
export PLUGIN_PATH=/path/to/cleantalk-spam-protect
./run-wp.sh
./run-headed.sh
```

`run-wp.sh` starts WordPress on `http://localhost:8080` (DB on host port `3310`) and activates the plugin. Default admin is `admin` / `password`.

Do not point this at a production site: the script writes API keys in the database.

## Banner IDs expected by the tests

| Stage | Dashboard | Settings |
|---|---|---|
| Empty key | `cleantalk_notice_key_is_empty` | same |
| Review | `cleantalk_notice_review` | same |
| Trial expired | `cleantalk_notice_trial` | `cleantalk_trial_fullpage` |
| Paid expired | `cleantalk_notice_trial` (shared banner) | `cleantalk_trial_fullpage` |
