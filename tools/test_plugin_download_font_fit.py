"""Regression guard for native PluginDownloadBrowser title/version sizing.

OpenATV PluginList.PluginDownloadComponent receives its two font aliases from
skin XML. A 32px primary font clipped long package versions in the approved
1920x1080 download/remove screen. Keep the original list geometry intact.
"""
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIN = ROOT / "source/package-root/usr/share/enigma2/hd_glass17/skin.xml"


class PluginDownloadTextFitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = ET.fromstring(SKIN.read_text(encoding="utf-8"))

    def test_native_download_font_is_legible_and_bounded(self):
        alias = self.root.find(".//alias[@name='PluginBrowser0']")
        self.assertIsNotNone(alias)
        self.assertEqual(alias.get("font"), "Prive4")
        self.assertEqual(alias.get("size"), "26")
        desc = self.root.find(".//alias[@name='PluginBrowser1']")
        self.assertEqual(desc.get("size"), "24")

    def test_install_and_remove_share_unmodified_native_screen(self):
        screen = self.root.find(".//screen[@name='PluginDownloadBrowser']")
        self.assertIsNotNone(screen)
        self.assertEqual(screen.get("size"), "1920,1080")
        widget = screen.find("widget[@name='list']")
        self.assertIsNotNone(widget)
        self.assertEqual(widget.get("position"), "190,200")
        self.assertEqual(widget.get("size"), "1540,720")
        self.assertEqual(widget.get("itemHeight"), "80")
        self.assertIsNotNone(screen.find("widget[@source='Title']"))

    def test_native_icon_and_text_offsets_remain_unchanged(self):
        want = {
            "PluginBrowserDownloadName": "125,3,45",
            "PluginBrowserDownloadDescr": "125,42,39",
            "PluginBrowserDownloadIcon": "2,0,120,75",
        }
        for name, value in want.items():
            with self.subTest(name=name):
                param = self.root.find(".//parameter[@name='%s']" % name)
                self.assertIsNotNone(param)
                self.assertEqual(param.get("value"), value)


if __name__ == "__main__":
    unittest.main()
