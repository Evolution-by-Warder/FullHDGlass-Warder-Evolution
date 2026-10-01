#######################################################################
#
#    Converter for Enigma2
#    Coded by shamann (c)2021
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
from Components.Renderer.Renderer import Renderer
from enigma import eServiceReference, eServiceCenter, ePixmap
from Components.config import config
from ServiceReference import ServiceReference
import os, re
try:
	from Plugins.Extensions.setupGlass17.weaUtils import fixNameOf, setDefPicon, isSH
except: pass

class g17RefTV(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.pngname = ""
		self.service_center = eServiceCenter.getInstance()
		self.__isInst = True
		self.__isInstShow = True
	GUI_WIDGET = ePixmap

	def changed(self, what):
		def fixZero(w):
			if w[0] == "0":
				w = w[1:]		
			return w
		if self.instance:
			if self.__isInst:
				self.instance.setScale(1)
				self.__isInst = False
				try:
					if config.plugins.setupGlass17.par161.value and config.plugins.setupGlass17.par166.value != "None":
						self.instance.setShowHideAnimation(config.plugins.setupGlass17.par166.value)
				except: pass
			pngname = ""
			if what[0] != self.CHANGED_CLEAR:
				service = self.source.service
				try:
					self.__enaSH = None
					self.__enaSH = isSH()
				except: pass
				marker = (service.flags & eServiceReference.isMarker == eServiceReference.isMarker)
				bouquet = (service.flags & eServiceReference.flagDirectory == eServiceReference.flagDirectory)
				if self.__enaSH is not None and bouquet is not None and bouquet is True:
					try:
						if self.__isInstShow:
							self.instance.hide()
							self.__isInstShow = False
					except: pass
				else:
					try:
						if self.__isInstShow is False:
							self.instance.show()
							self.__isInstShow = True
					except: pass
					if marker:
						try:
							pngname = setDefPicon("marker.png")
						except: pass
					else:
						sname = service.toString()
						if sname is not None and sname != "":
							tmp = self.alternative(sname).split(':', 10)[:10]
							sname = '_'.join(tmp)
							pngname = self.findPicon(sname)
							if pngname == "" and len(sname) > 11:
								if sname.startswith('4097'):
									tmp = sname.split('_')
									tmp[0] = '1'
									sname = '_'.join(tmp)
									pngname = self.findPicon(sname)
								if pngname == "":
									pngname = self.findPicon(sname[:-10]+"0000_0_0_0")
									if pngname == "":
										for i in ("1","19","16"):
											if i != tmp[2]:
												tmp[2] = i
												sname = '_'.join(tmp)
												pngname = self.findPicon(sname)
												if pngname == "":
													pngname = self.findPicon(sname[:-10]+"0000_0_0_0")
													if pngname != "":
														break
												else:
													break
					if pngname == "":
						if bouquet:
							info = self.service_center.info(service)		
							serviceName = info.getName(service) or ServiceReference(service).getServiceName() or ""
							if serviceName != "":
								tmp = ""
								try:
									serviceName = fixNameOf(serviceName)
								except: pass
								bb = re.search(r"(\d{1,3}[,\.]\d[EW])",serviceName)
								if "DVB-C" in serviceName:
									tmp = "picon_cable"
								elif "DVB-T" in serviceName:
									tmp = "picon_trs"
								elif bb:
									tmp = fixZero((bb.group()).replace(".","").replace(",",""))
								if tmp != "":
									pngname = self.findPicon(tmp, "piconSat")
								if pngname == "":					
									pngname = self.findPicon(serviceName.replace("--- ",""), "piconProv")
									if pngname == "":
										try:
											pngname = setDefPicon("bouquet.png")
										except: pass
						else:
							pngname = self.findPicon("picon_default")
							if pngname == "":
								try:
									pngname = setDefPicon()
								except: pass
					if pngname != "" and self.pngname != pngname:
						self.pngname = pngname
						self.instance.setPixmapFromFile(self.pngname)
            		
	def alternative(self, serviceName):
		def alternativeChannels(service):
			tmp = eServiceCenter.getInstance().list(eServiceReference(service))
			return tmp and tmp.getContent("S", True)
		if serviceName.startswith('1:134:'):
			channels = alternativeChannels(serviceName)
			if channels:
				return channels[0]
		return serviceName

	def findPicon(self, serviceName, typ="picon"):
		try:
			if self.__enaSH is None or self.__enaSH == 1:
				x = ("","_400x240","_220x132")
			else:
				x = ("_220x132","","_400x240")
			for i in x:
				pngname = "%s/%s/%s.png" % (config.plugins.setupGlass17.par39.value, typ + i, serviceName)
				if os.path.isfile(pngname):
					return pngname
		except: pass
		return ""
