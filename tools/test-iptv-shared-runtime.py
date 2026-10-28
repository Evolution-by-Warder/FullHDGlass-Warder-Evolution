"""Exercise the skin's actual shared IPTV worker and selection callback."""
import ast
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import struct
import tempfile
from types import SimpleNamespace
import unittest
import zipfile
import zlib

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('skin_dab_fixture',ROOT/'tools/test-dab-shared-runtime.py')
fixture=importlib.util.module_from_spec(spec);spec.loader.exec_module(fixture)
radio,sync,PKG=fixture.radio,fixture.sync,fixture.PKG
NAME='4097_0_2_1234_5678_EC_0_0_0_0.png'

def png(w,h):
    def chunk(kind,raw):return struct.pack('>I',len(raw))+kind+raw+struct.pack('>I',zlib.crc32(kind+raw)&0xffffffff)
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,6,0,0,0))+chunk(b'IDAT',zlib.compress((b'\0'+b'\xff'*w*4)*h))+chunk(b'IEND',b'')

def resources():
    iptv=radio.engine.iptv;content={};manifest={'schema':1,'status':'verified','collection':iptv.SELECTOR,'packages':{}}
    for res in iptv.RESOLUTIONS:
        manifest['packages'][res]={}
        for style in iptv.STYLES:
            raw=png(*map(int,res.split('x')));output=io.BytesIO()
            with zipfile.ZipFile(output,'w') as z:z.writestr(NAME,raw)
            archive=output.getvalue();url='https://raw.githubusercontent.com/'+iptv.REPOSITORY+'/'+'a'*40+'/picons/IPTV-SK-CZ/packages/iptv-sk-cz-'+style+'-'+res+'.zip'
            content[url]=archive
            manifest['packages'][res][style]={'url':url,'bytes':len(archive),'sha256':hashlib.sha256(archive).hexdigest(),'resolution':res,'files':{NAME:hashlib.sha256(raw).hexdigest()}}
    content[iptv.MANIFEST_URL]=json.dumps(manifest).encode()
    return content

def callback():
    tree=ast.parse((PKG/'plugin.py').read_text())
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='downloadMenu')
    node=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='warderPositionAnswer')
    scope={'warderRadio':radio,'warderPiconSync':sync,'_':lambda value:value}
    exec(compile(ast.Module(body=[node],type_ignores=[]),'skin-selection','exec'),scope)
    return scope[node.name]

def screen():
    return SimpleNamespace(warderPiconPrefs=sync.default_preferences(),warderPiconRows=('wp-pos',),menuListAll={0:['wp-pos','','','','x']},_setWarderPiconPrepared=lambda row:None,createList=lambda:None,reactivate=lambda:None)

class IPTVHostTests(unittest.TestCase):
    def test_all_three_iptv_resolutions_use_no_native_catalog_and_preserve_unrelated_files(self):
        for resolution in radio.engine.iptv.RESOLUTIONS:
            with tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);target=root/'picon';target.mkdir();(target/'keep.png').write_bytes(b'keep');content=resources();calls=[]
                def opener(url):calls.append(url);return io.BytesIO(content[url])
                p=dict(fixture.preferences(target),include_dab=False,include_iptv=True,resolution=resolution)
                worker=radio.Worker(p,opener=opener,enigma2_dir=tmp,lock_path=str(root/'lock'));worker.run()
                self.assertEqual(worker.drain()[-1],('done',{'added':1,'changed':0,'removed':0}))
                self.assertNotIn(radio.engine.sync.RUNTIME_MANIFEST_URL,calls)
                self.assertEqual((target/'keep.png').read_bytes(),b'keep')
                self.assertEqual((target/NAME).read_bytes(),png(*map(int,resolution.split('x'))))
    def test_combined_radio_task_installs_both_transports(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);target=root/'picon';target.mkdir();content=resources();dab=fixture.source()
            worker=radio.Worker(dict(fixture.preferences(target),include_iptv=True),opener=lambda u:io.BytesIO(content[u]) if u in content else dab(u),enigma2_dir=tmp,lock_path=str(root/'lock'));worker.run()
            self.assertEqual(worker.drain()[-1],('done',{'added':3,'changed':0,'removed':0}))
    def test_real_callback_keeps_iptv_separate_from_canalplus_orbital_identity(self):
        s=screen();callback()(s,[dict(radio.IPTV_BINDING),sync.task_binding_for_package_selector('CANALPLUS_SK')])
        self.assertTrue(s.warderPiconPrefs['include_iptv']);self.assertFalse(s.warderPiconPrefs['include_dab'])
        self.assertEqual(s.warderPiconPrefs['package_selectors'],['CANALPLUS_SK'])
        self.assertEqual(s.warderPiconPrefs['positions'],['23.5E'])
    def test_cancel_preserves_selection_but_confirming_empty_selection_clears_it(self):
        s=screen();choose=callback();choose(s,[dict(radio.IPTV_BINDING)])
        self.assertTrue(s.warderPiconPrefs['prepared']);before=dict(s.warderPiconPrefs)
        choose(s,None);self.assertEqual(s.warderPiconPrefs,before)
        choose(s,[]);self.assertFalse(s.warderPiconPrefs['include_iptv']);self.assertFalse(s.warderPiconPrefs['prepared'])

if __name__=='__main__':unittest.main()
