from Screens.Screen import Screen
from Components.Label import Label
from Components.ServiceEventTracker import ServiceEventTracker
from enigma import eTimer, iServiceInformation, iPlayableService, ePoint, eSize, eServiceReference 
from Components.Pixmap import Pixmap
from Tools.Directories import fileExists
from Components.config import config
from Plugins.Plugin import PluginDescriptor
import os

ENA = True
try:
	if config.plugins.setupGlass17.par78.value != "i":
		ENA = False
except: pass
ECMREFRESH = 6000
try:
	ECMREFRESH = int(config.plugins.setupGlass17.par74.value)*1000
except: pass

class InfoEcmScreen(Screen):

	skin = """      
		<screen name="InfoEcmScreen" position="135,180" zPosition="8" size="690,540" title="ECM Info ver. 12.00" backgroundColor="background">
		<widget name="ecmLabels" font="Prive3;24" position="30,15" size="165,397" zPosition="4" foregroundColor="#5a89d0" transparent="1" backgroundColor="background" />
		<widget name="ecmValues" font="Prive3;24" position="202,15" size="488,397" zPosition="4" transparent="1" backgroundColor="background" />
    <widget name="frameCode" position="103,400" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
		<widget name="piconCode" position="122,416" zPosition="5"  size="150,90" alphatest="on" />
    <widget name="frameCam" position="396,400" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
		<widget name="piconCam" position="415,416" zPosition="5" size="150,90" alphatest="on" />
		</screen>"""

	def __init__(self, session):
		Screen.__init__(self,session)
		self.session = session
		self.skin = InfoEcmScreen.skin
		self['ecmValues'] = Label("No information from ECM Info")
		self['ecmLabels'] = Label()
		for x in ('piconCode','piconCam','frameCode','frameCam'):
			self[x] = Pixmap()
			self[x].hide()
		self.__sleep = False
		self.__first = True
		self.ecmTimer = eTimer()
		try:
			self.ecmTimer_conn = self.ecmTimer.timeout.connect(self.__RefreshMe)
		except AttributeError:
			self.ecmTimer.timeout.get().append(self.__RefreshMe)
		if ENA:
			from Components.ActionMap import ActionMap
			self["actions"] = ActionMap(["ColorActions", "SetupActions", "DirectionActions"],
			{
            "green": self.exit,
            "red": self.exit,
            "ok": self.exit,
            "cancel": self.exit,
            "yellow": self.exit,
            "blue": self.exit
			}, -2)	
		else:	
			self._SpecialScreen__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evStopped: self._InfoEcmScreen__SetDef, iPlayableService.evUpdatedInfo: self._InfoEcmScreen__Wakeup, iPlayableService.evTunedIn: self._InfoEcmScreen__Wakeup})
			self.onHide.append(self.__goStandby)
		self.onLayoutFinish.append(self.firstRun)	
		self.onShow.append(self.__goWakeup)
			
	def exit(self):
		self.ecmTimer.stop()
		self.ecmTimer_conn = None
		self.ecmTimer = None
		self.close()
        
	def firstRun(self):
		if self.__first:
			self.__first = False
			if self.instance:
				try:
					self.instance.move(ePoint(config.plugins.setupGlass17.par10.value, config.plugins.setupGlass17.par11.value))
				except: pass
			for x in ("piconCode","piconCam"):
				try:
					self[x].instance.setScale(1)
				except: pass
      		
	def __SetDef(self):				
		self.ecmTimer.stop()
		self['ecmLabels'].setText(" ")
		self['ecmValues'].setText(" ")
		self.setPicons("default","default")

	def __goStandby(self):
		self.ecmTimer.stop()
		self.__sleep = True
    		
	def __goWakeup(self):
		self.__sleep = False
		self.__Wakeup()

	def __Wakeup(self):
		if not self.ecmTimer.isActive() and not self.__sleep:
			self.ecmTimer.start(1000, True)

	def __RefreshMe(self):
		self.ecmTimer.stop()
		caids,sid,pmtpid,nameSpaceId,refer = self.getEnigmaInformation()
		referenceId = ""
		if refer != "": 
			r = "_"
			try:
				if config.plugins.setupGlass17.par179.value != "a":
					r = ":"
			except: pass
			referenceId = r.join(refer.split(':', 10)[:10])
		if refer != "" and (refer.startswith("4097:0") or "3a//" in refer or "http" in refer):
			self.setPicons("STREAM","default","piconProv","")
			self.instance.resize(eSize(690,320))
			self["piconCode"].move(ePoint(269,168))
			self['piconCam'].hide()         
			self["frameCode"].move(ePoint(250,152))
			self['frameCam'].hide() 
			self['ecmLabels'].setText("\n\nReference:\nNamespace:")
			self['ecmValues'].setText("IPTV or Streaming Service\n\n"+referenceId+"\n"+nameSpaceId)
		elif not self.getFta():
			self.__getEcmInfoFile(caids,sid,pmtpid,nameSpaceId,referenceId)
		else:
			self.setPicons("Fta","default")
			self.instance.resize(eSize(690,320))
			self["piconCode"].move(ePoint(269,193))
			self['piconCam'].hide()         
			self["frameCode"].move(ePoint(250,177))
			self['frameCam'].hide() 
			self['ecmLabels'].setText("\n\nSID:\nReference:\nNamespace:")
			self['ecmValues'].setText("Free To Air\n\n"+sid+"\n"+referenceId+"\n"+nameSpaceId)
		if not self.__sleep:
			self.ecmTimer.start(ECMREFRESH, True)
            
	def chckEcmInfo(self):
		if os.path.isfile('/tmp/ecm.info'):
			try:
				if os.path.getsize('/tmp/ecm.info') > 10:
					f = open('/tmp/ecm.info', "r").read()
					if f.find("fta") == -1 and f.find("Signature OK") == -1 and f.find("system: BISS") == -1:
						return True
			except: pass
		return False
		
	def getFta(self):
		service = self.session.nav.getCurrentService()
		info = service and service.info()
		if info:
			serviceinfo = service.info()
			if serviceinfo.getInfo(iServiceInformation.sIsCrypted) or self.chckEcmInfo():
				return False    
		return True

	def getEnigmaInformation(self):
		caids = sid = pmtpid = nameSpaceId = refer = ""
		service = self.session.nav.getCurrentService()
		info = service and service.info()
		if info:
			serviceInfo = service.info()
			caidlist = info.getInfoObject(iServiceInformation.sCAIDs)
			if caidlist:
				if len(caidlist)>0:
					for tt in caidlist:
						caids += " "+ "%0.4X" % tt
			caids = caids.lstrip()
			sid = "%0.4X" % serviceInfo.getInfo(iServiceInformation.sSID)
			if "-0001" in sid:
				sid = ""
			pmtpid = "%0.4X" % serviceInfo.getInfo(iServiceInformation.sPMTPID) 
			if "-0001" in pmtpid:
				pmtpid = ""
			refer = eServiceReference(info.getInfoString(iServiceInformation.sServiceref))
			if refer is not None:
				refer = refer.toString()
				if refer.startswith("-1:"):
					refer = self.session.nav.getCurrentlyPlayingServiceReference()
					if refer is not None:
						refer = refer.toString()
			try:
				nameSpaceId = refer.split(":")
				nameSpaceId = nameSpaceId[len(nameSpaceId)-5]
			except: pass
		return caids,sid,pmtpid,nameSpaceId,refer

	def __getEcmInfoFile(self,caids,sid,pmtpid,nameSpaceId,referenceId):
		tmp = "2"
		try:
			tmp = config.plugins.setupGlass17.par38.value
			if not config.plugins.setupGlass17.par50.value:
				tmp += config.plugins.setupGlass17.par194.value
			tmp = tmp.strip().split('\n')
		except: pass
		if len(tmp) > 10 and tmp[1] != "..............":
			self.instance.resize(eSize(690,540))
			self["piconCode"].move(ePoint(122,416))        
			self["piconCam"].move(ePoint(415,416)) 
			self["frameCode"].move(ePoint(103,400))        
			self["frameCam"].move(ePoint(396,400))
			self.getEcmInfoData(tmp,caids,sid,pmtpid,nameSpaceId,referenceId)
		else:
			self.instance.resize(eSize(690,396))
			self.setPicons("Unknown","Unknown")
			self["piconCode"].move(ePoint(269,271))
			self['piconCam'].hide()
			self["frameCode"].move(ePoint(250,255))
			self['frameCam'].hide()
			self['ecmLabels'].setText("SID:\nPMT PID:\nNamespace:\nReference:\nCAIDs:")
			self['ecmValues'].setText(sid+"\n"+pmtpid+"\n"+nameSpaceId+"\n"+referenceId+"\n"+caids)                      

	def getPidInfoFile(self):
		lines = ""
		try:
			tmp = open('/tmp/pid.info','r')
			content = tmp.read()
			tmp.close()
			lines = content.split("\n")
		except: pass
		return lines
    
	def getEcmInfoData(self,tmp,caids,sid,pmtpid,nameSpaceId,referenceId):
		def cutMe(c):
			if len(c) > 33:
				c = c[0:33]+"..."
			return c
		for x in range(0,len(tmp)):
			if tmp[x] == "..............":
				tmp[x] = ""
		cam = tmp[0]
		caid = tmp[1]
		provider = ""
		try:
			if config.plugins.setupGlass17.par195.value != "Prov.:":
				provider = cutMe(tmp[2])
		except: pass
		provid = ""
		try:
			if config.plugins.setupGlass17.par195.value != "PrvID:":
				provid = cutMe(tmp[3])
		except: pass
		pid = tmp[4]
		using = cutMe(tmp[5])
		protocol = tmp[6]
		adresa = cutMe(tmp[7])
		hops = tmp[8]
		share = tmp[9]
		ecmTime = tmp[10]
		system = tmp[11]
		cw0 = tmp[12]
		cw1 = tmp[13] 
		typeR = ""
		try:
			typeR = config.plugins.setupGlass17.par178.value
		except: pass
		ecmType = cam
		if system == "":
			system = "Unknown"
		if cam == "":
			ecmType = "Unknown"							
		elif "Ncam" in cam:
			ecmType = "Ncam"
		elif "Gcam" in cam:
			ecmType = "Ncam"
		elif "DOScam" in cam:
			ecmType = "DOScam"
		elif "OScam" in cam:
			ecmType = "OScam"
		if provider == "" and provid != "":
			provider = provid
		elif provider != "" and provid == "":
			provid = provider
		caid2 = caid+":"+provid+":"+sid+":"+pmtpid+":"+pid
		caid3 = caid+":"+sid+":"+pmtpid+":"+pid
		self.setPicons(system,ecmType)
		if ecmType == "Wicardd":
			if adresa != "":
				self['ecmLabels'].setText("CAM:\nUsing:\nProvider:\nSystem:\nECM Time:\nDecoded:\n\nNamespace:\nCW0:\nCW1:\nAddress:\nReference:\nCAIDs:")
				self['ecmValues'].setText("Wicardd\n"+using+"\n"+provider+"\n"+system+"\n"+ecmTime+"\n"+caid2+"\n[CAID:ProvID:SID:PMT PID:PID]\n"+nameSpaceId+"\n"+cw0+"\n"+cw1+"\n"+adresa+"\n"+referenceId+"\n"+caids)
			elif system != "Unknown":
				self['ecmLabels'].setText("CAM:\nUsing:\nSystem:\nProvider:\nSystem:\nDecoded:\n\nNamespace:\nCW0:\nCW1:\nReference\nCAIDs:")
				self['ecmValues'].setText("Wicardd\n"+using+"\n"+system+"\n"+provider+"\n"+system+"\n"+caid2+"\n[CAID:ProvID:SID:PMT PID:PID]\n"+nameSpaceId+"\n"+cw0+"\n"+cw1+"\n"+referenceId+"\n"+caids)
			else:
				self['ecmLabels'].setText("CAM:\nSid:\nCW0:\nCW1:\nReference:\nCAIDs:")
				self['ecmValues'].setText("Wicardd\n"+sid+"\n"+cw0+"\n"+cw1+"\n"+referenceId+"\n"+caids)
		elif ecmType == "CCcam":
			if typeR in ("crd","emu"):
				self['ecmLabels'].setText("CAM:\nUsing:\nSystem:\nProvider:\nSystem:\nECM Time:\nDecoded:\n\nNamespace:\nReference:\nCAIDs:")
				self['ecmValues'].setText("CCcam\n"+using+"\n"+system+"\n"+provider+"\n"+system+"\n"+ecmTime+"\n"+caid2+"\n[CAID:ProvID:SID:PMT PID:PID]\n"+nameSpaceId+"\n"+referenceId+"\n"+caids)
			elif system != "Unknown":
				self['ecmLabels'].setText("CAM:\nUsing:\nSystem:\nProvider:\nSystem:\nECM Time:\nDecoded:\n\nNamespace:\nAddress:\nReference:\nCAIDs:")
				self['ecmValues'].setText("CCcam\n"+using+"\n"+system+"\n"+provider+"\n"+system+"\n"+ecmTime+"\n"+caid2+"\n[CAID:ProvID:SID:PMT PID:PID]\n"+nameSpaceId+"\n"+adresa+" [Hops: "+hops+"]\n"+referenceId+"\n"+caids)
		elif ecmType == "Mgcamd":
			if adresa != "":
				self['ecmLabels'].setText("CAM:\nUsing:\nSystem:\nProvider:\nSystem:\nECM Time:\nDecoded:\n\nNamespace:\nCW0:\nCW1:\nAddress:\nReference:\nCAIDs:")
				self['ecmValues'].setText("Mgcamd\n"+using+"\n"+system+"\n"+provider+"\n"+system+"\n"+ecmTime+"\n"+caid2+"\n[CAID:ProvID:SID:PMT PID:PID]\n"+nameSpaceId+"\n"+cw0+"\n"+cw1+"\n"+adresa+"\n"+referenceId+"\n"+caids)
			elif system != "Unknown":
				self['ecmLabels'].setText("CAM:\nUsing:\nSystem:\nProvider:\nSystem:\nDecoded:\n\nNamespace:\nCW0:\nCW1:\nReference:\nCAIDs:")
				self['ecmValues'].setText("Mgcamd\n"+using+"\n"+system+"\n"+provider+"\n"+system+"\n"+caid2+"\n[CAID:ProvID:SID:PMT PID:PID]\n"+nameSpaceId+"\n"+cw0+"\n"+cw1+"\n"+referenceId+"\n"+caids)
			else:
				self['ecmLabels'].setText("CAM:\nSid:\nCW0:\nCW1:\nReference:\nCAIDs:")
				self['ecmValues'].setText("Mgcamd\n"+sid+"\n"+cw0+"\n"+cw1+"\n"+referenceId+"\n"+caids)
		elif ecmType == "Gbox":
			provids = ""
			providsList = []
			lines = self.getPidInfoFile()
			for line in lines:
				tmp = (str(line)).upper().strip()
				if tmp.find("PROVID:") != -1:
					providsList.append((str(tmp.split("PROVID:")[1])).strip())
			providsList = [providsList[i] for i,x in enumerate(providsList) if x not in providsList[i+1:]]
			providsList.sort()
			provids = " ".join(str(n) for n in providsList)
			if len(caids)>34:
				self['ecmLabels'].setText("CAM:\nUsing:\nSystem:\nDecoded:\n\nNamespace:\nCW0:\nCW1:\nReference:\nCAIDs:\n\nProvids:")
				self['ecmValues'].setText("Gbox\n"+using+"\n"+system+"\n"+caid3+"\n[CAID:ProvID:SID:PMT PID:PID]\n"+nameSpaceId+"\n"+cw0+"\n"+cw1+"\n"+referenceId+"\n"+caids+"\n"+provids)
			else:
				self['ecmLabels'].setText("CAM:\nUsing:\nSystem:\nDecoded:\n\nNamespace:\nCW0:\nCW1:\nReference:\nCAIDs:\nProvids:")
				self['ecmValues'].setText("Gbox\n"+using+"\n"+system+"\n"+caid3+"\n[Caid:SID:PMT PID:PID]\n"+nameSpaceId+"\n"+cw0+"\n"+cw1+"\n"+referenceId+"\n"+caids+"\n"+provids)
		elif ecmType in ("OScam","DOScam","Ncam","Gcam"):
			if typeR == "crd":
				self['ecmLabels'].setText("CAM:\nUsing:\nProvider:\nSystem:\nECM Time:\nDecoded:\n\nNamespace:\nCW0:\nCW1:\nReference:\nCAIDs:")
				self['ecmValues'].setText(cam+ "\n"+using+"\n"+provider+"\n"+system+"\n"+ecmTime+"\n"+caid2+"\n[CAID:ProvID:SID:PMT PID:PID]\n"+nameSpaceId+"\n"+cw0+"\n"+cw1+"\n"+referenceId+"\n"+caids)     
			elif typeR == "net":
				if protocol == "constcw":
					self['ecmLabels'].setText("CAM:\nUsing:\nProvider:\nSystem:\nECM Time:\nDecoded:\n\nNamespace:\nCW0:\nCW1:\nFile:\nReference:\nCAIDs:")
					self['ecmValues'].setText(cam+"\n"+protocol+"\n"+provider+"\n"+system+"\n"+ecmTime+"\n"+caid2+"\n[CAID:ProvID:SID:PMT PID:PID]\n"+nameSpaceId+"\n"+cw0+"\n"+cw1+"\n"+adresa+"\n"+referenceId+"\n"+caids)
				elif adresa != "":
					self['ecmLabels'].setText("CAM:\nUsing:\nProvider:\nSystem:\nECM Time:\nDecoded:\n\nNamespace:\nCW0:\nCW1:\nAddress:\nReference:\nCAIDs:")
					self['ecmValues'].setText(cam+"\n"+using+"\n"+provider+"\n"+system+"\n"+ecmTime+"\n"+caid2+"\n[CAID:ProvID:SID:PMT PID:PID]\n"+nameSpaceId+"\n"+cw0+"\n"+cw1+"\n"+adresa+" [Hops: "+hops+"]\n"+referenceId+"\n"+caids)
				else:
					self['ecmLabels'].setText("CAM:\nUsing:\nProvider:\nSystem:\nECM Time:\nDecoded:\n\nNamespace:\nCW0:\nCW1:\nReference:\nCAIDs:")
					self['ecmValues'].setText(cam+"\n"+using+"\n"+provider+"\n"+system+"\n"+ecmTime+"\n"+caid2+"\n[CAID:ProvID:SID:PMT PID:PID]\n"+nameSpaceId+"\n"+cw0+"\n"+cw1+"\n"+referenceId+"\n"+caids)
			elif typeR == "emu":
				self['ecmLabels'].setText("CAM:\nUsing:\nProvider:\nSystem:\nECM Time:\nDecoded:\n\nNamespace:\nCW0:\nCW1:\nReference:\nCAIDs:")
				self['ecmValues'].setText(cam+"\n"+using+"\n"+provider+"\n"+system+"\n"+ecmTime+"\n"+caid2+"\n[CAID:ProvID:SID:PMT PID:PID]\n"+nameSpaceId+"\n"+cw0+"\n"+cw1+"\n"+referenceId+"\n"+caids)
    
	def setPicons(self,ecmCode,ecmType,path="piconCam",fs="-fs8"):
		try:
			path = config.plugins.setupGlass17.par39.value + "/%s/" % path
		except: pass
		pictDef = "/usr/share/enigma2/hd_glass17/icons/missing-fs8.png"
		pict = path + ecmCode + fs + ".png" 
		if not fileExists(pict):
			pict = pictDef
		self['piconCode'].instance.setPixmapFromFile(pict)
		self['piconCode'].show()
		self['frameCode'].show()
		pict = path + ecmType + "-fs8.png" 
		if not fileExists(pict):
			pict = pictDef
		self['piconCam'].instance.setPixmapFromFile(pict)
		self['piconCam'].show()    
		self['frameCam'].show()    
 


