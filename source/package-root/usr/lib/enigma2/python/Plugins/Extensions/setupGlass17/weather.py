#######################################################################
#
#    Weather for Enigma2
#    Coded by shamann (c)2021
#
#    xml from http://weather.service.msn.com
#    sunset, sunrise calculated by NOAA formula
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#######################################################################
from Screens.Screen import Screen
from Components.Label import Label
from Components.Pixmap import Pixmap
import time as time1
import os
from Components.config import config
from skin import parseColor
import gettext
from xml.dom.minidom import parseString
import codecs
from datetime import datetime, date, time
import datetime as datetime1
try:
	from string import upper
except: pass
from enigma import eTimer, ePoint
from Tools.LoadPixmap import LoadPixmap
from Plugins.Extensions.setupGlass17.weaUtils import *
from Plugins.Extensions.setupGlass17.txt import MoonInfo
from time import strftime, localtime
if ISP38:
	from urllib.request import Request, urlopen
	from urllib.error import URLError, HTTPError
	from urllib.parse import quote
	from Plugins.Extensions.setupGlass17.py38 import DG
else:
	from urllib2 import Request, urlopen, URLError, HTTPError
	from urllib import quote
	DG = unichr(176).encode("latin-1")
ENA_MSN = chMSN()
if not ENA_MSN:
	try:
		import simplejson
	except:
		import json as simplejson
PLUGINPATH = "/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/"
def Writelog(txt):
	log = PLUGINPATH+"w17.txt"
	try:
		f = open(log,"a")
		f.write(("%s\n" % str(txt)))
		f.close()
	except IOError: pass
try:
	if config.plugins.setupGlass17.par49.value:
		weather_language = []
		weather_language = config.osd.language.value.split("_")
		if os.path.exists(PLUGINPATH + "locale/%s" % (weather_language[0])):
			_ = gettext.Catalog('weather', PLUGINPATH + 'locale', weather_language).gettext
except: pass
if os.path.isfile(PLUGINPATH + "wea.log"):
	try:
		os.remove(PLUGINPATH + "wea.log")
	except OSError:
		pass
ENA_ANIM = False
try:
	if config.plugins.setupGlass17.par56.value:
		ENA_ANIM = True
except: pass
ENA_W = 0
ENA_C = 0
try:
	if config.plugins.setupGlass17.par93.value != "AutoColors":
		ENA_W = 9999
	if config.plugins.setupGlass17.par94.value != "AutoColors":
		ENA_C = -9999
except: pass
ENA_10 = False
#try:
#	ENA_10 = not ENA_MSN and config.plugins.setupGlass17.par143.value
#except: pass
NO_WIND_PICON = "/usr/share/enigma2/hd_glass17/icons/no-wind.png"
UNKNOWN_STATE = _("...N/A...")
UNKNOWN_STATE_TEMP = "--" + DG
DICT_DAYS = {'Sun':_('Sun'), 'Mon':_('Mon'), 'Tue':_('Tue'), 'Wed':_('Wed'), 'Thu':_('Thu'), 'Fri':_('Fri'), 'Sat':_('Sat')}
DICT_DATE = {'Jan':'1', 'Feb':'2', 'Mar':'3', 'Apr':'4', 'May':'5', 'Jun':'6', 'Jul':'7', 'Aug':'8', 'Sep':'9', 'Oct':'10', 'Nov':'11', 'Dec':'12',
'1':_('January'), '2':_('February'), '3':_('March'), '4':_('April'), '5':_('May'), '6':_('Jun'), '7':_('Jul'), '8':_('August'), '9':_('September'), '10':_('October'), '11':_('November'), '12':_('December')}
DICT_TEXT = {'Light Snow':_('Light Snow Shower'), 'Snow Showers':_('Light Snow Shower'), 'Foggy':_('Fog'), 'Fog':_('Fog'), 'Sun':_('Sunny'), 'Clouds':_('Cloudy'), 'Light Rain with Thunder':_('Light Rain with Thunder'), 'Drizzle':_('Drizzle'), 'Showers in the Vicinity':_('Showers in the Vicinity'),
'Rain Shower':_('Rain Shower'), 'Thunderstorm':_('Thunderstorm'), 'Thunder in the Vicinity':_('Thunder in the Vicinity'), 'Thundershowers':_('Thundershowers'), 'Light Drizzle':_('Light Drizzle'), 'Thunder':_('Thunder'), 'Light Rain Shower':_('Light Rain Shower'),
'Isolated Thunderstorms':_('Isolated Thunderstorms'), 'Scattered Thunderstorms':_('Scattered Thunderstorms'), 'AM':_('AM'), 'PM':_('PM'), 'Mostly Clear':_('Mostly Clear'), 'Snow':_('Snow'), 'Thunderstorms':_('Thunderstorms'), 'Wind':_('Wind'), 'Windy':_('Wind'), 'T-Storms':_('Thunderstorms'),
'Showers':_('Showers'), 'Light Snow Shower':_('Light Snow Shower'), 'Rain':_('Rain'), 'Mostly Sunny':_('Mostly Sunny'), 'Sunny':_('Sunny'), 'Clearing':_('Clear'), 'Clear':_('Clear'), 'Thunderstorms':_('Thunderstorms'), 'Partly Cloudy':_('Partly Cloudy'), 'Mostly Cloudy':_('Mostly Cloudy'),
'Scattered Showers':_('Scattered Showers'), 'Few Showers':_('Few Showers'), 'Light Rain':_('Light Rain'), 'Showers':_('Showers'), 'Cloudy':_('Cloudy'), 'Fair':_('Fair'), 'Scattered Snow Showers':_('Scattered Snow Showers'), 'Wintry Mix':_('Wintry Mix'), 'Icy':_('Ice'), 'Ice':_('Ice'),
'Breezy':_('Breezy'), 'Rain Showers':_('Rain Shower'), 'Freezing Drizzle':_('Freezing Drizzle'), 'Freezing Rain':_('Freezing Rain'), 'Partly Sunny':_('Partly Cloudy'), 'Light Rain and Snow':_('Light Rain')+' / '+_('Snow'), 'Heavy Rain':_('Rain'), 'Rain And Snow':_('Rain')+' / '+_('Snow'), 'Rain and Snow':_('Rain')+' / '+_('Snow')}
#######################################################################
def convToC(t):
	return int((t - 32) * 5.0/9.0)

class ColorLabel(Label):
	def __init__(self, text=""):
		Label.__init__(self, text)

	def colorA(self,v):
		if self.instance:
			cc = ("#FEFEFE","#E5E5E5","#B9B9B9","#CC99CC","#CC66CC","#CC00CC","#9933CC","#6666CC","#3377FF","#1155FF","#0066FF","#0099FF","#00BDFE","#AAFFFF","#00F7C6","#18D78C","#00A963","#27A727","#2AC72A","#00FD00","#CBFE00","#FEFE00","#ECEC7D",
			"#E4CC66","#DCAE49","#FFAA00","#FF5500","#FF2200","#FF0000","#FF0033","#FF3333","#FF3366","#FFFFFF")
			if v > 35:
				v = 35
			elif v < -26:
				v = -26
			v += 26
			if v != 0:
				i = int(v/2)
				if i*2 != v:
					i += 1
			else:
				i = 0
			self.instance.setForegroundColor(parseColor(cc[i])) 

	def colorW(self):
		if self.instance:
			self.instance.setForegroundColor(parseColor(config.plugins.setupGlass17.par93.value))

	def colorC(self):
		if self.instance:
			self.instance.setForegroundColor(parseColor(config.plugins.setupGlass17.par94.value))

	def colorF(self):
		if self.instance:
			self.instance.setForegroundColor(parseColor(config.plugins.setupGlass17.par95.value))
#######################################################################
class WeatherScreen(Screen):                  

	def __init__(self, session, skin_type):
		Screen.__init__(self, session)
		self.skin_type = skin_type
		from Plugins.Extensions.setupGlass17.g17weather_skins import skinWea
		self.skin = skinWea.get(str(self.skin_type))
		if config.plugins.setupGlass17.par174.value != "AutoColors" or config.plugins.setupGlass17.par175.value != "AutoColors":
			tmp = self.skin.split("\n")
			a = ""
			for i in tmp:
				if 'name="Weather_Date' in i and config.plugins.setupGlass17.par174.value != "AutoColors":
					a += setFcolor(i,config.plugins.setupGlass17.par174.value)
				elif 'name="Weather_state' in i and config.plugins.setupGlass17.par175.value != "AutoColors":
					a += setFcolor(i,config.plugins.setupGlass17.par175.value)
				else:
					a += i + "\n"
			self.skin = a
		self.LIGHT = False
		if self.skin_type in ("2","4","8","10"):	
			self.LIGHT = True
		self.RESET_VALUES = UNKNOWN_STATE+"\n"+UNKNOWN_STATE+"\n"+UNKNOWN_STATE+"\n"+UNKNOWN_STATE+"\n"+UNKNOWN_STATE+"\n"+UNKNOWN_STATE+"\n"+UNKNOWN_STATE+ "%s" % ({True:"\n"+UNKNOWN_STATE, False:""}[self.LIGHT])
		try:	
			if config.plugins.setupGlass17.par71.value:
				from keymapparser import readKeymap
				from GlobalActions import globalActionMap
				readKeymap("/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/keymap3.xml")
				globalActionMap.actions['eventNextPrev'] = self.changeCity
		except: pass
		self.TITLE_S = self.readTitleType()
		self['Weather_items'] = Label(self.setLabels())
		self['Weather_values'] = Label(self.RESET_VALUES)
		self['Weather_wind'] = Pixmap()
		self['Weather_wind_label'] = Label(_("Wind direction"))
		self['Weather_sunrise'] = Label(UNKNOWN_STATE)
		self['Weather_sunset'] = Label(UNKNOWN_STATE)		
		self['moon_pict'] = Pixmap()
		self['moon_phase'] = Label(UNKNOWN_STATE)
		for x in range(0,6):
			self['Weather_picon%s' % x] = Pixmap()
			self['Weather_Temperature%s' % x] = ColorLabel(UNKNOWN_STATE_TEMP)
			if x != 0:
				self['Weather_Temperaturelow%s' % x] = ColorLabel(UNKNOWN_STATE_TEMP)
				self['Weather_Date%s' % x] = Label(UNKNOWN_STATE)
			self['Weather_state%s' % x] = Label(UNKNOWN_STATE)
		self.onShow.append(self.__wakeup1)
		self.onHide.append(self.__standby)
		self.weaTimer = eTimer()
		self.att = 1
		try:
			self.weaTimer_conn = self.weaTimer.timeout.connect(self.__wakeup)
		except AttributeError:
			self.weaTimer.timeout.get().append(self.__wakeup)
		if ENA_ANIM:
			self.animTimer = eTimer()
			try:
				self.animTimer_conn = self.animTimer.timeout.connect(self.__runAnim)
			except AttributeError:
				self.animTimer.timeout.get().append(self.__runAnim)		
		if ENA_10:
			self.Yidx = 0
			self.YTimer = eTimer()
			try:
				self.YTimer_conn = self.YTimer.timeout.connect(self.__startShow)
			except AttributeError:
				self.YTimer.timeout.get().append(self.__startShow)	
		self.units = chckUnit()
		self.remainingTime = int(config.plugins.setupGlass17.par87.value)
		self.enaNC = True
		self.defCity = config.plugins.setupGlass17.par13.value
		self.__atFirst = True
		self.data = None		
		self.onLayoutFinish.append(self.fixMSNlayout)
		if "w" in config.plugins.setupGlass17.par78.value:
			from Components.ActionMap import ActionMap
			self["actions"] = ActionMap(["ColorActions", "SetupActions", "DirectionActions"],
			{
            "green": self.close,
            "red": self.close,
            "ok": self.close,
            "cancel": self.close,
            "yellow": self.close,
            "blue": self.close
			}, -2)            
                                                                     	
	def fixMSNlayout(self):
		self.resetWeather_values("", False)
		if self.__atFirst and not self.LIGHT and ENA_MSN and not config.plugins.setupGlass17.par92.value:
			self.__atFirst = False
			tt = {}
			for i in ('Weather_picon','Weather_Temperature','Weather_Temperaturelow','Weather_Date','Weather_state'):
				self['%s5' % i].hide()
				tt['%s1X' % i] = self['%s1' % i].instance.position().x()
				tt['%s5X' % i] = self['%s5' % i].instance.position().x()
				tt['%s5Y' % i] = self['%s5' % i].instance.position().y()
				tt['%s5W' % i] = self['%s5' % i].instance.size().width()
				f = ((tt['%s5X' % i]-tt['%s1X' % i] - 3*tt['%s5W' % i])/3) + tt['%s5W' % i]
				self['%s4' % i].move(ePoint(tt['%s5X' % i], tt['%s5Y' % i]))
				self['%s3' % i].move(ePoint(2*f + tt['%s1X' % i], tt['%s5Y' % i]))
				self['%s2' % i].move(ePoint(f + tt['%s1X' % i], tt['%s5Y' % i]))
			tt = None
		for x in range(0,6):
			try:
				self['Weather_picon%s' % x].instance.setScale(1)
			except: pass
		try:
			self['moon_pict'].instance.setScale(1)
			self['Weather_wind'].instance.setScale(1)
		except: pass
                				
	def readTitleType(self):
		self.TITLE_S = False
		try:
			if config.plugins.setupGlass17.par173.value == "s":
				self.TITLE_S = True
		except: pass
		return self.TITLE_S and not self.LIGHT

	def setLabels(self):
		if self.TITLE_S:
			a = _("Location")+":\n" +_("Wind")+":\n"+_("Wind direction")+":\n"+_("Humidity")+":\n"+({False:_("Visibility"), True:_("Geo position")}[ENA_MSN])+":\n"+({False:_("Pressure"), True:_("Feels like")}[ENA_MSN])+":"
		else:
			a = "%s" % ({False:_("City")+":\n"+_("Location")+":\n", True:""}[self.LIGHT]) +_("Wind")+":\n"+_("Wind direction")+":\n"+_("Humidity")+":\n"+({False:_("Visibility"), True:_("Geo position")}[ENA_MSN])+":\n"+({False:_("Pressure"), True:_("Feels like")}[ENA_MSN])+":"+ "%s" % ({True:"\n"+_("Sunrise")+":\n"+_("Sunset")+":\n"+_("Update")+":", False:""}[self.LIGHT])
		return a

	def changeCity(self):
		config.plugins.setupGlass17.par13.handleKey(1)
		self.att = 1
		self.__wakeup()

	def __standby(self):
		if self.weaTimer.isActive():
			self.weaTimer.stop()
		if ENA_ANIM:
			if self.animTimer.isActive():
				self.animTimer.stop()
			self.pics = None	
			self.slide = None	
		if ENA_10:
			if self.YTimer.isActive():
				self.YTimer.stop()
			self.Yidx = 0
		if self.defCity != config.plugins.setupGlass17.par13.value:
			config.plugins.setupGlass17.par13.value = self.defCity
				
	def __wakeup1(self):
		self.TITLE_S = self.readTitleType()
		self['Weather_items'].setText(self.setLabels())
		self.att = 1
		self.defCity = config.plugins.setupGlass17.par13.value
		self.__wakeup()

	def __wakeup(self):
		def fixDate(d):
			a = d.split()
			if len(a) == 3:
				for ii in (1,2):
					if len(a[ii]) == 2 and a[ii][0] == "0":
						a[ii] = a[ii][1]
				x = datetime1.datetime(int(a[0]), int(a[1]), int(a[2]))
				d = config.plugins.setupGlass17.par186.value
				d = d.replace("%A ","%A\n").replace(" %A","\n%A")
				try:
					if config.plugins.setupGlass17.par188.value:			
						d = d.replace("%d","%-d").replace("%m","%-m")
				except: pass
				d = x.strftime(d)
			return toLocale(d)
		def parse_line(line, what):
			def parse_AM_PM(txt):
				ttmp = txt.split(' ')
				ttmptxt = txt.replace('AM ','').replace('PM ','')
				if len(ttmp) == 2 and ttmp[1] in DICT_TEXT and ttmp[0] in DICT_TEXT:
					return "%s %s" % (DICT_TEXT.get(ttmp[0]), DICT_TEXT.get(ttmp[1]))
				elif len(ttmp) == 3 and ttmptxt in DICT_TEXT and ttmp[0] in DICT_TEXT:
					return "%s %s" % (DICT_TEXT.get(ttmp[0]), DICT_TEXT.get(ttmptxt))
				return txt
			if not ENA_MSN:
				txt = line.split(what)[1].split('"')[1]			
			else:
				txt = line
			if what == "day" and txt in DICT_DAYS:
				return DICT_DAYS.get(txt)
			elif what == "sunrise" or what == "sunset" :
				if "pm" in txt or "am" in txt:
					timeFull = txt.lower()
					txt = txt.replace(("pm").lower(),"").replace(("am").lower(),"").replace(" ","")
					time = txt.split(':')
					if len(time[1]) == 1:
						time[1] += "0"
					if "pm" in timeFull and not "12" in time[0]:
						return "%s:%s" % (int(time[0])+12, time[1])
					elif "am" in timeFull and "12" in time[0]:
						return "0:%s" % time[1]
					return ignZero(txt)
			elif what == "country":
				return line.split('country="')[1].split('"')[0]
			elif what == "date":
				ttmp = txt.split(' ')
				if len(ttmp) == 3 and ttmp[1] in DICT_DATE:
					return fixDate("%s %s %s" % (ttmp[2], DICT_DATE.get(ttmp[1]), ttmp[0]))
				elif len(ttmp) == 7 and ttmp[2] in DICT_DATE:
					timeFull = ttmp[4]
					time = ttmp[4].split(':')
					if "pm" in ttmp[5].lower() and not "12" in time[0]:
						timeFull = "%s:%s" % (int(time[0])+12, time[1])
					elif "am" in ttmp[5].lower() and "12" in time[0]:
						timeFull = "0:%s" % time[1]
					timeFull = ignZero(timeFull)
					self.timeUpdate = "%s %s" % (timeFull, ttmp[6])
					return "%s, %s %s" % ((fixDate("%s %s %s" % (ttmp[3], DICT_DATE.get(ttmp[2]), ttmp[1]))).replace("\n"," "), timeFull, ttmp[6])
				else:
					return txt
			elif what == "text":
				txt = txt.replace(" Early","").replace(" Late","")
				if txt in DICT_TEXT:
					return DICT_TEXT.get(txt)
				elif ('am' in txt.lower() or 'pm' in txt.lower()) and not '/' in txt:
					return parse_AM_PM(txt)
				elif '/' in txt:
					ttmp = txt.split('/')
					ret = ""
					for x in range(0, len(ttmp)):
						if ttmp[x] in DICT_TEXT:
							ret += "%s / " % DICT_TEXT.get(ttmp[x])
						elif 'am' in ttmp[x].lower() or 'pm' in ttmp[x].lower():
							ret += "%s / " % parse_AM_PM(ttmp[x])              
						else:
							ret += "%s / " % ttmp[x]
					if ret != "":
						return ret[:-3]
					return _(txt)
			if txt != "":
				return txt
			else:
				return UNKNOWN_STATE
		def download_xml():
			try:
				os.remove(XML_FILE)
			except OSError:
				pass
			er = ""
			if netChck():
				self.units = chckUnit()
				req = config.plugins.setupGlass17.par13.value[1:]
				data = None
				if not req.startswith("wc:"):						
					req = quote(config.plugins.setupGlass17.par13.getText())
				if ENA_MSN:
					if req.startswith("wc:") or req.startswith("fr:"):
						req = "wealocations="+req
					else:						
						req = "weasearchstr="+req
					req = "https://weather.service.msn.com/data.aspx?src=outlook&weadegreetype=%s&culture=en-us&%s" % (self.units.upper(), req)
				else:
					apkey = "&appid=" + config.plugins.setupGlass17.par228.value
					req = "q=%s" % quote(config.plugins.setupGlass17.par13.getText())
					if self.units.upper() == "F":
						u = "imperial"
					else:
						u = "metric"					
					req = "https://api.openweathermap.org/data/2.5/weather?%s&lang=%s&units=%s%s" % (req, WLANG, u, apkey)
					self.req = "https://api.openweathermap.org/data/2.5/forecast?&lon=%s&lat=%s&units=" + "%s&exclude=hourly,minutely,current&lang=%s%s" % (u,WLANG,apkey)
				try:
					response = urlopen(req, timeout = 10)
				except HTTPError as e:
					er = _('Error') + ": " + str(e)
				except URLError as e:
					er = _('Error') + ": " + str(e)
				except: er = _('Error') + ": " + _("Website data reading timeout")
				else:
					data = response.read()
					response.close()
				if data is not None:			
					if ISP38:
						try:
							data = data.decode("ascii", "ignore")
						except: 
							data = data.decode("utf-8", "ignore")	            					
					localFile = open(XML_FILE, 'w')											
					localFile.write(data)
					localFile.close()				
					if ENA_MSN:					
						self.data = data									
				elif er == "":
					er = _('Error') + ": " + _("None data received from website")
			else:
				return _('Error') + ": " + _("Website is not responding")
			return er.replace('>','').replace('<','')
		self.weaTimer.stop()
		if not self.enaNC:
			return
		self.enaNC = False
		self.weather_dict = {'feelslike':UNKNOWN_STATE, 'long':UNKNOWN_STATE, 'lat':UNKNOWN_STATE, 'sunrise':UNKNOWN_STATE, 'sunset':UNKNOWN_STATE, 'wind_direction':UNKNOWN_STATE, 'templow5':UNKNOWN_STATE_TEMP, 'templow1':UNKNOWN_STATE_TEMP, 'templow2':UNKNOWN_STATE_TEMP, 'templow3':UNKNOWN_STATE_TEMP, 'templow4':UNKNOWN_STATE_TEMP, 'date5':UNKNOWN_STATE, 'date0':UNKNOWN_STATE, 'date1':UNKNOWN_STATE, 'date2':UNKNOWN_STATE, 'date3':UNKNOWN_STATE, 'date4':UNKNOWN_STATE, 'city':UNKNOWN_STATE, 'country':UNKNOWN_STATE, 'wind':UNKNOWN_STATE, 'humidity':UNKNOWN_STATE, 'visibility':UNKNOWN_STATE, 'pressure':UNKNOWN_STATE, 'text0':UNKNOWN_STATE, 'temp0':UNKNOWN_STATE_TEMP, 'picon0':"3200", 'text1':UNKNOWN_STATE, 'temp1':UNKNOWN_STATE_TEMP, 'picon1':"3200", 'text2':UNKNOWN_STATE, 'temp2':UNKNOWN_STATE_TEMP, 'picon2':"3200", 'text3':UNKNOWN_STATE, 'temp3':UNKNOWN_STATE_TEMP, 'picon3':"3200", 'text4':UNKNOWN_STATE, 'temp4':UNKNOWN_STATE_TEMP, 'picon4':"3200", 'text5':UNKNOWN_STATE, 'temp5':UNKNOWN_STATE_TEMP, 'picon5':"3200", 'text6':UNKNOWN_STATE, 'temp6':UNKNOWN_STATE_TEMP, 'picon6':"3200", 'text7':UNKNOWN_STATE, 'temp7':UNKNOWN_STATE_TEMP, 'picon7':"3200", 'text8':UNKNOWN_STATE, 'temp8':UNKNOWN_STATE_TEMP, 'picon8':"3200", 'text9':UNKNOWN_STATE, 'temp9':UNKNOWN_STATE_TEMP, 'picon9':"3200", 'text10':UNKNOWN_STATE, 'temp10':UNKNOWN_STATE_TEMP, 'picon10':"3200"}
		units_dict = {'wind':'', 'visibility':'', 'pressure':''}
		self.timeUpdate = UNKNOWN_STATE
		a = _('Error') + ": " + _("City") + " " + _('is not defined')
		try:
			lt = int(config.plugins.setupGlass17.par87.value)
			self.remainingTime = lt
			if config.plugins.setupGlass17.par13.value != "None":
				aa = config.plugins.setupGlass17.par152.value
				if config.plugins.setupGlass17.par89.value != config.plugins.setupGlass17.par13.value:
					config.plugins.setupGlass17.par89.value = config.plugins.setupGlass17.par13.value 
					a = download_xml()
				elif aa[0] != config.plugins.setupGlass17.par86.value:
					config.plugins.setupGlass17.par152.value = config.plugins.setupGlass17.par86.value + aa[1]
					a = download_xml()
				elif os.path.isfile(XML_FILE):
					fileTime = int((time1.time() - os.stat(XML_FILE).st_mtime)/60)
					if fileTime >= lt or os.path.getsize(XML_FILE) < 300:
						a = download_xml()
					else:
						self.remainingTime = lt - fileTime
				else:
					a = download_xml()
			else:
				self.resetWeather_values(a, False)
				return			
		except:
			a = _('Error') + ": " + _("Website is not responding")
		if not os.path.isfile(XML_FILE):
			self.resetWeather_values(a)
			return
		if ENA_MSN:
			data = self.data
			dom = dom0 = None
			try:
				dom = parseString(data)
				dom0 = dom.getElementsByTagName("weather")[0]			
			except:	pass
			if data is not None and dom is not None and dom0 is not None:
				idx = 1
				for x in dom0.getElementsByTagName('forecast'):
					ena = -1
					if not config.plugins.setupGlass17.par92.value:
						try:
							w = x.getAttribute("date") or datetime.now().strftime("%Y-%m-%d")
							ena = (datetime.now()-datetime.strptime("%s-23-59" % w,"%Y-%m-%d-%H-%M")).days
						except: pass
					if ena < 0 and idx < 6:
						try:
							w = str(x.getAttribute("high"))
							self.weather_dict["temp%s" % idx] = w
							w = str(x.getAttribute("low"))
							self.weather_dict["templow%s" % idx] = w        
							self.weather_dict["date%s" % idx] = fixDate(x.getAttribute("date").replace("-"," "))
							self.weather_dict["picon%s" % idx] = nigttime(parse_line(str(x.getAttribute("skycodeday")), 'code'))
							self.weather_dict["text%s" % idx] = parse_line(str(x.getAttribute("skytextday")), 'text')
						except: pass
						idx += 1
				d = dom.getElementsByTagName("weather")
				if len(d) != 0:
					w = str(d[0].getAttribute("weatherlocationname"))
					try:
						self.weather_dict["country"] = ({False:w, True:" ".join((w.split(",")[1]).strip().split())}["," in w])
					except: pass
					self.weather_dict["long"] = str(d[0].getAttribute("long"))
					self.weather_dict["lat"] = str(d[0].getAttribute("lat"))
					sunrise, sunset = calcSun(-float(self.weather_dict["long"]),float(self.weather_dict["lat"]))
					self.weather_dict['sunset'] = ignZero(time.strftime(sunset, '%H:%M'))
					self.weather_dict['sunrise'] = ignZero(time.strftime(sunrise, '%H:%M'))
				d = dom.getElementsByTagName("current")
				if len(d) != 0:
					self.weather_dict["feelslike"] = temperature_fix(str(d[0].getAttribute("feelslike")))
					w = str(d[0].getAttribute("temperature"))
					self.weather_dict["temp0"] = w            
					self.weather_dict["humidity"] = str(d[0].getAttribute("humidity")) + " %"
					w = d[0].getAttribute("winddisplay").replace("kmph","km/h") 
					w = w.split()
					units_dict = {'Northwest':(_('NW'),'NW'), 'Southwest':(_('SW'),'SW'), 'Southeast':(_('SE'),'SE'), 'Northeast':(_('NE'),'NE'), 'South':(_('S'),'S'), 'North':(_('N'),'N'), 'West':(_('W'),'W'), 'East':(_('E'),'E')}
					w_directPix = "U"
					try:
						self.weather_dict["wind"] = str("%s %s" % (w[0],w[1]))
						self.weather_dict["wind_direction"] = units_dict[w[2]][0]
						w_directPix = units_dict[w[2]][1]
					except: pass
					self.weather_dict["text0"] = parse_line(str(d[0].getAttribute("skytext")), 'text')
					self.weather_dict["picon0"] = nigttime(parse_line(str(d[0].getAttribute("skycode")), 'code'))
					self.weather_dict["date0"] = str("%s, %s" % (ignZero(d[0].getAttribute("observationtime")[:5]),parse_line(d[0].getAttribute("shortday"), 'day')))	
					self.timeUpdate = str("%s %s" % (ignZero(d[0].getAttribute("observationtime")[:5]),fixDate((d[0].getAttribute("date")).replace("-"," "))))
		else:
			idx = 1
			w_directPix = 'X'
			req = open(XML_FILE).read()
			try:
				if ISP38:	
					r = simplejson.loads(req)
				else:
					r = simplejson.loads(fixUtf8(req))
				self.weather_dict['country'] = r.get("sys",{}).get("country",UNKNOWN_STATE)
				self.weather_dict['sunrise'] = ignZero(strftime("%H:%M",localtime(r.get("sys",{}).get("sunrise",""))))
				self.weather_dict['sunset'] = ignZero(strftime("%H:%M",localtime(r.get("sys",{}).get("sunset",""))))
				if self.units.upper() == "F":
					units_dict['wind'] = 'mps'
					units_dict['visibility'] = 'miles'
					units_dict['pressure'] = "mbar"
				else:
					units_dict['wind'] = 'm/s'
					units_dict['visibility'] = 'km'
					units_dict['pressure'] = "hPa"
				self.weather_dict['wind'] = "%.1f" % r.get("wind",{}).get("speed",0)
				direct = int(r.get("wind",{}).get("deg",0))
				if direct >= 0 and direct <= 28:
					w_direct = _('N')
					w_directPix = 'N'
				elif direct >= 29 and direct <= 62:
					w_direct = _('NE')
					w_directPix = 'NE'
				elif direct >= 63 and direct <= 117:
					w_direct = _('E')
					w_directPix = 'E'
				elif direct >= 118 and direct <= 152:
					w_direct = _('SE')
					w_directPix = 'SE'
				elif direct >= 153 and direct <= 207:
					w_direct = _('S')
					w_directPix = 'S'
				elif direct >= 208 and direct <= 242:
					w_direct = _('SW')
					w_directPix = 'SW'
				elif direct >= 243 and direct <= 297:
					w_direct = _('W')
					w_directPix = 'W'
				elif direct >= 298 and direct <= 332:
					w_direct = _('NW')
					w_directPix = 'NW'
				else:
					w_direct = _('N')
					w_directPix = 'N'
				self.weather_dict['wind_direction'] = w_direct
				self.weather_dict['humidity'] = str(r.get("main",{}).get("humidity",0)) + " %"
				self.weather_dict['visibility'] = str(r.get("visibility",0)/1000)
				self.weather_dict['pressure'] = str(r.get("main",{}).get("pressure",0))
				ttmp = float(self.weather_dict['pressure'])
				if units_dict['pressure'] == "hPa" and ttmp > 10000: 
					self.weather_dict['pressure'] = str(int(ttmp / 33.8638866667))
				self.weather_dict['date0'] = ignZero(strftime("%H:%M",localtime(r["dt"])))
				self.weather_dict['text0'] = fixUtf8(r.get("weather",[{}])[0].get("description",""))
				idI = str(r.get("weather",[{}])[0].get("id","0"))
				i = r.get("weather",[{}])[0].get("icon","")
				self.weather_dict['picon0'] = nigttime(chckWidI(i,idI))
				self.weather_dict['temp0'] = str(int(round(r.get("main",{}).get("temp",0))))
				self.weather_dict["long"] = str(r.get("coord",{}).get("lon",0))
				self.weather_dict["lat"] = str(r.get("coord",{}).get("lat",0))
			except: pass
			if self.weather_dict["long"] != UNKNOWN_STATE and self.weather_dict["lat"] != UNKNOWN_STATE:
				idx = 1
				req = Request(self.req % (self.weather_dict["long"], self.weather_dict["lat"]))
				data = None
				try:
					response = urlopen(req, timeout = 10)
				except HTTPError as e:
					pass
				except URLError as e:
					pass
				except: pass
				else:
					data = response.read()
					response.close()
				try:
					if data is not None:
						if ISP38:	
							r = simplejson.loads(data)
						else:
							r=simplejson.loads(fixUtf8(data))
#						Writelog(r)
						tmin = 999  
						tmax = -999
						text = None
						for xx in r["list"]:  
							tmin = min(tmin, xx["main"]["temp_min"])
							tmax = max(tmax, xx["main"]["temp_max"])
							self.weather_dict['templow%s' % idx] = "%d" % tmin
							self.weather_dict['temp%s' % idx] = "%d" % tmax
							if "15:00:00" in xx["dt_txt"]:  
								idI = str(xx["weather"][0]["id"])
								x = xx["weather"][0]["icon"] + ".png"
								self.weather_dict['picon%s' % idx] = nigttime(chckWidI(x,idI))
								text = xx["weather"][0]["description"]
								self.weather_dict['text%s' % idx] = fixUtf8(xx["weather"][0]["description"])
							if "18:00:00" in xx["dt_txt"]:  
								idI = str(xx["weather"][0]["id"])
								x = xx["weather"][0]["icon"] + ".png"
								self.weather_dict['picon%s' % idx] = nigttime(chckWidI(x,idI))
								text = text if text else xx["weather"][0]["description"]
								self.weather_dict['text%s' % idx] = fixUtf8(text)                                
							if "21:00:00" in xx["dt_txt"]:  
								idI = str(xx["weather"][0]["id"])
								x = xx["weather"][0]["icon"] + ".png"
								self.weather_dict['picon%s' % idx] = nigttime(chckWidI(x,idI))
								text = text if text else xx["weather"][0]["description"]
								self.weather_dict['text%s' % idx] = fixUtf8(text)
								t = localtime(xx["dt"])                                   
								self.weather_dict['date%s' % idx] = fixDate(strftime("%Y %m %d",localtime(xx["dt"])))
								tmin = 888 
								tmax = -888
								text = None
								idx += 1
#						if r.get("daily",None) != None:
#							for i in r.get("daily",[]):
#								self.weather_dict['temp%s' % idx] = "%d" % round(i.get("temp",{}).get("max",""))
#								self.weather_dict['templow%s' % idx] =  "%d" % round(i.get("temp",{}).get("min",""))
#								self.weather_dict['date%s' % idx] = fixDate(strftime("%Y %m %d",localtime(i["dt"])))
#								x = i.get("weather",[{}])[0].get("icon","") + ".png"
#								self.weather_dict['text%s' % idx] = fixUtf8(i.get("weather",[{}])[0].get("description",""))
#								idI = str(i.get("weather",[{}])[0].get("id","0"))
#								self.weather_dict['picon%s' % idx] = nigttime(chckWidI(x,idI))
#								idx += 1
				except: pass
		if self.weather_dict['date0'] != UNKNOWN_STATE:
			try:
				self.weather_dict['city'] = config.plugins.setupGlass17.par13.getText()
				if not ENA_MSN:
					for x in ['wind', 'visibility', 'pressure']:
						if self.weather_dict[x] != UNKNOWN_STATE:
							self.weather_dict[x] += " " + units_dict[x]
				if self.TITLE_S:
					a = self.weather_dict['country'] + "\n" + self.weather_dict['wind'] + "\n" + self.weather_dict['wind_direction'] + "\n" + self.weather_dict['humidity'] + "\n" + ({False:self.weather_dict['visibility'], True:self.weather_dict['lat']+", "+self.weather_dict['long']}[ENA_MSN]) + "\n" + ({False:self.weather_dict['pressure'], True:self.weather_dict['feelslike']}[ENA_MSN])
				else:
					a = ({False:self.weather_dict['city'] + "\n" + self.weather_dict['country'] + "\n", True:""}[self.LIGHT]) + self.weather_dict['wind'] + "\n" + self.weather_dict['wind_direction'] + "\n" + self.weather_dict['humidity'] + "\n" + ({False:self.weather_dict['visibility'], True:self.weather_dict['lat']+", "+self.weather_dict['long']}[ENA_MSN]) + "\n" + ({False:self.weather_dict['pressure'], True:self.weather_dict['feelslike']}[ENA_MSN])+({False:"", True:"\n" + self.weather_dict['sunrise'] + "\n" + self.weather_dict['sunset'] + "\n" + self.timeUpdate}[self.LIGHT])
				self['Weather_values'].setText(str(a))		
				self.setWindowTitle(({False:"", True:self.weather_dict['city']+", "}[self.TITLE_S])+self.weather_dict['date0'])
				if not self.LIGHT:
					path = config.plugins.setupGlass17.par39.value + "/weatherIcons/" + str(config.plugins.setupGlass17.par72.value) + "/" + w_directPix + ".png"
					if not os.path.isfile(path):
						path = NO_WIND_PICON
					self['Weather_wind'].instance.setPixmapFromFile(path)
					self['Weather_sunrise'].setText(self.weather_dict['sunrise'])
				self['Weather_sunset'].setText(({False:self.weather_dict['sunset'], True:self.weather_dict['city']}[self.LIGHT]))
				self.__startShow()
				a,x = MoonInfo()
				self['moon_pict'].instance.setPixmapFromFile(PLUGINPATH+"MoonPict/"+x)
				self['moon_phase'].setText(a)
			except: pass
		else:
			self.resetWeather_values(_('Error') + ": " + _("Mishmash in the data"))
		self.enaNC = True

	def __startShow(self):
		if ENA_10:
			self.YTimer.stop()
		try:
			if ENA_ANIM:
				if self.animTimer.isActive():
					self.animTimer.stop()
				self.slide = {}
				self.pics = {}
			for ii in range(0,6):
				x = ii
				if ENA_10 and ii != 0:
					x += self.Yidx
				if ENA_ANIM:
					f = None
					try:
						path = config.plugins.setupGlass17.par39.value + "/animIconWeather/" + self.weather_dict['picon%s' % x]
						f = len(os.listdir(path))
					except: pass
					self.slide[ii] = 0
					self.pics[ii] = []
					if f:
						for i in range(0,f):
							self.pics[ii].append(LoadPixmap(path+"/"+str(i)+".png"))					
					else:
						self['Weather_picon%s' % ii].instance.setPixmapFromFile(NO_WEATHER_PICON)
				else:
					path = config.plugins.setupGlass17.par39.value + "/weatherIcons/" + str(config.plugins.setupGlass17.par72.value) + "/" + self.weather_dict['picon%s' % x] + ".png"
					if not os.path.isfile(path):
						path = NO_WEATHER_PICON
					self['Weather_picon%s' % ii].instance.setPixmapFromFile(path)
				if not 'temp%s' % x in self.weather_dict or "--" in self.weather_dict['temp%s' % x]:
					self['Weather_Temperature%s' % ii].setText(UNKNOWN_STATE_TEMP)
					self['Weather_Temperature%s' % ii].colorA(32)
				else:
					self['Weather_Temperature%s' % ii].setText(temperature_fix(self.weather_dict['temp%s' % x]))
					self.setColor(ii, int(self.weather_dict['temp%s' % x]), "", ENA_W)
				self['Weather_state%s' % ii].setText(str(self.weather_dict['text%s' % x]))
				if x != 0:
					if 'date%s' % x in self.weather_dict:
						aa = self.weather_dict['date%s' % x]
					else:
						aa = UNKNOWN_STATE
					self['Weather_Date%s' % ii].setText(aa)
					if not 'templow%s' % x in self.weather_dict or "--" in self.weather_dict['templow%s' % x]:
						self['Weather_Temperaturelow%s' % ii].setText(UNKNOWN_STATE_TEMP)
						self['Weather_Temperaturelow%s' % ii].colorA(32)
					else:
						self['Weather_Temperaturelow%s' % ii].setText(temperature_fix(self.weather_dict['templow%s' % x]))
						self.setColor(ii, int(self.weather_dict['templow%s' % x]), 'low', ENA_C)
		except: pass       	  		
		if ENA_ANIM:
			self.animTimer.start(200)
		if ENA_10:
			self.YTimer.start(1000*int(config.plugins.setupGlass17.par184.value))
			if self.Yidx == 0:
				self.Yidx = 5
			else:
				self.Yidx = 0
			
	def resetWeather_values(self, d="", ee=True):  		
		try:
			if ENA_ANIM:
				if self.animTimer.isActive():
					self.animTimer.stop()
			if ENA_10:
				if self.YTimer.isActive():
					self.YTimer.stop()
				self.Yidx = 0
			self.setTitle(({False:_('Weather'), True:d}[d != ""]))
			self['Weather_values'].setText(self.RESET_VALUES)		
			self['Weather_wind'].instance.setPixmapFromFile(NO_WIND_PICON)
			self['Weather_sunrise'].setText(UNKNOWN_STATE)
			self['Weather_sunset'].setText(UNKNOWN_STATE)
			self['moon_pict'].instance.setPixmapFromFile(PLUGINPATH+"MoonPict/moon0000.png")
			self['moon_phase'].setText(UNKNOWN_STATE)
			for x in range(0,6):
				self['Weather_picon%s' % x].instance.setPixmapFromFile(NO_WEATHER_PICON)
				self['Weather_Temperature%s' % x].setText(UNKNOWN_STATE_TEMP)		
				self['Weather_Temperature%s' % x].colorA(32)
				self['Weather_state%s' % x].setText(UNKNOWN_STATE)
				if x != 0:
					self['Weather_Date%s' % x].setText(UNKNOWN_STATE)
					self['Weather_Temperaturelow%s' % x].setText(UNKNOWN_STATE_TEMP)		
					self['Weather_Temperaturelow%s' % x].colorA(32)
			self.enaNC = True
			if ee and config.plugins.setupGlass17.par91.value != "0":
				tt = _("Attempt") + ": " + str(self.att)
				if d != "": 
					tt += ", " + d
				self.setTitle(tt)
				self.att += 1
				if self.weaTimer.isActive():
					self.weaTimer.stop()
				self.weaTimer.startLongTimer(int(config.plugins.setupGlass17.par91.value))    
		except: pass
                   			
	def setWindowTitle(self, txt):
		if not self.TITLE_S:
			if self.LIGHT:
				txt = txt.replace(self.timeUpdate, "") + ' (%s min)' % self.remainingTime			
			else:
				txt += ', ' + _('time to reconnect')+': %s min' % self.remainingTime
			txt += ', ('+DG+'%s)' % ({False:'C', True:'F'}[self.units == 'f'])
		self.setTitle(txt)
		
	def __runAnim(self):
		self.animTimer.stop()
		try:
			for x in range(0,len(self.slide)):
				a = len(self.pics[x])
				if a != 0:
					if self.slide[x] == a:
						self.slide[x] = 0
					self['Weather_picon%s' % x].instance.setPixmap(self.pics[x][self.slide[x]])	
					self.slide[x] += 1
		except: pass
		a = 50
		try:
			a = config.plugins.setupGlass17.par158.value
		except: pass
		self.animTimer.start(a)
    
	def setColor(self, idx, temp, x, c):
		if self.units == "f":
			temp = convToC(temp)
			a = convToC(config.plugins.setupGlass17.par149.value)
			b = convToC(config.plugins.setupGlass17.par150.value)
		else:
			a = config.plugins.setupGlass17.par96.value
			b = config.plugins.setupGlass17.par97.value
		if c == 9999:			
			if config.plugins.setupGlass17.par95.value != "None" and temp < a:
				self['Weather_Temperature%s%s' % (x, idx)].colorF()
			else:
				self['Weather_Temperature%s%s' % (x, idx)].colorW()
		elif c == -9999:			
			if config.plugins.setupGlass17.par95.value != "None" and temp > b:
				self['Weather_Temperature%s%s' % (x, idx)].colorF()
			else:
				self['Weather_Temperature%s%s' % (x, idx)].colorC()
		else:			
			self['Weather_Temperature%s%s' % (x, idx)].colorA(temp)
				
