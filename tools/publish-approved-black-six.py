#!/usr/bin/env python3
"""Data-only publication of seven approved black PNG replacements, without an IPK."""
import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
from urllib.request import urlopen
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE_REF = 'a4fe40702b2bdfa10d66421773f0a34aad1fdc72'
SOURCE_REF = '95bbbd6b2c5919087a3579deb84ead04e62323b3'
DELIVERY = ROOT / 'assets/warder/downloads/picons/channels'
PKG = ROOT / 'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fetch_old(url):
    relative = url.split('/assets/', 1)[1]
    url = 'https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/' + BASE_REF + '/assets/' + relative
    with urlopen(url, timeout=90) as response:
        return response.read()


def main():
    protected = [PKG / 'version', PKG / 'plugin.py', PKG / 'warderPiconSync.py', ROOT / 'source/control/control', ROOT / 'update.json', ROOT / 'update-test.json']
    before_code = {str(p): sha(p.read_bytes()) for p in protected}
    assert (PKG / 'version').read_text().strip() == '1.0.13'
    spec = importlib.util.spec_from_file_location('sync', PKG / 'warderPiconSync.py')
    sync = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sync)
    assert sync.runtime_publication()['publication_source_id'] == 'production'
    approved_root = ROOT / '.approved-picons'
    approval = json.loads((approved_root / 'migration/canal-black-six-approved-20261022/manifest.json').read_text())
    rows = approval['picons']
    assert len(rows) == 7 and sum(r['country'] == 'sk' for r in rows) == 5 and sum(r['country'] == 'cz' for r in rows) == 2
    cache = {}
    report = []
    for suffix, source_id in (('', 'production'), ('test-candidate', 'test-candidate')):
        directory = DELIVERY / suffix
        path = directory / 'manifest.json'
        doc = json.loads(path.read_text())
        old_doc = copy.deepcopy(doc)
        checksums = {line.split()[-1]: line.split()[0] for line in (directory / 'SHA256SUMS').read_text().splitlines()}
        changed = set()
        for package in doc['packages']:
            if package['selector_id'] not in ('CANALPLUS_SK', 'CANALPLUS_CZ') or package['family'] != 'channel-black':
                continue
            country = package['selector_id'][-2:].lower()
            if package['sha256'] not in cache:
                cache[package['sha256']] = fetch_old(package['url'])
            data = cache[package['sha256']]
            assert len(data) == package['bytes'] and sha(data) == package['sha256']
            original = zipfile.ZipFile(io.BytesIO(data))
            files = {n: original.read(n) for n in original.namelist()}
            replacements = {}
            for row in rows:
                if row['country'] != country:
                    continue
                name = row['filename']
                png = (approved_root / 'picons/23.5e' / ('canal-plus-' + country) / 'black' / name).read_bytes()
                assert sha(files[name]) == row['before'], (country, name, 'input differs from approved preview')
                assert sha(png) == row['after'], (country, name, 'source differs from approved preview')
                replacements[name] = png
            out = io.BytesIO()
            with zipfile.ZipFile(out, 'w') as archive:
                archive.comment = original.comment
                for entry in original.infolist():
                    archive.writestr(copy.copy(entry), replacements.get(entry.filename, files[entry.filename]))
            data = out.getvalue()
            result = zipfile.ZipFile(io.BytesIO(data))
            assert result.namelist() == original.namelist()
            assert all(result.read(n) == replacements.get(n, files[n]) for n in result.namelist())
            assert len(result.namelist()) == (228 if country == 'sk' else 231)
            filename = 'canalplus_%s_black_220x132_%s.zip' % (country, sha(data)[:16])
            (directory / filename).write_bytes(data)
            package.update(filename=filename, bytes=len(data), sha256=sha(data), source_ref=SOURCE_REF)
            package['url'] = package['url'].rsplit('/', 1)[0] + '/' + filename
            checksums[filename] = sha(data)
            changed.add(package['selector_id'])
            report.append(dict(catalog=source_id, selector=package['selector_id'], filename=filename, sha256=sha(data), png_count=len(result.namelist()),
                               replaced=sorted(replacements), verified_pngs={n: sha(png) for n, png in replacements.items()}, untouched_png_count=len(files) - len(replacements)))
        assert changed == {'CANALPLUS_SK', 'CANALPLUS_CZ'}
        untouched = lambda d: [p for p in d['packages'] if not (p['selector_id'] in changed and p['family'] == 'channel-black')]
        assert untouched(doc) == untouched(old_doc), 'another package changed'
        assert not sync.validate_publication_manifest(doc, source_id)
        doc['approved_canal_black_six_source'] = dict(repository='Evolution-by-Warder/PiconHub-Warder-Evolution', ref=SOURCE_REF)
        path.write_text(json.dumps(doc, indent=2, sort_keys=True) + '\n')
        (directory / 'SHA256SUMS').write_text('\n'.join(f'{digest}  {name}' for name, digest in sorted(checksums.items())) + '\n')
    # Exercise the actual production receiver queue with every style/package.
    doc = json.loads((DELIVERY / 'manifest.json').read_text())
    for package in doc['packages']:
        if package['selector_id'] not in ('CANALPLUS_SK', 'CANALPLUS_CZ'):
            continue
        path = DELIVERY / package['filename']
        if not path.exists():
            data = fetch_old(package['url'])
            assert sha(data) == package['sha256'] and len(data) == package['bytes']
            path.write_bytes(data)
    for tool in ('test-complete-canalplus-install.py', 'test-live-picon-catalog.py', 'verify-radio-release.py'):
        subprocess.run(['python3', str(ROOT / 'tools' / tool)], cwd=ROOT, check=True)
    assert before_code == {str(p): sha(p.read_bytes()) for p in protected}, 'runtime, release or updater changed during data-only publication'
    path = ROOT / 'reports/canal-black-six-approved-20261022.json'
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(dict(source_ref=SOURCE_REF, ipk_version_unchanged='1.0.13', protected_files=before_code, packages=report), indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, indent=2))
    print('PASS: data-only publication; seven exact replacements; other PNGs, all 23.5E packages, other styles, runtime, version and update manifests unchanged')


if __name__ == '__main__':
    main()
