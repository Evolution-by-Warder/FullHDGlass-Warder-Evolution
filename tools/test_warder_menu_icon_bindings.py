"""Guard exact approved Warder main-menu icon IDs across native menu modes."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RENDERERS = ROOT / "source/package-root/usr/lib/enigma2/python/Components/Renderer"
MENU = ROOT / "source/package-root/usr/lib/enigma2/python/Screens/Menu-new17.py"
APPROVED = (
    "glass_sys_utils",
    "PiconHub_Warder_Evolution",
    "warder_radio_mainmenu",
    "warder_youtube_mainmenu",
    "FHD_Glass17_Setup",
)


class ApprovedMenuBindings(unittest.TestCase):
    def test_big_renderer_uses_exact_enigma_id(self):
        source = (RENDERERS / "g17MenuEntry2.py").read_text(encoding="utf-8")
        self.assertIn("self.source.entryName + self.pict + '.png'", source)

    def test_small_and_alternate_menu_can_reuse_approved_big_icons(self):
        small = (RENDERERS / "g17MenuEntry.py").read_text(encoding="utf-8")
        alternate = MENU.read_text(encoding="utf-8")
        for entry_id in APPROVED:
            with self.subTest(entry_id=entry_id):
                self.assertIn('"' + entry_id + '"', small)
                self.assertIn('"' + entry_id + '"', alternate)
        self.assertIn("fileExists(candidate_path)", small)
        self.assertIn("fileExists(candidate)", alternate)
        self.assertIn("else defPixpath", alternate)


if __name__ == "__main__":
    unittest.main()
