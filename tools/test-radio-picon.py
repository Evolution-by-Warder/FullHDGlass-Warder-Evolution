#!/usr/bin/env python3
"""Execute the real radio picon renderer with native service/path doubles."""
import ast
from pathlib import Path
from types import SimpleNamespace, ModuleType
import sys
import unittest
from unittest.mock import Mock, patch

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'source/package-root/usr/lib/enigma2/python/Components/Renderer/g17PicRef.py'
BAYERN='1:0:A:28A2:40F:1:C00000:0:0:0:'

class Renderer:
    CHANGED_CLEAR=2
    def __init__(self):
        self.instance=Mock()
        self.source=SimpleNamespace(text=BAYERN)

class RadioPiconTests(unittest.TestCase):
    def setUp(self):
        tree=ast.parse(PATH.read_text());cls=next(n for n in tree.body if isinstance(n,ast.ClassDef))
        self.native=Mock(return_value='/system/picon/bayern3.png')
        self.module=ModuleType('Components.Renderer.Picon');self.module.getPiconName=self.native
        self.playing=SimpleNamespace(toString=lambda:BAYERN)
        self.scope={'Renderer':Renderer,'ePixmap':object,'NavigationInstance':SimpleNamespace(instance=SimpleNamespace(getCurrentlyPlayingServiceReference=lambda:self.playing)),
                    'is_native_dab':lambda ref:False,'fileExists':lambda path:False,
                    'config':SimpleNamespace(plugins=SimpleNamespace(setupGlass17=SimpleNamespace(par39=SimpleNamespace(value='/skin'),par161=SimpleNamespace(value=False)))),
                    'setDefPicon':lambda:'/default.png'}
        exec(compile(ast.Module(body=[cls],type_ignores=[]),str(PATH),'exec'),self.scope)
        self.renderer=self.scope['g17PicRef']()
    def change(self):
        with patch.dict(sys.modules,{'Components.Renderer.Picon':self.module}):self.renderer.changed((0,))
    def test_aac_radio_uses_native_reference_and_name_lookup_before_default(self):
        self.change();self.native.assert_called_once_with(BAYERN)
        self.renderer.instance.setPixmapFromFile.assert_called_with('/system/picon/bayern3.png')
    def test_standard_radio_also_uses_system_path_fallback(self):
        ref=BAYERN.replace(':A:',':2:');self.renderer.source.text=ref
        self.change();self.native.assert_called_once_with(ref)
    def test_exact_skin_picon_keeps_precedence(self):
        self.scope['fileExists']=lambda path:path=='/skin/picon/1_0_A_28A2_40F_1_C00000_0_0_0.png'
        self.change();self.native.assert_not_called()
        self.assertEqual(self.renderer.pngname,'/skin/picon/1_0_A_28A2_40F_1_C00000_0_0_0.png')
    def test_existing_legacy_dimension_picon_is_read_without_moving_files(self):
        path='/skin/picon_220x132/1_0_A_28A2_40F_1_C00000_0_0_0.png'
        self.scope['fileExists']=lambda candidate:candidate==path
        self.change();self.assertEqual(self.renderer.pngname,path);self.native.assert_not_called()
    def test_canonical_picon_precedes_both_legacy_dimensions(self):
        self.scope['fileExists']=lambda path:path.endswith('1_0_A_28A2_40F_1_C00000_0_0_0.png')
        self.change();self.assertEqual(self.renderer.pngname,'/skin/picon/1_0_A_28A2_40F_1_C00000_0_0_0.png')
    def test_explicit_custom_directory_is_not_replaced_with_standard_paths(self):
        self.renderer.path='my-radio'
        self.scope['fileExists']=lambda path:path=='/skin/my-radio/1_0_A_28A2_40F_1_C00000_0_0_0.png'
        self.change();self.assertEqual(self.renderer.pngname,'/skin/my-radio/1_0_A_28A2_40F_1_C00000_0_0_0.png')
    def test_dab_keeps_existing_native_playing_reference_route(self):
        self.scope['is_native_dab']=lambda ref:True
        self.renderer.source.text='not-the-playing-dab-reference'
        self.change();self.native.assert_called_once_with(BAYERN)
    def test_tv_does_not_gain_legacy_directory_search(self):
        self.renderer.source.text=BAYERN.replace(':A:',':1:')
        self.scope['fileExists']=lambda path:'/picon_220x132/' in path
        self.change();self.assertEqual(self.renderer.pngname,'/default.png')
    def test_tv_does_not_gain_a_new_system_lookup(self):
        self.renderer.source.text=BAYERN.replace(':A:',':1:')
        self.change();self.native.assert_not_called();self.assertEqual(self.renderer.pngname,'/default.png')
    def test_missing_radio_returns_default_and_never_keeps_previous_station(self):
        self.change();self.native.return_value=''
        self.renderer.source.text=BAYERN.replace('28A2','28A3')
        self.change();self.assertEqual(self.renderer.pngname,'/default.png')
    def test_clear_hides_without_lookup(self):
        self.renderer.changed((Renderer.CHANGED_CLEAR,))
        self.native.assert_not_called();self.renderer.instance.hide.assert_called_once()
    def test_old_image_without_native_picon_module_keeps_default(self):
        del self.module.getPiconName
        self.change();self.assertEqual(self.renderer.pngname,'/default.png')

class InfobarVariantTests(unittest.TestCase):
    setUp=RadioPiconTests.setUp
    def test_both_additional_renderers_share_paths_and_native_radio_fallback(self):
        for name in ('g17PicRef2','g17PicRef3'):
            tree=ast.parse(PATH.with_name(name+'.py').read_text())
            cls=next(n for n in tree.body if isinstance(n,ast.ClassDef))
            scope=dict(self.scope,g17PicRef=self.scope['g17PicRef'],eTimer=Mock)
            exec(compile(ast.Module(body=[cls],type_ignores=[]),name,'exec'),scope)
            owner=scope[name]()
            with patch.dict(sys.modules,{'Components.Renderer.Picon':self.module}):owner.changed((0,))
            self.assertEqual(owner.pngname,'/system/picon/bayern3.png',name)
            self.assertEqual(self.native.call_args.args,(BAYERN,))
            path='/skin/picon_220x132/1_0_A_28A2_40F_1_C00000_0_0_0.png'
            self.scope['fileExists']=lambda candidate:candidate==path
            self.assertEqual(owner.findPicon('1_0_A_28A2_40F_1_C00000_0_0_0'),path,name)
            self.scope['fileExists']=lambda path:False

if __name__=='__main__':unittest.main()
