#!/usr/bin/env python3
"""Exercise the real lookup, selected renderer and native ServiceList handoffs."""
import argparse
import ast
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
PKG = Path(os.environ.get('WARDER_PICON_PACKAGE_ROOT', str(ROOT/'source/package-root/usr/lib/enigma2/python')))
spec = importlib.util.spec_from_file_location('channel_picons', PKG/'Plugins/Extensions/setupGlass17/warderChannelPicons.py')
picons = importlib.util.module_from_spec(spec)
spec.loader.exec_module(picons)
REF = '1:0:19:1F48:CA1:3:EB0000:0:0:0:'
NAME = '1_0_19_1F48_CA1_3_EB0000_0_0_0'
UPSTREAM = None


class LookupFixture:
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.active = True
        self.get_name = Mock(return_value='ČT 1 HD')
        self.native = Mock(return_value='/image/picon.png')
        self.native_renderer = NS(getPiconName=self.native)
        self.module = NS(getChannelSelectionPiconName=self.native, getPiconName=self.native)
        self.install()

    def install(self):
        return picons.install(self.module, lambda:self.active, lambda:str(self.base),
                              lambda ref:ref, self.get_name, lambda name:name)

    def put(self, folder, name=NAME):
        path = self.base/folder/(name+'.png')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b'fixture')
        return str(path)

    def lookup(self, ref=REF):
        return self.module.getChannelSelectionPiconName(ref)


class LookupTests(LookupFixture, unittest.TestCase):
    def test_mini_precedes_shared_set(self):
        mini=self.put('picon_50x30'); self.put('picon')
        self.assertEqual(self.lookup(),mini)
        self.get_name.assert_not_called()
        self.native.assert_not_called()

    def test_fallback_is_per_channel_in_a_partly_filled_mini_set(self):
        self.put('picon_50x30','1_0_19_999_CA1_3_EB0000_0_0_0')
        shared=self.put('picon')
        self.assertEqual(self.lookup(),shared)

    def test_absent_or_empty_mini_folder_uses_shared_set(self):
        shared=self.put('picon')
        self.assertEqual(self.lookup(),shared)
        (self.base/'picon_50x30').mkdir()
        self.assertEqual(self.lookup(),shared)

    def test_native_system_path_remains_final_fallback(self):
        self.assertEqual(self.lookup(),'/image/picon.png')
        self.native.assert_called_once_with(REF)

    def test_other_skins_delegate_even_with_a_mini_set(self):
        self.put('picon_50x30'); self.active=False
        self.assertEqual(self.lookup(),'/image/picon.png')
        self.get_name.assert_not_called()

    def test_native_infobar_lookup_is_never_replaced(self):
        self.put('picon_50x30')
        self.assertIs(self.native_renderer.getPiconName,self.native)
        self.assertEqual(self.native_renderer.getPiconName(REF),'/image/picon.png')

    def test_install_is_idempotent(self):
        original=self.module.getPiconName
        self.assertFalse(self.install())
        self.assertIs(self.module.getPiconName,original)

    def test_newly_downloaded_and_removed_picons_are_seen_without_restart(self):
        shared=self.put('picon')
        self.assertEqual(self.lookup(),shared)
        mini=self.put('picon_50x30')
        self.assertEqual(self.lookup(),mini)
        Path(mini).unlink()
        self.assertEqual(self.lookup(),shared)

    def test_base_path_change_is_applied_immediately(self):
        self.put('picon_50x30')
        self.base=self.base/'other-disk'
        shared=self.put('picon')
        self.assertEqual(self.lookup(),shared)

    def test_mini_service_type_alias_precedes_exact_shared_reference(self):
        mini=self.put('picon_50x30',NAME.replace('_19_','_1_'))
        self.put('picon')
        self.assertEqual(self.lookup(),mini)

    def test_namespace_and_iptv_aliases(self):
        mini=self.put('picon_50x30',NAME.replace('_19_','_1_'))
        self.assertEqual(self.lookup(REF.replace('EB0000','EB1234')),mini)
        self.assertEqual(self.lookup(REF.replace('1:0:','4097:0:',1)),mini)

    def test_alternative_group_resolves_before_lookup(self):
        mini=self.put('picon_50x30')
        self.module=NS(getPiconName=self.native)
        picons.install(self.module,lambda:True,lambda:str(self.base),lambda ref:REF,self.get_name,lambda n:n)
        self.assertEqual(self.module.getPiconName('1:134:1:0:0:0:0:0:0:0:'),mini)

    def test_name_based_mini_set_precedes_shared_reference(self):
        mini=self.put('picon_50x30','čt 1 hd'); self.put('picon')
        self.assertEqual(self.lookup(),mini)

    def test_name_suffix_alias_is_supported(self):
        mini=self.put('picon_50x30','t1')
        self.assertEqual(self.lookup(),mini)

    def test_malformed_reference_cannot_escape_selected_folders(self):
        self.put('picon_50x30')
        self.assertEqual(self.lookup(REF.replace('CA1','../CA1')),'/image/picon.png')
        self.assertEqual(self.lookup(None),'/image/picon.png')

    def test_unavailable_data_path_keeps_native_lookup(self):
        self.module=NS(getPiconName=self.native)
        picons.install(self.module,lambda:True,lambda:None,lambda ref:ref,self.get_name,lambda n:n)
        self.assertEqual(self.module.getPiconName(REF),'/image/picon.png')

    def test_disabled_and_reenabled_skin_uses_current_files(self):
        self.active=False
        self.assertEqual(self.lookup(),'/image/picon.png')
        mini=self.put('picon_50x30'); self.active=True
        self.assertEqual(self.lookup(),mini)


class SelectedPiconTests(LookupFixture, unittest.TestCase):
    def test_large_formats_keep_their_own_set_and_fall_back_to_shared(self):
        tree=ast.parse((PKG/'Components/Renderer/g17RefTV3.py').read_text())
        owner=next(n for n in tree.body if isinstance(n,ast.ClassDef))
        method=next(n for n in owner.body if isinstance(n,ast.FunctionDef) and n.name=='findPicon')
        import os
        scope=dict(os=os,config=NS(plugins=NS(setupGlass17=NS(par39=NS(value=str(self.base))))))
        exec(compile(ast.Module(body=[method],type_ignores=[]),'g17RefTV3.py','exec'),scope)
        shared=self.put('picon'); self.put('picon_50x30')
        for folder in ('picon_400x240','ZZPicon'):
            widget=NS(path=folder)
            self.assertEqual(scope['findPicon'](widget,NAME),shared)
            own=self.put(folder)
            self.assertEqual(scope['findPicon'](widget,NAME),own)


class WiringTests(unittest.TestCase):
    def test_runtime_hook_uses_live_skin_and_base_settings(self):
        text=(PKG/'Plugins/Extensions/setupGlass17/plugin.py').read_text()
        tree=ast.parse(text)
        node=next(n for n in tree.body if isinstance(n,ast.Try) and '_installWarderChannelPicons' in ast.unparse(n))
        call=next(n for n in ast.walk(node) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='_installWarderChannelPicons')
        self.assertEqual(ast.unparse(call.args[1]),"lambda: config.skin.primary_skin.value == 'hd_glass17/skin.xml'")
        self.assertEqual(ast.unparse(call.args[2]),'lambda: config.plugins.setupGlass17.par39.value')


class NativeHandoffTests(LookupFixture, unittest.TestCase):
    def test_real_native_callback_registration_respects_icon_toggle(self):
        if UPSTREAM is None:self.skipTest('Supply --upstream for the native image handoff')
        text=(UPSTREAM/'Components/ServiceList.py').read_text()
        tree=ast.parse(text)
        imports=[alias.name for n in tree.body if isinstance(n,ast.ImportFrom) and n.module=='Components.Renderer.Picon' for alias in n.names]
        name=next(n for n in ('getChannelSelectionPiconName','getPiconName') if n in imports)
        binding=next(n for n in ast.walk(tree) if isinstance(n,ast.If) and ast.unparse(n.test)=='config.usage.service_icon_enable.value')
        mini=self.put('picon_50x30'); self.put('picon')
        content=NS(setGetPiconNameFunc=Mock())
        scope=dict(vars(self.module),self=NS(l=content),config=NS(usage=NS(service_icon_enable=NS(value=True))))
        exec(compile(ast.Module(body=[binding],type_ignores=[]),'native-ServiceList.py','exec'),scope)
        callback=content.setGetPiconNameFunc.call_args.args[0]
        self.assertIs(callback,getattr(self.module,name))
        self.assertEqual(callback(REF),mini)
        scope['config'].usage.service_icon_enable.value=False
        exec(compile(ast.Module(body=[binding],type_ignores=[]),'native-ServiceList.py','exec'),scope)
        self.assertIsNone(content.setGetPiconNameFunc.call_args.args[0])

    def test_real_native_template_uses_mini_and_per_service_fallback(self):
        if UPSTREAM is None:self.skipTest('Supply --upstream for the native template handoff')
        tree=ast.parse((UPSTREAM/'Components/ServiceList.py').read_text())
        methods=[n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='buildOptionEntryServicePicon']
        if not methods:self.skipTest('Image uses the C++ callback path')
        scope=dict(vars(self.module),exists=lambda p:Path(p).is_file(),loadPNG=lambda p:p,
                   eServiceReference=NS(mustDescent=1))
        exec(compile(ast.Module(body=methods,type_ignores=[]),'native-ServiceList.py','exec'),scope)
        service=NS(flags=0,toString=lambda:REF)
        shared=self.put('picon'); mini=self.put('picon_50x30')
        self.assertEqual(scope['buildOptionEntryServicePicon'](None,service),mini)
        Path(mini).unlink()
        self.assertEqual(scope['buildOptionEntryServicePicon'](None,service),shared)


if __name__=='__main__':
    parser=argparse.ArgumentParser(add_help=False)
    parser.add_argument('--upstream',type=Path)
    args,remaining=parser.parse_known_args()
    UPSTREAM=args.upstream
    unittest.main(argv=[sys.argv[0]]+remaining)

