#!/bin/sh
set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
CONTROL="$ROOT/source/control"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT HUP INT TERM

fail() { echo "FAIL: $*" >&2; exit 1; }

# Static destructive-operation guardrails.
for f in preinst postinst postrm; do
  test -f "$CONTROL/$f" || fail "missing $f"
  sh -n "$CONTROL/$f"
done

! grep -REn 'rm[[:space:]]+-rf[[:space:]]+/(etc|usr/share/enigma2|usr/lib/enigma2)' "$CONTROL" || fail "broad destructive rm found"
grep -F "config.misc.ButtonSetup.epg=Infobar/openGraphEPG" "$CONTROL/postinst" >/dev/null || fail "missing fresh-install EPG default"
grep -F "^config.misc.ButtonSetup.epg=" "$CONTROL/postinst" >/dev/null || fail "missing explicit EPG-presence guard"
! grep -REn 'ButtonSetup\.info|sed.*settings|rm.*settings|mv.*settings' "$CONTROL" || fail "unrelated or whole-settings mutation found"
! grep -REn 'skin_default/spinner.*(rm|mv|ln)|(^|[;&|[:space:]])(rm|mv|ln)[[:space:]].*skin_default/spinner' "$CONTROL" || fail "spinner mutation in lifecycle scripts"

grep -Fx '/etc/enigma2/skin_user-hdg17.xml' "$CONTROL/conffiles" >/dev/null || fail "missing conffile"

# postrm upgrade-family states must exit before any restore/cleanup body.
python3 - "$CONTROL/postrm" <<'PY'
import pathlib, sys
p = pathlib.Path(sys.argv[1]).read_text()
case = p.find('case "${1:-}" in')
restore = p.find('restore_backup')
if case < 0 or restore < 0 or case > restore:
    raise SystemExit("postrm upgrade guard must precede restore cleanup")
for state in ("upgrade", "failed-upgrade", "abort-upgrade", "disappear"):
    if state not in p[:restore]:
        raise SystemExit("missing guarded state: " + state)
print("Lifecycle static semantics: PASS")
PY

echo "Package lifecycle guardrail test: PASS"

# Exercise the real lifecycle scripts with absolute system paths redirected into
# a temporary root, without touching receiver/system configuration.
SIM="$TMP/sim"
mkdir -p "$SIM/etc/enigma2" "$SIM/usr/share/enigma2" "$SIM/usr/lib/enigma2/python" "$SIM/tmp"
python3 - "$CONTROL" "$SIM" <<'PYTEST_SIM'
import pathlib, sys
source, root = pathlib.Path(sys.argv[1]), sys.argv[2]
for name in ("preinst", "postinst", "postrm"):
    text = (source / name).read_text()
    for prefix in ("/tmp/", "/etc/", "/usr/share/", "/usr/lib/enigma2/"):
        text = text.replace(prefix, root + prefix)
    text = text.replace("/var/lib/fullhdglass17", root + "/var/lib/fullhdglass17")
    (pathlib.Path(root) / (name + ".test")).write_text(text)
PYTEST_SIM
SIM_PRE="$SIM/preinst.test"
SIM_POST="$SIM/postinst.test"
SIM_POSTRM="$SIM/postrm.test"
SIM_SETTINGS="$SIM/etc/enigma2/settings"
SIM_STATE="$SIM/var/lib/fullhdglass17/epg-default-v1.state"

# A: fresh install appends only the EPG default; E also protects other hotkeys.
printf '%s\n' 'config.misc.ButtonSetup.info=Infobar/showInfo' 'config.misc.ButtonSetup.red=Infobar/showEventInfo' 'unrelated=value' > "$SIM_SETTINGS"
sh "$SIM_PRE" install
sh "$SIM_POST" configure
printf '%s\n' 'config.misc.ButtonSetup.info=Infobar/showInfo' 'config.misc.ButtonSetup.red=Infobar/showEventInfo' 'unrelated=value' 'config.misc.ButtonSetup.epg=Infobar/openGraphEPG' > "$SIM/settings.expected"
cmp "$SIM_SETTINGS" "$SIM/settings.expected" >/dev/null || fail "fresh install did not append only the Warder EPG default"

# F: repeated hooks after completion are idempotent.
cp "$SIM_SETTINGS" "$SIM/settings.once"
sh "$SIM_PRE" install
sh "$SIM_POST" configure
cmp "$SIM_SETTINGS" "$SIM/settings.once" >/dev/null || fail "repeated install hooks were not idempotent"

# B-D: upgrades preserve multi-service, arbitrary, and already-Warder values.
for value in 'Infobar/openMultiServiceEPG' 'Custom/userEPGAction' 'Infobar/openGraphEPG'; do
  rm -rf "$SIM/var/lib/fullhdglass17"
  printf 'config.misc.ButtonSetup.epg=%s\nconfig.misc.ButtonSetup.info=KeepInfo\nother=keep\n' "$value" > "$SIM_SETTINGS"
  cp "$SIM_SETTINGS" "$SIM/settings.expected"
  sh "$SIM_PRE" upgrade 1.0.5-test203-1
  sh "$SIM_POST" configure 1.0.5-test203-1
  cmp "$SIM_SETTINGS" "$SIM/settings.expected" >/dev/null || fail "upgrade overwrote EPG value $value"
done

# Upgrade with no explicit EPG key is still an upgrade; leave file byte-identical.
rm -rf "$SIM/var/lib/fullhdglass17"
printf '%s\n' 'config.misc.ButtonSetup.info=KeepInfo' 'config.misc.ButtonSetup.red=KeepRed' > "$SIM_SETTINGS"
cp "$SIM_SETTINGS" "$SIM/settings.expected"
sh "$SIM_PRE" upgrade 1.0.5-test203-1
sh "$SIM_POST" configure 1.0.5-test203-1
cmp "$SIM_SETTINGS" "$SIM/settings.expected" >/dev/null || fail "upgrade without EPG key was treated as fresh install"

# Full removal clears only the marker and leaves Enigma2 settings untouched.
cp "$SIM_SETTINGS" "$SIM/settings.expected"
sh "$SIM_POSTRM" remove
cmp "$SIM_SETTINGS" "$SIM/settings.expected" >/dev/null || fail "postrm changed Enigma2 settings"
test ! -e "$SIM_STATE" || fail "postrm left the marker after full removal"
echo "EPG install lifecycle regression: PASS (fresh default, upgrade preservation, unrelated keys, idempotence)"
