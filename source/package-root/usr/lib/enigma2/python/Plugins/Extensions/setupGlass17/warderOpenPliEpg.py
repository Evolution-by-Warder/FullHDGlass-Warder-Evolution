"""FullHDGlass graphical guide using OpenPLi's native services/timer controller.

Only the active FullHDGlass skin is dispatched to the owned subclass. Native
zap, bouquet, selection and recording methods stay with OpenPLi. No image files
or saved graphical-EPG preferences are changed.
"""
from types import MethodType


def fit_graph_rows(listing, font_offset, size_class):
    """Use complete rows; larger user fonts reduce rows instead of clipping."""
    height, width = listing.listHeight, listing.listWidth
    if not listing.instance or not height or not width:
        return
    font = max(1, int(listing.entryFontSize) + int(font_offset))
    minimum = font + max(4, round(font / 5))
    rows = max(1, min(15, int(height) // minimum))
    row_height = max(1, int(height) // rows)
    listing.instance.resize(size_class(int(width), row_height * rows))
    listing.l.setItemHeight(row_height)


def open_search(session, event, translate):
    if event is None:
        return
    try:
        from Plugins.Extensions.EPGSearch.EPGSearch import EPGSearch
    except ImportError:
        from Screens.MessageBox import MessageBox
        return session.open(MessageBox, translate("EPG Search is not installed."),
                            MessageBox.TYPE_INFO, timeout=6)
    return session.open(EPGSearch, event.getEventName() or "", False)


def install(graph_module, graph_plugin, info_bar_epg, config, static_text,
            action_map, size_class, program_info, translate, search=open_search,
            report_error=None, paint_installer=None, timeline_installer=None):
    """Install a skin-scoped dispatch, including the standard Multi EPG entry."""
    if getattr(graph_plugin, '_fullhdglass_epg_installed', False):
        return True
    native = getattr(graph_module, 'GraphMultiEPG', None)
    original_open = getattr(info_bar_epg, 'openMultiServiceEPG', None)
    required = ('onSelectionChanged', 'timerAdd', 'enterDateTime', 'onCreate',
                'zapTo', 'preview', 'eventSelected', 'setTitle')
    if (native is None or not callable(original_open) or
            not callable(getattr(graph_plugin, 'main', None)) or
            any(not callable(getattr(native, key, None)) for key in required)):
        return False
    if paint_installer is None:
        from .warderAtvEpgPaint import install_painter, install_timeline
        paint_installer, timeline_installer = install_painter, install_timeline
    original_factory = graph_plugin.GraphMultiEPG
    report_error = report_error or (lambda message: None)

    def active():
        return config.skin.primary_skin.value == 'hd_glass17/skin.xml'

    class FullHDGlassOpenPLiGraphEPG(native):
        def __init__(self, *args, **kwargs):
            self._warderProgramInfoOpen = False
            native.__init__(self, *args, **kwargs)
            self.skinName = ['FullHDGlassOpenPLiGraphEPG', 'GraphMultiEPG']
            for colour in ('red', 'green', 'yellow', 'blue'):
                self['warder_key_' + colour] = static_text('')
            self['warderEpgActions'] = action_map(self, ['GMEPGSelectActions'], {
                'red': (self.warderProgramInfo, translate('PROGRAM INFO')),
                'yellow': (self.enterDateTime, translate('Goto Date/Time')),
                'blue': (self.warderSearch, translate('EPG Search')),
            }, -2)
            # HELP must describe the active colour actions, not also advertise
            # the native red-zap/yellow-mode/blue-primetime bindings underneath.
            native_actions = self['gmepgactions']
            for index, record in enumerate(self.helpList):
                if len(record) == 3 and record[0] is native_actions:
                    owner, context, entries = record
                    self.helpList[index] = (owner, context, [entry for entry in entries
                                            if entry[0] not in ('red', 'yellow', 'blue')])
            self._fit_native_list()
            self._sync_labels()
            self.setTitle('')
            self.onClose.append(self._closed)

        def setTitle(self, title, *args, **kwargs):
            return native.setTitle(self, '', *args, **kwargs)

        def _closed(self):
            self._warderProgramInfoOpen = False

        def _fit_native_list(self):
            listing = self['list']
            painter = paint_installer(listing)
            # Default to the approved three-hour span without changing PLi settings.
            listing.time_epoch = 180
            original_mode = listing.setShowServiceMode
            timeline = self['timeline_text']
            original_skin = timeline.applySkin
            original_entries = timeline_installer(timeline, painter) if timeline_installer else timeline.setEntries

            def rows(component):
                offset = config.misc.graph_mepg.ev_fontsize.getValue()
                fit_graph_rows(component, offset, size_class)
                component.recalcEntrySize()
                return None

            def mode(component, requested):
                return original_mode('picon')

            def timeline_skin(component, desktop, screen):
                result = original_skin(desktop, screen)
                if component.instance:
                    component.listHeight = component.instance.size().height()
                    component.listWidth = component.instance.size().width()
                    component.l.setItemHeight(component.listHeight)
                return result

            def entries(component, epg_list, now, lines, force):
                result = original_entries(epg_list, now, lines, force)
                for line in lines:
                    line.visible = False
                return result

            listing.setItemsPerPage = MethodType(rows, listing)
            listing.setShowServiceMode = MethodType(mode, listing)
            timeline.applySkin = MethodType(timeline_skin, timeline)
            timeline.setEntries = MethodType(entries, timeline)

        def updEpoch(self, minutes):
            self['list'].setEpoch(minutes)
            self.moveTimeLines(True)

        def onSetupClose(self, ignore=-1):
            epoch = self['list'].time_epoch
            result = native.onSetupClose(self, ignore)
            self['list'].setEpoch(epoch)
            self.moveTimeLines(True)
            return result

        def _sync_labels(self):
            if 'warder_key_red' not in self:
                return
            self['warder_key_red'].setText(translate('PROGRAM INFO'))
            self['warder_key_green'].setText(self['key_green'].getText())
            self['warder_key_yellow'].setText(translate('Goto Date/Time'))
            self['warder_key_blue'].setText(translate('EPG Search'))

        def onSelectionChanged(self):
            result = native.onSelectionChanged(self)
            self._sync_labels()
            return result

        def warderProgramInfo(self):
            if self._warderProgramInfoOpen:
                return 1
            current = self['list'].getCurrent()
            event, service = current if current else (None, None)
            if event is None:
                return 1
            self._warderProgramInfoOpen = True
            try:
                self.showhideWindow(True)
                self.session.openWithCallback(self.warderProgramInfoClosed,
                                              program_info, event, service)
            except Exception as error:
                self._warderProgramInfoOpen = False
                report_error('FullHDGlass OpenPLi programme info: %s' % error)
            # OpenPLi's C++ action dispatcher consumes only integer results.
            # Returning the opened Screen would also run native red/zap below.
            return 1

        def warderProgramInfoClosed(self, action=None):
            self._warderProgramInfoOpen = False
            if action == 'green':
                return self.timerAdd()
            if action == 'yellow':
                return self.enterDateTime()
            if action == 'blue':
                return self.warderSearch()

        def warderSearch(self):
            current = self['list'].getCurrent()
            event = current[0] if current else None
            search(self.session, event, translate)
            return 1

    def graph_factory(*args, **kwargs):
        if active():
            return FullHDGlassOpenPLiGraphEPG(*args, **kwargs)
        return original_factory(*args, **kwargs)

    def open_multi(self, withCallback=True):
        # Preserve the native nested-event-view callback stack. The ordinary
        # Multi EPG/hotkey entry opens the same owned graphical guide as the menu.
        if active() and withCallback:
            return graph_plugin.main(self.session, servicelist=self.servicelist)
        return original_open(self, withCallback)

    graph_plugin.GraphMultiEPG = graph_factory
    info_bar_epg.openMultiServiceEPG = open_multi
    graph_plugin._fullhdglass_epg_installed = True
    return True
