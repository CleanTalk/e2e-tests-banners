#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

export BANNERS_TESTS_HEADLESS="${BANNERS_TESTS_HEADLESS:-no}"
export BANNERS_TESTS_STEP_PAUSE="${BANNERS_TESTS_STEP_PAUSE:-1.5}"

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
  export BANNERS_TESTS_HEADLESS="${BANNERS_TESTS_HEADLESS:-no}"
fi

if [[ -x .venv/bin/python ]] && .venv/bin/python -c 'import selenium' 2>/dev/null; then
  echo "Running banners e2e headed with .venv Python"
  exec .venv/bin/python apbct_check_banners.py
fi

if command -v python3 >/dev/null 2>&1 && python3 -c 'import selenium' 2>/dev/null; then
  echo "Running banners e2e headed with python3"
  exec python3 apbct_check_banners.py
fi

if docker image inspect banners-e2e:local >/dev/null 2>&1; then
  echo "Running banners e2e headed in Docker (Firefox on DISPLAY=${DISPLAY:-:0})"
  if command -v xhost >/dev/null 2>&1; then
    xhost +local: >/dev/null 2>&1 || true
  fi
  DOCKER_ENV=()
  if [[ -f .env ]]; then
    DOCKER_ENV+=(--env-file .env)
  fi
  exec docker run --rm --network host --ipc=host \
    --user "$(id -u):$(id -g)" \
    --security-opt seccomp=unconfined \
    "${DOCKER_ENV[@]}" \
    -e HOME=/tmp \
    -e DISPLAY \
    -e PYTHONPATH=/app \
    -e BANNERS_TESTS_HEADLESS \
    -e BANNERS_TESTS_STEP_PAUSE \
    -e MOZ_DISABLE_CONTENT_SANDBOX=1 \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v "$PWD:/app" -w /app \
    banners-e2e:local python apbct_check_banners.py
fi

echo "Install selenium (venv) or build image banners-e2e:local" >&2
exit 1
