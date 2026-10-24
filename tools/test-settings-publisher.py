#!/usr/bin/env python3
import importlib.util
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('publisher',Path(__file__).with_name('publish-settings-update.py'))
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)

class PublisherTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.rev='2'*40;self.main='1'*40;self.staged='3'*40;self.live='4'*40
        self.package=Path(self.temp.name)/'enigma2-skin-fullhdglass-warder-evolution_1.0.16-test263_all.ipk'
        self.package.write_bytes(b'verified test package')
        self.info={'version':'1.0.16-test263','package':self.package.name,'bytes':self.package.stat().st_size,'sha256':hashlib.sha256(self.package.read_bytes()).hexdigest(),'source_commit':self.rev}
        self.refs={'main':self.main,p.WORK:self.rev};self.events=[];self.files={}
        self.previous={'version':'1.0.15'}
        self.patches=[patch.object(p,'head',side_effect=lambda c,b:self.refs[b]),patch.object(p,'content',side_effect=self.content),patch.object(p,'commit',side_effect=self.commit),patch.object(p,'advance',side_effect=self.advance),patch.object(p,'verify_public',side_effect=self.verify)]
        for item in self.patches:item.start();self.addCleanup(item.stop)
    def content(self,c,path,branch):
        if path=='update.json':return p.encoded(self.previous)
        if path=='update-test.json':return p.encoded(self.previous)
        if path=='design/settings-ui-inventory.json':return p.encoded({'feeds_sha256':{}})
        raise AssertionError(path)
    def commit(self,c,parent,files,message):
        self.events.append(('commit',parent,files));self.files.update(files)
        return self.staged if parent==self.rev else self.live
    def advance(self,c,branch,old,new):
        self.assertEqual(self.refs[branch],old);self.refs[branch]=new;self.events.append(('advance',branch,new))
    def verify(self,c,url,size,digest):self.events.append(('verify',url))
    def run_publish(self,assets=None):return p.publish(self.package,self.info,self.rev,self.main,object(),assets or {})
    def test_stage_public_verify_then_both_feeds(self):
        self.assertEqual(self.run_publish(),self.live)
        self.assertEqual(self.refs,{'main':self.live,p.WORK:self.live})
        self.assertEqual([x[0] for x in self.events],['commit','advance','verify','commit','advance','advance'])
        self.assertNotIn('update.json',self.events[0][2])
        self.assertEqual(self.files['update.json'],self.files['update-test.json'])
        inventory=json.loads(self.files['design/settings-ui-inventory.json'])
        self.assertEqual(inventory['feeds_sha256']['update.json'],hashlib.sha256(self.files['update.json']).hexdigest())
    def test_bad_local_digest_refuses_all_writes(self):
        self.info['sha256']='0'*64
        with self.assertRaises(ValueError):self.run_publish()
        self.assertEqual(self.events,[])
    def test_changed_main_refuses_all_writes(self):
        self.refs['main']='5'*40
        with self.assertRaises(ValueError):self.run_publish()
        self.assertEqual(self.events,[])
    def test_superseded_source_refuses_all_writes(self):
        self.refs[p.WORK]='5'*40
        with self.assertRaises(ValueError):self.run_publish()
        self.assertEqual(self.events,[])
    def test_failed_public_package_leaves_old_feeds(self):
        with patch.object(p,'verify_public',side_effect=ValueError('bad public bytes')):
            with self.assertRaises(ValueError):self.run_publish()
        self.assertEqual(self.refs['main'],self.staged)
        self.assertNotIn('update.json',self.files)
        self.assertEqual(self.refs[p.WORK],self.rev)
    def test_bad_optional_asset_refuses_before_staging(self):
        with patch.object(p,'verify_public',side_effect=ValueError('bad asset')):
            with self.assertRaises(ValueError):self.run_publish({'help':{'url':'asset','size':1,'sha256':'0'*64}})
        self.assertEqual(self.events,[])
    def test_idempotent_existing_version(self):
        self.previous={'version':self.info['version'],'package_url':p.RAW+self.package.name,'sha256':self.info['sha256']}
        self.refs['main']=self.live
        self.assertEqual(self.run_publish(),self.live)
        self.assertEqual([x[0] for x in self.events],['verify'])
    def test_existing_version_cannot_change_bytes(self):
        self.previous={'version':self.info['version'],'package_url':p.RAW+self.package.name,'sha256':'0'*64}
        with self.assertRaises(ValueError):self.run_publish()
        self.assertEqual(self.events,[])
    def test_public_byte_integrity_check(self):
        class Client:
            def public_bytes(self,url,size):return b'corrupt'
        with self.assertRaises(ValueError):
            # Use the real verifier, bypassing this test's publication mock.
            self.patches[-1].stop()
            p.verify_public(Client(),'url',3,'0'*64)

if __name__=='__main__':unittest.main()
