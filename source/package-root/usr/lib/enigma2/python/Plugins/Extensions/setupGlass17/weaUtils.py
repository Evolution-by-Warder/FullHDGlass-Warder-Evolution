from Components.config import config
from socket import socket, AF_INET, SOCK_STREAM
try:
	from string import upper
except: pass
import os
import codecs
import time as time1
from datetime import date, time
import math
from Components.Language import language
SHAREPATH = "/usr/share/enigma2/"
SKINPATH = "/usr/share/enigma2/hd_glass17/"
XML_FILE = "/tmp/weather.xml"
NO_WEATHER_PICON = "/usr/share/enigma2/hd_glass17/icons/3200.png"
WLANG = language.getLanguage().replace("_","-")
if WLANG.upper() in ["NO-NO","CA-AD","SR-YU","EN-EN"]:
	WLANG = "en-us"
WLANG = WLANG[:2]	
try:
	import sys
	ISP38 = sys.version_info[0] == 3
except: 
	ISP38 = os.path.exists("/usr/lib/python3.8")
if ISP38:
	from Plugins.Extensions.setupGlass17.py38 import DG
else:
	DG = unichr(176).encode("latin-1")
lcMonths = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
if os.path.isfile('/etc/lcstrings.list') is True:
	myfile = open('/etc/lcstrings.list', 'r')
	lang = language.getActiveLanguage()
	for line in myfile.readlines():
		if line.startswith(str(lang)):
			line = line.strip().split(":")[1]
			lcMonths = (line.replace("\t","").replace(" ","")).strip().split(',')
			break
	myfile.close()

def chMSN():
	# MSN weather.service.msn.com is retired; FullHDGlass17 now always uses OpenWeatherMap.
	return False
	
def toLocale(s):
	WeekDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	Months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
	for index, weekday in enumerate(WeekDays): 
		if s.find(weekday) >= 0:
			s = s.replace(weekday, _(weekday))
			break
	for index, month in enumerate(Months): 
		if s.find(month) >= 0:
			s = s.replace(month, lcMonths[index])		
			break
	return s

def nigttime(v):		
	try:
		if not config.plugins.setupGlass17.par24.value:
			v = v.replace("27","28").replace("29","30").replace("31","32").replace("27","28").replace("33","34")
	except: pass
	return v
			
def temperature_fix(tt,ena=True):
	if ena and tt[0] != '-' and tt[0] != '0':
		tt = '+' + tt
	return tt+DG
      
def chckUnit():
	a = config.plugins.setupGlass17.par86.value
	return ({False: a, True:config.plugins.setupGlass17.par13.value[0]}[a == "0"])
    
def netChck(a=None):
	try:
		chck = socket(AF_INET, SOCK_STREAM)
		chck.settimeout(0.8)
		ena = False
		if a is None:
			ena = chMSN()
			a = ({False: 'openweathermap.org', True:'weather.service.msn.com'}[ena])
		b = not bool(chck.connect_ex((a, 80)))
		if not ena:
			return b
		elif not b:
			return not bool(chck.connect_ex(('www.msn.com', 80)))
		return b 
	except: pass
	return False
    
def setFcolor(w, c, v=None):
	if v:
		v = 'backgroundColor="'
	else:
		v = 'foregroundColor="'
	if not v in w:
		return w.replace('<widget', '<widget %s%s"' % (v,c)) + "\n"
	return w.replace('%s%s"' % (v,(w.split(v)[1]).split('"')[0]), '%s%s"' % (v,c)) + "\n"              			
 			
def fixUtf8(what):
	if what is None:
		return ""
	if not ISP38:
		what = what.replace('\xc2\x86', '').replace('\xc2\x87', '').decode("utf-8", "ignore").encode("utf-8") or ""
		return codecs.decode(what, 'UTF-8')
	else:
		return what.replace('\x86', '').replace('\x87', '')
		
def sinrad(deg):
	return math.sin(deg * math.pi/180)

def cosrad(deg):
	return math.cos(deg * math.pi/180)

def convertToDate(d):
	d += 0.5
	s = int((d-int(d))*24*60*60+.5)
	m = int(s/60)
#	h = int(m/60)+time1.localtime().tm_isdst+time1.localtime().tm_hour - time1.gmtime().tm_hour  
	h = int(m/60)+time1.localtime().tm_hour - time1.gmtime().tm_hour  
	if h < 0:
		h += 24
	if h == 24:
		h = 0
	return time(h, m % 60, s % 60)
    
def calcSun(longitude, latitude, day=0):
	dt = date.today()
	a = math.floor((14-dt.month)/12)
	y = dt.year+4800-a
	m = dt.month+12*a -3
	julian_date = day+dt.day+math.floor((153*m+2)/5)+365*y+math.floor(y/4)-math.floor(y/100)+math.floor(y/400)-32045    
	nstar = (julian_date - 2451545.0 - 0.0009)-(longitude/360)
	n = round(nstar)
	jstar = 2451545.0+0.0009+(longitude/360) + n
	M = (357.5291+0.98560028*(jstar-2451545)) % 360
	c = (1.9148*sinrad(M))+(0.0200*sinrad(2*M))+(0.0003*sinrad(3*M))
	l = (M+102.9372+c+180) % 360
	jtransit = jstar + (0.0053 * sinrad(M)) - (0.0069 * sinrad(2 * l))
	delta = math.asin(sinrad(l) * sinrad(23.45))*180/math.pi
	H = math.acos((sinrad(-0.83)-sinrad(latitude)*sinrad(delta))/(cosrad(latitude)*cosrad(delta)))*180/math.pi
	jstarstar = 2451545.0+0.0009+((H+longitude)/360)+n
	jset = jstarstar+(0.0053*sinrad(M))-(0.0069*sinrad(2*l))
	jrise = jtransit-(jset-jtransit)
	return (convertToDate(jrise), convertToDate(jset))

def ignZero(v):
	v = v.strip().split()[0]
	if config.plugins.setupGlass17.par138.value and v[0] == "0" and len(v) == 5:
		v = v[1:]
	elif not config.plugins.setupGlass17.par138.value and len(v) == 4:
		v = "0" + v		
	return v		

def fixNameOf(t):
	try:				
		if t.startswith("T-K"):
			t = "T-KABEL"
		elif t == "T-Systems/MTI":
			t = "T-SYSTEMS"
		t = ''.join(i for i in t if ord(i)<128)
		t = t.replace("\t","").strip().upper()
		t = t.replace(",","").replace("(","").replace(")","")
	except: pass
	return t    
            		
def setDefPicon(t="picon_default.png"):
	t = SKINPATH + t
	if os.path.isfile(t):
		return t
	else:
		return SHAREPATH + "skin_default/picon_default.png"
		
def readECMlabels(all=True):
	a = "CAM:\nCAID:\nProv.:\nPrvID:\nPID:\nUsing:\nProt.:\nAddr.:\nHops:\nShare:\nTime:\nSys.:"
	b = "..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n.............."
	c = b + "\n.............."
	if config.plugins.setupGlass17.par50.value:
		a += "\nCW0:\nCW1:"
		b += "\n..............\n.............."
	if all:
		return a,b,c
	else:
		return a,b		

def calc(dd,d,v,s='"',c=True):
	if v == "0":
		return dd
	a = dd.split(d)
	b = a[1].split(s)
	b[0] = b[0].strip()
	if b[0].isdigit():			
		b[0] = str(v) if c else str(int(b[0])+int(v))
	return a[0]+ d + s.join(b)

def setSideECM(w):
	if config.plugins.setupGlass17.par50.value:
		ww = w.split("\n")
		w = ""
		for i in ww:
			if 'name="ecmlabels"' in i: 
				w += calc(i,"Prive3;",-3,c=False)
			elif 'name="ecmValues"' in i: 
				w += calc(calc(i,"Prive3;",-3,c=False),'position="',-15,',',False)
			else:
				w += i
			w += "\n"
	return w

allIPTVprov = {}
for x in ("my_","enigma2/my_","","enigma2/"):
	if os.path.isfile('/etc/%siptvprov.list' % x) is True:
		f = open('/etc/%siptvprov.list' % x, 'r')
		for i in f.readlines():
			if "," in i:
				a = i.replace("\n","")
				a = a.strip().split(",")
				if len(a) == 2 and not a[0] in allIPTVprov:
					allIPTVprov[a[0]] = a[1].upper()

def chckIPTVprov(r):
	ret = 'STREAM'
	if len(allIPTVprov) != 0:
		for x in list(allIPTVprov.keys()):
			if x in r:
				ret = allIPTVprov.get(x)
				break
	return ret

def chckWidI(a,b):
	ret = "3200"
	ico = {
	"200":"4","201":"3","202":"3","210":"4","211":"4","212":"3","221":"37","230":"38","231":"38","232":"3",
	"300":"11","301":"11","302":"12","310":"12","311":"11","312":"12","313":"11","314":"12","321":"11",
	"500":"11","501":"11","502":"40","503":"40","504":"40","511":"8","520":"39","521":"12","522":"40","531":"39",
	"600":"13","601":"13","602":"14","611":"13","612":"13","615":"13","616":"8","620":"13","621":"13","622":"14",
	"701":"20","711":"22","721":"21","731":"19","741":"20","751":"21","761":"21","762":"21","771":"24","781":"24",
	"800":"32","801":"30","802":"30","803":"28","804":"28",
	"n800":"31","n803":"27","n802":"29"
	}
	try:
		if "n." in str(a) and "n"+b in ico:
			ret = ico.get("n"+b)
		elif b in ico:
			ret = ico.get(b)
	except: pass
	return ret

def isSH():	
	try:
		if config.plugins.setupGlass17.par19.value == "53":
			return 0
		elif config.plugins.setupGlass17.par19.value == "54":
			return 1
	except: pass		
	return None		

def dewpoint(Tc=0, RH=93, minRH=(0, 0.075)[0]):
	Es = 6.11 * 10.0**(7.5 * Tc / (237.7 + Tc))
	RH = RH or minRH  
	E = (RH * Es) / 100
	try:
		DewPoint = (-430.22 + 237.7 * math.log(E)) / (-math.log(E) + 19.08)
	except ValueError:
		DewPoint = 0 
	return str(int(DewPoint))

		