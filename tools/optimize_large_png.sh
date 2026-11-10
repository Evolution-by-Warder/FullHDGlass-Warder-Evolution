#!/usr/bin/env bash
# Fast, lossless pass over bundled PNGs; keep only files that become smaller.
set -euo pipefail
ROOT="${1:-source/package-root}"
LIMIT="${LIMIT:-25}"
MIN_BYTES="${MIN_BYTES:-102400}"
if ! command -v optipng >/dev/null 2>&1; then echo "optipng is required" >&2; exit 1; fi
if [[ ! -d "$ROOT" ]]; then echo "Missing path: $ROOT" >&2; exit 1; fi
before=0; after=0; changed=0; tested=0
while IFS= read -r -d '' file; do
  old=$(stat -c%s "$file")
  (( old >= MIN_BYTES )) || continue
  (( tested += 1 ))
  tmp=$(mktemp --suffix=.png)
  cp "$file" "$tmp"
  # -o1 is intentionally fast. Default handling preserves PNG metadata and alpha.
  if optipng -o1 -quiet "$tmp" >/dev/null 2>&1; then
    new=$(stat -c%s "$tmp")
    if (( new < old )); then
      # Pixel equality: compare decoded RGBA data, not merely file checksum.
      if python3 - "$file" "$tmp" <<'PY'
import sys
from PIL import Image
with Image.open(sys.argv[1]) as a, Image.open(sys.argv[2]) as b:
    assert a.size == b.size and a.convert("RGBA").tobytes() == b.convert("RGBA").tobytes()
PY
      then
        cat "$tmp" > "$file"
        (( changed += 1 ))
        (( before += old ))
        (( after += new ))
        printf '%s : %s -> %s bytes\n' "$file" "$old" "$new"
      fi
    fi
  fi
  rm -f "$tmp"
done < <(find "$ROOT" -type f -iname '*.png' -size +100k -printf '%s\t%p\0' | sort -zrn | sed -z -n "1,${LIMIT}p" | cut -z -f2-)
printf 'Checked: %s; optimized: %s; saved: %s bytes\n' "$tested" "$changed" "$(( before - after ))"
