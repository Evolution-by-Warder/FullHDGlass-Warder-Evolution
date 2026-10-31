#!/usr/bin/env python3
"""Guard direct r12 replacement and reject incomplete successful-looking installs."""
import ast
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
spec = importlib.util.spec_from_file_location('installation_health_test', PLUGIN/'warderInstallHealth.py')
health = importlib.util.module_from_spec(spec)
spec.loader.exec_module(health)


class DirectLegacyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bin = self.root/'bin'
        self.bin.mkdir()
        opkg = self.bin/'opkg'
        opkg.write_text("#!/bin/sh\nprintf '%s\\n' 'Package: enigma2-skin-fullhdglass17' 'Version: 9.50-r12.2' 'Status: install ok installed'\n")
        opkg.chmod(0o755)
        self.info = self.root/'var/lib/opkg/info'
        self.info.mkdir(parents=True)
        old = json.loads((ROOT/'tools/fixtures/legacy-r12-control.json').read_text())
        (self.info/'enigma2-skin-fullhdglass17.postrm').write_text(old['postrm'])
        skin = self.root/'usr/share/enigma2/skin_default/skin.xml'
        skin.parent.mkdir(parents=True)
        skin.write_text('<skin><parameters/></skin>')
        self.script = re.sub(r'/(?:etc|usr|var|tmp)/', lambda m: str(self.root)+m[0],
                             (ROOT/'source/control/preinst').read_text())

    def run_preinst(self, *arguments):
        return subprocess.run(['sh', '-c', self.script, 'preinst', *arguments],
                              env=dict(os.environ, PATH=str(self.bin)+':'+os.environ['PATH']),
                              text=True, capture_output=True)

    def test_verified_r12_upgrades_directly_and_preserves_epg_context(self):
        result = self.run_preinst('upgrade', '9.50-r12.2')
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertEqual((self.root/'var/lib/fullhdglass17/epg-default-v1.state').read_text().strip(), 'preserve-pending')

    def test_same_version_string_with_unknown_remover_is_not_trusted(self):
        (self.info/'enigma2-skin-fullhdglass17.postrm').write_text('# modified cleanup\n')
        self.assertNotEqual(self.run_preinst('upgrade', '9.50-r12.2').returncode, 0)

    def test_custom_prerm_cannot_be_admitted_by_known_postrm(self):
        (self.info/'enigma2-skin-fullhdglass17.prerm').write_text('# unknown\n')
        self.assertNotEqual(self.run_preinst('upgrade', '9.50-r12.2').returncode, 0)

    def test_only_known_upgrade_invocation_is_allowed(self):
        for arguments in [('install',), ('upgrade', '9.50-r11'), ('remove',), ()]:
            with self.subTest(arguments=arguments):
                self.assertNotEqual(self.run_preinst(*arguments).returncode, 0)

    def test_hook_symlink_is_not_trusted(self):
        hook = self.info/'enigma2-skin-fullhdglass17.postrm'
        hook.rename(hook.with_suffix('.saved'))
        hook.symlink_to(hook.with_suffix('.saved'))
        self.assertNotEqual(self.run_preinst('upgrade', '9.50-r12.2').returncode, 0)

    def test_original_950_gets_only_a_verified_upgrade_guard_and_is_retry_safe(self):
        data=json.loads((ROOT/'tools/fixtures/legacy-950-control.json').read_text())
        hook=self.info/'enigma2-skin-fullhdglass17.postrm'
        hook.write_text(data['postrm'])
        self.assertEqual(self.run_preinst('upgrade','9.50').returncode,0)
        self.assertEqual(hook.read_text(),data['guard_prefix']+data['postrm'])
        self.assertEqual(self.run_preinst('upgrade','9.50').returncode,0)
        self.assertFalse(list(self.info.glob('*.warder-guard.*')))

    def test_guarded_950_upgrade_does_not_run_old_cleanup(self):
        data=json.loads((ROOT/'tools/fixtures/legacy-950-control.json').read_text())
        hook=self.info/'enigma2-skin-fullhdglass17.postrm'
        hook.write_text(data['postrm'])
        self.assertEqual(self.run_preinst('upgrade','9.50').returncode,0)
        skin=self.root/'usr/share/enigma2/hd_glass17/skin.xml'
        skin.parent.mkdir(parents=True);skin.write_text('keep installed skin')
        rewritten=re.sub(r'/(?:etc|usr|var|tmp)/',lambda m:str(self.root)+m[0],hook.read_text())
        result=subprocess.run(['sh','-c',rewritten,'postrm','upgrade','1.0.50-test2'],capture_output=True)
        self.assertEqual(result.returncode,0)
        self.assertEqual(skin.read_text(),'keep installed skin')

    def test_modified_950_remover_is_rejected_without_writing_it(self):
        data=json.loads((ROOT/'tools/fixtures/legacy-950-control.json').read_text())
        hook=self.info/'enigma2-skin-fullhdglass17.postrm'
        changed=data['postrm']+'\n# unknown modification\n';hook.write_text(changed)
        self.assertNotEqual(self.run_preinst('upgrade','9.50').returncode,0)
        self.assertEqual(hook.read_text(),changed)


class InstallationHealthTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.plugin, self.skin = Path(self.temp.name)/'plugin', Path(self.temp.name)/'skin'
        self.plugin.mkdir()
        self.skin.mkdir()
        for name in ('plugin.py', '__init__.py'):
            (self.plugin/name).write_text('# installed module\n')
        (self.plugin/'version').write_text('1.0.49\n')
        (self.skin/'skin.xml').write_text('<skin><screen name="InfoBar"/></skin>')

    def status(self, state='installed', version='1.0.49-1', package=health.PACKAGE):
        return lambda *a, **kw: SimpleNamespace(returncode=0, stdout=f'Package: {package}\nVersion: {version}\nStatus: install ok {state}\n')

    def verify(self, **kw):
        return health.verify_installation('1.0.49', self.plugin, self.skin, **kw)

    def test_complete_package_is_accepted(self):
        self.assertEqual(self.verify(runner=self.status()), '1.0.49')

    def test_missing_skin_is_rejected_even_with_current_version_file(self):
        (self.skin/'skin.xml').unlink()
        with self.assertRaises(ValueError):
            self.verify(runner=self.status())

    def test_invalid_or_wrong_skin_is_rejected(self):
        for xml in ('<skin>', '<skin/>', '<html><screen name="InfoBar"/></html>'):
            (self.skin/'skin.xml').write_text(xml)
            with self.assertRaises(ValueError):
                self.verify(runner=self.status())

    def test_half_installed_and_wrong_identity_are_rejected(self):
        for status in (self.status('half-installed'), self.status('unpacked'),
                       self.status(version='1.0.48-1'), self.status(package='other')):
            with self.assertRaises(ValueError):
                self.verify(runner=status)

    def test_missing_plugin_entrypoint_and_wrong_runtime_version_are_rejected(self):
        (self.plugin/'plugin.py').unlink()
        with self.assertRaises(ValueError):
            self.verify(runner=self.status())
        (self.plugin/'plugin.py').write_text('# module')
        (self.plugin/'version').write_text('1.0.48')
        with self.assertRaises(ValueError):
            self.verify(runner=self.status())

    def test_dpkg_query_path_remains_supported(self):
        calls = []
        def runner(command, **kwargs):
            calls.append(command)
            return self.status()()
        self.assertEqual(self.verify(runner=runner, manager='dpkg'), '1.0.49')
        self.assertEqual(calls[0][0], 'dpkg-query')

    def test_gui_success_path_is_blocked_when_version_exists_but_skin_is_missing(self):
        (self.skin/'skin.xml').unlink()
        tree = ast.parse((PLUGIN/'plugin.py').read_text())
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name=='setupGlass17ScreenSetup')
        fn = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name=='_warderShowInstallResult')
        package = ModuleType('installation_gui_test')
        package.__path__ = []
        module = ModuleType(package.__name__+'.warderInstallHealth')
        module.verify_installation = lambda version, **kw: self.verify(runner=self.status())
        scope = {'__package__': package.__name__, 'subprocess': subprocess,
                 '_': lambda s:s, 'MessageBox': SimpleNamespace(TYPE_INFO=1, TYPE_ERROR=2)}
        exec(compile(ast.Module(body=[fn], type_ignores=[]), '<actual-update-result>', 'exec'), scope)
        messages = []
        owner = SimpleNamespace(warderUpdate={'version':'1.0.49'}, readVersion=lambda:'1.0.49',
                                warderInstallExitCode=0, warderInstallOutput=[], fileName='skin.ipk',
                                session=SimpleNamespace(open=lambda *args:messages.append(args)))
        with patch.dict(sys.modules, {package.__name__:package, module.__name__:module}):
            scope[fn.name](owner)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0][2], 2)
        self.assertFalse(hasattr(owner, 'warderRestartTimer'))


if __name__ == '__main__':
    unittest.main()
