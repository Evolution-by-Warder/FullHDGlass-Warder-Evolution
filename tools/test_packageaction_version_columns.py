"""Guard OpenATV 8.1 PackageAction name/version rendering geometry.

Unlike PluginDownloadBrowser, PackageAction renders the installer/uninstaller
package rows through a TemplatedMultiContent with right-aligned version text.
The original 390 px version field clipped long OpenATV package versions.
"""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SKIN = ROOT / "source/package-root/usr/share/enigma2/hd_glass17/skin.xml"


class PackageActionColumns(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = ET.fromstring(SKIN.read_text(encoding="utf-8"))
        cls.screen = cls.root.find(".//screen[@name='PackageAction']")
        assert cls.screen is not None
        cls.template = cls.screen.find("widget[@source='plugins']/convert")
        assert cls.template is not None
        cls.template = cls.template.text or ""

    def test_name_and_version_are_disjoint(self):
        name = re.search(
            r'MultiContentEntryText\(pos=\((\d+),\s*2\),\s*size=\((\d+),\s*34\),'
            r'\s*font=1,\s*flags=RT_VALIGN_CENTER,\s*text=3\)',
            self.template)
        version = re.search(
            r'MultiContentEntryText\(pos=\((\d+),\s*2\),\s*size=\((\d+),\s*34\),'
            r'\s*font=1,\s*flags=RT_VALIGN_CENTER\s*\|\s*RT_HALIGN_RIGHT,\s*text=5\)',
            self.template)
        self.assertIsNotNone(name)
        self.assertIsNotNone(version)
        nx, nw = map(int, name.groups())
        vx, vw = map(int, version.groups())
        self.assertEqual((nx, nw), (95, 690))
        self.assertEqual((vx, vw), (800, 630))
        self.assertLessEqual(nx + nw + 10, vx)
        self.assertLessEqual(vx + vw + 20, 1450)

    def test_item_geometry_and_font_are_preserved(self):
        self.assertIn('MultiContentEntryText(pos=(95, 0), size=(1430, 70), font=0', self.template)
        self.assertIn('MultiContentEntryText(pos=(95, 36), size=(1335, 30), font=2', self.template)
        self.assertIn('MultiContentEntryPixmapAlphaBlend(pos=(1450, 5), size=(60, 60), png=7', self.template)
        self.assertIn('gFont("Prive3", 33)', self.template)
        self.assertIn('gFont("Prive3", 27)', self.template)
        self.assertIn('gFont("Prive3", 24)', self.template)
        self.assertIn('"itemHeight": 70', self.template)
        self.assertEqual(self.screen.get("size"), "1650,840")
        self.assertEqual(self.screen.find("widget[@source='plugins']").get("size"), "1590,585")

    def test_native_plugin_download_browser_untouched(self):
        screen = self.root.find(".//screen[@name='PluginDownloadBrowser']")
        self.assertIsNotNone(screen)
        self.assertEqual(screen.find("widget[@name='list']").get("size"), "1540,720")
        alias = self.root.find(".//alias[@name='PluginBrowser0']")
        self.assertEqual(alias.get("size"), "32")


if __name__ == "__main__":
    unittest.main()
