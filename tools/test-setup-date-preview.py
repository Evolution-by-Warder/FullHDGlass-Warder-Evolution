#!/usr/bin/env python3
"""Static regression checks for date-preview wiring in Enigma2 setup."""
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py"

class SetupDatePreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE.read_text(encoding="utf-8")
        match = re.search(r'class setupGlass17ScreenSetup\(Screen, ConfigListScreen\):\s+skin\s*=\s*"""(.*?)"""', cls.source, re.S)
        assert match, "setup screen skin not found"
        cls.skin = ET.fromstring(match.group(1))

    def test_preview_is_both_registered_and_rendered(self):
        self.assertIn('self["selected_item"] = StaticText("")', self.source)
        widgets = self.skin.findall(".//widget[@source='selected_item']")
        self.assertEqual(len(widgets), 1)
        self.assertEqual(widgets[0].get("render"), "Label")
        self.assertTrue(widgets[0].get("font"))
        self.assertTrue(widgets[0].get("size"))

    def test_help_and_preview_are_in_same_screen(self):
        helps = self.skin.findall(".//widget[@name='help_txt']")
        self.assertEqual(len(helps), 1)
        self.assertIn('filename == "127-1"', self.source)
        self.assertIn('datetime.now().strftime(', self.source)
        self.assertIn('self["selected_item"].setText("")', self.source)

    def test_all_main_date_settings_use_shared_preview(self):
        for index in (127, 131, 132, 133, 134, 185, 186):
            self.assertRegex(self.source, rf'par{index}\.value')
        formats = re.search(r'dFormat\s*=\s*\[(.*?)\]', self.source, re.S)
        self.assertIsNotNone(formats)
        self.assertEqual(len(re.findall(r'_\("Type"\)', formats.group(1))), 10)

    def test_registered_visible_widgets_are_declared(self):
        start = self.source.index("class setupGlass17ScreenSetup(Screen, ConfigListScreen):")
        stop = self.source.find("\nclass ", start + 8)
        body = self.source[start:stop if stop != -1 else None]
        assigned = set(re.findall(r'self\[["\']([^"\']+)["\']\]\s*=', body))
        declared = {node.get("name") or node.get("source") for node in self.skin.findall(".//widget")}
        allowed_invisible = {"actions"}
        self.assertFalse(assigned - declared - allowed_invisible, assigned - declared - allowed_invisible)

if __name__ == "__main__":
    unittest.main()
