#######################################################################
#
#    Concerter for Enigma2
#    Coded by shamann (c)2020
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
from Components.config import config
from Components.Converter.Converter import Converter
from Components.Element import cached
from enigma import eServiceCenter, eServiceReference, iServiceInformation, iPlayableServicePtr, eDVBFrontendParametersTerrestrial	
from Plugins.Extensions.setupGlass17.weaUtils import ISP38
if ISP38:
	from Plugins.Extensions.setupGlass17.py38 import DG
else:
	DG = unichr(176).encode("latin-1")
ENA_S = False
try:
	if config.plugins.setupGlass17.par126.value == "0":
		ENA_S = True
except: pass
BQR = '1:7:2:0:0:0:0:0:0:0:FROM BOUQUET "bouquets.radio" ORDER BY bouquet'
BQT = '1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "bouquets.tv" ORDER BY bouquet'

class g17ServiceNum(Converter, object):
	NUMBERANDNAMEEVENT = 1
	NUMBERANDNAME = 2
	NUMBER = 3
  	
	def __init__(self, type):
		Converter.__init__(self, type)		
		self.serviceCenter = eServiceCenter.getInstance()
		self.lastService = None
		self.lastNum = ""
		self.count = 0
		if type == "Number":
			self.type = self.NUMBER
		elif type == "NumberAndName":
			self.type = self.NUMBERANDNAME
		elif type == "NumberAndNameEvent":
			self.type = self.NUMBERANDNAMEEVENT
		if ENA_S:
			self.allChBq  = {}				
			for x in (BQT,BQR):
				tot_num = 0 
				allBqt = self.serviceCenter.list(eServiceReference(x)) 		
				Bouquets = allBqt and allBqt.getContent("SN", True)
				for bq in Bouquets:
					q = self.clean(bq[0])
					srv = self.serviceCenter.list(eServiceReference(bq[0]))
					chs = srv and srv.getContent("SN", True)
					for ch in chs:
						if not ch[0].startswith('1:64:'):	 
							tot_num += 1
							self.allChBq[ch[0]+q] = tot_num
							if ":http" in ch[0] or ":rtmp" in ch[0] or ":rtsp" in ch[0]:
								self.allChBq[self.cleanCH(ch[0])+q] = tot_num							

	@cached
	def getText(self):
		service = self.source.service
		if self.type != self.NUMBERANDNAMEEVENT:
			info = service and service.info()
			if not info:
				return "---"		
		if self.type == self.NUMBER:
			return self.getNumber()
		elif self.type == self.NUMBERANDNAME:
			if isinstance(service, iPlayableServicePtr):
				info = service and service.info()
				ref = None
			else:
				info = service and self.source.info
				ref = service
			if info is None:
				return "Unknown Channel"
			name = ref and info.getName(ref)
			if name is None:
				name = info.getName()					
			return "%s%s%s" % (self.isEnaNumber(), self.isEnaSat(ref, info), name.replace('\xc2\x86', '').replace('\xc2\x87', ''))
		elif self.type == self.NUMBERANDNAMEEVENT:
			num = ""
			name = "Unknown Channel"
			try:
				info = service and self.source.info
				if info is not None:
					name = service and info.getName(service)
					if name is None:
						name = info.getName()
				num = self.isEnaNumber()
			except: pass
			return "%s%s" % (num, name.replace('\xc2\x86', '').replace('\xc2\x87', ''))

	text = property(getText)

	def isEnaSat(self, ref, info):
		try:
			if not config.plugins.setupGlass17.par79.value in ["2","3"]:
				return ""
		except: pass
		if ref:
			tp = info.getInfoObject(ref, iServiceInformation.sTransponderData)
		else:
			tp = info.getInfoObject(iServiceInformation.sTransponderData)
		if tp:
			if "orbital_position" in list(tp.keys()):
				numSat = int(tp["orbital_position"])
				ret = ({True:str((float(3600 - numSat))/10.0) + DG + "W", False:str((float(numSat))/10.0) + DG + "E"}[numSat > 1800])
				return "(%s) " % ret
			elif "tuner_type" in list(tp.keys()):
				ret = str(tp.get("tuner_type","None"))
				if ret in ["DVB-C","1"]:
					return "(DVB-C) "
				if ret in ["DVB-T","2","4"]:
					ret = "DVB-T"
					try:
						ret = {
									eDVBFrontendParametersTerrestrial.System_DVB_T : "DVB-T",
									eDVBFrontendParametersTerrestrial.System_DVB_T2 : "DVB-T2"
								}[tp.get("system", eDVBFrontendParametersTerrestrial.System_DVB_T)]
					except: pass
					return "(%s) " % ret
		try:
			ret = info.getInfoString(iServiceInformation.sServiceref)
			if ret.startswith("4097:0") or "http" in ret or "rtmp" in ret or "rtsp" in ret: 
				return "(IPTV) "
		except: pass
		return ""

	def isEnaNumber(self):
		try:
			if not config.plugins.setupGlass17.par79.value in ["1","3"]:
				return ""
		except: pass
		return self.getNumber()

	def getNumber(self):
		try:
			service = self.source.serviceref
			num = service and service.getChannelNum() or None
		except:
			num = None
		if num:
			return str(num) + ". "
		else:
			service = self.source.service
			if isinstance(service, iPlayableServicePtr):
				info = service and service.info()
				ref = None
			else:
				info = service and self.source.info
				ref = service
			ref = ref or eServiceReference(info.getInfoString(iServiceInformation.sServiceref))
			rr = None
			if info:
				try:
					rr = info.getInfoString(iServiceInformation.sServiceref)
				except: pass
			if self.lastService is not None and service is not None:
				if rr is not None and self.lastService == rr:
					if self.count > 2:
						return self.lastNum
				else:
					self.count = 0
			self.count += 1
			self.lastService = rr
			self.lastNum = self.getLastNum(ref,service)
			return self.lastNum

	def getLastNum(self,ref,service):
		i = 0
		if isinstance(ref, eServiceReference):
			isRadioService = ref.getData(0) in (2,10)
			lastpath = isRadioService and config.radio.lastroot.value or config.tv.lastroot.value
			if not 'FROM BOUQUET' in lastpath:
				if 'FROM PROVIDERS' in lastpath:
					return '(P)'
				if 'FROM SATELLITES' in lastpath:
					return '(S)'
				if ') ORDER BY name' in lastpath:
					return '(A)'
				return 'N/A'
			root = ''
			for x in lastpath.split(';'):
				if x != '':
					root = x
			if ENA_S:
				i = self.allChBq.get(ref.toString()+self.clean(root),0)
			else:
				try:
					acount = config.plugins.NumberZapExt.enable.value and config.plugins.NumberZapExt.acount.value or config.usage.alternative_number_mode.value
				except:
					acount = False
				if acount is True or not config.usage.multibouquet.value:
					service, i = self.calcNum(ref, 0, eServiceReference(root))
				else:
					if isRadioService:
						rootBqt = BQR
					else:
						rootBqt = BQT
					actBqt = eServiceReference(root)
					allBqt = self.serviceCenter.list(eServiceReference(rootBqt))
					if allBqt is not None:
						while True:
							bqt = allBqt.getNext()
							if not bqt.valid():
								break
							if bqt.flags & eServiceReference.isDirectory:
								ena = actBqt == bqt
								service, i = self.calcNum(ref, i, bqt, ena)
								if service is not None and ena:
									break
			if service is not None and i != 0:
				return str(i) + ". "
		return ""				        	

	def calcNum(self, ref, x, bqt, ena=True):
		servicelist = self.serviceCenter.list(bqt)
		if servicelist is not None:
			chs = servicelist and servicelist.getContent("SN", True)
			for ch in chs:
				if not ch[0].startswith('1:64:'):	
					x += 1
					if ena:
						ss = ch[0]
						if ss == ref.toString():
							return ss, x
						if ":http" in ss or ":rtmp" in ss or ":rtsp" in ss:
							ss = self.cleanCH(ss)
						if ss == ref.toString():
							return ss, x
		return None, x

	def clean(self, t):
		return t.replace('FROM BOUQUET','').replace('"','').replace('ORDER BY bouquet','').replace(' ','').replace('userbouquet','').replace('.','')

	def cleanCH(self, t):
		a = ":http"
		if ":rtmp" in t:
			a = ":rtmp"
		elif ":rtsp" in t:
			a = ":rtsp"
		t = t.split(a)
		a = ""
		b = t[1].split(":")
		for x in range(1,len(b)):
			a += b[x]
		return t[0]+"::"+a
		return t
		
