#!/usr/bin/env python3
"""Pin the approved channel catalogue and issue the minimal 1.0.12 update."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / 'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
ref = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
sync = PKG / 'warderPiconSync.py'
text = sync.read_text()
old = '3c65041a774b67431464dbc08a3a729b43b30577'
assert text.count(old) == 1
sync.write_text(text.replace(old, ref))
(PKG / 'version').write_text('1.0.12\n')
control = ROOT / 'source/control/control'
text = control.read_text()
assert 'Version: 1.0.11-1\n' in text
control.write_text(text.replace('Version: 1.0.11-1\n', 'Version: 1.0.12-1\n'))
builder = ROOT / 'tools/build-complete-canalplus.py'
text = builder.read_text()
assert text.count('31143f35ee537a9b7b1eaad766331cda71dc0c38') == 1
builder.write_text(text.replace('31143f35ee537a9b7b1eaad766331cda71dc0c38', 'f64caf688aae368c1b876d49f99e012fbc5cf0a1'))
change = PKG / 'CHANGELOG-WARDER.md'
change.write_text('## 1.0.12\n\n- Replaced CANAL+, CANAL+ Classics, CANAL+ Crime and CANAL+ Drama in Canal+ SK/CZ in all three styles with the approved originals and Warder backgrounds.\n- Added these four channels to every complete 23.5E colour package (762 PNGs each).\n- Pinned the receiver catalogue to the new verified archives. Radio, menus and MASTER templates are unchanged.\n\n' + change.read_text())
spec = importlib.util.spec_from_file_location('sync', sync)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
for suffix, source_id in (('', 'production'), ('test-candidate', 'test-candidate')):
    doc = json.loads((ROOT / 'assets/warder/downloads/picons/channels' / suffix / 'manifest.json').read_text())
    assert not module.validate_publication_manifest(doc, source_id)
    assert {p['png_count'] for p in doc['packages'] if p['selector_id'] == '235E'} == {762}
for tool in ('test-complete-canalplus-install.py', 'test-release-bytecode.py', 'verify-radio-release.py', 'build-release-ipk.py'):
    subprocess.run(['python3', str(ROOT / 'tools' / tool)], cwd=ROOT, check=True)
ipk = ROOT / 'packages/enigma2-skin-fullhdglass17-warder-evolution_1.0.12_all.ipk'
digest = hashlib.sha256(ipk.read_bytes()).hexdigest()
for name in ('update.json', 'update-test.json'):
    path = ROOT / name
    doc = json.loads(path.read_text())
    doc.update(version='1.0.12', sha256=digest,
               package_url='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/packages/' + ipk.name,
               changelog='Schvalene picony CANAL+, Classics, Crime a Drama: transparentne originaly a biele/cierne pozadia Warder v Canal+ SK, CZ a kompletnych balikoch 23.5E (762 PNG).')
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n')
readme = ROOT / 'README.md'
text = readme.read_text().replace('Latest approved release: 1.0.11', 'Latest approved release: 1.0.12').replace('evolution_1.0.11_all.ipk', 'evolution_1.0.12_all.ipk').replace('both offer 1.0.11', 'both offer 1.0.12')
readme.write_text(text + '\nRelease 1.0.12 replaces the four approved Canal+ channel picons in all three styles in both Canal+ packages and adds them to the complete 23.5E packages (762 PNGs per style). The radio baseline and MASTER templates are preserved.\n')
print('Release 1.0.12', digest, 'catalogue', ref)
