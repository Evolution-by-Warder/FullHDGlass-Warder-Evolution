#!/usr/bin/env python3
"""Offline guard for Warder-only Neutrino short-OK mapping."""
from pathlib import Path
import ast
from types import SimpleNamespace
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py"
KEYMAP = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/keymap.xml"


class NeutrinoShortOKTest(unittest.TestCase):
    def test_keymap_scoped_to_neutrino_only(self):
        root = ET.parse(KEYMAP).getroot()
        contexts = {node.attrib["context"]: node for node in root.findall("map")}
        self.assertEqual(set(contexts), {
            "g17Actions", "g17Actions_neutrino",
            "g17ActionsSpecial", "g17Actions_neutrinoSpecial",
        })
        for name, node in contexts.items():
            ok = [item for item in node.findall("key") if item.get("id") == "KEY_OK"]
            self.assertEqual(len(ok), 1, name)
            if "neutrino" in name:
                self.assertEqual(ok[0].get("mapto"), "warder_neutrino_channel_list")
                self.assertEqual(ok[0].get("flags"), "b")
                exit_keys = [item for item in node.findall("key") if item.get("id") == "KEY_EXIT"]
                self.assertEqual(exit_keys[0].get("mapto"), "ok_pressed")
            else:
                self.assertEqual(ok[0].get("mapto"), "ok_pressed")
                self.assertEqual(ok[0].get("flags"), "m")
        self.assertFalse(any(key.get("flags") == "l" for key in root.iter("key")))

    def test_handler_uses_native_api_not_system_patching(self):
        source = PLUGIN.read_text(encoding="utf-8")
        self.assertIn("InfoBarPlugins.warderNeutrinoChannelList17 = warderNeutrinoChannelList17", source)
        self.assertEqual(source.count('"warder_neutrino_channel_list": self.warderNeutrinoChannelList17'), 2)
        body = source.split("def warderNeutrinoChannelList17(self):", 1)[1].split("def controlWindow17(self):", 1)[0]
        self.assertIn("config.plugins.setupGlass17.par34.value", body)
        self.assertIn('"openServiceList"', body)
        self.assertIn("open_list()", body)
        self.assertIn('getattr(self, "LongButtonPressed", False)', body)
        self.assertIn('getattr(self.session, "current_dialog", None) is servicelist', body)
        self.assertNotIn("CHANSEL_FILE", body)
        self.assertNotIn("KMP_FILE", body)


    def test_native_api_dispatch_for_short_long_and_duplicate_ok(self):
        module = ast.parse(PLUGIN.read_text(encoding="utf-8"))
        handler = next(node for node in module.body
                       if isinstance(node, ast.FunctionDef)
                       and node.name == "warderNeutrinoChannelList17")
        class InfoBar:
            def __init__(self):
                self.called = 0
                self.servicelist = object()
                self.session = SimpleNamespace(current_dialog=None)
                self.LongButtonPressed = False
            def openServiceList(self):
                self.called += 1
        feature = SimpleNamespace(value=True)
        config = SimpleNamespace(plugins=SimpleNamespace(
            setupGlass17=SimpleNamespace(par34=feature)))
        sandbox = {"InfoBar": InfoBar, "config": config}
        exec(compile(ast.Module(body=[handler], type_ignores=[]),
                     str(PLUGIN), "exec"), sandbox)
        fn = sandbox["warderNeutrinoChannelList17"]

        box = InfoBar()
        fn(box)
        self.assertEqual(box.called, 1, "short OK should open the channel list")
        box.LongButtonPressed = True
        fn(box)
        self.assertEqual(box.called, 1, "long OK must not reopen the list")
        box.LongButtonPressed = False
        box.session.current_dialog = box.servicelist
        fn(box)
        self.assertEqual(box.called, 1, "already-open list must be left untouched")
        box.session.current_dialog = None
        feature.value = False
        fn(box)
        self.assertEqual(box.called, 1, "disabled Neutrino must not intercept OK")
        feature.value = True
        fn(object())
        self.assertEqual(box.called, 1)



if __name__ == "__main__":
    unittest.main()
