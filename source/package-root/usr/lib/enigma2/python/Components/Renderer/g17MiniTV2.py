#
#  MiniTV - Renderer (OpenAtv)
#
#  This plugin is licensed under the Creative Commons
#  Attribution-NonCommercial-ShareAlike 3.0 Unported
#  License. To view a copy of this license, visit
#  http://creativecommons.org/licenses/by-nc-sa/3.0/
#  or send a letter to Creative Commons, 559 Nathan
#  Abbott Way, Stanford, California 94305, USA.
#
#  This plugin is NOT free software. It is open source,
#  you are allowed to modify it (if you keep the license),
#  but it may not be commercially distributed other than
#  under the conditions noted above.
#

from Components.Renderer.Renderer import Renderer
from enigma import eVideoWidget, getDesktop, eTimer
from Screens.InfoBar import InfoBar
from Components.SystemInfo import SystemInfo

FBTool = None

def setFormat(x=105,y=435,w=600,h=330):
	fb_w = getDesktop(0).size().width()
	fb_h = getDesktop(0).size().height()
	x = format(int(float(x) / fb_w * 720.0), 'x').zfill(8)
	y = format(int(float(y) / fb_h * 576.0), 'x').zfill(8)
	w = format(int(float(w) / fb_w * 720.0), 'x').zfill(8)
	h = format(int(float(h) / fb_h * 576.0), 'x').zfill(8)
	return [w, h, x, y]

class g17MiniTV2(Renderer):
	def __init__(self):
		Renderer.__init__(self)
		global FBTool
		FBTool = FBHelper()		
		self.Position = self.Size = None		
		self.timer = eTimer()
		self.timer.callback.append(self.showpip)
		self.pipCreated = False
		self.pipRemoved = False
		self.Initialized = False
		self.decoder = 0
		if SystemInfo.get("NumVideoDecoders", 1) > 1:
			self.decoder = 1
		self.fb_size = None
		self.fb_size2 = setFormat()

	GUI_WIDGET = eVideoWidget

	def postWidgetCreate(self, instance):
		desk = getDesktop(0)
		instance.setDecoder(self.decoder)
		instance.setFBSize(desk.size())

	def applySkin(self, desktop, parent):
		if self.skinAttributes is not None:
			attribs = []
			for (attrib, value) in self.skinAttributes:
				if attrib == "position2":
					x1 = value.split(',')[0]
					y1 = value.split(',')[1]
				elif attrib == "size2":
					w1 = value.split(',')[0]
					h1 = value.split(',')[1]
				else:
					attribs.append((attrib, value))
				if attrib == "position":
					x = value.split(',')[0]
					y = value.split(',')[1]
				elif attrib == "size":
					w = value.split(',')[0]
					h = value.split(',')[1]
			self.skinAttributes = attribs
			self.fb_size = setFormat(x,y,w,h)				
			self.fb_size2 = setFormat(x1,y1,w1,h1)
		ret = Renderer.applySkin(self, desktop, parent)
		if ret:
			self.Position = self.instance.position()
			self.Size = self.instance.size()
		return ret

	def onShow(self):
		self.timer.stop()
		self.pipCreated = False
		self.pipRemoved = False
		self.Initialized = True
		if self.instance:
			if self.decoder > 0:
				if InfoBar.instance and not InfoBar.instance.session.pipshown:
					InfoBar.instance.showPiP()
					self.pipCreated = True
				if self.fb_size:
					FBTool.setFBSize(self.fb_size, self.decoder)
				FBTool.setFBSize_delayed(self.fb_size2, decoder = 0, delay = 200)
			else:
				if self.Size:
					self.instance.resize(self.Size)
				if self.Position:
					self.instance.move(self.Position)

	def changed(self, what):
		if InfoBar.instance:
			current = self.source.getCurrentService()
			service = current and current.toString()
			radio = service and service.startswith("1:0:2")
			if radio and InfoBar.instance.session.pipshown:
				InfoBar.instance.servicelist.setCurrentSelection(current)
				InfoBar.instance.servicelist.zap()
			else:
				if InfoBar.instance.session.pipshown:
					InfoBar.instance.session.pip.playService(current)
				else:
					InfoBar.instance.session.nav.playService(current)

	def onHide(self):
		if self.instance:
			if InfoBar.instance and self.Initialized == True:
				if self.pipCreated == True:
					if self.pipRemoved == False:
						InfoBar.instance.showPiP()
						self.pipRemoved = True
				elif self.decoder > 0:
					self.timer.start(5000)

	def showpip(self):
		self.timer.stop()
		InfoBar.instance.showPiP()

class FBHelper:
	def __init__(self):
		self.fb_proc_path = "/proc/stb/vmpeg"
		self.fb_info = ["dst_width", "dst_height", "dst_left", "dst_top"]
		self.new_fb_size_pos = None
		self.decoder = None
		self.delayTimer = None
		self.is_PiG = False

	def getFBSize(self, decoder = 0):
		ret = []
		for val in self.fb_info:
			try:
				f = open("%s/%d/%s" % (self.fb_proc_path, decoder, val), "r")
				fb_val = f.read().strip()
				ret.append(fb_val)
				f.close()
			except IOError:
				pass
		if len(ret) == 4:
			return ret
		return None

	def setFBSize(self, fb_size_pos, decoder = 0, force = False):
		if self.delayTimer:
			self.delayTimer.stop()
		if (InfoBar.instance and InfoBar.instance.session.pipshown) or force:
			if fb_size_pos and len(fb_size_pos) >= 4:
				i = 0
				for val in self.fb_info:
					try:
						f = open("%s/%d/%s" % (self.fb_proc_path, decoder, val), "w")
						fb_val = fb_size_pos[i]
						f.write(fb_val)
						f.close()
					except IOError:
						pass
					i += 1
				for val in ("00000001", "00000000"):
					try:
						f = open("%s/%d/%s" % (self.fb_proc_path, decoder, "dst_apply"), "w")
						f.write(val)
						f.close()
					except IOError:
						pass

	def delayTimerFinished(self):
		fb_size_pos = self.new_fb_size_pos
		decoder = self.decoder
		self.new_fb_size_pos = None
		self.decoder = None
		if not self.is_PiG:
			self.setFBSize(fb_size_pos, decoder)

	def setFBSize_delayed(self,fb_size_pos, decoder = 0, delay = 1000):
		if fb_size_pos and len(fb_size_pos) >= 4:
			self.new_fb_size_pos = fb_size_pos
			self.decoder = decoder
			self.delayTimer = eTimer()
			self.delayTimer.callback.append(self.delayTimerFinished)
			self.delayTimer.start(delay)
