#######################################################################
#
#    Netatmo for Enigma2
#    Coded by shamann (c)2018
#
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
from Components.config import config
from Components.MenuList import MenuList
from enigma import eListboxPythonMultiContent, eTimer, gFont, RT_HALIGN_CENTER, RT_HALIGN_RIGHT, eSize, RT_VALIGN_CENTER
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaBlend
from Tools.LoadPixmap import LoadPixmap
import gettext
import os
from Plugins.Extensions.setupGlass17.weaUtils import fixUtf8, dewpoint
ENA = True
try:
	if config.plugins.setupGlass17.par78.value != "a":
		ENA = False
except: pass
ENAA = False
try:
	from Plugins.Extensions.Netatmo.Netatmo import netatmo
	from Plugins.Extensions.Netatmo.NetatmoCore import NetatmoUnit
	ENAA = True
except: pass
ENA_ALL = True
try:
	if config.plugins.setupGlass17.par180.value == "b":
		ENA_ALL = False
except: pass
PLUGINPATH = "/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/"
SKINPATH = "/usr/share/enigma2/hd_glass17/netatmo/"
try:
	if config.plugins.setupGlass17.par49.value:
		Netatmo_language = []
		Netatmo_language = config.osd.language.value.split("_")
		if os.path.exists(PLUGINPATH + "locale/%s" % (Netatmo_language[0])):
			_ = gettext.Catalog('netatmo', PLUGINPATH + 'locale', Netatmo_language).gettext
except: pass

class netatmoList(MenuList):
	def __init__(self, list, enableWrapAround = False):
		MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
		self.l.setFont(0, gFont('Prive3', 30))
		self.l.setFont(1, gFont('Prive3', 25))
		self.l.setFont(2, gFont('Prive3', 27))
		self.l.setItemHeight(150)

class NetatmoScreen(Screen):

	skinC = """<screen position="center,15" zPosition="8" size="1520,620" title="Netatmo" backgroundColor="black" flags="wfNoBorder">
  <widget name="list" position="10,0" size="1500,1050" scrollbarMode="showNever" backgroundColor="black" />      
		</screen>"""
	skinB = """      
		<screen position="center,center" zPosition="8" size="1500,600" title="Netatmo" backgroundColor="black">
		<widget font="Regular;28" halign="center" valign="center" foregroundColor="#006cbcf0" position="0,0" render="Label" size="750,30" source="session.Netatmo" backgroundColor="black" transparent="1">
			<convert type="Netatmo">station.module_name</convert>
		</widget>
		<widget font="Regular;28" halign="center" valign="center" foregroundColor="green" position="0,60" render="Label" size="750,30" source="session.Netatmo" backgroundColor="black" transparent="1">
			<convert type="Netatmo">station.when</convert>
		</widget>
		<widget font="Regular;30" halign="center" valign="center" foregroundColor="black" position="625,0" zPosition="2" render="Label" size="250,45" source="session.Netatmo" backgroundColor="yellow" transparent="0">
			<convert type="Netatmo">elapsed_refresh</convert>
		</widget>
		<widget font="Regular;28" halign="center" valign="center" foregroundColor="#006cbcf0" position="750,0" render="Label" size="750,30" source="session.Netatmo" backgroundColor="black" transparent="1">
			<convert type="Netatmo">module.module_name</convert>
		</widget>
		<widget font="Regular;28" halign="center" valign="center" foregroundColor="green" position="750,60" render="Label" size="750,30" source="session.Netatmo" backgroundColor="black" transparent="1">
			<convert type="Netatmo">module.when</convert>
		</widget>
		<ePixmap pixmap="hd_glass17/netatmo/wifi_0.png" zPosition="0" position="345,110" size="60,60" alphatest="blend" />
		<widget zPosition="1" pixmaps="wifi_0.png,wifi_1.png,wifi_2.png,wifi_3.png,wifi_4.png" pixtype="wifi_status" skin_pixmaps="hd_glass17/netatmo" position="345,110" render="NetatmoPixmap" size="60,60" source="session.Netatmo" alphatest="blend" />
		<widget font="Regular;25" halign="center" position="0,190" render="Label" size="750,30" source="session.Netatmo" backgroundColor="black" transparent="1">
			<convert type="Netatmo">station.wifi_status</convert>
		</widget>
		<ePixmap pixmap="hd_glass17/netatmo/signal_0.png" zPosition="0" position="960,110" size="60,60" alphatest="blend" />
		<widget zPosition="1" pixmaps="signal_0.png,signal_1.png,signal_2.png,signal_3.png,signal_4.png,signal_5.png" pixtype="rf_status" skin_pixmaps="hd_glass17/netatmo" position="960,110" render="NetatmoPixmap" size="60,60" source="session.Netatmo" alphatest="blend" />
		<widget font="Regular;25" halign="center" position="790,190" render="Label" size="400,30" source="session.Netatmo" backgroundColor="black" transparent="1">
			<convert type="Netatmo">module.rf_status</convert>
		</widget>
		<ePixmap pixmap="hd_glass17/netatmo/battery_0.png" zPosition="0" position="1230,110" size="60,60" alphatest="blend" />
		<widget zPosition="1" pixmaps="battery_0.png,battery_1.png,battery_2.png,battery_3.png,battery_4.png,battery_5.png" pixtype="battery_vp" skin_pixmaps="hd_glass17/netatmo" position="1230,110" render="NetatmoPixmap" size="60,60" source="session.Netatmo" alphatest="blend" />
		<widget font="Regular;25" halign="center" position="1060,190" render="Label" size="400,30" source="session.Netatmo" backgroundColor="black" transparent="1">
			<convert type="Netatmo">module.battery_percent</convert>
		</widget>
		<eLabel backgroundColor="#1546AF" position="749,0" size="2,600" transparent="0" zPosition="1" />
		<ePixmap pixmap="hd_glass17/netatmo/temp.png" position="210,270" size="60,60" alphatest="blend" />
		<widget font="Regular;25" halign="center" position="40,350" render="Label" size="400,30" source="session.Netatmo" backgroundColor="black" transparent="1">
			<convert type="Netatmo">station.temperature?temp unit (min | max)</convert>
		</widget>
		<ePixmap pixmap="hd_glass17/netatmo/humidity.png" position="480,270" size="60,60" alphatest="blend" />
		<widget font="Regular;25" halign="center" position="310,350" render="Label" size="400,30" source="session.Netatmo" backgroundColor="black" transparent="1">
			<convert type="Netatmo">station.humidity</convert>
		</widget>
		<ePixmap pixmap="hd_glass17/netatmo/temp.png" position="960,270" size="60,60" alphatest="blend" />
		<widget font="Regular;25" halign="center" position="790,350" render="Label" size="400,30" source="session.Netatmo" backgroundColor="black" transparent="1">
			<convert type="Netatmo">module.temperature?temp unit (min | max)</convert>
		</widget>
		<ePixmap pixmap="hd_glass17/netatmo/humidity.png" position="1230,270" size="60,60" alphatest="blend" />
		<widget font="Regular;25" halign="center" position="1060,350" render="Label" size="400,30" source="session.Netatmo" backgroundColor="black" transparent="1">
			<convert type="Netatmo">module.humidity</convert>
		</widget>
		<ePixmap pixmap="hd_glass17/netatmo/co2.png" zPosition="0" position="142,420" size="60,60" alphatest="blend" />
		<eLabel font="Regular2;22" halign="center" text="Co2" valign="center" zPosition="2" position="142,420" size="60,60" transparent="1" foregroundColor="black" />
		<widget zPosition="1" pixmaps="co2_1.png,co2_2.png,co2_3.png,co2_4.png,co2_5.png,co2_6.png,co2_7.png,co2_8.png,co2_9.png,co2_10.png" pixtype="co2" skin_pixmaps="hd_glass17/netatmo" position="142,420" render="NetatmoPixmap" size="60,60" source="session.Netatmo" alphatest="blend" />
		<widget font="Regular;25" halign="center" position="22,500" render="Label" size="300,30" source="session.Netatmo" backgroundColor="black" transparent="1">
			<convert type="Netatmo">station.co2</convert>
		</widget>
		<ePixmap pixmap="hd_glass17/netatmo/pressure.png" position="345,420" size="60,60" alphatest="blend" />
		<widget font="Regular;25" halign="center" position="225,500" render="Label" size="300,30" source="session.Netatmo" backgroundColor="black" transparent="1">
			<convert type="Netatmo">station.pressure</convert>
		</widget>
		<ePixmap pixmap="hd_glass17/netatmo/noise.png" position="547,420" size="60,60" alphatest="blend" />
		<widget font="Regular;25" halign="center" position="427,500" render="Label" size="300,30" source="session.Netatmo" backgroundColor="black" transparent="1">
			<convert type="Netatmo">station.noise</convert>
		</widget>
		<eLabel backgroundColor="#1546AF" position="750,400" size="750,2" zPosition="2" transparent="0" />
		<eLabel backgroundColor="#1546AF" position="1125,400" size="2,250" zPosition="2" transparent="0" />
		<ePixmap pixmap="hd_glass17/netatmo/no-wind.png" zPosition="0" position="907,420" size="60,60" alphatest="blend" />
		<widget pixmap="hd_glass17/netatmo/wind.png" pixtype="wind" zPosition="1" position="907,420" render="NetatmoPixmap" size="60,60" source="session.Netatmo" alphatest="blend" />
		<widget font="Regular;25" halign="center" position="750,500" render="Label" size="375,30" source="session.Netatmo" backgroundColor="black" transparent="1">
			<convert type="Netatmo">windgauge.wind_strength?value unit direction</convert>
		</widget>
		<eLabel font="Regular;22" halign="right" text="RF Status:" position="770,550" size="125,30" transparent="1" backgroundColor="black" />
		<widget font="Regular;22" halign="left" position="905,550" render="Label" size="125,30" source="session.Netatmo" backgroundColor="black" transparent="1">
			<convert type="Netatmo">windgauge.rf_status</convert>
		</widget>
		<eLabel font="Regular;22" halign="right" text="Battery:" position="945,550" size="125,30" transparent="1" backgroundColor="black" />
		<widget font="Regular;22" halign="left" position="1080,550" render="Label" size="125,30" source="session.Netatmo" backgroundColor="black" transparent="1">
			<convert type="Netatmo">windgauge.battery_percent</convert>
		</widget>
		<ePixmap pixmap="hd_glass17/netatmo/no-rain.png" zPosition="0" position="1282,420" size="60,60" alphatest="blend" />
		<widget pixmap="hd_glass17/netatmo/rain.png" pixtype="rain" zPosition="1" position="1282,420" render="NetatmoPixmap" size="60,60" source="session.Netatmo" alphatest="blend" />
		<widget font="Regular;25" halign="center" position="1125,500" render="Label" size="375,30" source="session.Netatmo" backgroundColor="black" transparent="1">
			<convert type="Netatmo">rainfall?sum1|sum24 unit</convert>
		</widget>
		<eLabel font="Regular;22" halign="right" text="RF Status:" position="1145,550" size="125,30" transparent="1" backgroundColor="black" />
		<widget font="Regular;22" halign="left" position="1280,550" render="Label" size="125,30" source="session.Netatmo" backgroundColor="black" transparent="1">
			<convert type="Netatmo">rainfall.rf_status</convert>
		</widget>
		<eLabel font="Regular;22" halign="right" text="Battery:" position="1320,550" size="125,30" transparent="1" backgroundColor="black" />
		<widget font="Regular;22" halign="left" position="1455,550" render="Label" size="125,30" source="session.Netatmo" backgroundColor="black" transparent="1">
			<convert type="Netatmo">rainfall.battery_percent</convert>
		</widget>
		</screen>"""
	skinA = """      
		<screen position="center,center" zPosition="8" size="690,540" title="Netatmo" backgroundColor="background">
		<widget name="info" font="Regular;40" position="10,10" size="670,520" halign="center" valign="center" transparent="1" backgroundColor="background" />
		</screen>"""

	def __init__(self, session):
		Screen.__init__(self,session)
		self.session = session
		if not ENAA:
			self.skin = NetatmoScreen.skinA
			from Plugins.Extensions.setupGlass17.txt import NETATMO
			from Components.Label import Label
			self['info'] = Label(NETATMO)
		elif ENA_ALL:
			self.skin = NetatmoScreen.skinC
			self.__atmoTimer = eTimer()
			try:
				self.__atmoTimer_conn = self.__atmoTimer.timeout.connect(self.__nextStation)
			except AttributeError:
				self.__atmoTimer.timeout.get().append(self.__nextStation)
			self.numStations = 0
			self.stationID = -1
			self.list = []
			self['list'] = netatmoList(self.list)
			self.onHide.append(self.__goSleep)
			self.onShow.append(self.__goWakeup)
		else:
			self.skin = NetatmoScreen.skinB
		if ENA:
			from Components.ActionMap import ActionMap
			self["actions"] = ActionMap(["ColorActions", "SetupActions", "DirectionActions"],
			{
            "green": self.exit,
            "red": self.exit,
            "ok": self.exit,
            "cancel": self.exit,
            "yellow": self.exit,
            "blue": self.exit
			}, -2)	
			
	def exit(self):
		if ENA_ALL and ENAA:
			self.__atmoTimer.stop()
			self.__atmoTimer = None
			self.__atmoTimer_conn = None
		self.close()

	def __goSleep(self):
		if not ENA:
			self.__atmoTimer.stop()
		
	def __nextStation(self):
		self.__atmoTimer.stop()
		self.stationID += 1
		if self.stationID > self.numStations - 1:
			self.stationID = 0
		if self.numStations > 1:
			r = 10
			try:
				r = int(config.plugins.setupGlass17.par181.value)
			except: pass
			self.__atmoTimer.startLongTimer(r)
		self.showData()

	def __goWakeup(self):
		def angle(direct):
			try:
				direct = int(direct)
				if direct >= 0 and direct <= 28:
					return _('N')
				elif direct >= 29 and direct <= 62:
					return _('NE')
				elif direct >= 63 and direct <= 117:
					return _('E')
				elif direct >= 118 and direct <= 152:
					return _('SE')
				elif direct >= 153 and direct <= 207:
					return _('S')
				elif direct >= 208 and direct <= 242:
					return _('SW')
				elif direct >= 243 and direct <= 297:
					return _('W')
				elif direct >= 298 and direct <= 332:
					return _('NW')
			except:
					return _("N/A")
		self.stationID = -1
		self.numStations = 0
		try:
			self.numStations = len(netatmo.stations)
		except: pass
		if ENAA and self.numStations > 0:
			try:
				self.name = []
				self.temp = []
				self.hum = []
				self.press = []
				self.noise = []
				self.co2 = []
				self.wifi = []
				self.idx = []
				self.when = []
				self.modules = []
				moduleType = {'NAModule1': _("Outdoor"), 'NAModule2': _("Wind"), 'NAModule3': _("Rain"), 'NAModule4': _("Indoor")}
				for i in netatmo.stations:
					self.name.append(str(fixUtf8(i.module_name)))
					self.temp.append(str(i.measure.temperature))
					self.hum.append(str(i.measure.humidity))
					self.press.append(str(i.measure.pressure))
					self.noise.append(str(i.measure.noise))
					self.co2.append(str(i.measure.co2))
					self.wifi.append(int(i.wifi_status))
					self.when.append((str(i.measure.when)).replace("Last measurement:",""))
					try:
						self.idx.append(str(int(float(i.measure.idx_total))))
					except:
						self.idx.append("0")
					self.modules.append([]) 
					for x in i.modules:
						val1 = val2 = btr = rf = w = _("N/A")
						try:
							w = (str(x.measure.when)).replace("Last measurement:","")
						except: pass
						if x.module_type.startswith("NAModule"):
							btr = str(x.battery_percent)
							rf = int(x.rf_status)
						name = str(fixUtf8(x.module_name)) if i.module_name != "" else moduleType.get(x.module_type,_("N/A"))
						if x.measure.has_co2:
							val1 = str(x.measure.co2)
						if x.module_type == "NAModule3":
							self.modules[len(self.modules)-1].append([str(x.measure.getSensor("sum_rain_1")),str(x.measure.getSensor("sum_rain_24")),val1,val2,name,moduleType.get(x.module_type,_("N/A")),btr,rf,w])
						elif x.module_type == "NAModule2":
							self.modules[len(self.modules)-1].append([str(x.measure.wind_strength),angle(str(x.measure.wind_angle)),str(x.measure.gust_strength),angle(str(x.measure.gust_angle)),name,moduleType.get(x.module_type,_("N/A")),btr,rf,w])
						else:
							self.modules[len(self.modules)-1].append([str(x.measure.temperature),str(x.measure.humidity),val1,val2,name,moduleType.get(x.module_type,_("N/A")),btr,rf,w])
				self.Utemp = netatmo.getUint(NetatmoUnit.TEMPERATURE)
				self.Uhum = netatmo.getUint(NetatmoUnit.HUMIDITY)
				self.Upress = netatmo.getUint(NetatmoUnit.PRESSURE)
				self.Uco2 = netatmo.getUint(NetatmoUnit.CO2)
				self.Unoise = netatmo.getUint(NetatmoUnit.NOISE)
				self.Urain = " " + netatmo.getUint(NetatmoUnit.MM)
				self.Uwind = " " + (netatmo.getUint(NetatmoUnit.WIND)).replace("beaufort","bft").replace("kph","km/h")       
			except: pass
		self.__nextStation()

	def showData(self):
		self.list = []
		item = []		 
		if self.numStations == 0:
			item = ["*"]                        
			item.append(MultiContentEntryText(pos=(0, 0), size=(1500,150), font=0, color=int('0xff3300',16), text=_("No Netatmo station detected"), flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER))
			self.list.append(item)
		else:
			try:
				item = ["s"]                        
				item.append(MultiContentEntryText(pos=(0, 0), size=(500, 40), font=0, backcolor=int('0x1546AF',16), color=int('0xffffff',16), text=" "+_("Name")+": "+self.name[self.stationID]))
				item.append(MultiContentEntryText(pos=(500, 0), size=(500, 40), font=0, backcolor=int('0x1546AF',16), color=int('0xffffff',16), text=_("Type")+": "+_("Main station"), flags=RT_HALIGN_CENTER))
				item.append(MultiContentEntryText(pos=(1000, 0), size=(500, 40), font=0, backcolor=int('0x1546AF',16), color=int('0xffffff',16), text=self.when[self.stationID]+" ", flags=RT_HALIGN_RIGHT))
				item.append(MultiContentEntryText(pos=(0, 45), size=(210, 30), font=1, color=int('0xffcc00',16), text=_("Temperature"), flags=RT_HALIGN_CENTER))
				item.append(MultiContentEntryPixmapAlphaBlend(pos=(0, 80), size=(60, 60), png=LoadPixmap(SKINPATH+"temp.png")))
				item.append(MultiContentEntryText(pos=(60, 80), size=(150, 60), font=2, color=int('0xffffff',16), text=self.temp[self.stationID]+self.Utemp, flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER))
				item.append(MultiContentEntryText(pos=(210, 45), size=(210, 30), font=1, color=int('0xffcc00',16), text=_("Humidity"), flags=RT_HALIGN_CENTER))
				item.append(MultiContentEntryPixmapAlphaBlend(pos=(210, 80), size=(60, 60), png=LoadPixmap(SKINPATH+"humidity.png")))
				item.append(MultiContentEntryText(pos=(270, 80), size=(150, 60), font=2, color=int('0xffffff',16), text=self.hum[self.stationID]+self.Uhum, flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER))
				item.append(MultiContentEntryText(pos=(420, 45), size=(210, 30), font=1, color=int('0xffcc00',16), text=_("Noise"), flags=RT_HALIGN_CENTER))
				item.append(MultiContentEntryPixmapAlphaBlend(pos=(420, 80), size=(60, 60), png=LoadPixmap(SKINPATH+"noise.png")))
				item.append(MultiContentEntryText(pos=(480, 80), size=(150, 60), font=2, color=int('0xffffff',16), text=self.noise[self.stationID]+self.Unoise, flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER))
				item.append(MultiContentEntryText(pos=(630, 45), size=(210, 30), font=1, color=int('0xffcc00',16), text=_("Co2"), flags=RT_HALIGN_CENTER))
				item.append(MultiContentEntryPixmapAlphaBlend(pos=(630, 80), size=(60, 60), png=LoadPixmap(SKINPATH+self.co2pix(int(self.co2[self.stationID])))))
				item.append(MultiContentEntryText(pos=(690, 80), size=(150, 60), font=2, color=int('0xffffff',16), text=self.co2[self.stationID]+self.Uco2, flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER))
				item.append(MultiContentEntryText(pos=(840, 45), size=(210, 30), font=1, color=int('0xffcc00',16), text=_("Wifi Status"), flags=RT_HALIGN_CENTER))
				item.append(MultiContentEntryPixmapAlphaBlend(pos=(840, 80), size=(60, 60), png=LoadPixmap(SKINPATH+self.wifipix(self.wifi[self.stationID]))))
				item.append(MultiContentEntryText(pos=(900, 80), size=(150, 60), font=2, color=int('0xffffff',16), text=self.convertToPercent(87,56,self.wifi[self.stationID]), flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER))
				item.append(MultiContentEntryText(pos=(1050, 45), size=(210, 30), font=1, color=int('0xffcc00',16), text=_("Index"), flags=RT_HALIGN_CENTER))
				item.append(MultiContentEntryPixmapAlphaBlend(pos=(1050, 80), size=(60, 60), png=LoadPixmap(SKINPATH+self.idxpix(int(self.idx[self.stationID])))))
				item.append(MultiContentEntryText(pos=(1110, 80), size=(150, 60), font=2, color=int('0xffffff',16), text=self.idx[self.stationID], flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER))
				item.append(MultiContentEntryText(pos=(1260, 45), size=(240, 30), font=1, color=int('0xffcc00',16), text=_("Pressure"), flags=RT_HALIGN_CENTER))
				item.append(MultiContentEntryPixmapAlphaBlend(pos=(1260, 80), size=(60, 60), png=LoadPixmap(SKINPATH+"pressure.png")))
				item.append(MultiContentEntryText(pos=(1320, 80), size=(180, 60), font=2, color=int('0xffffff',16), text=self.press[self.stationID]+self.Upress, flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER))
				self.list.append(item)
				for x in range(0,len(self.modules[self.stationID])):
					item = ["m"]                        
					item.append(MultiContentEntryText(pos=(0, 0), size=(500, 40), font=0, backcolor=int('0x1546AF',16), color=int('0xffffff',16), text=" "+_("Name")+": "+self.modules[self.stationID][x][4]))
					item.append(MultiContentEntryText(pos=(500, 0), size=(500, 40), font=0, backcolor=int('0x1546AF',16), color=int('0xffffff',16), text=_("Type")+": "+self.modules[self.stationID][x][5], flags=RT_HALIGN_CENTER))
					item.append(MultiContentEntryText(pos=(1000, 0), size=(500, 40), font=0, backcolor=int('0x1546AF',16), color=int('0xffffff',16), text=self.modules[self.stationID][x][8]+" ", flags=RT_HALIGN_RIGHT))					
					if self.modules[self.stationID][x][5] == _("Rain"):
						item.append(MultiContentEntryText(pos=(0, 45), size=(150, 30), font=1, color=int('0xffcc00',16), text=_("Rainfall"), flags=RT_HALIGN_CENTER))
						item.append(MultiContentEntryPixmapAlphaBlend(pos=(0, 80), size=(60, 60), png=LoadPixmap(SKINPATH+"rain.png")))
						item.append(MultiContentEntryText(pos=(150, 45), size=(250, 30), font=1, color=int('0xffcc00',16), text=_("Summary 1 Hour"), flags=RT_HALIGN_CENTER))
						item.append(MultiContentEntryText(pos=(150, 80), size=(250, 60), font=2, color=int('0xffffff',16), text=self.modules[self.stationID][x][0]+self.Urain,flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER))
						item.append(MultiContentEntryText(pos=(400, 45), size=(250, 30), font=1, color=int('0xffcc00',16), text=_("Summary 24 Hours"), flags=RT_HALIGN_CENTER))
						item.append(MultiContentEntryText(pos=(400, 80), size=(250, 60), font=2, color=int('0xffffff',16), text=self.modules[self.stationID][x][1]+self.Urain,flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER))
						posX = 650
					elif self.modules[self.stationID][x][5] == _("Wind"):
						item.append(MultiContentEntryText(pos=(0, 45), size=(150, 30), font=1, color=int('0xffcc00',16), text=_("Wind"), flags=RT_HALIGN_CENTER))
						item.append(MultiContentEntryPixmapAlphaBlend(pos=(0, 80), size=(60, 60), png=LoadPixmap(SKINPATH+"wind.png")))
						item.append(MultiContentEntryText(pos=(150, 45), size=(225, 30), font=1, color=int('0xffcc00',16), text=_("Wind Strength"), flags=RT_HALIGN_CENTER))
						item.append(MultiContentEntryText(pos=(150, 80), size=(225, 60), font=2, color=int('0xffffff',16), text=self.modules[self.stationID][x][0]+self.Uwind,flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER))
						item.append(MultiContentEntryText(pos=(375, 45), size=(225, 30), font=1, color=int('0xffcc00',16), text=_("Wind Angle"), flags=RT_HALIGN_CENTER))
						item.append(MultiContentEntryText(pos=(375, 80), size=(225, 60), font=2, color=int('0xffffff',16), text=self.modules[self.stationID][x][1],flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER))
						item.append(MultiContentEntryText(pos=(600, 45), size=(225, 30), font=1, color=int('0xffcc00',16), text=_("Gust Strength"), flags=RT_HALIGN_CENTER))
						item.append(MultiContentEntryText(pos=(600, 80), size=(225, 60), font=2, color=int('0xffffff',16), text=self.modules[self.stationID][x][2]+self.Uwind,flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER))
						item.append(MultiContentEntryText(pos=(825, 45), size=(225, 30), font=1, color=int('0xffcc00',16), text=_("Gust Angle"), flags=RT_HALIGN_CENTER))
						item.append(MultiContentEntryText(pos=(825, 80), size=(225, 60), font=2, color=int('0xffffff',16), text=self.modules[self.stationID][x][3],flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER))
						posX = 1050
					else:
						item.append(MultiContentEntryText(pos=(0, 45), size=(210, 30), font=1, color=int('0xffcc00',16), text=_("Temperature"), flags=RT_HALIGN_CENTER))
						item.append(MultiContentEntryPixmapAlphaBlend(pos=(0, 80), size=(60, 60), png=LoadPixmap(SKINPATH+"temp.png")))
						item.append(MultiContentEntryText(pos=(60, 80), size=(150, 60), font=2, color=int('0xffffff',16), text=self.modules[self.stationID][x][0]+self.Utemp, flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER))
						item.append(MultiContentEntryText(pos=(210, 45), size=(210, 30), font=1, color=int('0xffcc00',16), text=_("Humidity"), flags=RT_HALIGN_CENTER))
						item.append(MultiContentEntryPixmapAlphaBlend(pos=(210, 80), size=(60, 60), png=LoadPixmap(SKINPATH+"humidity.png")))
						item.append(MultiContentEntryText(pos=(270, 80), size=(150, 60), font=2, color=int('0xffffff',16), text=self.modules[self.stationID][x][1]+self.Uhum, flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER))
						posX = 420
						if "C" in self.Utemp:
							item.append(MultiContentEntryText(pos=(posX, 45), size=(210, 30), font=1, color=int('0xffcc00',16), text=_("Dew Point"), flags=RT_HALIGN_CENTER))
							item.append(MultiContentEntryPixmapAlphaBlend(pos=(posX, 80), size=(60, 60), png=LoadPixmap(SKINPATH+"dewpoint.png")))
							item.append(MultiContentEntryText(pos=(posX+60, 80), size=(150, 60), font=2, color=int('0xffffff',16), text=dewpoint(int(float(self.modules[self.stationID][x][0])),int(self.modules[self.stationID][x][1]))+self.Utemp, flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER))
							posX += 210
						if self.modules[self.stationID][x][2] != _("N/A"):
							item.append(MultiContentEntryText(pos=(posX, 45), size=(210, 30), font=1, color=int('0xffcc00',16), text=_("Co2"), flags=RT_HALIGN_CENTER))
							item.append(MultiContentEntryPixmapAlphaBlend(pos=(posX, 80), size=(60, 60), png=LoadPixmap(SKINPATH+self.co2pix(int(self.modules[self.stationID][x][2])))))
							item.append(MultiContentEntryText(pos=(posX+60, 80), size=(150, 60), font=2, color=int('0xffffff',16), text=self.modules[self.stationID][x][2]+self.Uco2, flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER))
							posX += 210
					item.append(MultiContentEntryText(pos=(posX, 45), size=(210, 30), font=1, color=int('0xffcc00',16), text=_("RF Status"), flags=RT_HALIGN_CENTER))
					item.append(MultiContentEntryPixmapAlphaBlend(pos=(posX, 80), size=(60, 60), png=LoadPixmap(SKINPATH+self.rfpix(self.modules[self.stationID][x][7]))))
					item.append(MultiContentEntryText(pos=(posX+60, 80), size=(150, 60), font=2, color=int('0xffffff',16), text=self.convertToPercent(91,60,self.modules[self.stationID][x][7]), flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER))
					item.append(MultiContentEntryText(pos=(posX+210, 45), size=(210, 30), font=1, color=int('0xffcc00',16), text=_("Baterry"), flags=RT_HALIGN_CENTER))
					item.append(MultiContentEntryPixmapAlphaBlend(pos=(posX+210, 80), size=(60, 60), png=LoadPixmap(SKINPATH+self.batpix(int(self.modules[self.stationID][x][6])))))
					item.append(MultiContentEntryText(pos=(posX+270, 80), size=(150, 60), font=2, color=int('0xffffff',16), text=self.modules[self.stationID][x][6]+"%", flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER))
					self.list.append(item)
			except: pass
		self['list'].l.setList(self.list)
		self['list'].selectionEnabled(0)
		self.instance.resize(eSize(1520,20+len(self.list)*150))
		item = []
		
	def co2pix(self, c):
		y = float(c - 400)
		if c < 600:  
 			x = y / 15
		else:
 			x = y / 16
		if x >= 100:
 			x = "10"
		elif x <= 0:
 			x = "1"
		else:
 			x = str(1 + int(x / 10.0))
		return "co2_%s.png" % x

	def idxpix(self, x):
		if x < 10:
 			x = "1"
		elif x < 20:
 			x = "2"
		elif x < 30:
 			x = "3"
		elif x < 40:
 			x = "4"
		elif x < 50:
 			x = "5"
		elif x < 60:
 			x = "6"
		elif x < 70:
 			x = "7"
		elif x < 80:
 			x = "8"
		elif x < 90:
 			x = "9"
		else:
 			x = "10"
		return "co2_%s.png" % x
          
	def batpix(self, x):
		if x < 1:
 			x = "0"
		elif x < 25:
 			x = "1"
		elif x < 45:
 			x = "2"
		elif x < 65:
 			x = "3"
		elif x < 85:
 			x = "4"
		else:
 			x = "5"
		return "battery_%s.png" % x  

	def rfpix(self, x):
		if x <= 60:
 			x = "5"
		elif x <= 67:
 			x = "4"
		elif x <= 75:
 			x = "3"
		elif x <= 83:
 			x = "2"
		elif x <= 90:
 			x = "1"
		else:
 			x = "0"
		return "signal_%s.png" % x
                  					
	def wifipix(self, x):
		if x <= 56:
 			x = "4"
		elif x <= 66:
 			x = "3"
		elif x <= 76:
 			x = "2"
		elif x <= 86:
 			x = "1"
		else:
 			x = "0"
		return "wifi_%s.png" % x

	def convertToPercent(self, value0, value100, req):
		percent = 0
		if value0 > value100:
			if req >= value0:
				percent = 0
			elif req <= value100:
				percent = 100
			else:
				percent = (req - value0) * 100 / (value100 - value0)
		return "%s%%" % percent	
    		
