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
from Components.config import config
from Components.Renderer.Renderer import Renderer
from enigma import eLabel
from Components.VariableText import VariableText
import re

class g17ShowNetSpeed(VariableText, Renderer):

	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.__last = float(0)		
		self.onType = 99
          		
	def applySkin(self, desktop, parent):
		attribs = [ ]
		for (attrib, value) in self.skinAttributes:
			if attrib == "alwaysType":
				self.onType = int(value)
			else:
				attribs.append((attrib,value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)
		
	GUI_WIDGET = eLabel

	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))
		
	def changed(self, what):
		if self.instance and what[0] != self.CHANGED_CLEAR:
			ena = 1
			if not self.onType in (1,2):
				try:
					ena = int(config.plugins.setupGlass17.par209.value)
				except: pass
			else:
				ena = self.onType
			if ena != 0:
				sp = float(0)
				s = float(0)
				try:
					f = open("/proc/net/dev","r").readlines()
					if f:
						for i in f: 
							if ("eth" in i or "wlan" in i or "wifi" in i or "ra" in i) and ":" in i:
								s += self.calc(i)
					if s > self.__last:
						sp = s - self.__last
						sp = sp*8/1024
					if s != 0:
						self.__last = s
					if ena == 2:
						sp = sp/1024
						self.text = "%3.3f Mb/s" % sp
					else:
						self.text = "%6.1f kb/s" % sp
				except: pass
				
	def calc(self, s):
		ret = 0
		try:
			s = re.sub(r"\s+", " ", s)
			s = s.split(" ")
			ret = float(s[2]) + float(s[10])		
		except: pass
		return ret		
		
