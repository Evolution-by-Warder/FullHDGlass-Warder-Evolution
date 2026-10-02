#######################################################################
#
#    ScreenSaver for Enigma2
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

from Screens.Screen import Screen
from Components.Label import Label
from enigma import eTimer, ePoint, gRGB, eSize, iPlayableServicePtr, iPlayableService
from time import localtime, time, strftime
import random
from Components.ServiceEventTracker import ServiceEventTracker
try:
	from string import upper
except: pass

class ScreenSaverScreen(Screen):                  

	skin = """<screen name="ScreenSaver" position="0,0" size="1920,1080" zPosition="-1" backgroundColor="#00000000" flags="wfNoBorder" >	

		<widget name="saver_text" font="Prive3;36" position="127,115" zPosition="3" size="600,75" halign="center" backgroundColor="#31000000" transparent="1" />

    </screen>"""
                            	
	def __init__(self, session):
		Screen.__init__(self, session)
		self.skin = ScreenSaverScreen.skin
		self.session = session    
		self.suspend = True
		self['saver_text'] = Label("") 
		self.Sname = "- - -"
		self.__refreshTimer = eTimer()
		try:
			self.__refreshTimer_conn = self.__refreshTimer.timeout.connect(self.__updateInfo)
		except AttributeError:
			self.__refreshTimer.timeout.get().append(self.__updateInfo)    
		self.__colorTimer = eTimer()
		try:
			self.__colorTimer_conn = self.__colorTimer.timeout.connect(self.__updateColor)
		except AttributeError:
			self.__colorTimer.timeout.get().append(self.__updateColor)
		self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evStopped: self.noServiceName, iPlayableService.evStart: self.readServiceName, iPlayableService.evTunedIn: self.readServiceName,})
		self.onShow.append(self.__wakeup)
		self.onHide.append(self.__standby)
		self.colorR = 200
		self.colorG = 100
		self.colorB = 0
		self.DcolorR = 2
		self.DcolorG = 2
		self.DcolorB = 2
		self.ena = 0
		self.delay = 0 
                                      	
	def noServiceName(self):
		self.Sname = " "

	def __wakeup(self):
		self.readPosition()
		self.direction = "+"
		self.newsizeY = 75
		self.ena = 0
		self.__refreshTimer.start(10)
		self.__colorTimer.start(10)
		
	def readPosition(self):
		self.posX = self['saver_text'].instance.position().x()
		self.posY = self['saver_text'].instance.position().y()
		self.newposY = self.posY
		
	def readServiceName(self):
		service = self.session.nav.getCurrentService()
		if isinstance(service, iPlayableServicePtr):
			info = service and service.info()
			ref = None
		else:
			info = service and self.source.info
			ref = service
		if info is None:
			self.Sname = " "
		name = ref and info.getName(ref)
		if name is None:
			name = info.getName()
		self.Sname = name.replace('\xc2\x86', '').replace('\xc2\x87', '').upper()
    		
	def __standby(self):
		self.__refreshTimer.stop()
		self.__colorTimer.stop()
		self['saver_text'].instance.resize(eSize(600,75))
        	  		
	def __updateInfo(self):
		self.__refreshTimer.stop()
		t = localtime(time())
		self['saver_text'].setText("%s\n%s" % (self.Sname, strftime("%d %B %Y, %H:%M:%S", t)))	
		if self.ena == 1:
			self['saver_text'].instance.move(ePoint((random.randint(50, 1320)),(random.randint(50, 905))))
			self.readPosition()
			self.direction = "-"
			self.newsizeY = 0
			self.ena = 2
		elif self.ena == 3:
			self.readPosition()
			self.direction = "+"
			self.newsizeY = 75
			self.ena = 0
		elif self.ena == 4:
			self.delay += 1
			if self.delay == 4:
				self.ena = 3
				self.delay = 0
		self.__refreshTimer.start(1000)	
      		
	def __updateColor(self):
		self.__colorTimer.stop() 
		self.colorR += self.DcolorR
		if self.colorR > 255:  
			self.DcolorR = -2  
			self.colorR += self.DcolorR
		elif self.colorR < 0:  
			self.DcolorR = 2  
			self.colorR += self.DcolorR
		self.colorG += self.DcolorG
		if self.colorG > 255:  
			self.DcolorG = -2  
			self.colorG += self.DcolorG
		elif self.colorG < 0:  
			self.DcolorG = 2  
			self.colorG += self.DcolorG  
		self.colorB += self.DcolorB
		if self.colorB > 255:  
			self.DcolorB = -2  
			self.colorB += self.DcolorB
		elif self.colorB < 0:  
			self.DcolorB = 2  
			self.colorB += self.DcolorB   
		try:  
			self['saver_text'].instance.setForegroundColor(gRGB(int(("%0.2X%0.2X%0.2X" % (self.colorR, self.colorG, self.colorB)), 0x10)))  
		except: pass  
		if self.ena == 0 or self.ena == 2:
			if self.newposY > self.posY+75 or self.newsizeY < 0:
				self.ena = 1
			elif self.newposY < self.posY-75 or self.newsizeY > 75:
				self.ena = 4
			else:      
				if self.direction == "+": 
					self.newposY += 1
					self.newsizeY -= 1
				else: 
					self.newposY -= 1
					self.newsizeY += 1
				if self.newsizeY < 0:
					self['saver_text'].instance.resize(eSize(600, 0))
				else:
					self['saver_text'].instance.resize(eSize(600, int(self.newsizeY)))
				self['saver_text'].instance.move(ePoint(int(self.posX), int(self.newposY)))
		self.__colorTimer.start(30)  
  		
		
