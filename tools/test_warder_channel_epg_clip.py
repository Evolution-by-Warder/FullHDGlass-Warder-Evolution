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
        self.instance = self
        self.l = types.SimpleNamespace(celServiceInfo=2)

    def getList(self):
        return self.refs

    def getTopIndex(self):
        return 0

    def getCurrentIndex(self):
        return 1

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
            _opaque_black="#000000", _progress_border="#dfdfdf")
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
            _timer=types.SimpleNamespace(start=lambda *args: None),
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
