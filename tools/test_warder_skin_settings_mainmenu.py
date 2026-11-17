"""Verify FullHDGlass settings can open directly from Enigma2 Main menu.

Only the existing WHERE_MENU callback changes; plugin-list registration and
the actual setup screen stay untouched. No real Enigma2 GUI is required.
"""
import ast
from pathlib import Path
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py"
tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}

def fake_config(skin="hd_glass17/skin.xml", special="n", show_special=True):
    return SimpleNamespace(
        skin=SimpleNamespace(primary_skin=SimpleNamespace(value=skin)),
        plugins=SimpleNamespace(setupGlass17=SimpleNamespace(
            par78=SimpleNamespace(value=special, getText=lambda: "Weather"),
            par85=SimpleNamespace(value=show_special))))

class SkinMainMenuTests(unittest.TestCase):
    def register(self, skin="hd_glass17/skin.xml", special="n", show_special=True):
        open_skin = object()
        special_info = object()
        names = []
        def translate(message):
            names.append(message)
            return "Nastavenie skinu FullHDGlass" if message == "Configure the FullHDGlass skin" else message
        env = dict(config=fake_config(skin, special, show_special),
                   ui_text=translate, main=open_skin, main17=special_info)
        fn = functions["startSetup17"]
        exec(compile(ast.Module(body=[fn], type_ignores=[]), str(SOURCE), "exec"), env)
        return env["startSetup17"], open_skin, special_info, names

    def test_active_skin_has_settings_in_mainmenu_even_when_special_info_off(self):
        menu, open_skin, _, names = self.register()
        self.assertEqual(menu("mainmenu"), [
            ("FullHDGlass Warder Evolution", open_skin, "warder_fullhdglass_settings", 43)])
        self.assertEqual(names, [])

    def test_existing_special_info_entry_is_preserved(self):
        menu, open_skin, special_info, _ = self.register(special="w")
        self.assertEqual(menu("mainmenu"), [
            ("FullHDGlass Warder Evolution", open_skin, "warder_fullhdglass_settings", 43),
            ("Weather (FullHDGlass)", special_info, "w", 44)])

    def test_special_info_user_toggle_does_not_hide_skin_settings(self):
        menu, open_skin, _, _ = self.register(special="w", show_special=False)
        self.assertEqual([item[1] for item in menu("mainmenu")], [open_skin])

    def test_unrelated_menus_are_not_modified(self):
        menu, _, _, _ = self.register(special="w")
        for menuid in ("system", "setup", "plugins", "", None):
            self.assertEqual(menu(menuid), [])

    def test_other_skin_does_not_get_fullhdglass_entry(self):
        menu, _, _, _ = self.register(skin="MetrixHD/skin.xml", special="w")
        self.assertEqual(menu("mainmenu"), [])

    def test_existing_plugin_list_entry_keeps_same_main_callback(self):
        node = functions["Plugins"]
        entries = [x for x in ast.walk(node) if isinstance(x, ast.Call)
                   and isinstance(x.func, ast.Name) and x.func.id == "PluginDescriptor"]
        self.assertTrue(any(
            any(kw.arg == "where" and isinstance(kw.value, ast.Attribute) and
                kw.value.attr == "WHERE_PLUGINMENU" for kw in entry.keywords)
            and any(kw.arg == "fnc" and isinstance(kw.value, ast.Name)
                    and kw.value.id == "main" for kw in entry.keywords)
            for entry in entries))
        setup = functions["main"]
        self.assertTrue(any(
            isinstance(call, ast.Call)
            and isinstance(call.func, ast.Attribute)
            and call.func.attr == "open"
            and any(isinstance(arg, ast.Name) and arg.id == "setupGlass17ScreenSetup"
                    for arg in call.args)
            for call in ast.walk(setup)))


if __name__ == "__main__":
    unittest.main()
