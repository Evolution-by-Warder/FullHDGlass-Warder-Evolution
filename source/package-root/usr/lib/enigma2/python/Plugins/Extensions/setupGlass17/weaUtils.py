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
	# Compatibility shim: all Warder weather data now comes from Open-Meteo.
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
			a = 'api.open-meteo.com'
		return not bool(chck.connect_ex((a, 443))) 
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

		
# Open-Meteo compatibility helpers (FullHDGlass17 9.50-r5)
def weaText(v):
	try:
		if not ISP38 and isinstance(v, unicode):
			return v.encode('utf-8')
	except: pass
	if v is None: return ''
	return str(v)

def wmoPicon(code, night=False):
	try: code = int(code)
	except: return '3200'
	if code == 0: return '31' if night else '32'
	if code == 1: return '33' if night else '34'
	if code == 2: return '29' if night else '30'
	if code == 3: return '26'
	if code in (45,48): return '20'
	if code in (51,53,55,56,57): return '11'
	if code in (61,63,65,66,67,80,81,82): return '12'
	if code in (71,73,75,77,85,86): return '13'
	if code == 95: return '4'
	if code in (96,99): return '3'
	return '3200'

def wmoText(code):
	# Keep Classic Weather and Enhanced Weather on the same Open-Meteo/WMO
	# vocabulary so the active Enigma2 language catalog can translate both.
	texts={0:'Clear sky',1:'Mainly clear',2:'Partly cloudy',3:'Overcast',45:'Fog',48:'Depositing rime fog',51:'Light drizzle',53:'Drizzle',55:'Dense drizzle',56:'Freezing drizzle',57:'Freezing drizzle',61:'Slight rain',63:'Rain',65:'Heavy rain',66:'Freezing rain',67:'Heavy freezing rain',71:'Slight snow',73:'Snow',75:'Heavy snow',77:'Snow grains',80:'Rain showers',81:'Rain showers',82:'Heavy rain showers',85:'Snow showers',86:'Heavy snow showers',95:'Thunderstorm',96:'Thunderstorm with hail',99:'Thunderstorm with heavy hail'}
	try: return _(texts.get(int(code),'Unknown'))
	except: return _('Unknown')

def windDir(deg):
	dirs=('N','NE','E','SE','S','SW','W','NW')
	try: return dirs[int((float(deg)+22.5)//45)%8]
	except: return 'N'

_OPENMETEO_CACHE = {}

def openMeteo(city, unit='C', days=6):
	try:
		# Reuse the last successful Open-Meteo response inside Enigma2.
		# This prevents the Infobar from starting with N/A while a second
		# identical geocoding/forecast request is still in progress.
		ckey = ('%s' % (city or '')).strip().lower() + '|' + str(unit).upper() + '|' + str(days)
		cached = _OPENMETEO_CACHE.get(ckey)
		if cached and (time1.time() - cached[0]) < 600:
			return cached[1]
		if ISP38:
			from urllib.request import Request, urlopen
			from urllib.parse import urlencode
		else:
			from urllib2 import Request, urlopen
			from urllib import urlencode
		try: import simplejson as _json
		except: import json as _json
		def get(url):
			r=urlopen(Request(url,headers={'User-Agent':'FullHDGlass17/9.50-r5'}),timeout=12)
			try: raw=r.read()
			finally:
				try:r.close()
				except:pass
			if not ISP38:
				try: raw=raw.decode('utf-8')
				except: pass
			elif not isinstance(raw,str): raw=raw.decode('utf-8','replace')
			return _json.loads(raw)
		city=city.strip() if city else ''
		if not city or city == 'None': raise ValueError('City is not defined')
		search_name=city; country=''; district=''; postal=''
		if city.startswith('om|'):
			parts=city.split('|')
			search_name=parts[1] if len(parts)>1 else ''
			country=parts[2] if len(parts)>2 else ''
			district=parts[3] if len(parts)>3 else ''
			postal=parts[4] if len(parts)>4 else ''
		gp={'name':search_name,'count':100 if (district or postal) else 1,'language':WLANG[:2],'format':'json'}
		if country: gp['countryCode']=country
		g=get('https://geocoding-api.open-meteo.com/v1/search?'+urlencode(gp))
		rs=g.get('results') or []
		if not rs: raise ValueError('City not found')
		loc=rs[0]
		if district or postal:
			dl=district.lower()
			pc=postal.replace(' ','')
			for rr in rs:
				admin=(' '.join([str(rr.get('admin1','')),str(rr.get('admin2','')),str(rr.get('admin3','')),str(rr.get('admin4',''))])).lower()
				rp=str(rr.get('postcodes',''))+str(rr.get('postcode',''))
				if (not dl or dl in admin) and (not pc or pc in rp.replace(' ','')):
					loc=rr; break
		lat=float(loc['latitude']); lon=float(loc['longitude']); uf=str(unit).upper()=='F'
		p={'latitude':lat,'longitude':lon,'timezone':'auto','forecast_days':max(1,min(int(days),10)),'current':'temperature_2m,relative_humidity_2m,apparent_temperature,is_day,weather_code,surface_pressure,wind_speed_10m,wind_direction_10m,visibility','daily':'weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,wind_speed_10m_max,wind_direction_10m_dominant','temperature_unit':'fahrenheit' if uf else 'celsius','wind_speed_unit':'mph' if uf else 'kmh'}
		d=get('https://api.open-meteo.com/v1/forecast?'+urlencode(p)); d['_location']=loc
		_OPENMETEO_CACHE[ckey] = (time1.time(), d)
		return d
	except Exception as e:
		raise e