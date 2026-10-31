#!/usr/bin/env python3
"""Verify real external archives, download boundaries, native apply and UI paging."""
import ast
import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
P = ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
SKIN = ROOT/'source/package-root/usr/share/enigma2/hd_glass17'
ASSETS = ROOT/'assets/warder/downloads/ui/spinners/online'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


online = load('spinner_online_tests', P/'warderSpinnerOnline.py')
backend = load('spinner_backend_online_tests', P/'warderSpinner.py')
ROWS = online.parse_catalog((ASSETS/'catalog.json').read_bytes())


class ArchiveTests(unittest.TestCase):
    def test_every_individual_archive_and_static_thumbnail_validates(self):
        self.assertEqual(len(ROWS), 154)
        for row in ROWS:
            with self.subTest(spinner=row['id']):
                theme, frames = online.archive_data(row, (ASSETS/row['archive']['path']).read_bytes(), backend.validate_theme)
                self.assertTrue(frames)
                self.assertLessEqual(len(frames),64)
                raw = (ASSETS/row['thumbnail']['path']).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(),row['thumbnail']['sha256'])
                online.png(raw,(80,80))

    def test_only_requested_resource_is_downloaded(self):
        calls=[]
        row=ROWS[7]
        def opener(request, **kwargs):
            calls.append(request.full_url)
            return io.BytesIO((ASSETS/row['thumbnail']['path']).read_bytes())
        online.checked_resource(row['thumbnail'],'png',online.MAX_THUMB,opener)
        self.assertEqual(calls,[online.BASE+row['thumbnail']['path']])
        self.assertFalse(any(url.endswith('.zip') for url in calls))

    def test_invalid_catalog_paths_duplicates_and_oversized_resources_are_rejected(self):
        base=json.loads((ASSETS/'catalog.json').read_text())
        mutations=[lambda d:d['entries'][0]['archive'].update(path='archives/../../bad.zip'),
                   lambda d:d['entries'][0]['thumbnail'].update(path='https://example.com/p.png'),
                   lambda d:d['entries'].append(d['entries'][0]),
                   lambda d:d['entries'][0]['archive'].update(bytes=online.MAX_ZIP+1)]
        for change in mutations:
            data=copy.deepcopy(base);change(data)
            with self.assertRaises((ValueError,KeyError)):
                online.parse_catalog(json.dumps(data).encode())

    def test_traversal_unlisted_member_and_bad_pixels_are_rejected_before_install(self):
        row=copy.deepcopy(ROWS[2]);raw=(ASSETS/row['archive']['path']).read_bytes()
        for name, body in [('../outside',b'x'),('wait99.png',b'broken')]:
            stream=io.BytesIO(raw)
            with zipfile.ZipFile(stream,'a') as archive:archive.writestr(name,body)
            changed=stream.getvalue();row['archive'].update(bytes=len(changed),sha256=online.digest(changed))
            with self.assertRaises(ValueError):online.archive_data(row,changed,backend.validate_theme)

    def test_checksum_mismatch_and_animated_or_corrupt_png_are_rejected(self):
        row=ROWS[4]
        with self.assertRaises(ValueError):online.archive_data(row,b'wrong',backend.validate_theme)
        raw=bytearray((ASSETS/row['thumbnail']['path']).read_bytes());raw[-5]^=1
        with self.assertRaises(ValueError):online.png(bytes(raw),(80,80))


class CacheTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)/'skin';self.root.mkdir()
        shutil.copytree(SKIN/'spinner',self.root/'spinner')
        shutil.copytree(SKIN/'spinner-themes',self.root/'spinner-themes')
        self.cache=Path(self.temp.name)/'downloaded'
        self.original={p.name:p.read_bytes() for p in (self.root/'spinner').iterdir()}

    def install(self,row):
        return online.install_selected(row,(ASSETS/row['archive']['path']).read_bytes(),backend,self.root,self.cache)

    def test_download_does_not_apply_and_native_switch_restores_dove(self):
        key=self.install(ROWS[3])
        self.assertEqual({p.name:p.read_bytes() for p in (self.root/'spinner').iterdir()},self.original)
        self.assertIn(key,backend.catalog(download_root=self.cache)['themes'])
        self.assertTrue(backend.apply(key,self.root,download_root=self.cache))
        self.assertTrue(backend.apply('dove',self.root,download_root=self.cache))
        self.assertEqual({p.name:p.read_bytes() for p in (self.root/'spinner').iterdir()},self.original)

    def test_cache_keeps_active_and_one_pending_set_and_is_offline_usable(self):
        active=self.install(ROWS[3]);backend.apply(active,self.root,download_root=self.cache)
        for row in ROWS[4:10]:
            self.install(row)
            self.assertEqual(len(backend.downloaded(self.cache)),2)
            self.assertIn(active,backend.downloaded(self.cache))
        with patch.object(online,'fetch',side_effect=AssertionError('Unexpected network')):
            backend.apply(active,self.root,download_root=self.cache)

    def test_user_file_prevents_pruning_and_is_preserved(self):
        self.install(ROWS[3]);other=self.install(ROWS[4]);(self.cache/other/'my-file').write_text('keep')
        # Both inactive candidates need pruning validation; make the first one
        # protected as the currently selected native set.
        first=next(k for k in backend.downloaded(self.cache) if k!=other)
        backend.apply(first,self.root,download_root=self.cache)
        with self.assertRaises(ValueError):self.install(ROWS[5])
        self.assertEqual((self.cache/other/'my-file').read_text(),'keep')

    def test_corrupted_cache_does_not_stop_bundled_settings_choices(self):
        key=self.install(ROWS[3]);(self.cache/key/'manifest.json').write_text('broken')
        data=backend.catalog(download_root=self.cache)
        self.assertEqual(set(data['themes']),{'dove','bakussa'})

    def test_symlink_cache_is_never_followed(self):
        target=Path(self.temp.name)/'user';target.mkdir();(target/'keep').write_text('safe')
        self.cache.symlink_to(target,target_is_directory=True)
        with self.assertRaises(ValueError):self.install(ROWS[3])
        self.assertEqual((target/'keep').read_text(),'safe')


class ScreenContractTests(unittest.TestCase):
    def test_real_screen_renders_only_six_rows_and_releases_temp_images(self):
        class Widget:
            def __init__(self,*args,**kwargs):self.items=[];self.l=self;self.instance=True
            def setItemHeight(self,*a):pass
            def setFont(self,*a):pass
            def setList(self,items):self.items=items
            def moveToIndex(self,index):self.index=index
            def setText(self,text):self.text=text
        class Screen(dict):
            def __init__(self,session):dict.__init__(self);self.onLayoutFinish=[];self.onClose=[]
            def setTitle(self,title):self.title=title
            def close(self,answer):self.answer=answer;self.cleanup()
        class Deferred:
            def addCallbacks(self,*args):return self
            def addBoth(self,*args):return self
        config=ModuleType('Components.config');config.config=SimpleNamespace(osd=SimpleNamespace(language=SimpleNamespace(value='sk_SK')))
        modules={
            'Components.ActionMap':SimpleNamespace(ActionMap=Widget),
            'Components.Label':SimpleNamespace(Label=Widget),
            'Components.MenuList':SimpleNamespace(MenuList=Widget),
            'Components.MultiContent':SimpleNamespace(MultiContentEntryText=lambda **kw:kw,MultiContentEntryPixmapAlphaBlend=lambda **kw:kw),
            'Screens.Screen':SimpleNamespace(Screen=Screen),
            'enigma':SimpleNamespace(eListboxPythonMultiContent=object,gFont=lambda *a:a,loadPNG=lambda path:path,BT_SCALE=1),
            'twisted.internet.threads':SimpleNamespace(deferToThread=lambda worker:Deferred()),
            'Components.config':config,
        }
        package=ModuleType('spinner_screen_contract');package.__path__=[str(P)]
        modules[package.__name__]=package
        modules[package.__name__+'.warderSpinner']=backend
        modules[package.__name__+'.warderSpinnerOnline']=online
        with patch.dict(sys.modules,modules):
            module=load(package.__name__+'.warderSpinnerScreen',P/'warderSpinnerScreen.py')
            box=module.SpinnerChoice(None);box.rows=copy.deepcopy(ROWS);box.show_page()
            self.assertEqual(len(box['list'].items),6)
            self.assertFalse(box.busy)
            self.assertEqual(box.pending_page,None)
            box.step(6);self.assertEqual(len(box['list'].items),6)
            box.loaded(copy.deepcopy(ROWS));self.assertLessEqual(len(box['list'].items),6)
            temp=Path(box.temp.name);box.cancel();self.assertFalse(temp.exists())
            self.assertTrue(box.closed)
            self.assertIsNone(box.answer)

    def test_approved_old_bakussa_tail_is_recognized_after_default_overlay(self):
        from PIL import Image
        definitions=json.loads((ROOT/'design/spinner-choice/sources.json').read_text())
        definition=next(d for d in definitions['themes'] if d['id']=='bakussa')
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);shutil.copytree(SKIN/'spinner',root/'spinner');shutil.copytree(SKIN/'spinner-themes',root/'spinner-themes')
            with zipfile.ZipFile(ROOT/definition['source']['original_archive']) as archive:
                for index in (19,20):
                    name='wait%d.png'%index
                    im=Image.open(io.BytesIO(archive.read('HG glass17 spinner  (bakussa)/'+name)))
                    im.convert('RGBa').resize((104,104),Image.Resampling.LANCZOS).convert('RGBA').save(root/'spinner'/name,format='PNG',compress_level=9)
                    self.assertEqual(online.digest((root/'spinner'/name).read_bytes()),definition['legacy_frames'][index-1]['sha256'])
            backend.apply('bakussa',root,download_root=root/'none')
            self.assertEqual(len(list((root/'spinner').iterdir())),20)
            backend.apply('dove',root,download_root=root/'none')
            self.assertEqual(len(list((root/'spinner').iterdir())),18)


if __name__ == '__main__':
    unittest.main()
