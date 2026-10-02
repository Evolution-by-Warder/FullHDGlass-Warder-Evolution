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
from enigma import eLabel
from Components.VariableText import VariableText
try:
	from Components.Sensors import sensors
except: pass
import os
from Plugins.Extensions.setupGlass17.weaUtils import ISP38
if ISP38:
	from Plugins.Extensions.setupGlass17.py38 import DG
else:
	DG = unichr(176).encode("latin-1")
  	
class g17trpm(VariableText, Renderer):

	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.enaRefresh = -1		
		self.maxRefreshTime = 8
	GUI_WIDGET = eLabel

	def applySkin(self, desktop, parent):
		attribs = [ ]
		for (attrib, value) in self.skinAttributes:
			if attrib == "refreshTime":
				self.maxRefreshTime = int(value)
			else:
				attribs.append((attrib,value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))
		
	def changed(self, what):
		if self.instance:
			if what[0] != self.CHANGED_CLEAR:
				if self.enaRefresh > self.maxRefreshTime or self.enaRefresh == -1:
					self.enaRefresh = 0 
					temperature = "Temp.: N/A"
					temp = -1
					rpmTXT = ", Rpm: N/A"
					rpm = 0
					try:
						allsensors = sensors.getSensorsList(sensors.TYPE_TEMPERATURE)
						numtemp = len(allsensors)
						for num in range(numtemp):
							idx = allsensors[num]
							isMax = sensors.getSensorValue(idx)
							if isMax > temp:
								temp = isMax
					except:
						pass
					if temp > 0 :
						temperature = ("Temp.: " + str(temp) + DG + "C")
					try:
						allsensors = sensors.getSensorsList(sensors.TYPE_FAN_RPM)
						numtemp = len(allsensors)
						for num in range(numtemp):
							idx = allsensors[num]
							isMax = sensors.getSensorValue(idx)
							if isMax > rpm:
								rpm = isMax
					except:
						pass
					if rpm > 0 :
						rpmTXT = ", Rpm: " + str(rpm)
					self.text = temperature + rpmTXT 
				else:
					self.enaRefresh += 1

	def onHide(self):
		self.enaRefresh = -1
        					
