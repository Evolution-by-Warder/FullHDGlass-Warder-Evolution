#!/usr/bin/env python3
"""Verify original package names, complete sets, install paths and safe cleanup."""
import argparse
import ast
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import struct
import tempfile
from types import SimpleNamespace
import unittest
import zipfile
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
builder=load(ROOT/'tools/build-canonical-picons.py','canonical_build')
installer=load(P/'warderCanonicalPicons.py','canonical_install')
sync=load(P/'warderPiconSync.py','canonical_sync')
publisher=load(ROOT/'tools/publish-native-skin.py','canonical_publisher')
parser=argparse.ArgumentParser();parser.add_argument('--built-dir',type=Path);args,left=parser.parse_known_args()

def png(size,color):
    out=io.BytesIO();Image.new('RGBA',size,color).save(out,format='PNG');return out.getvalue()

def archive(path,root,files):
    with zipfile.ZipFile(path,'w') as z:
        for name,data in files.items():z.writestr(root+'/'+name,data)
    return path


class CanonicalTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.base=Path(self.temp.name)
    def test_overlay_preserved_exactly_and_legacy_dimensions_normalized(self):
        old=archive(self.base/'old.zip','piconProv',{'same.png':png((150,90),'red'),'only.png':png((150,90),'blue')})
        approved=png((220,132),'green');safe=archive(self.base/'safe.zip','piconProv_220x132',{'same.png':approved})
        files,count=builder.merge([({'root':'piconProv'},old),({'root':'piconProv_220x132'},safe)],'provider')
        data=dict(files);self.assertEqual(set(data),{'same.png','only.png'});self.assertEqual(data['same.png'],approved)
        self.assertEqual(Image.open(io.BytesIO(data['only.png'])).size,(220,132));self.assertEqual(count,2)
        output=self.base/'piconProv.zip';builder.package(output,'piconProv',files)
        with zipfile.ZipFile(output) as z:self.assertEqual(z.namelist(),['piconProv/only.png','piconProv/same.png'])
    def test_unsafe_archive_rejected(self):
        path=archive(self.base/'bad.zip','wrong',{'x.png':png((220,132),'red')})
        with self.assertRaises(ValueError):builder.merge([({'root':'piconProv'},path)],'provider')
    def test_only_equal_old_copies_removed(self):
        canonical=self.base/'piconProv';old=self.base/'piconProv_220x132';canonical.mkdir();old.mkdir()
        for name,data in [('same.png',b'equal'),('custom.png',b'old custom')]: (old/name).write_bytes(data)
        (canonical/'same.png').write_bytes(b'equal');(canonical/'custom.png').write_bytes(b'new')
        screen=SimpleNamespace(_warderFilesMatch=lambda a,b:Path(a).read_bytes()==Path(b).read_bytes())
        installer.remove_verified_duplicates(screen,str(self.base),'piconProv')
        self.assertFalse((old/'same.png').exists());self.assertEqual((old/'custom.png').read_bytes(),b'old custom')
        self.assertEqual((canonical/'custom.png').read_bytes(),b'new')
    def test_successful_install_uses_original_directory_and_cleans_equal_duplicates(self):
        raw=png((220,132),'green');source=archive(self.base/'piconProv.zip','piconProv',{'current.png':raw})
        data=source.read_bytes();url=builder.RAW+'assets/warder/downloads/picons/providers/transparent/piconProv.zip'
        entry={'delivery':'canonical-220x132-v1','resolution':[220,132],'root':'piconProv','filename':'piconProv.zip','url':url,'publication_source_id':'fullhd-production','png_count':1,'size':len(data),'sha256':hashlib.sha256(data).hexdigest()}
        target=self.base/'receiver';target.mkdir();old=target/'piconProv_220x132';old.mkdir();(old/'current.png').write_bytes(raw)
        class Screen:
            zzz='original-state'
            def _warderAuxiliaryDestination(_,root):
                self.assertEqual(root,'piconProv');destination=target/root;destination.mkdir(exist_ok=True);return str(destination)
            def _warderFetchAuxiliaryArchive(_,asset,path):self.assertEqual(asset['filename'],'piconProv.zip');Path(path).write_bytes(data)
            def _safeExtractZip(_,path,stage):
                with zipfile.ZipFile(path) as z:z.extractall(stage)
            def cprmFiles(s,root):
                files=list((Path(s.zzz)/root).glob('*.png'))
                for file in files:shutil.copyfile(file,target/root/file.name)
                shutil.rmtree(Path(s.zzz)/root);return len(files),len(files)
            def rmTmp2(_,stage,root):shutil.rmtree(Path(stage)/root,ignore_errors=True)
            def _warderFilesMatch(_,a,b):return Path(a).read_bytes()==Path(b).read_bytes()
        screen=Screen();message=installer.install(screen,'aux-prov','transparent',lambda:('',{'piconProv-220':entry}),lambda x:x)
        self.assertIn('1/1',message);self.assertEqual(screen.zzz,'original-state');self.assertEqual((target/'piconProv/current.png').read_bytes(),raw);self.assertFalse(old.exists())
    def test_bad_descriptor_rejected_before_writes(self):
        screen=SimpleNamespace()
        with self.assertRaises(ValueError):installer.install(screen,'aux-prov','black',lambda:('',{'piconProv-b':{'filename':'wrong.zip'}}),lambda x:x)
    def test_all_220_channel_routes_use_picon(self):
        self.assertEqual(sync.DEFAULT_DESTINATION,'/usr/share/enigma2/picon');self.assertEqual(sync.default_preferences()['destination'],sync.DEFAULT_DESTINATION)
        self.assertEqual(sync.legacy_channel_destination('220x132'),'picon')
        tree=ast.parse((P/'plugin.py').read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='piconSize')
        scope={};exec(compile(ast.Module(body=[fn],type_ignores=[]),'picon-route','exec'),scope)
        self.assertEqual(scope['piconSize']('220,132'),'picon');self.assertEqual(scope['piconSize']('150,90'),'picon');self.assertEqual(scope['piconSize']('400,240'),'picon_400x240')
    def test_raw_publisher_accepts_canonical_paths_only(self):
        from unittest.mock import patch
        url=builder.RAW+'assets/warder/downloads/picons/providers/black/piconProv.zip';response=io.BytesIO(b'zip');response.geturl=lambda:url
        with patch.object(publisher.p,'urlopen',return_value=response):self.assertEqual(publisher.p.GitHub('test-token').public_bytes(url,3),b'zip')
        with self.assertRaises(ValueError):publisher.p.GitHub('test-token').public_bytes(url.replace('piconProv.zip','piconProv_220x132.zip'),3)
    def test_git_deletion_uses_null_blob_without_creating_an_empty_archive(self):
        calls=[]
        class Client:
            def request(_,method,path,payload=None):
                calls.append((method,path,payload))
                if path.startswith('/git/commits/'):return {'tree':{'sha':'base-tree'}}
                if path=='/git/trees':return {'sha':'new-tree'}
                if path=='/git/commits':return {'sha':'new-commit'}
                raise AssertionError(path)
        self.assertEqual(publisher.p.commit(Client(),'old-commit',{'obsolete.zip':None},'Remove obsolete duplicate'),'new-commit')
        entry=next(c[2]['tree'][0] for c in calls if c[1]=='/git/trees')
        self.assertIsNone(entry['sha']);self.assertEqual(entry['path'],'obsolete.zip')

    @unittest.skipIf(args.built_dir is None,'Pass --built-dir for real packages')
    def test_all_six_real_packages_are_original_named_complete_and_220x132(self):
        report=json.loads((args.built_dir/'catalogue.json').read_text());self.assertEqual(len(report['variants']),6)
        for key,entry in report['variants'].items():
            self.assertEqual(entry['filename'],entry['root']+'.zip');raw=(args.built_dir/entry['path']).read_bytes();self.assertEqual(len(raw),entry['size']);self.assertEqual(hashlib.sha256(raw).hexdigest(),entry['sha256'])
            with zipfile.ZipFile(io.BytesIO(raw)) as z:
                self.assertEqual(len(z.namelist()),entry['png_count']);self.assertIsNone(z.testzip())
                for name in z.namelist():
                    self.assertTrue(name.startswith(entry['root']+'/'));data=z.read(name);self.assertEqual(data[:8],b'\x89PNG\r\n\x1a\n');self.assertEqual(struct.unpack('>II',data[16:24]),(220,132),name)
                if key.startswith('provider/'):
                    names={Path(n).name.lower() for n in z.namelist()};self.assertIn('canal+ sk.png',names);self.assertIn('canal+ cz.png',names)
        files,entries=publisher.canonical_files(args.built_dir,{'assets':{'help':{'keep':True},'piconProv-old':{}}})
        catalogue=json.loads(files['assets/warder/downloads.json']);self.assertTrue(catalogue['assets']['help']['keep']);self.assertEqual(len(entries),6)
        self.assertEqual({a['filename'] for key,a in catalogue['assets'].items() if key.startswith(('piconProv','piconSat'))},{'piconProv.zip','piconSat.zip'})
        self.assertTrue(all(files[p] is None for p in report['remove_paths']))


if __name__=='__main__':unittest.main(argv=[__file__]+left)
