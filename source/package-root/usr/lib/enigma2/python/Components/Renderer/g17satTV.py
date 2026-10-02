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
from Tools.Directories import fileExists
from enigma import eServiceCenter, iServiceInformation, ePixmap, eServiceReference
from Components.config import config
ENA_TT = False
try:
	from enigma import iDVBFrontend
	ENA_TT = True
except: pass
try:
	from Plugins.Extensions.setupGlass17.weaUtils import setDefPicon, isSH
except: pass

class g17satTV(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.satCache = { }
		self.pngname = ""
		self.__isInst = True
		self.__isInstShow = True
	GUI_WIDGET = ePixmap

	def changed(self, what):
		if self.instance:
			if self.__isInst:
				self.instance.setScale(1)
				self.__isInst = False
				try:
					if config.plugins.setupGlass17.par161.value and config.plugins.setupGlass17.par166.value != "None":
						self.instance.setShowHideAnimation(config.plugins.setupGlass17.par166.value)
				except: pass
			pngname = name = ""
			if what[0] != self.CHANGED_CLEAR:
				serviceref = self.source.service
				try:
					self.__enaSH = None
					self.__enaSH = isSH()
				except: pass
				bouquet = None
				try:
					marker = (serviceref.flags & eServiceReference.isMarker == eServiceReference.isMarker)
					bouquet = (serviceref.flags & eServiceReference.flagDirectory == eServiceReference.flagDirectory)
					if marker:
						pngname = setDefPicon("marker.png")
					elif bouquet:
						pngname = setDefPicon("bouquet.png")
				except: pass
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
					info = eServiceCenter.getInstance().info(serviceref)
					if info and serviceref and pngname == "":
						try:
							sname = info.getInfoObject(serviceref, iServiceInformation.sTransponderData)
							orb = str(sname.get("tuner_type","None"))
							if ENA_TT and orb != "None":
								try:
									orb = {iDVBFrontend.feSatellite : "0",iDVBFrontend.feCable : "1",iDVBFrontend.feTerrestrial : "2",iDVBFrontend.feSatellite2 : "0",iDVBFrontend.feTerrestrial2 : "2"}[int(orb)]
								except: 
									try:
										orb = {iDVBFrontend.feSatellite : "0",iDVBFrontend.feCable : "1",iDVBFrontend.feTerrestrial : "2"}[int(orb)]
									except: pass
							if orb in ("1","DVB-C"):
								name = "picon_cable"
							elif orb in ("2","DVB-T"):
								name = "picon_trs"
							if name == "":
								if "orbital_position" in sname:	
									orb = sname["orbital_position"]
									if orb > 1800:
										orb = str(3600 - orb) + "W"
									else:
										orb = str(orb) + "E"
									name = orb
							if name != "":
								pngname = self.chckS(name)
								if pngname == "":
									pngname = self.chckS("picon_sat")
						except: pass
					if pngname == "":
						try:
							sname = serviceref.toString()
							if sname is not None and sname != "":
								if sname.startswith("4097:0") or "3a//" in sname or "http" in sname:
									pngname = self.chckS("IPTV")
						except: pass
					if pngname == "":
						pngname = self.chckS("picon_default")
						if pngname == "":
							try:
								pngname = setDefPicon()
								self.satCache["default"] = pngname
							except: pass
					if pngname != "" and self.pngname != pngname:
						self.pngname = pngname
						self.instance.setPixmapFromFile(self.pngname)            		

	def chckS(self, p):
		a = self.satCache.get(p, "")
		if a == "":
			a = self.findSat(p)
			if a != "":
				self.satCache[p] = a
		return a

	def findSat(self, serviceName):
		try:
			if self.__enaSH is None or self.__enaSH == 1:
				x = ("","_220x132")
			else:
				x = ("_220x132","")
			for i in x:
				pngname = config.plugins.setupGlass17.par39.value + "/piconSat%s/" % i + serviceName + ".png"
				if fileExists(pngname):
					return pngname
		except: pass
		return ""
