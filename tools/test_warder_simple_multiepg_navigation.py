#!/usr/bin/env python3
"""Offline regression tests: yellow/blue traverse events ONLY in row Multi EPG.

No OpenATV import, GUI device, network request or system keymap modification.
"""
import importlib.util
import json
import re
import hashlib
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


class AuxiliaryLanguageTests(unittest.TestCase):
    LANGUAGES = set("al cs de el en es et fa fr hu it lt nl pl pt ro ru sk tr uk zh".split())

    def test_all_21_localized_buttons_and_aliases(self):
        self.assertEqual(set(module.LABELS), self.LANGUAGES)
        for lang in self.LANGUAGES:
            klass = modern_screen()
            module.install(SimpleNamespace(EPG_TYPE_MULTI=7, EPGSelectionMulti=klass), config(language=lang))
            screen = klass()
            self.assertEqual((screen["key_yellow"].text, screen["key_blue"].text), module.LABELS[lang])
        for alias, lang in (("sq_AL","al"),("gr_GR","el"),("ua_UA","uk"),("cn_CN","zh"),("cz_CZ","cs")):
            self.assertEqual(module._language(config(language=alias)),lang)

    def test_shared_catalog_integrity_and_placeholders(self):
        core = SOURCE.parent / "warderRadioCore"
        catalog = json.loads((core / "data/translations.json").read_text(encoding="utf-8"))
        self.assertEqual(set(catalog), self.LANGUAGES)
        self.assertEqual(len(catalog["en"]),128)
        for lang, values in catalog.items():
            self.assertEqual(set(values), set(catalog["en"]))
            for key, value in values.items():
                self.assertTrue(value.strip(), (lang, key))
                self.assertEqual(re.findall(r"%[sd%]",key),re.findall(r"%[sd%]",value),(lang,key))
        record = json.loads((core / "SOURCE.json").read_text())
        for name, digest in record["sha256"].items():
            self.assertEqual(hashlib.sha256((core / name).read_bytes()).hexdigest(),digest)

    def test_updater_and_shared_core_fallback(self):
        def load(name, path):
            spec = importlib.util.spec_from_file_location(name,path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
        updater = load("warder_update_text", SOURCE.parent / "warderUpdateText.py")
        i18n = load("warder_shared_i18n", SOURCE.parent / "warderRadioCore/warder_i18n.py")
        self.assertEqual(set(updater.TEXT),self.LANGUAGES)
        self.assertEqual(set(i18n.SUPPORTED),self.LANGUAGES)
        for lang in self.LANGUAGES:
            for kind in updater.TEXT["en"]:
                self.assertTrue(updater.update_text(kind,"PRODUCT",current="OLD",new="NEW",notes="NOTES",error="ERROR",language=lang))
        self.assertEqual(i18n.translate("Stiahnuť","sq_AL"),"Shkarko")
        self.assertEqual(i18n.translate("Stiahnuť","gr_GR"),"Λήψη")
        self.assertEqual(i18n.translate("Stiahnuť","unknown"),"Download")
        self.assertEqual(updater.update_text("confirm","x",language="sq_AL"),"Konfirmo")
        self.assertEqual(updater.update_text("confirm","x",language="unknown"),"Confirm")


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

