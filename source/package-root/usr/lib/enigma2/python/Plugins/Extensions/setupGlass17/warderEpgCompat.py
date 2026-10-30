"""FullHDGlass graphical EPG integration for legacy and refactored OpenATV.

No receiver diagnostics, workers or timers. Bind the real graphical controller,
leave other skins/EPG screens to their native handlers, and keep caption sources
separate from image-owned colour labels.
"""

def configure_graph(config):
    epg = getattr(config, "epgselection", None)
    if epg is None:
        return
    grid = getattr(epg, "grid", None)
    if grid is not None:
        for name, value in (("servicetitle_mode", "picon"), ("piconwidth", 60),
                            ("btn_red", "openEventView"), ("btn_green", "addEditTimer"),
                            ("btn_yellow", "enterDateTime"), ("btn_blue", "openEPGSearch")):
            item = getattr(grid, name, None)
            if item is not None:
                item.value = value


def install(epg_module, config, StaticText, translate, program_info, report_error=None, info_bar=None):
    WarderEPGSelection = getattr(epg_module, "EPGSelectionGrid", None)
    modern = WarderEPGSelection is not None
    if not modern:
        WarderEPGSelection = getattr(epg_module, "EPGSelection", None)
    if WarderEPGSelection is None:
        return False
    if WarderEPGSelection.__dict__.get("_warderEpgCompatInstalled", False):
        return True
    _warderUiText = translate
    WarderProgramInfo = program_info
    Writelog = report_error or (lambda message: None)
    originals = {}
    for colour in ("red", "green", "yellow", "blue"):
        name = "_btn_" + colour if modern else colour + "ButtonPressed"
        method = getattr(WarderEPGSelection, name, None)
        if not callable(method):
            return False  # Validate all required entry points before mutating the class.
        originals[colour] = method
    WarderEPGSelection_setTitle = WarderEPGSelection.setTitle
    WarderEPGSelection_init = WarderEPGSelection.__init__
    WarderEPGSelection_RefreshColouredKeys = getattr(WarderEPGSelection, "RefreshColouredKeys", None)
    native_update_text = getattr(WarderEPGSelection, "_updateButtonText", None)

    def _warderGraphicalEPGPIG(self):
        names = getattr(self, "skinName", None)
        own = names == "GraphicalEPGPIG" or isinstance(names, (list, tuple)) and "GraphicalEPGPIG" in names
        return config.skin.primary_skin.value == "hd_glass17/skin.xml" and own

    def _warderShortColour(self):
        if not _warderGraphicalEPGPIG(self):
            return False
        return not (modern and getattr(getattr(info_bar, "instance", None), "LongButtonPressed", False))

    def _warderGraphicalEPGLabels(self):
        if not _warderGraphicalEPGPIG(self):
            return
        for key, text in (("warder_key_red", _warderUiText("PROGRAM INFO")),
                          ("warder_key_green", _warderUiText("Add Timer")),
                          ("warder_key_yellow", _warderUiText("Goto Date/Time")),
                          ("warder_key_blue", _warderUiText("EPG Search"))):
            if key not in self:
                self[key] = StaticText("")
            self[key].setText(text)

    def warderEPGSelectionSetTitle(self, title, *args, **kwargs):
        if _warderGraphicalEPGPIG(self):
            title = ""
        return WarderEPGSelection_setTitle(self, title, *args, **kwargs)

    def warderEPGSelectionInit(self, *args, **kwargs):
        WarderEPGSelection_init(self, *args, **kwargs)
        _warderGraphicalEPGLabels(self)
        if _warderGraphicalEPGPIG(self):
            self.setTitle("")

    def warderEPGSelectionRefreshColouredKeys(self, *args, **kwargs):
        result = WarderEPGSelection_RefreshColouredKeys(self, *args, **kwargs)
        _warderGraphicalEPGLabels(self)
        return result

    def warderEPGSelectionUpdateButtonText(self, *args, **kwargs):
        result = native_update_text(self, *args, **kwargs)
        _warderGraphicalEPGLabels(self)
        return result

    def _close_native_event_view(self):
        if modern:
            close = getattr(self, "closeEventViewDialog", None)
            if callable(close):
                close()

    def warderProgramInfoClosed(self, action=None):
        self._warderProgramInfoOpen = False
        if action == "green": return self.RecordTimerQuestion(True)
        if action == "yellow": return self.enterDateTime()
        if action == "blue": return self.openEPGSearch()

    # Never fall through to OpenATV/legacy info/CSFD handlers.
    def warderEPGSelectionRedButtonPressed(self):
        if _warderShortColour(self):
            if getattr(self, "_warderProgramInfoOpen", False):
                return None
            _close_native_event_view(self)
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
            except Exception as error:
                Writelog("WarderProgramInfo open: %s" % error)
            return None
        return originals["red"](self)

    def warderEPGSelectionGreenButtonPressed(self):
        if _warderShortColour(self):
            _close_native_event_view(self)
            return self.RecordTimerQuestion(True)
        return originals["green"](self)

    def warderEPGSelectionYellowButtonPressed(self):
        if _warderShortColour(self):
            _close_native_event_view(self)
            return self.enterDateTime()
        return originals["yellow"](self)

    def warderEPGSelectionBlueButtonPressed(self):
        if _warderShortColour(self):
            _close_native_event_view(self)
            return self.openEPGSearch()
        return originals["blue"](self)

    WarderEPGSelection.setTitle = warderEPGSelectionSetTitle
    WarderEPGSelection.__init__ = warderEPGSelectionInit
    if callable(WarderEPGSelection_RefreshColouredKeys):
        WarderEPGSelection.RefreshColouredKeys = warderEPGSelectionRefreshColouredKeys
    if callable(native_update_text):
        WarderEPGSelection._updateButtonText = warderEPGSelectionUpdateButtonText
    WarderEPGSelection.warderProgramInfoClosed = warderProgramInfoClosed
    WarderEPGSelection.redButtonPressed = warderEPGSelectionRedButtonPressed
    WarderEPGSelection.greenButtonPressed = warderEPGSelectionGreenButtonPressed
    WarderEPGSelection.yellowButtonPressed = warderEPGSelectionYellowButtonPressed
    WarderEPGSelection.blueButtonPressed = warderEPGSelectionBlueButtonPressed
    if modern:
        WarderEPGSelection._btn_red = warderEPGSelectionRedButtonPressed
        WarderEPGSelection._btn_green = warderEPGSelectionGreenButtonPressed
        WarderEPGSelection._btn_yellow = warderEPGSelectionYellowButtonPressed
        WarderEPGSelection._btn_blue = warderEPGSelectionBlueButtonPressed
    WarderEPGSelection._warderEpgCompatInstalled = True
    return True
