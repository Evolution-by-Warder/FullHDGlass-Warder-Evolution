from Screens.Screen import Screen
from Components.Label import Label
from Components.ProgressBar import ProgressBar
try:
	from Components.Sensors import sensors
except: pass
from Components.Harddisk import harddiskmanager
import os
from Components.ServiceEventTracker import ServiceEventTracker
from Tools.Directories import fileExists
from os import system
from enigma import eTimer, iServiceInformation, iPlayableService, iPlayableServicePtr, eServiceReference, eEPGCache
from Components.config import config
from GlobalActions import globalActionMap
from keymapparser import readKeymap
from Components.Pixmap import *
import re
from Plugins.Extensions.setupGlass17.weaUtils import readECMlabels, setSideECM, ISP38
if ISP38:
	from Plugins.Extensions.setupGlass17.py38 import DG
else:
	DG = unichr(176).encode("latin-1")
	
class UserInfo17(Screen):

	skin_sysInfo = """<screen name="User screen" position="610,147" size="1226,433" zPosition="2" title="System Info" backgroundColor="background" >
                                           
                      <widget name="mem_labels" font="Prive4;23" position="15,15" zPosition="0" size="150,150" valign="top" halign="left" backgroundColor="background" foregroundColor="#666666" transparent="1" />
                      <widget name="ram" font="Prive4;23" position="184,15" zPosition="3" size="135,150" valign="top" halign="left" backgroundColor="background" transparent="1" />
                      <widget name="swap" font="Prive4;23" position="336,15" zPosition="4" size="135,150" valign="top" halign="left" backgroundColor="background" transparent="1" />      
                      <widget name="mem_tot" font="Prive4;23" position="478,15" zPosition="5" size="135,150" valign="top" halign="left" backgroundColor="background" transparent="1" />
                      <widget name="root" font="Prive4;23" position="621,15" zPosition="3" size="135,150" valign="top" halign="left" backgroundColor="background" transparent="1" />

                      <widget name="hdd" font="Prive4;23" position="763,15" zPosition="3" size="135,150" valign="top" halign="left" backgroundColor="background" transparent="1" />
                      <widget name="usb" font="Prive4;23" position="915,15" zPosition="4" size="135,150" valign="top" halign="left" backgroundColor="background" transparent="1" />      
                      <widget name="sd" font="Prive4;23" position="1067,15" zPosition="4" size="135,150" valign="top" halign="left" backgroundColor="background" transparent="1" />      

                      <widget name="mem_bar" position="162,45" size="7,112" pixmap="hd_glass17/user_info/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="background" transparent="1" />
                      <widget name="swap_bar" position="313,45" size="7,112" pixmap="hd_glass17/user_info/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="background" transparent="1" />
                      <widget name="memtotal_bar" position="453,45" size="7,112" pixmap="hd_glass17/user_info/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="background" transparent="1" />
                      <widget name="root_bar" position="595,45" size="7,112" pixmap="hd_glass17/user_info/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="background" transparent="1" />

                      <widget name="hdd_bar" position="738,45" size="7,112" pixmap="hd_glass17/user_info/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="background" transparent="1" />
                      <widget name="usb_bar" position="889,45" size="7,112" pixmap="hd_glass17/user_info/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="background" transparent="1" />
                      <widget name="sd_bar" position="1040,45" size="7,112" pixmap="hd_glass17/user_info/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="background" transparent="1" />

                      <ePixmap pixmap="hd_glass17/user_info/bar_back.png" position="162,45" size="7,112" zPosition="1" alphatest="on"/>
                      <ePixmap pixmap="hd_glass17/user_info/bar_back.png" position="313,45" size="7,112" zPosition="1" alphatest="on"/>
                      <ePixmap pixmap="hd_glass17/user_info/bar_back.png" position="453,45" size="7,112" zPosition="1" alphatest="on"/>
                      <ePixmap pixmap="hd_glass17/user_info/bar_back.png" position="595,45" size="7,112" zPosition="1" alphatest="on"/>
                      <ePixmap pixmap="hd_glass17/user_info/bar_back.png" position="738,45" size="7,112" zPosition="1" alphatest="on"/>
                      <ePixmap pixmap="hd_glass17/user_info/bar_back.png" position="889,45" size="7,112" zPosition="1" alphatest="on"/>
                      <ePixmap pixmap="hd_glass17/user_info/bar_back.png" position="1040,45" size="7,112" zPosition="1" alphatest="on"/>
                      <ePixmap pixmap="hd_glass17/user_info/mem.png" position="184,180" size="60,120" zPosition="2" alphatest="off"/>
                      <ePixmap pixmap="hd_glass17/user_info/swap.png" position="336,180" size="60,120" zPosition="2" alphatest="off"/>                      
                      <ePixmap pixmap="hd_glass17/user_info/summ.png" position="488,180" size="60,120" zPosition="2" alphatest="off"/>
                      <ePixmap pixmap="hd_glass17/user_info/root.png" position="630,180" size="60,120" zPosition="2" alphatest="off"/>
                      <ePixmap pixmap="hd_glass17/user_info/hdd.png" position="772,180" size="60,120" zPosition="2" alphatest="off"/>
                      <ePixmap pixmap="hd_glass17/user_info/usb.png" position="924,180" size="60,120" zPosition="2" alphatest="off"/>
                      <ePixmap pixmap="hd_glass17/user_info/sd.png" position="1076,180" size="60,120" zPosition="2" alphatest="off"/>
                      <ePixmap pixmap="hd_glass17/menu/box.png" position="46,168" size="445,273" zPosition="2" alphatest="blend"/>

                      <widget name="HDDTemperature" position="588,277" zPosition="3" size="165,60" font="Prive4;23" halign="center" valign="top" backgroundColor="background" transparent="1" />
                      <widget name="cpu_value" font="Prive4;23" position="816,277" zPosition="3" size="165,60" valign="top" halign="center" backgroundColor="background" transparent="1" />      
                      <widget name="temperature_value" font="Prive4;23" position="1029,277" zPosition="3" size="165,60" valign="top" halign="center" backgroundColor="background" transparent="1" />      
                      <ePixmap pixmap="hd_glass17/user_info/hdd_temp.png" position="621,337" size="60,120" zPosition="2" alphatest="off"/>
                      <ePixmap pixmap="hd_glass17/user_info/cpu.png" position="847,337" size="60,120" zPosition="2" alphatest="off"/>
                      <ePixmap pixmap="hd_glass17/user_info/sensor.png" position="1076,337" size="60,120" zPosition="2" alphatest="off"/>
                      <widget name="hddtempbar" position="586,337" size="8,66" pixmap="hd_glass17/user_info/barm.png" orientation="orBottomToTop" zPosition="2" backgroundColor="background" transparent="1" />
                      <widget name="cpu_bar" position="813,337" size="8,66" pixmap="hd_glass17/user_info/barm.png" orientation="orBottomToTop" zPosition="2" backgroundColor="background" transparent="1" />
                      <widget name="temperature_bar" position="1040,337" size="8,66" pixmap="hd_glass17/user_info/barm.png" orientation="orBottomToTop" zPosition="2" backgroundColor="background" transparent="1" />
                      <ePixmap pixmap="hd_glass17/user_info/barm_back.png" position="586,337" size="8,66" zPosition="1" alphatest="on"/>
                      <ePixmap pixmap="hd_glass17/user_info/barm_back.png" position="813,337" size="8,66" zPosition="1" alphatest="on"/>
                      <ePixmap pixmap="hd_glass17/user_info/barm_back.png" position="1040,337" size="8,66" zPosition="1" alphatest="on"/>

                        </screen>"""

	skin_event = """<screen name="User screen" position="753,105" size="1074,502" zPosition="2" title="Extended description" backgroundColor="background" >	
               <widget name="description" font="Prive4;30" position="15,0" zPosition="0" size="1044,487" valign="top" halign="left" backgroundColor="background" transparent="1" />      
              </screen>"""                        

	skin_event2 = """<screen name="User screen" position="0,0" size="1920,1080" zPosition="9" title="Extended description" backgroundColor="black" >	
		<widget source="Title" render="Label" position="60,100" size="1800,50" foregroundColor="un6cbcf0" backgroundColor="black" zPosition="1" valign="center" halign="center" font="Prive4;35" transparent="1"/>
               <widget name="description" font="Prive4;32" position="60,160" size="1800,820" valign="top" halign="left" backgroundColor="black" transparent="1" />      
              </screen>"""

	side_infobar = """<screen name="User screen" position="0,0" size="540,667" zPosition="1" backgroundColor="#ffffffff" flags="wfNoBorder" >	

		<widget name="ecmlabels" font="Prive3;24" position="108,172" zPosition="2" size="150,328" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,172" zPosition="3" size="318,328" backgroundColor="background" transparent="1" />
    <widget name="piconEcm" position="120,522"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,522"  size="150,90"  zPosition="2" alphatest="on"/>
    <ePixmap position="60,7"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0"/>
    <widget name="picProv" position="120,61"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="picSat" position="318,61"  size="150,90"  zPosition="2" alphatest="on"/>
              </screen>""" 

	skin_event_infobar = """<screen name="User screen" position="0,0" size="1920,667" zPosition="1"  backgroundColor="#ffffffff" flags="wfNoBorder" >	

		<widget name="ecmlabels" font="Prive3;24" position="108,172" zPosition="2" size="150,328" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,172" zPosition="3" size="318,328" backgroundColor="background" transparent="1" />
    <widget name="piconEcm" position="120,522"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,522"  size="150,90"  zPosition="2" alphatest="on"/>
    <ePixmap position="60,7"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0"/>
    <widget name="picProv" position="120,61"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="picSat" position="318,61"  size="150,90"  zPosition="2" alphatest="on"/>

    <ePixmap position="730,42" size="1119,622" pixmap="hd_glass17/menu/back_event.png" alphatest="off" zPosition="0"/>
		<widget source="Title" render="Label" position="775,76" size="1026,60" foregroundColor="un6cbcf0" zPosition="1" backgroundColor="background" valign="center" halign="left" font="Prive3;31" transparent="1"/>
    <widget name="description" font="Prive4;30" position="775,144" zPosition="1" size="1036,480" valign="top" halign="block" backgroundColor="background" transparent="1" />      

    </screen>"""                        

	skin_eventActualNext_side = """<screen name="User screen" position="0,0" size="1920,667" zPosition="1"  backgroundColor="#ffffffff" flags="wfNoBorder" >	

		<widget name="ecmlabels" font="Prive3;24" position="108,172" zPosition="2" size="150,328" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,172" zPosition="3" size="318,328" backgroundColor="background" transparent="1" />
    <widget name="piconEcm" position="120,522"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,522"  size="150,90"  zPosition="2" alphatest="on"/>
    <ePixmap position="60,7"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0"/>
    <widget name="picProv" position="120,61"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="picSat" position="318,61"  size="150,90"  zPosition="2" alphatest="on"/>

    <ePixmap position="730,42" size="1119,622" pixmap="hd_glass17/menu/back_event.png" alphatest="off" zPosition="0"/>
    <widget name="titleNow" font="Prive4;28" position="775,142" zPosition="1" size="1036,31" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />      
    <widget name="description" font="Prive4;28" position="775,187" zPosition="1" size="1036,177" valign="top" halign="block" backgroundColor="background" transparent="1" /> 
                    
    <widget name="titleNext" font="Prive4;28" position="775,382" zPosition="2" size="1036,31" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />      
    <widget name="description2" font="Prive4;28" position="775,427" zPosition="3" size="1036,177" valign="top" halign="block" backgroundColor="background" transparent="1" />      

    </screen>"""
                            	
	def __init__(self, session):
		Screen.__init__(self, session)
		if config.plugins.setupGlass17.par31.value == "s":
			self.skin = UserInfo17.skin_sysInfo
			self['cpu_value'] = Label("CPU using:\nN/A")
			self['temperature_value'] = Label("Temp. DB:\nN/A")
			self["mem_labels"] = Label("\nTotal:\nFree:\nUsed:\nUsed(%):")        
			self["sd"] = Label("")
			self["usb"] = Label("")
			self["hdd"] = Label("")
			self["ram"] = Label("")
			self["root"] = Label("")
			self["swap"] = Label("")
			self["mem_tot"] = Label("")
			self["HDDTemperature"] = Label("")
			self['hddtempbar'] = ProgressBar()
			self['mem_bar'] = ProgressBar()
			self['root_bar'] = ProgressBar()
			self['swap_bar'] = ProgressBar()
			self['cpu_bar'] = ProgressBar()
			self['memtotal_bar'] = ProgressBar()
			self['temperature_bar'] = ProgressBar()
			self['sd_bar'] = ProgressBar()
			self['usb_bar'] = ProgressBar()
			self['hdd_bar'] = ProgressBar()
			self.onShow.append(self.generateInfo)
			self.onHide.append(self.stopTimer)
			self.cpuTimer = eTimer()
			try:
				self.cpuTimer_conn = self.cpuTimer.timeout.connect(self.getCPUInfo)
			except AttributeError:
				self.cpuTimer.timeout.get().append(self.getCPUInfo)
			self.cpu_count = 0
			self.prev_info = self.getCpuInfo(-3)
			self.curr_info = self.getCpuInfo()
		elif config.plugins.setupGlass17.par31.value == "en":
			self.skin_event_nowNext = """<screen name="User screen" position="75,105" size="1770,513" zPosition="2" title="Event now and next" backgroundColor="background" >"""		
			self.skin_event_nowNext += '<widget name="titleNow" font="Prive4;31" position="15,0" zPosition="0" size="1740,40" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />\n'      
			self.skin_event_nowNext += '<widget name="description" font="Prive4;31" position="15,42" zPosition="1" size="1740,199" valign="top" halign="block" backgroundColor="background" transparent="1" />\n'                     
			self.skin_event_nowNext += '<widget name="titleNext" font="Prive4;31" position="15,256" zPosition="2" size="1740,40" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />\n'      
			self.skin_event_nowNext += '<widget name="description2" font="Prive4;31" position="15,298" zPosition="3" size="1740,199" valign="top" halign="block" backgroundColor="background" transparent="1" />\n'      
			self.skin_event_nowNext += """</screen>""" 
			self.skin = self.skin_event_nowNext
			self.session = session
			self.suspend = True
			self.epgQuery = eEPGCache.getInstance().lookupEventTime
			self.onShow.append(self.__wakeupNowNext)
			self.onHide.append(self.__standby)
			self["description"] = Label("")
			self["description2"] = Label("")
			self["titleNow"] = Label("")
			self["titleNext"] = Label("")
			self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evUpdatedEventInfo: self.__actualNextEventDesc,})
		elif config.plugins.setupGlass17.par31.value == "e" or config.plugins.setupGlass17.par31.value == "e2":
			if config.plugins.setupGlass17.par31.value == "e":
				self.skin = UserInfo17.skin_event
			else:
				self.skin = UserInfo17.skin_event2
			self.session = session
			self.suspend = True
			self.epgQuery = eEPGCache.getInstance().lookupEventTime
			self.onShow.append(self.__wakeup)
			self.onHide.append(self.__standby)
			self.eventShowed = 0
			if config.plugins.setupGlass17.par33.value:
				readKeymap("/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/keymap3.xml")
				globalActionMap.actions['eventNextPrev'] = self.changeEvent
			self["description"] = Label("")
			self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evUpdatedEventInfo: self.__actualEventDesc,})
		elif config.plugins.setupGlass17.par31.value == "si":
			self.skin = setSideECM(UserInfo17.side_infobar)
			self.ECM_LABELS, self.CLRDATA = readECMlabels(False)
			self.session = session
			self.suspend = True
			self.fta = False
			self.prov = ""
			self.sat = ""
			self["picSat"] = Pixmap()
			self["picProv"] = Pixmap()
			self["piconCam"] = Pixmap()
			self["piconEcm"] = Pixmap()
			self['ecmValues'] = Label(self.CLRDATA)
			self['ecmlabels'] = Label(self.ECM_LABELS) 
			self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evUpdatedInfo: self.__evUpdatedInfo, iPlayableService.evTunedIn: self.__evUpdatedInfo})
			self.ecmTimer = eTimer()
			try:
				self.ecmTimer_conn = self.ecmTimer.timeout.connect(self.__updECM)
			except AttributeError:
				self.ecmTimer.timeout.get().append(self.__updECM)    
			self.onLayoutFinish.append(self.setscale)
			self.onShow.append(self.startEcmInfo)
			self.onHide.append(self.stopEcmInfo)
		elif config.plugins.setupGlass17.par31.value == "esi":
			self.skin = setSideECM(UserInfo17.skin_event_infobar)
			self.ECM_LABELS, self.CLRDATA = readECMlabels(False)
			self.session = session    
			self.suspend = True
			self.fta = False
			self.prov = ""
			self.sat = ""
			self["picSat"] = Pixmap()
			self["picProv"] = Pixmap()
			self["piconCam"] = Pixmap()
			self["piconEcm"] = Pixmap()
			self['ecmValues'] = Label(self.CLRDATA)
			self['ecmlabels'] = Label(self.ECM_LABELS) 
			self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evUpdatedInfo: self.__evUpdatedInfo, iPlayableService.evTunedIn: self.__evUpdatedInfo, iPlayableService.evUpdatedEventInfo: self.__actualEventDesc,})
			self.ecmTimer = eTimer()
			try:
				self.ecmTimer_conn = self.ecmTimer.timeout.connect(self.__updECM)
			except AttributeError:
				self.ecmTimer.timeout.get().append(self.__updECM)    
			self.onShow.append(self.startEcmInfo)
			self.onHide.append(self.stopEcmInfo)
			self.epgQuery = eEPGCache.getInstance().lookupEventTime
			self.onShow.append(self.__wakeup)
			self.onHide.append(self.__standby)
			self.eventShowed = 0
			if config.plugins.setupGlass17.par33.value:
				readKeymap("/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/keymap3.xml")
				globalActionMap.actions['eventNextPrev'] = self.changeEvent
			self["description"] = Label("")
			self.onLayoutFinish.append(self.setscale)
		else:
			self.skin = setSideECM(UserInfo17.skin_eventActualNext_side)
			self.ECM_LABELS, self.CLRDATA = readECMlabels(False)
			self.session = session    
			self.suspend = True
			self.fta = False
			self.prov = ""
			self.sat = ""
			self["picSat"] = Pixmap()
			self["picProv"] = Pixmap()
			self["piconCam"] = Pixmap()
			self["piconEcm"] = Pixmap()             
			self['ecmValues'] = Label(self.CLRDATA)
			self['ecmlabels'] = Label(self.ECM_LABELS) 
			self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evUpdatedInfo: self.__evUpdatedInfo, iPlayableService.evTunedIn: self.__evUpdatedInfo, iPlayableService.evUpdatedEventInfo: self.__actualNextEventDesc,})
			self.ecmTimer = eTimer()
			try:
				self.ecmTimer_conn = self.ecmTimer.timeout.connect(self.__updECM)
			except AttributeError:
				self.ecmTimer.timeout.get().append(self.__updECM)    
			self.onShow.append(self.startEcmInfo)
			self.onHide.append(self.stopEcmInfo)
			self.epgQuery = eEPGCache.getInstance().lookupEventTime
			self.onShow.append(self.__wakeupNowNext)
			self.onHide.append(self.__standby)
			self["description"] = Label("")
			self["description2"] = Label("")
			self["titleNow"] = Label("")
			self["titleNext"] = Label("")
			self.onLayoutFinish.append(self.setscale)
      
	def setscale(self):
			for x in ("picSat","picProv","piconCam","piconEcm"):
				try:
					self[x].instance.setScale(1)
				except: pass  
                              		
	def __evUpdatedInfo(self):
		service = self.session.nav.getCurrentService()
		info = (service and service.info())
		if info:
			serviceinfo = service.info()
			if not serviceinfo.getInfo(iServiceInformation.sIsCrypted):
				self.fta = True
				x = config.plugins.setupGlass17.par39.value+"/piconCam/Fta-fs8.png"
				if not fileExists(x):
					x = "/usr/share/enigma2/hd_glass17/icons/missing-fs8.png"
				self["piconEcm"].instance.setPixmapFromFile(x)
				self["piconCam"].instance.setPixmapFromFile(x)
			else:
				self.fta = False	
				
	def __updECM(self):
		if not self.suspend:
			if self.sat != config.plugins.setupGlass17.par37.value:
				self["picSat"].instance.setPixmapFromFile(config.plugins.setupGlass17.par37.value)
				self.sat = config.plugins.setupGlass17.par37.value
			if self.prov != config.plugins.setupGlass17.par36.value:
				self["picProv"].instance.setPixmapFromFile(config.plugins.setupGlass17.par36.value)
				self.prov = config.plugins.setupGlass17.par36.value
			coding = config.plugins.setupGlass17.par38.value
			if config.plugins.setupGlass17.par195.value == "Prov.:":
				self['ecmlabels'].setText(self.ECM_LABELS.replace("Prov.:","CHID:"))
			elif config.plugins.setupGlass17.par195.value == "PrvID:":
				self['ecmlabels'].setText(self.ECM_LABELS.replace("PrvID:","CHID:"))
			else:
				self['ecmlabels'].setText(self.ECM_LABELS)
			self['ecmValues'].setText(coding)
			if not self.fta:
				coding = coding.replace("\n","*")
				code = coding.strip().split('*')
				if len(coding) > 10:
					code = coding.strip().split('*')[11]
					if str(code) == "..............":
						code = "Unknown"
					self["piconEcm"].instance.setPixmapFromFile((config.plugins.setupGlass17.par39.value+"/piconCam/" + code + "-fs8.png"))				
					cam = coding.strip().split('*')[0]
					if str(cam) == "..............":
						cam = "Unknown"							
					elif "Ncam" in cam:
						cam = "Ncam"
					elif "Gcam" in cam:
						cam = "Ncam"
					elif "DOScam" in cam:
						cam = "DOScam"
					elif "OScam" in cam:
						cam = "OScam"
					code = config.plugins.setupGlass17.par39.value+"/piconCam/" + cam + "-fs8.png"
					if not os.path.isfile(code):
						code = "/usr/share/enigma2/hd_glass17/icons/missing-fs8.png"
					self["piconCam"].instance.setPixmapFromFile(code)				
				self.ecmTimer.start(int(config.plugins.setupGlass17.par74.value)*1000)

	def startEcmInfo(self):
		self.suspend = False	
		self.ecmTimer.start(300)	
		
	def stopEcmInfo(self):
		self.suspend = True	
		self.ecmTimer.stop()      	
    		
	def setWindowTitle(self, titleName):
		self.setTitle(titleName)

	def __wakeup(self):
		self.suspend = False
		self.__actualEventDesc()

	def __wakeupNowNext(self):
		self.suspend = False
		self.__actualNextEventDesc()

	def __standby(self):
		self.suspend = True	
	
	def changeEvent(self):
		if not self.suspend:
			if self.eventShowed == 0:
				self.eventShowed = 1
			else:
				self.eventShowed = 0
			event, desc = self.readEventDesc(self.eventShowed)
			self.setWindowTitle(event)
			self["description"].setText(desc)

	def __actualNextEventDesc(self):
		if not self.suspend:
			event, desc = self.readEventDesc(0)
			self["titleNow"].setText(event)
			self["description"].setText(desc)
			event, desc = self.readEventDesc(1)
			self["titleNext"].setText(event)
			self["description2"].setText(desc)

	def __actualEventDesc(self):
		if not self.suspend:
			self.eventShowed = 0
			event, desc = self.readEventDesc(0)
			self.setWindowTitle(event)
			self["description"].setText(desc)

	def readEventDesc(self, what):
		service = self.session.nav.getCurrentService()
		no_desc = "EPG data unavailable"
		info = service and service.info()
		if info is None:
			return no_desc, no_desc
		act_event = info and info.getEvent(what)
		if not act_event and info:
			refstr = info.getInfoString(iServiceInformation.sServiceref)
			act_event = self.epgQuery(eServiceReference(refstr), -1, what)
		if act_event is None:
			return no_desc, no_desc 
		else:
			short = act_event.getShortDescription()
			tmp = act_event.getExtendedDescription()
			if tmp == "" or tmp is None:
				tmp = short		
				if tmp == "" or tmp is None:
					tmp = no_desc
				else:
					tmp = tmp.strip()
			else:
				tmp = tmp.strip()
				if short != "" or short is not None:
					if len(short) > 3:
						if not short[:-2] in tmp:
							tmp = short.strip() + "..." + tmp
			title = act_event.getEventName()
			try:
				title = "%s (%d min) %s" % ((act_event.getBeginTimeString().strip().split(",")[1]), act_event.getDuration()/60, title)
			except: pass
			if len(title) > 58:
				title = title[:57] + "..."
			tmp = tmp.replace("\r", " ").replace("\n", " ").replace("\xc2\x8a", " ")
			return title, re.sub(r'[\s\t]+', ' ', tmp)
		
	def generateInfo(self):
		self.getCPUInfo()
		self.getTempSensorsInfo()
		self.getMemInfo()
		self.getSpaceInfo()    		
		self.getHddInfo() 
			
	def getHddInfo(self):
		t = "Temp. %s:\nN/A" % config.plugins.setupGlass17.par182.value
		tmp = self.getTemp(config.plugins.setupGlass17.par140.value)
		if tmp != 0:
			t = t.replace("N/A",str(tmp) + DG + "C")
		self['hddtempbar'].setRange((0, 60))
		self['hddtempbar'].setValue(tmp)
		self["HDDTemperature"].setText(t)

	def getTemp(self, dev):
		tmp1 = 0                                                 
		if dev != "None":
			tt = '/tmp/b.tmp'
			what = ['smartctl -a %s | grep Temperature > %s','/usr/bin/hdd_temp_hdg17 -q -n %s > %s','hddtemp -n -q %s > %s']
			if config.plugins.setupGlass17.par21.value:
				what.append('/usr/bin/hdd_temp_hdg17 -q -n -w %s > %s')
				what.append('hddtemp -q -n -w %s > %s')
			for x in what:
				try:
					tta = x % (dev, tt)
					system(tta)
					f = open(tt, 'r')
					temp = f.readlines()
					if "smartctl" in tta:
						tmp1 = int((temp[0].strip().split("-")[1]).replace("\n","").replace("\t","").replace(" ",""))
					else:
						tmp1 = int(temp[0].strip().split(" ")[0])
					f.close()
				except: pass
				system('rm -rf '+tt)
				if tmp1 != 0:
					break
		return tmp1	

	def getCPUInfo(self):
		self.cpuTimer.stop()
		tmp =  'CPU using:\nN/A'
		zataz = 0
		self.prev_info, self.curr_info = self.curr_info, self.getCpuInfo()
		for i in range(len(self.curr_info)):
			try:
				zataz = int(100 * ( self.curr_info[i][2] - self.prev_info[i][2] ) / ( self.curr_info[i][1] - self.prev_info[i][1] ))
				tmp = "CPU using:\n" + str(zataz) + " %"
			except ZeroDivisionError:
				tmp =  'CPU using:\nN/A'
		self['cpu_bar'].setValue(zataz)
		self['cpu_value'].setText(tmp)
		self.cpuTimer.start(3000)

	def stopTimer(self):
		self.cpuTimer.stop()

	def getCpuInfo(self, cpu=-1):
		def validCpu(c):
			if cpu == -3 and c.isdigit():
				return True
			elif c == " " and cpu == -1:
				return True
			elif c == str(cpu):
				return True
			return False		
		res = []
		calc_cpus = cpu == -3 and self.cpu_count == 0
		try:
			fd = open("/proc/stat", "r")
			for l in fd:
				if l[0] != "c": continue
				if l.find("cpu") == 0 and validCpu(l[3]):
					if calc_cpus:
						self.cpu_count += 1
						continue
					total = busy = 0
					tmp = l.split()
					for i in range(1, len(tmp)):
						tmp[i] = int(tmp[i])
						total += tmp[i]
					busy = total - tmp[4] - tmp[5]
					res.append([tmp[0], total, busy])
			fd.close()
		except:
			pass
		return res
		
	def getTempSensorsInfo(self):
		temperature = "Temp. DB:\nN/A"
		self['temperature_bar'].setRange((0, 100))
		temp = 0
		try:
			allsensors = sensors.getSensorsList(sensors.TYPE_TEMPERATURE)
			numtemp = len(allsensors)
			for num in range(numtemp):
				idx = allsensors[num]
				isMax = sensors.getSensorValue(idx)
				if isMax > temp:
					temp = isMax
		except:
			pass
		if temp > 0 :
			temperature = "Temp. DB:\n" + str(temp) + DG + "C"
		elif fileExists('/sys/devices/virtual/thermal/thermal_zone0/temp'):
			try:
				idx = open('/sys/devices/virtual/thermal/thermal_zone0/temp').read()[:2]
				temp = idx.replace('\n', '')
				temperature = "CPU Temp.:\n" + temp + DG + "C"
			except: pass
		self['temperature_bar'].setValue(int(temp))
		self['temperature_value'].setText(temperature)

	def getMemInfo(self):
		def parse(i):
			return int((i.strip().split(":")[1]).strip().split(" ")[0])
		def setUnits(value):
			if value >= 1024*1024:
				return '%.1f%s' % (float(value)/(1024*1024),'GB')
			elif value >= 1024:
				return '%.1f%s' % (float(value)/1024,'MB')
			else:
				return '%.1f%s' % (float(value),'kB')
		ramperc = swapperc = ramtot = swaptot = ramfree = swapfree = ramused = swapused = totalperc = 0
		try:
			tmp = open('/proc/meminfo').readlines()
			ramfree = parse(tmp[1])
			ramtot = parse(tmp[0]) 
			ramused = ramtot - ramfree
			for x in tmp:
				if "SwapTotal" in x:
					swaptot = parse(x)
				elif "SwapFree" in x:
					swapfree = parse(x)
			swapused = swaptot - swapfree
			if ramtot != 0:
				ramperc = int((ramused * 100) / ramtot)
			if swaptot != 0:
				swapperc = int((swapused * 100) / swaptot)
			if swaptot != 0 or ramtot != 0:
				totalperc = int(((ramused+swapused)*100)/(ramtot+swaptot))
		except: pass
		self["ram"].setText(("RAM:\n" + setUnits(ramtot) + "\n" + setUnits(ramfree) + "\n" + setUnits(ramused) + "\n" + str(ramperc) + "%"))
		self["swap"].setText(("Swap:\n" + setUnits(swaptot) + "\n" + setUnits(swapfree) + "\n" + setUnits(swapused) + "\n" + str(swapperc) + "%"))
		self["mem_tot"].setText(("Total:\n" + setUnits(ramtot+swaptot) + "\n" + setUnits(ramfree+swapfree) + "\n" + setUnits(ramused+swapused) + "\n" + str(totalperc) + "%"))
		self['memtotal_bar'].setValue(int(totalperc))
		self['swap_bar'].setValue(int(swapperc))
		self['mem_bar'].setValue(int(ramperc))
		
	def getSpaceInfo(self):
		os.system('df -h > /tmp/tempinfo.tmp')
		usbperc = hddperc = rootperc = sdperc = 0                                                            
		usbsumm = "USB:\n.... \n.... \n.... \n...."
		sdsumm = "SD/CF:\n.... \n.... \n.... \n...."
		hddsumm = config.plugins.setupGlass17.par182.value+":\n.... \n.... \n.... \n...."
		if fileExists('/tmp/tempinfo.tmp'):
			f = open('/tmp/tempinfo.tmp', 'r')
			for line in f.readlines():
				line = line.replace('part1', ' ')
				parts = line.strip().split()
				totsp = len(parts) - 1
				if parts[0] == '/dev/root' or parts[totsp] == "/":
					rootperc = parts[4]
					self["root"].setText("Root:\n" + str(parts[1]) + "B\n" + str(parts[3]) + "B\n" + str(parts[2]) + "B\n" + str(rootperc))
					rootperc = rootperc.replace('%','') 
					self['root_bar'].setValue(int(rootperc))		
				if parts[totsp] == '/media/sd' or parts[totsp] == '/media/mmc' or parts[totsp] == '/media/cf' or (parts[totsp] == '/media/ba' and parts[0] == '/dev/mmcblk1p1'):
					sdperc = int(parts[totsp-1].replace('%', ''))
					sdsumm = "SD/CF:\n" + parts[totsp-4] + "B\n" +  parts[totsp-2] + "B\n" + parts[totsp-3] + "B\n" + parts[totsp-1]
				if parts[totsp] == '/media/usb' or (parts[totsp] == '/media/ba' and parts[0] == '/dev/sdb1'):
					usbperc = int(parts[totsp-1].replace('%', ''))
					usbsumm = "USB:\n" + parts[totsp-4] + "B\n" +  parts[totsp-2] + "B\n" + parts[totsp-3] + "B\n" + parts[totsp-1]
				if parts[totsp] == '/media/hdd':
					strview = parts[totsp-1].replace('%', '')
					if strview.isdigit():
						hddperc = int(parts[totsp-1].replace('%', ''))
						hddsumm = config.plugins.setupGlass17.par182.value+":\n" + parts[totsp-4] + "B\n" +  parts[totsp-2] + "B\n" + parts[totsp-3] + "B\n" + parts[totsp-1]
			f.close()
			os.remove('/tmp/tempinfo.tmp')
		self["sd"].setText(sdsumm)
		self["usb"].setText(usbsumm)
		self["hdd"].setText(hddsumm)
		self['sd_bar'].setValue(int(sdperc))
		self['usb_bar'].setValue(int(usbperc))
		self['hdd_bar'].setValue(int(hddperc))      		
