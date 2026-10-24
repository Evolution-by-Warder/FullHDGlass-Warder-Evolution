#!/usr/bin/env python3
"""Validate publication ordering and immutable bridge/native identities."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("category_publication", Path(__file__).with_name("publish-package-transition.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.rev, self.base = "a"*40, "b"*40
        self.refs = {"main": self.base, m.p.WORK: self.rev}
        self.events, self.commits, self.bytes = [], [], {}
        for folder, version, prefix in (("bridge", "1.0.18", m.LEGACY), ("test", "1.0.19", m.NEW)):
            target = self.root / "packages" / folder
            target.mkdir(parents=True)
            name = prefix + "_" + version + "_all.ipk"
            raw = ("verified " + version).encode()
            (target / name).write_bytes(raw)
            digest = hashlib.sha256(raw).hexdigest()
            info = {"version": version, "package": name, "source_commit": self.rev, "bytes": len(raw), "sha256": digest}
            (target / "settings-ui-build.json").write_text(json.dumps(info))
            self.bytes[m.p.RAW + name] = raw
            self.bytes["https://github.com/"+m.p.REPO+"/releases/download/v"+version+"/"+name] = raw
        docs = self.root / "docs"; docs.mkdir()
        (docs / "PRODUCTION-APPROVAL.json").write_text(json.dumps({
            "production_version":"1.0.19","transition_version":"1.0.18","expected_main_sha":self.base,
            "preview_assets":{},"product":"FullHDGlass Warder Evolution","approved_on":"2026-10-24","authorization":"Owner approval"
        }))
        test = self
        class Client:
            def public_bytes(self,url,size):return test.bytes[url]
            def request(self,method,path,payload=None):
                if method=="PATCH":
                    test.events.append("promote")
                    return {"draft":False,"prerelease":False}
                version=path.rsplit("/v",1)[1]
                prefix=m.NEW if version=="1.0.19" else m.LEGACY
                name=prefix+"_"+version+"_all.ipk";raw=test.bytes[m.p.RAW+name]
                return {"id":18 if version=="1.0.18" else 19,"draft":False,"target_commitish":test.rev,
                        "assets":[{"name":name,"size":len(raw),"digest":"sha256:"+hashlib.sha256(raw).hexdigest(),
                                   "browser_download_url":"https://github.com/"+m.p.REPO+"/releases/download/v"+version+"/"+name}]}
        self.client=Client()
        self.patches=[
            patch.object(m,"ROOT",self.root),patch.object(m.p,"GitHub",return_value=self.client),
            patch.object(m.p,"head",side_effect=lambda c,b:self.refs[b]),
            patch.object(m.p,"content",return_value=m.p.encoded({"feeds_sha256":{}})),
            patch.object(m.p,"commit",side_effect=self.commit),patch.object(m.p,"advance",side_effect=self.advance),
            patch.dict(os.environ,{"GH_TOKEN":"test","GITHUB_RUN_ID":"123"}),
            patch.object(sys,"argv",["publisher","--revision",self.rev])]
        for item in self.patches:item.start();self.addCleanup(item.stop)

    def commit(self,client,parent,files,message):
        self.commits.append(files);self.events.append("commit")
        return "c"*40 if len(self.commits)==1 else "d"*40

    def advance(self,client,branch,old,new):
        self.assertEqual(self.refs[branch],old);self.refs[branch]=new;self.events.append("advance")

    def test_both_packages_precede_three_atomic_feed_changes(self):
        m.main()
        self.assertEqual(len(self.commits),2)
        self.assertNotIn("update.json",self.commits[0])
        self.assertEqual(json.loads(self.commits[1]["update.json"])["version"],"1.0.18")
        self.assertEqual(self.commits[1]["update.json"],self.commits[1]["update-test.json"])
        self.assertEqual(json.loads(self.commits[1]["update-production.json"])["version"],"1.0.19")
        self.assertEqual(self.refs["main"],self.refs[m.p.WORK])
        self.assertEqual(self.events[-2:],["promote","promote"])

    def test_bad_build_identity_cannot_start_publication(self):
        path=self.root/"packages/bridge/settings-ui-build.json"
        data=json.loads(path.read_text());data["sha256"]="0"*64;path.write_text(json.dumps(data))
        with self.assertRaises(ValueError):m.main()
        self.assertEqual(self.events,[])

    def test_failed_public_bytes_leave_feeds_and_references_unchanged(self):
        key=next(k for k in self.bytes if k.startswith("https://github.com"))
        self.bytes[key]=b"corrupted"
        with self.assertRaises(ValueError):m.main()
        self.assertEqual(self.events,[])
        self.assertEqual(self.refs["main"],self.base)


if __name__=="__main__":unittest.main()

