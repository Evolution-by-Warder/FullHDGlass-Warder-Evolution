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

class g17cutCHSS(VariableText, Renderer):

	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		
	GUI_WIDGET = eLabel

	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))
		
	def changed(self, what):
		if self.instance:
			if what[0] != self.CHANGED_CLEAR:
				txt = self.source.text
				try:
					a = ""
					if "/" in txt and ("Bouquets" in txt or "bouquets" in txt):
						a = "/"
					elif "(TV)" in txt:
						a = "(TV)"
					elif "(Radio)" in txt:
						a = "(Radio)"
					if a != "":
						a = a.join((txt.strip().split(a))[1:])
						if a != "":
							txt = a
					txt = " ".join(txt.strip().split(" "))
				except: pass
				self.text = txt


