"""Regression: approved spinner ordering never selects a missing theme."""
import ast
from pathlib import Path
import textwrap
import types
import unittest

FILE = (Path(__file__).resolve().parents[1] /
        'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderSpinnerScreen.py')

class SpinnerOrderTests(unittest.TestCase):
    def get_method(self, name):
        source = FILE.read_text()
        tree = ast.parse(source)
        cls = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'SpinnerChoice')
        method = next(node for node in cls.body if isinstance(node, ast.FunctionDef) and node.name == name)
        return textwrap.dedent(ast.get_source_segment(source, method))

    def test_local_rows_and_static_warder_thumbnail(self):
        class Root:
            def __init__(self, value): self.value = str(value)
            def __truediv__(self, other): return Root(self.value + '/' + str(other))
            def __str__(self): return self.value
        themes = {
            'dove': {'title':'Dove','author':'','frames':[{'name':'wait1.png'}]},
            'bakussa': {'title':'HDGlass - bakussa','author':'bakussa','frames':[{'name':'wait1.png'}]},
            'warder': {'title':'Warder','author':'bakussa','frames':[{'name':'wait1.png'}],
                       'preview_frame':'wait1.png'}
        }
        env = {'backend': types.SimpleNamespace(
            catalog=lambda: {'themes': themes, 'downloaded_sources': {}},
            SKIN_ROOT=Root('/skin')),
            'Path': lambda p: Root(p)}
        exec(self.get_method('local_rows'), env)
        rows = env['local_rows'](object())
        self.assertEqual([row['id'] for row in rows], ['system','warder','bakussa','dove'])
        self.assertEqual(rows[1]['author'], 'bakussa')
        self.assertTrue(rows[1]['local_picture'].endswith('/warder/wait1.png'))

    def test_online_keeps_installed_first_and_does_not_auto_apply(self):
        src = self.get_method('loaded')
        self.assertIn("ordered = ('system', 'warder', 'bakussa', 'dove')", src)
        self.assertIn("self.rows = [local[key] for key in ordered if key in local]", src)
        self.assertNotIn("apply('warder')", FILE.read_text())

    def test_offline_does_not_fabricate_missing_warder(self):
        src = self.get_method('local_rows')
        self.assertIn("for key, theme in catalog['themes'].items():", src)
        self.assertNotIn("rows.append({'id':'warder'", src)

if __name__ == '__main__':
    unittest.main()
