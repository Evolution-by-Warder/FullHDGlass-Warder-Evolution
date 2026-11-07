"""Default ChannelSelection: pixel-fit event titles without altering native bars.

The legacy native service-list renderer has no per-event painter clip. When all
required Enigma2 APIs are present, suppress only its unbounded event text and
repaint those titles inside the reserved field. Service names, picons, progress
bars, selection and fonts remain owned by the image. On unsupported images the
native renderer is left completely unchanged.
"""
from Components.Renderer.Renderer import Renderer
from Components.config import config
from enigma import eCanvas, eLabel, eTimer, eRect, eSize, RT_VALIGN_CENTER, RT_HALIGN_LEFT
from skin import parseColor
from Plugins.Extensions.setupGlass17.warderEpgTextFit import fit_title_to_width


class WarderChannelEpgClip(Renderer):
    GUI_WIDGET = eCanvas

    def __init__(self):
        Renderer.__init__(self)
        self._timer = eTimer()
        self._connection = None
        try:
            self._connection = self._timer.timeout.connect(self.refresh)
        except AttributeError:
            self._timer.callback.append(self.refresh)
        self._label = None
        self._component = None
        self._native_hidden = False
        self._last = None
        self._transparent = parseColor("#ff000000")

    def postWidgetCreate(self, instance):
        self._label = eLabel(instance)
        # Measure actual glyph widths with a large, non-wrapping label.
        # A zero-sized helper could silently report false-fitting long text.
        self._label.setNoWrap(1)
        self._label.resize(eSize(4096, 120))
        self._label.hide()
        self._last = None
        self._timer.start(250, True)

    def preWidgetRemove(self, instance):
        self._timer.stop()
        self._restore_native()
        self._label = None

    def changed(self, what):
        if self.instance:
            self._last = None
            self.refresh()

    def _restore_native(self):
        component = self._component
        if self._native_hidden and component is not None:
            try:
                component.l.setElementFont(component.l.celServiceInfo, component.ServiceInfoFont)
            except (AttributeError, TypeError, RuntimeError):
                pass
        self._native_hidden = False
        self._component = None

    def _find_component(self):
        try:
            from Screens.InfoBar import InfoBar
            screen = InfoBar.instance.servicelist
            component = screen["list"]
            if not hasattr(component, "ServiceInfoFont"):
                return None
            if not hasattr(component, "ServiceNameFont"):
                return None
            if not hasattr(component.l, "celServiceInfo"):
                return None
            if not hasattr(component.l, "getList"):
                return None
            if component.instance is None or not hasattr(component.instance, "getTopIndex"):
                return None
            return component
        except (AttributeError, KeyError, TypeError):
            return None

    def _name_and_event(self, center, ref):
        try:
            if ref.flags & 7:  # marker/directory and non-service entries
                return "", ""
            info = center.info(ref)
            if info is None:
                return "", ""
            name = info.getName(ref) or ""
            event = info.getEvent(ref)
            return name, (event.getEventName() or "") if event else ""
        except (AttributeError, RuntimeError, TypeError):
            return "", ""

    def _draw_rows(self, component):
        from enigma import eServiceCenter
        rows = component.getList()
        if rows is None:
            return False
        top = component.instance.getTopIndex()
        if top < 0:
            return False
        selected = component.instance.getCurrentIndex()
        width = component.instance.size().width()
        height = component.instance.size().height()
        row_height = int(component.ItemHeight)
        if row_height < 10 or width < 120 or height < row_height:
            return False
        # The native progressbar remains at the far-right edge.
        bar_left = width - int(component.listMarginRight) - int(component.progressBarWidth)
        available_rows = min(len(rows) - top, (height + row_height - 1) // row_height)
        if available_rows < 0 or bar_left < 100:
            return False
        font = component.ServiceInfoFont
        name_font = component.ServiceNameFont
        self._label.setFont(font)
        center = eServiceCenter.getInstance()
        drawing = []
        for row_index in range(available_rows):
            index = top + row_index
            ref = rows[index]
            name, title = self._name_and_event(center, ref)
            if not title:
                continue
            # Service names remain native; use the image's actual name font.
            self._label.setFont(name_font)
            self._label.setText(name)
            name_width = self._label.calculateSize().width()
            # The legacy row reserves its number/picon column before the name.
            picon_width = int((row_height + 2 * int(config.usage.servicelist_picon_downsize.value)) *
                              int(config.usage.servicelist_picon_ratio.value) / 100)
            start = max(0, int(component.listMarginLeft) + picon_width +
                        2 * int(component.itemsDistances) + name_width)
            end = bar_left - max(12, int(component.fieldMargins))
            remaining = end - start
            if remaining <= 0:
                continue
            self._label.setFont(font)
            def measure(text):
                self._label.setText(text)
                return self._label.calculateSize().width()
            fitted = fit_title_to_width(title, remaining, measure)
            if fitted:
                drawing.append((start, row_index * row_height, remaining, row_height,
                                fitted, index == selected))
        if not drawing:
            return False
        signature = (top, selected, row_height, width, height, tuple(drawing))
        if signature == self._last:
            return True
        normal = parseColor(config.plugins.setupGlass17.par109.value)
        highlighted = parseColor(config.plugins.setupGlass17.par110.value)
        self.instance.clear(self._transparent)
        for x, y, w, h, value, is_selected in drawing:
            self.instance.writeText(eRect(x, y, w, h), highlighted if is_selected else normal,
                                    self._transparent, font, value,
                                    RT_HALIGN_LEFT | RT_VALIGN_CENTER)
        self.instance.flush()
        self._last = signature
        return True

    def refresh(self):
        try:
            if not self.instance or not self._label:
                return
            component = self._find_component()
            if component is None:
                self._restore_native()
                return
            if component is not self._component:
                self._restore_native()
                self._component = component
                self._last = None
            # Draw first; hide the C++ event text only after a complete frame
            # has been produced, so unsupported environments do not go blank.
            if not self._draw_rows(component):
                self._restore_native()
                return
            if not self._native_hidden:
                try:
                    component.l.setElementFont(component.l.celServiceInfo, None)
                except (AttributeError, RuntimeError, TypeError):
                    self.instance.clear(self._transparent)
                    self.instance.flush()
                    self._component = None
                    return
                self._native_hidden = True
                # Force the native list to repaint without its unbounded EPG
                # text, including the selected and non-selected rows.
                self._last = None
                try:
                    component.instance.invalidate()
                except (AttributeError, TypeError, RuntimeError):
                    pass
        except (AttributeError, RuntimeError, TypeError, ValueError, IndexError):
            self._restore_native()
            if self.instance:
                self.instance.clear(self._transparent)
                self.instance.flush()
        finally:
            if self.instance:
                self._timer.start(250, True)
