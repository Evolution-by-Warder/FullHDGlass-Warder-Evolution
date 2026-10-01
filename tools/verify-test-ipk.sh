#!/bin/sh
set -eu

IPK="${1:-}"
EXPECTED_RUNTIME="${2:-1.0.5-test1}"
test -n "$IPK"
test -f "$IPK"
test -f "$IPK.sha256"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT HUP INT TERM

test "$(ar t "$IPK" | tr '\n' ' ')" = "debian-binary control.tar.gz data.tar.gz "
(
  cd "$TMP"
  ar x "$OLDPWD/$IPK"
)
test "$(cat "$TMP/debian-binary")" = "2.0"
(
  cd "$(dirname "$IPK")"
  sha256sum -c "$(basename "$IPK").sha256"
)

tar -xOzf "$TMP/control.tar.gz" ./control > "$TMP/control"
grep -Fx 'Package: enigma2-skin-fullhdglass17' "$TMP/control"
grep -Eq '^Version: 9\.50\+warder.*-test[0-9A-Za-z.-]*$' "$TMP/control"
CONTROL_VERSION="$(sed -n 's/^Version:[[:space:]]*//p' "$TMP/control" | head -n1)"
case "$CONTROL_VERSION" in
  *"warder$EXPECTED_RUNTIME") ;;
  *) echo "Control/runtime TEST version mismatch: $CONTROL_VERSION vs $EXPECTED_RUNTIME" >&2; exit 4 ;;
esac

tar -xOzf "$TMP/control.tar.gz" ./conffiles | grep -Fx '/etc/enigma2/skin_user-hdg17.xml'
for f in preinst postinst postrm; do
  tar -tzf "$TMP/control.tar.gz" | grep -Fx "./$f" >/dev/null
done

tar -tzf "$TMP/data.tar.gz" > "$TMP/payload"
grep -Fx './usr/share/enigma2/hd_glass17/skin.xml' "$TMP/payload" >/dev/null
grep -Fx './usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py' "$TMP/payload" >/dev/null
grep -Fx './usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/version' "$TMP/payload" >/dev/null
! grep -E '/(__pycache__/|[^/]+\.py[co]$)' "$TMP/payload"
ACTUAL_RUNTIME="$(tar -xOzf "$TMP/data.tar.gz" ./usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/version | tr -d '\r\n')"
test "$ACTUAL_RUNTIME" = "$EXPECTED_RUNTIME"

echo "TEST IPK integrity: PASS ($ACTUAL_RUNTIME)"
