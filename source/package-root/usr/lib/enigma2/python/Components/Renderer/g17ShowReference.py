#######################################################################
#
#    Renderer for Enigma2
#    Coded by shamann (c)2021
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
from enigma import eServiceReference, eServiceCenter
try:
	from Plugins.Extensions.setupGlass17.txt import NO_REF
	from Plugins.Extensions.setupGlass17.weaUtils import isSH
	if isSH() is not None:
		NO_REF = ""
except: NO_REF = 'Reference is not detected'

class g17ShowReference(VariableText, Renderer):

	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		
	GUI_WIDGET = eLabel

	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))
		
	def changed(self, what):
		if self.instance:
			self.text = NO_REF
			if what[0] != self.CHANGED_CLEAR:
				service = self.source.service
				marker = (service.flags & eServiceReference.isMarker == eServiceReference.isMarker)
				bouquet = (service.flags & eServiceReference.flagDirectory == eServiceReference.flagDirectory)
				sname = service.toString()
				if not marker and not bouquet and sname is not None and sname != "":
					marker = '_'
					try:
						if config.plugins.setupGlass17.par179.value != "a":
							marker = ':' 
					except: pass
					tmp = self.alternative(sname).split(':', 10)[:10]
					if len(tmp) > 0 and tmp[0] == '4097':
						tmp[0] = '1'
					self.text = "Reference: " + marker.join(tmp)

	def alternative(self, serviceName):
		def alternativeChannels(service):
			tmp = eServiceCenter.getInstance().list(eServiceReference(service))
			return tmp and tmp.getContent("S", True)
		if serviceName.startswith('1:134:'):
			channels = alternativeChannels(serviceName)
			if channels:
				return channels[0]
		return serviceName
		
