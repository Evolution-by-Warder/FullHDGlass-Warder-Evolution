#!/usr/bin/env python3
"""Native ConfigList spacing regression, without receiver-side Enigma2."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderNativeConfigSpacing.py"
spec = importlib.util.spec_from_file_location("warderNativeConfigSpacing", FILE)
spacing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spacing)


class FakeContent:
    def __init__(self):
        self.separators = []

    def setSeperation(self, value):
        self.separators.append(value)


class FakeInstance:
    def __init__(self, width):
        self.width = width

    def size(self):
        return self

    def width(self):
        return self.width


class NativeConfig:
    def __init__(self, width):
        self.l = FakeContent()
        self.instance = types.SimpleNamespace(size=lambda: types.SimpleNamespace(width=lambda: width))
        self.native_applied = 0

    def applySkin(self, desktop, parent):
        self.native_applied += 1
        return "native-result"


class NativeConfigSpacingTests(unittest.TestCase):
    def native(self):
        # A different class for each test keeps the monkey patch isolated.
        klass = type("ConfigList", (NativeConfig,), {})
        package = types.ModuleType("Components")
        config = types.ModuleType("Components.ConfigList")
        config.ConfigList = klass
        return klass, {"Components": package, "Components.ConfigList": config}

    def test_native_fullhd_screens_have_nonoverlapping_label_columns(self):
        cls, modules = self.native()
        with patch.dict(sys.modules, modules):
            self.assertTrue(spacing.install())
            for width in (1560, 1590, 1650):
                obj = cls(width)
                self.assertEqual(obj.applySkin(None, None), "native-result")
                expected = spacing.separator_for_width(width)
                self.assertEqual(obj.l.separators, [expected])
                self.assertGreaterEqual(expected, 850 if width >= 1560 else 800)
                self.assertGreaterEqual(width - expected, 450)
                self.assertEqual(obj.native_applied, 1)

    def test_narrow_plugin_and_preview_lists_keep_native_spacing(self):
        cls, modules = self.native()
        with patch.dict(sys.modules, modules):
            spacing.install()
            for width in (500, 825, 910, 1199):
                obj = cls(width)
                obj.applySkin(None, None)
                self.assertEqual(obj.l.separators, [])

    def test_scaling_tracks_widget_width(self):
        self.assertEqual(spacing.separator_for_width(1590), 874)
        self.assertEqual(spacing.separator_for_width(2120), 1166)
        self.assertIsNone(spacing.separator_for_width(825))

    def test_install_idempotent(self):
        cls, modules = self.native()
        with patch.dict(sys.modules, modules):
            self.assertTrue(spacing.install())
            first = cls.applySkin
            self.assertTrue(spacing.install())
            self.assertIs(cls.applySkin, first)
            obj = cls(1590)
            obj.applySkin(None, None)
            self.assertEqual(len(obj.l.separators), 1)

    def test_native_errors_not_masked(self):
        cls, modules = self.native()
        def error(self, desktop, parent):
            raise ValueError("native screen error")
        cls.applySkin = error
        with patch.dict(sys.modules, modules):
            spacing.install()
            with self.assertRaisesRegex(ValueError, "native screen error"):
                cls(1590).applySkin(None, None)

    def test_missing_native_api_keeps_screen_usable(self):
        cls, modules = self.native()
        with patch.dict(sys.modules, modules):
            spacing.install()
            obj = cls(1590)
            obj.l = object()
            self.assertEqual(obj.applySkin(None, None), "native-result")
            self.assertEqual(obj.native_applied, 1)


if __name__ == "__main__":
    unittest.main()
