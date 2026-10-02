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
from Components.config import config
from time import localtime, strftime
from Components.Language import language
import os
try:
	from Plugins.Extensions.setupGlass17.weaUtils import toLocale
except: pass

class g17dateFormat(VariableText, Renderer):

	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.format = "%A %B %d, %Y"
		self.fTyp = "0"
		
	def applySkin(self, desktop, parent):
		attribs = [ ]
		for (attrib, value) in self.skinAttributes:
			if attrib == "format":
				self.format = value
			elif attrib == "fTyp":
				self.fTyp = value
			else:
				attribs.append((attrib,value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = eLabel

	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))
		
	def changed(self, what):
		if self.instance:
			if what[0] != self.CHANGED_CLEAR:
				time = self.source.time
				if time is None:
					self.text = ""
				else:
					f = self.format
					try:				
						if self.fTyp == "1" and config.plugins.setupGlass17.par131.value != "D": 		
							f = config.plugins.setupGlass17.par131.value
						elif self.fTyp == "2" and config.plugins.setupGlass17.par132.value != "D": 		
							f = config.plugins.setupGlass17.par132.value
						elif self.fTyp == "3" and config.plugins.setupGlass17.par133.value != "D": 		
							f = config.plugins.setupGlass17.par133.value
						elif self.fTyp == "4" and config.plugins.setupGlass17.par134.value != "D": 		
							f = config.plugins.setupGlass17.par134.value
						elif config.plugins.setupGlass17.par127.value != "D":			
							f = config.plugins.setupGlass17.par127.value
					except: pass
					try:
						if config.plugins.setupGlass17.par138.value:			
							f = f.replace("%H","%-H")
						if config.plugins.setupGlass17.par188.value:			
							f = f.replace("%d","%-d").replace("%m","%-m")
					except: pass
					t = localtime(time)
					spos = f.find('%')
					if spos > 0:
						s = str(f[:spos]+strftime(f[spos:], t))
					else:
						s = strftime(f, t)
					try:
						self.text = toLocale(s)
					except: self.text = s
