#######################################################################
#
#    Renderer for Enigma2
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
from enigma import eServiceCenter, iPlayableServicePtr, eServiceReference, ePixmap
from Components.config import config
try:
	from Plugins.Extensions.setupGlass17.weaUtils import fixNameOf, setDefPicon, chckIPTVprov, isSH
except: pass
try:
	from string import upper
except: pass

class g17provTV(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.provCache = { }
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
				service = self.source.service
				try:
					self.__enaSH = None
					self.__enaSH = isSH()
				except: pass
				bouquet = None
				try:
					marker = (service.flags & eServiceReference.isMarker == eServiceReference.isMarker)
					bouquet = (service.flags & eServiceReference.flagDirectory == eServiceReference.flagDirectory)
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
					if isinstance(service, iPlayableServicePtr):
						info = service and service.info()
						ref = None
					else:  
						info = service and self.source.info
						ref = service
					if info is not None and pngname == "":
						try:
							if isinstance(ref, eServiceReference):
								from Screens.ChannelSelection import service_types_radio, service_types_tv
								typestr = ref.getData(0) in (2, 10) and service_types_radio or service_types_tv
								pos = typestr.rfind(':')
								rootstr = '%s (channelID == %08x%04x%04x) && %s FROM PROVIDERS ORDER BY name' % (typestr[:pos + 1], ref.getUnsignedData(4), ref.getUnsignedData(2), ref.getUnsignedData(3), typestr[pos + 1:])
								provider_root = eServiceReference(rootstr)
								serviceHandler = eServiceCenter.getInstance()
								providerlist = serviceHandler.list(provider_root)
								if not providerlist is None:
									while True:
										provider = providerlist.getNext()
										if not provider.valid(): break
										if provider.flags & eServiceReference.isDirectory:
											servicelist = serviceHandler.list(provider)
											if not servicelist is None:
												while True:
													s = servicelist.getNext()
													if not s.valid(): break
													if s == ref:
														info = serviceHandler.info(provider)
														name = info and info.getName(provider) or ""
														if name != "":
															name = fixNameOf(name)
						except: pass
					try:
						sname = service.toString()
						if sname is not None and sname != "":
							if sname.startswith("4097:0") or "3a//" in sname or "http" in sname:
								pngname = self.chckP(fixNameOf(chckIPTVprov(sname)))
							elif name != "":
								sname = sname.split(':', 10)[:10]
								sname = '_'.join(sname)
								sname = ((sname[:-10]).split('_')[6]).upper()
								pngname = self.chckP(sname + "x" + name)
					except: pass
					if pngname == "":
						try:
							if name != "":
								pngname = self.chckP(name)
						except: pass
					if pngname == "":
						pngname = self.chckP("picon_default")
						if pngname == "":
							try:
								pngname = setDefPicon()
								self.provCache["default"] = pngname
							except: pass
					if pngname != "" and self.pngname != pngname:
						self.pngname = pngname
						self.instance.setPixmapFromFile(self.pngname)            		

	def chckP(self, p):
		a = self.provCache.get(p, "")
		if a == "":
			a = self.findProv(p)
			if a != "":
				self.provCache[p] = a
		return a

	def findProv(self, serviceName):
		try:
			if self.__enaSH is None or self.__enaSH == 1:
				x = ("","_220x132")
			else:
				x = ("_220x132","")
			for i in x:
				pngname = config.plugins.setupGlass17.par39.value + "/piconProv%s/" % i + serviceName + ".png"
				if fileExists(pngname):
					return pngname
		except: pass
		return ""
