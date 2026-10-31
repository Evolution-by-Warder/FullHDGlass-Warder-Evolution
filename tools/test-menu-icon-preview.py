#!/usr/bin/env python3
"""Exercise actual preview path selection for current and legacy menu sets."""
import ast
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch
import os
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py'
TREE = ast.parse(PLUGIN.read_text())
OWNER = next(n for n in TREE.body if isinstance(n, ast.ClassDef) and n.name == 'selectIconsDisplayed')


class MenuPreviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.scope = {'config': SimpleNamespace(plugins=SimpleNamespace(setupGlass17=SimpleNamespace(
            par39=SimpleNamespace(value=str(self.root))))), 'fileExists': lambda p: Path(p).is_file()}
        node = next(n for n in OWNER.body if isinstance(n, ast.FunctionDef) and n.name == 'previewIconPath')
        exec(compile(ast.Module(body=[node], type_ignores=[]), str(PLUGIN), 'exec'), self.scope)
        self.preview = SimpleNamespace(what=1, wahtType='/menuIcons/')

    def path(self, sample):
        return self.scope['previewIconPath'](self.preview, '1', sample)

    def put(self, name):
        path = self.root/'menuIcons/1'/(name+'.png')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b'fixture')
        return str(path)

    def test_new_catalog_ids_are_visible_without_an_old_backup(self):
        pairs = [('av_setup','video_setup'),('setup','setup'),
                 ('standby_restart_list','shutdown'),('system_selection','system'),
                 ('timer_edit','timer_edit'),('tuner_setup','tuner_setup'),
                 ('info_screen','information'),('manual_scan','manual_scan'),
                 ('network_setup','network')]
        for sample, current in pairs:
            self.assertEqual(self.path(sample), '')
            expected = self.put(current)
            self.assertEqual(self.path(sample), expected)

    def test_current_ids_take_precedence_over_leftover_legacy_art(self):
        old = self.put('info_screen')
        self.assertEqual(self.path('info_screen'), old)
        current = self.put('information')
        self.assertEqual(self.path('info_screen'), current)

    def test_weather_names_are_not_remapped(self):
        self.preview.what = 2
        self.put('information')
        self.assertEqual(self.path('info_screen'), '')
        self.assertEqual(self.path('information'), str(self.root/'menuIcons/1/information.png'))

    def test_every_grid_widget_requests_native_aspect_preserving_scaling(self):
        init = next(n for n in OWNER.body if isinstance(n, ast.FunctionDef) and n.name == '__init__')
        strings = [n.value for n in ast.walk(init) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
        fragment = next(s for s in strings if 'size="300,183"' in s)
        self.assertIn('scale="centerScaled"', fragment)
        # The nine existing 300x183 cells have four-pixel vertical gutters.
        cells = [(672+(i % 3)*300, 221+(i//3)*187, 300, 183) for i in range(9)]
        for x,y,w,h in cells:
            self.assertLessEqual(x+w, 1653)
            self.assertLessEqual(y+h, 865)


class DownloadStagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.path = str(Path(self.temp.name)/'hdd/staging')
        node = next(n for n in ast.walk(TREE) if isinstance(n,ast.FunctionDef) and n.name=='setWdir')
        self.scope = {'os':os,'HDDTMP':self.path}
        exec(compile(ast.Module(body=[node],type_ignores=[]),str(PLUGIN),'exec'),self.scope)

    def choose(self, kind):
        return self.scope['setWdir'](SimpleNamespace(type_download=kind))

    def test_small_download_does_not_require_or_create_hdd(self):
        self.assertEqual(self.choose('menuicons'),'/tmp/')
        self.assertFalse(Path(self.path).exists())

    def test_large_download_prefers_working_hdd_staging(self):
        for kind in ('menuiconsbig','ZZPicon','picon400'):
            self.assertEqual(self.choose(kind),self.path+'/')
            self.assertTrue(Path(self.path).is_dir())

    def test_unavailable_or_readonly_hdd_falls_back_before_free_space_check(self):
        with patch.object(os,'makedirs',side_effect=OSError('read-only')):
            self.assertEqual(self.choose('menuiconsbig'),'/tmp/')
        with patch.object(os,'access',return_value=False):
            self.assertEqual(self.choose('menuiconsbig'),'/tmp/')


if __name__ == '__main__':
    unittest.main()
