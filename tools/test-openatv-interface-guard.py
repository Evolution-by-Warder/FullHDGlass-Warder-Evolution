"""Prove the source guard rejects real removals and display/signature changes."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('check-openatv-interfaces.py')
spec = importlib.util.spec_from_file_location('interface_guard', SCRIPT)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)
SOURCE = '''from somewhere import Label
class Dialog:
    def __init__(self, session, title=""):
        self["prompt"] = Label(title)
        Screen.__init__(self, session, mandatoryWidgets=["prompt"])
'''


class GuardTests(unittest.TestCase):
    def check(self, source):
        import ast
        contract = {'module': 'Screens.Dialog', 'class': 'Dialog', 'kind': 'display'}
        contract['expected'] = guard.inspect_contract(ast.parse(SOURCE), contract)
        signature = {'module': 'Screens.Dialog', 'class': 'Dialog', 'method': '__init__', 'kind': 'signature'}
        signature['expected'] = guard.inspect_contract(ast.parse(SOURCE), signature)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'Screens').mkdir()
            (root / 'Screens/Dialog.py').write_text(source)
            manifest = root / 'interfaces.json'
            manifest.write_text(json.dumps({'project': 'fixture', 'modules': {'Screens.Dialog': ['Dialog', 'Label']}, 'contracts': [contract, signature]}))
            return subprocess.run([sys.executable, str(SCRIPT), '--manifest', str(manifest), '--upstream', str(root)], capture_output=True, text=True)

    def test_reviewed_interface_passes(self):
        result = self.check(SOURCE)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_removed_export_fails(self):
        result = self.check(SOURCE.replace('class Dialog:', 'class Renamed:'))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('missing imported exports', result.stderr)

    def test_changed_constructor_fails(self):
        result = self.check(SOURCE.replace('session, title=""', 'session, required, title=""'))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('reviewed interface changed', result.stderr)

    def test_new_field_or_changed_widget_type_fails(self):
        for source in (SOURCE.replace('Label(title)', 'StaticText(title)'), SOURCE + '        self["description"] = Label("new")\n'):
            self.assertNotEqual(self.check(source).returncode, 0)

    def test_added_mandatory_widget_fails(self):
        self.assertNotEqual(self.check(SOURCE.replace('["prompt"]', '["prompt", "description"]')).returncode, 0)


if __name__ == '__main__':
    unittest.main()
