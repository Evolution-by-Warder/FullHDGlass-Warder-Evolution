#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "source/package-root"
PLUGIN = (PKG / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py").read_text(encoding="utf-8")
CITY = (PKG / "etc/city_Code-17.txt").read_text(encoding="utf-8")
SKIN = (PKG / "usr/share/enigma2/hd_glass17/skin.xml").read_text(encoding="utf-8")
WEAUTILS = (PKG / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/weaUtils.py").read_text(encoding="utf-8")
WEATHER = (PKG / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/weather.py").read_text(encoding="utf-8")
EWEATHER = (PKG / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/E_weather.py").read_text(encoding="utf-8")

rows = [x for x in CITY.splitlines() if x.startswith("om|")]
sk = [x for x in rows if x.split("|")[3] == "SK"]
cz = [x for x in rows if x.split("|")[3] == "CZ"]
assert len(sk) == 4208, len(sk)
assert len(cz) == 6258, len(cz)
assert len(rows) == 11010, len(rows)
country_codes = {x.split("|")[3] for x in rows if len(x.split("|")) > 3 and x.split("|")[3]}
assert len(country_codes) == 51, len(country_codes)
assert {"SK", "CZ", "AT", "DE", "PL", "HU", "GB", "VA"}.issubset(country_codes)
assert "om|Rišňovce|" in CITY

# Warder must expose the complete r12 country/city surface in Enhanced Weather too.
# Derive it deterministically from the authoritative r12 Classic database.
generator = ROOT / "tools/generate-ewea-city.py"
with tempfile.TemporaryDirectory() as tmp:
    generated = Path(tmp) / "ewea_city_Code-17.txt"
    subprocess.check_call([sys.executable, str(generator), str(PKG / "etc/city_Code-17.txt"), str(generated)])
    ewea_bytes = generated.read_bytes()
    ewea_rows = [x for x in ewea_bytes.decode("utf-8").splitlines() if x.startswith("q|")]
    assert len([x for x in ewea_rows if x.split("|")[2] == "SK"]) == 4208
    assert len([x for x in ewea_rows if x.split("|")[2] == "CZ"]) == 6258
    assert "q|Rišňovce|SK||Slovakia|Nitra" in ewea_rows
    ewea_codes = {x.split("|")[2] for x in ewea_rows}
    assert len(ewea_codes) == 51, len(ewea_codes)
    assert {"SK", "CZ", "AT", "DE", "PL", "HU", "GB", "VA"}.issubset(ewea_codes)
    assert all(len(x.split("|")) == 6 for x in ewea_rows)
    assert all(x.split("|")[0] == "q" for x in ewea_rows)

POSTINST = (ROOT / "source/control/postinst").read_text(encoding="utf-8")
BUILD_TEST = (ROOT / "tools/build-test-ipk.sh").read_text(encoding="utf-8")
assert 'copy_default_if_missing /etc/ewea_city_Code-17.txt /etc/ewea_city_Code.txt' in POSTINST
assert 'generate-ewea-city.py' in BUILD_TEST
assert 'self.fileName = "/etc/ewea_city_Code.txt"' in EWEATHER
# r12 Enhanced Weather city selector layout: country heading, cities below it,
# blank separator, next country; country must not be repeated on every city row.
for token in ('value.startswith("#")', 'self.list.append((country.upper(), "__country__"))',
              'self.list.append(("", "__country__"))', 'cityNo = 0',
              'label = p[1] + (", " + p[5] if p[5] else "")',
              'not any(x.startswith("#") for x in lines)'):
    assert token in EWEATHER, token
assert '# Slovakia' in ewea_bytes.decode("utf-8")
assert '# Czechia' in ewea_bytes.decode("utf-8")
assert '# Albania' in ewea_bytes.decode("utf-8")
assert '# Vatican City' in ewea_bytes.decode("utf-8")

assert "unicodedata.normalize" in PLUGIN
assert "_citySearchKey" in PLUGIN
assert "geocoding-api.open-meteo.com/v1/search" in PLUGIN
assert "weather.service.msn.com/find.aspx" not in PLUGIN
assert 'country|' in PLUGIN
assert '/etc/city_Code-17.txt' in PLUGIN
assert "Open-Meteo city search" in PLUGIN
assert '"group|EUROPE"' not in PLUGIN
assert '"Krajiny Európy"' not in PLUGIN
assert 'item = ["country|" + country]' in PLUGIN
assert 'for country in seen:' in PLUGIN
# r4 Open-Meteo behaviour preserved by the cumulative r12 reference.
assert "def openMeteo(" in WEAUTILS
for token in (
    "geocoding-api.open-meteo.com/v1/search",
    "api.open-meteo.com/v1/forecast",
    "temperature_2m",
    "relative_humidity_2m",
    "apparent_temperature",
    "weather_code",
    "surface_pressure",
    "wind_speed_10m",
    "wind_direction_10m",
    "visibility",
    "sunrise",
    "sunset",
):
    assert token in WEAUTILS, token
for field in (
    "weather_dict['city']",
    "weather_dict['country']",
    "weather_dict['lat']",
    "weather_dict['long']",
    "weather_dict['wind']",
    "weather_dict['wind_direction']",
    "weather_dict['sunrise']",
    "weather_dict['sunset']",
):
    assert field in WEATHER, field
assert "wmoText(" in WEATHER
assert "Error" in WEATHER and "Open-Meteo" in WEATHER
assert "Weather_values'].setText" in WEATHER
assert "Weather_sunrise'].setText" in WEATHER
assert "Weather_sunset'].setText" in WEATHER
assert "Weather_state%s' % ii].setText" in WEATHER
assert "Weather_Date%s' % ii].setText" in WEATHER
assert "openMeteo(" in WEATHER
assert "Classic Open-Meteo" in PLUGIN
assert '_("Provider"), config.plugins.setupGlass17.par88' not in PLUGIN
assert '_("API-Key OpenWeatherMap"), config.plugins.setupGlass17.par228' not in PLUGIN
assert 'if not rows:' in EWEATHER
assert 'endswith(" station")' in EWEATHER
assert "str(tmp).strip() not in lines" in PLUGIN
assert '<screen name="ScreenSaver" position="0,0" size="1920,1080"' in SKIN
assert 'name="picture" position="0,0" size="1280,720"' in SKIN
for screen in ("Menu", "menu_mainmenu", "menu_information", "menu_setup", "menu_scan", "menu_system", "menu_harddisk", "menu_shutdown"):
    m = re.search(r'<screen\b[^>]*name="%s"[\s\S]*?</screen>' % screen, SKIN)
    assert m, screen
    assert len(re.findall(r'render="Listbox"', m.group(0))) == 1, screen
assert '<screen name="Opkg"' in SKIN
assert 'source="key_red"' in re.search(r'<screen\b[^>]*name="Opkg"[\s\S]*?</screen>', SKIN).group(0)
assert 'source="key_blue"' in re.search(r'<screen\b[^>]*name="Opkg"[\s\S]*?</screen>', SKIN).group(0)
print("r1-r12 regression gate: PASS")
print("weather locations: SK=%d CZ=%d TOTAL=%d COUNTRIES=%d" % (len(sk), len(cz), len(rows), len(country_codes)))

# r12 visual/functional baseline: this context menu must not disappear during modernization.
assert '<screen name="EventViewContextMenu"' in SKIN

# r12 authoritative package parity: preserve the functional surface of the supplied 9.50-r12.
# These symbols are taken directly from the maintainer-supplied r12 IPK and must remain reachable.
for symbol in (
    "def chckPigFont(", "def menusel(", "def changePIGres(", "def reloadCities(",
    "def findCity(", "def addNewLine(", "def restoreCfgFromFile(", "def updateChck(",
    "def findPicon(", "def showEnhancedInfo(", "def changeSkinXml(", "def changeScreenXml(",
):
    assert symbol in PLUGIN, symbol
for symbol in ("def changeCity(", "def download_xml(", "def resetWeather_values(", "def fixDate("):
    assert symbol in WEATHER, symbol
# Enhanced Weather may modernize the old geocode_legacy helper, but the r9/r10
# migration behaviour itself is mandatory: legacy station names must resolve via
# Open-Meteo, empty/incomplete results must be guarded, and the city editor path
# must remain reachable.
for symbol in ("def resolve_location(", "def changeCityAnswer(", "def callbackNewCity("):
    assert symbol in EWEATHER, symbol
for token in (
    "geocoding-api.open-meteo.com/v1/search",
    "if not rows:",
    "Incomplete location data:",
    'endswith(" station")',
    "config.plugins.setupGlass17.par98.value = new_loc",
):
    assert token in EWEATHER, token
for symbol in ("def calcSun(", "def dewpoint(", "def wmoPicon(", "def wmoText(", "def windDir(", "def openMeteo("):
    assert symbol in WEAUTILS, symbol
for variant in ('"with PIG":"3"', '"simply PIG":"10"', '"PIG2":"11"', '"PIG4":"13"'):
    assert variant in PLUGIN, variant


# Picon/runtime path parity and Warder ownership safety.
# Keep legacy convenience links outside /usr/share/enigma2, but never create
# or retarget image/package-manager-owned picon paths on OpenATV.
setpath = PLUGIN[PLUGIN.find("def setPathFiles("):PLUGIN.find("ENAFINDER =")]
assert 'links = ["/picon"]' in setpath
assert 'links.append("/media/usb/picon")' in setpath
assert '"/usr/share/enigma2/picon"' not in setpath
assert '"/usr/share/enigma2/picon_50x30"' not in setpath
assert "elif not os.path.lexists(x):" in setpath
assert "if os.path.islink(x):" in setpath
assert "os.unlink(x)" in setpath
assert "elif not os.path.lexists(x):\n\t\t\t\t\tmakelnk(x)" in setpath
assert '"/hdg17_files" in a or "/hdg18_files" in a' in setpath

# A blank/corrupt legacy picon base path must not crash setupGlass17.
chckpath = PLUGIN[PLUGIN.find("def chckPath("):PLUGIN.find("def _atomicWriteText(")]
assert 'path = (path or "").strip()' in chckpath
assert 'if not path or path == "/":' in chckpath
assert "return False" in chckpath

# The retired spinner helper may repair only the exact legacy FullHDGlass
# symlink; it must leave a normal image-owned spinner and unrelated symlinks alone.
spinner = PLUGIN[PLUGIN.find("def spinnerOnOff("):PLUGIN.find("def autoHdd(")]
assert "if not os.path.islink(spinner):" in spinner
assert "target != os.path.realpath(legacy)" in spinner
assert "if not os.path.isdir(original):" in spinner
assert spinner.find("if not os.path.isdir(original):") < spinner.find("os.unlink(spinner)")
assert "os.unlink(spinner)" in spinner


# OpenATV ownership boundary: legacy controls that would rewrite image-owned
# ChannelSelection.py or encoding.conf must not be exposed on modern OpenATV.
assert "if not isATV and os.path.isfile(CHANSEL_FILE):" in PLUGIN
assert 'if not isATV and not os.path.exists(\'/etc/dpkg\'):' in PLUGIN
for fn, guard in (
    ("def chnlSelPatch(", "if isATV:"),
    ("def setEncodingUser(", "if isATV:"),
    ("def setMenuPyo(", "if isATV:"),
):
    block = PLUGIN[PLUGIN.find(fn):PLUGIN.find("################################################################", PLUGIN.find(fn) + 20)]
    assert guard in block, fn

# Warder updater trust boundary and r12 installation-result behaviour.
for token in (
    'manifest_url = "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/update.json"',
    'package_url.startswith("https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/packages/")',
    're.match(r"^[0-9a-f]{64}$", sha256)',
    "actual_sha != expected_sha",
    'cmd = ["opkg", "install", "--force-reinstall", "--force-overwrite", target]',
    "def _warderInstallFinished(",
    'MessageBox.TYPE_ERROR, 15',
    'restartbox.setTitle(_("Restart GUI now?"))',
):
    assert token in PLUGIN, token


# Picon compatibility without taking ownership of OpenATV's /usr/share/enigma2.
set_path_start = PLUGIN.find("def setPathFiles(")
set_path_end = PLUGIN.find("ENAFINDER = False", set_path_start)
assert set_path_start >= 0 and set_path_end > set_path_start
set_path = PLUGIN[set_path_start:set_path_end]
assert 'links = ["/picon"]' in set_path
assert 'links.append("/media/usb/picon")' in set_path
assert '"/usr/share/enigma2/picon"' not in set_path
assert '"/usr/share/enigma2/picon_50x30"' not in set_path
find_picon = PLUGIN[PLUGIN.find("def findPicon("):PLUGIN.find("def showDyn_EMM_ECM(", PLUGIN.find("def findPicon("))]
for fallback in ("picon_400x240", "picon_220x132", "piconSat", "piconProv"):
    assert fallback in find_picon, fallback


# r12 live weather refresh after a city change: the active ExtraInfo17 instance
# must be reachable from setup saving, and the refresh must be scheduled without GUI restart.
for token in (
    "G17_EXTRAINFO_INSTANCE = None",
    "global G17_EXTRAINFO_INSTANCE",
    "G17_EXTRAINFO_INSTANCE = self",
    "def refreshWeatherNow(self):",
    "self._weatherCityAtOpen = config.plugins.setupGlass17.par13.value",
    "G17_EXTRAINFO_INSTANCE.refreshWeatherNow()",
):
    assert token in PLUGIN, token

# Infobar/EPG event integration retained from r12: service start, event update,
# user weather overlay and timeout handling must remain wired.
for token in (
    "InfoBarPlugins.__init__ = hdg17inicialize",
    "iPlayableService.evStart: self.serviceStartNow17",
    "iPlayableService.evUpdatedEventInfo: self.serviceStartNow173",
    "self.onShow.append(self.serviceStartNow172)",
    "from Plugins.Extensions.setupGlass17.weather import WeatherScreen",
    "self.g17dialogUser = self.session.instantiateDialog(WeatherScreen",
    "def serviceStartNow17(",
    "def serviceStartNow172(",
    "def serviceStartNow173(",
    "def controlWindow17(",
    "def hideWindow17(",
):
    assert token in PLUGIN, token


# Setup/config and updater parity: user configuration remains Enigma2-owned,
# restore/save paths stay available, and updates use package-manager argv.
for token in (
    "configfile.save()",
    "def saving(",
    "def restoreCfgFromFile(",
    '_atomicWriteText(config.plugins.setupGlass17.par144.value+"hdg17.conf", allLines)',
    'cmd = ["opkg", "install", "--force-reinstall", "--force-overwrite", target]',
    'cmd = ["dpkg", "-i", "--force-overwrite", target]',
    "self.warderInstallContainer.execute(*cmd)",
):
    assert token in PLUGIN, token


# r11/r12 PIG menu behaviour, not just symbol presence.
menu_select = PLUGIN[PLUGIN.find("def menusel("):PLUGIN.find("def listDir(")]
for variant, code in (("with PIG","3"), ("simply PIG","10"), ("PIG2","11"), ("PIG4","13")):
    assert '"%s":"%s"' % (variant, code) in menu_select, variant
pig_change = PLUGIN[PLUGIN.find("def changePIGres("):PLUGIN.find("def changeScreenXml(")]
for token in ('session.VideoPicture', 'position="157,166"', 'position="66,120"', 'size="697,435"', 'size="882,528"'):
    assert token in pig_change, token
screen_change = PLUGIN[PLUGIN.find("def changeScreenXml("):PLUGIN.find("def setTypeIcos(")]
for screen in ("menu_mainmenu", "menu_information", "menu_setup", "menu_scan", "menu_system", "menu_harddisk", "menu_shutdown", "Menu"):
    assert '"%s"' % screen in screen_change, screen
assert 'new in ("12","13")' in screen_change
pig_font = PLUGIN[PLUGIN.find("def chckPigFont("):PLUGIN.find("def chMT(")]
for token in ("changePIGres()", "cChannelsel()", "changeChF()", "setFontEventEpgsel("):
    assert token in pig_font, token

# r12 OpenATV software/package-manager skin surfaces. Opkg must expose both
# red Close and blue Log sources; installer/log screens must remain present.
opkg = re.search(r'<screen\b[^>]*name="Opkg"[\s\S]*?</screen>', SKIN).group(0)
for token in ('source="key_red"', 'source="key_blue"', 'name="log"', 'name="activityslider"'):
    assert token in opkg, token
for screen in ("OPKGMenu", "OPKGSource", "OpkgInstaller", "IpkgInstaller", "SoftwareManagerInfo",
               "SoftwareManagerSetup", "SoftwareUpdate", "RunSoftwareUpdate",
               "PackageAction", "PackageActionLog", "LogManager", "LogManagerViewLog"):
    assert re.search(r'<screen\b[^>]*name="%s"[\s\S]*?</screen>' % screen, SKIN), screen
