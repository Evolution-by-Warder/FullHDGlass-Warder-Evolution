"""Default ChannelSelection: pixel-fit event titles without altering native bars.

The legacy native service-list renderer has no per-event painter clip. When all
required Enigma2 APIs are present, suppress only its unbounded event text and
repaint those titles inside the reserved field. Service names, picons, progress
bars, selection and fonts remain owned by the image. On unsupported images the
native renderer is left completely unchanged.
"""
from time import time
from Components.Renderer.Renderer import Renderer
from Components.config import config
from enigma import eCanvas, eLabel, eTimer, eRect, eSize, gFont, RT_VALIGN_CENTER, RT_HALIGN_LEFT
from skin import parseColor
from Plugins.Extensions.setupGlass17.warderEpgTextFit import fit_title_to_width


def scroll_title_window(title, width, measure, pixel_offset):
    """Return a width-bounded moving title window without painting into native cells.

    A canvas text rectangle cannot safely extend past the event field: such an
    extension would overwrite the native station name or progress bar. Scroll
    at glyph boundaries while retaining a pixel-clock for consistent speed.
    """
    if not title or width <= 0:
        return ""
    if measure(title) <= width:
        return title
    if pixel_offset <= 0:
        return fit_title_to_width(title, width, measure)
    lo, hi = 0, len(title)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if measure(title[:mid]) <= pixel_offset:
            lo = mid
        else:
            hi = mid - 1
    # A moving window must reveal the real suffix, not keep inserting an
    # ellipsis.  Use measured glyph boundaries; the event field owns clipping.
    suffix = title[lo:]
    if measure(suffix) <= width:
        return suffix
    lo, hi = 0, len(suffix)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if measure(suffix[:mid]) <= width:
            lo = mid
        else:
            hi = mid - 1
    return suffix[:lo]


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
        self._scroll_started = time()
        self._scroll_selected = None
        # SWIG bindings do not universally accept None for gFont*; a 1px
        # temporary font is ABI-compatible and keeps original user fonts
        # untouched, restored when the overlay is removed.
        self._quiet_font = gFont("Regular", 1)
        self._transparent = parseColor("#ff000000")
        self._opaque_black = parseColor("#00000000")
        self._progress_border = parseColor("#dfdfdf")
        self._diag_seen = set()
        # Optional receiver-QA dimensions; absent in production XML.
        self._warder_bar_width = None
        self._warder_test_marker = False

    def _diag(self, key, details=""):
        # TEST59 only: bounded, local status events; never include EPG titles.
        # Silently skip unavailable/readonly /tmp; diagnosis must not crash GUI.
        try:
            if key in self._diag_seen or len(self._diag_seen) >= 32:
                return
            self._diag_seen.add(key)
            with open("/tmp/warder-epg-clip-test59.log", "a") as output:
                output.write("%s %s\n" % (key, details))
        except (OSError, AttributeError, TypeError, ValueError):
            pass

    def applySkin(self, desktop, parent):
        # Private, per-overlay receiver QA flags must never be forwarded to
        # generic Enigma2 skin attribute processing as unknown properties.
        passthrough = []
        for key, value in (self.skinAttributes or []):
            if key == "warderProgressWidth":
                try:
                    self._warder_bar_width = max(1, int(value))
                except (ValueError, TypeError):
                    self._warder_bar_width = None
            elif key == "warderTestMarker":
                self._warder_test_marker = value == "1"
            else:
                passthrough.append((key, value))
        self.skinAttributes = passthrough
        self._diag("apply_skin_flags", "width=%s marker=%s" %
                   (self._warder_bar_width, self._warder_test_marker))
        return Renderer.applySkin(self, desktop, parent)

    def postWidgetCreate(self, instance):
        # eCanvas needs an allocated backing pixmap, not only GUI geometry.
        size = next((v for k, v in (self.skinAttributes or []) if k == "size"), None)
        if size:
            width, height = (int(v) for v in size.split(","))
            if width > 0 and height > 0:
                instance.setSize(eSize(width, height))
        self._diag("canvas_created", "allocated=%s barOverride=%s marker=%s" %
                   (bool(size), self._warder_bar_width, self._warder_test_marker))
        self._label = eLabel(instance)
        # Measure actual glyph widths with a large, non-wrapping label.
        # A zero-sized helper could silently report false-fitting long text.
        self._label.setNoWrap(1)
        self._label.resize(eSize(4096, 120))
        self._label.hide()
        self._last = None
        self._scroll_started = time()
        self._scroll_selected = None
        self._timer.start(55, True)

    def preWidgetRemove(self, instance):
        self._timer.stop()
        self._restore_native()
        self._label = None

    def changed(self, what):
        if self.instance:
            self._last = None
            self._scroll_started = time()
            self.refresh()

    def _restore_native(self):
        component = self._component
        if self._native_hidden:
            self._diag("native_font_restoring")
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
                self._diag("no_service_info_font")
                return None
            if not hasattr(component, "ServiceNameFont"):
                self._diag("no_service_name_font")
                return None
            if not hasattr(component.l, "celServiceInfo"):
                self._diag("no_native_event_cell")
                return None
            if not hasattr(component.l, "getList"):
                self._diag("no_native_get_list")
                return None
            if component.instance is None or not hasattr(component.instance, "getTopIndex"):
                self._diag("no_native_top_index")
                return None
            self._diag("native_component_found", "component=%s" % type(component).__name__)
            return component
        except (AttributeError, KeyError, TypeError) as exc:
            self._diag("native_lookup_error", "%s" % type(exc).__name__)
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

    def _progress_fraction(self, center, ref):
        try:
            event = center.info(ref).getEvent(ref)
            if event is None:
                return None
            duration = int(event.getDuration())
            if duration <= 0:
                return None
            elapsed = time() - int(event.getBeginTime())
            return int(max(0.0, min(1.0, elapsed / float(duration))) * 100) / 100.0
        except (AttributeError, RuntimeError, TypeError, ValueError, ZeroDivisionError):
            return None

    def _draw_progress(self, x, y, width, row_height, elapsed):
        # Match the native 2px border and 6px interior; opaque underlay
        # prevents the inherited native event text showing through the bar.
        top = y + (row_height - 10) // 2
        self.instance.fillRect(eRect(x, top, width, 10), self._opaque_black)
        b = self._progress_border
        self.instance.fillRect(eRect(x, top, width, 2), b)
        self.instance.fillRect(eRect(x, top + 8, width, 2), b)
        self.instance.fillRect(eRect(x, top + 2, 2, 6), b)
        self.instance.fillRect(eRect(x + width - 2, top + 2, 2, 6), b)
        filled = int(max(0, width - 4) * elapsed)
        # Draw only 8 gradient segments to keep timer CPU use low.
        for segment in range(8):
            a = (filled * segment) // 8
            z = (filled * (segment + 1)) // 8
            if z <= a:
                continue
            t = ((a + z) / 2.0) / max(1, width - 4)
            if t < .55:
                u = t / .55
                rgb = (int(53 + 179 * u), int(177 + 23 * u), int(63 - 14 * u))
            else:
                u = (t - .55) / .45
                rgb = (232, int(200 - 139 * u), int(49 + 5 * u))
            self.instance.fillRect(eRect(x + 2 + a, top + 2, z - a, 6),
                                   parseColor("#%02x%02x%02x" % rgb))

    def _native_right_bar_enabled(self):
        """Never paint a synthetic right bar over left, percentage or off modes.

        The receiver's native ServiceList owns all non-barright layouts.
        Unknown/unsupported configurations fail open to the native renderer.
        """
        try:
            usage = config.usage
            if getattr(getattr(usage, "servicelist_twolines", None), "value", False):
                return False
            mode = usage.show_event_progress_in_servicelist.value
            return mode == "barright"
        except (AttributeError, TypeError, ValueError):
            return False

    def _draw_rows(self, component):
        # All other modes must use native placement, without any overlay.
        if not self._native_right_bar_enabled():
            self._diag("native_progress_mode_fallback")
            return False
        from enigma import eServiceCenter
        rows = component.getList()
        if rows is None:
            self._diag("native_rows_none")
            return False
        top = component.instance.getTopIndex()
        if top < 0:
            self._diag("native_top_negative")
            return False
        selected = component.instance.getCurrentIndex()
        # A new focused service starts its own scroll at the beginning.
        if selected != getattr(self, "_scroll_selected", None):
            self._scroll_selected = selected
            self._scroll_started = time()
            self._last = None
        width = component.instance.size().width()
        height = component.instance.size().height()
        row_height = int(component.ItemHeight)
        if row_height < 10 or width < 120 or height < row_height:
            self._diag("native_geometry_invalid", "%d,%d,%d" % (width, height, row_height))
            return False
        # The native progressbar remains at the far-right edge.
        # Image-specific progress mode can allocate a wider native bar than
        # ServiceListLegacy.progressBarWidth reports. A receiver-scoped
        # override comes from this overlay's own XML attributes.
        bar_width = self._warder_bar_width or int(component.progressBarWidth)
        bar_left = width - int(component.listMarginRight) - bar_width
        available_rows = min(len(rows) - top, (height + row_height - 1) // row_height)
        if available_rows < 0 or bar_left < 100:
            self._diag("native_bar_invalid", "%d,%d" % (bar_left, available_rows))
            return False
        font = component.ServiceInfoFont
        name_font = component.ServiceNameFont
        self._label.setFont(font)
        center = eServiceCenter.getInstance()
        drawing = []
        scroll_age = max(0.0, time() - getattr(self, '_scroll_started', time()) - 1.2)
        pixel_clock = int(scroll_age * 1000.0 / 55.0) * 2
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
            overflow = max(0, measure(title) - remaining)
            # Pause at both ends; replay the whole title from its beginning.
            # 2px per 55ms virtual motion, with safe glyph-aligned painting.
            journey = overflow + 220
            # Only the focused row animates; every other event remains
            # ellipsized and stable even while the timer refreshes the canvas.
            position = (min(overflow, max(0, (pixel_clock % journey) - 110))
                        if overflow and index == selected else 0)
            fitted = scroll_title_window(title, remaining, measure, position)
            if fitted:
                drawing.append((start, row_index * row_height, remaining, row_height,
                                fitted, index == selected, self._progress_fraction(center, ref)))
        if not drawing:
            self._diag("native_no_fitted_rows", "rows=%d top=%d visible=%d" % (len(rows), top, available_rows))
            return False
        self._diag("native_rows_ready", "visible=%d fitted=%d width=%d bar=%d barWidth=%d" %
                   (available_rows, len(drawing), width, bar_left, bar_width))
        signature = (top, selected, row_height, width, height, tuple(drawing))
        if signature == self._last:
            return True
        normal = parseColor(config.plugins.setupGlass17.par109.value)
        highlighted = parseColor(config.plugins.setupGlass17.par110.value)
        self.instance.clear(self._transparent)
        for x, y, w, h, value, is_selected, progress in drawing:
            # Repaint the text field and the bar above native C++ rendering,
            # regardless of whether the image accepts our native font change.
            mask_width = max(0, bar_left + bar_width - x)
            if mask_width:
                self.instance.fillRect(eRect(x, y + 2, mask_width, h - 4),
                                       self._opaque_black)
            self.instance.writeText(eRect(x, y, w, h), highlighted if is_selected else normal,
                                    self._transparent, font, value,
                                    RT_HALIGN_LEFT | RT_VALIGN_CENTER)
            if progress is not None:
                self._draw_progress(bar_left, y, bar_width, h, progress)
        # Receiver visual probe: 16x6 magenta marker at the list's top-left.
        # Enabled ONLY through a diagnostic skin attribute in TEST60.
        if self._warder_test_marker:
            # Bright magenta in the progress-column region: intentionally
            # distinct from the independent green native eLabel test marker.
            self.instance.fillRect(eRect(925, 14, 24, 14), parseColor("#00ff00ff"))
            self._diag("canvas_test_marker_drawn")
        self._last = signature
        self._diag("canvas_painted")
        return True

    def refresh(self):
        try:
            if not self.instance or not self._label:
                return
            component = self._find_component()
            if component is None:
                self._diag("native_component_absent")
                self._restore_native()
                return
            if component is not self._component:
                self._restore_native()
                self._component = component
                self._last = None
            # Draw first; hide the C++ event text only after a complete frame
            # has been produced, so unsupported environments do not go blank.
            if not self._draw_rows(component):
                self._diag("draw_rows_declined")
                # Mode can change while ChannelSelection stays open.
                # Remove old right-hand canvas bars before restoring
                # native text; otherwise a ghost bar remains on screen.
                had_overlay = self._native_hidden or self._last is not None
                if had_overlay:
                    self.instance.clear(self._transparent)
                self._last = None
                self._restore_native()
                # Invalidate once on mode transition, never at every 55ms tick.
                if had_overlay:
                    try:
                        component.instance.invalidate()
                    except (AttributeError, TypeError, RuntimeError):
                        pass
                return
            if not self._native_hidden:
                try:
                    component.l.setElementFont(component.l.celServiceInfo, self._quiet_font)
                except (AttributeError, RuntimeError, TypeError) as exc:
                    self._diag("native_font_suppress_error", type(exc).__name__)
                    self.instance.clear(self._transparent)
                    self._component = None
                    return
                self._native_hidden = True
                self._diag("native_font_suppressed")
                # A native font adjustment is visible only on freshly
                # invalidated rows; the overlay paints the original size.
                # Force the native list to repaint without its unbounded EPG
                # text, including the selected and non-selected rows.
                self._last = None
                try:
                    component.instance.invalidate()
                except (AttributeError, TypeError, RuntimeError):
                    pass
        except (AttributeError, RuntimeError, TypeError, ValueError, IndexError) as exc:
            self._diag("refresh_exception", type(exc).__name__)
            self._restore_native()
            if self.instance:
                self.instance.clear(self._transparent)
        finally:
            if self.instance:
                self._timer.start(55, True)
