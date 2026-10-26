#!/usr/bin/env python3
"""Verify atomic optional downloads and a nonblocking settings entry point."""
import importlib.util
import io
import hashlib
import os
from pathlib import Path
import tempfile
import unittest
import subprocess
import shutil
import sys
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
spec=importlib.util.spec_from_file_location('asset_download',P/'warderPreviewAssets.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class Opener:
    def __init__(self,data):self.data=data;self.calls=0
    def open(self,*args,**kwargs):self.calls+=1;return io.BytesIO(self.data)

class AssetsTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.env=patch.dict(os.environ,{mod._ENV:self.temp.name});self.env.start();self.addCleanup(self.env.stop)
        self.data=b'PK-test-verified-preview'
        self.entry={'filename':'small.zip','size':len(self.data),'sha256':hashlib.sha256(self.data).hexdigest(),'url':'https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/download/test/small.zip'}
        self.manifest=patch.object(mod,'_MANIFEST',{'help':self.entry,'types':self.entry});self.manifest.start();self.addCleanup(self.manifest.stop)
    def test_atomic_success_then_offline_reuse_without_network(self):
        opener=Opener(self.data);path=mod._download('help',opener);self.assertEqual(Path(path).read_bytes(),self.data)
        mod._download('help',Opener(b'wrong'));self.assertEqual(opener.calls,1)
        self.assertEqual([p.name for p in Path(self.temp.name).iterdir()],[Path(path).name])
    def test_bad_checksum_never_installs_or_leaves_partial_data(self):
        with self.assertRaises(ValueError):mod._download('help',Opener(b'x'*len(self.data)))
        self.assertEqual(list(Path(self.temp.name).iterdir()),[])
    def test_oversize_is_rejected_and_cleaned(self):
        with self.assertRaises(ValueError):mod._download('help',Opener(self.data+b'x'))
        self.assertEqual(list(Path(self.temp.name).iterdir()),[])
    def test_untrusted_source_and_redirect_are_rejected(self):
        self.entry['url']='https://attacker.invalid/preview.zip'
        with self.assertRaises(ValueError):mod._download('help',Opener(self.data))
        with self.assertRaises(ValueError):mod._Redirect().redirect_request(None,None,302,'',{},'http://github.com/file')
        with self.assertRaises(ValueError):mod._Redirect().redirect_request(None,None,302,'',{},'https://attacker.invalid/file')
    def test_opening_settings_only_schedules_one_daemon_worker(self):
        mod._RUNNING=False
        try:
            with patch.object(mod.threading,'Thread') as thread,patch.object(mod,'_download',side_effect=AssertionError('GUI must not download')):
                mod.ensure_assets(self.temp.name);mod.ensure_assets(self.temp.name)
                thread.assert_called_once();self.assertTrue(thread.call_args.kwargs['daemon']);thread.return_value.start.assert_called_once()
        finally:mod._RUNNING=False
    def test_offline_failure_is_retryable(self):
        mod._RUNNING=True
        with patch.object(mod,'_download',side_effect=OSError('offline')):mod._prepare()
        self.assertFalse(mod._RUNNING)

class FreshInstallTests(unittest.TestCase):
    def test_worker_uses_downloaded_archive_without_original_help_files(self):
        archive=ROOT/'design/preview-assets/warder-infobar-types.zip'
        self.assertTrue(archive.is_file())
        manifest=__import__('json').loads((P/'preview-assets.json').read_text())
        prepared=Path('/tmp/g17_setup_pict.zip')
        # CI produces the same verified optional asset under the shorter name.
        if not prepared.is_file():prepared=Path('/tmp/warder-help-previews.zip')
        self.assertTrue(prepared.is_file())
        art_spec=importlib.util.spec_from_file_location('fresh_help_art',P/'warderHelpArt.py')
        art=importlib.util.module_from_spec(art_spec);art_spec.loader.exec_module(art)
        digest,first=next(iter(art._index()['images'].items()))
        revision=hashlib.sha256((art._STYLE+':'+first['mask']).encode('ascii')).hexdigest()[:12]
        cached=Path(art._CACHE_DIR)/(digest+'-'+revision+'.png')
        previous=cached.read_bytes() if cached.is_file() else None
        cached.unlink(missing_ok=True)
        def restore():
            if previous is not None:cached.write_bytes(previous)
            else:cached.unlink(missing_ok=True)
        self.addCleanup(restore)
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);destination=root/(manifest['help']['sha256']+'-'+manifest['help']['filename'])
            shutil.copyfile(prepared,destination)
            original=root/'not-installed'/Path(first['names'][0]).name
            env=dict(os.environ);env[mod._ENV]=str(root)
            result=subprocess.run([sys.executable,str(P/'warderHelpArt.py'),'--prepare',str(original)],env=env,capture_output=True,text=True,check=True,timeout=20)
            ready=Path(__import__('json').loads(result.stdout))
            self.assertNotEqual(ready,original);self.assertTrue(ready.is_file())
            self.assertEqual(ready.read_bytes()[:8],b'\x89PNG\r\n\x1a\n')
            self.assertFalse(original.exists())

if __name__=='__main__':unittest.main()
