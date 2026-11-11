#!/usr/bin/env python3
"""Offline guard for Warder-only Neutrino short-OK mapping."""
from pathlib import Path
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
        self.assertNotIn("CHANSEL_FILE", body)
        self.assertNotIn("KMP_FILE", body)


if __name__ == "__main__":
    unittest.main()
