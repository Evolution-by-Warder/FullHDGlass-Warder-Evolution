#!/usr/bin/env python3
"""Fetch reviewed upstream Python text for the 8.1 animation regression."""
import hashlib
import json
from pathlib import Path
import sys
from urllib.request import urlopen

ROOT=Path(__file__).resolve().parents[1]
record=json.loads((ROOT/'design/openatv81-compatibility/upstream.json').read_text())
target=Path(sys.argv[1])
for name,expected in record['normalised_text_sha256'].items():
    url='https://raw.githubusercontent.com/openatv/enigma2/'+record['commit']+'/lib/python/'+name
    with urlopen(url,timeout=30) as response:
        raw=(response.read().decode('utf-8').rstrip()+'\n').encode('utf-8')
    assert hashlib.sha256(raw).hexdigest()==expected,name
    path=target/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
print('Verified pinned OpenATV 8.1 Python fixture:',record['commit'])
