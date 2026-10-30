#!/usr/bin/env python3
"""Check shared auxiliary routing and exclude preview ZIP release attachments."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
assets=json.loads((P/'preview-assets.json').read_text())
catalogue=json.loads((ROOT/'assets/warder/downloads.json').read_text())['assets']
paths={'help':'ui/help/g17_setup_pict.zip','types':'ui/icon-set-previews/warder-infobar-types.zip'}
keys={'help':'help','types':'infobar_types_preview'}
prefix='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/'
for kind,path in paths.items():
    entry=assets[kind]
    assert entry['url']==prefix+path,kind
    live=catalogue[keys[kind]]
    assert all(live[key]==entry[key] for key in ('url','filename','size','sha256')),kind
    local=ROOT/'assets/warder/downloads'/path
    if local.exists():
        raw=local.read_bytes()
        assert len(raw)==entry['size'] and hashlib.sha256(raw).hexdigest()==entry['sha256'],kind
assert not (ROOT/'design'/'preview-assets'/'warder-infobar-types.zip').exists()
workflow=(ROOT/'.github/workflows/build-settings-ui.yml').read_text()
creation=workflow.split('gh release create "$TAG"',1)[1].split('fi',1)[0]
assert '/tmp/g17_setup_pict.zip' not in creation
assert 'warder-infobar-types.zip' not in creation
for base in (ROOT/'source',ROOT/'tools',ROOT/'.github/workflows'):
    for path in base.rglob('*'):
        if path.is_file() and path.suffix in ('.py','.yml') and path!=Path(__file__):
            assert 'design'+'/preview-assets/warder-infobar-types.zip' not in path.read_text(),str(path)
print('PASS: canonical auxiliary paths, catalogue, checksums and package-only release attachments')
