#!/bin/sh
set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
CONTROL="$ROOT/source/control"
PAYLOAD="$ROOT/source/package-root"
OUTDIR="$ROOT/packages/test"
VERSION_FILE="$PAYLOAD/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/version"

test -f "$CONTROL/control"
test -f "$VERSION_FILE"
test -d "$PAYLOAD"

PKG="$(sed -n 's/^Package:[[:space:]]*//p' "$CONTROL/control" | head -n1)"
PKGVER="$(sed -n 's/^Version:[[:space:]]*//p' "$CONTROL/control" | head -n1)"
RUNTIMEVER="$(tr -d '\r\n' < "$VERSION_FILE")"

case "$PKGVER" in
  *-test*) ;;
  *) echo "Refusing non-test package version: $PKGVER" >&2; exit 2 ;;
esac
case "$RUNTIMEVER" in
  *-test*) ;;
  *) echo "Refusing non-test runtime version: $RUNTIMEVER" >&2; exit 2 ;;
esac

test "$PKG" = "enigma2-skin-fullhdglass17"
EXPECTED_PKGVER="${RUNTIMEVER}-1"
case "$PKGVER" in
  "$EXPECTED_PKGVER") ;;
  *) echo "Control/runtime TEST package version mismatch: $PKGVER vs $EXPECTED_PKGVER" >&2; exit 2 ;;
esac

# opkg treats the final hyphen component as package revision. Keep a numeric
# revision after the visible TEST identity so OpenATV reports 1.0.5-testXX
# rather than reducing the visible version to 1.0.5.

# Compile gettext catalogs from authoritative PO sources before staging.
# This prevents stale MO files from hiding r10 language fixes on receivers.
command -v msgfmt >/dev/null 2>&1 || { echo "ERROR: msgfmt is required to build translated weather catalogs" >&2; exit 1; }
find "$PAYLOAD/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/locale" -type f -name '*.po' -print | sort | while IFS= read -r po; do
  msgfmt --check -o "${po%.po}.mo" "$po"
done

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT HUP INT TERM
mkdir -p "$WORK/CONTROL" "$OUTDIR"
cp -a "$PAYLOAD"/. "$WORK"/

# TEST93: build radio.mvi only from the approved package-owned production master.
# Never fall back to the retired synthetic generator: a missing/wrong master must fail CI.
RADIO_MASTER="$WORK/usr/share/enigma2/hd_glass17/warder-radio-background.jpg"
test -f "$RADIO_MASTER" || { echo "ERROR: approved TEST93 radio master missing: $RADIO_MASTER" >&2; exit 1; }
RADIO_MASTER_SHA256="2d1e26b6c097d167d51c8ba9850b16c093171ac07e69ef3d69f4cbd9cae4939d"
ACTUAL_RADIO_MASTER_SHA256="$(sha256sum "$RADIO_MASTER" | awk '{print $1}')"
test "$ACTUAL_RADIO_MASTER_SHA256" = "$RADIO_MASTER_SHA256" || {
  echo "ERROR: TEST93 radio master SHA-256 mismatch: $ACTUAL_RADIO_MASTER_SHA256" >&2
  exit 1
}
echo "TEST93 radio master SHA-256: PASS $ACTUAL_RADIO_MASTER_SHA256"
python3 - "$RADIO_MASTER" <<'PY'
from PIL import Image
import sys
path = sys.argv[1]
with Image.open(path) as image:
    if image.size != (1920, 1080):
        raise SystemExit("ERROR: TEST93 radio master must be exactly 1920x1080, got %sx%s" % image.size)
print("TEST93 radio master geometry: PASS 1920x1080")
PY

# TEST146: bake the opaque Radio text rails directly into the package master.
# This changes pixels in the base JPEG/radio.mvi; it does not create GUI masks or backing eLabels.
python3 - "$RADIO_MASTER" <<'PY'
from PIL import Image, ImageDraw
import sys
path = sys.argv[1]
with Image.open(path) as source:
    image = source.convert("RGB")
draw = ImageDraw.Draw(image)
# Preserve the existing thin rail outlines by filling just inside them.
draw.rounded_rectangle((29, 17, 1891, 101), radius=8, fill=(0, 0, 0))
draw.rounded_rectangle((29, 815, 1891, 1033), radius=8, fill=(0, 0, 0))
image.save(path, "JPEG", quality=95, subsampling=0)
print("TEST146 baked opaque Radio rails into base master: PASS")
PY
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: ffmpeg is required for Warder radio.mvi" >&2; exit 1; }
ffmpeg -y -loglevel error \
    -i "$RADIO_MASTER" \
    -frames:v 1 -c:v mpeg2video -q:v 5 -f mpeg2video \
    "$WORK/usr/share/enigma2/hd_glass17/radio.mvi"

# r12 parity: ship the Enhanced Weather SK/CZ database alongside the Classic
# Weather database. It is deterministically derived from city_Code-17.txt so
# both databases stay synchronized without maintaining duplicate source data.
python3 "$ROOT/tools/generate-ewea-city.py" \
    "$PAYLOAD/etc/city_Code-17.txt" "$WORK/etc/ewea_city_Code-17.txt"

cp "$CONTROL/control" "$WORK/CONTROL/control"
for f in conffiles preinst postinst postrm; do
  if [ -f "$CONTROL/$f" ]; then
    cp "$CONTROL/$f" "$WORK/CONTROL/$f"
  fi
done
chmod 0755 "$WORK/CONTROL/preinst" "$WORK/CONTROL/postinst" "$WORK/CONTROL/postrm" 2>/dev/null || true
chmod 0644 "$WORK/CONTROL/control" "$WORK/CONTROL/conffiles" 2>/dev/null || true

if find "$WORK" -type d -name __pycache__ -print -quit | grep -q . || find "$WORK" -type f \( -name '*.pyc' -o -name '*.pyo' \) -print -quit | grep -q .; then
  echo "Refusing package containing Python bytecode artifacts." >&2
  exit 3
fi

OUT="$OUTDIR/enigma2-skin-fullhdglass17-warder-evolution_${RUNTIMEVER}_all.ipk"
BUILD="$WORK/.ipk-build"
mkdir -p "$BUILD"
printf '2.0\\n' > "$BUILD/debian-binary"
(
  cd "$WORK/CONTROL"
  tar --format=gnu --owner=0 --group=0 --numeric-owner -czf "$BUILD/control.tar.gz" .
)
(
  cd "$WORK"
  tar --format=gnu --owner=0 --group=0 --numeric-owner --exclude='./CONTROL' --exclude='./.ipk-build' -czf "$BUILD/data.tar.gz" .
)
rm -f "$OUT"
(
  cd "$BUILD"
  ar rcs "$OUT" debian-binary control.tar.gz data.tar.gz
)

test "$(ar t "$OUT" | tr '\n' ' ')" = "debian-binary control.tar.gz data.tar.gz "
(
  cd "$OUTDIR"
  sha256sum "$(basename "$OUT")" > "$(basename "$OUT").sha256"
)
echo "Built TEST package only:"
cat "$OUT.sha256"
