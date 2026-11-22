#!/usr/bin/env python3
"""Offline regression checks for the FullHDGlass common radio saver."""
import ast
import importlib.util
import pathlib
import sys
import types
import unittest
from unittest.mock import patch
from xml.etree import ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17"


def load_pure():
    spec = importlib.util.spec_from_file_location("warderRadioSaverLayout", PLUGIN / "warderRadioSaverLayout.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


layout = load_pure()


class LayoutChecks(unittest.TestCase):
    def test_delay_choices(self):
        self.assertEqual([layout.delay_seconds(x) for x in ("0", "10", "20", "30", "60")],
                         [0, 10, 20, 30, 60])
        self.assertEqual([layout.delay_seconds(x) for x in ("abc", -1, 1, 90, None)],
                         [0, 0, 0, 0, 0])

    def test_xml_widgets_are_unique_and_fully_onscreen(self):
        markup, positions = layout.make_widgets()
        root = ET.fromstring("<skin>" + markup + "</skin>")
        names = [item.attrib["name"] for item in root]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(set(names), set(positions))
        self.assertEqual(positions["saver_black"], (0, 0, 1920, 1080))
        self.assertTrue({"saver_picon", "saver_cover", "saver_artist",
                         "saver_track", "saver_time", "saver_signal"} <= set(names))
        for name, (x, y, w, h) in positions.items():
            if name == "saver_black":
                continue
            self.assertGreaterEqual(x - 90, 0, name)
            self.assertGreaterEqual(y - 60, 0, name)
            self.assertLessEqual(x + w + 90, 1920, name)
            self.assertLessEqual(y + h + 60, 1080, name)

    def test_motion_is_bounded(self):
        offset, direction = (0, 0), (1, 1)
        points = set()
        for _ in range(200):
            offset, direction = layout.bounded_motion(offset, direction)
            self.assertLessEqual(abs(offset[0]), 90)
            self.assertLessEqual(abs(offset[1]), 60)
            points.add(offset)
        self.assertGreater(len(points), 20)


class StaticChecks(unittest.TestCase):
    def test_every_modified_python_file_parses(self):
        for file in ("plugin.py", "screenSaver.py", "warderRadioSaverController.py",
                     "warderRadioSaverLayout.py"):
            with self.subTest(file=file):
                ast.parse((PLUGIN / file).read_text(encoding="utf-8"))

    def test_legacy_tuner_gate_removed(self):
        source = (PLUGIN / "plugin.py").read_text(encoding="utf-8")
        self.assertIn("radioSaverDelay = ConfigSelection", source)
        self.assertIn("_installRadioSaver(self, config.plugins.setupGlass17.radioSaverDelay)", source)
        self.assertNotIn("if isRadioService and keyManage.TunerTest()", source)


class ControllerChecks(unittest.TestCase):
    def setUp(self):
        self.package = types.ModuleType("saver_test_pkg")
        self.package.__path__ = [str(PLUGIN)]
        self.timer_calls = []
        class Timer:
            def __init__(inner):
                inner.callback = []
            def start(inner, delay, periodic=False):
                self.timer_calls.append((delay, periodic))
            def stop(inner):
                pass
        class Actions:
            def __init__(inner):
                inner.callback = None
            def bindAction(inner, context, priority, callback):
                inner.callback = callback
            def unbindAction(inner, context, callback):
                inner.callback = None
        self.actions = Actions()
        self.modules = {
            "saver_test_pkg": self.package,
            "saver_test_pkg.warderRadioSaverLayout": layout,
            "saver_test_pkg.screenSaver": types.SimpleNamespace(ScreenSaverScreen=object),
            "enigma": types.SimpleNamespace(eTimer=Timer,
                eActionMap=types.SimpleNamespace(getInstance=lambda: self.actions)),
            "Components": types.ModuleType("Components"),
            "Components.Converter": types.ModuleType("Components.Converter"),
            "Components.Converter.WarderRadioOnly": types.SimpleNamespace(
                is_radio_reference=lambda ref: bool(ref and (
                    ref.kind in ("radio", "dab", "stream")))),
        }
        self.inject = patch.dict(sys.modules, self.modules)
        self.inject.start()
        spec = importlib.util.spec_from_file_location(
            "saver_test_pkg.warderRadioSaverController",
            PLUGIN / "warderRadioSaverController.py")
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.clock = 1000.0
        self.time_mock = patch.object(self.module.time, "monotonic", lambda: self.clock)
        self.time_mock.start()
        self.bar = types.SimpleNamespace(onClose=[])
        self.bar.session = types.SimpleNamespace(
            nav=types.SimpleNamespace(getCurrentlyPlayingServiceReference=lambda: self.ref),
            current_dialog=self.bar)
        self.opened = []
        class Dialog:
            def close(inner):
                self.bar.session.current_dialog = self.bar
                self.opened[-1][0]()
        def open_saver(callback, screen):
            self.opened.append((callback, screen))
            self.bar.session.current_dialog = Dialog()
            return self.bar.session.current_dialog
        self.bar.session.openWithCallback = open_saver
        self.ref = types.SimpleNamespace(kind="radio", toString=lambda: "1:0:2:1")
        self.setting = types.SimpleNamespace(value="10")

    def tearDown(self):
        self.time_mock.stop()
        self.inject.stop()

    def test_all_radio_kinds_delay_and_first_remote_key(self):
        for kind in ("radio", "dab", "stream"):
            with self.subTest(kind=kind):
                self.ref.kind = kind
                ctrl = self.module.UnifiedRadioSaver(self.bar, self.setting)
                ctrl.poll()
                self.clock += 11
                ctrl.poll()
                self.assertEqual(len(self.opened), 1)
                self.assertIsNotNone(ctrl.dialog)
                self.assertEqual(ctrl._key("ok", 0), 1)
                self.assertIsNone(ctrl.dialog)
                self.assertIs(self.bar.session.current_dialog, self.bar)
                ctrl.close()
                self.opened.clear()
                self.clock += 1

    def test_tv_and_foreground_plugin_never_show_saver(self):
        ctrl = self.module.UnifiedRadioSaver(self.bar, self.setting)
        self.ref = types.SimpleNamespace(kind="tv", toString=lambda: "1:0:1:1")
        ctrl.poll()
        self.clock += 30
        ctrl.poll()
        self.assertFalse(self.opened)
        self.ref = types.SimpleNamespace(kind="stream", toString=lambda: "4097:0:2:1")
        self.bar.session.current_dialog = object()
        ctrl.poll()
        self.clock += 30
        ctrl.poll()
        self.assertFalse(self.opened)
        ctrl.close()

    def test_switch_station_resets_inactivity(self):
        ctrl = self.module.UnifiedRadioSaver(self.bar, self.setting)
        ctrl.poll()
        self.clock += 9
        self.ref = types.SimpleNamespace(kind="dab", toString=lambda: "DAB:new")
        ctrl.poll()
        self.clock += 2
        ctrl.poll()
        self.assertFalse(self.opened)
        self.clock += 9
        ctrl.poll()
        self.assertEqual(len(self.opened), 1)
        ctrl.close()


if __name__ == "__main__":
    unittest.main()
