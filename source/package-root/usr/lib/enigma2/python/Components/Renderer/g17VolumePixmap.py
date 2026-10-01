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
from enigma import ePixmap, eTimer, eDVBVolumecontrol
from Tools.Directories import fileExists

class g17VolumePixmap(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.start = False 
		self.vTimer = eTimer()
		self.__last = ""
		try:
			self.vTimer_conn = self.vTimer.timeout.connect(self.changed)
		except AttributeError:
			self.vTimer.callback.append(self.changed)

	GUI_WIDGET = ePixmap

	def changed(self, what=""):
		if self.start:
			pixpath = '/usr/share/enigma2/hd_glass17/volume/%s.png' % str(eDVBVolumecontrol.getInstance().getVolume())
			if fileExists(pixpath) and self.__last != pixpath:
				self.__last = pixpath
				self.instance.setPixmapFromFile(pixpath)

	def onShow(self):
		self.start = True
		self.vTimer.start(200)

	def onHide(self):
		self.start = False
		self.vTimer.stop()	