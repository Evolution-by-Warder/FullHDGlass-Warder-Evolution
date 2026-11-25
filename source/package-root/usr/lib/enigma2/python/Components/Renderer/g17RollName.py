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
from Plugins.Extensions.setupGlass17.warderMipsRuntime import MIPS_RUNTIME, RendererTimerGuard
from enigma import eLabel
from enigma import ePoint, eTimer
from Components.VariableText import VariableText
from Tools.HardwareInfo import HardwareInfo

class g17RollName(VariableText, Renderer):

	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.direct = "R"
		self.x = self.start = 10
		self.OLED_size = 132
		if HardwareInfo().get_device_name() == 'dm800se':
			self.OLED_size = 96
		self.__moveLCD1Text = eTimer()
		if MIPS_RUNTIME:
			self._warder_timer_guard = RendererTimerGuard(self.__moveLCD1Text, self.__moveLCD1TextRun)
		else:
			try:
				self.__moveLCD1Text_conn = self.__moveLCD1Text.timeout.connect(self.__moveLCD1TextRun)
			except AttributeError:
				self.__moveLCD1Text.timeout.get().append(self.__moveLCD1TextRun)

	def applySkin(self, desktop, parent):
		attribs = [ ]
		for (attrib, value) in self.skinAttributes:
			if attrib == "position":
				self.posX = int(value.strip().split(",")[0])
				self.posY = int(value.strip().split(",")[1])
			attribs.append((attrib,value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)
                     		
	GUI_WIDGET = eLabel

	if MIPS_RUNTIME:
		def postWidgetCreate(self, instance):
			Renderer.postWidgetCreate(self, instance)
			self._warder_timer_guard.attach()

		def preWidgetRemove(self, instance):
			self._warder_timer_guard.detach()
			Renderer.preWidgetRemove(self, instance)

		def doSuspend(self, suspended):
			self._warder_timer_guard.suspend(suspended)
			if not suspended and self._warder_timer_guard.ready(self.instance) and self.source is not None and hasattr(self, 'posX'):
				self.changed((self.CHANGED_DEFAULT,))

		def destroy(self):
			guard = getattr(self, '_warder_timer_guard', None)
			if guard is not None:
				guard.detach()
			Renderer.destroy(self)


	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))
		
	def changed(self, what):
		if MIPS_RUNTIME:
			self.__moveLCD1Text.stop()
		if what[0] == self.CHANGED_CLEAR:
			self.text = ""
		else:
			self.text = self.source.text
			if HardwareInfo().get_device_name() != 'dm7020hd':
				self.text = (self.text).upper()
		if self.instance and (not MIPS_RUNTIME or (self._warder_timer_guard.ready(self.instance) and what[0] != self.CHANGED_CLEAR and hasattr(self, 'posX'))):
			text_width = self.instance.calculateSize().width()
			if self.__moveLCD1Text.isActive():
				self.__moveLCD1Text.stop()
			if self.posX > 9:
				self.x = self.posX
				self.oled_size = self.OLED_size - self.posX
			else:
				self.x = 10
				self.oled_size = self.OLED_size
			self.start = self.x
			if text_width > self.oled_size:
				self.end = self.oled_size - text_width - 15
				self.direct = "R"
				self.__moveLCD1Text.start(10000)						
			self.instance.move(ePoint(self.x,self.posY))
         
	def __moveLCD1TextRun(self):
		if MIPS_RUNTIME and (not getattr(self, '_warder_timer_guard', None) or not self._warder_timer_guard.ready(getattr(self, 'instance', None))):
			return
		self.__moveLCD1Text.stop()
		if self.x != self.end and self.direct == "R":
			self.x = self.x-1       
		elif self.x != self.start and self.direct == "L":
			self.x = self.x+1
		elif self.x == self.start:
			self.direct = "R"        
		elif self.x == self.end:
			self.direct = "L"        
		self.instance.move(ePoint(self.x,self.posY))
		self.__moveLCD1Text.start(90)       			
