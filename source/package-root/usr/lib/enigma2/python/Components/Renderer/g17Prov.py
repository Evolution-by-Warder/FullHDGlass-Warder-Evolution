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
from Tools.LoadPixmap import LoadPixmap
from Components.Pixmap import Pixmap
from Components.Renderer.Renderer import Renderer
from enigma import eServiceReference, ePixmap, iServiceInformation, eTimer
from Tools.Directories import fileExists
from Components.config import config
try:
	from Plugins.Extensions.setupGlass17.weaUtils import fixNameOf, setDefPicon, chckIPTVprov
except: pass
import NavigationInstance
try:
	from string import upper
except: pass

class g17Prov(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.pngname = ""
		self.path = "piconProv"
		self.__isInst = True
		self.delayTimer = eTimer()
		try:
			self.delayTimer_conn = self.delayTimer.timeout.connect(self.changed)
		except AttributeError:
			self.delayTimer.timeout.get().append(self.changed)
          		
	def applySkin(self, desktop, parent):
		attribs = [ ]
		for (attrib, value) in self.skinAttributes:
			if attrib == "path":
				self.path = value
			else:
				attribs.append((attrib,value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)
		
	GUI_WIDGET = ePixmap

	def changed(self, what=None):
		if self.delayTimer.isActive():
			self.delayTimer.stop()
		if self.instance:
			if self.__isInst:
				self.instance.setScale(1)
				self.__isInst = False
			pngname = ""
			nav = NavigationInstance.instance
			if nav:
				service = nav.getCurrentService()
				info = service and service.info()
				if info is not None:
					refer = eServiceReference(info.getInfoString(iServiceInformation.sServiceref))
					if refer is not None:
						refer = refer.toString()
						if refer.startswith("-1:"):
							refer = nav.getCurrentlyPlayingServiceReference()
							if refer is not None:
								refer = refer.toString()
						try:
							if refer.startswith("4097:0") or "3a//" in refer or "http" in refer:							
								pngname = self.findPicon(fixNameOf(chckIPTVprov(refer)))
							else:
								sname = refer.split(':', 10)[:10]
								sname = '_'.join(sname)
								sname = ((sname[:-10]).split('_')[6]).upper()
								name = fixNameOf(self.getServiceInfoValue(info, iServiceInformation.sProvider))
								pngname = self.findPicon(sname + "x" + name)						
						except: pass
						try:
							if pngname == "":
								pngname = self.findPicon(fixNameOf(self.getServiceInfoValue(info, iServiceInformation.sProvider)))						
						except: pass
			if pngname == "":
				pngname = self.findPicon("picon_default")
				if pngname == "":
					try:
						pngname = setDefPicon()
					except: pass
			if pngname != "" and self.pngname != pngname:
				self.pngname = pngname
				self.instance.setPixmapFromFile(self.pngname)
		else:
			self.delayTimer.start(50) 
			
	def findPicon(self, serviceName):
		try:
			pngname = "%s/%s/%s.png" % (config.plugins.setupGlass17.par39.value, self.path, serviceName)
			if fileExists(pngname):
				return pngname
		except: pass
		return ""

	def getServiceInfoValue(self, info, what, ref=None):
		v = ref and info.getInfo(ref, what) or info.getInfo(what)
		if v != iServiceInformation.resIsString:
			return ""
		return ref and info.getInfoString(ref, what) or info.getInfoString(what)
