#######################################################################
#
#    Renderer for Enigma2
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
from Tools.LoadPixmap import LoadPixmap
from Components.Pixmap import Pixmap
from Components.Renderer.Renderer import Renderer
from enigma import eServiceReference, eServiceCenter, ePixmap, eTimer
from Tools.Directories import fileExists
from Components.config import config
try:
	from Plugins.Extensions.setupGlass17.weaUtils import setDefPicon
except: pass

class g17PicRef3(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.pngname = ""
		self.path = "picon"
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
				try:
					if config.plugins.setupGlass17.par161.value and config.plugins.setupGlass17.par166.value != "None":
						self.instance.setShowHideAnimation(config.plugins.setupGlass17.par166.value)
				except: pass
			pngname = ""
			sname = self.source.text
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
			
	def alternative(self, serviceName):
		def alternativeChannels(service):
			tmp = eServiceCenter.getInstance().list(eServiceReference(service))
			return tmp and tmp.getContent("S", True)
		if serviceName.startswith('1:134:'):
			channels = alternativeChannels(serviceName)
			if channels:
				return channels[0]
		return serviceName

	def findPicon(self, serviceName):
		try:
			pngname = "%s/%s/%s.png" % (config.plugins.setupGlass17.par39.value, self.path, serviceName)
			if fileExists(pngname):
				return pngname
		except: pass
		return ""
