#!/usr/bin/env python3
from pathlib import Path
import re

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
assert "unicodedata.normalize" in PLUGIN
assert "_citySearchKey" in PLUGIN
assert "geocoding-api.open-meteo.com/v1/search" in PLUGIN
assert "weather.service.msn.com/find.aspx" not in PLUGIN
assert 'country|' in PLUGIN
assert '/etc/city_Code-17.txt' in PLUGIN
assert "Open-Meteo city search" in PLUGIN
assert '"group|SK"' in PLUGIN and '"Slovensko"' in PLUGIN
assert '"group|CZ"' in PLUGIN and '"Česko"' in PLUGIN
assert '"group|EUROPE"' in PLUGIN and '"Krajiny Európy"' in PLUGIN
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
    "def refreshWeatherNow(", "def chckPigFont(", "def menusel(", "def changePIGres(",
    "def reloadCities(", "def openWeatherCityChoice(", "def weatherCityChoiceSelected(",
    "def findCity(", "def addNewLine(", "def restoreCfgFromFile(", "def updateChck(",
    "def findPicon(", "def showEnhancedInfo(", "def changeSkinXml(", "def changeScreenXml(",
):
    assert symbol in PLUGIN, symbol
for symbol in ("def changeCity(", "def download_xml(", "def resetWeather_values(", "def fixDate("):
    assert symbol in WEATHER, symbol
for symbol in ("def resolve_location(", "def geocode_legacy(", "def changeCityAnswer(", "def callbackNewCity("):
    assert symbol in EWEATHER, symbol
for symbol in ("def calcSun(", "def dewpoint(", "def wmoPicon(", "def wmoText(", "def windDir(", "def openMeteo("):
    assert symbol in WEAUTILS, symbol
for variant in ('"with PIG":"3"', '"simply PIG":"10"', '"PIG2":"11"', '"PIG4":"13"'):
    assert variant in PLUGIN, variant
