"""Unit tests for pixel-accurate EPG title truncation."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderEpgTextFit.py"
spec = spec_from_file_location("warderEpgTextFit", SOURCE)
module = module_from_spec(spec)
spec.loader.exec_module(module)


class TitleFitTests(unittest.TestCase):
    def measure(self, text):
        # A controlled fake font width: production code uses gFont/eLabel.
        return len(text) * 8

    def test_short_title_is_unchanged(self):
        self.assertEqual(module.fit_title_to_width("Správy", 200, self.measure), "Správy")

    def test_long_title_stays_within_width(self):
        for title in ("Paul Simon, Graceland: The African Concert",
                      "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
                      "VeľmiDlhéNázvyBezMedzier"):
            for width in (8, 16, 64, 112, 200):
                fitted = module.fit_title_to_width(title, width, self.measure)
                self.assertLessEqual(self.measure(fitted), width)
                if self.measure(title) > width and width >= 8:
                    self.assertTrue(fitted.endswith("…"))

    def test_no_space_returns_empty(self):
        self.assertEqual(module.fit_title_to_width("ABC", 0, self.measure), "")
        self.assertEqual(module.fit_title_to_width("ABC", 7, self.measure), "")


if __name__ == "__main__":
    unittest.main()
