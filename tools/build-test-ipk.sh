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

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT HUP INT TERM
mkdir -p "$WORK/CONTROL" "$OUTDIR"
cp -a "$PAYLOAD"/. "$WORK"/
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
if command -v opkg-build >/dev/null 2>&1; then
  opkg-build "$WORK" "$OUT"
elif command -v dpkg-deb >/dev/null 2>&1; then
  dpkg-deb --build --root-owner-group "$WORK" "$OUT"
else
  echo "Need opkg-build or dpkg-deb to build the test IPK." >&2
  exit 4
fi

sha256sum "$OUT" > "$OUT.sha256"
echo "Built TEST package only:"
cat "$OUT.sha256"
