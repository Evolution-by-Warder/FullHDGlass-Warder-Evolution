#!/usr/bin/env python3
"""Copy approved existing 23.5E artwork into AntikSAT and generic 16E archives."""
import ast
import copy
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
from urllib.request import urlopen
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE_REF = '0b68f810073f492771117533ae0dbd4b2b024086'
SOURCE_REF = '2d5b1ec8d37742825bb5571508c856d919590377'
DELIVERY = ROOT / 'assets/warder/downloads/picons/channels'
PKG = ROOT / 'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
SELECTORS = {'ANTIKSAT', '160E'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fetch_old(package):
    chunks = []
    for url in package.get('parts') or [package['url']]:
        tail = url.split('/assets/', 1)[1]
        with urlopen('https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/' + BASE_REF + '/assets/' + tail, timeout=120) as response:
            chunks.append(response.read())
    data = b''.join(chunks)
    assert len(data) == package['bytes'] and sha(data) == package['sha256']
    return data


def main():
    protected = [PKG / 'version', PKG / 'plugin.py', PKG / 'warderPiconSync.py', ROOT / 'source/control/control', ROOT / 'update.json', ROOT / 'update-test.json']
    before = {str(p): sha(p.read_bytes()) for p in protected}
    assert (PKG / 'version').read_text().strip() == '1.0.13'
    spec = importlib.util.spec_from_file_location('sync', PKG / 'warderPiconSync.py')
    sync = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sync)
    assert sync.runtime_publication()['publication_source_id'] == 'production'
    approved = ROOT / '.approved-picons'
    mapping = json.loads((approved / 'migration/discovery-235e-to-antik-20261022/manifest.json').read_text())
    replacements = {}
    for row in mapping['rows']:
        png = (approved / row['source_path']).read_bytes()
        assert sha(png) == row['sha256']
        for path in row['target_paths']:
            assert (approved / path).read_bytes() == png
            replacements.setdefault(row['style'], {})[Path(path).name] = png
    assert set(replacements) == {'transparent', 'white', 'black'}
    assert all(len(r) == 2 for r in replacements.values())
    method = next(n for n in ast.walk(ast.parse((PKG / 'plugin.py').read_bytes())) if isinstance(n, ast.FunctionDef) and n.name == '_warderInstallChannelArchive')
    scope = dict(warderPiconSync=sync, os=os, shutil=shutil, stat=stat, tempfile=tempfile, zipfile=zipfile)
    exec(compile(ast.Module(body=[method], type_ignores=[]), 'receiver-installer', 'exec'), scope)
    installer = scope['_warderInstallChannelArchive']
    production = json.loads((DELIVERY / 'manifest.json').read_text())
    candidate = json.loads((DELIVERY / 'test-candidate/manifest.json').read_text())
    initial = {'production': copy.deepcopy(production), 'test-candidate': copy.deepcopy(candidate)}
    generic = [copy.deepcopy(p) for p in candidate['packages'] if p['selector_id'] == '160E']
    assert len(generic) == 3 and sum(p['selector_id'] == '160E' for p in production['packages']) == 3
    cache, report = {}, []
    for suffix, source_id, doc in (('', 'production', production), ('test-candidate', 'test-candidate', candidate)):
        directory = DELIVERY / suffix
        checksums = {line.split()[-1]: line.split()[0] for line in (directory / 'SHA256SUMS').read_text().splitlines()}
        seen = set()
        for package in doc['packages']:
            selector = package['selector_id']
            if selector not in SELECTORS:
                continue
            style = package['family'].removeprefix('channel-')
            expected = replacements[style]
            if package['sha256'] not in cache:
                cache[package['sha256']] = fetch_old(package)
            original = zipfile.ZipFile(io.BytesIO(cache[package['sha256']]))
            files = {n: original.read(n) for n in original.namelist()}
            assert len(files) == (109 if selector == 'ANTIKSAT' else 559)
            assert len(files.keys() & expected.keys()) == 1
            output = io.BytesIO()
            with zipfile.ZipFile(output, 'w') as archive:
                archive.comment = original.comment
                for entry in original.infolist():
                    archive.writestr(copy.copy(entry), expected.get(entry.filename, files[entry.filename]))
                for name in sorted(expected.keys() - files.keys()):
                    entry = zipfile.ZipInfo(name, (2026, 10, 22, 0, 0, 0))
                    entry.compress_type = zipfile.ZIP_DEFLATED
                    entry.create_system = 3
                    entry.external_attr = 0o100644 << 16
                    archive.writestr(entry, expected[name])
            data = output.getvalue()
            result = zipfile.ZipFile(io.BytesIO(data))
            assert set(result.namelist()) == files.keys() | expected.keys()
            assert all(result.read(n) == expected.get(n, old) for n, old in files.items())
            assert all(result.read(n) == png for n, png in expected.items())
            assert len(result.namelist()) == (110 if selector == 'ANTIKSAT' else 560)
            with tempfile.TemporaryDirectory() as temp:
                archive_path, dest = Path(temp) / 'archive.zip', Path(temp) / 'picon'
                archive_path.write_bytes(data)
                dest.mkdir()
                for name in expected:
                    (dest / name).write_bytes(b'old picon')
                installed, available = installer(None, str(archive_path), str(dest), set(expected))
                assert installed == expected.keys() and available == set(result.namelist())
                assert all((dest / name).read_bytes() == png for name, png in expected.items())
            filename = 'warder-' + selector.lower() + '-channel-' + style + '-' + sha(data)[:16] + '.zip'
            branch = 'main' if source_id == 'production' else 'warder-modernization-work'
            url_root = 'https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/' + branch + '/' + directory.relative_to(ROOT).as_posix() + '/'
            old_names = {u.rsplit('/', 1)[-1] for u in package.get('parts', [])}
            parts, records = [], []
            for number, start in enumerate(range(0, len(data), 18 * 1024 * 1024)):
                name = filename + '.part%02d' % number
                chunk = data[start:start + 18 * 1024 * 1024]
                (directory / name).write_bytes(chunk)
                parts.append(url_root + name)
                records.append(dict(filename=name, bytes=len(chunk), sha256=sha(chunk)))
                checksums[name] = sha(chunk)
            doc['parts'] = [p for p in doc['parts'] if p['filename'] not in old_names] + records
            package.pop('url', None)
            package.update(filename=filename, parts=parts, bytes=len(data), sha256=sha(data), source_ref=SOURCE_REF,
                           source_repository='Evolution-by-Warder/PiconHub-Warder-Evolution', png_count=len(result.namelist()),
                           included_references=sorted(n[:-4] for n in result.namelist()))
            seen.add((selector, style))
            report.append(dict(catalog=source_id, selector=selector, style=style, sha256=sha(data), png_count=len(result.namelist()),
                               overwritten=sorted(expected.keys() & files.keys()), added=sorted(expected.keys() - files.keys()),
                               receiver_install_verified=True, unrelated_pngs_unchanged=True,
                               ambiguous_exclusions_preserved=len(package.get('ambiguous_exclusions', []))))
        assert seen == {(selector, style) for selector in SELECTORS for style in replacements}
        other = lambda d: [p for p in d['packages'] if p['selector_id'] not in SELECTORS]
        assert other(doc) == other(initial[source_id]), 'unrelated package changed'
        if source_id == 'production':
            for package in doc['packages']:
                if package['selector_id'] == '160E':
                    old = next(p for p in generic if p['family'] == package['family'])
                    assert package.get('ambiguous_exclusions') == old.get('ambiguous_exclusions')
        assert not sync.validate_publication_manifest(doc, source_id)
        doc['approved_discovery_from_235e'] = dict(repository='Evolution-by-Warder/PiconHub-Warder-Evolution', ref=SOURCE_REF)
        (directory / 'manifest.json').write_text(json.dumps(doc, indent=2, sort_keys=True) + '\n')
        (directory / 'SHA256SUMS').write_text('\n'.join(f'{digest}  {name}' for name, digest in sorted(checksums.items())) + '\n')
    for tool in ('test-live-picon-catalog.py', 'verify-radio-release.py'):
        subprocess.run(['python3', str(ROOT / 'tools' / tool)], cwd=ROOT, check=True)
    assert before == {str(p): sha(p.read_bytes()) for p in protected}
    path = ROOT / 'reports/discovery-235e-to-antik-20261022.json'
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(dict(source_ref=SOURCE_REF, ipk_unchanged='1.0.13', packages=report, protected_files=before), indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, indent=2))
    print('PASS: approved Discovery Channel picons copied exactly to AntikSAT and 16E in three styles; unrelated images and IPK unchanged')


if __name__ == '__main__':
    main()
