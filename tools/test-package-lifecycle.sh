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
! grep -REn '/etc/enigma2/settings' "$CONTROL" | grep -Ev 'deliberately never modified|intentionally|Do not remove|configuration lives in' || fail "settings mutation candidate found"
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
