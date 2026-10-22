#!/usr/bin/env python3
"""Build the one-time live catalogue upgrade without changing any picon data."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / 'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
spec = importlib.util.spec_from_file_location('sync', PKG / 'warderPiconSync.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)
assert sync.runtime_publication()['publication_source_id'] == 'production'
delivery = ROOT / 'assets/warder/downloads/picons/channels'
doc = json.loads((delivery / 'manifest.json').read_text())
assert not sync.validate_publication_manifest(doc)
for package in doc['packages']:
    if package['selector_id'] not in ('CANALPLUS_SK', 'CANALPLUS_CZ'):
        continue
    assert sync.trusted_publication_url(package['url'])
    with urlopen(package['url'], timeout=90) as response:
        assert sync.trusted_publication_url(response.geturl())
        data = response.read()
    assert len(data) == package['bytes'] and hashlib.sha256(data).hexdigest() == package['sha256']
    (delivery / package['filename']).write_bytes(data)
for tool in ('test-live-picon-catalog.py', 'test-runtime-safety.py', 'test-complete-canalplus-install.py',
             'test-release-bytecode.py', 'test-picon-native-sync.py', 'verify-radio-release.py', 'build-release-ipk.py'):
    subprocess.run(['python3', str(ROOT / 'tools' / tool)], cwd=ROOT, check=True)
ipk = ROOT / 'packages/enigma2-skin-fullhdglass17-warder-evolution_1.0.13_all.ipk'
digest = hashlib.sha256(ipk.read_bytes()).hexdigest()
for name in ('update.json', 'update-test.json'):
    path = ROOT / name
    doc = json.loads(path.read_text())
    doc.update(version='1.0.13', sha256=digest,
               package_url='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/packages/' + ipk.name,
               changelog='Picony bez dalsich IPK: skin nacita pri kazdom stahovani aktualny schvaleny katalog z main. Zachovana kontrola zdroja, velkosti a SHA-256 archivov. Jednorazovy upgrade z 1.0.12.')
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n')
readme = ROOT / 'README.md'
text = readme.read_text().replace('Latest approved release: 1.0.12', 'Latest approved release: 1.0.13').replace('evolution_1.0.12_all.ipk', 'evolution_1.0.13_all.ipk').replace('both offer 1.0.12', 'both offer 1.0.13')
readme.write_text(text + '\nRelease 1.0.13 follows the current approved main channel-picon catalogue at each download. Future channel-picon content changes need only archive/catalogue publication, without another IPK. Source, redirect, size and SHA-256 checks remain enabled. See [picon update policy](docs/PICON-CATALOG-UPDATES.md).\n')
subprocess.run(['python3', str(ROOT / 'tools/verify-radio-release.py')], cwd=ROOT, check=True)
assert not subprocess.check_output(['git', 'diff', '--name-only', '--', 'assets/warder/downloads'], cwd=ROOT).strip()
print('Release 1.0.13', digest, 'approved live production catalogue; existing picon data preserved')
