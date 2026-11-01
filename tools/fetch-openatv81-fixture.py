#!/usr/bin/env python3
"""Fetch reviewed upstream Python text for the 8.1 animation regression."""
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys
from urllib.request import urlopen

ROOT=Path(__file__).resolve().parents[1]
record=json.loads((ROOT/'design/openatv81-compatibility/upstream.json').read_text())
target=Path(sys.argv[1])
jobs=[(name,record['commit'],name,expected) for name,expected in record['normalised_text_sha256'].items()]
jobs.extend((name,entry['commit'],entry['path'],entry['sha256']) for name,entry in record.get('extra_revisions',{}).items())

def fetch(job):
    name,commit,source,expected=job
    url='https://raw.githubusercontent.com/openatv/enigma2/'+commit+'/lib/python/'+source
    with urlopen(url,timeout=30) as response:
        raw=(response.read().decode('utf-8').rstrip()+'\n').encode('utf-8')
    assert hashlib.sha256(raw).hexdigest()==expected,name
    path=target/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)

with ThreadPoolExecutor(max_workers=6) as pool:
    list(pool.map(fetch,jobs))  # Every hash/error must complete before any replay runs.
print('Verified pinned OpenATV Python fixtures:',len(jobs),'files; 8.1 base',record['commit'])
