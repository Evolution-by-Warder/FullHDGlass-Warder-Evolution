"""Behavioral source-level tests for default legacy service-list EPG clipping.

Uses an isolated AST method and mock components; no Enigma2 receiver is implied.
"""
import ast
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "source/package-root/usr/lib/enigma2/python/Components/Renderer/WarderChannelEpgClip.py"
FIT = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderEpgTextFit.py"

scope_fit = {}
exec(compile(FIT.read_text(encoding="utf-8"), str(FIT), "exec"), scope_fit)
fit_title_to_width = scope_fit["fit_title_to_width"]
scroll_scope = {"fit_title_to_width": fit_title_to_width}
scroll_fn = next(n for n in ast.parse(RENDERER.read_text(encoding="utf-8")).body
                 if isinstance(n, ast.FunctionDef) and n.name == "scroll_title_window")
exec(compile(ast.Module(body=[scroll_fn], type_ignores=[]), str(RENDERER), "exec"), scroll_scope)
scroll_title_window = scroll_scope["scroll_title_window"]


class Label:
    def setFont(self, font):
        self.font = font

    def setText(self, text):
        self.text = text

    def calculateSize(self):
        return types.SimpleNamespace(width=lambda: len(self.text) * 10)


class Canvas:
    def __init__(self):
        self.calls = []

    def clear(self, color):
        self.calls.append(("clear", color))

    def writeText(self, rect, foreground, background, font, text, flags):
        self.calls.append(("write", rect, foreground, font, text))

    def fillRect(self, rect, color):
        self.calls.append(("fill", rect, color))

    # OpenATV 8.0-next eCanvas has no flush() method. Do not add a
    # mock: exercising draw/exception paths must catch accidental use.


class Service:
    def __init__(self, name, title):
        self.name = name
        self.title = title


class Component:
    ItemHeight = 37
    listMarginRight = 25
    progressBarWidth = 90
    listMarginLeft = 5
    itemsDistances = 8
    fieldMargins = 26
    ServiceInfoFont = "info"
    ServiceNameFont = "name"

    def __init__(self, refs):
        self.refs = refs
        self.selected = 1
        self.instance = self
        self.l = types.SimpleNamespace(celServiceInfo=2)

    def getList(self):
        return self.refs

    def getTopIndex(self):
        return 0

    def getCurrentIndex(self):
        return self.selected

    def size(self):
        return types.SimpleNamespace(width=lambda: 700, height=lambda: 222)


def method(name):
    tree = ast.parse(RENDERER.read_text(encoding="utf-8"))
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "WarderChannelEpgClip")
    fn = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == name)
    env = {
        "config": types.SimpleNamespace(usage=types.SimpleNamespace(
            servicelist_picon_downsize=types.SimpleNamespace(value=-2),
            servicelist_picon_ratio=types.SimpleNamespace(value="167")),
            plugins=types.SimpleNamespace(setupGlass17=types.SimpleNamespace(
                par109=types.SimpleNamespace(value="#ffffff"),
                par110=types.SimpleNamespace(value="#62aaff")))),
        "fit_title_to_width": fit_title_to_width,
        "scroll_title_window": scroll_title_window,
        "time": __import__("time").time,
        "parseColor": lambda value: value,
        "eRect": lambda *args: args,
        "RT_HALIGN_LEFT": 1,
        "RT_VALIGN_CENTER": 2,
    }
    exec(compile(ast.Module(body=[fn], type_ignores=[]), str(RENDERER), "exec"), env)
    return env[name]


class ClippedEventTests(unittest.TestCase):
    def setUp(self):
        self.refs = [
            Service("CT 1 PHA HD", "Létající Čestmír, Modrý kámen, Miloš Macourek a pokračovanie " * 4),
            Service("JOJ PLUS HD", "Nové bývanie"),
            Service("Markiza", "X" * 400),
        ]
        self.component = Component(self.refs)
        self.renderer = types.SimpleNamespace(
            _label=Label(), instance=Canvas(), _last=None, _transparent="#transparent",
            _name_and_event=lambda center, ref: (ref.name, ref.title),
            _progress_fraction=lambda center, ref: 0.35,
            _draw_progress=lambda x, y, width, row_height, elapsed: None,
            _opaque_black="#000000", _progress_border="#dfdfdf",
            _warder_bar_width=None, _warder_test_marker=False,
            _progress_mode=lambda: "barright",
            _native_right_bar_enabled=lambda: True,
            _diag=lambda *args: None)
        self.service_stub = types.ModuleType("enigma")
        self.service_stub.eServiceCenter = types.SimpleNamespace(getInstance=lambda: object())

    def draw(self):
        with patch.dict(sys.modules, {"enigma": self.service_stub}):
            return method("_draw_rows")(self.renderer, self.component)

    def test_titles_never_reach_reserved_progress_column(self):
        self.assertTrue(self.draw())
        writes = [x for x in self.renderer.instance.calls if x[0] == "write"]
        self.assertEqual(len(writes), 3)
        bar_start = 700 - 25 - 90
        for _, rect, color, font, title in writes:
            x, y, width, height = rect
            self.assertLessEqual(x + width, bar_start - 12)
            self.assertLessEqual(len(title) * 10, width)
            self.assertLessEqual(y + height, 222)
        self.assertTrue(writes[0][-1].endswith("…"))
        masks = [item for item in self.renderer.instance.calls if item[0] == "fill"]
        self.assertEqual(len(masks), 3)
        for _, rect, color in masks:
            self.assertGreater(rect[2], 0)
            self.assertEqual(color, "#000000")
        self.assertEqual(writes[1][-1], "Nové bývanie")
        self.assertEqual(writes[1][2], "#62aaff")
        self.assertLessEqual(writes[2][1][0] + writes[2][1][2], bar_start - 12)

    def test_long_title_scrolls_without_overflowing_reserved_field(self):
        text = "Very long event name with additional details " * 5
        measure = lambda item: len(item) * 10
        width = 170
        first = scroll_title_window(text, width, measure, 0)
        after = scroll_title_window(text, width, measure, 110)
        self.assertNotEqual(first, after)
        self.assertTrue(after.startswith(text[11:15]))
        self.assertLessEqual(measure(after), width)
        self.assertEqual(scroll_title_window("Short show", width, measure, 100), "Short show")
        self.assertEqual(scroll_title_window(text, 0, measure, 10), "")

    def test_scrolling_reveals_full_suffix_without_ellipsis(self):
        title = "ABCDEFGHIJ"
        measure = lambda item: len(item) * 10
        # Scrolled past seven characters, the last three must be visible.
        self.assertEqual(scroll_title_window(title, 30, measure, 70), "HIJ")
        # Early moving windows are bounded and contain no artificial dots.
        self.assertEqual(scroll_title_window(title, 30, measure, 20), "CDE")
        # An unscrolled long name still advertises truncation.
        self.assertTrue(scroll_title_window(title, 30, measure, 0).endswith("…"))

    def test_variable_width_scroll_reaches_final_glyphs(self):
        title = "WWWWiiiiABC"
        widths = {"W": 17, "i": 4, "A": 11, "B": 10, "C": 9}
        def measure(value):
            return sum(widths[ch] for ch in value)
        width = 31
        overflow = measure(title) - width
        end = scroll_title_window(title, width, measure, overflow)
        self.assertTrue(end.endswith("ABC"))
        self.assertLessEqual(measure(end), width)
        # Offsets beyond the end cannot make the terminal glyph disappear.
        self.assertEqual(scroll_title_window(title, width, measure, overflow + 50), end)

    def test_scrolling_event_changes_while_short_event_stays_still(self):
        from time import time
        self.renderer._scroll_started = time() - 7
        self.assertTrue(self.draw())
        writes = [x for x in self.renderer.instance.calls if x[0] == "write"]
        self.assertLessEqual(len(writes[0][-1]) * 10, writes[0][1][2])
        self.assertEqual(writes[1][-1], "Nové bývanie")
        self.assertLessEqual(writes[2][1][0] + writes[2][1][2], 700 - 25 - 90 - 12)

    def test_only_focused_long_event_scrolls(self):
        from time import time
        self.component.selected = 0
        self.renderer._scroll_selected = 0
        self.renderer._scroll_started = time() - 8
        self.assertTrue(self.draw())
        written = [call[-1] for call in self.renderer.instance.calls if call[0] == "write"]
        self.assertNotEqual(written[0], scroll_title_window(
            self.refs[0].title, 100, lambda text: len(text) * 10, 0))
        self.assertTrue(written[2].endswith("…"))
        self.assertEqual(written[1], "Nové bývanie")
        self.component.selected = 2
        self.assertTrue(self.draw())
        self.assertEqual(self.renderer._scroll_selected, 2)
        self.assertLess(time() - self.renderer._scroll_started, 2)
        new_written = [call[-1] for call in self.renderer.instance.calls if call[0] == "write"][-3:]
        self.assertTrue(new_written[0].endswith("…"))
        self.assertTrue(new_written[2].endswith("…"))

    def test_mode_switch_reapplies_native_event_suppression(self):
        # Native ServiceList.setMode restores the original event font.
        # A cached _native_hidden=True must be reset on each mode change.
        from time import time
        self.component.selected = 1
        self.renderer._scroll_selected = 1
        self.renderer._scroll_mode = "barright"
        self.renderer._scroll_started = time() - 4
        self.renderer._native_hidden = True
        self.renderer._progress_mode = lambda: "percright"
        self.assertTrue(self.draw())
        self.assertFalse(self.renderer._native_hidden)
        self.assertEqual(self.renderer._scroll_mode, "percright")
        self.renderer._native_hidden = True
        self.assertTrue(self.draw())
        self.assertTrue(self.renderer._native_hidden)
        self.renderer._progress_mode = lambda: "minsleft"
        self.assertTrue(self.draw())
        self.assertFalse(self.renderer._native_hidden)

    def test_native_progress_modes_selected_safely(self):
        mode_method = method("_progress_mode")
        usage = types.SimpleNamespace(
            show_event_progress_in_servicelist=types.SimpleNamespace(value="barright"),
            servicelist_twolines=types.SimpleNamespace(value=False))
        mode_method.__globals__["config"] = types.SimpleNamespace(usage=usage)
        for mode in ("barright", "barleft", "no", "percleft",
                     "percright", "minsleft", "minsright"):
            usage.show_event_progress_in_servicelist.value = mode
            self.assertEqual(mode_method(self.renderer), mode)
        for mode in ("unknown", "barcenter"):
            usage.show_event_progress_in_servicelist.value = mode
            self.assertIsNone(mode_method(self.renderer))
        usage.servicelist_twolines.value = True
        usage.show_event_progress_in_servicelist.value = "barright"
        self.assertIsNone(mode_method(self.renderer))

    def test_left_bar_shifts_names_and_keeps_native_bars(self):
        self.renderer._progress_mode = lambda: "barleft"
        bars = []
        self.renderer._draw_progress = lambda *args: bars.append(args)
        self.assertTrue(self.draw())
        writes = [x for x in self.renderer.instance.calls if x[0] == "write"]
        self.assertEqual(len(writes), 3)
        # At 700px list width, 90px native left bar plus 26px margin
        # moves event text right; no second right-hand bar is rendered.
        self.assertGreater(writes[0][1][0], 200)
        self.assertTrue(all(x[1][0] + x[1][2] <= 700 - 25 - 12 for x in writes))
        self.assertEqual(bars, [])

    def test_disabled_bar_uses_full_text_width_without_redraw(self):
        self.renderer._progress_mode = lambda: "no"
        bars = []
        self.renderer._draw_progress = lambda *args: bars.append(args)
        self.assertTrue(self.draw())
        writes = [x for x in self.renderer.instance.calls if x[0] == "write"]
        self.assertTrue(all(x[1][0] + x[1][2] <= 700 - 25 - 12 for x in writes))
        self.assertEqual(bars, [])
        self.assertTrue(any(call[0] == "write" for call in self.renderer.instance.calls))

    def test_all_seven_progress_modes_preserve_indicator_column(self):
        # The native progress/percent/minutes cells are never repainted by
        # our canvas except the legacy verified right-hand bar layout.
        modes = {
            "barright": (True, 700 - 25 - 90 - 26),
            "barleft": (False, 700 - 25 - 12),
            "percright": (False, 700 - 25 - 146),
            "percleft": (False, 700 - 25 - 12),
            "minsright": (False, 700 - 25 - 201),
            "minsleft": (False, 700 - 25 - 12),
            "no": (False, 700 - 25 - 12),
        }
        starts = {}
        for mode, (draw_bar, text_end) in modes.items():
            self.renderer.instance = Canvas()
            self.renderer._last = None
            self.renderer._progress_mode = lambda m=mode: m
            bar_calls = []
            self.renderer._draw_progress = lambda *args: bar_calls.append(args)
            self.assertTrue(self.draw(), mode)
            writes = [x for x in self.renderer.instance.calls if x[0] == "write"]
            self.assertEqual(len(writes), 3, mode)
            self.assertTrue(all(x[1][0] + x[1][2] <= text_end for x in writes), mode)
            self.assertEqual(bool(bar_calls), draw_bar, mode)
            starts[mode] = writes[0][1][0]
        self.assertGreater(starts["barleft"], starts["no"])
        self.assertGreater(starts["percleft"], starts["no"])
        self.assertGreater(starts["minsleft"], starts["percleft"])

    def test_numeric_indicator_uses_progress_font_when_wider(self):
        class WideProgressLabel(Label):
            def calculateSize(self):
                if getattr(self, "font", None) == "progress":
                    return types.SimpleNamespace(width=lambda: 225)
                return super().calculateSize()
        self.component.ProgressInfoFont = "progress"
        self.renderer._label = WideProgressLabel()
        for mode in ("percright", "minsright"):
            self.renderer.instance = Canvas()
            self.renderer._last = None
            self.renderer._progress_mode = lambda m=mode: m
            self.assertTrue(self.draw())
            writes = [x for x in self.renderer.instance.calls if x[0] == "write"]
            self.assertTrue(all(x[1][0] + x[1][2] <= 700 - 25 - 225 - 26
                                for x in writes), mode)

    def test_unsupported_modes_do_not_draw_synthetic_bar_or_text(self):
        self.renderer._progress_mode = lambda: None
        self.assertFalse(self.draw())
        self.assertEqual(self.renderer.instance.calls, [])

    def test_no_events_causes_no_native_suppression_candidate(self):
        self.refs = [Service("No EPG", "")]
        self.component = Component(self.refs)
        self.assertFalse(self.draw())
        self.assertEqual(self.renderer.instance.calls, [])

    def test_openatv_canvas_without_flush_renders_and_caches(self):
        self.assertFalse(hasattr(self.renderer.instance, "flush"))
        self.assertTrue(self.draw())
        self.assertTrue(any(call[0] == "write" for call in self.renderer.instance.calls))
        self.assertTrue(self.draw())

    def test_refresh_error_handler_does_not_require_flush(self):
        import types
        renderer = types.SimpleNamespace(
            instance=Canvas(), _label=Label(), _native_hidden=False,
            _component=None, _transparent="#transparent", _timer=types.SimpleNamespace(
                start=lambda *args: None),
            _diag=lambda *args: None,
            _find_component=lambda: object(),
            _draw_rows=lambda c: (_ for _ in ()).throw(AttributeError("test failure")),
            _restore_native=lambda: None,
        )
        method("refresh")(renderer)
        self.assertTrue(any(call[0] == "clear" for call in renderer.instance.calls))

    def test_canvas_pixmap_is_allocated_from_runtime_skin(self):
        class FakeLabel:
            def __init__(self, parent):
                self.parent = parent
            def setNoWrap(self, value):
                pass
            def resize(self, dimensions):
                pass
            def hide(self):
                pass
        class FakeCanvas:
            def __init__(self):
                self.sizes = []
            def setSize(self, dims):
                self.sizes.append(dims)
        canvas = FakeCanvas()
        mock = types.SimpleNamespace(
            skinAttributes=[("size", "1065,842")],
            _label=None, _last=None,
            _warder_bar_width=None, _warder_test_marker=False,
            _timer=types.SimpleNamespace(start=lambda *args: None),
            _diag=lambda *args: None,
        )
        fn = method("postWidgetCreate")
        # The postWidgetCreate AST function resolves eLabel/eSize globally.
        with patch.dict(fn.__globals__, {
            "eLabel": FakeLabel,
            "eSize": lambda width, height: (width, height),
        }):
            fn(mock, canvas)
        self.assertEqual(canvas.sizes, [(1065, 842)])

    def test_rendering_same_frame_is_cached(self):
        self.assertTrue(self.draw())
        initial = len(self.renderer.instance.calls)
        self.assertTrue(self.draw())
        self.assertEqual(len(self.renderer.instance.calls), initial)

    def test_receiver_width_override_and_test_only_marker(self):
        self.renderer._warder_bar_width = 90
        self.renderer._warder_test_marker = True
        self.assertTrue(self.draw())
        writes = [x for x in self.renderer.instance.calls if x[0] == "write"]
        for _, (x, y, width, height), *_ in writes:
            self.assertLessEqual(x + width, 700 - 25 - 90 - 12)
        marks = [x for x in self.renderer.instance.calls if x[0] == "fill"
                 and x[1] == (925, 14, 24, 14)]
        self.assertEqual(len(marks), 1)

    def test_private_skin_attributes_are_consumed_safely(self):
        target = types.SimpleNamespace(
            skinAttributes=[("warderProgressWidth", "90"),
                            ("warderTestMarker", "1"),
                            ("size", "1065,842")],
            _warder_bar_width=None, _warder_test_marker=False,
            _diag=lambda *args: None)
        f = method("applySkin")
        class StubRenderer:
            @staticmethod
            def applySkin(self, desktop, parent):
                return True
        with patch.dict(f.__globals__, {"Renderer": StubRenderer}):
            self.assertTrue(f(target, None, None))
        self.assertEqual(target._warder_bar_width, 90)
        self.assertTrue(target._warder_test_marker)
        self.assertEqual(target.skinAttributes, [("size", "1065,842")])

    def test_progress_redraw_obscures_transparent_underlay(self):
        self.renderer.instance.calls.clear()
        method("_draw_progress")(self.renderer, 870, 37, 90, 37, 0.35)
        fills = [x for x in self.renderer.instance.calls if x[0] == "fill"]
        self.assertGreaterEqual(len(fills), 6)
        self.assertEqual(fills[0][1], (870, 50, 90, 10))
        self.assertEqual(fills[0][2], "#000000")
        self.assertTrue(any(item[2] == "#dfdfdf" for item in fills))
        self.assertTrue(all(item[1][2] > 0 and item[1][3] > 0 for item in fills))

    def test_diagnostics_are_bounded_and_fail_open(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            logfile = Path(d) / "diagnostics.log"
            instance = types.SimpleNamespace(_diag_seen=set())
            def fake_open(filename, mode):
                self.assertEqual(mode, "a")
                return logfile.open("a", encoding="utf-8")
            fn = method("_diag")
            with patch.dict(fn.__globals__, {"open": fake_open}):
                for i in range(40):
                    fn(instance, "code%d" % i, "no event titles")
            lines = logfile.read_text().splitlines()
            self.assertEqual(len(lines), 32)
            self.assertTrue(lines[0].startswith("code0 "))
            self.assertTrue(lines[-1].startswith("code31 "))

    def test_renderer_is_fail_open_and_default_only(self):
        content = RENDERER.read_text(encoding="utf-8")
        self.assertIn("component.l.setElementFont(component.l.celServiceInfo, self._quiet_font)", content)
        self.assertIn('self._quiet_font = gFont("Regular", 1)', content)
        self.assertNotIn("setElementFont(component.l.celServiceInfo, None)", content)
        self.assertIn("self._restore_native()", content)
        self.assertIn("component.instance.invalidate()", content)
        self.assertIn("self._label.setNoWrap(1)", content)
        self.assertIn("self._label.resize(eSize(4096, 120))", content)
        self.assertIn("instance.setSize(eSize(width, height))", content)
        self.assertIn("self.instance.fillRect(", content)
        self.assertIn("self._draw_progress(bar_left", content)
        self.assertIn("if not drawing:", content)
        self.assertNotIn("fontSize = 0", content)
        self.assertNotIn("self.instance.flush()", content)
        xml = (ROOT / "source/package-root/usr/share/enigma2/hd_glass17/skin.xml").read_text(encoding="utf-8")
        self.assertNotIn('render="WarderChannelEpgClip"', xml)


if __name__ == "__main__":
    unittest.main()
