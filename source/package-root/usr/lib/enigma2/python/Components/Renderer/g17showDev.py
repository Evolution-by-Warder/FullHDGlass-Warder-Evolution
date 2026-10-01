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
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, eTimer
import os
from Components.config import config

class g17showDev(Renderer):

	def __init__(self):
		Renderer.__init__(self)                    		
		self.name = ""
		self.pngname = "/usr/share/enigma2/hd_glass17/menu/dev-def.png"
		self.getDevName()
		self.delayInitTimer = eTimer()
		try:
			self.delayInitTimer_conn = self.delayInitTimer.timeout.connect(self.changed)
		except AttributeError:
			self.delayInitTimer.timeout.get().append(self.changed)
	GUI_WIDGET = ePixmap

	def changed(self, what=""):
		if self.delayInitTimer.isActive():
			self.delayInitTimer.stop()
		if self.instance and self.pngname != self.name:
			try:
				self.instance.setScale(1)
				self.instance.setPixmapFromFile(self.pngname)
				self.name = self.pngname
			except: pass
		else:
			self.delayInitTimer.start(500)
      		
	def getDevName(self):
		try:
			for x in ("boxtype","vumodel","model"):
				if os.path.exists("/proc/stb/info/"+x):
					dev = open("/proc/stb/info/"+x,'r').read().strip()
					if x == "vumodel" and not "vu" in dev:
						dev = "vu"+dev
					break
			dev = "%s/menuIcons/%s/%s.png" % (config.plugins.setupGlass17.par39.value, config.plugins.setupGlass17.par69.value, dev)
			if os.path.isfile(dev):
				self.pngname = dev
		except: pass
	
