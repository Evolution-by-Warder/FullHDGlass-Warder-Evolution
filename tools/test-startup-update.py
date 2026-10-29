#!/usr/bin/env python3
"""Exercise startup scheduling and the actual existing update offer path offline."""
import ast
import importlib.util
import io
import json
from pathlib import Path
import re
import sys
from types import ModuleType, SimpleNamespace, MethodType
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
pkg=ModuleType('startup_test_package');pkg.__path__=[str(P)];sys.modules[pkg.__name__]=pkg
spec=importlib.util.spec_from_file_location(pkg.__name__+'.warderAutoUpdate',P/'warderAutoUpdate.py');auto=importlib.util.module_from_spec(spec);sys.modules[spec.name]=auto;spec.loader.exec_module(auto)
tree=ast.parse((P/'plugin.py').read_text())
cls=next(c for c in tree.body if isinstance(c,ast.ClassDef) and any(isinstance(n,ast.FunctionDef) and n.name=='_warderAutoUpdateCheck' for n in c.body))

def method(name,scope):
    fn=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name==name)
    env=dict(scope);env['__package__']=pkg.__name__;exec(compile(ast.Module(body=[fn],type_ignores=[]),'startup-runtime','exec'),env);return env[name]

class Call:
    def __init__(self,callback):self.callback=callback;self.pending=True
    def active(self):return self.pending
    def cancel(self):self.pending=False
class Loop:
    def __init__(self):self.workers=[];self.calls=[]
    def spawnProcess(self,worker,exe,argv,env):
        worker.transport=SimpleNamespace(killed=False)
        worker.transport.kill=lambda:setattr(worker.transport,'killed',True)
        self.workers.append((worker,exe,argv))
    def callLater(self,delay,callback):
        call=Call(callback);self.calls.append((delay,call));return call
class Timer:
    def __init__(self):self.starts=[];self.stops=0
    def stop(self):self.stops+=1
    def start(self,*args):self.starts.append(args)
class Session:
    def __init__(self):self.offers=[]
    def openWithCallback(self,*args):self.offers.append(args);return SimpleNamespace(setTitle=lambda title:None)
    def open(self,*args):raise AssertionError('Automatic current/offline checks must stay silent')

class StartupTests(unittest.TestCase):
    def owner(self):
        owner=SimpleNamespace(version='1.0.26',delayTimer=Timer(),session=Session(),onClose=[],updCont=lambda *args:None)
        owner.readVersion=lambda:owner.version
        config=SimpleNamespace(plugins=SimpleNamespace(setupGlass17=SimpleNamespace(par75=SimpleNamespace(value=False))),osd=SimpleNamespace(language=SimpleNamespace(value='sk_SK')))
        def no_network(*args,**kwargs):raise AssertionError('GUI must not access network for automatic check')
        scope={'config':config,'re':re,'MessageBox':SimpleNamespace(TYPE_YESNO=1,TYPE_INFO=2,TYPE_ERROR=3),'update_text':lambda *a,**kw:'offer','urlopen':no_network}
        for name in ('_warderFetchJson','_warderVersionTuple','updatechckact'):
            setattr(owner,name,MethodType(method(name,scope),owner))
        return owner
    def finish(self,loop,manifest=None,code=0):
        worker=loop.workers[-1][0]
        if manifest is not None:worker.outReceived(json.dumps(manifest).encode())
        worker.complete(code)
    def manifest(self,version='1.0.27'):
        return {'version':version,'package_url':auto.BASE+'main/packages/update.ipk','sha256':'a'*64,'changelog':'Zmeny'}
    def test_every_new_screen_schedules_check_after_layout(self):
        init=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='__init__')
        self.assertIn('self.onLayoutFinish.append(self._warderStartAutoUpdateCheck)',ast.unparse(init))
        start=method('_warderStartAutoUpdateCheck',{})
        for _ in range(2):
            owner=self.owner();start(owner);self.assertEqual(owner.delayTimer.starts,[(3000,True)])
    def test_closing_before_initial_delay_cancels_scheduled_check(self):
        owner=self.owner();method('_warderStartAutoUpdateCheck',{})(owner)
        self.assertEqual(len(owner.onClose),1)
        for callback in owner.onClose:callback()
        self.assertEqual(owner.delayTimer.stops,2)
    def test_actual_screen_start_registers_worker_shutdown_on_close(self):
        owner=self.owner();loop=Loop();original=auto.AutoCheck
        with patch.object(auto,'AutoCheck',side_effect=lambda target:original(target,loop)):
            method('_warderAutoUpdateCheck',{})(owner)
        self.assertEqual(len(owner.onClose),1)
        for callback in owner.onClose:callback()
        self.finish(loop,self.manifest())
        self.assertTrue(loop.workers[0][0].transport.killed);self.assertEqual(owner.session.offers,[])
    def test_new_version_offer_uses_child_result_even_when_manual_flag_is_disabled(self):
        owner=self.owner();loop=Loop()
        with patch.object(auto,'fetch',side_effect=AssertionError('No fetch in GUI')):check=auto.AutoCheck(owner,loop)
        self.assertEqual(owner.session.offers,[]);self.assertEqual(loop.workers[0][1],'/usr/bin/python3');self.assertEqual(loop.workers[0][2][-1],auto.PRODUCTION)
        self.finish(loop,self.manifest())
        self.assertEqual(len(owner.session.offers),1);self.assertEqual(owner.warderUpdate['version'],'1.0.27');self.assertFalse(hasattr(owner,'_warderPreparedManifest'))
    def test_manual_check_cancels_pending_automatic_offer(self):
        owner=self.owner();loop=Loop();owner._warderAutoCheck=auto.AutoCheck(owner,loop)
        owner._warderFetchJson=lambda url:self.manifest()
        owner.updatechckact(True)
        self.assertTrue(loop.workers[0][0].transport.killed);self.assertEqual(len(owner.session.offers),1)
        self.finish(loop,self.manifest());self.assertEqual(len(owner.session.offers),1)
    def test_installed_test2_automatic_path_offers_the_published_stable_release(self):
        owner=self.owner();owner.version='1.0.40-test2';loop=Loop()
        auto.AutoCheck(owner,loop)
        self.assertEqual(loop.workers[-1][2][-1],auto.TEST)
        native_test=json.loads((ROOT/'update-test.json').read_text())
        production=json.loads((ROOT/'update-production.json').read_text())
        self.finish(loop,native_test)
        self.assertEqual(len(owner.session.offers),1)
        self.assertEqual(owner.warderUpdate['version'],production['version'])
        self.assertEqual(owner.warderUpdate['url'],production['package_url'])
        self.assertEqual(owner.warderUpdate['sha256'],production['sha256'])
    def test_installed_test2_manual_path_offers_the_published_stable_release(self):
        owner=self.owner();owner.version='1.0.40-test2';requests=[]
        def fetch(url):
            requests.append(url)
            return json.loads((ROOT/'update-test.json').read_text())
        owner._warderFetchJson=fetch
        owner.updatechckact(True)
        production=json.loads((ROOT/'update-production.json').read_text())
        self.assertEqual(requests,[auto.TEST]);self.assertEqual(len(owner.session.offers),1)
        self.assertEqual(owner.warderUpdate['version'],production['version'])
        self.assertEqual(owner.warderUpdate['sha256'],production['sha256'])
    def test_current_version_and_offline_failure_are_silent(self):
        for manifest,code in [(self.manifest('1.0.26'),0),(None,1)]:
            owner=self.owner();loop=Loop();auto.AutoCheck(owner,loop);self.finish(loop,manifest,code);self.assertEqual(owner.session.offers,[])
    def test_close_kills_worker_and_ignores_late_offer(self):
        owner=self.owner();loop=Loop();check=auto.AutoCheck(owner,loop);worker=loop.workers[0][0]
        check.close();self.assertTrue(worker.transport.killed);self.finish(loop,self.manifest());self.assertEqual(owner.session.offers,[])
    def test_timeout_does_not_block_or_offer(self):
        owner=self.owner();loop=Loop();auto.AutoCheck(owner,loop);delay,call=loop.calls[-1];self.assertEqual(delay,20);call.callback();self.finish(loop,None,1);self.assertEqual(owner.session.offers,[])
    def test_prepared_json_cannot_bypass_url_allowlist(self):
        owner=self.owner();owner._warderPreparedManifest=('https://attacker.invalid',self.manifest())
        with self.assertRaises(ValueError):owner._warderFetchJson('https://attacker.invalid')
    def test_worker_fetch_uses_fresh_official_https_url_and_rejects_redirect(self):
        response=io.BytesIO(json.dumps(self.manifest()).encode());response.geturl=lambda:auto.PRODUCTION+'?cb=123';requests=[]
        def opened(request,timeout):requests.append((request.full_url,timeout));return response
        with patch.object(auto,'urlopen',side_effect=opened):self.assertEqual(auto.fetch(auto.PRODUCTION)['version'],'1.0.27')
        self.assertTrue(requests[0][0].startswith(auto.PRODUCTION+'?cb='));self.assertEqual(requests[0][1],12)
        response=io.BytesIO(b'{}');response.geturl=lambda:'https://attacker.invalid'
        with patch.object(auto,'urlopen',return_value=response),self.assertRaises(ValueError):auto.fetch(auto.PRODUCTION)
        with self.assertRaises(ValueError):auto.fetch('http://example.invalid')

if __name__=='__main__':unittest.main()
