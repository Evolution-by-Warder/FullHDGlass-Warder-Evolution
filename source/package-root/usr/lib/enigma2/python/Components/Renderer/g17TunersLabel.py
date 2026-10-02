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
from enigma import eLabel, eCanvas, eRect, eSize, gRGB, gFont, RT_HALIGN_LEFT, RT_WRAP
from skin import parseColor, parseFont
from Components.NimManager import nimmanager
from enigma import eDVBResourceManager, iPlayableService, iRecordableService, iPlayableServicePtr, iRecordableServicePtr, eTimer
from Components.config import config
import os

class g17TunersLabel(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.tuners = 4         	
		self.fcolor = parseColor("#000077ff")
		self.bcolor = parseColor("#31000000")
		self.Acolor = parseColor("#0000d100")
		self.BAcolor = parseColor("#00ecb100")
		self.Mcolor = parseColor("#00777777")
		self.RECcolor = parseColor("#00dd0000")
		self.RECLcolor = parseColor("#00dd00ff")
		self.used_font = gFont("Regular", 24)	
		self.Nfont = "Regular" 
		self.Hfont = 24
		self.hfont = self.Hfont
		self.W = self.H =0
		self.mask = 0
		self.posLR = "C"
		self.name = "A"
		self.all = []
		self.sepW = 5
		self.recT = []
		self.isInput = False
		self.__noFirst = False
		self.noClear = True
		res_mgr = eDVBResourceManager.getInstance()
		if res_mgr:
			try:
				self.frontendInputUseMaskChanged_conn = res_mgr.frontendInputUseMaskChanged.connect(self.re_changed)
			except AttributeError:
				try:
					self.frontendUseMaskChanged_conn = res_mgr.frontendUseMaskChanged.connect(self.re_changed)
				except AttributeError:
					res_mgr.frontendUseMaskChanged.get().append(self.re_changed)
		self.testSizeLabel = None 
		self.__updTimer = eTimer()
		try:
			self.__updTimer_conn = self.__updTimer.timeout.connect(self.chckRT)
		except AttributeError:
			self.__updTimer.timeout.get().append(self.chckRT)
		self.__updTimer.startLongTimer(40)                            		

	GUI_WIDGET = eCanvas

	def applySkin(self, desktop, parent):
		attribs = [ ]
		for (attrib, value) in self.skinAttributes:
			if attrib == "tuners":
				self.tuners = int(value)
				if self.tuners > 20 or self.tuners < 1:
					self.tuners = 4
			elif attrib == "font":
				self.used_font = parseFont(value, ((1,1),(1,1)))
				self.Nfont, self.Hfont = value.split(';')
				self.Hfont = int(self.Hfont.strip())
				self.hfont = self.Hfont
			elif attrib == "TunerColor":
				self.fcolor = parseColor(value)
			elif attrib == "ActiveTunerColor":
				self.Acolor = parseColor(value)
			elif attrib == "backgroundColor":
				self.bcolor = parseColor(value)
			elif attrib == "BackgroundActiveTunerColor":
				self.BAcolor = parseColor(value)
			elif attrib == "MissingTunerColor":
				self.Mcolor = parseColor(value)
			elif attrib == "RecordTunerColor":
				self.RECcolor = parseColor(value)
			elif attrib == "RecordandLiveTunerColor":
				self.RECLcolor = parseColor(value)
			elif attrib == "PosLR":
				self.posLR = value
			else:
				attribs.append((attrib,value))
		self.skinAttributes = attribs
		self.testSizeLabel.setFont(self.used_font)
		self.testSizeLabel.resize(eSize(self.W+750,60))
		self.testSizeLabel.setVAlign(eLabel.alignTop)
		self.testSizeLabel.setHAlign(eLabel.alignLeft)
		self.testSizeLabel.setNoWrap(1)
		return Renderer.applySkin(self, desktop, parent)

	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))
		
	def changed(self, what):
		if self.instance:
			if what[0] != self.CHANGED_CLEAR:
				self.re_changed()

	def getTunerName(self, i):
		all = ""
		if self.isInput:
			all = getTunerDesc(i)
		else:
			try:
				all = (nimmanager.getNimDescription(i).split(":")[0]).strip()
				if all[-1].isdigit():
					all = all[-2:]
				else:
					all = all[-1]
			except: pass
		if all != "":
			return all, False
		all = "ABCDEFGHIJKLMNOPQRS"
		if "B2" in self.all and i > 3:
			i -= 2 
		elif "A2" in self.all and i > 1: 
			i -= 1
		return all[i], True
		
	def chckRT(self):
		self.__updTimer.stop()
		if self.__noFirst:
			recT = []
			try:
				from NavigationInstance import instance
				if instance is not None:
					for x in instance.RecordTimer.timer_list:
						if x.isRunning() and not x.justplay	and (x.state == x.StateRunning or x.state == x.StatePrepared):
							tmp = x.record_service
							if isinstance(tmp, (iPlayableService, iRecordableService, iPlayableServicePtr, iRecordableServicePtr)):
								feinfo = tmp and tmp.frontendInfo()
								data = feinfo and feinfo.getFrontendData()
								if isinstance(data, dict):
									num = None
									if self.isInput:
										num = data.get("input_number", -1)
									if num is None or num < 0:
										num = data.get("slot_number", -1)
										if num is None or num < 0:
											num = data.get("tuner_number", -1)
									if num is not None and num > -1:
										recT.append(num)
			except: pass
			if recT != self.recT:
				self.recT = []
				if len(recT) != 0: 
					for x in range(0, len(recT)):
						self.recT.append(recT[x])
				self.re_changed()
			del recT
		else:
			self.__noFirst = True
			try:
				if self.instance and self.noClear:
					self.instance.clear(self.bcolor)
			except: pass
		self.__updTimer.startLongTimer(20)
			
	def re_changed(self, mask=None):
		if mask:
			self.mask = mask
		enaM = False
		try:
			if self.instance:
				enaM = True
				self.instance.clear(self.bcolor)
				self.noClear = False
		except: pass
		sx = True
		try:
			sx = config.plugins.setupGlass17.par104.value != "99"
		except: pass
		if enaM and sx:
			self.instance.clear(self.bcolor)
			Acolor = self.Acolor
			BAcolor = self.BAcolor
			fcolor = self.fcolor
			Mcolor = self.Mcolor
			RECcolor = self.RECcolor
			RECLcolor = self.RECLcolor
			tuners = self.tuners
			auto = False
			no_h = True
			try:
				if config.plugins.setupGlass17.par105.value != "AutoColors":
					Acolor = parseColor(config.plugins.setupGlass17.par105.value)
				if config.plugins.setupGlass17.par106.value != "AutoColors":
					BAcolor = parseColor(config.plugins.setupGlass17.par106.value)
				if config.plugins.setupGlass17.par107.value != "AutoColors":
					fcolor = parseColor(config.plugins.setupGlass17.par107.value)
				if config.plugins.setupGlass17.par108.value != "AutoColors":
					Mcolor = parseColor(config.plugins.setupGlass17.par108.value)
				if config.plugins.setupGlass17.par112.value != "AutoColors":
					RECcolor = parseColor(config.plugins.setupGlass17.par112.value)
				if config.plugins.setupGlass17.par113.value != "AutoColors":
					RECLcolor = parseColor(config.plugins.setupGlass17.par113.value)
				tuners = int(config.plugins.setupGlass17.par104.value)
				if tuners == 0:
					tuners = 20
					auto = True
				if config.plugins.setupGlass17.par139.value:
					no_h = False
			except: pass  
			dd = 1
			xx = 0
			dt = [] 
			self.all = []
			if self.hfont != self.Hfont:
				self.hfont = self.Hfont
				self.used_font = gFont(self.Nfont, self.hfont)
				self.testSizeLabel.setFont(self.used_font)
			self.isInput = False
			slot = -1
			if os.path.exists('/etc/dpkg'):
				try:
					slot = self.source.input_number
					self.isInput = True
				except: pass
			try:
				if slot == -1:
					slot = self.source.slot_number
				for x in range(0, tuners):					
					tuner = self.mask & dd and True or False
					dd *= 2
					self.name, isMissing = self.getTunerName(x)
					if slot == x:
						if len(self.recT) != 0 and x in self.recT:
							c = RECLcolor
						else:
							c = Acolor
					elif isMissing:
						if auto:
							break
						c = Mcolor
					elif tuner:
						if len(self.recT) != 0 and x in self.recT:
							c = RECcolor
						else:
							c = BAcolor
					else:
						c = fcolor
					self.all.append(self.name)
					if no_h or (not no_h and not c in(fcolor,Mcolor)):
						w, h = self.calcWidth(self.name)
						dt.append([xx, w+7, h+4, c, self.name])
						xx += w + self.sepW
				if xx + w > self.W:
					self.hfont = int(self.hfont*self.W/(xx + w))
					while (xx + w > self.W) and self.hfont > 10:
						xx = 0
						self.used_font = gFont(self.Nfont, self.hfont)
						self.testSizeLabel.setFont(self.used_font)
						for x in range(0,len(self.all)):
							w, h = self.calcWidth(self.all[x])
							dt[x][0] = xx 
							dt[x][1] = w+7
							dt[x][2] = h+4							
							xx += w + self.sepW
						self.hfont -= 2
			except: pass                                  
			w = 0
			xx -= self.sepW
			if xx > 0:
				if self.posLR == "R":
					w = int(self.W - xx)
					if w < 0:
						w = 0					
				elif self.posLR == "C":	
					w = int((self.W - xx)/2)
			try:
				for x in range(0, len(dt)):					
					h = self.instance.writeText(eRect(w+dt[x][0], 0, dt[x][1], dt[x][2]), dt[x][3], self.bcolor, self.used_font, dt[x][4], RT_HALIGN_LEFT) 
			except: pass
			del dt
                   			
	def calcWidth(self, name):
		self.testSizeLabel.setText(name)
		name = self.testSizeLabel.calculateSize()
		return name.width(), name.height() 

	def preWidgetRemove(self, instance):
		self.testSizeLabel = None

	def postWidgetCreate(self, instance):
		for (attrib, value) in self.skinAttributes:
			if attrib == "size":
				x, y = value.split(',')
				self.W, self.H = int(x), int(y)
		self.instance.setSize(eSize(self.W,self.H))
		self.testSizeLabel = eLabel(instance)
		self.testSizeLabel.hide()
			
def getTunerDesc(n):
	ret = ""
	n = int(n)
	idx = -1
	slotid = 0
	try:
		slots = len(nimmanager.nim_slots)
		while slotid < slots:
			slot = nimmanager.nim_slots[slotid]
			if slot.inputs is None or slot.channel < len(slot.inputs):
				idx += 1
			if idx >= n:
				break
			slotid += 1
		if slotid < nimmanager.getSlotCount():
			ret = nimmanager.getNimSlotInputName(slotid)		
	except: pass
	return ret
		