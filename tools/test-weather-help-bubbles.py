#!/usr/bin/env python3
"""UV/wind contextual preview regression; no Enigma2 imports required."""
import ast
import hashlib
import os
from pathlib import Path
import struct
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py"
IMAGES = PLUGIN.parent / "images/help"
EXPECTED = {
    "weather-uv-help.png": "5b1cb8ad89db6bf8b159b2b5585c3a3bac86419cb09f2dbcb555a22a62bba789",
    "weather-wind-help.png": "e07c01850d668f8dc19a70cbfe539a26c3a5f16b856b1927d644bf9723f3f7eb",
}

class FakeWidget:
    def __init__(self): self.actions = []
    def hide(self): self.actions.append("hide")
    def show(self): self.actions.append("show")
    def setText(self, text): self.actions.append(("text", text))

class ScreenStub:
    def __init__(self):
        self.widgets = {key: FakeWidget() for key in
                        ("helpPicon", "helpPiconFrame", "helpTxtAnim",
                         "selected_item", "help_txt", "help_pict")}
        self.loaded, self.samples = [], []
    def __getitem__(self, key): return self.widgets[key]
    def _warderLoadHelpPicture(self, path): self.loaded.append(path)
    def sampleColor(self, color): self.samples.append(color)

class WeatherHelpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = PLUGIN.read_text(encoding="utf-8")
        cls.tree = ast.parse(cls.source)
        cls.cls = next(n for n in cls.tree.body if isinstance(n, ast.ClassDef)
                       and n.name == "setupGlass17ScreenSetup")
        cls.method = next(n for n in cls.cls.body if isinstance(n, ast.FunctionDef)
                          and n.name == "doMyHelpWindow")

    def test_binary_graphics_approved_and_not_interchanged(self):
        for name, expected in EXPECTED.items():
            raw = (IMAGES / name).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), expected)
            self.assertTrue(raw.startswith(b"\x89PNG\r\n\x1a\n"))
            self.assertEqual(struct.unpack(">II", raw[16:24]), (882, 300))
            # Approved PNGs may be RGBA (type 6) or losslessly palette-encoded
            # with a tRNS alpha table (type 3). Do not regenerate artwork.
            color_type = raw[25]
            self.assertIn(color_type, (3, 6), "PNG must preserve transparency")
            if color_type == 3:
                cursor, chunks = 8, set()
                while cursor + 12 <= len(raw):
                    size = struct.unpack(">I", raw[cursor:cursor + 4])[0]
                    chunk = raw[cursor + 4:cursor + 8]
                    self.assertLessEqual(cursor + 12 + size, len(raw))
                    chunks.add(chunk)
                    cursor += size + 12
                    if chunk == b"IEND":
                        break
                self.assertIn(b"tRNS", chunks, "Indexed PNG must declare transparent palette entries")
        self.assertNotEqual(EXPECTED["weather-uv-help.png"],
                            EXPECTED["weather-wind-help.png"])

    def test_selector_switches_on_highlight_without_confirm(self):
        # Compile only the actual conditional from doMyHelpWindow; never import
        # receiver-only modules. This exercises the real branch body in isolation.
        uv = SimpleNamespace(value="AutoColors")
        wind = SimpleNamespace(value="AutoColors")
        cfg = SimpleNamespace(plugins=SimpleNamespace(setupGlass17=SimpleNamespace(
            par176=uv, par177=wind)))
        selected = next((n for n in ast.walk(self.method)
                         if isinstance(n, ast.If) and
                         ast.unparse(n.test) ==
                         "t in (config.plugins.setupGlass17.par176, config.plugins.setupGlass17.par177)"), None)
        self.assertIsNotNone(selected, "Both weather settings must have a preview callback")
        fn = ast.FunctionDef(name="run_preview", args=ast.arguments(
            posonlyargs=[], args=[ast.arg(arg="self"), ast.arg(arg="t")],
            kwonlyargs=[], kw_defaults=[], defaults=[], vararg=None, kwarg=None),
            body=[selected, ast.Return(value=ast.Constant(False))],
            decorator_list=[], returns=None, type_comment=None)
        module = ast.fix_missing_locations(ast.Module(body=[fn], type_ignores=[]))
        scope = {"config": cfg, "ENA_ANIM": True, "os": os, "__file__": str(PLUGIN)}
        exec(compile(module, str(PLUGIN), "exec"), scope)
        for item, name in ((uv, "weather-uv-help.png"), (wind, "weather-wind-help.png")):
            screen = ScreenStub()
            scope["run_preview"](screen, item)
            self.assertEqual([Path(v).name for v in screen.loaded], [name])
            self.assertEqual(screen.widgets["help_pict"].actions, ["show"])
            self.assertEqual(screen.widgets["help_txt"].actions, [("text", "")])
            for widget in ("helpPicon", "helpPiconFrame", "helpTxtAnim"):
                self.assertEqual(screen.widgets[widget].actions, ["hide"])
        screen = ScreenStub()
        self.assertFalse(scope["run_preview"](screen, object()))
        self.assertEqual(screen.loaded, [])

    def test_preserves_other_help_and_gui_geometry(self):
        self.assertIn('if t == config.plugins.setupGlass17.par230:', self.source)
        self.assertIn('elif t in (config.plugins.setupGlass17.par221,', self.source)
        self.assertIn('self._warderLoadHelpPicture(filename)', self.source)
        import re
        match = re.search(r'<widget name="help_pict" position="(\d+),(\d+)" size="(\d+),(\d+)"', self.source)
        self.assertIsNotNone(match)
        x,y,w,h = map(int, match.groups())
        self.assertTrue(0 <= x and 0 <= y and x+w <= 1920 and y+h <= 960)
        self.assertLess(abs(w/h - 882/300), 0.02)

if __name__ == "__main__":
    unittest.main()
