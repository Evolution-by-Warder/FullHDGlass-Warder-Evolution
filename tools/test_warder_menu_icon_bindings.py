"""Guard exact approved Warder main-menu icon IDs across native menu modes."""
from pathlib import Path
import unittest
import importlib.util
import tempfile
import hashlib
import subprocess
import sys

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


class MissingMenuReportTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("report", RENDERERS / "warderMenuIconReport.py")
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def test_report_deduplicates_and_ignores_invalid_names(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "report.txt"
            for name in ("missing3.png", "missing3.png", "missing.png", ".png", "../bad.png", "bad\\nname.png"):
                self.module.report_missing(name, str(path))
            self.assertEqual(path.read_text().splitlines(), ["missing3.png", "missing.png"])

    def test_report_refuses_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / "target"
            target.write_text("unchanged")
            link = Path(d) / "report"
            link.symlink_to(target)
            self.module.report_missing("missing.png", str(link))
            self.assertEqual(target.read_text(), "unchanged")

    def test_skin_alias_and_variant_fallback(self):
        root = "/storage"
        canonical = root + "/menuIconsBig/FHD_Glass17_Setup.png"
        bundled = self.module.SKIN_ART
        for key in self.module.SKIN_IDS:
            self.assertEqual(self.module.skin_artwork(key, root, "3", {canonical}.__contains__), canonical)
            self.assertEqual(self.module.skin_artwork(key, root, "3", {bundled}.__contains__), bundled)
        self.assertEqual(self.module.skin_artwork("warder_fullhdglass_settings", root, "3", {canonical, bundled}.__contains__), bundled)
        custom = root + "/menuIconsBig/warder_fullhdglass_settings.png"
        self.assertEqual(self.module.skin_artwork("warder_fullhdglass_settings", root, "3", {custom, bundled}.__contains__), custom)
        self.assertIsNone(self.module.skin_artwork("other", root, "3", {bundled}.__contains__))

    def test_bundle_is_exact_previously_approved_art(self):
        bundled = ROOT / "source/package-root/usr/share/enigma2/hd_glass17/menu/warder_skin.png"
        original = ROOT / "assets/warder/menu-icon-overrides/warder_skin.png"
        data = bundled.read_bytes()
        # Sparse CI checkouts intentionally omit the original asset directory.
        # Pin the approved immutable Git blob rather than weakening the check.
        git_blob = b"blob " + str(len(data)).encode("ascii") + b"\0" + data
        self.assertEqual(hashlib.sha1(git_blob).hexdigest(), "d9ed25d28f2ceda795796449d4dc8046a43a5872")
        if original.is_file():
            self.assertEqual(hashlib.sha256(data).digest(), hashlib.sha256(original.read_bytes()).digest())


class UserInfoScrollRegression(unittest.TestCase):
    def test_user_info_scroll_suite(self):
        subprocess.run([sys.executable, str(ROOT / "tools/test_warder_user_info_scroll.py"), "-q"], check=True)
        subprocess.run([sys.executable, str(ROOT / "tools/test_warder_optional_menu_keys.py"), "-q"], check=True)


if __name__ == "__main__":
    unittest.main()
