from Screens.Screen import Screen
from Components.Sources.List import List
from Components.ActionMap import NumberActionMap
from Components.Sources.StaticText import StaticText
from Components.config import configfile
from Components.PluginComponent import plugins
from Components.config import config
from Components.SystemInfo import SystemInfo
from enigma import ePoint, eTimer, eSize
from Tools.Directories import resolveFilename, SCOPE_SKIN, SCOPE_CURRENT_SKIN, fileExists
from Tools.LoadPixmap import LoadPixmap
from Components.PluginComponent import plugins
from Plugins.Plugin import PluginDescriptor
import xml.etree.cElementTree
import os
from Screens.Setup import Setup, getSetupTitle
from Components.Pixmap import Pixmap, MovingPixmap 
import six
lastMenuID = None

def Writelog(txt):
	log = "/usr/lib/enigma2/python/Screens//menu.log"
	if os.path.isfile(log) and os.path.getsize(log) > 1000000:
		try:
			os.remove(log)
		except OSError:
			pass
	try:
		f = open(log,"a")
		f.write("%s\n" % str(txt))
		f.close()
	except IOError: pass
	
IS_VU = False
DM8X = 0
try:
	if os.path.exists("/proc/stb/info/vumodel"):
		f = open("/proc/stb/info/vumodel")
		model = f.read().strip()
		f.close()
		if "duo2" in model:
			IS_VU = True
	elif os.path.exists("/proc/stb/info/model"):
		f = open('/proc/stb/info/model')
		line = f.read()
		f.close()
		if "800se" in line or "820" in line:
			DM8X = 1			
		elif "dm9" in line:
			DM8X = 2
except: pass
	
def MenuEntryPixmap(entryID, png_cache, lastMenuID):
	png = png_cache.get(entryID, None)
	if png is None: # no cached entry
		png = LoadPixmap(resolveFilename(SCOPE_CURRENT_SKIN, "menu/" + entryID + ".png")) #lets look for a dedicated icon
		if png is None: # no dedicated icon found
			if lastMenuID is not None:
				png = png_cache.get(lastMenuID, None)
		png_cache[entryID] = png
	if png is None:
		png = png_cache.get("missing", None)
		if png is None:
			png = LoadPixmap(resolveFilename(SCOPE_CURRENT_SKIN, "menu/missing.png"))
			png_cache["missing"] = png
	return png

# read the menu
mdom = xml.etree.cElementTree.parse(resolveFilename(SCOPE_SKIN, 'menu.xml'))

def findMenu(key):
	menuList = mdom.getroot().findall(f".//menu[@key='{key}']")
	count = len(menuList)
	if menuList:
		for index, menu in enumerate(menuList):
			print(f"[Menu] Found menu entry '{menu.get('text', '* Unknown *')}' ({index + 1} of {count}).")
		menu = menuList[0]
	else:
		print(f"[Menu] Error: Menu '{key}' not found!")
		menu = None
	return menu
	
class boundFunction:
	def __init__(self, fnc, *args):
		self.fnc = fnc
		self.args = args
	def __call__(self):
		self.fnc(*self.args)

class MenuUpdater:
	def __init__(self):
		self.updatedMenuItems = {}

	def addMenuItem(self, id, pos, text, module, screen, weight, description):
		if not self.updatedMenuAvailable(id):
			self.updatedMenuItems[id] = []
		self.updatedMenuItems[id].append([text, pos, module, screen, weight, description])

	def delMenuItem(self, id, pos, text, module, screen, weight, description):
		self.updatedMenuItems[id].remove([text, pos, module, screen, weight, description])

	def updatedMenuAvailable(self, id):
		return id in self.updatedMenuItems

	def getUpdatedMenu(self, id):
		return self.updatedMenuItems[id]

menuupdater = MenuUpdater()

class MenuSummaryIcon(Screen):

	if DM8X == 0:
		if IS_VU:
			skin = """
			<screen position="0,0" size="140,32">
			<widget source="parent.title" render="Label" position="0,0" size="140,16" font="Prive3;13" halign="center" valign="top" noWrap="1" />
			<widget source="item" render="Label" position="0,16" size="140,16" font="Prive3;13" halign="center" valign="center" noWrap="1" />
			</screen>"""
		else:
			skin = """
			<screen position="0,0" size="136,64" id="1">
			<widget source="parent.title" render="Label" position="6,0" size="120,22" font="Prive3;14" halign="center" valign="top" noWrap="1" />
			<widget source="item" render="Label" position="6,23" size="120,41" font="Prive3;15" halign="center" valign="center" />
			</screen>"""
	elif DM8X == 2:
		skin = """
		<screen position="0,0" size="400,240" id="3">
    <eLabel position="0,0" size="400,240" backgroundColor="#00000000" zPosition="-1" transparent="0" />
    <widget source="parent.title" render="Label" position="0,5" size="400,48" font="Prive3;46" halign="center" valign="top" noWrap="1" />
    <widget source="item" render="Label" position="0,12" size="400,220" font="Prive3;60" halign="center" valign="center" />
		</screen>"""
	else:
		skin = """
		<screen position="0,0" size="96,64" id="2">
    <widget source="parent.title" render="Label" position="0,0" size="96,22" font="Prive3;13" halign="center" valign="top" noWrap="1" />
    <widget source="item" render="Label" position="0,23" size="96,41" font="Prive3;14" halign="center" valign="center" />
		</screen>"""

	def __init__(self, session, parent):
		Screen.__init__(self, session, parent)
		self["item"] = StaticText("")

	def updateOLED(self, what):
		self["item"].setText(what)
                
class MenuSummary(Screen):
	skin = """
	<screen position="0,0" size="132,64">
		<widget source="parent.title" render="Label" position="6,4" size="120,21" font="Regular;18" />
		<widget source="parent.menu" render="Label" position="6,25" size="120,21" font="Regular;16">
			<convert type="StringListSelection" />
		</widget>
		<widget source="global.CurrentTime" render="Label" position="56,46" size="82,18" font="Regular;16" >
			<convert type="ClockToText">WithSeconds</convert>
		</widget>
	</screen>"""
	
class Menu(Screen):

	ALLOW_SUSPEND = True
	png_cache = {}

	def okbuttonClick(self):
		selection = self["menu"].getCurrent()
		if config.skin.primary_skin.value == "hd_glass17/skin.xml":
			selection = self.tlist[self.index]
		if selection is not None:
			global lastMenuID
			lastMenuID = selection[2]
			selection[1]()

	def execText(self, text):
		exec(text)

	def runScreen(self, arg):
		# arg[0] is the module (as string)
		# arg[1] is Screen inside this module
		#        plus possible arguments, as
		#        string (as we want to reference
		#        stuff which is just imported)
		# FIXME. somehow
		if os.path.exists("/usr/lib/python2.7") and str(arg[0]).find("Screens.Bh") != -1:
			self.openBhMenu(arg[0])
		else:
			if arg[0] != "":
				exec("from " + arg[0] + " import *")
			self.openDialog(*eval(arg[1]))

	def openBhMenu(self, module):
		module  = module.replace("Screens", "Blackhole")
		exec("from " + module + " import *")		
		if module == "Blackhole.BhSettings":
			self.session.openWithCallback(self.menuClosed, DeliteSettings)		
		elif module == "Blackhole.BhEpgPanel":
			self.session.openWithCallback(self.menuClosed, DeliteEpgPanel)			
		elif module == "Blackhole.BhAddons":
			self.session.openWithCallback(self.menuClosed, DeliteAddons)		
		elif module == "Blackhole.BhRed":
			exec("from Blackhole.BhUtils import BhU_check_proc_version")
			flash = True
			mounted = False
			bh_ver = BhU_check_proc_version()
			un_ver = bh_ver		
			f = open("/proc/mounts",'r')
			for line in f.readlines():
				if line.find('/universe') != -1:
					if line.find('ext') != -1:
						mounted = True
			f.close()		
			if fileExists("/.meoinfo"):
				flash = False		
			if flash == True:
				if mounted == True:
					if fileExists("/universe/.buildv"):
						f = open("/universe/.buildv",'r')
						un_ver = f.readline().strip()
						f.close()
					else:
						out = open("/universe/.buildv",'w')
						out.write(bh_ver)
						out.close()
						os.chmod("/universe/.buildv", 0o444)
					if un_ver == bh_ver:
						self.session.openWithCallback(self.menuClosed, BhRedPanel)
					else:
						self.session.openWithCallback(self.menuClosed, BhRedWrong)
				else:
					self.session.openWithCallback(self.menuClosed, BhRedDisabled, "0")
			else:
				self.session.openWithCallback(self.menuClosed, BhRedDisabled, "flash")

	def nothing(self):	#dummy
		pass

	def openDialog(self, *dialog):	# in every layer needed
		self.session.openWithCallback(self.menuClosed, *dialog)

	def openSetup(self, dialog):
		self.session.openWithCallback(self.menuClosed, Setup, dialog)

	def addMenu(self, destList, node):
		requires = node.get("requires")
		if requires:
			if requires[0] == '!':
				if SystemInfo.get(requires[1:], False):
					return
			elif not SystemInfo.get(requires, False):
				return
		MenuTitle = _(six.ensure_str(node.get("text", "??")))
		entryID = node.get("entryID", "undefined")
		if entryID == "undefined":
			entryID = node.get("entryId", "undefined")
			if entryID == "undefined":
				entryID = node.get("key", "undefined")	
		weight = node.get("weight", 50)
		description = six.ensure_str(node.get("description", "")) or None
		description = description and _(description)
		menupng = MenuEntryPixmap(entryID, self.png_cache, lastMenuID)
		x = node.get("flushConfigOnClose")
		if x:
			a = boundFunction(self.session.openWithCallback, self.menuClosedWithConfigFlush, Menu, node)
		else:
			a = boundFunction(self.session.openWithCallback, self.menuClosed, Menu, node)
		#TODO add check if !empty(node.childNodes)
		destList.append((MenuTitle, a, entryID, weight, description, menupng))

	def menuClosedWithConfigFlush(self, *res):
		configfile.save()
		self.menuClosed(*res)

	def menuClosed(self, *res):
		if res and res[0]:
			global lastMenuID
			lastMenuID = None
			self.close(True)

	def addItem(self, destList, node):
		requires = node.get("requires")
		if requires:
			if requires[0] == '!':
				if SystemInfo.get(requires[1:], False):
					return
			elif not SystemInfo.get(requires, False):
				return
		item_text = six.ensure_str(node.get("text", ""))
		entryID = node.get("entryID", "undefined")
		if entryID == "undefined":
			entryID = node.get("entryId", "undefined")
			if entryID == "undefined":
				entryID = node.get("key", "undefined")			
		weight = node.get("weight", 50)
		description = six.ensure_str(node.get("description", "")) or ''
		description = description and _(description)
		menupng = MenuEntryPixmap(entryID, self.png_cache, lastMenuID)
		for x in node:
			if x.tag == 'screen':
				module = x.get("module")
				screen = x.get("screen")
				if screen is None:
					screen = module
				if module:
					module = "Screens." + module
				else:
					module = ""

				# check for arguments. they will be appended to the
				# openDialog call
				args = x.text or ""
				screen += ", " + args

				destList.append((_(item_text or "??"), boundFunction(self.runScreen, (module, screen)), entryID, weight, description, menupng))
				return
			elif x.tag == 'code':
				destList.append((_(item_text or "??"), boundFunction(self.execText, x.text), entryID, weight, description, menupng))
				return
			elif x.tag == 'setup':
				id = x.get("id")
				if item_text == "":
					item_text = _(getSetupTitle(id))
				else:
					item_text = _(item_text)
				destList.append((item_text, boundFunction(self.openSetup, id), entryID, weight, description, menupng))
				return
		destList.append((item_text, self.nothing, entryID, weight, description, menupng))

	def __init__(self, session, parent):
		Screen.__init__(self, session)
		self.pos = []
		list = []
		self.typeIcons = "all"                                                              
		count = 17
		try:
			if config.plugins.setupGlass17.par7.value == "Icons Bar":
				self.typeIcons = "bar"
			if config.plugins.setupGlass17.par7.value in ["Icons Bar","Icons Right","Icons"]:
				count = 99
		except: pass
		if count == 99: 
			self.moveTimer = eTimer()
			try:
				self.moveTimer_conn = self.moveTimer.timeout.connect(self.moveON)
			except AttributeError:
				self.moveTimer.timeout.get().append(self.moveON)
		count = 17
		if self.typeIcons == "all":
			self['Page'] = StaticText()
			self['selection_frame'] = MovingPixmap()
			self['selection_frame1'] = MovingPixmap()
		elif self.typeIcons == "bar":
			count = 8
		for x in range(1,count):
			self['Ico%s' % x] = Pixmap()
			self['Description%s' % x] = StaticText()
		menuID = None
		count = 0
		for x in parent:	#walk through the actual nodelist
			if x.tag == 'item':
				item_level = int(x.get("level", 0))
				if item_level <= config.usage.setup_level.index:
					self.addItem(list, x)
					count += 1
			elif x.tag == 'menu':
				self.addMenu(list, x)
				count += 1
			elif x.tag == "id":
				menuID = x.get("val")
				count = 0
			if menuID is not None:
				# menuupdater?
				if menuupdater.updatedMenuAvailable(menuID):
					for x in menuupdater.getUpdatedMenu(menuID):
						if x[1] == count:
							description = six.ensure_str(x.get("description", "")) or ''
							description = description and _(description)
							menupng = MenuEntryPixmap(menuID, self.png_cache, lastMenuID)
							list.append((x[0], boundFunction(self.runScreen, (x[2], x[3] + ", ")), x[4], description, menupng))
							count += 1
		if menuID is None:
			try:
				menuID = parent.get("key")
			except: pass
		if menuID is not None:
			# plugins
			for l in plugins.getPluginsForMenu(menuID):
				# check if a plugin overrides an existing menu
				plugin_menuid = l[2]
				for x in list:
					if x[2] == plugin_menuid:
						list.remove(x)
						break
				description = None
				try:
					description = plugins.getDescriptionForMenuEntryID(menuID, plugin_menuid)
				except: pass
				menupng = MenuEntryPixmap(l[2], self.png_cache, lastMenuID)
				list.append((l[0], boundFunction(l[1], self.session), l[2], l[3] or 50, description, menupng))
		list.sort(key=lambda x: int(x[3]))
		self.tlist = list
		self["menu"] = List(list)
		if config.skin.primary_skin.value == "hd_glass17/skin.xml":
			if self.typeIcons == "all":
				self.skinName = 'AllMenuIcons'
				try:
					if config.plugins.setupGlass17.par7.value == "Icons Right":
						self.skinName = 'AllMenuIconsRight'
				except: pass
			elif self.typeIcons == "bar":
				self.skinName = 'BarMenuIcons'
		else:
			self.skinName = [ ]
			if menuID is not None:
				self.skinName.append("menu_" + menuID)
			self.skinName.append("Menu")			
			if os.path.exists('/etc/dpkg'):
				self._list = List(list)
				self["pixmap"] = Pixmap()
				self["description"] = StaticText()
				self.onLayoutFinish.append(self._onLayoutFinish)
				self._list.onSelectionChanged.append(self._onSelectionChanged)
		if config.skin.primary_skin.value != "hd_glass17/skin.xml":
			self["actions"] = NumberActionMap(["OkCancelActions", "MenuActions", "NumberActions"],
			{
				"ok": self.okbuttonClick,
				"cancel": self.closeNonRecursive,
				"menu": self.closeRecursive,
				"1": self.keyNumberGlobal,
				"2": self.keyNumberGlobal,
				"3": self.keyNumberGlobal,
				"4": self.keyNumberGlobal,
				"5": self.keyNumberGlobal,
				"6": self.keyNumberGlobal,
				"7": self.keyNumberGlobal,
				"8": self.keyNumberGlobal,
				"9": self.keyNumberGlobal
			})
		else:
			if self.typeIcons == "all":
				self.Aicon = 1
				self["actions"] = NumberActionMap(["OkCancelActions", "MenuActions", "DirectionActions", "NumberActions"],
				{
					"ok": self.okbuttonClick2,
					"cancel": self.closeNonRecursive,
					"left": self.key_left,
					"right": self.key_right,
					"up": self.key_up,
					"down": self.key_down,
					"menu": self.closeRecursive,
					"1": self.keyNumberGlobal,
					"2": self.keyNumberGlobal,
					"3": self.keyNumberGlobal,
					"4": self.keyNumberGlobal,
					"5": self.keyNumberGlobal,
					"6": self.keyNumberGlobal,
					"7": self.keyNumberGlobal,
					"8": self.keyNumberGlobal,
					"9": self.keyNumberGlobal
				})
			elif self.typeIcons == "bar":
				self.Aicon = 4
				self["actions"] = NumberActionMap(["OkCancelActions", "MenuActions", "DirectionActions", "NumberActions"],
				{
					"ok": self.okbuttonClick2,
					"cancel": self.closeNonRecursive,
					"left": self.key_left_bar,
					"right": self.key_right_bar,
					"menu": self.closeRecursive,
					"1": self.keyNumberGlobal,
					"2": self.keyNumberGlobal,
					"3": self.keyNumberGlobal,
					"4": self.keyNumberGlobal,
					"5": self.keyNumberGlobal,
					"6": self.keyNumberGlobal,
					"7": self.keyNumberGlobal,
					"8": self.keyNumberGlobal,
					"9": self.keyNumberGlobal
				})
		a = six.ensure_str(parent.get("title", "")) or None
		a = a and _(a)
		if a is None:
			a = _(six.ensure_str(parent.get("text", "")))
		self["title"] = StaticText(a)
		self.menu_title = a
		if self.typeIcons == "all":
			self.onShown.append(self.setIco)
			self.onLayoutFinish.append(self.setFramePositions)
			self.firstStart = True    
		elif self.typeIcons == "bar":
			self.onShown.append(self.setBarIco)
			self.onLayoutFinish.append(self.initPicsLabels)
		self.menuSort = False
		self.ena = False
		for p in plugins.getPlugins(where = [PluginDescriptor.WHERE_PLUGINMENU]):
			if  str(p.name) == "MenuSort":
				self.menuSort = True            		

	def _onLayoutFinish(self):
		self._onSelectionChanged()

	def _onSelectionChanged(self):
		current = self._list.current
		description, pixmap = "", None
		if current:
			description, pixmap = current[4:]
		self["description"].setText(_(description))
		if pixmap:
			self["pixmap"].setPixmap(pixmap)
			
	def initPicsLabels(self):
		list = self["menu"].list
		self.tlist = list
		self.maxentry = len(list) - 1
		self.maxPages = str(int(self.maxentry/16) + 1)
		self.index = 0
		self.page = 0
		self.pics = []
		self.labels = []
		defPixpath = "/usr/share/enigma2/hd_glass17/menu/undefined.png"
		try:
			pixpath = config.plugins.setupGlass17.par39.value + '/menuIcons/' + str(config.plugins.setupGlass17.par69.value) + "/undefined.png"
			if fileExists(pixpath):
				defPixpath = pixpath
		except : pass
		pixpath = defPixpath
		for x in list:
			pic = "undefined.png"
			try:
				pic = str(x[2]) + '.png'
			except : pass
			try:
				pixpath = config.plugins.setupGlass17.par39.value + '/menuIcons/' + str(config.plugins.setupGlass17.par69.value) + "/" + pic
			except : pass
			if not fileExists(pixpath):
				pixpath = defPixpath
			self.pics.append(pixpath)
			self.labels.append(x[0])
		if self.typeIcons == "all":
			self.setIco()
			
	def setFramePositions(self):
		if self.firstStart:
			self.initPicsLabels()
			self['Page'].setText("Page: %s / %s" % (self.page+1, self.maxPages))
			for x in range(1,17):
				self.pos.append([self['Ico%s' % x].instance.position().x(), self['Ico%s' % x].instance.position().y()])
			self.firstStart = False
          	
	def paintFrame(self):
		if self.menuSort:
			list = self["menu"].list		
			if self.tlist != list:
				self.initPicsLabels()
		if self.maxentry < self.index or self.index < 0:
			return 
		self.updOLED()
		idx = self.index - (self.page*16)
		if self.index > ((self.page*16) + 15):
			while self.index > ((self.page*16) + 15):
				self.page += 1
			self.setIco()
			idx = self.index - self.page*16
		elif self.index < ((self.page*16)):
			self.page -= 1
			self.setIco()
			idx = self.index - self.page*16
		ipos = self.pos[idx]
		self.Aicon = idx + 1
		self['Page'].setText("Page: %s / %s " % (self.page+1, self.maxPages))
		for what in ("", "1"):
			self['selection_frame%s' % what].moveTo(ipos[0], ipos[1], 1)
			self['selection_frame%s' % what].startMoving()

	def setIco(self):
		self.updOLED()
		rr = 16
		if self.page > 0 or (self.maxentry + 1) < 17:
			rr = len(self.tlist) - self.page*16
		for i in range(0, rr):
			self[('Ico' + str(i + 1))].instance.setPixmapFromFile(self.pics[self.page*16 + i])
			self[('Description' + str(i + 1))].setText(self.labels[self.page*16 + i])
		i += 1
		if i < 16:
			try:
				if config.plugins.setupGlass17.par60.value:
					rr = 16
					defPixpath = "/usr/share/enigma2/hd_glass17/menu/empty.png"
					pixpath = config.plugins.setupGlass17.par39.value + '/menuIcons/' + str(config.plugins.setupGlass17.par69.value) + "/empty.png"
					if fileExists(pixpath):
						defPixpath = pixpath
					for x in range(i,16):
						self[('Ico' + str(x + 1))].instance.setPixmapFromFile(defPixpath)
						self[('Description' + str(x + 1))].setText("")
			except: pass
		for i in range(0, rr):
			self[('Ico' + str(i + 1))].show()
		i += 1
		for x in range(i,16):
			self[('Ico' + str(x + 1))].hide()
			self[('Description' + str(x + 1))].setText("")		
		
	def key_left(self):
		if self.ena:
			return
		self.index -= 1
		if self.index < 0:
			self.index = self.maxentry
		self.paintFrame()

	def key_right(self):
		if self.ena:
			return
		self.index += 1
		if self.index > self.maxentry:
			self.index = 0
			self.page = 0
			self.setIco()
		self.paintFrame()

	def key_up(self):
		if self.ena:
			return
		self.index -= 4
		if self.index < 0:
			self.index = self.maxentry
		self.paintFrame()

	def key_down(self):
		if self.ena:
			return
		self.index += 4
		if self.index > self.maxentry:
			self.index = 0
			self.page = 0
			self.setIco()
		self.paintFrame()
                
	def setBarIco(self):
		if self.menuSort:
			list = self["menu"].list		
			if self.tlist != list:
				self.initPicsLabels()
		if self.maxentry < self.index or self.index < 0:
			return 
		self.updOLED()
		self['Ico4'].instance.setPixmapFromFile(self.pics[self.index])
		self['Description4'].setText(self.labels[self.index])
		i = 1
		while ((self.index + i) < (self.maxentry+1)) and i < 4:   
			self[('Ico' + str(i+4))].instance.setPixmapFromFile(self.pics[self.index+i])    
			self[('Ico' + str(i+4))].show()    
			self[('Description' + str(i+4))].setText(self.labels[self.index+i])
			i +=1
		for x in range(i+4,8):
			self[('Ico' + str(x))].hide()
			self[('Description' + str(x))].setText("")
		i = 1
		while ((self.index - i) > -1) and i < 4:   
			self[('Ico' + str(4-i))].instance.setPixmapFromFile(self.pics[self.index-i])    
			self[('Ico' + str(4-i))].show()    
			self[('Description' + str(4-i))].setText(self.labels[self.index-i])
			i +=1
		for x in range(1, 5-i):
			self[('Ico' + str(x))].hide()    
			self[('Description' + str(x))].setText("")
          
	def key_left_bar(self):
		if self.ena:
			return
		self.index -= 1
		if self.index < 0:
			self.index = self.maxentry
		self.setBarIco()

	def key_right_bar(self):
		if self.ena:
			return
		self.index += 1
		if self.index > self.maxentry:
			self.index = 0
		self.setBarIco()

	def okbuttonClick2(self):
		if self.ena:
			return                                                                                     
		try:
			if config.plugins.setupGlass17.par63.value and (config.plugins.setupGlass17.par7.value == "Icons Bar" or config.plugins.setupGlass17.par7.value == "Icons Right" or config.plugins.setupGlass17.par7.value == "Icons"):
				self.posX = self['Ico%s' % str(self.Aicon)].instance.position().x()
				self.posY = self['Ico%s' % str(self.Aicon)].instance.position().y()
				self.sizeXY = self['Ico%s' % str(self.Aicon)].instance.size().width()
				self.newposY = self.posY
				self.newsizeY = self.sizeXY
				self['Description%s' % str(self.Aicon)].setText(_("Starting"))	
				self.ena = True
				self.moveTimer.start(10)
			else:
				self.okbuttonClick()
		except: self.okbuttonClick()

	def moveON(self):
		self.moveTimer.stop()
		if self.newposY > self.posY+self.sizeXY or self.newsizeY < 0:
			self.okbuttonClick()
			self['Ico%s' % str(self.Aicon)].instance.move(ePoint(int(self.posX), int(self.posY)))
			self['Ico%s' % str(self.Aicon)].instance.resize(eSize(self.sizeXY, self.sizeXY))
			self['Description%s' % str(self.Aicon)].setText(self.labels[self.index])
			self.ena = False
		else:
			self.newposY += 3
			self.newsizeY -= 3
			if self.newsizeY < 0:
				self['Ico%s' % str(self.Aicon)].instance.resize(eSize(self.sizeXY, 0))
			else:
				self['Ico%s' % str(self.Aicon)].instance.resize(eSize(self.sizeXY, int(self.newsizeY)))
			self['Ico%s' % str(self.Aicon)].instance.move(ePoint(int(self.posX), int(self.newposY)))
			self.moveTimer.start(20)

	def keyNumberGlobal(self, number):
		number -= 1

		if len(self["menu"].list) > number:
			self["menu"].setIndex(number)
			self.okbuttonClick()

	def closeNonRecursive(self):
		self.close(False)

	def closeRecursive(self):
		self.close(True)

	def createSummary(self):
		if config.skin.primary_skin.value == "hd_glass17/skin.xml":
			return MenuSummaryIcon
		else:
			return MenuSummary

	def updOLED(self):
		try:
			self.session.summary.updateOLED(self.labels[self.index])
		except: pass

class MainMenu(Menu):
	#add file load functions for the xml-file

	def __init__(self, *x):
		self.skinName = "Menu"
		Menu.__init__(self, *x)
