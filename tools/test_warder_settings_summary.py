"""Reader-visible support summary; no Enigma2 runtime or image is required."""
import importlib.util
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17"
spec = importlib.util.spec_from_file_location("warder_settings_summary",
                                              SOURCE / "warderSettingsSummary.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SupportHeaderTests(unittest.TestCase):
    def test_channel_type_and_epg_state_are_visible_in_existing_header(self):
        text = module.channel_diagnostic_suffix("35", True, True, "0", "0", "1", "sk")
        self.assertIn("Výber kanálov: 35", text)
        self.assertIn("EPG: ZAP/GLES", text)
        self.assertIn("F N/E/R: 0/0/1", text)
        self.assertNotIn("\n", text)

    def test_czech_and_native_fallback_do_not_misrepresent_gles(self):
        text = module.channel_diagnostic_suffix("12", True, False, 33, 30, 37, "cs")
        self.assertIn("Výběr kanálů: 12", text)
        self.assertIn("EPG: ZAP/NAT", text)
        self.assertIn("F N/E/R: 33/30/37", text)
        off = module.channel_diagnostic_suffix("35", False, True, 0, 0, 1, "en")
        self.assertIn("EPG: OFF/GLES", off)

    def test_original_selected_settings_line_remains_only_header_target(self):
        source = (SOURCE / "plugin.py").read_text(encoding="utf-8")
        self.assertIn('from .warderSettingsSummary import channel_diagnostic_suffix', source)
        self.assertIn('self.textShowInfo += channel_diagnostic_suffix(', source)
        self.assertIn('self["description"].setText(self.textShowInfo)', source)
        match = re.search(r'<widget name="description" position="60,174" size="1800,46"[^>]*>', source)
        self.assertIsNotNone(match)
        self.assertIn('noWrap="1"', match.group(0))
        self.assertNotIn('source="channel_diagnostic"', source)


if __name__ == "__main__":
    unittest.main()
