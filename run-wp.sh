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

if ! docker run --rm --volumes-from "$WP_ID" --network "container:$WP_ID" wordpress:cli wp core is-installed >/dev/null 2>&1; then
  docker run --rm \
    --volumes-from "$WP_ID" \
    --network "container:$WP_ID" \
    wordpress:cli wp core install \
      --url="http://localhost:${WP_PORT:-8080}" \
      --title="Banners e2e" \
      --admin_user="admin" \
      --admin_password="password" \
      --admin_email="admin@example.com" \
      --skip-email
fi

docker run --rm \
  --volumes-from "$WP_ID" \
  --network "container:$WP_ID" \
  wordpress:cli wp plugin activate cleantalk-spam-protect

docker run --rm \
  --volumes-from "$WP_ID" \
  --network "container:$WP_ID" \
  wordpress:cli wp option delete ct_plugin_do_activation_redirect >/dev/null 2>&1 || true

echo "WordPress is ready at http://localhost:${WP_PORT:-8080} (admin / password)"
