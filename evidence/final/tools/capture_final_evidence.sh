#!/bin/bash
set -euo pipefail

export PYTHONDONTWRITEBYTECODE=1

APP_URL="${1:-}"
if [[ -z "$APP_URL" ]]; then
  echo "Usage: $0 <application-url>"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
OUTPUT_DIR="$REPO_ROOT/evidence/final"
WORK_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/secureflow-final-capture.XXXXXX")"
PW_NODE="$HOME/.cache/secureflow-playwright-system-chrome/node"

cleanup() {
  rm -rf "$WORK_ROOT"
}
trap cleanup EXIT

if [[ ! -d "$PW_NODE/node_modules/playwright" ]]; then
  echo "Stable Playwright runtime is missing: $PW_NODE"
  exit 1
fi

rm -f \
  "$OUTPUT_DIR"/01-application-overview.png \
  "$OUTPUT_DIR"/02-security-pipeline.png \
  "$OUTPUT_DIR"/03-assessment-findings.png \
  "$OUTPUT_DIR"/04-remediation-retest.png \
  "$OUTPUT_DIR"/05-detection-investigation.png \
  "$OUTPUT_DIR"/06-governance-recovery.png

PAGES_DIR="$WORK_ROOT/pages"
mkdir -p "$PAGES_DIR"

python3 "$SCRIPT_DIR/build_final_pages.py" \
  --root "$REPO_ROOT" \
  --output "$PAGES_DIR"

NODE_PATH="$PW_NODE/node_modules" \
  node "$SCRIPT_DIR/capture.cjs" \
    "$APP_URL" \
    "$PAGES_DIR" \
    "$OUTPUT_DIR"

echo "Final evidence capture completed."
