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
from enigma import eServiceReference, eServiceCenter, ePixmap, eSize
from Components.config import config
from ServiceReference import ServiceReference
import os, re
try:
	from Plugins.Extensions.setupGlass17.weaUtils import fixNameOf, isSH
except: pass

class g17RefTVBQT(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.pngname = ""		
		self.service_center = eServiceCenter.getInstance()
		self.__isInstShow = True
		self.__isInst = True
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
			pngname = ""
			if what[0] != self.CHANGED_CLEAR:
				service = self.source.service
				try:
					enaSH = None
					enaSH = isSH()
				except: pass
				marker = (service.flags & eServiceReference.isMarker == eServiceReference.isMarker)
				bouquet = (service.flags & eServiceReference.flagDirectory == eServiceReference.flagDirectory)
				if enaSH is None or bouquet is None or bouquet is False:
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
					info = self.service_center.info(service)		
					serviceName = info.getName(service) or ServiceReference(service).getServiceName() or ""
					if serviceName != "":
						tmp = ""
						try:
							serviceName = fixNameOf(serviceName)
						except: pass
						bb = re.search(r"\d{1,3}[,\.]\d[EW]",serviceName)
						if "DVB-C" in serviceName:
							tmp = "picon_cable"
						elif "DVB-T" in serviceName:
							tmp = "picon_trs"
						elif bb:
							tmp = fixZero((bb.group()).replace(".","").replace(",",""))
						elif "--- " in serviceName:
							serviceName = serviceName.replace("--- ","")
						pngname = self.findPicon(serviceName)
						if pngname == "" and tmp != "":
							pngname = self.findPicon(tmp)
					if pngname == "":
						pngname = "/usr/share/enigma2/hd_glass17/pidef17.png"
					if pngname != "" and self.pngname != pngname:
						self.pngname = pngname
						self.instance.setPixmapFromFile(self.pngname)            		

	def findPicon(self, serviceName):
		try:
			pngname = config.plugins.setupGlass17.par39.value + "/picon_BQT/" + serviceName + ".png"
			if os.path.isfile(pngname):
				return pngname
		except: pass
		return ""
		
