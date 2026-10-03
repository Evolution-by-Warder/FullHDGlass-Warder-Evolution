# -*- coding: utf-8 -*-
# Warder Evolution: Radio-only top rail used by the normal InfoBar.
# Original FullHDGlass17 credits remain in the project.
from Components.Renderer.Renderer import Renderer
from Components.VariableText import VariableText
from Components.config import config
from enigma import eLabel, eTimer
from time import localtime, strftime, time
try:
	from Plugins.Extensions.setupGlass17.weaUtils import toLocale
except Exception:
	def toLocale(value):
		return value

class WarderRadioInfoBarTop(VariableText, Renderer):
	GUI_WIDGET = eLabel

	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.mode = "time"
		self.timer = eTimer()
		try:
			self.timer_conn = self.timer.timeout.connect(self._refresh)
		except AttributeError:
			self.timer.timeout.get().append(self._refresh)

	def applySkin(self, desktop, parent):
		attribs = []
		for attrib, value in self.skinAttributes:
			if attrib == "mode":
				self.mode = value
			else:
				attribs.append((attrib, value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	def connect(self, source):
		Renderer.connect(self, source)
		self._refresh()
		self.timer.start(500, False)

	def preWidgetRemove(self, instance):
		try:
			self.timer.stop()
		except Exception:
			pass
		Renderer.preWidgetRemove(self, instance)

	def changed(self, what):
		self._refresh()

	def _isRadio(self):
		try:
			ref = self.source.text or ""
			fields = ref.split(":")
			return len(fields) > 2 and fields[2].upper() == "A"
		except Exception:
			return False

	def _date(self):
		fmt = "%A  %d.%B %Y"
		try:
			if config.plugins.setupGlass17.par134.value != "D":
				fmt = config.plugins.setupGlass17.par134.value
			if config.plugins.setupGlass17.par138.value:
				fmt = fmt.replace("%H", "%-H")
			if config.plugins.setupGlass17.par188.value:
				fmt = fmt.replace("%d", "%-d").replace("%m", "%-m")
		except Exception:
			pass
		try:
			return toLocale(strftime(fmt, localtime()))
		except Exception:
			return strftime(fmt, localtime())

	def _refresh(self):
		if not self.instance:
			return
		if not self._isRadio():
			self.text = ""
			return
		if self.mode == "date":
			self.text = self._date()
		elif self.mode == "brand":
			self.text = "FullHDGlass17 · Warder Evolution"
		else:
			self.text = strftime("%H:%M:%S", localtime())
