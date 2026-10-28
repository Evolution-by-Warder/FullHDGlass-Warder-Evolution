#!/usr/bin/env python3
"""Verify a public known-song lookup without printing or publishing its lyrics."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderLyrics.py'
spec=importlib.util.spec_from_file_location('provider_check',path)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
with tempfile.TemporaryDirectory() as temp:
    result=m.lookup('ABBA','Dancing Queen',Path(temp))
record={'artist':'ABBA','title':'Dancing Queen','status':result['status'],
        'characters':len(result['text']),'text_sha256':hashlib.sha256(result['text'].encode()).hexdigest(),
        'lyrics_published':False,'note':'One known international track is not a coverage measurement.'}
out=ROOT/'packages/test/provider-check.json';out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
if result['status']!='found':raise SystemExit('Known-song live provider check did not return an exact match')
