#!/usr/bin/env python3
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
pkg = root / "source/package-root"
errors = []

def fail(msg):
    errors.append(msg)

for p in pkg.rglob("*.py"):
    text = p.read_text(encoding="utf-8", errors="replace")
    rel = p.relative_to(root)
    if re.search(r"ssl\._create_unverified_context|CERT_NONE|check_hostname\s*=\s*False", text):
        fail(f"{rel}: TLS verification bypass")
    if re.search(r"\bos\.system\s*\(\s*['\"]rm\s+-rf", text):
        fail(f"{rel}: shell rm -rf")
    if re.search(r"\bsystem\s*\(\s*['\"]rm\s+-rf", text):
        fail(f"{rel}: shell rm -rf")
    if re.search(r"subprocess\.(?:call|Popen|run)\s*\([^\n]*shell\s*=\s*True", text):
        fail(f"{rel}: subprocess shell=True")
    if re.search(r"\beval\s*\(|\bexec\s*\(", text):
        fail(f"{rel}: dynamic eval/exec requires explicit audit")

plugin = (pkg / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py").read_text(encoding="utf-8")
if "from Screens.Console" in plugin:
    fail("plugin.py: updater must not use Screens.Console")
if "eConsoleAppContainer" not in plugin:
    fail("plugin.py: updater eConsoleAppContainer missing")
if "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/update.json" not in plugin:
    fail("plugin.py: authoritative HTTPS updater manifest missing")
if 're.match(r"^[0-9a-f]{64}$", expected)' not in plugin:
    fail("plugin.py: exact Warder asset SHA validation missing")
if 'not all(url.startswith("https://") for url in urls)' not in plugin:
    fail("plugin.py: Warder asset HTTPS validation missing")
if 'stat.S_ISLNK(mode)' not in plugin or "ZIP path traversal rejected" not in plugin:
    fail("plugin.py: safe ZIP extraction guards missing")
if "install_opener(" in plugin:
    fail("plugin.py: downloader must not replace the process-global urllib opener")
if "http://weather.service.msn.com/" in plugin:
    fail("plugin.py: MSN weather transport regressed to cleartext HTTP")
if "PiconHub-Warder/FullHDGlass-Warder-Evolution" in plugin:
    fail("plugin.py: obsolete Warder repository owner returned")
if "unsafe asset manifest redirect" not in plugin:
    fail("plugin.py: official asset manifest redirect guard missing")
asset_prefix = "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/"
if plugin.count(asset_prefix) < 2 or "unsafe asset redirect" not in plugin:
    fail("plugin.py: Warder asset payload channel/redirect guards missing")
if "if isATV:" not in plugin[plugin.find("def chnlSelPatch"):plugin.find("def writeStyleCfg")]:
    fail("plugin.py: OpenATV ChannelSelection patch guard missing")
menu_guard = plugin[plugin.find("def setMenuPyo"):plugin.find("def chckPath")]
if "if isATV:" not in menu_guard:
    fail("plugin.py: OpenATV Menu.py ownership guard missing")
encoding_guard = plugin[plugin.find("def setEncodingUser"):plugin.find("def setCFGoff")]
if "if isATV:" not in encoding_guard:
    fail("plugin.py: OpenATV encoding.conf ownership guard missing")
official_packages = "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/packages/"
if plugin.count(official_packages) < 2:
    fail("plugin.py: updater is not pinned at both metadata and pre-install gates")
if "unsafe manifest redirect" not in plugin or "unsafe package redirect" not in plugin:
    fail("plugin.py: updater HTTPS redirect guards missing")
if '"/usr/bin/7z_g"' in plugin or "'/usr/bin/7z_g'" in plugin:
    fail("plugin.py: downloaded 7zip helper escaped FullHDGlass runtime ownership")
if 'SEVENZIP = os.path.join(PLUGINPATH, "bin", "7z_g")' not in plugin:
    fail("plugin.py: private FullHDGlass 7zip helper path missing")
for owned in (
    '/etc/enigma2/skin_user-172.xml',
    '/etc/enigma2/skin_user-173.xml',
):
    if ('os.remove("' + owned + '")') in plugin or ("os.remove('" + owned + "')") in plugin:
        fail("plugin.py: runtime deletes package-owned file " + owned)

userinfo = (pkg / "usr/lib/enigma2/python/Screens/G17_UserInfo.py").read_text(encoding="utf-8")
if "system(tta)" in userinfo or "df -h > /tmp/" in userinfo:
    fail("G17_UserInfo.py: legacy shell probe returned")

weather = (pkg / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/weather.py").read_text(encoding="utf-8")
if re.search(r"(?:os\.)?system\s*\(\s*['\"]rm\s+-rf", weather):
    fail("weather.py: legacy shell deletion returned")
if "http://weather.service.msn.com/" in weather:
    fail("weather.py: classic MSN fallback regressed to cleartext HTTP")

if errors:
    print("\n".join("FAIL: " + e for e in errors), file=sys.stderr)
    raise SystemExit(1)
print("Runtime safety guardrail: PASS")
