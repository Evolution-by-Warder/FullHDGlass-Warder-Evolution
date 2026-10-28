#!/usr/bin/env python3
"""Validate silent weekly updates without a receiver or external HTTP requests."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
pkg=ModuleType('radio_update_tests');pkg.__path__=[str(P)];sys.modules[pkg.__name__]=pkg
spec=importlib.util.spec_from_file_location(pkg.__name__+'.warderRadioUpdate',P/'warderRadioUpdate.py')
auto=importlib.util.module_from_spec(spec);sys.modules[spec.name]=auto;spec.loader.exec_module(auto)
NOW=1800000000


def bouquet(count=3000):
    lines=['#NAME Warder Radio Streams\n','#SERVICE 1:64:2:0:0:0:0:0:0:0:\n#DESCRIPTION Slovensko\n',
           '#SERVICE 1:64:2:0:0:0:0:0:0:0:\n#DESCRIPTION Čechy\n']
    for i in range(1,count+1):
        lines.append(f'#SERVICE 4097:0:2:{i:X}:1:EC:0:0:0:0:https%3a//station.test/{i}\n#DESCRIPTION Radio {i}\n')
    return ''.join(lines).encode()


class Call:
    def __init__(self,callback):self.callback=callback;self.pending=True
    def active(self):return self.pending
    def cancel(self):self.pending=False


class Loop:
    def __init__(self):self.calls=[];self.workers=[]
    def callLater(self,delay,callback):
        call=Call(callback);self.calls.append((delay,call));return call
    def spawnProcess(self,worker,exe,argv,env):
        worker.transport=SimpleNamespace(kill=lambda:worker.complete(1))
        self.workers.append((worker,exe,argv))


class RefreshTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.directory=Path(self.temp.name);self.target=self.directory/auto.FILENAME
        self.old=b'#NAME Warder Radio Streams\n#SERVICE 1:64:2:0:0:0:0:0:0:0:\n#DESCRIPTION Old\n'
        self.target.write_bytes(self.old)
        self.raw=bouquet()
        self.report={'bouquet_sha256':hashlib.sha256(self.raw).hexdigest(),'total_stations':3000}
        self.requests=[]
    def fetch(self,url,limit):
        self.requests.append(url)
        if 'api.github.com' in url:return json.dumps([{'sha':'a'*40}]).encode()
        if url.endswith('.json'):return json.dumps(self.report).encode()
        return self.raw
    def run_refresh(self,now=NOW):
        with patch.object(auto,'fetch',side_effect=self.fetch):return auto.refresh(self.directory,now)
    def test_replaces_only_managed_file_and_retains_backup(self):
        other=self.directory/'userbouquet.personal.radio';other.write_text('untouched')
        self.assertEqual(self.run_refresh(),{'changed':True})
        self.assertEqual(self.target.read_bytes(),self.raw)
        self.assertEqual((self.directory/(auto.FILENAME+'.bak')).read_bytes(),self.old)
        self.assertEqual(other.read_text(),'untouched')
    def test_weekly_timestamp_survives_restart(self):
        self.run_refresh();self.requests.clear()
        self.assertEqual(self.run_refresh(NOW+6*86400)['skipped'],'not-due')
        self.assertEqual(self.requests,[])
        self.assertEqual(self.run_refresh(NOW+auto.WEEK),{'changed':False})
        self.assertEqual(len(self.requests),1)
    def test_failed_network_preserves_file_and_retries_after_six_hours(self):
        with patch.object(auto,'fetch',side_effect=OSError('offline')):
            with self.assertRaises(OSError):auto.refresh(self.directory,NOW)
        self.assertEqual(self.target.read_bytes(),self.old)
        self.assertEqual(self.run_refresh(NOW+1)['skipped'],'not-due')
        self.assertTrue(self.run_refresh(NOW+auto.RETRY)['changed'])
    def test_bad_checksum_preserves_last_good_file(self):
        self.raw=b'truncated'
        with self.assertRaises(ValueError):self.run_refresh()
        self.assertEqual(self.target.read_bytes(),self.old)
    def test_valid_checksum_does_not_bypass_structure_checks(self):
        self.raw=b'#NAME Warder Radio Streams\n#SERVICE broken\n'
        self.report['bouquet_sha256']=hashlib.sha256(self.raw).hexdigest()
        with self.assertRaises(ValueError):self.run_refresh()
        self.assertEqual(self.target.read_bytes(),self.old)
    def test_concurrent_user_edit_is_not_overwritten(self):
        fetch=self.fetch
        def edit(url,limit):
            result=fetch(url,limit)
            if url.endswith('.radio'):self.target.write_bytes(b'personal edit')
            return result
        with patch.object(auto,'fetch',side_effect=edit),self.assertRaises(ValueError):auto.refresh(self.directory,NOW)
        self.assertEqual(self.target.read_bytes(),b'personal edit')
    def test_missing_or_unmanaged_file_is_not_imported(self):
        self.target.unlink()
        self.assertEqual(self.run_refresh()['skipped'],'not-installed')
        self.target.write_bytes(b'#NAME My personal radio\n')
        self.assertEqual(self.run_refresh()['skipped'],'unmanaged')
        self.assertEqual(self.requests,[])
    def test_symlink_is_not_replaced(self):
        self.target.unlink();self.target.symlink_to(self.directory/'personal')
        (self.directory/'personal').write_bytes(self.old)
        self.assertEqual(self.run_refresh()['skipped'],'not-installed')
        self.assertTrue(self.target.is_symlink())
    def test_incorrect_system_clock_does_not_download(self):
        self.assertEqual(self.run_refresh(123)['skipped'],'clock')
        self.assertEqual(self.requests,[])
    def test_clock_correction_does_not_block_due_check(self):
        self.assertTrue(auto.due({'last_success':NOW+auto.WEEK,'last_attempt':NOW+1},NOW))
    def test_unexpected_redirect_is_rejected(self):
        response=io.BytesIO(b'{}');response.geturl=lambda:'https://other.invalid/'
        with patch.object(auto,'urlopen',return_value=response),self.assertRaises(ValueError):auto.fetch(auto.REPORT_URL,100)
    def test_gui_launches_child_and_reloads_only_on_change(self):
        reloads=[];loop=Loop()
        ctl=auto.Controller(loop,lambda:reloads.append(True))
        self.assertEqual(loop.calls[0][0],60)
        with patch.object(auto,'fetch',side_effect=AssertionError('GUI may not access network')):ctl.check()
        worker,exe,argv=loop.workers[-1]
        self.assertEqual(exe,'/usr/bin/python3');self.assertEqual(argv[-1],'--refresh')
        worker.outReceived(b'{"changed":true}');worker.complete(0)
        self.assertEqual(reloads,[True]);self.assertEqual(loop.calls[-1][0],3600)
        ctl.check();loop.workers[-1][0].complete(1)
        self.assertEqual(reloads,[True])
        ctl.close()
    def test_frozen_guard_rejects_modified_background_hook(self):
        import ast
        spec=importlib.util.spec_from_file_location('weekly_style_guard',ROOT/'tools/style-setup-screens.py')
        style=importlib.util.module_from_spec(spec);spec.loader.exec_module(style)
        original=(P/'plugin.py').read_text()
        altered=original.replace('start_radio_update(reason)', 'start_radio_update(0)', 1)
        self.assertNotEqual(style.normalized(ast.parse(original)),style.normalized(ast.parse(altered)))

    def test_session_hook_installs_silent_controller(self):
        import ast
        tree=ast.parse((P/'plugin.py').read_text())
        start=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='startHdg17')
        self.assertIn('start_radio_update(reason)',ast.unparse(start))


if __name__=='__main__':unittest.main()
