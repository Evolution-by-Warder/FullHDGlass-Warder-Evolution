#!/usr/bin/env python3
"""Reuse the exact receiver-approved test5 helpers for the normal release."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile
from urllib.request import urlopen
from bitrate_package import validate_helpers
from sync_header_version import sync_headers

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / 'source/package-root'
PLUGIN = 'usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/'
VERSION = '1.0.55'
URL = 'https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/download/v1.0.54-test5/enigma2-plugin-skins-fullhdglass_1.0.54-test5_all.ipk'
SHA = 'e00abf5a30741152b3e1d1ea7908bb95914f87befbe94d91a97e80c65b2083a7'

def main():
    before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('update*.json')}
    assert (PAYLOAD / PLUGIN / 'version').read_text().strip() == VERSION
    assert 'Version: ' + VERSION + '-1\n' in (ROOT / 'source/control/control').read_text()
    with urlopen(URL, timeout=120) as response:
        raw = response.read(17204829)
    assert len(raw) == 17204828 and hashlib.sha256(raw).hexdigest() == SHA
    with tempfile.NamedTemporaryFile(suffix='.ipk') as package:
        package.write(raw); package.flush()
        data = subprocess.check_output(['ar', 'p', package.name, 'data.tar.gz'])
    names = {'usr/bin/warder-bitrate-' + name: 0o755 for name in ('arm', 'mipsel', 'aarch64')}
    names.update({PLUGIN + 'warderBitrateTargets.json': 0o644})
    names.update({'usr/share/doc/fullhdglass/' + name: 0o644 for name in ('bitrate-musl-COPYRIGHT', 'bitrate-zig-LICENSE')})
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as archive:
        members = {m.name.removeprefix('./'): m for m in archive if m.isfile()}
        for name, mode in names.items():
            path = PAYLOAD / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(archive.extractfile(members[name]).read())
            path.chmod(mode)
    proof = json.loads((ROOT / 'reports/bitrate-test5-20261101.json').read_text())
    assert proof['package_sha256'] == SHA
    out = ROOT / 'packages/test'; out.mkdir(parents=True, exist_ok=True)
    for name, report in zip(('arm', 'mipsel', 'aarch64'), proof['builds']):
        filename = 'bitrate-helper-build.json' if name == 'arm' else 'bitrate-helper-' + name + '-build.json'
        (out / filename).write_text(json.dumps(report, indent=2) + '\n')
    validate_helpers(ROOT)
    sync_headers(PAYLOAD, check=True)
    path = ROOT / 'design/settings-ui-inventory.json'
    inventory = json.loads(path.read_text())
    inventory['feeds_sha256'] = {name: before[name] for name in ('update.json', 'update-test.json')}
    for filename, field in [('update.json', 'current_feed_version'), ('update-test.json', 'test_feed_version'), ('update-production.json', 'production_feed_version')]:
        inventory[field] = json.loads((ROOT / filename).read_text())['version']
    path.write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + '\n')
    (out / 'spinner-choice-feed-isolation.json').write_text(json.dumps(before, indent=2) + '\n')
    assert before == {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('update*.json')}
    print('Prepared stable ' + VERSION + ' with unchanged receiver-approved helpers and public feeds')

if __name__ == '__main__':
    main()
