#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

# Prefer the compatible Homebrew runtime without changing the user's shell.
if [[ -x /opt/homebrew/opt/ruby@3.3/bin/ruby ]]; then
  export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH"
fi
export BUNDLE_PATH="${BUNDLE_PATH:-$PWD/vendor/bundle}"
exec bundle exec jekyll "$@"
