"""Integrated skin changes, no receiver GUI required."""
import ast
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
PLUGIN=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
RENDERER=ROOT/'source/package-root/usr/lib/enigma2/python/Components/Renderer/g17MenuEntry2.py'

class SkinIntegrationTests(unittest.TestCase):
    def test_menu_title_and_existing_setup_callback(self):
        tree=ast.parse((PLUGIN/'plugin.py').read_text())
        fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='startSetup17')
        txt=ast.get_source_segment((PLUGIN/'plugin.py').read_text(),fn)
        self.assertIn('FullHDGlass Warder Evolution',txt)
        self.assertNotIn('FullHDGlass - Warder Evolution',txt)
        self.assertIn('"warder_fullhdglass_settings"',txt)
        self.assertIn(' main, ',txt)
        self.assertIn('main17',txt)
    def test_internal_storage_detector(self):
        spec=importlib.util.spec_from_file_location('safe', PLUGIN/'warderStorageSafety.py')
        mod=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.NamedTemporaryFile(mode='w') as m:
            m.write('22 1 0:1 / / rw - overlay overlay rw\n')
            m.flush()
            self.assertTrue(mod.is_internal('/media/usb/hdg17_files',m.name))
        with tempfile.NamedTemporaryFile(mode='w') as m:
            m.write('22 1 0:1 / / rw - overlay overlay rw\n23 22 8:1 / /media/usb rw - ext4 /dev/sda1 rw\n')
            m.flush()
            self.assertFalse(mod.is_internal('/media/usb/hdg17_files',m.name))
    def test_download_requires_explicit_confirmation(self):
        txt=(PLUGIN/'plugin.py').read_text()
        self.assertIn('self._warderStorageChoice, ChoiceBox',txt)
        self.assertIn('ui_text("Continue anyway"), "continue"',txt)
        self.assertIn('ui_text("Cancel"), "cancel"',txt)
        self.assertIn('if _warderStorageHasSpace(storage_target):',txt)
        self.assertIn('if not _warderStorageHasSpace(target):',txt)
    def test_artwork_only_uses_stable_menu_ids(self):
        txt=RENDERER.read_text()
        for ident in ('warder_radio_mainmenu','PiconHub_Warder_Evolution','glass_sys_utils'):
            self.assertIn(ident,txt)
        helper = RENDERER.with_name('warderMenuIconReport.py')
        spec = importlib.util.spec_from_file_location('menu_report', helper)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.assertEqual(set(mod.SKIN_IDS), {'warder_fullhdglass_settings', 'FHD_Glass17_Setup'})
        self.assertIn('skin_artwork(entry_id,',txt)
        self.assertIn('if pixpath == self.default',txt)
    def test_spinner_order_preserves_existing_themes(self):
        txt=(PLUGIN/'warderSpinnerScreen.py').read_text()
        self.assertIn("'system', 'warder', 'bakussa', 'dove'",txt)
        self.assertIn("if key in local",txt)
    def test_date_example_is_already_bound(self):
        txt=(PLUGIN/'plugin.py').read_text()
        self.assertIn('<widget source="selected_item" render="Label"',txt)

if __name__=='__main__':
    unittest.main()
