#!/usr/bin/env python3
"""Check every candidate payload byte, package identity and feed isolation."""
import argparse
import importlib.util
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile

ROOT=Path(__file__).resolve().parents[1]
PAYLOAD=ROOT/'source/package-root'
P=PAYLOAD/'usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
parser=argparse.ArgumentParser();parser.add_argument('--help-previews',type=Path);args=parser.parse_args()
version=(P/'version').read_text().strip()
spec=importlib.util.spec_from_file_location('png_optimizer',ROOT/'tools/optimize-png.py')
optimizer=importlib.util.module_from_spec(spec);spec.loader.exec_module(optimizer)
package=ROOT/'packages/test'/('enigma2-skin-fullhdglass-warder-evolution_'+version+'_all.ipk')
assert subprocess.check_output(['ar','p',str(package),'debian-binary'])==b'2.0\n'
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['ar','p',str(package),'control.tar.gz'])),mode='r:gz') as archive:
    control=archive.extractfile('./control').read().decode()
    assert 'Package: enigma2-skin-fullhdglass17\n' in control
    assert 'Version: '+version+'-1\n' in control
    for name in ('preinst','postinst','postrm'):
        assert archive.getmember('./'+name).mode & 0o111 == 0o111
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['ar','p',str(package),'data.tar.gz'])),mode='r:gz') as archive:
    files={m.name.removeprefix('./'):m for m in archive if m.isfile()}
    expected={p.relative_to(PAYLOAD).as_posix():p for p in PAYLOAD.rglob('*') if p.is_file() and p.suffix!='.po'}
    assert not any(name.endswith(('warder-help-previews.zip','warder-infobar-types.zip')) for name in files)
    assert files.keys()==expected.keys(), 'Payload file list differs from source'
    for name in files:
        path=expected[name]
        assert '__pycache__' not in name and path.suffix not in ('.pyc','.pyo')
        raw=path.read_bytes()
        expected_raw=optimizer.optimize(raw) if path.suffix.lower()=='.png' else raw
        assert archive.extractfile(files[name]).read()==expected_raw,name
        if path.suffix=='.py':assert files[name].mtime==(int(hashlib.sha256(raw).hexdigest()[:8],16)&0x7fffffff),name
for name in ('update.json','update-test.json'):
    document=json.loads((ROOT/name).read_text())
    inventory=json.loads((ROOT/'design/settings-ui-inventory.json').read_text())
    assert document['version']==inventory.get('current_feed_version','1.0.15')
    if document['version']==version:assert document['sha256']==hashlib.sha256(package.read_bytes()).hexdigest()
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==json.loads((ROOT/'design/settings-ui-inventory.json').read_text())['feeds_sha256'][name]
print('PASS:',len(expected),'payload files match source / compressed PNGs; large preview archives excluded; package metadata, Python cache invalidation and stable/test feeds verified')


assert package.stat().st_size < 16*1024*1024, 'Small IPK size budget exceeded'
