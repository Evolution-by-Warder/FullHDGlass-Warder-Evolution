"""Approved OpenATV graph painter with an OpenPLi data/timer bridge.

buildGraphEntry is copied unchanged from openatv/enigma2 EpgList.py at
 da455f57dda38b5f0de0744c913ee2270b7dc2ba (GPL-2.0-only).
Only the bridge below adapts OpenPLi objects; no second cell renderer is used.
"""
from time import time
from types import SimpleNamespace as NS


def make_graph_builder(api):
    # Dependencies are supplied by the receiver or the rendering verification.
    CompareWithAlternatives = api.CompareWithAlternatives
    MultiContentEntryPixmapAlphaBlend = api.MultiContentEntryPixmapAlphaBlend
    MultiContentEntryPixmapAlphaTest = api.MultiContentEntryPixmapAlphaTest
    MultiContentEntryText = api.MultiContentEntryText
    getChannelSelectionPiconName = api.getChannelSelectionPiconName
    loadPNG = api.loadPNG
    gFont = api.gFont
    getTextBoundarySize = api.getTextBoundarySize
    RT_HALIGN_LEFT, RT_HALIGN_CENTER = api.RT_HALIGN_LEFT, api.RT_HALIGN_CENTER
    RT_VALIGN_CENTER = api.RT_VALIGN_CENTER
    BT_SCALE, BT_KEEP_ASPECT_RATIO = api.BT_SCALE, api.BT_KEEP_ASPECT_RATIO
    config = api.config
    time = api.time

    def buildGraphEntry(self, service, service_name, events, picon, channel):
    	if self.listSizeWidth != self.l.getItemSize().width():
    		self.recalcEntrySize()
    	r1 = self.service_rect
    	r2 = self.event_rect
    	left = r2.x
    	top = r2.y
    	width = r2.w
    	height = r2.h
    	selected = self.cur_service is not None and self.cur_service[0] == service
    	res = [None]

    	serviceForeColor = self.foreColorService
    	serviceBackColor = self.backColorService
    	bgpng = self.othServPix
    	if CompareWithAlternatives(service, self.currentlyPlaying and self.currentlyPlaying.toString()):
    		serviceForeColor = self.foreColorServiceNow
    		serviceBackColor = self.backColorServiceNow
    		bgpng = self.nowServPix

    	if bgpng is not None and self.graphic:
    		serviceBackColor = None
    		res.append(MultiContentEntryPixmapAlphaBlend(
    			pos=(r1.x + self.serviceBorderWidth, r1.y + self.serviceBorderWidth),
    			size=(r1.w - 2 * self.serviceBorderWidth, r1.h - 2 * self.serviceBorderWidth),
    			png=bgpng, flags=BT_SCALE))
    	else:
    		res.append(MultiContentEntryText(
    			pos=(r1.x, r1.y), size=(r1.w, r1.h),
    			font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER,
    			text="",
    			color=serviceForeColor, color_sel=serviceForeColor,
    			backcolor=serviceBackColor, backcolor_sel=serviceBackColor,
    			border_width=self.serviceBorderWidth, border_color=self.borderColorService))

    	displayPicon = None
    	piconWidth = 0
    	if self.showPicon:
    		if picon is None:
    			picon = getChannelSelectionPiconName(service)
    			curIdx = self.l.getCurrentSelectionIndex()
    			self.list[curIdx] = (service, service_name, events, picon, channel)
    		if picon != "":
    			displayPicon = loadPNG(picon)
    		if displayPicon is not None:
    			piconWidth = self.picon_size.width()
    			res.append(MultiContentEntryPixmapAlphaBlend(
    				pos=(r1.x + self.serviceBorderWidth, r1.y + self.serviceBorderWidth),
    				size=(piconWidth, self.picon_size.height()),
    				png=displayPicon,
    				backcolor=None, backcolor_sel=None,
    				flags=BT_SCALE | BT_KEEP_ASPECT_RATIO))
    		elif not self.showServiceTitle:
    			piconWidth = self.picon_size.width()

    	channelWidth = 0
    	if self.showServiceNumber:
    		if not isinstance(channel, int):
    			channel = self._getChannelNumber(channel)
    		if channel:
    			namefontflag = RT_HALIGN_CENTER | RT_VALIGN_CENTER
    			font = gFont(self.serviceFontNameGraph,
    							self.serviceFontSizeGraph + self.epgConfig.servfs.value)
    			channelWidth = getTextBoundarySize(
    				self.instance, font, self.instance.size(),
    				(channel < 10000) and "0000" or str(channel)).width()
    			res.append(MultiContentEntryText(
    				pos=(r1.x + self.serviceNamePadding + piconWidth + self.serviceNamePadding,
    						r1.y + self.serviceBorderWidth),
    				size=(channelWidth, r1.h - 2 * self.serviceBorderWidth),
    				font=0, flags=namefontflag,
    				text=str(channel),
    				color=serviceForeColor, color_sel=serviceForeColor,
    				backcolor=serviceBackColor, backcolor_sel=serviceBackColor))

    	if self.showServiceTitle or displayPicon is None:
    		namefont = 0
    		namefontflag = int(config.epgselection.grid.servicename_alignment.value)
    		namewidth = r1.w - channelWidth - piconWidth
    		res.append(MultiContentEntryText(
    			pos=(r1.x + self.serviceNamePadding + piconWidth + self.serviceNamePadding
    					+ channelWidth + self.serviceNumberPadding,
    					r1.y + self.serviceBorderWidth),
    			size=(namewidth - 3 * (self.serviceBorderWidth + self.serviceNamePadding),
    					r1.h - 2 * self.serviceBorderWidth),
    			font=namefont, flags=namefontflag,
    			text=service_name,
    			color=serviceForeColor, color_sel=serviceForeColor,
    			backcolor=serviceBackColor, backcolor_sel=serviceBackColor))

    	if self.isIceTV(service) and config.epg.eit.value and self.icetvicon:
    		iceicon_size = self.icetvicon.size()
    		res.append(MultiContentEntryPixmapAlphaBlend(
    			pos=(r1.x + r1.w - self.serviceBorderWidth - iceicon_size.width(),
    					r1.y + r1.h - self.serviceBorderWidth - iceicon_size.height()),
    			size=(iceicon_size.width(), iceicon_size.height()),
    			png=self.icetvicon, backcolor=None, backcolor_sel=None))

    	# Service borders (graphic mode).
    	for (pixmap, pos, size) in (
    			(self.borderTopPix, (r1.x, r1.y), (r1.w, self.serviceBorderWidth)),
    			(self.borderTopPix, (r2.x, r2.y), (r2.w, self.eventBorderWidth)),
    			(self.borderBottomPix, (r1.x, r1.h - self.serviceBorderWidth), (r1.w, self.serviceBorderWidth)),
    			(self.borderBottomPix, (r2.x, r2.h - self.eventBorderWidth), (r2.w, self.eventBorderWidth)),
    			(self.borderLeftPix, (r1.x, r1.y), (self.serviceBorderWidth, r1.h)),
    			(self.borderLeftPix, (r2.x, r2.y), (self.eventBorderWidth, r2.h)),
    			(self.borderRightPix, (r1.w - self.serviceBorderWidth, r1.x), (self.serviceBorderWidth, r1.h)),
    			(self.borderRightPix, (r2.x + r2.w - self.eventBorderWidth, r2.y), (self.eventBorderWidth, r2.h)),
    	):
    		if pixmap is not None and self.graphic:
    			res.append(MultiContentEntryPixmapAlphaTest(
    				pos=pos, size=size, png=pixmap, flags=BT_SCALE))

    	# Default event area background.
    	if self.graphic:
    		areaPix = self.selEvPix if selected else self.othEvPix
    		if areaPix:
    			res.append(MultiContentEntryPixmapAlphaTest(
    				pos=(r2.x + self.eventBorderWidth, r2.y + self.eventBorderWidth),
    				size=(r2.w - 2 * self.eventBorderWidth, r2.h - 2 * self.eventBorderWidth),
    				png=areaPix, flags=BT_SCALE))
    	else:
    		res.append(MultiContentEntryText(
    			pos=(left, top), size=(width, height),
    			font=1, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER,
    			text="", color=None, color_sel=None,
    			backcolor=self.backColor, backcolor_sel=self.backColorSelected,
    			border_width=self.eventBorderWidth, border_color=self.borderColor))

    	if events:
    		start = self.time_base + self.offs * self.time_epoch * 60
    		end = start + self.time_epoch * 60
    		now = time()
    		infowidth = self.epgConfig.infowidth.value

    		for ev in events:
    			stime = ev[2]
    			duration = ev[3]
    			xpos, ewidth = self.calcEntryPosAndWidthHelper(stime, duration, start, end, width)
    			clock_types = self.getPixmapForEntry(service, ev[0], stime, duration)

    			isNow = stime <= now < (stime + duration)
    			isRec = clock_types is not None and clock_types in (2, 12)
    			isZap = clock_types is not None and clock_types == 7

    			if isNow:
    				if isRec:
    					foreColor, backColor = self.foreColorRecord, self.backColorRecord
    					foreColorSel, backColorSel = self.foreColorRecordSelected, self.backColorRecordSelected
    				else:
    					foreColor, backColor = self.foreColorNow, self.backColorNow
    					foreColorSel, backColorSel = self.foreColorNowSelected, self.backColorNowSelected
    			elif isRec:
    				foreColor, backColor = self.foreColorRecord, self.backColorRecord
    				foreColorSel, backColorSel = self.foreColorRecordSelected, self.backColorRecordSelected
    			elif isZap:
    				foreColor, backColor = self.foreColorZap, self.backColorZap
    				foreColorSel, backColorSel = self.foreColorZapSelected, self.backColorZapSelected
    			else:
    				foreColor, backColor = self.foreColor, self.backColor
    				foreColorSel, backColorSel = self.foreColorSelected, self.backColorSelected

    			isSelected = selected and self.select_rect is not None and self.select_rect.x == xpos + left

    			if isSelected:
    				clocks = self.selclocks[clock_types] if clock_types is not None else None
    				bTopPix = self.borderSelectedTopPix
    				bLeftPix = self.borderSelectedLeftPix
    				bBottomPix = self.borderSelectedBottomPix
    				bRightPix = self.borderSelectedRightPix
    				infoPix = self.selInfoPix
    				if isRec:
    					bgpng = self.recSelEvPix
    				elif isNow:
    					bgpng = self.nowSelEvPix
    				else:
    					bgpng = self.selEvPix
    			else:
    				clocks = self.clocks[clock_types] if clock_types is not None else None
    				bTopPix = self.borderTopPix
    				bLeftPix = self.borderLeftPix
    				bBottomPix = self.borderBottomPix
    				bRightPix = self.borderRightPix
    				infoPix = self.InfoPix
    				if isNow:
    					if clock_types is not None and clock_types in (2, 12):
    						bgpng = self.recordingEvPix
    					else:
    						bgpng = self.nowEvPix
    				else:
    					if isRec:
    						bgpng = self.recEvPix
    					elif isZap:
    						bgpng = self.zapEvPix
    					else:
    						bgpng = self.othEvPix

    			# Event background.
    			if bgpng is not None and self.graphic:
    				backColor = backColorSel = None
    				res.append(MultiContentEntryPixmapAlphaTest(
    					pos=(left + xpos + self.eventBorderWidth, top + self.eventBorderWidth),
    					size=(ewidth - 2 * self.eventBorderWidth, height - 2 * self.eventBorderWidth),
    					png=bgpng, flags=BT_SCALE))
    			else:
    				res.append(MultiContentEntryText(
    					pos=(left + xpos, top), size=(ewidth, height),
    					font=1, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER,
    					text="", color=None, color_sel=None,
    					backcolor=backColor, backcolor_sel=backColorSel,
    					border_width=self.eventBorderWidth, border_color=self.borderColor))

    			# Event text.
    			evX = left + xpos + self.eventBorderWidth + self.eventNamePadding
    			evY = top + self.eventBorderWidth
    			evW = ewidth - 2 * (self.eventBorderWidth + self.eventNamePadding)
    			evH = height - 2 * self.eventBorderWidth
    			if evW < infowidth and infoPix is not None:
    				res.append(MultiContentEntryPixmapAlphaBlend(
    					pos=(evX, evY), size=(evW, evH), png=infoPix))
    			else:
    				res.append(MultiContentEntryText(
    					pos=(evX, evY), size=(evW, evH),
    					font=1, flags=int(config.epgselection.grid.event_alignment.value),
    					text=ev[1],
    					color=foreColor, color_sel=foreColorSel,
    					backcolor=backColor, backcolor_sel=backColorSel))

    			# Event borders (graphic mode).
    			for (pixmap, pos, size) in (
    					(bTopPix, (left + xpos, top), (ewidth, self.eventBorderWidth)),
    					(bBottomPix, (left + xpos, height - self.eventBorderWidth), (ewidth, self.eventBorderWidth)),
    					(bLeftPix, (left + xpos, top), (self.eventBorderWidth, height)),
    					(bRightPix, (left + xpos + ewidth - self.eventBorderWidth, top), (self.eventBorderWidth, height)),
    			):
    				if pixmap is not None and self.graphic:
    					res.append(MultiContentEntryPixmapAlphaTest(
    						pos=pos, size=size, png=pixmap, flags=BT_SCALE))

    			# Recording icon.
    			rec_icon_height_cfg = config.epgselection.grid.rec_icon_height.value
    			if ewidth > 23 and rec_icon_height_cfg != "hide":
    				if rec_icon_height_cfg == "middle":
    					RecIconY = top + height // 2 - self.posy
    				elif rec_icon_height_cfg == "top":
    					RecIconY = top + self.gap
    				else:
    					RecIconY = top + height - self.picy - self.gap

    				if clocks is not None:
    					if clock_types in (1, 6, 11):
    						pos = (left + xpos + ewidth - self.picx, RecIconY)
    					elif clock_types in (5, 10, 15):
    						pos = (left + xpos - self.picx - self.posx, RecIconY)
    					else:
    						pos = (left + xpos + ewidth - self.picx - self.posx, RecIconY)
    					res.append(MultiContentEntryPixmapAlphaBlend(
    						pos=pos, size=(self.picx, self.picy), png=clocks))
    				else:
    					pos = (left + xpos + ewidth - self.picx - self.posx, RecIconY)

    				for typeIcon in self.getIcons(clock_types, service, stime):
    					res.append(MultiContentEntryPixmapAlphaBlend(
    						pos=(pos[0] - self.picx - self.gap, pos[1]),
    						size=(self.picx, self.picy), png=typeIcon))

    	return res

    return buildGraphEntry


class GraphPainter:
    """Translate native PLi list state into the approved ATV painter's fields."""
    def __init__(self, listing, api, textures):
        self.native = listing
        self.api = api
        self.graphic = True
        self.listSizeWidth = None
        self.epgConfig = NS(infowidth=NS(value=25))
        self.showServiceNumber = False
        self.serviceNamePadding, self.serviceNumberPadding = 3, 9
        self.eventNamePadding = 3
        self.serviceBorderWidth = self.eventBorderWidth = 1
        self.foreColorServiceNow = self.foreColorService = 0xffffff
        self.backColorServiceNow, self.backColorService = 0x00825f, 0x2d455e
        self.borderColorService = self.borderColor = 0xc0c0c0
        self.foreColor = self.foreColorSelected = 0xffffff
        self.backColor, self.backColorSelected = 0x2d455e, 0xd69600
        for state, colour, selected in (('Now',0x00825f,0xd69600), ('Record',0xd13333,0x9e2626), ('Zap',0x669466,0x436143)):
            setattr(self,'foreColor'+state,0xffffff)
            setattr(self,'foreColor'+state+'Selected',0xffffff)
            setattr(self,'backColor'+state,colour)
            setattr(self,'backColor'+state+'Selected',selected)
        for attr, name in TEXTURES.items():
            setattr(self, attr, api.loadPNG(textures[name]))
        self.icetvicon = None
        self.posx,self.posy,self.picx,self.picy,self.gap = 2,13,25,25,2
        self.clocks = self.selclocks = [None] * 17
        # PLi clock ordering is different. Load ATV clock names explicitly.
        names=('epgclock_add','epgclock_pre','epgclock','epgclock_prepost','epgclock_post',
               'epgclock_add','epgclock_pre','epgclock_zap','epgclock_prepost','epgclock_post',
               'epgclock_add','epgclock_pre','epgclock_zaprec','epgclock_prepost','epgclock_post',
               'epgclock_disabled','epgclock_fallback')
        self.clocks=[api.clock(name) for name in names]
        self.selclocks=[api.clock(name.replace('_pre','_selpre').replace('_post','_selpost')) for name in names]
        self.paint = make_graph_builder(api).__get__(self, type(self))

    def __getattr__(self, name):
        return getattr(self.native, name)

    def recalcEntrySize(self):
        self.native.recalcEntrySize()
        self.listSizeWidth = self.native.l.getItemSize().width()

    def isIceTV(self, service):
        return False

    def getIcons(self, *args):
        return ()

    def getPixmapForEntry(self, service, eventid, start, duration):
        rec=self.native.timer.isInTimer(eventid,start,duration,service)
        if rec is None:
            return None
        types=rec[1]
        if not isinstance(types,(tuple,list)):
            return int(types)  # ATV-compatible timer providers.
        # PLi returns a list of clock indices with extra repeat/combined banks.
        types=[int(value)%15 for value in types]
        for value in (12,2,7):
            if value in types:
                return value
        return types[-1] if types else None


TEXTURES = {
    'nowEvPix':'CurrentEvent.png', 'nowSelEvPix':'SelectedCurrentEvent.png',
    'othEvPix':'OtherEvent.png', 'selEvPix':'SelectedEvent.png',
    'othServPix':'OtherService.png', 'nowServPix':'CurrentService.png',
    'recEvPix':'RecordEvent.png', 'recSelEvPix':'SelectedRecordEvent.png',
    'recordingEvPix':'RecordingEvent.png', 'zapEvPix':'ZapEvent.png',
    'zapSelEvPix':'SelectedZapEvent.png', 'borderTopPix':'BorderTop.png',
    'borderBottomPix':'BorderBottom.png', 'borderLeftPix':'BorderLeft.png',
    'borderRightPix':'BorderRight.png', 'borderSelectedTopPix':'SelectedBorderTop.png',
    'borderSelectedBottomPix':'SelectedBorderBottom.png',
    'borderSelectedLeftPix':'SelectedBorderLeft.png',
    'borderSelectedRightPix':'SelectedBorderRight.png',
    'InfoPix':'information.png', 'selInfoPix':'SelectedInformation.png',
}


def install_painter(listing):
    from enigma import gFont, RT_HALIGN_LEFT, RT_HALIGN_CENTER, RT_VALIGN_CENTER, BT_SCALE, BT_KEEP_ASPECT_RATIO, eSize
    from Components.EpgList import Rect
    from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest, MultiContentEntryPixmapAlphaBlend
    from Components.Renderer.Picon import getPiconName
    from Tools.LoadPixmap import LoadPixmap
    from Tools.Alternatives import CompareWithAlternatives
    from Tools.TextBoundary import getTextBoundarySize
    from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN
    from types import MethodType
    from os.path import join, dirname
    # Owned, pinned fallback PNGs: never depend on the selected image's defaults.
    base=join(dirname(resolveFilename(SCOPE_CURRENT_SKIN,'epg/SelectedEvent.png')),'atv')
    textures={name:join(base,name) for name in set(TEXTURES.values())}
    def loadPNG(path):
        return LoadPixmap(path=path, cached=True)
    alignment=NS(value=RT_HALIGN_LEFT|RT_VALIGN_CENTER)
    cfg=NS(epgselection=NS(grid=NS(servicename_alignment=alignment,event_alignment=alignment,rec_icon_height=NS(value='bottom'))),epg=NS(eit=NS(value=True)))
    def clock(name):
        return LoadPixmap(path=join(base,'clock-'+name+'.png'),cached=True)
    api=NS(**locals())
    api.config=cfg
    api.time=time
    api.getChannelSelectionPiconName=getPiconName
    painter=GraphPainter(listing,api,textures)
    def geometry(component):
        size=component.l.getItemSize();width,height=size.width(),size.height()
        picon_width=max(1,round(60*component.listWidth/1845))
        component.service_rect=Rect(0,0,picon_width,height)
        component.event_rect=Rect(picon_width,0,width-picon_width,height)
        component.picon_size=eSize(max(1,picon_width-2),max(1,height-2))
        painter.listSizeWidth=width
    listing.recalcEntrySize=MethodType(geometry,listing)
    listing.buildEntry=painter.paint
    listing.l.setBuildFunc(painter.paint)
    listing._fullhdglass_atv_painter=painter
    return painter


def make_timeline_builder(api):
    config=api.config
    time=api.time
    localtime=api.localtime
    strftime=api.strftime
    _=api.translate
    RT_HALIGN_LEFT,RT_HALIGN_RIGHT=api.RT_HALIGN_LEFT,api.RT_HALIGN_RIGHT
    RT_VALIGN_CENTER=api.RT_VALIGN_CENTER
    EPG_TYPE_GRAPH,EPG_TYPE_INFOBARGRAPH=0,1
    MAX_TIMELINES=6
    BT_SCALE=api.BT_SCALE
    MultiContentEntryText=api.MultiContentEntryText
    MultiContentEntryPixmapAlphaTest=api.MultiContentEntryPixmapAlphaTest
    def setEntries(self, epgList, timeline_now, time_lines, force):
    	event_rect = epgList.getEventRect()
    	time_epoch = epgList.getTimeEpoch()
    	time_base = epgList.getTimeBase()

    	if event_rect is None or time_epoch is None or time_base is None:
    		return

    	alignment = (RT_HALIGN_RIGHT if self.timelineAlign.lower() == "right" else RT_HALIGN_LEFT) | RT_VALIGN_CENTER

    	eventLeft = event_rect.left()
    	res = [None]

    	if self.time_base != time_base or self.time_epoch != time_epoch or force:
    		service_rect = epgList.getServiceRect()
    		time_steps = 60 if time_epoch > 180 else 30
    		num_lines = time_epoch // time_steps
    		incWidth = event_rect.width() / num_lines
    		timeStepsCalc = time_steps * 60

    		nowTime = localtime(time())
    		begTime = localtime(time_base)
    		ServiceWidth = service_rect.width()
    		if nowTime[2] != begTime[2]:
    			if ServiceWidth > 179:
    				datestr = strftime(_("%A %d %B"), localtime(time_base))
    			elif ServiceWidth > 139:
    				datestr = strftime(_("%a %d %B"), localtime(time_base))
    			elif ServiceWidth > 129:
    				datestr = strftime(_("%a %d %b"), localtime(time_base))
    			elif ServiceWidth > 119:
    				datestr = strftime(_("%a %d"), localtime(time_base))
    			elif ServiceWidth > 109:
    				datestr = strftime(_("%A"), localtime(time_base))
    			else:
    				datestr = strftime(_("%a"), localtime(time_base))
    		else:
    			datestr = str(_("Today"))

    		foreColor = self.foreColor
    		backColor = self.backColor
    		bgpng = self.TlDate
    		if bgpng is not None and self.graphic:
    			backColor = None
    			res.append(MultiContentEntryPixmapAlphaTest(
    				pos=(0, 0), size=(service_rect.width(), self.listHeight),
    				png=bgpng, flags=BT_SCALE))
    		else:
    			res.append(MultiContentEntryText(
    				pos=(0, 0), size=(service_rect.width(), self.listHeight),
    				color=foreColor, backcolor=backColor,
    				border_width=self.borderWidth, border_color=self.borderColor))

    		res.append(MultiContentEntryText(
    			pos=(5, 0), size=(service_rect.width() - 15, self.listHeight),
    			font=0, flags=alignment,
    			text=_(datestr), color=foreColor, backcolor=backColor))

    		bgpng = self.TlTime
    		xpos = 0
    		if bgpng is not None and self.graphic:
    			backColor = None
    			res.append(MultiContentEntryPixmapAlphaTest(
    				pos=(service_rect.width(), 0),
    				size=(event_rect.width(), self.listHeight),
    				png=bgpng, flags=BT_SCALE))
    		else:
    			res.append(MultiContentEntryText(
    				pos=(service_rect.width(), 0),
    				size=(event_rect.width(), self.listHeight),
    				color=foreColor, backcolor=backColor,
    				border_width=self.borderWidth, border_color=self.borderColor))

    		use24h = (
    			(self.type == EPG_TYPE_GRAPH and config.epgselection.grid.timeline24h.value) or
    			(self.type == EPG_TYPE_INFOBARGRAPH and config.epgselection.infobar.timeline24h.value)
    		)
    		for x in range(num_lines):
    			ttime = localtime(time_base + x * timeStepsCalc)
    			if use24h:
    				timetext = strftime("%H:%M", ttime)
    			else:
    				h = int(strftime("%H", ttime))
    				timetext = strftime("%-I:%M", ttime) + (_("pm") if h >= 12 else _("am"))
    			res.append(MultiContentEntryText(
    				pos=(service_rect.width() + xpos, 0),
    				size=(incWidth, self.listHeight),
    				font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER,
    				text=timetext, color=foreColor, backcolor=backColor))
    			line = time_lines[x]
    			old_pos = line.position
    			line.setPosition(xpos + eventLeft, old_pos[1])
    			line.visible = True
    			xpos += incWidth
    		for x in range(num_lines, MAX_TIMELINES):
    			time_lines[x].visible = False
    		self.l.setList([res])
    		self.time_base = time_base
    		self.time_epoch = time_epoch

    	now = time()
    	if time_base <= now < (time_base + time_epoch * 60):
    		xpos = int((((now - time_base) * event_rect.width()) / (time_epoch * 60))
    					- (timeline_now.instance.size().width() / 2))
    		old_pos = timeline_now.position
    		new_pos = (xpos + eventLeft, old_pos[1])
    		if old_pos != new_pos:
    			timeline_now.setPosition(new_pos[0], new_pos[1])
    		timeline_now.visible = True
    	else:
    		timeline_now.visible = False
    return setEntries


def install_timeline(component, painter):
    from time import localtime, strftime
    from enigma import RT_HALIGN_RIGHT
    api=NS(**vars(painter.api))
    api.localtime,api.strftime=localtime,strftime
    api.translate=lambda value:value
    api.RT_HALIGN_RIGHT=RT_HALIGN_RIGHT
    api.config.epgselection.grid.timeline24h=NS(value=True)
    component.type=0
    component.graphic=True
    component.timelineAlign='left'
    component.borderWidth=1
    component.borderColor=component.backColor=0
    component.foreColor=0xffc000
    from os.path import join, dirname
    base=dirname(next(iter(painter.api.textures.values())))
    component.TlDate=api.loadPNG(join(base,'TimeLineDate.png'))
    component.TlTime=api.loadPNG(join(base,'TimeLineTime.png'))
    return make_timeline_builder(api).__get__(component,type(component))
