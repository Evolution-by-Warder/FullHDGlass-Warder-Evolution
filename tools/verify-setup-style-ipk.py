#!/usr/bin/env python3
"""Check every candidate payload byte, package identity and feed isolation."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile

ROOT=Path(__file__).resolve().parents[1]
PAYLOAD=ROOT/'source/package-root'
P=PAYLOAD/'usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
version=(P/'version').read_text().strip()
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
    assert files.keys()==expected.keys(), 'Payload file list differs from source'
    for name,path in expected.items():
        assert '__pycache__' not in name and path.suffix not in ('.pyc','.pyo')
        raw=path.read_bytes();assert archive.extractfile(files[name]).read()==raw,name
        if path.suffix=='.py':assert files[name].mtime==(int(hashlib.sha256(raw).hexdigest()[:8],16)&0x7fffffff),name
for name in ('update.json','update-test.json'):
    document=json.loads((ROOT/name).read_text());assert document['version']=='1.0.15'
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==json.loads((ROOT/'design/settings-ui-inventory.json').read_text())['feeds_sha256'][name]
print('PASS:',len(expected),'payload files match source; package metadata, Python cache invalidation and stable/test feeds verified')
