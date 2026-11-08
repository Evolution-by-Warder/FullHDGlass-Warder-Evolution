"""Default ChannelSelection: pixel-fit event titles without altering native bars.

The legacy native service-list renderer has no per-event painter clip. When all
required Enigma2 APIs are present, suppress only its unbounded event text and
repaint those titles inside the reserved field. Service names, picons, progress
bars, selection and fonts remain owned by the image. On unsupported images the
native renderer is left completely unchanged.
"""
from time import time, monotonic
from Components.Renderer.Renderer import Renderer
from Components.config import config
from enigma import eCanvas, eLabel, eTimer, eRect, eSize, RT_VALIGN_CENTER, RT_HALIGN_LEFT
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
    # At the rightmost end, anchor the visible window to the *last* glyph.
    # Cutting from the left by pixel offset alone can discard the final
    # one or two letters when glyph widths are not uniform.
    if pixel_offset >= max(0, measure(title) - width):
        lo, hi = 0, len(title)
        while lo < hi:
            mid = (lo + hi) // 2
            if measure(title[mid:]) <= width:
                hi = mid
            else:
                lo = mid + 1
        return title[lo:]
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
        self._native_disable_unsupported = False
        self._last = None
        self._scroll_started = time()
        self._scroll_selected = None
        self._scroll_mode = None
        # Never fake native EPG suppression with a tiny font. The C++ list
        # skips elements whose font pointer is null; where the image's SWIG
        # binding rejects None, leave its native list untouched.
        self._transparent = parseColor("#ff000000")
        self._diag_seen = set()
        # Optional receiver-QA dimensions; absent in production XML.
        self._warder_bar_width = None
        self._warder_test_marker = False
        # TEST3 ONLY: bounded timing samples; no per-frame disk writes.
        self._perf_since = monotonic()
        self._perf_ticks = 0
        self._perf_elapsed_ms = 0.0
        self._perf_worst_ms = 0.0
        self._perf_over_20ms = 0
        self._perf_row_changes = 0
        self._perf_last_row = None
        self._perf_name_calls = 0
        self._perf_progress_calls = 0
        self._epg_snapshots = {}
        self._epg_cache_hits = 0
        self._epg_cache_misses = 0
        # TEST5: static title/geometry and glyph width measurements.
        # Neither cache stores channel references or paints pixels.
        self._row_fit_cache = {}
        self._glyph_width_cache = {}
        # TEST6: reusable exact pixel paint plans (not raster approximations).
        self._progress_paint_cache = {}
        self._bar_canvas = None
        self._bar_last = None
        self._perf_bar_skips = 0
        self._perf_bar_plan_hits = 0
        self._perf_bar_plan_misses = 0
        self._perf_text_measure_calls = 0
        self._perf_text_cache_hits = 0

    def _diag(self, key, details=""):
        # Retained as a no-op for compatibility with diagnostic call sites.
        # TEST59 startup traces are obsolete; do not create a second log.
        pass

    def _perf_tick(self, elapsed_ms):
        try:
            self._perf_ticks += 1
            self._perf_elapsed_ms += elapsed_ms
            self._perf_worst_ms = max(self._perf_worst_ms, elapsed_ms)
            if elapsed_ms >= 20.0:
                self._perf_over_20ms += 1
            now = monotonic()
            if now - self._perf_since < 5.0:
                return
            count = self._perf_ticks
            if count > 0:
                with open('/tmp/warder-channelselection-perf-test3.log', 'a') as report:
                    report.write('uptime_window_s=%.1f ticks=%d mean_ms=%.3f max_ms=%.3f over20ms=%d selections=%d name_epg_calls=%d progress_epg_calls=%d cache_hits=%d cache_misses=%d measure_calls=%d text_cache_hits=%d bar_plan_hits=%d bar_plan_misses=%d bar_skips=%d split_canvas=%d mode=%s\n' % (
                        now - self._perf_since, count, self._perf_elapsed_ms / count,
                        self._perf_worst_ms, self._perf_over_20ms,
                        self._perf_row_changes, self._perf_name_calls,
                        self._perf_progress_calls, self._epg_cache_hits,
                        self._epg_cache_misses, self._perf_text_measure_calls,
                        self._perf_text_cache_hits, self._perf_bar_plan_hits,
                        self._perf_bar_plan_misses, self._perf_bar_skips,
                        int(self._bar_canvas is not None), str(self._progress_mode())))
            self._perf_since = now
            self._perf_ticks = 0
            self._perf_elapsed_ms = 0.0
            self._perf_worst_ms = 0.0
            self._perf_over_20ms = 0
            self._perf_row_changes = 0
            self._perf_name_calls = 0
            self._perf_progress_calls = 0
            self._epg_cache_hits = 0
            self._epg_cache_misses = 0
            self._perf_text_measure_calls = 0
            self._perf_text_cache_hits = 0
            self._perf_bar_plan_hits = 0
            self._perf_bar_plan_misses = 0
            self._perf_bar_skips = 0
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
        self._scroll_mode = None
        if hasattr(self, '_row_fit_cache'):
            self._row_fit_cache.clear()
        if hasattr(self, '_glyph_width_cache'):
            self._glyph_width_cache.clear()
        if hasattr(self, '_epg_snapshots'):
            self._epg_snapshots.clear()
        # TEST8: independent transparent child canvas for progress bars.
        # On unsupported Enigma2 versions the original combined painter
        # remains active without touching the approved XML or layout.
        try:
            self._bar_canvas = eCanvas(instance)
            self._bar_canvas.setSize(instance.size())
            self._bar_canvas.clear(self._transparent)
            self._bar_canvas.show()
        except (NameError, AttributeError, TypeError, RuntimeError):
            self._bar_canvas = None
        self._bar_last = None
        self._timer.start(55, True)

    def _clear_bar_canvas(self):
        child = getattr(self, '_bar_canvas', None)
        if child is not None:
            try:
                child.clear(self._transparent)
            except (AttributeError, RuntimeError, TypeError):
                pass
        self._bar_last = None

    def preWidgetRemove(self, instance):
        self._timer.stop()
        if hasattr(self, '_clear_bar_canvas'):
            self._clear_bar_canvas()
        self._bar_canvas = None
        if hasattr(self, '_row_fit_cache'):
            self._row_fit_cache.clear()
        if hasattr(self, '_glyph_width_cache'):
            self._glyph_width_cache.clear()
        if hasattr(self, '_epg_snapshots'):
            self._epg_snapshots.clear()
        self._restore_native()
        self._label = None

    def changed(self, what):
        if self.instance:
            self._last = None
            self._scroll_started = time()
            # Selection notifications must NOT wipe the other visible rows.
            # Their snapshots expire naturally after at most one second.
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

    def _event_snapshot(self, center, ref):
        """Keep a short-lived service/EPG snapshot shared by title and bar.

        The GUI still refreshes/scrolls every 55ms, but the native service
        center is consulted at most once per service per one-second TTL.
        A fresh event is loaded on the next second, screen rebuild or source
        change. Never cache indefinitely, and keep memory bounded.
        """
        try:
            if ref.flags & 7:
                return ("", "", None)
            key = ref.toString()
            now = monotonic()
            cached = self._epg_snapshots.get(key)
            if cached is not None and now - cached[0] < 1.0:
                self._epg_cache_hits += 1
                return cached[1]
            info = center.info(ref)
            if info is None:
                snapshot = ("", "", None)
            else:
                event = info.getEvent(ref)
                snapshot = (info.getName(ref) or "",
                            (event.getEventName() or "") if event else "", event)
            if len(self._epg_snapshots) >= 96:
                # The visible list is usually <= 30. Bound long browsing
                # sessions without affecting currently visible rows.
                self._epg_snapshots.clear()
            self._epg_snapshots[key] = (now, snapshot)
            self._epg_cache_misses += 1
            return snapshot
        except (AttributeError, RuntimeError, TypeError, ValueError):
            return ("", "", None)

    def _name_and_event(self, center, ref):
        self._perf_name_calls += 1
        name, title, event = self._event_snapshot(center, ref)
        return name, title

    def _progress_fraction(self, center, ref):
        self._perf_progress_calls += 1
        try:
            name, title, event = self._event_snapshot(center, ref)
            if event is None:
                return None
            duration = int(event.getDuration())
            if duration <= 0:
                return None
            elapsed = time() - int(event.getBeginTime())
            return int(max(0.0, min(1.0, elapsed / float(duration))) * 100) / 100.0
        except (AttributeError, RuntimeError, TypeError, ValueError, ZeroDivisionError):
            return None

    def _progress_mode(self):
        """Supported single-line native modes; unknown modes remain native."""
        try:
            usage = config.usage
            if getattr(getattr(usage, "servicelist_twolines", None), "value", False):
                return None
            mode = usage.show_event_progress_in_servicelist.value
            return mode if mode in ("barright", "barleft", "percright", "percleft", "minsright", "minsleft", "no") else None
        except (AttributeError, TypeError, ValueError):
            return None

    def _native_right_bar_enabled(self):
        # Compatibility for legacy renderer tests and native callers.
        return self._progress_mode() == "barright"

    def _draw_rows(self, component):
        mode = self._progress_mode()
        if mode is None:
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
        if getattr(self, '_perf_last_row', None) is not None and selected != self._perf_last_row:
            self._perf_row_changes = getattr(self, '_perf_row_changes', 0) + 1
        self._perf_last_row = selected
        # A new focused service starts its own scroll at the beginning.
        if (selected != getattr(self, "_scroll_selected", None)
                or mode != getattr(self, "_scroll_mode", None)):
            self._scroll_selected = selected
            self._scroll_mode = mode
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
        # Numeric indicators are native service-list cells, not progressbars.
        # Reserve conservative widths for their complete value and the gap
        # to the event title. Never paint over percentages/minutes.
        # ServiceListLegacy uses ProgressInfoFont and measures "+000 min"
        # or "100 %" to set the native numeric indicator width. Match that
        # font, with a conservative fallback for unsupported image builds.
        indicator_width = bar_width
        if mode.startswith(("perc", "mins")):
            numeric_sample = "+000 min." if mode.startswith("mins") else "100 %"
            fallback_width = 175 if mode.startswith("mins") else 120
            try:
                progress_font = component.ProgressInfoFont
                self._label.setFont(progress_font)
                self._label.setText(numeric_sample)
                indicator_width = max(1, self._label.calculateSize().width(), fallback_width)
            except (AttributeError, TypeError, RuntimeError, ValueError):
                indicator_width = fallback_width
        field_gap = max(12, int(component.fieldMargins))
        right_reserve = (indicator_width + field_gap
                         if mode.endswith("right") else 12)
        left_shift = (indicator_width + field_gap
                      if mode.endswith("left") else 0)
        text_end = width - int(component.listMarginRight) - right_reserve
        available_rows = min(len(rows) - top, (height + row_height - 1) // row_height)
        if available_rows < 0 or text_end < 100:
            self._diag("native_bar_invalid", "%d,%d" % (text_end, available_rows))
            return False
        font = component.ServiceInfoFont
        name_font = component.ServiceNameFont
        self._label.setFont(font)
        center = eServiceCenter.getInstance()
        # Invalidate geometrical measurements whenever a style/geometry
        # property changes; color changes are applied at painting time.
        geometry_key = (mode, width, height, row_height, text_end, left_shift,
                        int(component.listMarginLeft), int(component.itemsDistances),
                        str(config.usage.servicelist_picon_downsize.value),
                        str(config.usage.servicelist_picon_ratio.value),
                        id(font), id(name_font))
        if getattr(self, '_row_geometry_key', None) != geometry_key:
            if hasattr(self, '_row_fit_cache'):
                self._row_fit_cache.clear()
            if hasattr(self, '_glyph_width_cache'):
                self._glyph_width_cache.clear()
            self._row_geometry_key = geometry_key
        drawing = []
        # One progress lookup per visible service: reuse it for the
        # selected-row text and for the original progress indicator.
        # Avoid asking the native EPG cache twice on every 55ms refresh.
        fractions = {}
        scroll_age = max(0.0, time() - getattr(self, '_scroll_started', time()) - 1.2)
        pixel_clock = int(scroll_age * 1000.0 / 55.0) * 2
        for row_index in range(available_rows):
            index = top + row_index
            ref = rows[index]
            name, title = self._name_and_event(center, ref)
            if not title:
                continue
            # Stable rows retain their measured name/title geometry across
            # timer ticks and rapid selection changes. The source snapshot
            # supplies new text on EPG changes, automatically changing the key.
            row_cache = getattr(self, '_row_fit_cache', None)
            glyph_cache = getattr(self, '_glyph_width_cache', None)
            row_key = (name, title, geometry_key)
            cached_row = row_cache.get(row_key) if row_cache is not None else None
            if cached_row is None:
                self._label.setFont(name_font)
                self._label.setText(name)
                name_width = self._label.calculateSize().width()
                if hasattr(self, '_perf_text_measure_calls'):
                    self._perf_text_measure_calls += 1
                picon_width = int((row_height + 2 * int(config.usage.servicelist_picon_downsize.value)) *
                                  int(config.usage.servicelist_picon_ratio.value) / 100)
                start = max(0, int(component.listMarginLeft) + picon_width +
                            2 * int(component.itemsDistances) + name_width + left_shift)
                remaining = text_end - start
            else:
                start, remaining, overflow, first_frame = cached_row
                if hasattr(self, '_perf_text_cache_hits'):
                    self._perf_text_cache_hits += 1
            if remaining <= 0:
                continue
            self._label.setFont(font)
            def measure(text):
                if glyph_cache is not None:
                    key = (title, text)
                    found = glyph_cache.get(key)
                    if found is not None:
                        if hasattr(self, '_perf_text_cache_hits'):
                            self._perf_text_cache_hits += 1
                        return found
                self._label.setText(text)
                result = self._label.calculateSize().width()
                if hasattr(self, '_perf_text_measure_calls'):
                    self._perf_text_measure_calls += 1
                if glyph_cache is not None:
                    if len(glyph_cache) >= 512:
                        glyph_cache.clear()
                    glyph_cache[(title, text)] = result
                return result
            if cached_row is None:
                overflow = max(0, measure(title) - remaining)
                first_frame = scroll_title_window(title, remaining, measure, 0)
                if row_cache is not None:
                    if len(row_cache) >= 128:
                        row_cache.clear()
                    row_cache[row_key] = (start, remaining, overflow, first_frame)
            # Pause at both ends; replay the whole title from its beginning.
            # 2px per 55ms virtual motion, with safe glyph-aligned painting.
            journey = overflow + 220
            # Only the focused row animates; every other event remains
            # ellipsized and stable even while the timer refreshes the canvas.
            position = (min(overflow, max(0, (pixel_clock % journey) - 110))
                        if overflow and index == selected else 0)
            fitted = (first_frame if position == 0 else
                      scroll_title_window(title, remaining, measure, position))
            if fitted:
                fraction = self._progress_fraction(center, ref)
                fractions[row_index] = fraction
                drawing.append((start, row_index * row_height, remaining, row_height,
                                fitted, index == selected, fraction))
        # On stock OpenATV, disabling native EPG text also prevents the native
        # C++ progressbar from receiving its event. Draw its real elapsed
        # fraction in the reserved bar cell: no C++ patch or black mask.
        progress_bars = []
        if mode in ("barleft", "barright"):
            bar_x = (int(component.listMarginLeft) if mode == "barleft"
                     else width - int(component.listMarginRight) - bar_width)
            bar_h = 10
            for row_index in range(available_rows):
                # No second EPG lookup when this row already has a fraction.
                fraction = fractions.get(row_index)
                if row_index not in fractions:
                    ref = rows[top + row_index]
                    fraction = self._progress_fraction(center, ref)
                if fraction is None:
                    continue
                progress_bars.append((bar_x, row_index * row_height + (row_height - bar_h) // 2,
                                      bar_width, bar_h, fraction))
        if not drawing:
            self._diag("native_no_fitted_rows", "rows=%d top=%d visible=%d" % (len(rows), top, available_rows))
            return False
        self._diag("native_rows_ready", "mode=%s visible=%d fitted=%d width=%d bar=%d barWidth=%d" %
                   (mode, available_rows, len(drawing), width, bar_left, bar_width))
        # Full native painting is the fallback; with a working child canvas,
        # progress bars are repainted ONLY when their visible pixels change.
        split = getattr(self, '_bar_canvas', None) is not None
        bar_signature = (mode, top, row_height, width, height, tuple(progress_bars))
        normal_setting = config.plugins.setupGlass17.par109.value
        selected_setting = config.plugins.setupGlass17.par110.value
        # Fractions are bar-only pixels in split mode. Otherwise retain the
        # original joint signature so fallback repaints bars when they move.
        text_content = (tuple((x, y, w, h, value, is_selected)
                              for x, y, w, h, value, is_selected, fraction in drawing)
                        if split else tuple(drawing))
        text_signature = (mode, top, selected, row_height, width, height,
                          normal_setting, selected_setting, text_content)
        signature = (text_signature, None if split else bar_signature)
        text_dirty = signature != self._last
        bar_dirty = split and bar_signature != getattr(self, '_bar_last', None)
        if not text_dirty and not bar_dirty:
            return True
        if text_dirty:
            normal = parseColor(normal_setting)
            highlighted = parseColor(selected_setting)
            self.instance.clear(self._transparent)
        for x, y, w, h, value, is_selected, progress in (drawing if text_dirty else ()):
            # Native C++ must already have stopped rendering celServiceInfo.
            # Paint only our own fitted letters; never black-mask native rows
            # or repaint the indicator that belongs to the native list.
            self.instance.writeText(eRect(x, y, w, h), highlighted if is_selected else normal,
                                    self._transparent, font, value,
                                    RT_HALIGN_LEFT | RT_VALIGN_CENTER)
        target = self._bar_canvas if split else self.instance
        if bar_dirty:
            target.clear(self._transparent)
        if split and not bar_dirty and progress_bars:
            if hasattr(self, '_perf_bar_skips'):
                self._perf_bar_skips += 1
        if progress_bars and (not split or bar_dirty):
            # The exact eight-segment gradient, frame width, rectangles and
            # source colors remain identical to TEST5. Only geometry and
            # parseColor conversion are reused across rows/timer frames.
            #
            # Cache by actual pixel width/height and integer filled length,
            # *not* by service: a programme changing does not inherit an
            # outdated bar, and no user-selected position is shared.
            paint_cache = getattr(self, '_progress_paint_cache', None)
            if paint_cache is None:
                paint_cache = {}
            border = parseColor("#dfdfdf")
            for bx, by, bw, bh, fraction in progress_bars:
                if bw <= 4 or bh <= 4:
                    continue
                inner_width = bw - 4
                filled = int(inner_width * fraction)
                key = (bw, bh, filled)
                plan = paint_cache.get(key)
                if plan is None:
                    if hasattr(self, '_perf_bar_plan_misses'):
                        self._perf_bar_plan_misses += 1
                    # Immutable relative rectangles preserve every original
                    # eCanvas fillRect call; only offset by the current row.
                    segments = []
                    for segment in range(8):
                        a = filled * segment // 8
                        z = filled * (segment + 1) // 8
                        if z <= a:
                            continue
                        t = ((a + z) / 2.0) / max(1, inner_width)
                        if t < .55:
                            u = t / .55
                            rgb = (int(53 + 179 * u), int(177 + 23 * u),
                                   int(63 - 14 * u))
                        else:
                            u = (t - .55) / .45
                            rgb = (232, int(200 - 139 * u), int(49 + 5 * u))
                        segments.append((2 + a, 2, z - a, bh - 4,
                                         parseColor("#%02x%02x%02x" % rgb)))
                    plan = tuple(segments)
                    if len(paint_cache) >= 128:
                        paint_cache.clear()
                    paint_cache[key] = plan
                elif hasattr(self, '_perf_bar_plan_hits'):
                    self._perf_bar_plan_hits += 1
                target.fillRect(eRect(bx, by, bw, 2), border)
                target.fillRect(eRect(bx, by + bh - 2, bw, 2), border)
                target.fillRect(eRect(bx, by + 2, 2, bh - 4), border)
                target.fillRect(eRect(bx + bw - 2, by + 2, 2, bh - 4), border)
                for dx, dy, pw, ph, color in plan:
                    target.fillRect(eRect(bx + dx, by + dy, pw, ph), color)
        # Receiver visual probe: 16x6 magenta marker at the list's top-left.
        # Enabled ONLY through a diagnostic skin attribute in TEST60.
        if self._warder_test_marker:
            # Bright magenta in the progress-column region: intentionally
            # distinct from the independent green native eLabel test marker.
            self.instance.fillRect(eRect(925, 14, 24, 14), parseColor("#00ff00ff"))
            self._diag("canvas_test_marker_drawn")
        self._last = signature
        if split:
            self._bar_last = bar_signature
        self._diag("canvas_painted")
        return True

    def refresh(self):
        # Local import also supports isolated AST-method regression tests.
        from time import monotonic
        started = monotonic()
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
                if hasattr(self, '_epg_snapshots'):
                    self._epg_snapshots.clear()
                if hasattr(self, '_row_fit_cache'):
                    self._row_fit_cache.clear()
                if hasattr(self, '_glyph_width_cache'):
                    self._glyph_width_cache.clear()
                self._native_disable_unsupported = False
                self._last = None
                if hasattr(self, '_clear_bar_canvas'):
                    self._clear_bar_canvas()
            # Unsupported views must remain completely native; never
            # toggle celServiceInfo on every timer tick for those modes.
            if self._progress_mode() is None:
                had_overlay = self._native_hidden or self._last is not None
                if had_overlay:
                    self.instance.clear(self._transparent)
                    if hasattr(self, '_clear_bar_canvas'):
                        self._clear_bar_canvas()
                self._last = None
                self._restore_native()
                if had_overlay:
                    try:
                        component.instance.invalidate()
                    except (AttributeError, TypeError, RuntimeError):
                        pass
                return
            # ServiceListLegacy.setMode() restores the native EPG font.
            # Detect the mode change BEFORE disabling it and BEFORE painting,
            # rather than resetting _native_hidden inside _draw_rows().
            current_mode = self._progress_mode()
            if current_mode != getattr(self, "_scroll_mode", None):
                self._native_hidden = False
            # C++ paint() only skips an element when its font pointer is
            # null. A 1px substitute still paints garbage glyphs. SWIG may
            # reject None on older images: fail open without any overlay.
            if self._native_disable_unsupported:
                return
            # Reassert on every refresh without repeatedly invalidating.
            # Native setMode()/setFontsize() can restore celServiceInfo
            # between two ticks even when the indicator mode is unchanged.
            first_disable = not self._native_hidden
            try:
                component.l.setElementFont(component.l.celServiceInfo, None)
            except (AttributeError, RuntimeError, TypeError, ValueError) as exc:
                self._diag("native_event_disable_unsupported", type(exc).__name__)
                self._native_disable_unsupported = True
                self.instance.clear(self._transparent)
                if hasattr(self, '_clear_bar_canvas'):
                    self._clear_bar_canvas()
                self._last = None
                self._restore_native()
                self._component = component
                return
            self._native_hidden = True
            if first_disable:
                self._last = None
                try:
                    component.instance.invalidate()
                except (AttributeError, TypeError, RuntimeError):
                    pass
            if not self._draw_rows(component):
                self._diag("draw_rows_declined")
                # Mode can change while ChannelSelection stays open.
                # Remove old right-hand canvas bars before restoring
                # native text; otherwise a ghost bar remains on screen.
                had_overlay = self._native_hidden or self._last is not None
                if had_overlay:
                    self.instance.clear(self._transparent)
                    if hasattr(self, '_clear_bar_canvas'):
                        self._clear_bar_canvas()
                self._last = None
                self._restore_native()
                # Invalidate once on mode transition, never at every 55ms tick.
                if had_overlay:
                    try:
                        component.instance.invalidate()
                    except (AttributeError, TypeError, RuntimeError):
                        pass
                return
        except (AttributeError, RuntimeError, TypeError, ValueError, IndexError) as exc:
            self._diag("refresh_exception", type(exc).__name__)
            self._restore_native()
            if self.instance:
                self.instance.clear(self._transparent)
                if hasattr(self, '_clear_bar_canvas'):
                    self._clear_bar_canvas()
        finally:
            if hasattr(self, '_perf_tick'):
                self._perf_tick((monotonic() - started) * 1000.0)
            if self.instance:
                self._timer.start(55, True)
