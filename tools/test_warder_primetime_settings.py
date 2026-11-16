"""Check PrimeTime opt-in config and menu without importing Enigma2."""
import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py"
TEXT = SRC.read_text(encoding="utf-8")
TREE = ast.parse(TEXT)


class PrimeTimeSettingsTests(unittest.TestCase):
    def test_defaults_and_separate_registry(self):
        self.assertIn("config.plugins.warderEvolutionPrimeTime = ConfigSubsection()", TEXT)
        self.assertIn("config.plugins.warderEvolutionPrimeTime.enabled = ConfigYesNo(default=False)", TEXT)
        self.assertIn("default=[20, 25]", TEXT)
        self.assertNotIn("config.plugins.setupGlass17.warderPrimeTimeEnabled", TEXT)
        self.assertNotIn("config.plugins.setupGlass17.warderPrimeTimeClock", TEXT)

    def test_menu_follows_legacy_order_and_is_conditional(self):
        owner = next(n for n in TREE.body if isinstance(n, ast.ClassDef) and n.name == "setupGlass17ScreenSetup")
        method = next(n for n in owner.body if isinstance(n, ast.FunctionDef) and n.name == "runSetup")
        text = ast.unparse(method)
        self.assertLess(text.index('config.plugins.setupGlass17.par19'), text.index('config.plugins.setupGlass17.par231'))
        self.assertLess(text.index('config.plugins.setupGlass17.par231'), text.index('config.plugins.setupGlass17.par132'))
        self.assertLess(text.index('config.plugins.setupGlass17.par132'), text.index('config.plugins.warderEvolutionPrimeTime.enabled'))
        self.assertIn('if config.plugins.warderEvolutionPrimeTime.enabled.value:', text)
        self.assertIn('config.plugins.warderEvolutionPrimeTime.clock', text)

    def test_save_cancel_and_immediate_refresh(self):
        owner = next(n for n in TREE.body if isinstance(n, ast.ClassDef) and n.name == "setupGlass17ScreenSetup")
        methods = {n.name: ast.unparse(n) for n in owner.body if isinstance(n, ast.FunctionDef)}
        for key in ("enabled", "clock"):
            self.assertIn("config.plugins.warderEvolutionPrimeTime.%s.save()" % key, methods["saving"])
            self.assertIn("config.plugins.warderEvolutionPrimeTime.%s.cancel()" % key, methods["exitNow"])
        self.assertIn("config.plugins.warderEvolutionPrimeTime.enabled", methods["chckSetup"])
        self.assertIn("config.plugins.warderUserPicons.enabled", methods["chckSetup"])
        self.assertIn("self.runSetup()", methods["chckSetup"])


if __name__ == "__main__":
    unittest.main()
