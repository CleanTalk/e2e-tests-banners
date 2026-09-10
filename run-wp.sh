#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

PLUGIN_PATH="${PLUGIN_PATH:-}"
if [[ -z "$PLUGIN_PATH" ]]; then
  CANDIDATE="$(cd ../wordpress/wp-content/plugins/cleantalk-spam-protect 2>/dev/null && pwd || true)"
  if [[ -n "$CANDIDATE" && -f "$CANDIDATE/cleantalk.php" ]]; then
    PLUGIN_PATH="$CANDIDATE"
  fi
fi
if [[ -z "$PLUGIN_PATH" || ! -f "$PLUGIN_PATH/cleantalk.php" ]]; then
  echo "Set PLUGIN_PATH to the cleantalk-spam-protect directory" >&2
  exit 1
fi
export PLUGIN_PATH
echo "Plugin: $PLUGIN_PATH"

docker compose up -d

echo "Waiting for WordPress..."
for i in $(seq 1 30); do
  if curl -fsS "http://localhost:${WP_PORT:-8080}" >/dev/null 2>&1; then
    break
  fi
  sleep 2
done

WP_ID="$(docker ps -qf name=banners-e2e-wordpress)"
if [[ -z "$WP_ID" ]]; then
  echo "WordPress container is not running" >&2
  exit 1
fi

# wordpress:cli does not inherit WORDPRESS_DB_* from the WP container;
# wp-config falls back to host `mysql` without these env vars.
WP_CLI=(
  docker run --rm
  --volumes-from "$WP_ID"
  --network "container:$WP_ID"
  -e WORDPRESS_DB_HOST=db
  -e WORDPRESS_DB_USER=wordpress
  -e WORDPRESS_DB_PASSWORD=wordpress
  -e WORDPRESS_DB_NAME=wordpress
  wordpress:cli
)

if ! "${WP_CLI[@]}" wp core is-installed >/dev/null 2>&1; then
  "${WP_CLI[@]}" wp core install \
    --url="http://localhost:${WP_PORT:-8080}" \
    --title="Banners e2e" \
    --admin_user="admin" \
    --admin_password="password" \
    --admin_email="admin@example.com" \
    --skip-email
fi

"${WP_CLI[@]}" wp plugin activate cleantalk-spam-protect

"${WP_CLI[@]}" wp option delete ct_plugin_do_activation_redirect >/dev/null 2>&1 || true

echo "WordPress is ready at http://localhost:${WP_PORT:-8080} (admin / password)"
