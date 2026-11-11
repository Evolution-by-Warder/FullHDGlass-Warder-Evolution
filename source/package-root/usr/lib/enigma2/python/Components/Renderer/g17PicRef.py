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
import NavigationInstance
from Components.Converter.WarderRadioOnly import is_native_dab
from Tools.LoadPixmap import LoadPixmap
from Components.Pixmap import Pixmap
from Components.Renderer.Renderer import Renderer
from enigma import eServiceReference, eServiceCenter, ePixmap
from Tools.Directories import fileExists
from Components.config import config
try:
	from Plugins.Extensions.setupGlass17.weaUtils import setDefPicon
except: pass

class g17PicRef(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.pngname = ""
		self.path = "picon"
		self.__isInst = True
    		
	def applySkin(self, desktop, parent):
		attribs = [ ]
		for (attrib, value) in self.skinAttributes:
			if attrib == "path":
				self.path = value
			else:
				attribs.append((attrib,value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)
		
	GUI_WIDGET = ePixmap

	def changed(self, what):
		if self.instance:
			if self.__isInst:
				self.instance.setScale(1)
				self.__isInst = False
				try:
					if config.plugins.setupGlass17.par161.value and config.plugins.setupGlass17.par162.value != "None":
						self.instance.setShowHideAnimation(config.plugins.setupGlass17.par162.value)
				except: pass
			pngname = ""
			if what[0] == self.CHANGED_CLEAR:
				self.pngname = ""
				self.instance.hide()
				return
			if what[0] != self.CHANGED_CLEAR:
				reference = self.source.text
				sname = reference
				nav = NavigationInstance.instance
				playing = nav and nav.getCurrentlyPlayingServiceReference()
				native_dab = is_native_dab(playing)
				if native_dab:
					from Components.Renderer.Picon import getPiconName
					pngname = getPiconName(playing.toString()) or ""
				if sname is not None and sname != "" and not native_dab:
					tmp = self.alternative(sname).split(':', 10)[:10]
					sname = '_'.join(tmp)
					pngname = self.findPicon(sname)
					if pngname == "" and len(sname) > 11:
						if sname.startswith('4097'):
							tmp = sname.split('_')
							tmp[0] = '1'
							sname = '_'.join(tmp)
							pngname = self.findPicon(sname)
						if pngname == "":
							pngname = self.findPicon(sname[:-10]+"0000_0_0_0")
							if pngname == "":
								for i in ("1","19","16"):
									if i != tmp[2]:
										tmp[2] = i
										sname = '_'.join(tmp)
										pngname = self.findPicon(sname)
										if pngname == "":
											pngname = self.findPicon(sname[:-10]+"0000_0_0_0")
											if pngname != "":
												break
										else:
											break
			if pngname == "" and not native_dab:
				# Satellite radio can use a name-based or system-configured picon
				# that the legacy reference-only skin lookup cannot resolve.
				fields = (reference or "").split(":", 10)
				if len(fields) >= 10 and fields[2].upper() in ("2", "A"):
					try:
						from Components.Renderer.Picon import getPiconName
						pngname = getPiconName(reference) or ""
					except (ImportError, AttributeError):
						pass
			if pngname == "":
				pngname = self.findPicon("picon_default")
				if pngname == "":
					try:
						pngname = setDefPicon()
					except: pass
			if pngname != "" and self.pngname != pngname:
				self.pngname = pngname
				self.instance.setPixmapFromFile(self.pngname)
			if pngname:
				self.instance.show()
			else:
				self.pngname = ""
				self.instance.hide()

	def alternative(self, serviceName):
		def alternativeChannels(service):
			tmp = eServiceCenter.getInstance().list(eServiceReference(service))
			return tmp and tmp.getContent("S", True)
		if serviceName.startswith('1:134:'):
			channels = alternativeChannels(serviceName)
			if channels:
				return channels[0]
		return serviceName

	def findPicon(self, serviceName):
		try:
			base = config.plugins.setupGlass17.par39.value
			from Plugins.Extensions.setupGlass17.warderUserPicons import selected_source
			override, custom = selected_source(config)
			fields = (self.source.text or "").split(":", 10)
			radio = len(fields) >= 10 and fields[2].upper() in ("2", "A")
			paths = ("picon", "picon_220x132", "picon_400x240") if self.path == "picon" and radio else (self.path,)
			# An explicitly selected expert destination is a picon directory,
			# not a skin-data root. It takes priority over the PATHS default.
			if override and self.path in ("picon", "picon_50x30", "picon_220x132", "picon_400x240"):
				pngname = "%s/%s.png" % (custom.rstrip("/"), serviceName)
				if fileExists(pngname):
					return pngname
			for path in (() if override and self.path in ("picon", "picon_50x30", "picon_220x132", "picon_400x240") else paths):
				pngname = "%s/%s/%s.png" % (base, path, serviceName)
				if fileExists(pngname):
					return pngname
			# Resolve aliases only within Warder's configured private data root.
			# Never use a system picon here: it may belong to an older installation.
			if self.path in ("picon", "picon_50x30", "picon_220x132", "picon_400x240"):
				from Plugins.Extensions.setupGlass17.warderChannelPicons import find_picon
				from Tools.Alternatives import GetWithAlternative
				from Tools.Directories import sanitizeFilename
				from ServiceReference import ServiceReference
				return find_picon(
					self.source.text, base, GetWithAlternative,
					lambda ref: ServiceReference(ref).getServiceName(),
					sanitizeFilename, prefer_mini=self.path == "picon_50x30",
					custom_folder=custom if override else None)
		except (AttributeError, ImportError, OSError, TypeError, ValueError):
			pass
		return ""
