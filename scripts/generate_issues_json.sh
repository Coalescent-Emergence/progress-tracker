#!/usr/bin/env bash
set -euo pipefail

# Generates a sanitized issues JSON for the tracker and writes to docs/data/issues.json
# Expects env: OWNER (default Coalescent-Emergence), REPO (default Kerrigan), TOKEN (GitHub token)

OWNER="${OWNER:-Coalescent-Emergence}"
REPO="${REPO:-Kerrigan}"
TOKEN="${TOKEN:-}"
OUTDIR="docs/data"
OUTFILE="$OUTDIR/issues.json"

mkdir -p "$OUTDIR"

if ! command -v curl >/dev/null 2>&1; then
  echo "curl is required but not installed"
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required but not installed"
  exit 1
fi

TMPDIR=$(mktemp -d)
ALL_FILE="$TMPDIR/all.json"
echo '[]' > "$ALL_FILE"
PAGE=1

echo "Fetching issues for $OWNER/$REPO"
while :; do
  URL="https://api.github.com/repos/$OWNER/$REPO/issues?state=all&per_page=100&page=$PAGE"

  if [ -n "$TOKEN" ]; then
    HTTP_RESP_HEADERS="$TMPDIR/headers_$PAGE.txt"
    BODY_FILE="$TMPDIR/body_$PAGE.json"
    curl -sS -D "$HTTP_RESP_HEADERS" -H "Authorization: token $TOKEN" -H "Accept: application/vnd.github.v3+json" "$URL" -o "$BODY_FILE"
  else
    HTTP_RESP_HEADERS="$TMPDIR/headers_$PAGE.txt"
    BODY_FILE="$TMPDIR/body_$PAGE.json"
    curl -sS -D "$HTTP_RESP_HEADERS" -H "Accept: application/vnd.github.v3+json" "$URL" -o "$BODY_FILE"
  fi

  STATUS_CODE=$(awk 'toupper($1) ~ /^HTTP\// {code=$2} END {print code}' "$HTTP_RESP_HEADERS")
  if [ -z "$STATUS_CODE" ] || [ "$STATUS_CODE" -lt 200 ] || [ "$STATUS_CODE" -ge 300 ]; then
    MESSAGE=$(python3 - "$BODY_FILE" <<'PY'
import json
import sys

path = sys.argv[1]
try:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(data.get("message", "Unknown API error") if isinstance(data, dict) else "Unknown API error")
except Exception:
    print("Unknown API error")
PY
)
    echo "GitHub API request failed (HTTP ${STATUS_CODE:-unknown}) for $URL: $MESSAGE"
    exit 1
  fi

  # Filter out PRs and map to safe schema
  PAGE_FILTERED="$TMPDIR/filtered_$PAGE.json"
  python3 - "$BODY_FILE" "$PAGE_FILTERED" <<'PY'
import json
import sys

infile = sys.argv[1]
outfile = sys.argv[2]

with open(infile, "r", encoding="utf-8") as f:
    payload = json.load(f)

if not isinstance(payload, list):
    raise SystemExit("GitHub API payload is not a list")

filtered = []
for issue in payload:
    if not isinstance(issue, dict):
        continue
    if issue.get("pull_request") is not None:
        continue
    labels = issue.get("labels") or []
    label_names = []
    for label in labels:
        if isinstance(label, dict):
            name = label.get("name")
            if isinstance(name, str):
                label_names.append(name)

    filtered.append(
        {
            "number": issue.get("number"),
            "title": issue.get("title", ""),
            "state": issue.get("state", "open"),
            "labels": label_names,
            "html_url": issue.get("html_url", ""),
            "updated_at": issue.get("updated_at", ""),
        }
    )

with open(outfile, "w", encoding="utf-8") as f:
    json.dump(filtered, f, ensure_ascii=False)
PY

  # If empty array, break
  PAGE_COUNT=$(python3 - "$PAGE_FILTERED" <<'PY'
import json
import sys

with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = json.load(f)
print(len(data) if isinstance(data, list) else 0)
PY
)
  if [ "$PAGE_COUNT" -eq 0 ]; then
    break
  fi

  # Merge into all.json
  python3 - "$ALL_FILE" "$PAGE_FILTERED" "$TMPDIR/merged.json" <<'PY'
import json
import sys

all_file, page_file, out_file = sys.argv[1:4]

with open(all_file, "r", encoding="utf-8") as f:
    all_items = json.load(f)
with open(page_file, "r", encoding="utf-8") as f:
    page_items = json.load(f)

merged = list(all_items) + list(page_items)
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False)
PY
  mv "$TMPDIR/merged.json" "$ALL_FILE"

  # Check Link header for next
  if grep -qi '\brel="next"' "$HTTP_RESP_HEADERS"; then
    PAGE=$((PAGE+1))
    continue
  else
    break
  fi
done

# Final sanity: remove duplicates by number (keep latest updated_at)
python3 - "$ALL_FILE" "$OUTFILE" <<'PY'
import json
import sys

in_file, out_file = sys.argv[1:3]

with open(in_file, "r", encoding="utf-8") as f:
  data = json.load(f)

by_number = {}
for item in data:
  if not isinstance(item, dict):
    continue
  number = item.get("number")
  if not isinstance(number, int):
    continue
  existing = by_number.get(number)
  if existing is None or (item.get("updated_at", "") >= existing.get("updated_at", "")):
    by_number[number] = item

result = [by_number[n] for n in sorted(by_number.keys())]
with open(out_file, "w", encoding="utf-8") as f:
  json.dump(result, f, ensure_ascii=False, indent=2)
PY

COUNT=$(python3 - "$OUTFILE" <<'PY'
import json
import sys

with open(sys.argv[1], "r", encoding="utf-8") as f:
  data = json.load(f)
print(len(data) if isinstance(data, list) else 0)
PY
)

echo "Wrote $OUTFILE with $COUNT issues"

rm -rf "$TMPDIR"
