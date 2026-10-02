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
from Components.VariableValue import VariableValue
from Components.Renderer.Renderer import Renderer
from enigma import eSlider

class g17Progress(VariableValue, Renderer):
	def __init__(self):
		Renderer.__init__(self)
		VariableValue.__init__(self)
		self.__start = 0
		self.__end = 100

	GUI_WIDGET = eSlider

	def changed(self, what):
		if what[0] == self.CHANGED_CLEAR:
			(self.range, self.value) = ((0, 1), 0)
			return

		range = self.source.range or 100
		v = int(100*self.source.value/range)
		if v is None:
			v = 0
		elif v < 10:
			v = 0		
		elif v < 20:
			v = 10
		elif v < 30:
			v = 20
		elif v < 40:
			v = 30
		elif v < 50:
			v = 40
		elif v < 60:
			v = 50
		elif v < 70:
			v = 60
		elif v < 80:
			v = 70
		elif v < 90:
			v = 80
		elif v < 99:
			v = 90
		else:
			v = 100
		(self.range, self.value) = ((0, range), v)

	GUI_WIDGET = eSlider

	def postWidgetCreate(self, instance):
		instance.setRange(self.__start, self.__end)

	def setRange(self, range):
		(self.__start, self.__end) = range
		if self.instance is not None:
			self.instance.setRange(self.__start, self.__end)

	def getRange(self):
		return (self.__start, self.__end)

	range = property(getRange, setRange)
