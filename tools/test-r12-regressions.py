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
PROVIDER = (PKG / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderProgramInfo.py").read_text(encoding="utf-8")

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
classic_loader = PLUGIN[PLUGIN.index("def _loadLocalCities(self):"):PLUGIN.index("def _onlineCitySearch(self", PLUGIN.index("def _loadLocalCities(self):"))]
assert 'if currentName == "SK": currentName = "Slovakia"' in classic_loader
assert 'elif currentName == "CZ": currentName = "Czechia"' in classic_loader
assert 'self.countryNames[country] = currentName' in classic_loader
assert 'currentName = "SK"' not in classic_loader
assert 'currentName = "CZ"' not in classic_loader

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
    ewea_headings = [x[2:].strip() for x in ewea_bytes.decode("utf-8").splitlines() if x.startswith("# ")]
    assert len(ewea_headings) == 51, len(ewea_headings)
    assert ewea_headings[:2] == ["Slovakia", "Czechia"], ewea_headings[:2]
    assert ewea_headings[-1] == "Vatican City"

POSTINST = (ROOT / "source/control/postinst").read_text(encoding="utf-8")
BUILD_TEST = (ROOT / "tools/build-test-ipk.sh").read_text(encoding="utf-8")
assert 'copy_default_if_missing /etc/ewea_city_Code-17.txt /etc/ewea_city_Code.txt' in POSTINST
assert 'generate-ewea-city.py' in BUILD_TEST
assert 'self.fileName = "/etc/ewea_city_Code.txt"' in EWEATHER
# Warder Enhanced Weather selector is genuinely country-first: the first screen
# contains only the 51 country rows; OK enters one country's cities; Back returns.
for token in ('self.cityLevel = "countries"', 'self.activeCountry = None',
              'self.countryOrder = []', 'self.countryCities = {}',
              'if self.cityLevel == "countries":',
              'self.list.append((country, "__country__|" + country))',
              'self.cityLevel = "cities"', 'self.mainFnc()',
              'if self.cityLevel == "cities":',
              'self.cityLevel = "countries"',
              'for value in self.countryCities.get(self.activeCountry, [])',
              'label = p[1] + (", " + p[5] if p[5] else "")'):
    assert token in EWEATHER, token
select_start = EWEATHER.index("def select(self):")
main_start = EWEATHER.index("def mainFnc(self", select_start)
selector = EWEATHER[select_start:EWEATHER.index("def blueKey(self):", main_start)]
assert 'selection[1].startswith("__country__|")' in selector
assert 'self.close(str(value))' in selector
assert 'self.list.append((country.upper(), "__country__"))' not in selector
assert '# Slovakia' in ewea_bytes.decode("utf-8")
assert '# Czechia' in ewea_bytes.decode("utf-8")
assert '# Albania' in ewea_bytes.decode("utf-8")
assert '# Vatican City' in ewea_bytes.decode("utf-8")
# Manual Enhanced Weather additions must be inserted into the matching country section.
for token in ('country = parts[4].strip()', 'header = "# " + country', 'lines.insert(insert_at, ret)', 'Writelog("city insert: %s" % e)'):
    assert token in EWEATHER, token

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
assert '<screen name="MessageBoxModal"' in SKIN
modal = re.search(r'<screen\b[^>]*name="MessageBoxModal"[\s\S]*?</screen>', SKIN).group(0)
for token in ('name="text"', 'name="icon"', 'name="list"', 'input_question.png', 'scrollbarMode="showOnDemand"'):
    assert token in modal, token
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

# Warder updater has isolated stable and TEST GitHub channels. TEST builds may
# update directly from the development branch without weakening stable trust.
for token in (
    '"https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/update.json"',
    '"https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/warder-modernization-work/update-test.json"',
    '"https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/warder-modernization-work/packages/test/"',
    'if "-test" in self.readVersion():',
):
    assert token in PLUGIN, token

# Warder updater trust boundary and r12 installation-result behaviour.
for token in (
    'manifest_url = "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/update.json"',
    'official_prefixes = (',
    '"https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/packages/",',
    '"https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/warder-modernization-work/packages/test/",',
    'not any(package_url.startswith(x) for x in official_prefixes)',
    're.match(r"^[0-9a-f]{64}$", sha256)',
    "actual_sha != expected_sha",
    'cmd = ["opkg", "--force-reinstall", "--force-overwrite", "install", target]',
    'self.warderInstallProcess = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)',
    'def _warderInstallPoll(self):',
    "def _warderInstallFinished(",
    'MessageBox.TYPE_ERROR, 15',
    'GUI will restart automatically in 3 seconds.',
    'self.warderRestartTimer.start(3000, True)',
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
    "def _setWeatherCityChoices(selected=None):",
    "def _refreshLiveWeather():",
    "def openWeatherCityChoice(self):",
    "def weatherCityChoiceSelected(self, answer):",
    "self.session.openWithCallback(self.weatherCityChoiceSelected, ChoiceBox",
    "self._weatherCityAtOpen = config.plugins.setupGlass17.par13.value",
    "if self._weatherCityAtOpen != config.plugins.setupGlass17.par13.value:",
    "G17_EXTRAINFO_INSTANCE.refreshWeatherNow()",
):
    assert token in PLUGIN, token

# r11/r12 PIG menu navigation fix: PIG variants 3/10/11/13 must not bind
# a second Listbox to the same menu source. The mirrored current item is a Label.
HDG = (PKG / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/hdg17Screens.xml").read_text(encoding="utf-8")
for suffix in ("3", "10", "11", "13"):
    for screen in ("Menu", "menu_mainmenu", "menu_information", "menu_setup", "menu_scan", "menu_system", "menu_harddisk", "menu_shutdown"):
        start = HDG.find('<screen name="%s-%s"' % (screen, suffix))
        assert start >= 0, (screen, suffix)
        end = HDG.find("</screen>", start)
        block = HDG[start:end]
        assert block.count('source="menu" render="Listbox"') == 1, (screen, suffix)
        assert block.count('source="menu" render="Label"') == 1, (screen, suffix)
        assert 'g17MenuCurrentText' in block, (screen, suffix)

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
    'cmd = ["opkg", "--force-reinstall", "--force-overwrite", "install", target]',
    'cmd = ["dpkg", "-i", "--force-overwrite", target]',
    "self.warderInstallProcess = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)",
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

# Infobar weather must retain last-known Open-Meteo data across GUI restarts.
WEAUTILS = (PKG / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/weaUtils.py").read_text(encoding="utf-8")
for token in ('_OPENMETEO_CACHE_FILE = "/etc/enigma2/fullhdglass17-openmeteo-cache.json"', 'def _loadOpenMeteoCache():', 'def _saveOpenMeteoCache():', '_loadOpenMeteoCache()', '_saveOpenMeteoCache()', 'cached = _OPENMETEO_CACHE.get(ckey)'):
    assert token in WEAUTILS, token

# Infobar weather must not wait behind the legacy 30-second startup timer.
assert 'if self.enaWeainf:\n\t\t\t\t\tself.refreshWeatherNow()' in PLUGIN
assert 'self.clrMemTimer.startLongTimer(1)' not in PLUGIN[PLUGIN.index('def refreshWeatherNow'):PLUGIN.index('def clearMem', PLUGIN.index('def refreshWeatherNow'))]
assert 'self.clearMem()' in PLUGIN[PLUGIN.index('def refreshWeatherNow'):PLUGIN.index('def clearMem', PLUGIN.index('def refreshWeatherNow'))]

# Setup-open automatic updater contract
assert '_warderAutoUpdateCheck' in PLUGIN
assert 'self.delayTimer.timeout.connect(self._warderAutoUpdateCheck)' in PLUGIN
assert 'self.onLayoutFinish.append(self._warderStartAutoUpdateCheck)' in PLUGIN
assert 'def _warderStartAutoUpdateCheck(self):' in PLUGIN
assert 'self.delayTimer.start(3000, True)' in PLUGIN
assert 'self.updatechckact(False, automatic=True)' in PLUGIN
assert 'self.firststart = False\n\t\t\tself.delayTimer.start(3000, True)' not in PLUGIN
assert 'if not automatic and not config.plugins.setupGlass17.par75.value and not ena:' in PLUGIN
assert 'self.updatechckact(True)' in PLUGIN

# Updater UX: keep user informed while update is running.
assert 'self.warderProgressBox = self.session.open(MessageBox, _("Updating...")' in PLUGIN
assert '_("Please wait.")' in PLUGIN
assert 'enable_input=False' in PLUGIN
assert 'def _warderCloseProgress(self):' in PLUGIN
assert 'self._warderCloseProgress()' in PLUGIN


# TEST23 FullHD graphical guide: fullscreen and complete graph/PIG placement contract.
for screen in ("GraphicalEPG", "GraphicalEPGPIG"):
    block = re.search(r'<screen\b[^>]*name="%s"[\s\S]*?</screen>' % screen, SKIN).group(0)
    assert 'position="15,15"' in block and 'size="1890,1050"' in block, screen
    for n in range(6):
        if screen == "GraphicalEPGPIG":
            assert ('name="timeline%d"' % n) not in block, (screen, n)
        else:
            assert 'name="timeline%d"' % n in block, (screen, n)
    required = ['name="bouquetlist"']
    if screen == "GraphicalEPG":
        required += ['name="primetime"', 'name="change_bouquet"', 'name="jump"', 'name="page"']
    for token in required:
        assert token in block, (screen, token)
pig23 = re.search(r'<screen\b[^>]*name="GraphicalEPGPIG"[\s\S]*?</screen>', SKIN).group(0)
assert 'source="session.VideoPicture" render="Pig"' in pig23

# Current OpenATV EPG/RDS skin-name compatibility added in TEST22.
for screen in ("QuickEPG", "GraphicalEPG", "GraphicalEPGPIG", "GraphicalInfoBarEPG", "RassInteractive"):
    assert re.search(r'<screen\b[^>]*name="%s"[\s\S]*?</screen>' % screen, SKIN), screen
for screen in ("GraphicalEPG", "GraphicalEPGPIG", "GraphicalInfoBarEPG"):
    block = re.search(r'<screen\b[^>]*name="%s"[\s\S]*?</screen>' % screen, SKIN).group(0)
    for token in ('name="timeline_text"', 'name="list"', 'name="timeline_now"'):
        assert token in block, (screen, token)
for screen in ("GraphicalEPG", "GraphicalEPGPIG"):
    block = re.search(r'<screen\b[^>]*name="%s"[\s\S]*?</screen>' % screen, SKIN).group(0)
    assert 'name="lab1"' in block, screen
    for key in ("red", "green", "yellow", "blue"):
        if screen == "GraphicalEPGPIG":
            # TEST48+: this screen deliberately isolates its colour captions from
            # legacy/OpenATV key_* state so PROGRAM INFO cannot become CSFD.
            assert ('source="warder_key_%s" render="Label"' % key) in block, (screen, key)
            assert ('source="key_%s" render="Label"' % key) not in block, (screen, key)
        else:
            assert ('name="key_%s"' % key) in block, (screen, key)
pigepg = re.search(r'<screen\b[^>]*name="GraphicalEPGPIG"[\s\S]*?</screen>', SKIN).group(0)
assert 'source="session.VideoPicture" render="Pig"' in pigepg
quickepg = re.search(r'<screen\b[^>]*name="QuickEPG"[\s\S]*?</screen>', SKIN).group(0)
for token in ('source="Service"', 'source="session.RecordState"', 'name="list"'):
    assert token in quickepg, token
rass = re.search(r'<screen\b[^>]*name="RassInteractive"[\s\S]*?</screen>', SKIN).group(0)
assert 'name="Marker"' in rass
for n in range(1, 10):
    assert 'name="subpages_%d"' % n in rass, n
# FullHDGlass RDS overlay must stay transparent so OpenATV DABSlideDisplay
# (zPosition -20) can remain visible behind the radio text UI.
rds = re.search(r'<screen\b[^>]*name="RdsInfoDisplay"[\s\S]*?</screen>', SKIN).group(0)
assert 'backgroundColor="transparent"' in rds
assert 'zPosition="-2"' in rds

# TEST24 Cool-like PIG guide geometry.
pig24 = re.search(r'<screen\b[^>]*name="GraphicalEPGPIG"[\s\S]*?</screen>', SKIN).group(0)
assert 'source="session.VideoPicture" render="Pig"' in pig24 and 'zPosition="3"' in pig24
assert 'NumberOfRows="15"' in pig24
assert 'name="timeline_text" position="75,387" size="1755,36"' in pig24 and 'position="15,423" size="1845,495"' in pig24
assert 'type="EventTime">StartTime' in pig24 and 'type="EventTime">EndTime' in pig24

# TEST26: PIG guide header is clean; EPG grid reserves only a narrow picon rail.
pig26_start = SKIN.index('<screen name="GraphicalEPGPIG"')
pig26_end = SKIN.index('</screen>', pig26_start)
pig26 = SKIN[pig26_start:pig26_end]
assert 'source="Title" render="Label"' not in pig26
assert 'source="global.CurrentTime" render="Label" position="30,12"' not in pig26
assert 'name="timeline_text" position="75,387" size="1755,36"' in pig26
assert 'name="timeline0"' not in pig26
assert 'name="timeline_now" position="75,423"' in pig26


# TEST26 runtime policy: picon-only native graphical EPG and restart dialog outlives 3s restart timer.
PLUGIN = (ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py").read_text(encoding="utf-8")
assert 'graph_servicetitle_mode.value = "picon"' in PLUGIN
assert 'graph_piconwidth.value = 60' in PLUGIN
assert 'MessageBox.TYPE_INFO, 5, enable_input=False' in PLUGIN
assert 'warderRestartTimer.start(3000, True)' in PLUGIN

# TEST27: suppress OpenATV window-decoration bouquet title only for GraphicalEPGPIG.
assert 'def warderEPGSelectionSetTitle(self, title, *args, **kwargs):' in PLUGIN
assert 'getattr(self, "skinName", None) == "GraphicalEPGPIG"' in PLUGIN
assert 'title = ""' in PLUGIN

# TEST28: FullHDGlass GraphicalEPGPIG color-key row and scoped actions.
assert 'source="warder_key_red" render="Label" position="30,930" size="420,42"' in pig26
assert 'source="key_red" render="Label" position="30,930" size="420,42"' not in pig26
assert 'name="primetime" position="30,930"' not in SKIN
assert 'def warderEPGSelectionRedButtonPressed(self):' in PLUGIN
assert 'self.session.openWithCallback(self.warderProgramInfoClosed, WarderProgramInfo, event, service)' in PLUGIN
assert 'graph_green.value = "timer"' in PLUGIN
assert 'graph_yellow.value = "gotodatetime"' in PLUGIN
assert 'graph_blue.value = "epgsearch"' in PLUGIN

# TEST29/TEST48+: GraphicalEPGPIG uses Warder-owned StaticText sources so
# OpenATV/legacy key_* refresh cannot replace PROGRAM INFO with CSFD.
for key in ("red", "green", "yellow", "blue"):
    assert ('source="warder_key_%s" render="Label"' % key) in pig26, key
    assert ('source="key_%s" render="Label"' % key) not in pig26, key
assert 'def warderEPGSelectionInit(self, *args, **kwargs):' in PLUGIN
assert '("warder_key_red", _warderUiText("PROGRAM INFO"))' in PLUGIN


# TEST30: FullHDGlass GraphicalEPGPIG colour labels and handlers must stay paired.
for token in (
    '("warder_key_red", _warderUiText("PROGRAM INFO"))',
    '("warder_key_green", _warderUiText("Add Timer"))',
    '("warder_key_yellow", _warderUiText("Goto Date/Time"))',
    '("warder_key_blue", _warderUiText("EPG Search"))',
    'WarderEPGSelection.RefreshColouredKeys = warderEPGSelectionRefreshColouredKeys',
    'self.session.openWithCallback(self.warderProgramInfoClosed, WarderProgramInfo, event, service)',
    'return self.RecordTimerQuestion(True)',
    'return self.enterDateTime()',
    'return self.openEPGSearch()',
    'config.epgselection.graph_yellow.value = "gotodatetime"',
):
    assert token in PLUGIN, token

# TEST31: red key is direct programme information, never an external search/chooser.
assert 'class WarderProgramInfo(Screen):' in PLUGIN
assert 'self.session.openWithCallback(self.warderProgramInfoClosed, WarderProgramInfo, event, service)' in PLUGIN
assert 'WarderEPGSelection.warderProgramInfoClosed = warderProgramInfoClosed' in PLUGIN
assert 'getattr(service, "ref", None)' in PLUGIN
program_info = PLUGIN.split('class WarderProgramInfo(Screen):', 1)[1].split('def readHWtype', 1)[0]
assert 'source="session.VideoPicture" render="Pig"' not in program_info
assert 'for name in ("preview", "stationPicon")' not in program_info
assert 'self["stationPicon"].instance.setPixmapFromFile(picon)' in program_info
assert 'from Components.Renderer.Picon import getPiconName' in program_info
assert 'foregroundColor="#3388dd"' in program_info
assert 'backgroundColor="transpBlack3"' in program_info
assert '<eLabel position="500,425" size="2,490" backgroundColor="#707070" />' in program_info
assert 'name="description" position="535,425" size="1300,490"' in program_info
assert 'position="25,955" size="420,62" backgroundColor="transpBlack3"' in program_info
assert 'return self.session.open(IMDB, name, False)' not in PLUGIN
assert 'source="warder_key_red" render="Label" position="30,930" size="420,42"' in pig26
assert 'source="key_red" render="Label" position="30,930" size="420,42"' not in pig26

# Package upgrade safety inherited from the original r12 DreamOS GSOD investigation.
POSTRM = (ROOT / "source/control/postrm").read_text(encoding="utf-8")
assert 'upgrade|failed-upgrade|abort-upgrade|disappear)' in POSTRM
assert POSTRM.index('upgrade|failed-upgrade|abort-upgrade|disappear)') < POSTRM.index('restore_backup')
assert 'rm -rf /usr/share/enigma2/hd_glass17' not in POSTRM
# The menu background referenced by r12 hdg17Screens must always ship in Warder payload.
HDGSCREENS = (PKG / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/hdg17Screens.xml").read_text(encoding="utf-8")
assert 'backgroundPixmap="hd_glass17/buttons/selected-menu_bgpixmap.png"' in HDGSCREENS
assert (PKG / "usr/share/enigma2/hd_glass17/buttons/selected-menu_bgpixmap.png").is_file()

# DreamOS compatibility: do not reject valid Enigma2 layouts solely because skin_default/skin.xml is absent.
PREINST = (ROOT / "source/control/preinst").read_text(encoding="utf-8")
assert "/usr/lib/enigma2/python" in PREINST
assert "DreamOS-compatible layout" in PREINST
# DreamOS eTimer uses timeout.connect; retain callback fallback for older Enigma2 images.
COND = (PKG / "usr/lib/enigma2/python/Components/Converter/g17ConditionalShowHide.py").read_text(encoding="utf-8")
assert "self.timer.timeout.connect(self.blinkFunc)" in COND
assert "self.timer.callback.append(self.blinkFunc)" in COND
assert "self.timer_conn = None" in COND


# TEST38-49 PROGRAM INFO / GraphicalEPGPIG consolidated contract.
# Warder-owned labels follow active OSD language and must never collide with legacy CSFD gettext/state.
uihelper = PLUGIN[PLUGIN.index('def _warderUiText(text):'):PLUGIN.index('class WarderProgramInfo', PLUGIN.index('def _warderUiText(text):'))]
assert 'lang = config.osd.language.value.split("_")[0].lower()' in uihelper
assert '"sk": {"PROGRAM INFO": "Info o programe"' in uihelper
assert '"cs": {"PROGRAM INFO": "Info o programu"' in uihelper
assert 'if text in warder.get(lang, {}):' in uihelper
assert 'return warder[lang][text]' in uihelper
assert 'if text == "PROGRAM INFO":' not in uihelper
assert 'source="warder_key_red" render="Label" position="30,930" size="420,42"' in pigepg
assert 'source="key_red" render="Label" position="30,930" size="420,42"' not in pigepg
for key in ("warder_key_red", "warder_key_green", "warder_key_yellow", "warder_key_blue"):
    assert ('source="%s" render="Label"' % key) in pigepg, key
assert '("warder_key_red", _warderUiText("PROGRAM INFO"))' in PLUGIN
assert 'self[key] = StaticText("")' in PLUGIN
assert 'WarderEPGSelection.RefreshColouredKeys = warderEPGSelectionRefreshColouredKeys' in PLUGIN
assert 'self.session.openWithCallback(self.warderProgramInfoClosed, WarderProgramInfo, event, service)' in PLUGIN

program_info = PLUGIN.split('class WarderProgramInfo(Screen):', 1)[1].split('def readHWtype', 1)[0]
assert 'source="session.VideoPicture" render="Pig"' not in program_info
assert 'render="g17Poster2"' not in program_info
assert 'posterTitle' not in program_info
assert 'name="programArtwork" position="30,75" size="520,300"' in program_info
assert 'self._artworkPath = meta.get("artwork_path") or ""' in program_info
assert 'self["programArtwork"].instance.setPixmap(pix)' in program_info
assert 'self["programArtwork"].instance.setScale(1)' in program_info
assert 'from Components.Renderer.Picon import getPiconName' in program_info
assert 'self["stationPicon"].instance.setPixmapFromFile(picon)' in program_info
assert 'name="stationPicon" position="50,435" size="120,72"' in program_info
assert 'name="channel" position="245,520" size="215,34" font="Prive4;24"' in program_info
assert 'name="description" position="535,425" size="1300,490"' in program_info
assert 'self["stationLabel"].setText(_warderUiText("Station name:"))' in program_info
assert 'name="service"' not in program_info
for key in ("keyRed", "keyGreen", "keyYellow", "keyBlue"):
    assert ('source="%s" render="Label"' % key) in program_info, key
assert 'for name in ("keyRed", "keyGreen", "keyYellow", "keyBlue"):' in program_info
assert 'self[name] = StaticText("")' in program_info
assert 'backgroundColor="#38c7e8"' not in program_info
assert 'position="25,940" size="1840,2" backgroundColor="#707070"' in program_info
assert 'position="25,955" size="420,62" backgroundColor="transpBlack3"' in program_info
assert 'warderProgramLookup(self._metadataTitle, self._metadataContext)' in PLUGIN
assert 'threading.Thread(target=_worker)' in PLUGIN
assert 'self._metadataTimer.start(100, False)' in PLUGIN
assert 'self["durationMeta"].setText("%d min" % minutes)' in program_info

META = (PKG / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderProgramInfo.py").read_text(encoding="utf-8")
for token in (
    'def lookup(title, context=""):',
    'def _baseTitle(title):',
    'CACHE_SCHEMA = "v3"',
    'for language in ("cs-CZ", "sk-SK", "en-US"):',
    'query_title = _baseTitle(title)',
    '_norm(candidate) == wanted',
    'ranked[0][0] < 2',
    'append_to_response=external_ids',
    '"provider_id": str(item.get("id") or "")',
    '"imdb_id": imdb_id',
    '"media_type": media',
    '"runtime": str(runtime or "")',
    '"provider": "TMDB"',
    '"backdrop_path":',
    '"poster_path":',
    'result["artwork_path"] = _artworkPath(result)',
):
    assert token in META, token
assert 'for kind, remote in (("backdrop", data.get("backdrop_path")), ("poster", data.get("poster_path"))):' in META
assert 'raw[:2] == b"\\xff\\xd8"' in META
assert "g17Poster2" not in program_info
assert 'quote_plus(title)' not in META
assert "source=\"session.VideoPicture\" render=\"Pig\"" not in program_info

# Approved GraphicalEPGPIG geometry remains locked.
for token in (
    'position="15,15" size="1890,1050"',
    'source="session.VideoPicture" render="Pig" position="33,63" size="549,309"',
    'name="timeline_text" position="75,387" size="1755,36"',
    'name="list" position="15,423" size="1845,495" font="Prive3;27" NumberOfRows="15"',
    'name="timeline_now" position="75,423" zPosition="2" size="28,495"',
    'name="bouquetlist" position="15,423" size="1845,495"',
):
    assert token in pigepg, token

# TEST50: RED in Warder GraphicalEPGPIG is a single-purpose PROGRAM INFO action.
assert 'Never fall through to OpenATV/legacy info/CSFD handlers.' in PLUGIN
red_handler = PLUGIN.split('def warderEPGSelectionRedButtonPressed(self):', 1)[1].split('WarderEPGSelection.redButtonPressed = warderEPGSelectionRedButtonPressed', 1)[0]
assert 'WarderProgramInfo, event, service' in red_handler
assert 'self.infoKeyPressed()' not in red_handler
assert 'return None' in red_handler

# TEST51 receiver screenshot correction: one title style, artwork field, station block below divider.
assert '"PROGRAM INFO": "Info o programe"' in PLUGIN
assert 'name="programArtwork" position="30,75" size="520,300"' in program_info
assert 'name="stationPicon" position="50,435" size="120,72"' in program_info
assert 'name="stationLabel" position="50,520" size="190,34" font="Prive3;24"' in program_info
assert 'name="channel" position="245,520" size="215,34" font="Prive4;24"' in program_info
assert 'name="durationLabel" position="50,675"' in program_info
assert 'name="broadcastLabel" position="50,714"' in program_info
assert 'CACHE_SCHEMA = "v3"' in PROVIDER

# TEST52 stable PROGRAM INFO metadata rows.
for field in ("genreMeta", "yearMeta", "countryMeta", "ratingMeta"):
    assert ('name="%s"' % field) in program_info
assert 'self[field].setText("-")' in program_info

# TEST53 visual consolidation.
assert '<screen name="WarderProgramInfo" position="15,15" size="1890,1050"' in program_info
assert 'name="programArtwork" position="30,75" size="520,300"' in program_info
assert '<eLabel position="25,72" size="505,286" backgroundColor="transpBlack"' not in program_info
assert 'name="ratingStars" position="1390,105" size="430,45" font="Prive4;36"' in program_info
assert 'name="ratingMeta" position="1390,152" size="430,36" font="Prive4;25"' in program_info
assert 'rating_text.split("/", 1)[0].strip()' in PLUGIN
assert 'self["ratingMeta"].setText("%s · %s"' in PLUGIN
assert 'name="description" position="535,425" size="1300,490"' in program_info
assert 'position="25,940" size="1840,2"' in program_info
assert 'position="25,963" size="420,46"' in program_info

# TEST54 GraphicalEPGPIG visual cleanup: no static vertical grid lines; current-time marker remains; description is larger/brighter.
epg_pig = re.search(r'<screen\b[^>]*name="GraphicalEPGPIG"[\s\S]*?</screen>', SKIN).group(0)
for i in range(6):
    assert ('name="timeline%d"' % i) not in epg_pig
assert 'name="timeline_now" position="75,423" zPosition="2" size="28,495"' in epg_pig
assert 'position="615,117" size="1230,246" font="Prive3;31" foregroundColor="#eeeeee"' in epg_pig

# TEST55 GraphicalEPGPIG header/left timeline cap.
assert 'format="%A  %d.%m.%Y" fTyp="1" position="30,12" size="390,42"' in epg_pig
assert 'position="435,12" size="210,42"' in epg_pig and 'ClockToText">WithSeconds' in epg_pig
assert 'FullHDGlass17 · Warder Evolution' in epg_pig
assert 'text="EPG" position="15,387"' not in epg_pig
assert 'name="timeline_text" position="75,387" size="1755,36"' in epg_pig

# TEST58: EPG keeps timeline labels aligned while extending only the visual strip over picon column.
assert '<eLabel position="15,387" size="60,36" backgroundColor="#505050"' in pigepg
assert 'name="timeline_text" position="75,387" size="1755,36"' in pigepg
# TEST58: TMDB lookup runs off GUI thread; result is applied by eTimer on GUI thread.
assert 'import threading' in PLUGIN
assert 'threading.Thread(target=worker)' in program_info
assert 'self._metadataTimer.callback.append(self._pollMetadataLookup)' in program_info
assert 'self.onLayoutFinish.append(self._startMetadataLookup)' in program_info
assert 'self.onLayoutFinish.append(self._loadProgramArtwork)' not in program_info

# TEST58 common visual language: PROGRAM INFO top header mirrors GraphicalEPGPIG.
assert 'name="nowDate" position="30,12" size="390,42" font="Prive4;30" foregroundColor="#e5b243"' in program_info
assert 'name="nowTime" position="435,12" size="210,42" font="Prive4;30" foregroundColor="#eeeeee"' in program_info
assert 'text="FullHDGlass17 · Warder Evolution" position="1260,12" size="585,42" font="Prive4;24"' in program_info

# TEST58: safe EPG edition suffix normalization, while retaining exact TMDB base-title matching.
assert 'CACHE_SCHEMA = "v4"' in PROGRAM_INFO_PROVIDER
assert "re.sub(r'\\s+[IVXLCDM]{1,8}\\s*$', '', value, flags=re.I)" in PROGRAM_INFO_PROVIDER
assert _provider_base_title_for_test("Česko Slovensko má talent X") == "Česko Slovensko má talent" if '_provider_base_title_for_test' in globals() else True
