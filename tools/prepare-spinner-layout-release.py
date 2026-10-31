#!/usr/bin/env python3
"""Prepare the next numbered IPK, preserving all public update manifests."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from sync_header_version import sync_headers

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
VERSION = '1.0.52'


def main():
    feeds = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('update*.json')}
    current = (PLUGIN/'version').read_text().strip()
    if current != VERSION:
        subprocess.run([sys.executable,str(ROOT/'tools/prepare-spinner-choice-test.py')],check=True)
        control = ROOT/'source/control/control'
        text = control.read_text()
        assert 'Version: 1.0.51-1\n' in text
        control.write_text(text.replace('Version: 1.0.51-1\n','Version: '+VERSION+'-1\n',1))
        (PLUGIN/'version').write_text(VERSION+'\n')
        for name,text in {
            'history.txtSk':'Výber spinnerov využíva dostupnú plochu obrazovky.\nSprávna veľkosť a pomer strán náhľadov bez orezávania.',
            'history.txt':'Spinner selection fills the available screen area.\nCorrect thumbnail sizing and aspect ratio without clipping.',
        }.items():
            path=PLUGIN/name
            path.write_text('FullHDGlass '+VERSION+' — 31.10.2026\n'+text+'\n\n'+path.read_text())
    sync_headers(ROOT/'source/package-root')
    # Refresh only the staging feed snapshot. Controller logic baselines stay intact.
    path=ROOT/'design/settings-ui-inventory.json'
    inventory=json.loads(path.read_text())
    inventory['feeds_sha256']={key:feeds[key] for key in ('update.json','update-test.json')}
    for filename,field in [('update.json','current_feed_version'),('update-test.json','test_feed_version'),('update-production.json','production_feed_version')]:
        inventory[field]=json.loads((ROOT/filename).read_text())['version']
    path.write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
    assert feeds=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('update*.json')}
    folder=ROOT/'packages/test';folder.mkdir(parents=True,exist_ok=True)
    (folder/'spinner-choice-feed-isolation.json').write_text(json.dumps(feeds,indent=2)+'\n')
    print('Prepared '+VERSION+' with public feeds unchanged')


if __name__=='__main__':main()
