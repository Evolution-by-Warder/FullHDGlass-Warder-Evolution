# -*- coding: utf-8 -*-
from Screens.Screen import Screen
from Components.config import config, configfile
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
import gettext
import random
from datetime import time
import datetime
import math
import os
import json
import time as time2
from Plugins.Extensions.setupGlass17.weather import PLUGINPATH, ColorLabel, ENA_W, ENA_C, convToC 
from Screens.InputBox import InputBox
from Components.Input import Input
from Components.Sources.List import List
from socket import socket, AF_INET, SOCK_STREAM
from Plugins.Extensions.setupGlass17.txt import EWEA, MoonInfo, EWEA_ERROR
from enigma import eTimer
from Tools.LoadPixmap import LoadPixmap
from Plugins.Extensions.setupGlass17.weaUtils import NO_WEATHER_PICON, setFcolor, fixUtf8, calcSun, ignZero, toLocale, ISP38, WLANG
ENAACC = True
try:
	if ISP38:
		from urllib.request import Request, urlopen
		from urllib.error import URLError, HTTPError
		from urllib.parse import quote, urlencode
		from Plugins.Extensions.setupGlass17.py38 import DG
	else:
		from urllib2 import Request, urlopen, URLError, HTTPError
		from urllib import quote, urlencode
		DG = unichr(176).encode("latin-1")
except Exception:
	ENAACC = False

DEFAULT_V = "----"
try:
	if config.plugins.setupGlass17.par49.value:
		E_weather_language = []
		E_weather_language = config.osd.language.value.split("_")
		if os.path.exists(PLUGINPATH + "locale/%s" % (E_weather_language[0])):
			_ = gettext.Catalog('eWeather', PLUGINPATH + 'locale', E_weather_language).gettext
except: pass
ENA_ANIM = False
try:
	if config.plugins.setupGlass17.par66.value:
		ENA_ANIM = True
except: pass

FORECAST = ("obsdate", "sunrise", "sunset", "txtshort", "weathericon","hightemperature","lowtemperature","windspeed","winddirection","maxuv")
EW_FILE = "/tmp/eWeather"
def Writelog(txt):
	log = PLUGINPATH+"e17.txt"
	try:
		f = open(log,"a")
		f.write("%s\n" % str(txt))
		f.close()
	except IOError: pass			
class mainmenu(Screen):

	def __init__(self, session):
		Eskin = """<screen position="0,0" size="1920,1080" title="Enhanced Weather" backgroundColor="black" flags="wfNoBorder" >			
			<widget name="Lnow1" font="Prive3;28" position="75,45" zPosition="2" size="225,300" valign="top" halign="right" foregroundColor="yellow" backgroundColor="black" transparent="1" />
			<widget name="now1" font="Prive3;28" position="315,45" zPosition="3" size="315,300" valign="top" halign="left" backgroundColor="black" transparent="1" />
			<widget name="Lnow2" font="Prive3;28" position="590,45" zPosition="2" size="225,300" valign="top" halign="right" foregroundColor="yellow" backgroundColor="black" transparent="1" />
			<widget name="now2" font="Prive3;28" position="830,45" zPosition="3" size="315,300" valign="top" halign="left" backgroundColor="black" transparent="1" />
			<widget name="weathertext" font="Prive3;25" position="1020,45" zPosition="3" size="183,90" valign="top" halign="center" foregroundColor="#00d100" backgroundColor="black" transparent="1" />
			<widget name="weathericon_9" position="1057,142" size="108,108" zPosition="0" alphatest="blend" />
			<widget name="sunrise0" font="Prive3;27" position="1252,112" zPosition="1" size="114,30" valign="top" halign="center" foregroundColor="#ffcc00" backgroundColor="black" transparent="1" />		
			<widget name="sunset0" font="Prive3;27" position="1369,112" zPosition="1" size="114,30" valign="top" halign="center" foregroundColor="#ff3300" backgroundColor="black" transparent="1" />		
			<widget name="temperature" font="Prive3;56" position="1222,160" zPosition="2" size="262,75" valign="center" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
			<widget name="moon_phase" font="Prive3;25" position="1562,105" zPosition="3" size="183,90" valign="top" halign="center" foregroundColor="#00d100" backgroundColor="black" transparent="1" />
			<widget name="moon_pict" position="1603,172" size="100,100" zPosition="0" alphatest="blend" />
			<eLabel position="1522,92" size="300,1" zPosition="8" backgroundColor="#006cbcf0" />
			<ePixmap position="1522,45" size="37,37" pixmap="/usr/share/enigma2/hd_glass17/buttons/blue25.png" zPosition="2" alphatest="blend" />
			<widget name="key_blue" position="1575,45" zPosition="3" size="285,60" valign="top" halign="left" font="Prive3;25" transparent="1" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" />
			<eLabel position="69,289" size="1782,1" zPosition="8" backgroundColor="#006cbcf0" />"""
		Eskin += '<ePixmap position="1252,45" zPosition="0" size="232,60" pixmap="'+PLUGINPATH+'pict/setrise.png" alphatest="blend" />\n'
		Eskin += '<widget name="init_txt" position="60,0" size="1800,1080" zPosition="9" font="Prive4;'
		if ENAACC:		
			Eskin += '75'
		else:
			Eskin += '55'
		Eskin += '" valign="center" halign="center" foregroundColor="white" backgroundColor="black" transparent="0" />\n'
		offset = 69
		for i in range(0,9):
			a = offset+i*198
			if i != 0:
				Eskin += '<eLabel position="'+str(1+a)+',307" size="1,735'+'" zPosition="8" backgroundColor="#006cbcf0" />\n'
			Eskin += '<ePixmap position="'+str(a)+',667" zPosition="0" size="198,381 " pixmap="'+PLUGINPATH+'pict/ewea3.png" alphatest="blend" />\n'
			for x in FORECAST:
				if x == "obsdate":
					Eskin += '<widget name="obsdate_'+str(i)+'" font="Prive3;25" position="'+str(a)+',300" zPosition="6" size="198,60" valign="center" halign="center" foregroundColor="#3399FF" backgroundColor="black" transparent="1" />\n'			
				elif x == "weathericon":
					Eskin += '<widget name="weathericon_'+str(i)+'" position="'+str(45+a)+',366" zPosition="0" size="108,108" alphatest="blend" />\n'
					Eskin += '<widget name="wDir_'+str(i)+'" position="'+str(51+a)+',930" zPosition="1" size="96,96" alphatest="blend" />\n'
				elif x == "txtshort":
					Eskin += '<widget name="txtshort_'+str(i)+'" font="Prive3;25" position="'+str(7+a)+',481" zPosition="1" size="183,120" valign="top" halign="center" foregroundColor="#00d100" backgroundColor="black" transparent="1" />\n'			
				elif x == "hightemperature":
					Eskin += '<widget name="hightemperature_'+str(i)+'" font="Prive3;31" position="'+str(99+a)+',615" zPosition="3" size="99,37" valign="center" halign="center" foregroundColor="#cc3300" backgroundColor="black" transparent="1" />\n'			
				elif x == "lowtemperature":
					Eskin += '<widget name="lowtemperature_'+str(i)+'" font="Prive3;31" position="'+str(a)+',615" zPosition="3" size="99,37" valign="center" halign="center" foregroundColor="#00d100" backgroundColor="black" transparent="1" />\n'			
				elif x == "windspeed":
					Eskin += '<widget name="windspeed_'+str(i)+'" font="Prive3;27" position="'+str(30+a)+',703" zPosition="1" size="168,30" valign="top" halign="center" foregroundColor="#26cfc0" backgroundColor="black" transparent="1" />\n'			
				elif x == "maxuv":
					Eskin += '<widget name="maxuv_'+str(i)+'" font="Prive3;27" position="'+str(85+a)+',763" zPosition="1" size="112,30" valign="top" halign="center" foregroundColor="#cc00c0" backgroundColor="black" transparent="1" />\n'			
				elif x == "sunrise":
					Eskin += '<widget name="sunrise_'+str(i)+'" font="Prive3;27" position="'+str(a)+',862" zPosition="1" size="99,30" valign="top" halign="center" foregroundColor="#ffcc00" backgroundColor="black" transparent="1" />\n'			
				elif x == "sunset":
					Eskin += '<widget name="sunset_'+str(i)+'" font="Prive3;27" position="'+str(99+a)+',862" zPosition="1" size="99,30" valign="top" halign="center" foregroundColor="#ff3300" backgroundColor="black" transparent="1" />\n'			
		Eskin += """</screen>""" 
		if config.plugins.setupGlass17.par174.value != "AutoColors" or config.plugins.setupGlass17.par175.value != "AutoColors" or config.plugins.setupGlass17.par176.value != "AutoColors" or config.plugins.setupGlass17.par177.value != "AutoColors":	
			tmp = Eskin.split("\n")
			a = ""
			for i in tmp:
				if 'name="obsdate_' in i and config.plugins.setupGlass17.par174.value != "AutoColors":
					a += setFcolor(i,config.plugins.setupGlass17.par174.value)
				elif 'name="txtshort_' in i and config.plugins.setupGlass17.par175.value != "AutoColors":
					a += setFcolor(i,config.plugins.setupGlass17.par175.value)
				elif 'name="maxuv' in i and config.plugins.setupGlass17.par176.value != "AutoColors":
					a += setFcolor(i,config.plugins.setupGlass17.par176.value)
				elif 'name="windspeed' in i and config.plugins.setupGlass17.par177.value != "AutoColors":
					a += setFcolor(i,config.plugins.setupGlass17.par177.value)
				else:
					a += i + "\n"
			Eskin = a
		self.skin = Eskin
		Screen.__init__(self, session)
		self.now = ("time","city","state","lat","lon","pressure","temperature","realfeel","humidity","weathertext","weathericon","windspeed","winddirection","visibility","uvindex")
		self.Wunits = {"temp":"", "dist":"", "speed":"", "pres":""}
		self["key_blue"] = Label(_("Select City"))                                   
		self.units = self.chckUnit()
		self["weathericon_9"] = Pixmap()
		self["temperature"] = ColorLabel("--")
		self["weathertext"] = Label(DEFAULT_V)
		self["init_txt"] = Label(({False:EWEA_ERROR, True:EWEA}[ENAACC]))
		self["now1"] = Label(DEFAULT_V)
		self["now2"] = Label(DEFAULT_V)
		self["sunrise0"] = Label(DEFAULT_V)
		self["sunset0"] = Label(DEFAULT_V)
		self['moon_pict'] = Pixmap()
		self['moon_phase'] = Label(DEFAULT_V)
		self["Lnow1"] = Label(_("Updated at")+":\n"+_("Pressure")+":\n"+_("Latitude")+":\n"+_("Longtitude")+":\n"+_("City")+":\n"+_("Location")+":")
		self["Lnow2"] = Label(_("Realfeel")+":\n"+_("Humidity")+":\n"+_("Wind")+":\n"+_("Visibility")+":\n"+_("Uvindex")+":")		
		self.location = "%s,sk,bratislava,297345" % WLANG[:2]	
		self.remainingTime = int(config.plugins.setupGlass17.par87.value)
		a = config.plugins.setupGlass17.par98.value
		if "," in a:
			if len(a.split(",")) == 4:
				self.location = a
		for i in range(0,9):
			for x in FORECAST:
				if x == "weathericon":
					self["%s_%s" % (x,i)] = Pixmap()
					self["wDir_%s" % i] = Pixmap()
				elif x in ("hightemperature","lowtemperature"):
					self["%s_%s" % (x,i)] = ColorLabel(DEFAULT_V)
				elif not x in ("winddirection"):
					self["%s_%s" % (x,i)] = Label(DEFAULT_V)
		self.waitTimer = eTimer()
		try:
			self.waitTimer_conn = self.waitTimer.timeout.connect(self.letsgo)
		except AttributeError:
			self.waitTimer.timeout.get().append(self.letsgo)
		if ENA_ANIM:
			self.animTimer = eTimer()
			try:
				self.animTimer_conn = self.animTimer.timeout.connect(self.__runAnim)
			except AttributeError:
				self.animTimer.timeout.get().append(self.__runAnim)
		self["actions"] = ActionMap(["SetupActions", "ColorActions"],
		{
			"blue": self.blueKey,
			"ok": self.exit,
			"yellow": self.exit,
			"red": self.exit,
			"cancel": self.exit
		}, -2)
		self.onLayoutFinish.append(self.startWait)

	def chckUnit(self):
		a = config.plugins.setupGlass17.par151.value
		if a != "0":
			return a
		old = config.plugins.setupGlass17.par98.value or ""
		if old[:1].lower() in ("c", "f"):
			return old[:1].lower()
		return "c"
		
	def startWait(self):
		self.setTitle(_("Enhanced Weather"))
		for i in range(0,10):
			self["weathericon_%s" % i].instance.setScale(1)
		self['moon_pict'].instance.setScale(1)
		if ENAACC:
			self.waitTimer.start(2000)

	def letsgo(self):
		self.waitTimer.stop()
		if ENA_ANIM:
			if self.animTimer.isActive():
				self.animTimer.stop()
			self.slide = {}
			self.pics = {}
			self.ena_s = 0

		def showWicon(val, what="_9"):
			val = str(val)
			if ENA_ANIM:
				path = config.plugins.setupGlass17.par39.value + "/animIconWeather/" + val
				x = int(what.replace("_", ""))
				self.slide[x] = 0
				self.pics[x] = []
				try:
					for name in sorted(os.listdir(path), key=lambda n: int(n.split('.')[0]) if n.split('.')[0].isdigit() else 9999):
						if name.endswith('.png'):
							self.pics[x].append(LoadPixmap(path + "/" + name))
				except Exception:
					pass
				if not self.pics[x]:
					self["weathericon" + what].instance.setPixmapFromFile(NO_WEATHER_PICON)
				else:
					self.ena_s += 1
			else:
				pix = config.plugins.setupGlass17.par39.value + "/weatherIcons/" + str(config.plugins.setupGlass17.par72.value) + "/" + val + ".png"
				if not os.path.isfile(pix):
					pix = NO_WEATHER_PICON
				self["weathericon" + what].instance.setPixmapFromFile(pix)

		def fmt_temp(v):
			try:
				n = int(round(float(v)))
				return ("+" if n > 0 else "") + str(n) + DG + self.Wunits["temp"]
			except Exception:
				return DEFAULT_V

		def wind_dir(deg):
			dirs = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")
			try:
				return dirs[int((float(deg) + 22.5) // 45) % 8]
			except Exception:
				return "N"

		def wmo_text(code):
			texts = {
				0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
				45: "Fog", 48: "Depositing rime fog", 51: "Light drizzle", 53: "Drizzle", 55: "Dense drizzle",
				56: "Freezing drizzle", 57: "Dense freezing drizzle", 61: "Slight rain", 63: "Rain", 65: "Heavy rain",
				66: "Freezing rain", 67: "Heavy freezing rain", 71: "Slight snow", 73: "Snow", 75: "Heavy snow",
				77: "Snow grains", 80: "Rain showers", 81: "Rain showers", 82: "Heavy rain showers",
				85: "Snow showers", 86: "Heavy snow showers", 95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with heavy hail"
			}
			return _(texts.get(int(code), "Unknown"))

		def wmo_icon(code, night=False):
			try: code = int(code)
			except Exception: return "3200"
			if code == 0: return "31" if night else "32"
			if code == 1: return "33" if night else "34"
			if code == 2: return "29" if night else "30"
			if code == 3: return "26"
			if code in (45,48): return "20"
			if code in (51,53,55,56,57): return "9"
			if code in (61,63,65,66,67,80,81,82): return "12"
			if code in (71,73,75,77,85,86): return "16"
			if code in (95,96,99): return "35"
			return "3200"

		def fetch_json(url):
			req = Request(url, headers={'User-Agent': 'FullHDGlass17/9.50-r10-Warder'})
			with urlopen(req, timeout=12) as response:
				raw = response.read()
			if not isinstance(raw, str):
				raw = raw.decode('utf-8', 'replace')
			return json.loads(raw)

		def resolve_location(value):
			# r9/r10 migration: accept the current coordinate format and legacy Enhanced Weather entries.
			if value and '|' in value:
				p = value.split('|')
				if len(p) >= 6 and p[2] and p[3]:
					return p[1], float(p[2]), float(p[3]), p[4], p[5]
			city = "Bratislava"
			if value and ',' in value:
				p = value.split(',')
				if len(p) >= 3 and p[2].strip():
					city = p[2].strip()
			elif config.plugins.setupGlass17.par13.getText() not in ("", "None"):
				city = config.plugins.setupGlass17.par13.getText()
			# Old Enhanced Weather records can end in the literal word "station".
			if city.lower().endswith(" station"):
				city = city[:-8].strip()
			url = "https://geocoding-api.open-meteo.com/v1/search?" + urlencode({'name': city, 'count': 10, 'language': WLANG[:2], 'format': 'json'})
			g = fetch_json(url)
			rows = g.get('results') or []
			if not rows:
				raise ValueError("City not found: " + city)
			r = rows[0]
			if r.get('latitude') is None or r.get('longitude') is None:
				raise ValueError("Incomplete location data: " + city)
			return r.get('name', city), float(r['latitude']), float(r['longitude']), r.get('country', ''), r.get('admin1', '')

		try:
			self.units = self.chckUnit()
			unit_f = self.units.lower() == 'f'
			self.Wunits = {"temp": ("F" if unit_f else "C"), "dist": " km", "speed": (" mph" if unit_f else " km/h"), "pres": " hPa"}
			city, lat, lon, country, admin = resolve_location(config.plugins.setupGlass17.par98.value)
			params = {
				'latitude': lat, 'longitude': lon, 'timezone': 'auto', 'forecast_days': 9,
				'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,is_day,weather_code,surface_pressure,wind_speed_10m,wind_direction_10m,visibility',
				'daily': 'weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,wind_speed_10m_max,wind_direction_10m_dominant',
				'temperature_unit': ('fahrenheit' if unit_f else 'celsius'),
				'wind_speed_unit': ('mph' if unit_f else 'kmh')
			}
			data = fetch_json("https://api.open-meteo.com/v1/forecast?" + urlencode(params))
			cur = data.get('current', {})
			code = cur.get('weather_code', -1)
			night = not bool(cur.get('is_day', 1))
			self["temperature"].setText(fmt_temp(cur.get('temperature_2m')))
			try: setColor("temperature", int(round(float(cur.get('temperature_2m')))), ENA_W)
			except Exception: pass
			self["weathertext"].setText(wmo_text(code))
			upd = str(cur.get('time', '')).replace('T', ' ')
			pressure = cur.get('surface_pressure', DEFAULT_V)
			self["now1"].setText("%s\\n%s%s\\n%.4f\\n%.4f\\n%s\\n%s" % (upd, pressure, self.Wunits['pres'], lat, lon, city, ", ".join([x for x in (admin, country) if x])))
			realfeel = fmt_temp(cur.get('apparent_temperature'))
			hum = str(cur.get('relative_humidity_2m', DEFAULT_V)) + "%"
			wd = wind_dir(cur.get('wind_direction_10m', 0))
			wind = str(int(round(float(cur.get('wind_speed_10m', 0))))) + self.Wunits['speed'] + ", " + wd
			vis = cur.get('visibility')
			vis = ("%.1f km" % (float(vis)/1000.0)) if vis not in (None, DEFAULT_V) else DEFAULT_V
			self["now2"].setText("%s\\n%s\\n%s\\n%s\\n%s" % (realfeel, hum, wind, vis, DEFAULT_V))
			showWicon(wmo_icon(code, night))
			a, x = MoonInfo()
			self['moon_pict'].instance.setPixmapFromFile(PLUGINPATH + "MoonPict/" + x)
			self['moon_phase'].setText(a)

			d = data.get('daily', {})
			for i in range(0, 9):
				try:
					date_s = d.get('time', [])[i]
					dt = datetime.datetime.strptime(date_s, '%Y-%m-%d')
					date_fmt = dt.strftime(config.plugins.setupGlass17.par185.value)
					self["obsdate_%s" % i].setText(toLocale(date_fmt))
					c = d.get('weather_code', [])[i]
					self["txtshort_%s" % i].setText(wmo_text(c))
					hi = d.get('temperature_2m_max', [])[i]
					lo = d.get('temperature_2m_min', [])[i]
					self["hightemperature_%s" % i].setText(fmt_temp(hi))
					self["lowtemperature_%s" % i].setText(fmt_temp(lo))
					try: setColor("hightemperature_%s" % i, int(round(float(hi))), ENA_W)
					except Exception: pass
					try: setColor("lowtemperature_%s" % i, int(round(float(lo))), ENA_C)
					except Exception: pass
					ws = d.get('wind_speed_10m_max', [])[i]
					wdir = wind_dir(d.get('wind_direction_10m_dominant', [])[i])
					self["windspeed_%s" % i].setText(str(int(round(float(ws)))) + self.Wunits['speed'] + ", " + wdir)
					wfile = PLUGINPATH + 'pict/' + wdir + '.png'
					if os.path.isfile(wfile): self["wDir_%s" % i].instance.setPixmapFromFile(wfile)
					uv = d.get('uv_index_max', [])[i]
					self["maxuv_%s" % i].setText("max %.1f" % float(uv))
					sr = d.get('sunrise', [])[i].split('T')[-1]
					ss = d.get('sunset', [])[i].split('T')[-1]
					self["sunrise_%s" % i].setText(sr)
					self["sunset_%s" % i].setText(ss)
					showWicon(wmo_icon(c, False), "_%s" % i)
				except Exception as e:
					Writelog("Open-Meteo daily[%s]: %s" % (i, e))
			if d.get('sunrise'):
				self["sunrise0"].setText(d['sunrise'][0].split('T')[-1])
			if d.get('sunset'):
				self["sunset0"].setText(d['sunset'][0].split('T')[-1])
			# Persist migrated location and a timestamp cache marker.
			new_loc = "c|%s|%s|%s|%s|%s" % (city, lat, lon, country, admin)
			if config.plugins.setupGlass17.par98.value != new_loc:
				config.plugins.setupGlass17.par98.value = new_loc
				config.plugins.setupGlass17.par98.save()
				configfile.save()
			try:
				with open(EW_FILE, 'w') as f: f.write(str(time2.time()))
			except Exception: pass
			self["init_txt"].hide()
			if ENA_ANIM and self.ena_s:
				self.animTimer.start(200)
		except Exception as e:
			Writelog("Open-Meteo: %s" % e)
			self["init_txt"].setText(_("Error") + ": Open-Meteo - " + str(e))

	def __runAnim(self):
		self.animTimer.stop()
		for x in range(0,len(self.slide)):
			a = len(self.pics[x])
			if a != 0:
				if self.slide[x] == a:
					self.slide[x] = 0
				self['weathericon_%s' % x].instance.setPixmap(self.pics[x][self.slide[x]])	
				self.slide[x] += 1
		a = 50
		try:
			a = config.plugins.setupGlass17.par159.value
		except: pass
		self.animTimer.start(a)

	def exit(self):
		if self.waitTimer is not None and self.waitTimer.isActive():
			self.waitTimer.stop()
		if ENA_ANIM:
			if self.animTimer.isActive():
				self.animTimer.stop()
			self.pics = None
			self.slide = None
			self.animTimer_conn = None
		self.waitTimer_conn = None
		self.waitTimer = None
		self.close()

	def blueKey(self):
		if ENAACC:
			self.session.openWithCallback(self.selAnswer, selectCity)

	def selAnswer(self, ret):        
		if ret: 
			if ret != "x" and ret != config.plugins.setupGlass17.par100.value:
				self.location = ret
				config.plugins.setupGlass17.par98.value = ret
				config.plugins.setupGlass17.par98.save()
				configfile.save()
				self.letsgo()

class selectCity(Screen):   

	skin = """
	<screen name="selectCity" position="center,center" size="1200,770" title="" backgroundColor="background" >
		<widget source="list" render="Listbox" position="15,15" zPosition="1" size="1170,660" scrollbarMode="showOnDemand" transparent="1" >
      <convert type="TemplatedMultiContent">
				{"template": [ MultiContentEntryText(pos = (0, 0), size = (1170, 60), flags = RT_HALIGN_LEFT, text = 0) ],"fonts": [gFont("Prive3", 32)],"itemHeight": 40}
			</convert>
		</widget>
	<widget name="key_red" position="0,690" size="300,80" zPosition="2" valign="center" halign="center" font="Prive3;33" transparent="1" foregroundColor="red" />
	<widget name="key_yellow" position="300,690" size="300,80" zPosition="2" valign="center" halign="center" font="Prive3;33" transparent="1" foregroundColor="yellow" />
	<widget name="key_blue" position="600,690" size="300,80" zPosition="2" valign="center" halign="center" font="Prive3;33" transparent="1" foregroundColor="blue" />
	<widget name="key_green" position="900,690" size="300,80" zPosition="2" valign="center" halign="center" font="Prive3;33" transparent="1" foregroundColor="green" />
	</screen>"""

	def __init__(self,session):
		self.skin = selectCity.skin
		self.session = session
		Screen.__init__(self, session)
		self.list = []
		self.fileName = "/etc/ewea_city_Code.txt"
		self["key_green"] = Label(_("Select City"))
		self["key_yellow"] = Label(_("Add City")+" (TXT)")
		self["key_red"] = Label(_("Delete City"))
		self["key_blue"] = Label(_("Change Temperature Unit"))
		if config.plugins.setupGlass17.par151.value != "0":
			self["key_blue"].hide()
		self['list'] = List(self.list)	
		self["actions"] = ActionMap(['WizardActions','ColorActions','VirtualKeyboardActions'],
		{
			"green": self.select,
			"ok": self.select,
			"yellow": self.yellowKey,
			"red": self.redKey,
			"blue": self.blueKey,
			'showVirtualKeyboard': self.KeyText,
			"back": self.exit
		})    
		self.onLayoutFinish.append(self.mainFnc)

	def exit(self): 
		self.close('x')
		
	def setWindowTitle(self):
		self.setTitle(_("Select City"))
		
	def select(self):
		selection = self['list'].getCurrent()
		if selection:
			self.close(str(selection[1]))
		self.exit()
		
	def mainFnc(self,w="",d=False):
		self.setWindowTitle()
		self.list = []
		allLines = []
		try:
			with open(self.fileName, "r") as f:
				lines = [x.strip() for x in f.readlines() if x.strip() and x.strip() != "None"]
			for value in lines:
				valid = ('|' in value and len(value.split('|')) >= 6) or (',' in value and len(value.split(',')) == 4)
				if not valid:
					continue
				if d and value == w:
					continue
				allLines.append(value)
				if '|' in value:
					p = value.split('|'); label = p[1] + (", " + p[5] if p[5] else "") + (", " + p[4] if p[4] else "")
				else:
					p = value.split(','); label = p[2]
				self.list.append((str(len(self.list)+1) + ".    " + label, value))
			with open(self.fileName, "w") as f:
				f.write(("\n".join(allLines) + "\n") if allLines else "None\n")
		except Exception as e:
			Writelog("city list: %s" % e)
		if not self.list:
			self.list = [(_('None city founded'), 'x')]
		self['list'].list = self.list

	def blueKey(self):
		if config.plugins.setupGlass17.par151.value == "0":
			selection = self['list'].getCurrent()
			if selection and selection[1] != "x":
				self.mainFnc(selection[1])

	def redKey(self):
		selection = self['list'].getCurrent()
		if selection and selection[1] != "x":
			self.mainFnc(selection[1],True)
		
	def KeyText(self):
		self.yellowKey(True)

	def yellowKey(self,vc=False):
		if vc:
			from Screens.VirtualKeyBoard import VirtualKeyBoard
			self.session.openWithCallback(self.changeCityAnswer, VirtualKeyBoard, title=_("Please enter a city name")+": ", text="banska bystrica")
		else:
			self.session.openWithCallback(self.changeCityAnswer, InputBox, title=_("Please enter a city name")+": ", text="banska bystrica                   ", maxSize=50, type=Input.TEXT)

	def changeCityAnswer(self, name):
		if name is None and name != "":
			return		
		self.session.openWithCallback(self.callbackNewCity, addSelectCity, name)

	def callbackNewCity(self, ret):
		if ret != "x":
			try:
				f = open(self.fileName,"a")
				f.write(ret+"\n")		
				f.close()
			except: pass				
			self.mainFnc()				
				
class addSelectCity(Screen):
	skin = """<screen position="center,center" size="1500,920" title="Select city">
		<widget source="list" render="Listbox" position="10,10" zPosition="1" size="1480,900" scrollbarMode="showOnDemand" transparent="1" >
      <convert type="TemplatedMultiContent">
				{"template": [ MultiContentEntryText(pos = (0, 0), size = (1500, 100), flags = RT_HALIGN_LEFT, text = 0) ],"fonts": [gFont("Prive3", 32)],"itemHeight": 100}
			</convert>
		</widget>
		</screen>"""

	def __init__(self, session, name):
		Screen.__init__(self, session)
		self.name = name.strip()
		self.list = [(_('None city founded'), 'x')]
		self['list'] = List(self.list)
		self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'back': self.exit,'ok': self.retSel})
		self.onLayoutFinish.append(self.initList)					

	def exit(self): 
		self.close('x')

	def dwn(self, url):
		try:
			req = Request(url, headers={'User-Agent': 'FullHDGlass17/9.51-modern2'})
			data = urlopen(req, timeout=12).read()
			if not isinstance(data, str):
				data = data.decode('utf-8', 'replace')
			return data
		except Exception as e:
			Writelog("geocoding: %s" % e)
		return None

	def initList(self):
		self.setTitle(_("Select City"))
		url = "https://geocoding-api.open-meteo.com/v1/search?" + urlencode({'name': self.name, 'count': 20, 'language': WLANG[:2], 'format': 'json'})
		data = self.dwn(url)
		if data:
			try:
				obj = json.loads(data)
				c = []
				for r in obj.get('results', []):
					name = r.get('name', '')
					admin = r.get('admin1', '')
					country = r.get('country', '')
					lat = r.get('latitude')
					lon = r.get('longitude')
					if name and lat is not None and lon is not None:
						label = name + (", " + admin if admin else "") + (", " + country if country else "")
						value = "c|%s|%s|%s|%s|%s" % (name, lat, lon, country, admin)
						c.append((label, value))
				if c:
					self.list = c
			except Exception as e:
				Writelog("geocoding parse: %s" % e)
		self['list'].list = self.list

	def retSel(self):  
		del self.list
		selected = self['list'].getCurrent()
		if selected:
			self.close(selected[1])
		else: 
			self.close('x')
