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

    def test_big_renderer_respects_downloaded_image_and_approved_ids(self):
        source = (RENDERERS / "g17MenuEntry2.py").read_text(encoding="utf-8")
        self.assertIn('if pixpath == self.default:', source)
        self.assertLess(source.index("if not fileExists(pixpath):"),
                        source.index("if pixpath == self.default:"))
        for entry_id, image in (
            ("warder_radio_mainmenu", "warder_radio.png"),
            ("PiconHub_Warder_Evolution", "warder_piconhub.png"),
            ("glass_sys_utils", "warder_gsu.png"),
            ("FHD_Glass17_Setup", "FHD_Glass17_Setup.png"),
            ("warder_fullhdglass_settings", "FHD_Glass17_Setup.png"),
        ):
            with self.subTest(entry_id=entry_id):
                self.assertIn('"' + entry_id + '": "' + image + '"', source)
        self.assertIn("if fileExists(candidate):", source)
        # No unapproved image is generated or downloaded as a fallback.
        self.assertIn('candidate = "/usr/share/enigma2/hd_glass17/menu/" + art', source)

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
