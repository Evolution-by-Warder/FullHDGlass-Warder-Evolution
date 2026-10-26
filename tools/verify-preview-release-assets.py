#!/usr/bin/env python3
"""Verify the exact optional archives before attaching them to a release."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--help-previews',required=True,type=Path);args=parser.parse_args()
manifest=json.loads((ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/preview-assets.json').read_text())
for kind,path,count in (('help',args.help_previews,252),('types',ROOT/'design/preview-assets/warder-infobar-types.zip',78)):
    raw=path.read_bytes();entry=manifest[kind]
    assert len(raw)==entry['size'] and hashlib.sha256(raw).hexdigest()==entry['sha256'],kind
    with zipfile.ZipFile(path) as archive:
        assert len(archive.namelist())==count and archive.testzip() is None
    print('Verified optional preview asset:',kind,len(raw),'bytes',entry['sha256'])
