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
from enigma import eLabel, eServiceReference, eEPGCache, eSize
from Components.VariableText import VariableText
from time import localtime, time
from skin import parseFont
from Components.config import config

class g17ShowExtEpg(VariableText, Renderer):

	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.EPGcache = eEPGCache.getInstance()
		self.numEvents = 4
		self.testSizeLabel = None           	

	GUI_WIDGET = eLabel

	def applySkin(self, desktop, parent):
		attribs = [ ]
		for (attrib, value) in self.skinAttributes:
			if attrib == "size":
				self.sizeX = int(value.strip().split(",")[0])
				attribs.append((attrib,value))
			elif attrib == "numEvents":
				self.numEvents = int(value) + 1
			elif attrib == "font":
				self.used_font = parseFont(value, ((1,1),(1,1)))
				attribs.append((attrib,value))
			else:
				attribs.append((attrib,value))
		self.skinAttributes = attribs
		self.testSizeLabel.setFont(self.used_font)
		self.testSizeLabel.resize(eSize(self.sizeX+500,20))
		self.testSizeLabel.setVAlign(eLabel.alignTop)
		self.testSizeLabel.setHAlign(eLabel.alignLeft)
		self.testSizeLabel.setNoWrap(1)
		return Renderer.applySkin(self, desktop, parent)

	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))
		
	def changed(self, what):
		if self.instance:
			if what[0] == self.CHANGED_CLEAR:
				self.text = ""
				return
			self.text = "Extended EPG is not available!"
			if what[0] != self.CHANGED_CLEAR:
				service = None
				try:
					service = self.source.service
					marker = (service.flags & eServiceReference.isMarker == eServiceReference.isMarker)
					bouquet = (service.flags & eServiceReference.flagDirectory == eServiceReference.flagDirectory)
					sname = service.toString()
				except:
					marker = False
					bouquet = False
					sname = self.source.text
				if not marker and not bouquet and self.EPGcache is not None:
					pos = sname.rfind(':')
					if pos != -1:
						sname = sname[:pos].rstrip(':')
						if not "::" in sname:
							try:
								info = service and self.source.info
							except: info = True
							if info is not None:
								epgList =  self.EPGcache.lookupEvent(['TBX', (sname, 1, -1, 1440)])
								extEpg = ""
								visible_events = self.numEvents
								from Plugins.Extensions.setupGlass17.warderEpgTextFit import fit_title_to_width
								def measure_epg(text):
									self.testSizeLabel.setText(text)
									return self.testSizeLabel.calculateSize().width()
								# Use one of the existing upcoming-event lines, not
								# additional screen height, when Prime Time is enabled.
								try:
									pt_cfg = config.plugins.warderEvolutionPrimeTime
									if pt_cfg.enabled.value:
										from Plugins.Extensions.setupGlass17.warderPrimeTime import prime_time_event
										hour, minute = [int(v) for v in pt_cfg.clock.value]
										pt = prime_time_event(self.EPGcache, service, time(), hour, minute)
										header = "Prime Time %02d:%02d: %s" % (hour, minute, pt[1] if pt else "EPG unavailable")
										extEpg = fit_title_to_width(header, max(0, self.sizeX - 30), measure_epg) + "\n"
										visible_events = max(1, self.numEvents - 1)
								except (AttributeError, IndexError, TypeError, ValueError, RuntimeError):
									pass
								for x in range(1,visible_events):
									try:
										t = localtime(int(epgList[x][1]))
										tmp = "%02d:%02d  %s" % (t.tm_hour, t.tm_min, epgList[x][0])
										tmp = fit_title_to_width(tmp, max(0, self.sizeX - 30), measure_epg)
										extEpg += "%s\n" % tmp
									except (IndexError, TypeError, ValueError):
										pass
								if extEpg != "":
									self.text = extEpg

	def preWidgetRemove(self, instance):
		self.testSizeLabel = None

	def postWidgetCreate(self, instance):
		self.testSizeLabel = eLabel(instance)
		self.testSizeLabel.hide()
		
		
		
