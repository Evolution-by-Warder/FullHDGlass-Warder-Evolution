#!/usr/bin/env python3
"""Check silent default logging and cleanup on failed runtime file writes."""
import ast
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
PYTHON=ROOT/'source/package-root/usr/lib/enigma2/python'
PLUGIN=PYTHON/'Plugins/Extensions/setupGlass17'
sys.path.insert(0,str(PLUGIN))


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


class CleanupTests(unittest.TestCase):
    def test_all_legacy_loggers_have_no_file_or_console_side_effect(self):
        relatives=['Plugins/Extensions/setupGlass17/plugin.py','Plugins/Extensions/setupGlass17/weather.py',
                   'Plugins/Extensions/setupGlass17/E_weather.py','Components/Renderer/g17MenuEntry.py',
                   'Components/Renderer/g17MenuEntry2.py','Components/Renderer/g17Poster2.py','Screens/Menu-new17.py']
        for relative in relatives:
            with self.subTest(module=relative):
                tree=ast.parse((PYTHON/relative).read_bytes())
                function=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='Writelog')
                scope={};exec(compile(ast.Module(body=[function],type_ignores=[]),relative,'exec'),scope)
                output=io.StringIO()
                with patch('builtins.open',side_effect=AssertionError('Unexpected diagnostic write')),contextlib.redirect_stdout(output):
                    scope['Writelog']('test message')
                self.assertEqual(output.getvalue(),'')

    def test_receiver_lyrics_lookup_and_cache_hit_do_not_write_trace(self):
        lyrics=load('cleanup_lyrics',PLUGIN/'warderLyrics.py')
        import json
        row={'artistName':'Artist','trackName':'Song','plainLyrics':'An original test line.'}
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            kwargs={'site_providers':(),'opener':lambda *a,**kw:io.BytesIO(json.dumps([row]).encode())}
            self.assertEqual(lyrics.lookup('Artist','Song',folder,**kwargs)['status'],'found')
            self.assertEqual(lyrics.lookup('Artist','Song',folder,**kwargs)['status'],'found')
            self.assertFalse((folder/'.last-result').exists())
            self.assertEqual(len(list(folder.glob('*.json'))),1)

    def test_failed_lyrics_json_serialization_leaves_no_temporary_file(self):
        lyrics=load('cleanup_lyrics_atomic',PLUGIN/'warderLyrics.py')
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'cache.json';path.write_text('old')
            with self.assertRaises(TypeError):lyrics.atomic_json(path,object())
            self.assertEqual(path.read_text(),'old');self.assertEqual(list(Path(tmp).iterdir()),[path])

    def test_generated_cache_pruning_is_bounded_and_preserves_other_files_and_links(self):
        cache=load('cleanup_cache',PLUGIN/'warderRuntimeCache.py')
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);unknown=folder/'user-cover.jpg';unknown.write_bytes(b'user')
            files=[]
            for number in range(5):
                path=folder/(('%040x'%number)+'.jpg');path.write_bytes(b'cache')
                os.utime(path,(number+1,number+1));files.append(path)
            alias=folder/(('a'*40)+'.jpg');alias.symlink_to(unknown)
            cache.prune(tmp,r'[0-9a-f]{40}\.jpg',2,100,keep=(files[-1],))
            self.assertEqual([path.exists() for path in files],[False,False,False,True,True])
            self.assertTrue(alias.is_symlink());self.assertEqual(unknown.read_bytes(),b'user')

    def test_atomic_cover_failure_keeps_old_file_and_removes_partial_file(self):
        cache=load('cleanup_cache_atomic',PLUGIN/'warderRuntimeCache.py')
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'cover.jpg';path.write_bytes(b'old')
            with patch.object(cache.os,'replace',side_effect=OSError('disk error')):
                with self.assertRaises(OSError):cache.write_atomic(str(path),b'new')
            self.assertEqual(path.read_bytes(),b'old');self.assertEqual(list(Path(tmp).iterdir()),[path])

    def test_metadata_refreshes_artwork_evicted_from_the_ram_cache(self):
        info=load('cleanup_program_info',PLUGIN/'warderProgramInfo.py')
        record={'artwork_path':'/missing/generated-cache.jpg','provider_id':'7'}
        with patch.object(info,'_readCache',return_value=record),patch.object(info,'_artworkPath',return_value='/new/cover.jpg') as fetch:
            self.assertEqual(info.lookup('Title')['artwork_path'],'/new/cover.jpg')
        fetch.assert_called_once_with(record)

    def test_radio_hook_failure_removes_first_temp_when_second_creation_fails(self):
        source=(PLUGIN/'plugin.py').read_text();tree=ast.parse(source)
        function=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='_warderRadioGrabRender')
        import types
        reference=types.SimpleNamespace(toString=lambda:'1:0:2:0:0:0:0:0:0:0:')
        scope={'NavigationInstance':types.SimpleNamespace(instance=types.SimpleNamespace(getCurrentlyPlayingServiceReference=lambda:reference)),
               'is_radio_reference':lambda ref:True,'_warderOwiGetUrlArg':lambda request,key:None,
               '_warderNativeGrabRender':lambda self,request:b'fallback','os':os,'tempfile':tempfile}
        exec(compile(ast.Module(body=[function],type_ignores=[]),'radio-hook','exec'),scope)
        with tempfile.TemporaryDirectory() as tmp:
            fd,path=tempfile.mkstemp(dir=tmp)
            with patch.object(tempfile,'mkstemp',side_effect=[(fd,path),OSError('full')]),patch('builtins.open',side_effect=OSError('missing')):
                self.assertEqual(scope['_warderRadioGrabRender'](object(),object()),b'fallback')
            self.assertFalse(Path(path).exists())

    def test_failed_package_read_deletes_partial_ipk(self):
        import hashlib
        from urllib.request import Request
        source=(PLUGIN/'plugin.py').read_text();tree=ast.parse(source)
        method=next(node for node in ast.walk(tree) if isinstance(node,ast.FunctionDef) and node.name=='_warderDownload')
        class BrokenResponse:
            calls=0
            def __enter__(self):return self
            def __exit__(self,*args):return False
            def geturl(self):return 'https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/packages/test.ipk'
            def read(self,size):
                self.calls+=1
                if self.calls==1:return b'partial'
                raise OSError('connection lost')
        scope={'Request':Request,'hashlib':hashlib,'urlopen':lambda *a,**kw:BrokenResponse(),'os':os}
        exec(compile(ast.Module(body=[method],type_ignores=[]),'updater','exec'),scope)
        import types
        owner=types.SimpleNamespace(readVersion=lambda:'1.0.39')
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'test.ipk'
            with self.assertRaises(OSError):scope['_warderDownload'](owner,BrokenResponse().geturl(),str(target))
            self.assertFalse(target.exists())

    def test_download_error_uses_deferred_result_instead_of_a_second_modal(self):
        import re
        import types
        from unittest.mock import Mock
        tree=ast.parse((PLUGIN/'plugin.py').read_text())
        method=next(node for node in ast.walk(tree) if isinstance(node,ast.FunctionDef) and node.name=='updCont')
        box=Mock();session=types.SimpleNamespace(open=Mock(return_value=box))
        owner=types.SimpleNamespace(session=session,warderUpdate={'url':'https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/packages/cleanup-test.ipk','version':'1.0.40-test1','sha256':'a'*64},
                                    _warderDownload=Mock(side_effect=OSError('offline')),_warderInstallFinished=Mock())
        scope={'os':os,'re':re,'_':lambda text:text,'update_text':lambda *args,**kwargs:'progress',
               'MessageBox':types.SimpleNamespace(TYPE_INFO=0,TYPE_ERROR=1),
               'config':types.SimpleNamespace(osd=types.SimpleNamespace(language=types.SimpleNamespace(value='sk')))}
        exec(compile(ast.Module(body=[method],type_ignores=[]),'updater-modal','exec'),scope)
        with patch.object(os.path,'exists',return_value=False):scope['updCont'](owner,True)
        self.assertEqual(session.open.call_count,1)
        owner._warderInstallFinished.assert_called_once_with(1)
        self.assertIn('offline',owner.warderInstallOutput[0])


if __name__=='__main__':unittest.main()
