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
from Tools.Directories import fileExists
from Components.config import config
from enigma import ePixmap, eTimer

def Writelog(txt):
	f = "/tmp/missing_menu_icons.txt"
	if fileExists(f):
		try:
			ff = open(f, "r").read()
			if ff.find(txt) != -1:
				txt = ""
		except IOError: pass
	if txt != "":
		try:
			f = open(f,"a")
			f.write("%s\n" % str(txt))
			f.close()
		except IOError: pass

class g17MenuEntry(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.delayInitTimer = eTimer()
		self.__isInst = True
		self.__last = ""
		try:
			self.delayInitTimer_conn = self.delayInitTimer.timeout.connect(self.changed)
		except AttributeError:
			self.delayInitTimer.timeout.get().append(self.changed)		
	GUI_WIDGET = ePixmap
        
	def changed(self, what=None):
		if self.delayInitTimer.isActive():
			self.delayInitTimer.stop()
		if self.instance:
			if self.__isInst:
				self.instance.setScale(1)
				self.__isInst = False
				try:
					if config.plugins.setupGlass17.par161.value and config.plugins.setupGlass17.par165.value != "None":
						self.instance.setShowHideAnimation(config.plugins.setupGlass17.par165.value)
				except: pass
			pixpath = "/usr/share/enigma2/hd_glass17/menu/undefined.png"
			try:
				pixpath = config.plugins.setupGlass17.par39.value + '/menuIcons/' + str(config.plugins.setupGlass17.par69.value) + "/" + self.source.entryName + '.png'
				if not fileExists(pixpath):
					pixpath = config.plugins.setupGlass17.par39.value + '/menuIcons/' + str(config.plugins.setupGlass17.par69.value) + "/undefined.png"
					Writelog(self.source.entryName + '.png')
					if not fileExists(pixpath):
						pixpath = "/usr/share/enigma2/hd_glass17/menu/undefined.png"
			except: pass
			if self.__last != pixpath:
				self.__last = pixpath
				self.instance.setPixmapFromFile(pixpath)					
		else:
			self.delayInitTimer.start(50)        
