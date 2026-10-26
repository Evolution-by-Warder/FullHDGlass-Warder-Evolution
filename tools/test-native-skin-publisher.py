#!/usr/bin/env python3
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('native_pub',ROOT/'tools/publish-native-skin.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


class NativePublisherTests(unittest.TestCase):
    def setUp(self):
        self.folder=tempfile.TemporaryDirectory();self.addCleanup(self.folder.cleanup)
        self.path=Path(self.folder.name)/(m.PACKAGE+'_1.0.20_all.ipk');self.raw=b'tested native IPK';self.path.write_bytes(self.raw)
        self.hash=hashlib.sha256(self.raw).hexdigest();self.rev='a'*40;self.base='b'*40
        self.info={'version':'1.0.20','package':self.path.name,'bytes':len(self.raw),'sha256':self.hash,'source_commit':self.rev}
        self.approval={'enabled':True,'version':'1.0.20','expected_main_sha':self.base,'authorization':'Owner request','changelog':'Translucent settings'}
        self.feed={'version':'1.0.19','sha256':'old','package_url':'old'}
        self.heads={'main':self.base,m.p.WORK:self.rev};self.commits=[];self.public={m.p.RAW+self.path.name:self.raw,'https://github.com/release.ipk':self.raw}
        self.release={'draft':False,'prerelease':False,'target_commitish':self.rev,'assets':[{'name':self.path.name,'size':len(self.raw),'digest':'sha256:'+self.hash,'browser_download_url':'https://github.com/release.ipk'}]}
        class Client:
            def request(_,method,path):return self.release
        self.client=Client()
        def content(client,path,branch):
            if path=='update-production.json':return json.dumps(self.feed).encode()
            if path=='docs/PRODUCTION.json':return json.dumps({'transition':{'version':'1.0.18'},'preview_assets':{}}).encode()
            if path=='design/settings-ui-inventory.json':return b'{}'
            raise AssertionError('Unexpected content read '+path)
        def commit(client,parent,files,message):
            self.commits.append(files);return str(len(self.commits))*40
        def advance(client,branch,old,new):
            if self.heads[branch]!=old:raise ValueError('Moved')
            self.heads[branch]=new
        def verify(client,url,size,digest):
            raw=self.public[url]
            if len(raw)!=size or hashlib.sha256(raw).hexdigest()!=digest:raise ValueError('Wrong public bytes')
        for name,value in {'content':content,'commit':commit,'advance':advance,'head':lambda client,branch:self.heads[branch],'verify_public':verify}.items():
            p=patch.object(m.p,name,side_effect=value);p.start();self.addCleanup(p.stop)
        buf=io.BytesIO()
        with tarfile.open(fileobj=buf,mode='w:gz') as tar:
            raw=('Package: '+m.PACKAGE+'\nVersion: 1.0.20-1\n').encode();item=tarfile.TarInfo('./control');item.size=len(raw);tar.addfile(item,io.BytesIO(raw))
        p=patch.object(m.subprocess,'check_output',return_value=buf.getvalue());p.start();self.addCleanup(p.stop)

    def publish(self):return m.publish(self.path,self.info,self.rev,self.approval,self.client,{})
    def test_verified_native_feed_advances_without_touching_legacy_bridge(self):
        self.publish();self.assertEqual(len(self.commits),2)
        files=self.commits[-1];self.assertIn('update-production.json',files)
        self.assertNotIn('update.json',files);self.assertNotIn('update-test.json',files)
        record=json.loads(files['docs/PRODUCTION.json']);self.assertEqual(record['transition']['version'],'1.0.18')
        self.assertEqual(self.heads['main'],self.heads[m.p.WORK])
    def test_same_canonical_help_bundle_updates_original_download_and_catalogue(self):
        raw=b'canonical tested help ZIP';bundle=Path(self.folder.name)/'g17_setup_pict.zip';bundle.write_bytes(raw)
        digest=hashlib.sha256(raw).hexdigest()
        entry={'filename':bundle.name,'size':len(raw),'sha256':digest,'url':'https://github.com/help.zip'}
        raw_url='https://raw.githubusercontent.com/'+m.p.REPO+'/main/assets/warder/downloads/ui/help/g17_setup_pict.zip'
        self.public[entry['url']]=raw;self.public[raw_url]=raw
        old=m.p.content.side_effect
        def content(client,path,branch):
            if path=='assets/warder/downloads.json':return json.dumps({'assets':{'help':{'old':True},'other':{'keep':True}}}).encode()
            return old(client,path,branch)
        m.p.content.side_effect=content
        m.publish(self.path,self.info,self.rev,self.approval,self.client,{'help':entry},bundle)
        staged=self.commits[0]
        self.assertEqual(staged['assets/warder/downloads/ui/help/g17_setup_pict.zip'],raw)
        catalogue=json.loads(staged['assets/warder/downloads.json'])
        self.assertEqual(catalogue['assets']['help']['sha256'],digest)
        self.assertEqual(catalogue['assets']['help']['url'],raw_url)
        self.assertEqual(catalogue['assets']['other'],{'keep':True})

    def test_wrong_download_prevents_all_publication(self):
        self.public['https://github.com/release.ipk']=b'wrong'
        with self.assertRaises(ValueError):self.publish()
        self.assertFalse(self.commits)
    def test_moved_branch_prevents_all_publication(self):
        self.heads['main']='c'*40
        with self.assertRaises(ValueError):self.publish()
        self.assertFalse(self.commits)
    def test_prerelease_cannot_be_published_as_stable(self):
        self.release['prerelease']=True
        with self.assertRaises(ValueError):self.publish()
        self.assertFalse(self.commits)
    def test_version_requires_explicit_authorization(self):
        self.approval['enabled']=False
        with self.assertRaises(ValueError):self.publish()
        self.assertFalse(self.commits)
    def test_immutable_retry_checks_public_package_and_never_mutates_feeds(self):
        self.feed={'version':'1.0.20','sha256':self.hash,'package_url':m.p.RAW+self.path.name}
        self.publish();self.assertFalse(self.commits)
    def test_immutable_collision_refuses_different_hash(self):
        self.feed={'version':'1.0.20','sha256':'wrong','package_url':m.p.RAW+self.path.name}
        with self.assertRaises(ValueError):self.publish()
        self.assertFalse(self.commits)


if __name__=='__main__':unittest.main()
