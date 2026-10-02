from enigma import eTimer
from Components.Converter.Converter import Converter
from Components.config import config

class g17ConditionalShowHide(Converter, object):
	def __init__(self, argstr):
		Converter.__init__(self, argstr)
		args = [x.strip() for x in argstr.replace(';', ',').split(',')]
		self.invert = "Invert" in args
		self.blink = "Blink" in args
		self.blinktime = next((int(x) for x in args if x.isdigit()), 500)
		if self.blink:
			self.timer = eTimer()
			try:
				self.timer_conn = self.timer.timeout.connect(self.blinkFunc)
			except Exception:
				self.timer_conn = None
				self.timer.callback.append(self.blinkFunc)
		else:
			self.timer = None

	def blinkFunc(self):
		if self.blinking == True:
			for x in self.downstream_elements:
				x.visible = not x.visible

	def startBlinking(self):
		self.blinking = True
		self.timer.start(self.blinktime)

	def stopBlinking(self):
		self.blinking = False
		for x in self.downstream_elements:
			if x.visible:
				x.hide()
		self.timer.stop()

	def calcVisibility(self):
		b = self.source.boolean
		if b is None:
			b = False
		b ^= self.invert
		return b

	def changed(self, what):
		try:
			if not config.plugins.setupGlass17.par114.value:
				return
		except: pass
		vis = self.calcVisibility()
		if self.blink:
			if vis:
				self.startBlinking()
			else:
				self.stopBlinking()
		else:
			for x in self.downstream_elements:
				x.visible = vis
		Converter.changed(self, what)

	def connectDownstream(self, downstream):
		Converter.connectDownstream(self, downstream)
		vis = self.calcVisibility()
		if self.blink:
			if vis:
				self.startBlinking()
			else:
				self.stopBlinking()
		else:
			downstream.visible = self.calcVisibility()

	def destroy(self):
		if self.timer:
			try:
				if self.timer_conn is not None:
					self.timer_conn = None
				elif self.blinkFunc in self.timer.callback:
					self.timer.callback.remove(self.blinkFunc)
			except Exception:
				pass
