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
from enigma import eServiceReference, ePixmap
from Components.config import config
try:
	from Plugins.Extensions.setupGlass17.weaUtils import isSH
except: pass

class g17shTVpix(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.__isInst = True
		self.__isInstShow = True
		self.pngname = "/usr/share/enigma2/hd_glass17/general/greyline17.png"

	def applySkin(self, desktop, parent):
		attribs = [ ]
		for (attrib, value) in self.skinAttributes:
			if attrib == "pixPath":
				self.pngname = value
			else:
				attribs.append((attrib,value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = ePixmap

	def changed(self, what):
		if self.instance:
			if self.__isInst:
				self.instance.setScale(1)
				self.__isInst = False
				self.instance.setPixmapFromFile(self.pngname)
			if what[0] != self.CHANGED_CLEAR:
				service = self.source.service
				try:
					enaSH = None
					enaSH = isSH()
				except: pass
				bouquet = None
				try:
					bouquet = (service.flags & eServiceReference.flagDirectory == eServiceReference.flagDirectory)
				except: pass
				if enaSH is not None and bouquet is not None and bouquet is True:
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
            		
