WarderEPGSelection_setTitle = None
try:
	from Screens.EpgSelection import EPGSelection as WarderEPGSelection
	WarderEPGSelection_setTitle = WarderEPGSelection.setTitle
	def warderEPGSelectionSetTitle(self, title, *args, **kwargs):
		if config.skin.primary_skin.value == "hd_glass17/skin.xml" and getattr(self, "skinName", None) == "GraphicalEPGPIG":
			title = ""
		return WarderEPGSelection_setTitle(self, title, *args, **kwargs)
	WarderEPGSelection.setTitle = warderEPGSelectionSetTitle
	def _warderGraphicalEPGPIG(self):
		return config.skin.primary_skin.value == "hd_glass17/skin.xml" and getattr(self, "skinName", None) == "GraphicalEPGPIG"

	def _warderGraphicalEPGLabels(self):
		if not _warderGraphicalEPGPIG(self):
			return
		for key, text in (("warder_key_red", _warderUiText("PROGRAM INFO")), ("warder_key_green", _warderUiText("Add Timer")), ("warder_key_yellow", _warderUiText("Goto Date/Time")), ("warder_key_blue", _warderUiText("EPG Search"))):
			try:
				self[key].setText(text)
			except Exception:
				pass

	WarderEPGSelection_init = WarderEPGSelection.__init__
	def warderEPGSelectionInit(self, *args, **kwargs):
		WarderEPGSelection_init(self, *args, **kwargs)
		if _warderGraphicalEPGPIG(self):
			for key in ("warder_key_red", "warder_key_green", "warder_key_yellow", "warder_key_blue"):
				self[key] = StaticText("")
		_warderGraphicalEPGLabels(self)
	WarderEPGSelection.__init__ = warderEPGSelectionInit

	# OpenATV refreshes StaticText colour-key sources after construction. Re-apply
	# the FullHDGlass labels afterwards so the visible label always matches the handler.
	WarderEPGSelection_RefreshColouredKeys = WarderEPGSelection.RefreshColouredKeys
	def warderEPGSelectionRefreshColouredKeys(self, *args, **kwargs):
		result = WarderEPGSelection_RefreshColouredKeys(self, *args, **kwargs)
		_warderGraphicalEPGLabels(self)
		return result
	WarderEPGSelection.RefreshColouredKeys = warderEPGSelectionRefreshColouredKeys

	WarderEPGSelection_redButtonPressed = WarderEPGSelection.redButtonPressed
	def warderProgramInfoClosed(self, action=None):
		self._warderProgramInfoOpen = False
		if action == "green": return self.RecordTimerQuestion(True)
		if action == "yellow": return self.enterDateTime()
		if action == "blue": return self.openEPGSearch()
	WarderEPGSelection.warderProgramInfoClosed = warderProgramInfoClosed

	def warderEPGSelectionRedButtonPressed(self):
		if _warderGraphicalEPGPIG(self):
			# One physical RED press can be delivered more than once by the EPG key path.
			# Never stack two Program Info screens: the first close must reveal the EPG.
			if getattr(self, "_warderProgramInfoOpen", False):
				return None
			# Warder contract: RED in our graphical EPG has exactly one destination:
			# the local PROGRAM INFO screen for the currently selected EPG event.
			# Never fall through to OpenATV/legacy info/CSFD handlers.
			try:
				active = getattr(self, "activeList", 1)
				listing = self["list%s" % active]
				cur = listing.getCurrent()
				event = cur[0] if cur else None
				service = cur[1] if cur and len(cur) > 1 else None
				if event is not None:
					self._warderProgramInfoOpen = True
					try:
						return self.session.openWithCallback(self.warderProgramInfoClosed, WarderProgramInfo, event, service)
					except Exception:
						self._warderProgramInfoOpen = False
						raise
			except Exception as e:
				Writelog("WarderProgramInfo open: %s" % e)
			return None
		return WarderEPGSelection_redButtonPressed(self)
	WarderEPGSelection.redButtonPressed = warderEPGSelectionRedButtonPressed

	WarderEPGSelection_greenButtonPressed = WarderEPGSelection.greenButtonPressed
	def warderEPGSelectionGreenButtonPressed(self):
		if _warderGraphicalEPGPIG(self):
			return self.RecordTimerQuestion(True)
		return WarderEPGSelection_greenButtonPressed(self)
	WarderEPGSelection.greenButtonPressed = warderEPGSelectionGreenButtonPressed

	WarderEPGSelection_yellowButtonPressed = WarderEPGSelection.yellowButtonPressed
	def warderEPGSelectionYellowButtonPressed(self):
		if _warderGraphicalEPGPIG(self):
			return self.enterDateTime()
		return WarderEPGSelection_yellowButtonPressed(self)
	WarderEPGSelection.yellowButtonPressed = warderEPGSelectionYellowButtonPressed

	WarderEPGSelection_blueButtonPressed = WarderEPGSelection.blueButtonPressed
	def warderEPGSelectionBlueButtonPressed(self):
		if _warderGraphicalEPGPIG(self):
			return self.openEPGSearch()
		return WarderEPGSelection_blueButtonPressed(self)
	WarderEPGSelection.blueButtonPressed = warderEPGSelectionBlueButtonPressed

except Exception:
	pass

