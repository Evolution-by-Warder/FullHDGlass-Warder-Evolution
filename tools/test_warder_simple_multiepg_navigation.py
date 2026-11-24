#!/usr/bin/env python3
"""Offline regression tests: yellow/blue traverse events ONLY in row Multi EPG.

No OpenATV import, GUI device, network request or system keymap modification.
"""
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "source/package-root/usr/lib/enigma2/python/"
          "Plugins/Extensions/setupGlass17/warderSimpleMultiEpg.py")
spec = importlib.util.spec_from_file_location("_warder_simple_multi_test", SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Label:
    def __init__(self, text="native"):
        self.text = text

    def setText(self, value):
        self.text = value


def config(skin="hd_glass17/skin.xml", language="cs_CZ"):
    return SimpleNamespace(
        skin=SimpleNamespace(primary_skin=SimpleNamespace(value=skin)),
        osd=SimpleNamespace(language=SimpleNamespace(value=language)),
    )


def modern_screen():
    class Multi:
        def __init__(self, type_value=7, skin="EPGSelectionMulti"):
            self.type = type_value
            self.skinName = skin
            self.bouquetlist_active = False
            self.widgets = {"key_yellow": Label(), "key_blue": Label()}
            self.actions = []
            self.selection_calls = 0

        def __getitem__(self, key):
            return self.widgets[key]

        def _btn_yellow(self):
            self.actions.append("native-yellow")

        def _btn_blue(self):
            self.actions.append("native-blue")

        def leftPressed(self):
            self.actions.append("left-event")

        def rightPressed(self):
            self.actions.append("right-event")

        def closeEventViewDialog(self):
            self.actions.append("close-event")

        def onSelectionChanged(self):
            self.selection_calls += 1
            self["key_yellow"].setText("native yellow")
            self["key_blue"].setText("native blue")

    return Multi


def legacy_screen():
    class Legacy:
        def __init__(self, type_value=7, skin="EPGSelectionMulti"):
            self.type = type_value
            self.skinName = skin
            self.bouquetlist_active = False
            self.widgets = {"key_yellow": Label(), "key_blue": Label()}
            self.actions = []

        def __getitem__(self, key):
            return self.widgets[key]

        def yellowButtonPressed(self):
            self.actions.append("native-yellow")

        def blueButtonPressed(self):
            self.actions.append("native-blue")

        def leftPressed(self):
            self.actions.append("left-event")

        def rightPressed(self):
            self.actions.append("right-event")

    return Legacy


class MultiEpgNavigationTests(unittest.TestCase):
    def test_modern_yellow_blue_are_previous_next_events_and_update_labels(self):
        klass = modern_screen()
        app = config()
        info = SimpleNamespace(instance=SimpleNamespace(LongButtonPressed=False))

        epg = SimpleNamespace(EPG_TYPE_MULTI=7, EPGSelectionMulti=klass)
        self.assertTrue(module.install(epg, app, info))
        screen = klass()
        self.assertEqual(screen["key_yellow"].text, "Předchozí")
        self.assertEqual(screen["key_blue"].text, "Následující")
        self.assertEqual(screen._btn_yellow(), 1)
        self.assertEqual(screen._btn_blue(), 1)
        self.assertEqual(screen.actions, [
            "close-event", "left-event", "close-event", "right-event"
        ])
        screen.onSelectionChanged()
        self.assertEqual(screen.selection_calls, 1)
        self.assertEqual(screen["key_yellow"].text, "Předchozí")
        self.assertEqual(screen["key_blue"].text, "Následující")
        before = klass._btn_yellow
        self.assertTrue(module.install(epg, app, info))
        self.assertIs(klass._btn_yellow, before)

    def test_modern_long_press_keeps_native_binding(self):
        klass = modern_screen()
        info = SimpleNamespace(instance=SimpleNamespace(LongButtonPressed=True))
        module.install(SimpleNamespace(EPG_TYPE_MULTI=7, EPGSelectionMulti=klass),
                       config(), info)
        screen = klass()
        screen._btn_yellow()
        screen._btn_blue()
        self.assertEqual(screen.actions, ["native-yellow", "native-blue"])

    def test_legacy_short_colours_follow_native_left_right(self):
        klass = legacy_screen()
        epg = SimpleNamespace(EPG_TYPE_MULTI=7, EPGSelection=klass)
        self.assertTrue(module.install(epg, config(language="sk_SK")))
        screen = klass()
        self.assertEqual(screen["key_yellow"].text, "Predchádzajúci")
        self.assertEqual(screen["key_blue"].text, "Nasledujúci")
        self.assertEqual(screen.yellowButtonPressed(), 1)
        self.assertEqual(screen.blueButtonPressed(), 1)
        self.assertEqual(screen.actions, ["left-event", "right-event"])

    def test_other_skin_and_other_epg_screen_are_untouched(self):
        klass = modern_screen()
        epg = SimpleNamespace(EPG_TYPE_MULTI=7, EPGSelectionMulti=klass)
        app = config(skin="other/skin.xml")
        self.assertTrue(module.install(epg, app))
        row = klass()
        row._btn_yellow()
        row._btn_blue()
        self.assertEqual(row.actions, ["native-yellow", "native-blue"])
        self.assertEqual(row["key_yellow"].text, "native")
        app.skin.primary_skin.value = "hd_glass17/skin.xml"
        graph = klass(type_value=3, skin="GraphicalEPGPIG")
        graph._btn_yellow()
        graph._btn_blue()
        self.assertEqual(graph.actions, ["native-yellow", "native-blue"])
        self.assertEqual(graph["key_blue"].text, "native")
        other = klass(type_value=7, skin="EPGSelection")
        other._btn_yellow()
        self.assertEqual(other.actions, ["native-yellow"])

    def test_bouquet_list_retains_native_colour_functions(self):
        klass = modern_screen()
        module.install(SimpleNamespace(EPG_TYPE_MULTI=7, EPGSelectionMulti=klass), config())
        screen = klass()
        screen.bouquetlist_active = True
        screen._btn_yellow()
        screen._btn_blue()
        self.assertEqual(screen.actions, ["native-yellow", "native-blue"])

    def test_missing_native_buttons_fails_closed(self):
        class Incomplete:
            def __init__(self):
                pass
        cls = Incomplete
        epg = SimpleNamespace(EPG_TYPE_MULTI=7, EPGSelectionMulti=cls)
        self.assertFalse(module.install(epg, config()))
        self.assertNotIn("_warderSimpleMultiEpgInstalled", cls.__dict__)

    def test_fallback_if_image_lacks_event_mover(self):
        klass = modern_screen()
        module.install(SimpleNamespace(EPG_TYPE_MULTI=7, EPGSelectionMulti=klass), config())
        screen = klass()
        screen.leftPressed = None
        screen._btn_yellow()
        self.assertEqual(screen.actions, ["native-yellow"])

    def test_real_multiepg_skin_has_label_sources_without_geometry_change(self):
        path = ROOT / "source/package-root/usr/share/enigma2/hd_glass17/skin.xml"
        xml = path.read_text(encoding="utf-8")
        screen = xml.split('<screen name="EPGSelectionMulti"', 1)[1].split("</screen>", 1)[0]
        self.assertIn('source="key_yellow"', screen)
        self.assertIn('source="key_blue"', screen)
        self.assertIn('name="list"', screen)


if __name__ == "__main__":
    unittest.main()

