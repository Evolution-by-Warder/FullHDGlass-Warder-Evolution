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

    def test_user_menu_numbers_are_stable_and_default_first(self):
        source = (SOURCE / "plugin.py").read_text(encoding="utf-8")
        self.assertIn('menu_support_number(config.plugins.setupGlass17.par7.value)', source)
        self.assertIn('_("Menu Icons")', source)
        self.assertNotIn('Menu: " + menusel(config.plugins.setupGlass17.par7.value)', source)
        # Do not repurpose native template IDs (List is technically 2 there).
        self.assertEqual(module.menu_support_number("List"), "1")
        self.assertEqual(module.menu_support_number("Icons"), "2")
        self.assertEqual(module.menu_support_number("Icons Right"), "3")
        self.assertEqual(module.menu_support_number("PIG4"), "9")
        self.assertEqual(module.menu_support_number("Li3"), "11")
        self.assertEqual(module.menu_support_number("unknown"), "?")
        self.assertEqual(len(set(module.MENU_DISPLAY_ORDER)), 11)

    def test_all_existing_choice_values_have_support_numbers(self):
        import ast
        text = (SOURCE / "plugin.py").read_text(encoding="utf-8")
        tree = ast.parse(text)
        target = next(n for n in ast.walk(tree) if isinstance(n, ast.Assign)
                      and any(isinstance(t, ast.Attribute) and t.attr == 'par7'
                              for t in n.targets)
                      and isinstance(n.value, ast.Call)
                      and getattr(n.value.func, 'id', '') == 'ConfigSelection')
        self.assertEqual(next(k.value.value for k in target.value.keywords
                              if k.arg == 'default'), "List")
        choices = next(k.value for k in target.value.keywords if k.arg == 'choices')
        configured = {x.elts[0].value for x in choices.elts}
        self.assertEqual(configured, set(module.MENU_DISPLAY_ORDER))

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
