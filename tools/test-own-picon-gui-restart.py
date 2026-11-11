#!/usr/bin/env python3
"""Own-channel-picon switch must use the existing GUI restart path."""
import ast
from pathlib import Path
import unittest

PLUGIN = Path(__file__).resolve().parents[1] / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py"
TREE = ast.parse(PLUGIN.read_text(encoding="utf-8"))
OWNER = next(node for node in TREE.body if isinstance(node, ast.ClassDef) and node.name == "setupGlass17ScreenSetup")
METHODS = {node.name: node for node in OWNER.body if isinstance(node, ast.FunctionDef)}


class OwnPiconRestartTest(unittest.TestCase):
    def test_open_snapshot_and_switch_only_gate(self):
        init = ast.unparse(METHODS["__init__"])
        save = ast.unparse(METHODS["save"])
        self.assertIn("self._ownPiconsAtOpen = bool(config.plugins.warderUserPicons.enabled.value)", init)
        self.assertIn("own_picons_changed = self._ownPiconsAtOpen != bool(config.plugins.warderUserPicons.enabled.value)", save)
        self.assertIn("if own_picons_changed:", save)
        self.assertIn('ui_text(\'Use own channel picons\')', save)

    def test_3_second_message_and_delayed_existing_gui_restart(self):
        save = ast.unparse(METHODS["save"])
        self.assertIn("3 if own_picons_changed else 8", save)
        self.assertIn("self.rstGUI(3000 if own_picons_changed else 8000)", save)
        self.assertIn("enable_input=False", save)
        rst = ast.unparse(METHODS["rstGUI"])
        self.assertIn("self.start_rst.start(delay, True)", rst)
        saving = ast.unparse(METHODS["saving"])
        self.assertLess(saving.index("config.plugins.warderUserPicons.enabled.save()"), saving.index("configfile.save()"))
        self.assertIn("self.sDr()", saving)

    def test_invalid_enabled_folder_rejects_restart(self):
        save = ast.unparse(METHODS["save"])
        check = save.index("if own_picons_changed and config.plugins.warderUserPicons.enabled.value:")
        show = save.index("self.session.open(MessageBox, str(msg + msgScr)")
        self.assertLess(check, show)
        self.assertIn("if not own_folder or not os.path.isdir(own_folder)", save)


if __name__ == "__main__":
    unittest.main()
