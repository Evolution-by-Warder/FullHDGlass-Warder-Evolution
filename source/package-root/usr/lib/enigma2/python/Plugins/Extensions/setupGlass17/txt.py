# -*- coding: utf-8 -*-
from Components.config import config, ConfigSubsection, ConfigYesNo 
import gettext
import os
from datetime import datetime
import math
PLUGINPATH = "/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/"
config.plugins.setupGlass17 = ConfigSubsection()
config.plugins.setupGlass17.par49 = ConfigYesNo(default = True) # enable translation
L = True
try:
	if config.plugins.setupGlass17.par49.value:
		g17_language = []
		g17_language = config.osd.language.value.split("_")
		if os.path.exists(PLUGINPATH + "locale/%s" % (g17_language[0])):
			_ = gettext.Catalog('helpTxt', PLUGINPATH + 'locale', g17_language).gettext
		if "cs" in g17_language[0]:
			L = False
except: pass
from Plugins.Extensions.setupGlass17.weaUtils import ISP38
if ISP38:
	from Plugins.Extensions.setupGlass17.py38 import DG
else:
	DG = unichr(176).encode("latin-1")
NA = _('N/A')
FREE = _('free')
NO_TP = _('TP info is not detected')
NO_REF = _('Reference is not detected')
E_EPG = _('No EPG data available')
EWEA = _('Please wait for the reading and processing of data')+' .....'
EWEA_ERROR = _('Please install beautifulsoup4')+':\n\nDeb package:\n\napt-get update && dpkg -i python-beautifulsoup4 && apt-get -f install\n\nIpk package:\n\nopkg update && opkg install python-beautifulsoup4'
EWEA_ERROR += '\n\nIpk package (python 3.x):\n\nopkg update && opkg install python3-beautifulsoup4'
OKGREEN = '\n\n' + _('Press button "OK" to select favorite directory.')
A1T1 = _('Autocolor - use definition from skin.xml or g17Screens.py; selected color - display with selected color')
A1T2 = ' ('+_('Channels from all satelitte positions and sk/cz terrestrial channels')+')'
NETATMO = _('No plugin Netatmo installed')
helpTxt = {
'228-0' : _('Your API-key'),
'227-0' : _('The layout is selected automatically calculating by picon size in the infobar'),
'209-0' : _('Measurement of current network speed is disabled'),
'209-1' : _('Measurement of current network speed is enabled and is displayed in kb/s'),
'209-2' : _('Measurement of current network speed is enabled and is displayed in Mb/s'),
'207-0' : _('Poster is displayed if exists'),
'207-1' : _('Currently displayed Poster will be erased after press long "OK" and do not displayed back again'),
'204-i' : _('Poster search from "Internet Movie Database (IMDb)"'),
'204-m' : _('Poster search from "The Movie Database (TMDb)"'),
'204-a' : _('Poster search from "Internet Movie Database (IMDb) if not found then search from "The Movie Database (TMDb)"'),
'205' : _('Poster search is started with selected delay'),
'202' : _('Poster is displayed with the selected size'),
'193-0' : _('ECM info is displayed from all channels - current displayed, background recording, streaming etc.'),
'193-1' : _('ECM info is displayed from current channel'),
'189-0' : _('Bitrate is calculated by using included bitrate binary'),
'189-1' : _('Bitrate is calculated by using eBitrateCalculator from plugin BitrateViewer'),
'180-a' : _('All available stations with their modules are displayed one by one with defined switching time'),
'180-b' : _('Info is displayed from Station selected in Netatmo plugin'),
'181-x' : _('Time in seconds'),
'168-F' : _('Real tuner data are displayed'),
'168-T' : _('Data are displayed from Transponder information'),
'161-0' : _('Animations are disabled'),
'161-1' : _('Selected animations are applyied to selected objects'),
'160-0' : _('Do not display info about HDD/SSD state'),
'160-1' : _('HDD/SSD temperature, size and free space is displayed in EMC and Movieplayer infobar'),
'fifo-0' : _('Last 10 searched channels are displayed only'),
'fifo-1' : _('Searched channels are displayed as long list and you can browse in the list'),
'as-1' : _('Refresh time between frames of animated icon (default value is 50ms)'),
'lbs-1' : _('Apply to all screens where the listbox is used'),
'024-0' : _('Nighttime icons are replaced by daytime icons'),
'024-1' : _('Nighttime icons are displayed'),
'ok-1' : _('Press button "OK" to activate selected function'),
'6517-0' : _('Spinner will be used as default from image'),
'6517-1' : _('Spinner will be used from Full HD Glass17. Original spinner is moved to dir spinner-ori'),
'460-0' : _('EPG list will be displayed with selected font size'),
'5017-0' : _('PIP types of channel selections are unavailable'),
'5017-1' : _('PIP types of channel selections are available but it can generate GSOD in some images'),
'141-0' : _('Directory where is located the file: satellites.xml') + OKGREEN,
'144-0' : _('Directory where will be saved actual configuration of FHDG (file: hdg17.conf)') + OKGREEN,
'143n-0' : _('Display forecast for 5 days'),
'143n-1' : _('Display forecast for 10 days at first 5 days after timeout of switch time display next 5 days'),
'101-1' : _('Appears info about sunrise, sunset of planets, sun and moon'),
'00' : _('Sorry, help info is missing'),
'1-0' : _('Info is displayed with defined color'),
'1-1' : _('Info is displayed with autoselected color'),
'5-1' : _('Show extra screen only'),
'10-n' : _('None special info is selected'),
'12-0' : _('Show extra infobar only'),
'12-1' : _('Show side bar and extra infobar only'),
'13-0' : _('1 - fastest, 10 - slowest'),
'14-0' : _('Infobar appears immediately and disapears immediately'),
'14-1' : _('Infobar (dis)appears from full/defined transparency to defined(full) transparency'),
'15-0' : _('Infobar appears immediately and disapears from defined to full transparency'),
'15-1' : _('Infobar (dis)appears from full/defined transparency to defined(full) transparency'),
'17-0' : _('Show extra infobar only'),
'17-1' : _('Show extra infobar and press 2xOK show User info'),
'18-n' : _('Show extra infobar only'),
'19-0' : _('Apears user info press 2x"OK" and disappears with extra infobar'),
'19-1' : _('Apears user info press 2x"OK" and disappears press "OK" or "exit"'),
'20-0' : _('Show actual event(EPG) only'),
'20-1' : _('Press long ">" switch between actual and next evet(EPG)'),
'21-0' : _('Show extra infobar only'),
'21-1' : _('Display ECM PID info with extra infobar'),
'23-0' : _('Show events name in infobar as static text'),
'23-1' : _('Show events name in infobar char by char with typewritter effect'),
'25-0' : _('Show OLED design from "image" definition'),
'27-0' : _('Display "Btr too high - stopped" if realtime bitrate is higher as the set value'),
'29-0' : _('Use only if in your image is keymapping set to "standard Enigma2"'),
'29-1' : _('Use only if in your image is keymapping set to "Neutrino keymap type"'),
'35-0' : _('Show messages in default language - english'),
'35-1' : _('Show localized messages autodetected from active OSD setting of language'), 
'39-0' : _('Infobar disappears after a defined timeout in system settings'), 
'39-1' : _('Infobar activated by switching between channels disappears after a defined timeout in system settings. Infobar activated press "OK" appears permanently but can be cancelled press "exit" or "OK"'),
'39-2' : _('Infobar activated press "OK" appears permanently but disappears press "exit" or "OK"'),
'41-3' : _('Check connection to the point in internet defined by IP adress'),
'1007-70' : _('Wake up HDD/SSD is managing by image only'),
'1007-71' : _('Wake up HDD/SSD if any function cannot read requested info if HDD/SSD is sleeping'),
'104-0' : _('auto - autodetection of tuners presented in box; value (1-19) - display selected numbers of tuners'),
'105-0' : A1T1,
'106-0' : A1T1,
'107-0' : A1T1,
'108-0' : A1T1,
'112-0' : A1T1,
'113-0' : A1T1,
'114-0' : _('Do not display flashing icon "R" in infobar'),
'114-1' : _('Display flashing icon "R" in infobar'),
'42-0' : _('Leave memory management untouched'),
'420-0' : _('Detecting AC3/Dolby in all available audio tracks'),
'420-1' : _('Detecting AC3/Dolby, Dolby Digital 5.1/2.0, DTS, AAC, Mpeg in current audio track'),
'42-1' : _('Automatic memory cleaning - refresh time: 3min'),
'42-2' : _('IP Address used for network status check - available connection to the Internet'),
'43-0' : _('Used to encoding.conf origin from active image'),
'43-1' : _('Used to encoding-user.conf located in /usr/share/enigma2'),
'45-0' : _('Channel selection works with standard functionality'),
'45-1' : _('Press "OK" - activate selected channel and channel selection no appear then press "OK" - disappear channel selection or press "exit" revert on last playd channel before activating Channel selection'),
'46-0' : _('Press "OK" to start selected item without animation'),
'46-1' : _('Press "OK" to start animation before activating selected item'),
'52-0' : _('Show Weather for selected city in the setup'),
'52-1' : _('Press ">" show Weather for next city'),
'53-0' : _('Special info screen (activated press "help") disappear press "help"'),
'53-1' : _('Special info screen (activated press "help") disappear automatically after 20s'),
'54-0' : _('Refresh time for reading ecm.info file'),
'55-0' : _('Disable autocheck of new version of the HDG'),
'55-1' : _('Enable autocheck of new version of the HDG'),
'56-0' : _('Static text - no scrolling'),
'56-1' : _('Roll up at end of text and stop wait selected seconds (text roll delay) then roll down back'),
'56-2' : _('Roll up at end of text and stop'),
'57-0' : _('Text rolling starts with delay defined in skin.xml'),
'57-1' : _('Text rolling starts with selected delay (s)'),
'58-n' : _('None special info is selected'),
'59-0' : _('Show channel name only'),
'59-1' : _('Show number and channel name'),
'59-2' : _('Show satellite position and channel name'),
'59-3' : _('Show number, satellite position and channel name'),
'60-0' : _('None info about "Provider" in infobar'),
'60-1' : _('Show info about "Provider" in infobar'),
'61-0' : _('None info about "Temperature and RPM" in infobar'),
'61-1' : _('Show info about "Temperature and RPM" in infobar'),
'62-0' : _('None info about "CPU usage and Memory usage" in infobar'),
'62-1' : _('Show info about "CPU usage and Memory usage" in infobar'),
'63-0' : _('None info about "Temperature HDD/SSD" in infobar'),
'63-1' : _('Show info about "Temperature HDD/SSD" in infobar'),
'64-0' : _('Do not display selected special info "extensions" in main menu'),
'64-1' : _('Display selected special info "extensions" in main menu'),
'65-0' : _('Temperature will be displayed with units defined in my_city_Code.txt or city_Code.txt'),
'151-0' : _('Temperature will be displayed with units defined in eWea_city_Code.txt'),
'65-c' : _('Temperature will be displayed in Celsius'),
'65-f' : _('Temperature will be displayed in Fahrenheit'),
'66-0' : _('Reconnect time for reading weather data from website in minutes'),
'67-0' : _('Reading weather data from OpenWeatherMap but you have to enter your API-key from registration on the website openweathermap.org (Registration and base API-key is free) and can be readed from /etc/openweathermap.api'),
'67-1' : _('Reading weather data from MSN website'),
'90-0' : _('"Find a city" is disabled'),
'90-1' : _('"Find a city" is disabled in extensions list'),
'90-2' : _('"Find a city" is disabled in main menu'),
'91-0' : _('Do not try get data from provider if an error is detected'),
'91-1' : _('Autoreconnect - try get data from provider if an error is detected - try with cycle in selected time while data are not ok'),
'92-0' : _('Display forecast for today and next 3 days'),
'92-1' : _('Display forecast for yesterday, today and next 3 days'),
'93-0' : _('High temperature appear in Autocolor'),
'93-1' : _('High temperature appear in selected color'),
'94-0' : _('Low temperature appear in Autocolor'),
'94-1' : _('Low temperature appear in selected color'),
'95-0' : _('Cold/warm temperature appears in selected color (Cold/Warm color)'),
'95-1' : _('Cold temperature is higher as settings of "Cold temperature" or/and Warm temperature is lower as "Warm temperature"'),
'96-0' : _('Warm temperature limit range: 15-40')+DG+"C",
'97-0' : _('Cold temperature limit range: 1-14')+DG+"C", 
'149-0' : _('Warm temperature limit range: 58-104')+DG+"F",
'150-0' : _('Cold temperature limit range: 33-57')+DG+"F",
'22-1-0' : _('HDD/SSD detected by kernel as device'),
'39-1-0' : _('Path to all required directories like picon, piconProv and more.'),
'124-0' : _('User defined path to all required directories like picon, piconProv and more.') + OKGREEN,
'126-0' : _('Channel numbers are calculated at enigma start so any change in channels order have no effect to channel numbers'),
'126-1' : _('Channel number is calculated after switching between channels always so every change in channel order is applied on calculation of channel number'),
'127-0' : _('Date format will be used from definition in skin part'),
'127-1' : _('Date format will be used as follow'),
'wa' : _('Channel logos with white background')+A1T2,
'ba' : _('Channel logos with black background')+A1T2,
'oa' : _('Channel logos for OLED display')+A1T2,
'wp' : _('Provider logos with white background'),
'bp' : _('Provider logos with black background'),
'ws' : _('Satellite logos with white background'),
'bs' : _('Satellite logos with black background'),
'wc' : _('CA system and SoftCam logos with white background'),
'bc' : _('CA system and SoftCam logos with black background'),
'h' : _('Selected option previews in setup of skin'),
'i' : _('Extra screen previews and icon sets used in infobar'),
'a' : _('Graphics used in extra screen and after download it you get more choices of Extra screen'),
'm' : _('Icons used in some menu types'),
'mb' : _('Big icons used in some menu types'),
'w' : _('Weather icons used in special and user info types: Weather, Weather light a Extended weather'),
'ww' : _('piconWeather white used as second picon type in infobar if is selected'),
'bw' : _('piconWeather black used as second picon type in infobar if is selected'),
'560-1' : _('Animated icons will be displayed'),
'560-0' : _('Static icons will be displayed'),
'wanim' : _('Animated Weather icons used in: Infobar, Special, User info type Weather or Enhanced Weather '),
'z' : _('Channel logos with picture background')+' ('+_('Package of Skylink and Freesat channels only')+')',
'wa5' : _('Channel logos with white background')+A1T2,
'ba5' : _('Channel logos with black background')+A1T2,
'p4' : _('Channel logos with transparent background')+A1T2,
'7z' : _('Tool needed to extract picon packages'),
'p4p' : _('Provider logos with transparent background'),
'p4s' : _('Satellite logos with transparent background'),
'chs' : _('Channelselection icons with transparent background used in some Channelselecion types')
}
SATLIST = [
("(0.8W) Freesat","","FREESAT","2141","3666","1804","1352","4298","4046","1206"),
(({True:"(0.8W) Digi",False:"(0.8W) Telly"}[L]),"",({True:"DIGI",False:"TELLY"}[L]),"2135","3660","1796","1344","4292","4040","1199"),
("(16.0E) Antiksat","","ANTIKSAT","2133","3658","1794","1342","4290","4038","1197"),
("(23.5E) Skylink","","SKYLINK","2146","3670","1809","1356","4302","4050","1211"),
("DVB-T sk/cz","EEEE","EEE","2139","3664","1801","1349","4296","4044","1204"),
("(45.0W) Intelsat 14 (IS-14)","C4E","450W","2096","3626","1757","1305","4258","4006","1161"),
("(30.0W) Hispasat 1D,1E","CE4","300W","2079","3610","1735","1285","4242","3990","1145"),
("(27.5W) Intelsat 907","CFD","275W","2073","3606","1730","1281","4238","3986","1141"),
("(24.5W) AlcomSat 1","D1B","248W","2068","3602","1725","1277","4234","3982","1135"),   
("(22.0W) SES 4","D34","220W","2063","3598","1721","1271","4230","3978","1131"),
("(15.0W) Telstar 12","D7A","150W","2048","3586","1708","1259","4218","3966","1119"),
("(14.0W) Express AM8","D84","140W","2045","3584","1706","1257","4216","3964","1103"),
("(12.5W) Eutelsat 12 West A","D93","125W","2041","3580","1701","1253","4212","3960","1101"),
("(11.0W) Express AM44","DA2","110W","2039","3578","1698","1251","4210","3958","1099"),
("(8.0W) Eutelsat 8 West B,D","DC0","80W","2033","3572","1691","1245","4204","3952","1092"),
("(7.0W) Nilesat 102,201/Eutelsat 7 West A","DCA","70W","2031","3570","1688","1243","4202","3950","1090"),
("(5.0W) Eutelsat 5 West A,B","DDE","50W","2026","3566","1684","1237","4198","3946","1085"),
("(4.0W) Amos 2/Amos 3","DE8","40W","2020","3560","1677","1230","4192","3940","1079"),
("(1.0W) Thor 5,6,7/Intelsat 10-02","E06","8W","2008","3550","1666","1219","4182","3930","1068"),
("(0.8W) Thor 5,6,7/Intelsat 10-02","E08","8W","2006","3548","1663","1216","4180","3928","1066"),
("(1.9E) BulgariaSat-1","13","19E","2011","3552","1668","1221","4184","3932","1070"),
("(3.0E) Eutelsat 3B","1E","30E","2013","3554","1670","1223","4186","3934","1072"),
("(3.1E) Eutelsat 3B","1F","31E","2018","3558","1675","1228","4190","3938","1077"),
("(4.8E) SES 5/Astra 4A","30","48E","2022","3562","1679","1233","4194","3942","1081"),
("(4.9E) SES 5/Astra 4A","31","48E","2024","3564","1682","1235","4196","3944","1083"),
("(7.0E) Eutelsat 7A/7B","46","70E","2029","3568","1686","1240","4200","3948","1087"),
("(9.0E) Eutelsat 9A","5A","90E","2035","3574","1693","1247","4206","3954","1094"),
("(10.0E) Eutelsat 10A","64","100E","2037","3576","1695","1249","4208","3956","1096"),
("(13.0E) Hot Bird 13B/13C/13D","82","130E","2043","3582","1704","1255","4214","3962","1105"),
("(16.0E) Eutelsat 16A","A0","160E","2050","3588","1710","1261","4220","3968","1121"),
("(19.2E) Astra 1KR,1L,1M,1N","C0","192E","2054","3592","1714","1265","4224","3972","1125"),
("(21.5E) Eutelsat 21B","D7","216E","2060","3596","1719","1269","4228","3976","1129"),
("(23.5E) Astra 3B","EB","235E","2066","3600","1723","1274","4232","3980","1133"),
("(26.0E) Badr 4,5,6","104","260E","2070","3604","1728","1279","4236","3984","1139"),
("(28.2E) Astra 2A,2E,2F,2G","11A","282E","2076","3608","1732","1283","4240","3988","1143"),
("(30.5E) Arabsat 5A,6A","131","305E","2081","3612","1738","1288","4244","3992","1147"),
("(31.5E) Astra 1G,5B","13B","315E","2083","3614","1741","1290","4246","3994","1149"),
("(33.0E) Eutelsat 33C","14A","330E","2085","3616","1743","1293","4248","3996","1151"),
("(36.0E) Eutelsat 36A,36B","168","360E","2087","3618","1746","1295","4250","3998","1153"),
("(39.0E) Hellas Sat 2","186","390E","2089","3620","1749","1297","4252","4000","1155"),
("(42.0E) Turksat 2A,3A,4A","1A4","420E","2091","3622","1752","1300","4254","4002","1157"),
("(45.0E) Intelsat 12 (IS-12)","1C2","450E","2094","3624","1755","1302","4256","4004","1159"),
("(46.0E) Azerspace-1","1CC","460E","2099","3628","1760","1307","4260","4008","1164"),
("(51.5E) Belintersat 1","203","515E","2103","3630","1762","1310","4262","4010","1166"),
("(52.0E) TurkmenAlem/MonacoSat","208","520E","2105","3632","1764","1312","4264","4012","1168"),
("(52.5E) Yahsat 1A","20D","525E","2107","3634","1766","1315","4266","4014","1171"),
("(53.0E) Express AM6","212","530E","2109","3636","1768","1317","4268","4016","1173"),
("(54.9E) Yamal 402","225","549E","2111","3638","1771","1319","4270","4018","1175"),
("(56.0E) Express AT1","230","560E","2114","3640","1774","1321","4272","4020","1177"),
("(62.0E) Intelsat 902","26C","620E","2116","3642","1776","1323","4274","4022","1180"),
("(66.0E) Intelsat 17","294","660E","2118","3644","1778","1325","4276","4024","1182"),
("(68.5E) Intelsat 20 (IS-20)","2AD","685E","2120","3646","1781","1327","4278","4026","1184"),
("(70.5E) Eutelsat 70B","2C1","705E","2122","3648","1783","1330","4280","4028","1186"),
("(74.9E) ABS 2/ABS 2A","2ED","750E","2124","3650","1785","1332","4282","4030","1188"),
("(75.0E) ABS 2/ABS 2A","2EE","750E","2126","3652","1788","1335","4284","4032","1190"),
("(85.0E) Intelsat 15/Horizons 2","352","851E","2128","3654","1790","1337","4286","4034","1193"),
("(85.1E) Intelsat 15/Horizons 2","353","851E","2131","3656","1792","1339","4288","4036","1195"),
]

"""
Author: Sean B. Palmer, inamidst.com
http://inamidst.com/code/moonphase.py
"""

def MoonPosition(now=None): 
	if now is None: 
		now = datetime.now()
	diff = now - datetime(2001, 1, 1)
	days = float(diff.days) + (float(diff.seconds) / float(86400))
	lunations = float("0.20439731") + (days * float("0.03386319269"))
	return lunations % float(1)

def MoonPhase(pos): 
	index = (pos * float(8)) + float("0.5")
	index = math.floor(index)
	return {
		0: _("New Moon"), 
		1: _("First Quarter"), 
		2: _("Waxing Crescent"), 
		3: _("Waxing Moon"), 
		4: _("Full Moon"), 
		5: _("Waning Moon"), 
		6: _("Waning Crescent"),
		7: _("Last Quarter")
		}[int(index) & 7]		
		
def MoonInfo():
	p = MoonPosition()
	return MoonPhase(p), "moon%04d.png" % round(p*100)
	
