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
    legacy_poster = p.name in ("g17Poster.py", "g17Poster2.py")
    if re.search(r"\bos\.system\s*\(\s*['\"]rm\s+-rf", text) and not legacy_poster:
        fail(f"{rel}: shell rm -rf")
    if re.search(r"\bsystem\s*\(\s*['\"]rm\s+-rf", text) and not legacy_poster:
        fail(f"{rel}: shell rm -rf")
    if re.search(r"subprocess\.(?:call|Popen|run)\s*\([^\n]*shell\s*=\s*True", text):
        fail(f"{rel}: subprocess shell=True")
    if re.search(r"\beval\s*\(|\bexec\s*\(", text) and p.name != "Menu-new17.py":
        fail(f"{rel}: dynamic eval/exec requires explicit audit")

plugin = (pkg / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py").read_text(encoding="utf-8")
if "from Screens.Console" in plugin:
    fail("plugin.py: updater must not use Screens.Console")
if "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/update.json" not in plugin:
    fail("plugin.py: authoritative HTTPS updater manifest missing")
if 're.match(r"^[0-9a-f]{64}$", expected)' not in plugin:
    fail("plugin.py: exact Warder asset SHA validation missing")
if 'all(url.startswith(official_asset_prefix) for url in urls)' not in plugin:
    fail("plugin.py: Warder asset official-prefix validation missing")
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
fifo_guard = plugin[plugin.find("def chckFifo"):plugin.find("def chckPigFont")]
if "if isATV:" not in fifo_guard:
    fail("plugin.py: OpenATV ServiceScan.py ownership guard missing")
if "def _atomicWriteText(" not in plugin or 'open(SKINXML,"w")' in plugin or "open(SKINXML, 'w')" in plugin:
    fail("plugin.py: generated skin.xml writes must remain atomic")
if 'open(CHANSEL_FILE,"w")' in plugin or "open(CHANSEL_FILE, 'w')" in plugin:
    fail("plugin.py: legacy ChannelSelection compatibility write must remain atomic")
if 'cmd = "btrGen17 ' in plugin or "self.container.execute(cmd)" in plugin:
    fail("plugin.py: bitrate helper execution regressed to shell-string form")
if 'cmd = "opkg install ' in plugin or 'cmd = "dpkg -i ' in plugin or "warderInstallContainer.execute(" in plugin:
    fail("plugin.py: updater installer execution must preserve executable as argv[0]")
if "warderInstallProcess = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)" not in plugin:
    fail("plugin.py: updater must execute exact package-manager argv via subprocess.Popen")
if "def _warderShowInstallResult(self):" not in plugin or "self.warderResultTimer.start(250, True)" not in plugin:
    fail("plugin.py: updater result dialog must be deferred until progress modal is closed")
version_cmp = plugin[plugin.find("def _warderVersionTuple"):plugin.find("def _warderFetchJson")]
for required in ('(?:-test(\\d+))?', 'return (major, minor, patch, 1, 0)', 'return (major, minor, patch, 0, int(test_no))'):
    if required not in version_cmp:
        fail("plugin.py: prerelease-aware Warder version ordering missing")
for direct_write in (
    'open(SCREENSPATH + "g17Screens.cfg","w")',
    'open(config.plugins.setupGlass17.par144.value+"hdg17.conf","w")',
    'open("/etc/my_city_Code.txt", \'w\')',
    'open("/etc/my_city_Code.txt","a")',
):
    if direct_write in plugin:
        fail("plugin.py: non-atomic FullHDGlass state write returned: " + direct_write)
official_packages = "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/packages/"
if plugin.count(official_packages) < 2:
    fail("plugin.py: updater is not pinned at both metadata and pre-install gates")
if "unsafe manifest redirect" not in plugin or "unsafe package redirect" not in plugin:
    fail("plugin.py: updater HTTPS redirect guards missing")
download_guard = plugin[plugin.find("def _warderDownload"):plugin.find("def updatechckact")]
stable_pkg = "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/packages/"
test_pkg = "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/warder-modernization-work/packages/test/"
if "official_package_prefixes = (" not in download_guard or stable_pkg not in download_guard or test_pkg not in download_guard:
    fail("plugin.py: updater stable/TEST download channel prefixes missing")
if "any(str(response.geturl()).startswith(x) for x in official_package_prefixes)" not in download_guard:
    fail("plugin.py: updater package redirect escaped official channels")
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

enhanced_weather = (pkg / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/E_weather.py").read_text(encoding="utf-8")
if "self.waitTimer.stop()" not in enhanced_weather[enhanced_weather.find("def exit(self)"):enhanced_weather.find("def blueKey")]:
    fail("E_weather.py: wait timer cleanup missing on exit")
download_exit = plugin[plugin.find("class Glass17Download"):plugin.find("class Glass17DownLoad")]
if download_exit and "self.dwnTimer.stop()" not in download_exit:
    fail("plugin.py: download-menu timer cleanup missing")

weather = (pkg / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/weather.py").read_text(encoding="utf-8")
if re.search(r"(?:os\.)?system\s*\(\s*['\"]rm\s+-rf", weather):
    fail("weather.py: legacy shell deletion returned")
if "http://weather.service.msn.com/" in weather:
    fail("weather.py: classic MSN fallback regressed to cleartext HTTP")

if errors:
    print("\n".join("FAIL: " + e for e in errors), file=sys.stderr)
    raise SystemExit(1)
print("Runtime safety guardrail: PASS")


# Warder updater must keep stable and TEST authorities explicit and isolated.
assert '"https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/update.json"' in plugin
assert '"https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/warder-modernization-work/update-test.json"' in plugin
assert 'if str(url) not in official_manifests:' in plugin
assert 'if final_url not in official_manifests:' in plugin
assert "PiconHub-Warder/FullHDGlass-Warder-Evolution" not in plugin
assert 'FullHDGlass17 - Warder Evolution' in plugin
assert 'any(str(response.geturl()).startswith(x) for x in official_package_prefixes)' in plugin
