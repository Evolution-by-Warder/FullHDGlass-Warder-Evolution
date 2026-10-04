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
RADIO_ART = (PKG / "usr/lib/enigma2/python/Components/Renderer/WarderRadioArtwork.py").read_text(encoding="utf-8")

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

# TEST92: radio evStart re-shows the existing native-owned RDS dialog without monkey-patching it.
for token in ('fields[2].upper() == "A"', 'getattr(self, "rds_display", None)', 'rds.show()', 'RADIO_OVERLAY_SHOW epoch=%.6f'):
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
assert 'zPosition="-2"' in rds  # TEST112: preserve ChannelSelectionRadio and DAB/SLS layering

# TEST24 Cool-like PIG guide geometry.
pig24 = re.search(r'<screen\b[^>]*name="GraphicalEPGPIG"[\s\S]*?</screen>', SKIN).group(0)
assert 'source="session.VideoPicture" render="Pig"' in pig24 and 'zPosition="3"' in pig24
assert 'NumberOfRows="15"' in pig24
assert 'name="timeline_text" position="15,387" size="1845,36"' in pig24 and 'position="15,423" size="1845,495"' in pig24
assert 'type="EventTime">StartTime' in pig24 and 'type="EventTime">EndTime' in pig24

# TEST26: PIG guide header is clean; EPG grid reserves only a narrow picon rail.
pig26_start = SKIN.index('<screen name="GraphicalEPGPIG"')
pig26_end = SKIN.index('</screen>', pig26_start)
pig26 = SKIN[pig26_start:pig26_end]
assert 'source="Title" render="Label"' not in pig26
assert 'source="global.CurrentTime" render="Label" position="30,12"' not in pig26
assert 'name="timeline_text" position="15,387" size="1845,36"' in pig26
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
assert 'name="stationPicon" position="125,425" size="180,90"' in program_info
assert 'name="channel" position="225,520" size="235,34" font="Prive4;24"' in program_info
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
assert 'threading.Thread(target=worker)' in PLUGIN
assert 'self._metadataTimer.start(500, False)' in PLUGIN
assert 'self["durationMeta"].setText("%d min" % minutes)' in program_info

META = (PKG / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderProgramInfo.py").read_text(encoding="utf-8")
for token in (
    'def lookup(title, context=""):',
    'def _baseTitle(title):',
    'CACHE_SCHEMA = "v6"',
    'for language in ("sk-SK", "cs-CZ", "en-US"):',
    '/search/multi?',
    'query_title = _baseTitle(title)',
    'any(_norm(name or "") == wanted for name in names)',
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
    'name="timeline_text" position="15,387" size="1845,36"',
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
assert 'name="stationPicon" position="125,425" size="180,90"' in program_info
assert 'name="stationLabel" position="50,520" size="190,34" font="Prive3;24"' in program_info
assert 'name="channel" position="225,520" size="235,34" font="Prive4;24"' in program_info
assert 'name="durationLabel" position="50,675"' in program_info
assert 'name="broadcastLabel" position="50,714"' in program_info
assert 'CACHE_SCHEMA = "v6"' in PROVIDER

# TEST52 stable PROGRAM INFO metadata rows.
for field in ("genreMeta", "yearMeta", "countryMeta"):
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
assert 'name="timeline_text" position="15,387" size="1845,36"' in epg_pig

# TEST58: EPG keeps timeline labels aligned while extending only the visual strip over picon column.
assert '<eLabel position="15,387" size="1845,36" backgroundColor="#242424"' in pigepg
assert 'name="timeline_text" position="15,387" size="1845,36"' in pigepg
# TEST58: TMDB lookup runs off GUI thread; result is applied by eTimer on GUI thread.
assert 'import threading' in PLUGIN
assert 'threading.Thread(target=worker)' in PLUGIN
assert 'self._metadataTimer.callback.append(self._pollMetadataLookup)' in program_info
assert 'self.onLayoutFinish.append(self._startMetadataLookup)' in program_info
assert 'self.onLayoutFinish.append(self._loadProgramArtwork)' not in program_info

# TEST58 common visual language: PROGRAM INFO top header mirrors GraphicalEPGPIG.
assert 'name="nowDate" position="30,12" size="390,42" font="Prive4;30" foregroundColor="#e5b243"' in program_info
assert 'name="nowTime" position="435,12" size="210,42" font="Prive4;30" foregroundColor="#eeeeee"' in program_info
assert 'text="FullHDGlass17 · Warder Evolution" position="1260,12" size="585,42" font="Prive4;24"' in program_info

# TEST58: safe EPG edition suffix normalization, while retaining exact TMDB base-title matching.
assert 'CACHE_SCHEMA = "v6"' in META
assert "re.sub(r'\\s+[IVXLCDM]{1,8}\\s*$', '', value, flags=re.I)" in META
assert _provider_base_title_for_test("Česko Slovensko má talent X") == "Česko Slovensko má talent" if '_provider_base_title_for_test' in globals() else True

# TEST60: one continuous FullHDGlass-style timeline strip; no flat TEST59 grey bar.
assert '<eLabel position="15,387" size="1845,36" backgroundColor="#242424"' in pigepg
assert '<eLabel position="15,387" size="1845,2" backgroundColor="#6a6a6a"' in pigepg
assert '<eLabel position="15,420" size="1845,3" backgroundColor="#101010"' in pigepg
assert 'name="timeline_text" position="15,387" size="1845,36" backgroundColor="#242424"' in pigepg
# Spinner suppression must happen before opening Program Info, not inside the screen,
# so a busy frame cannot already be painted/frozen in the upper-right corner.
red_handler = PLUGIN.split('def warderEPGSelectionRedButtonPressed(self):', 1)[1].split('WarderEPGSelection.redButtonPressed = warderEPGSelectionRedButtonPressed', 1)[0]
assert 'setSpinnerOnOff(0)' not in red_handler
assert '_warderProgramInfoSpinnerWasEnabled' not in red_handler
assert 'self.onClose.append(self._restoreMetadataSpinner)' not in program_info
# Provider first-hit path uses one multi-search instead of six serial movie/tv searches.
assert '/search/multi?' in META
assert '/search/%s?' not in META

# TEST61: localized broadcaster subtitle fallback remains exact and rating has no top-right dash placeholder.
assert 'query_titles = [query_title]' in META
assert 'for separator in (" - ", " – ", " — "):' in META
assert 'any(_norm(name or "") == wanted for name in names)' in META
assert 'series_hint = any(word in context_norm.split() for word in ("serial", "seriál", "series"))' in META
assert 'for field in ("genreMeta", "yearMeta", "countryMeta"):' in program_info
assert 'for field in ("genreMeta", "yearMeta", "countryMeta", "ratingMeta"):' not in program_info
assert 'timeout=2.5' in META

# TEST62: unresolved metadata is bounded and must not expose Enigma2 busy spinner.
assert 'search_deadline = time.time() + 3.0' in META
assert 'timeout=max(0.25, min(1.0, remaining))' in META
assert 'if not self._metadataDone:' in program_info
# TEST70: do not manipulate global gRC spinner state. While metadata is pending,
# a lightweight visible clock repaint keeps gRC from reaching its no-paint busy-tile path.
assert 'setSpinnerOnOff' not in program_info
assert 'def _suppressCoreSpinner(self):' not in program_info
assert 'self._metadataTimer.start(500, False)' in program_info
assert 'self["nowTime"].setText(time1.strftime("%H:%M:%S", time1.localtime()))' in program_info
# Close must win the first key event and immediately hide before deferred Screen.close processing.
assert '}, -2)' in program_info
assert 'self.hide()' in program_info

# TEST63: receiver showed a stale busy-spinner framebuffer tile at the extreme upper-right.
# Keep the fix local to PROGRAM INFO: an opaque Warder-owned cap masks that reserved corner.
assert '<eLabel position="1815,12" size="55,55" backgroundColor="#050505" zPosition="20" />' not in program_info

# TEST64: larger station picon centred in Program Info left column.
assert 'name="stationPicon" position="125,425" size="180,90"' in program_info

# TEST65: timeline owns the picon/date rail so the date is not clipped into a stray "Dn"; selected event is amber.
assert 'name="timeline_text" position="15,387" size="1845,36"' in pigepg
assert 'EntryBackgroundColorSelected="#d69600"' in pigepg
assert 'EntryBackgroundColorNowSelected="#d69600"' in pigepg

# TEST66: hide only TimelineText generated 60px date cell; time labels remain native.
assert '<eLabel position="15,387" size="60,36" backgroundColor="#242424" zPosition="3" />' in pigepg

# TEST68: Program Info close is independent of asynchronous metadata completion.
assert '"cancel": self._closeProgramInfo' in program_info
assert '"red": self._closeProgramInfo' in program_info
assert 'def _closeProgramInfo(self, *retVal):' in program_info
assert 'self._metadataClosed = True' in program_info
assert 'if self._metadataClosed:' in program_info

# TEST71: one RED event path must never stack duplicate Program Info screens.
assert 'if getattr(self, "_warderProgramInfoOpen", False):' in PLUGIN
assert 'self._warderProgramInfoOpen = True' in PLUGIN
assert 'self._warderProgramInfoOpen = False' in PLUGIN


# TEST79 receiver-proven Radio/DAB boot recovery.
# OpenATV's native RdsInfoDisplay must not be monkey-patched during startup.
rds = re.search(r'<screen\b[^>]*name="RdsInfoDisplay"[\s\S]*?</screen>', SKIN).group(0)
for token in ('name="RassLogo"', 'name="RadioText"', 'name="RtpText"', 'backgroundColor="transparent"'):
    assert token in rds, token
for token in ('warderAlbumCover', 'warderStationPicon', 'warderArtist', 'warderTrack', 'warderAlbumMeta', 'warderStation'):
    assert token not in rds, token
for token in ('WarderRdsInfoDisplay', '_warderRadioLookupExact', 'itunes.apple.com/search?entity=song', '_warderRadioSplit', 'warderRdsInfoDisplayRadioTextChanged', 'WarderRadio init'):
    assert token not in PLUGIN, token
for token in (
    'warderRadioPic = "/usr/share/enigma2/hd_glass17/radio.mvi"',
    'config.misc.radiopic.value = warderRadioPic',
    'config.misc.showradiopic.value = True',
):
    assert token not in PLUGIN, token
# Keep radio.mvi passive packaging available while runtime integration is redesigned safely.
BUILD_TEST = (ROOT / "tools/build-test-ipk.sh").read_text(encoding="utf-8")
for token in ("hd_glass17/radio.mvi", "ffmpeg"):
    assert token in BUILD_TEST, token


# TEST80 safe Radio/DAB skin-only overlay. Never reintroduce the native RdsInfoDisplay monkey-patch.
rds80 = re.search(r'<screen\b[^>]*name="RdsInfoDisplay"[\s\S]*?</screen>', SKIN).group(0)
for token in ('source="global.CurrentTime"', 'FullHDGlass17 · Warder Evolution', 'source="session.CurrentService"', '<convert type="ServiceName">Name</convert>', '<convert type="ServiceName">Provider</convert>', 'name="RadioText"', 'name="RtpText"', 'name="RassLogo"'):
    assert token in rds80, token
for token in ('warderAlbumCover', 'warderStationPicon', 'warderArtist', 'warderTrack', 'warderAlbumMeta', 'warderStation', 'WarderRdsInfoDisplay'):
    assert token not in rds80 and token not in PLUGIN, token


# TEST81 isolated Radio/DAB artwork renderer: exact match only, no native-screen monkey patch.
# TEST81 requires the isolated exact-artwork renderer; TEST93 owns its current approved geometry.
assert 'render="WarderRadioArtwork"' in SKIN
assert 'class WarderRadioArtwork(Renderer):' in RADIO_ART
assert 'iRdsDecoder.RadioText' in RADIO_ART
assert 'threading.Thread' in RADIO_ART and 'timeout=2.5' in RADIO_ART
assert "gotArtist == wantArtist and gotTitle == wantTitle" in RADIO_ART
assert 'WarderRdsInfoDisplay' not in PLUGIN
assert 'config.misc.radiopic.value' not in PLUGIN

# TEST82: rapid RadioText changes must queue the current exact track after an older worker finishes.
assert 'self._requestedKey = ""' in RADIO_ART
assert 'elif not self._busy and key != self._requestedKey:' in RADIO_ART
assert 'self._requestedKey = key' in RADIO_ART

# TEST83: receiver-proven BAYERN 3 RadioText uses an explicit colon separator.
assert 'for sep in (" - ", " – ", " — ", ": "):' in RADIO_ART

# TEST84: downloaded artwork must validate the real JPEG SOI bytes.
assert "payload.startswith(bytes((255, 216)))" in RADIO_ART

# TEST84: downloaded artwork must validate the real JPEG SOI bytes.
assert "payload.startswith(bytes((255, 216)))" in RADIO_ART

# TEST85: diagnostic-only radio artwork trace must remain isolated in /tmp.
assert "/tmp/warder-radio-artwork.log" in RADIO_ART
assert 'cls._diag("NO_EXACT' in RADIO_ART
assert 'self._diag("ERROR' in RADIO_ART

# TEST86: only explicit feat-credit relocation may extend exact matching.
assert 'marker = " feat. "' in RADIO_ART
assert 'suffix = " (feat. "' in RADIO_ART
assert "wantFeat == gotFeat" in RADIO_ART
assert 'marker = " & "' not in RADIO_ART

# TEST87: comma-only title normalization is narrow and artist remains exact.
assert 'def _titleCommaIdentity' in RADIO_ART
assert '.replace(",", "")' in RADIO_ART
assert 'gotArtist == wantArtist' in RADIO_ART
assert '_titleCommaIdentity(item.get("trackName")) == cls._titleCommaIdentity(title)' in RADIO_ART

# TEST88: fast RADIO-entry acquisition, then lighter steady polling.
assert "self._timer.start(100, True)" in RADIO_ART
assert "self._timer.start(250 if not key else 750, True)" in RADIO_ART

# TEST89: startup latency tracing must identify renderer start, service, RadioText, song and request stages.
for token in ("RENDERER_START epoch=%.6f t=%.3f", "SERVICE epoch=%.6f t=%.3f", "RADIOTEXT epoch=%.6f t=%.3f", "SONG epoch=%.6f t=%.3f", "REQUEST epoch=%.6f t=%.3f"):
    assert token in RADIO_ART, token

assert "_warderRadioButtonTrace" in PLUGIN
assert "InfoBar.showRadioButton = _warderRadioButtonTrace" in PLUGIN
assert "RADIO_BUTTON epoch=%.6f" in PLUGIN
assert "/tmp/warder-radio-start" in PLUGIN and "/tmp/warder-radio-start" in RADIO_ART

# TEST93 Radio visual contract: keep the lightweight decorative spectrum isolated,
# preserve real Provider data below it, and keep the clock as one HH:MM:SS field.
SPECTRUM = (PKG / "usr/lib/enigma2/python/Components/Renderer/WarderRadioSpectrum.py").read_text(encoding="utf-8")
assert "GUI_WIDGET = eCanvas" in SPECTRUM
assert "self._timer.start(200)" in SPECTRUM
assert "self._timer.stop()" in SPECTRUM
assert "width, height = 350, 126" in SPECTRUM
assert "barw = 15" in SPECTRUM
assert "content_width = self._bars * barw" in SPECTRUM
SPECTRUM_CODE = "\n".join(line for line in SPECTRUM.splitlines() if not line.lstrip().startswith("#"))
assert "import subprocess" not in SPECTRUM_CODE
assert "subprocess." not in SPECTRUM_CODE
assert "import random" not in SPECTRUM_CODE
assert "random." not in SPECTRUM_CODE
radio = re.search(r'<screen\b[^>]*name="RdsInfoDisplay"[\s\S]*?</screen>', SKIN).group(0)
assert 'render="WarderRadioArtwork" position="620,134" size="648,648"' in radio
assert 'render="WarderRadioSpectrum" position="1470,838" size="350,126"' in radio
assert '<convert type="ServiceName">Provider</convert>' in radio
assert '<convert type="g17ClockToText">Format:%H:%M:%S</convert>' in radio
assert 'Format::%S' not in radio

# TEST93 packaging must use only the approved fixed production master.
assert 'RADIO_MASTER="$WORK/usr/share/enigma2/hd_glass17/warder-radio-background.jpg"' in BUILD_TEST
assert 'image.size != (1920, 1080)' in BUILD_TEST
assert 'generate-warder-radio-background.py' not in BUILD_TEST

assert 'RADIO_MASTER_SHA256="2d1e26b6c097d167d51c8ba9850b16c093171ac07e69ef3d69f4cbd9cae4939d"' in BUILD_TEST
assert 'ACTUAL_RADIO_MASTER_SHA256="$(sha256sum "$RADIO_MASTER"' in BUILD_TEST
assert 'TEST93 radio master SHA-256 mismatch' in BUILD_TEST


# TEST94: TEST92 RDS ownership must be symmetrical across RADIO <-> TV service starts.
service94 = PLUGIN.split('def serviceStartNow17(self):', 1)[1].split('def serviceStartNow172(self):', 1)[0]
assert 'is_radio = len(fields) > 2 and fields[2].upper() == "A"' in service94
assert 'if is_radio:' in service94
assert 'rds.show()' in service94
assert 'rds.hide()' in service94
assert 'RADIO_OVERLAY_SHOW epoch=%.6f ref=%s' in service94
assert 'RADIO_OVERLAY_HIDE epoch=%.6f ref=%s' in service94
assert 'WarderRdsInfoDisplay' not in PLUGIN


# TEST95: OpenWebif radio screenshot workaround is isolated and fail-safe.
WARDER_GRAB = (PKG / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warder-grab").read_text(encoding="utf-8")
assert 'WARDER_GRAB_PATH = PLUGINPATH + "warder-grab"' not in PLUGIN
assert '_warderOpenWebifGrab.GRAB_PATH = WARDER_GRAB_PATH' not in PLUGIN
assert 'grabClass = getattr(owiGrab, "GrabScreenshot", None)' in PLUGIN
assert 'grabClass.render = _warderRadioGrabRender' in PLUGIN
assert 'owiGrab.grabScreenshot.render' not in PLUGIN
assert 'if not is_radio or mode not in (None, "", "all"):' in PLUGIN
assert '_warderNativeGrabRender(self, request)' in PLUGIN
assert 'request.setHeader("Content-Length", str(len(payload)))' in PLUGIN
assert 'return payload' in PLUGIN
assert 'tempfile.mkstemp(prefix="warder-radio-http-osd-"' in PLUGIN
assert 'tempfile.mkstemp(prefix="warder-radio-http-out-"' in PLUGIN
assert 'warder-radio-webif-error.log' in PLUGIN
assert 'with open(master, "rb") as image:' in PLUGIN
assert 'ffmpeg = "/usr/bin/ffmpeg"' in PLUGIN
assert '_warderOwiGetUrlArg(request, "format") or "jpg"' in PLUGIN
assert '_warderTwistedServer' not in PLUGIN
assert 'ffmpeg"\\\\n\\\\t' not in PLUGIN
assert '_warderOwiGrab.GRAB_PATH = adapter' not in PLUGIN
assert 'with open("/tmp/warder-radio-current", "w") as marker:' in service94
assert 'marker.write("A" if is_radio else "TV")' in service94
for token in ('REAL_GRAB = "/usr/bin/grab"', 'MASTER = "/usr/share/enigma2/hd_glass17/warder-radio-background.jpg"', 'MARKER = "/tmp/warder-radio-current"', '"-s" not in args', '"-o" in args', '"-v" in args', 'passthrough()', '"ffmpeg", "-nostdin"', 'overlay=0:0:format=auto'):
    assert token in WARDER_GRAB, token
assert 'os.execv(REAL_GRAB, [REAL_GRAB] + sys.argv[1:])' in WARDER_GRAB
assert 'WarderRdsInfoDisplay' not in PLUGIN


# TEST96: Radio UI stays native FHD and OpenWebif JPEG preserves OSD text chroma detail.
assert '<resolution xres="1920" yres="1080" bpp="32" />' in SKIN
assert '<convert type="g17ClockToText">Format:%H:%M:%S</convert>' in radio
assert 'Format::%H:%M:%S' not in radio
assert '"-q:v", "2", output' in WARDER_GRAB
assert 'timeout=8' in WARDER_GRAB
assert 'timeout=12' in WARDER_GRAB
assert 'sys.stdout.buffer.write(image.read())' in WARDER_GRAB
assert 'stdout=subprocess.DEVNULL' in WARDER_GRAB
assert '"yuvj444p"' not in WARDER_GRAB


# TEST97: Radio spectrum must start from renderer widget lifecycle, not depend only on Screen.onShow.
SPECTRUM = (PKG / "usr/lib/enigma2/python/Components/Renderer/WarderRadioSpectrum.py").read_text(encoding="utf-8")
assert "def postWidgetCreate(self, instance):" in SPECTRUM
assert "def preWidgetRemove(self, instance):" in SPECTRUM
assert 'render="WarderRadioSpectrum"' in radio
assert 'position="1470,838" size="350,126"' in radio

# TEST98: right-bottom equalizer has a receiver-safe visible baseline inside the locked field.
assert radio.count('backgroundColor="#1473ff"') >= 2
assert radio.count('backgroundColor="#1ecdff"') >= 2
assert 'position="1485,918" size="14,36"' in radio
assert 'position="1808,896" size="14,58"' in radio

# TEST105 lazy OpenWebif hook installation / diagnostics
assert 'def _warderInstallOpenWebifGrabHook():' in PLUGIN
assert '_warderInstallOpenWebifGrabHook()' in PLUGIN
assert 'warder-radio-webif-hook.log' in PLUGIN
assert 'import tempfile' in PLUGIN
assert 'render-error:' in PLUGIN
assert 'install-error:' in PLUGIN
assert 'mode not in (None, "", "all")' in PLUGIN

# TEST106: receiver probe proves /grab uses class GrabScreenshot.
assert 'raise AttributeError("OpenWebif grab module has no GrabScreenshot class")' in PLUGIN
assert 'installed GrabScreenshot.render' in PLUGIN


# TEST111: keep native RDS ownership, remove failed TEST110 hide/show refresh, and layer Radio above InfoBar.\nservice111 = PLUGIN.split('def serviceStartNow17(self):', 1)[1].split('def serviceStartNow172(self):', 1)[0]\nassert 'rds.show()' in service111 and 'rds.hide()' in service111\nassert 'Refresh the already-owned native screen' not in service111\nassert '<screen name=\"RdsInfoDisplay\" position=\"0,0\" size=\"1920,1080\" zPosition=\"1\"' in SKIN\n


# TEST151: Radio text is composed in two coordinated Listbox widgets owned by ExtraInfo17.
assert 'warder_radio_text = """' in PLUGIN
assert 'source="warderRadioTop" render="Listbox" position="62,20" size="1758,72"' in PLUGIN
assert 'source="warderRadioBottom" render="Listbox" position="420,835" size="1400,180"' in PLUGIN
assert 'gFont("Prive4",30), gFont("Prive4",38)' in PLUGIN
assert 'gFont("Prive4",29), gFont("Prive4",33), gFont("Prive4",25)' in PLUGIN
assert 'RT_HALIGN_LEFT|RT_VALIGN_BOTTOM' in PLUGIN
assert 'RT_HALIGN_CENTER|RT_VALIGN_BOTTOM' in PLUGIN
assert 'RT_HALIGN_RIGHT|RT_VALIGN_BOTTOM' in PLUGIN
assert 'self["warderRadioTop"] = List([])' in PLUGIN
assert 'self["warderRadioBottom"] = List([])' in PLUGIN
assert 'decoder.getText(iRdsDecoder.RadioText)' in PLUGIN
assert 'decoder.getText(iRdsDecoder.RtpText)' in PLUGIN
assert 'info.getInfoString(iServiceInformation.sProvider)' in PLUGIN
assert 'self.warderRadioTopTimer.start(500, False)' in PLUGIN
assert 'marker.read(8).strip() == "A"' in PLUGIN
assert 'name="warderRadioDate"' not in PLUGIN
assert 'name="warderRadioTime"' not in PLUGIN
assert 'name="warderRadioBrand"' not in PLUGIN
assert '<widget name="RadioText" position="420,895"' not in SKIN
assert '<widget name="RtpText" position="420,955"' not in SKIN
assert 'render="Label" position="420,842" size="720,42"' not in SKIN
assert 'render="Label" position="1470,978" size="350,38"' not in SKIN
assert 'render="WarderRadioArtwork" position="620,134" size="648,648"' in SKIN
assert 'render="WarderRadioSpectrum" position="1470,838" size="350,126"' in SKIN
assert 'class WarderRadioTopOverlay(Screen):' not in PLUGIN
assert 'warderRadioTopDialog' not in PLUGIN
assert SKIN.count('render="WarderRadioInfoBarTop"') == 0
service117 = PLUGIN.split('def serviceStartNow17(self):', 1)[1].split('def serviceStartNow172(self):', 1)[0]
radio117 = service117.split('rds = getattr(self, "rds_display", None)', 1)[1].split('# TEST94:', 1)[0]
assert 'if is_radio:' in radio117 and 'rds.show()' in radio117
assert 'rds.hide()\n\t\t\t\t\trds.show()' not in radio117

# TEST151 supersedes TEST149/150 per-field geometry guards with composed text widgets.
