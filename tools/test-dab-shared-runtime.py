#!/usr/bin/env python3
"""Exercise the shared Warder radio engine and the actual skin callback."""
import ast
import hashlib
import importlib
import importlib.util
import io
import json
from pathlib import Path
import struct
import sys
import tempfile
from types import ModuleType, SimpleNamespace
import unittest
import zipfile
import zlib

ROOT=Path(__file__).resolve().parents[1]
PKG=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
package=ModuleType('warder_skin_radio_test');package.__path__=[str(PKG)];sys.modules[package.__name__]=package
radio=importlib.import_module(package.__name__+'.warderRadio')
spec=importlib.util.spec_from_file_location('native_sync',PKG/'warderPiconSync.py');sync=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync)
FIRST='4115_0_2_1019_C98_3_EB0000_1019_100D_10BC.png'
SECOND=FIRST.replace('_C98_3_EB0000_','_5_85_C00000_')
URL='https://raw.githubusercontent.com/Evolution-by-Warder/PiconHub-Warder-Evolution/'+'a'*40+'/picons/DAB/packages/test.zip'

def image():
    def chunk(tag,data):return struct.pack('>I',len(data))+tag+data+struct.pack('>I',zlib.crc32(tag+data)&0xffffffff)
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',220,132,8,6,0,0,0))+chunk(b'IDAT',zlib.compress((b'\0'+b'\xff'*880)*132))+chunk(b'IEND',b'')

def source():
    raw=image();output=io.BytesIO()
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr(FIRST,raw);z.writestr(SECOND,raw)
    archive=output.getvalue();package={'url':URL,'bytes':len(archive),'sha256':hashlib.sha256(archive).hexdigest(),'resolution':'220x132','files':{name:hashlib.sha256(raw).hexdigest() for name in (FIRST,SECOND)}}
    catalog=json.dumps({'schema':1,'status':'verified','packages':{s:dict(package) for s in ('transparent','white','black')}}).encode()
    return lambda url:io.BytesIO(catalog if url==radio.engine.dab.MANIFEST_URL else archive)

def preferences(target,positions=()):
    return dict(sync.default_preferences(str(target)),include_dab=True,positions=list(positions),resolution='220x132',style='black',update_mode=sync.UPDATE_MODE_INCREMENTAL,prepared=True)

class RadioTests(unittest.TestCase):
    def test_canonical_engine_files_match_recorded_shared_source(self):
        root=PKG/'warderRadioCore';record=json.loads((root/'SOURCE.json').read_text())
        self.assertEqual(record['repository'],'Evolution-by-Warder/PiconHub-Warder-Evolution')
        for name,digest in record['sha256'].items():self.assertEqual(hashlib.sha256((root/name).read_bytes()).hexdigest(),digest,name)
    def test_worker_installs_dab_without_loading_a_satellite_catalog(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);target=root/'picon';target.mkdir();(target/'existing.png').write_bytes(b'keep')
            worker=radio.Worker(preferences(target),opener=source(),enigma2_dir=str(root),lock_path=str(root/'lock'));worker.run()
            events=worker.drain();self.assertEqual(events[-1],('done',{'added':2,'changed':0,'removed':0}))
            self.assertEqual((target/'existing.png').read_bytes(),b'keep');self.assertEqual((target/FIRST).read_bytes(),image())
    def test_mixed_task_uses_canonical_positions_from_real_selection(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);target=root/'picon';target.mkdir();p=preferences(target)
            p=sync.set_task_position_bindings(p,[sync.task_binding_for_package_selector('235E')])
            worker=radio.Worker(p,opener=source(),enigma2_dir=str(root),lock_path=str(root/'lock'));worker.run()
            self.assertEqual(worker.drain()[-1],('done',{'added':1,'changed':0,'removed':0}))
            self.assertTrue((target/FIRST).exists());self.assertFalse((target/SECOND).exists())
    def test_invalid_options_are_rejected_before_start(self):
        for change in ({'resolution':'50x30'},{'update_mode':sync.UPDATE_MODE_SYNC_TV},{'style':'other'}):
            with self.assertRaises(ValueError):radio.Worker(dict(preferences('/tmp/picon'),**change))
    def test_cancelled_worker_does_not_install(self):
        with tempfile.TemporaryDirectory() as t:
            p=preferences(Path(t)/'picon');worker=radio.Worker(p,opener=source(),lock_path=str(Path(t)/'lock'));worker.cancel.set();worker.run()
            self.assertEqual(worker.drain()[-1][0],'error');self.assertFalse((Path(t)/'picon'/FIRST).exists())
    def test_actual_skin_callback_accepts_dab_without_fake_orbital_position(self):
        tree=ast.parse((PKG/'plugin.py').read_text());cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='downloadMenu');node=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='warderPositionAnswer')
        scope={'warderRadio':radio,'warderPiconSync':sync,'_':lambda text:text};exec(compile(ast.Module(body=[node],type_ignores=[]),'skin','exec'),scope)
        screen=SimpleNamespace(warderPiconPrefs=sync.default_preferences(),warderPiconRows=('wp-pos',),menuListAll={0:['wp-pos','','','', 'x']},_setWarderPiconPrepared=lambda row:None,createList=lambda:None,reactivate=lambda:None)
        scope[node.name](screen,[dict(radio.DAB_BINDING)])
        self.assertTrue(screen.warderPiconPrefs['include_dab']);self.assertTrue(screen.warderPiconPrefs['prepared']);self.assertEqual(screen.warderPiconPrefs['positions'],[])
        self.assertIn('DAB / DAB+',screen.menuListAll[0][1])
    def test_dab_binding_is_not_a_provider_or_satellite(self):
        self.assertTrue(radio.is_dab(dict(radio.DAB_BINDING)))
        self.assertFalse(radio.is_dab({'canonical_position':'DAB','package_selector':'DAB'}))
    def test_completed_satellite_queue_is_not_restarted_before_dab(self):
        tree=ast.parse((PKG/'plugin.py').read_text());cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='downloadMenu');node=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='dwnLoop')
        scope={'warderPiconSync':sync,'find_sevenzip':lambda _:True,'SEVENZIP':'7z','_':lambda text:text};exec(compile(ast.Module(body=[node],type_ignores=[]),'skin','exec'),scope)
        calls=[]
        screen=SimpleNamespace(dwnTimer=SimpleNamespace(isActive=lambda:False),clrSelectsat=False,warderPiconPrefs=preferences('/tmp/picon'),warderDABOnly=False,warderChannelState='done',warderDABPending=True,
            _warderDABStart=lambda:calls.append('DAB'),_warderRunChannelQueue=lambda:self.fail('Completed satellite queue restarted'))
        scope[node.name](screen)
        self.assertEqual(calls,['DAB']);self.assertFalse(screen.warderDABPending)
    def test_position_picons_scale_the_whole_image_instead_of_cropping(self):
        path=ROOT/'source/package-root/usr/lib/enigma2/python/Components/g17SelectionList.py'
        tree=ast.parse(path.read_text());node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='SelectionEntryComponent')
        content=SimpleNamespace(TYPE_TEXT=0,TYPE_PIXMAP_ALPHABLEND=2,TYPE_PIXMAP_ALPHATEST=1)
        scope={'eListboxPythonMultiContent':content,'RT_HALIGN_LEFT':0,'LoadPixmap':lambda path:('full-size',path),'selectionpng':'selected','BT_SCALE':1,'BT_KEEP_ASPECT_RATIO':2}
        exec(compile(ast.Module(body=[node],type_ignores=[]),'selector','exec'),scope)
        row=scope[node.name]('Astra','235E',0,False,'220x132.png')
        self.assertEqual(row[2][3:5],(75,45))
        self.assertEqual(row[2][8],3)
        self.assertEqual(row[0][1],'235E')
    def test_actual_skin_selector_places_dab_and_dvb_t_first(self):
        tree=ast.parse((PKG/'plugin.py').read_text());cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='warderPositionSelectorScr');node=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='startSelect')
        import os
        config=SimpleNamespace(plugins=SimpleNamespace(setupGlass17=SimpleNamespace(par39=SimpleNamespace(value='/tmp'))))
        scope={'warderPiconSync':sync,'warderRadio':radio,'SKINPATH':'/skin/','PLUGINPATH':str(PKG)+'/','os':os,'config':config,'SATLIST':[['(0.8W) Freesat','', '08w'],['DVB-T sk/cz','','DTT']]}
        exec(compile(ast.Module(body=[node],type_ignores=[]),'skin','exec'),scope)
        rows=[];screen=SimpleNamespace(selected={'DAB'},list=SimpleNamespace(addSelection=lambda *value:rows.append(value)))
        scope[node.name](screen)
        self.assertEqual([row[1]['package_selector'] for row in rows[:2]],['DAB','DVB-T-SK-CZ'])
        self.assertTrue(rows[0][3])
        self.assertEqual(rows[0][0],'DAB / DAB+')
        self.assertTrue(rows[0][-1].endswith('images/selectors/DAB.png'))
        self.assertTrue(rows[1][-1].endswith('images/selectors/DVB-T-SK-CZ.png'))

if __name__=='__main__':unittest.main()
