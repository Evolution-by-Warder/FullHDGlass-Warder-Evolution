#!/usr/bin/env python3
"""Publish approved CS Film / CS Horror picons in all styles without changing the IPK."""
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
BASE_REF = '61393baaf124907bc153c133d325b065fb312c10'
SOURCE_REF = 'f39316527f1b3aa792bd6ffd734acbbd51a2a989'
DELIVERY = ROOT / 'assets/warder/downloads/picons/channels'
PKG = ROOT / 'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fetch_old(url):
    relative = url.split('/assets/', 1)[1]
    url = 'https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/' + BASE_REF + '/assets/' + relative
    with urlopen(url, timeout=120) as response:
        return response.read()


def main():
    protected = [PKG / 'version', PKG / 'plugin.py', PKG / 'warderPiconSync.py', ROOT / 'source/control/control', ROOT / 'update.json', ROOT / 'update-test.json']
    before_code = {str(p): sha(p.read_bytes()) for p in protected}
    assert (PKG / 'version').read_text().strip() == '1.0.13'
    spec = importlib.util.spec_from_file_location('sync', PKG / 'warderPiconSync.py')
    sync = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sync)
    assert sync.runtime_publication()['publication_source_id'] == 'production'
    source = ROOT / '.approved-picons/migration/cs-film-approved-20261022'
    approval = json.loads((source / 'manifest.json').read_text())
    pngs = {style: (source / row['file']).read_bytes() for style, row in approval['styles'].items()}
    assert all(sha(pngs[style]) == row['sha256'] for style, row in approval['styles'].items())
    targets = set(approval['target_identities'])
    assert len(targets) == 2
    for row in approval['source_paths']:
        assert (ROOT / '.approved-picons' / row['path']).read_bytes() == pngs[row['style']]
    tree = ast.parse((PKG / 'plugin.py').read_bytes())
    method = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == '_warderInstallChannelArchive')
    scope = dict(warderPiconSync=sync, os=os, shutil=shutil, stat=stat, tempfile=tempfile, zipfile=zipfile)
    exec(compile(ast.Module(body=[method], type_ignores=[]), 'receiver-installer', 'exec'), scope)
    installer = scope['_warderInstallChannelArchive']
    cache = {}
    report = []
    selectors = {'235E', 'CANALPLUS_SK', 'CANALPLUS_CZ'}
    for suffix, source_id in (('', 'production'), ('test-candidate', 'test-candidate')):
        directory = DELIVERY / suffix
        path = directory / 'manifest.json'
        doc = json.loads(path.read_text())
        old_doc = copy.deepcopy(doc)
        checksums = {line.split()[-1]: line.split()[0] for line in (directory / 'SHA256SUMS').read_text().splitlines()}
        changed = set()
        for package in doc['packages']:
            selector = package['selector_id']
            if selector not in selectors or package['family'] not in ('channel-transparent', 'channel-white', 'channel-black'):
                continue
            style = package['family'].removeprefix('channel-')
            png = pngs[style]
            if package['sha256'] not in cache:
                cache[package['sha256']] = b''.join(fetch_old(url) for url in (package.get('parts') or [package['url']]))
            old = cache[package['sha256']]
            assert len(old) == package['bytes'] and sha(old) == package['sha256']
            original = zipfile.ZipFile(io.BytesIO(old))
            files = {n: original.read(n) for n in original.namelist()}
            selected = targets & files.keys()
            assert len(selected) == (2 if selector == '235E' else 1)
            out = io.BytesIO()
            with zipfile.ZipFile(out, 'w') as archive:
                archive.comment = original.comment
                for entry in original.infolist():
                    archive.writestr(copy.copy(entry), png if entry.filename in selected else files[entry.filename])
            data = out.getvalue()
            result = zipfile.ZipFile(io.BytesIO(data))
            assert result.namelist() == original.namelist()
            assert all(result.read(n) == (png if n in selected else files[n]) for n in result.namelist())
            assert len(result.namelist()) == (762 if selector == '235E' else 231 if selector == 'CANALPLUS_CZ' else 228 if style == 'black' else 226)
            with tempfile.TemporaryDirectory() as temp:
                archive_path, dest = Path(temp) / 'archive.zip', Path(temp) / 'picon'
                archive_path.write_bytes(data)
                dest.mkdir()
                for name in selected:
                    (dest / name).write_bytes(b'obsolete CS Film')
                installed, available = installer(None, str(archive_path), str(dest), selected)
                assert installed == selected and available == files.keys()
                assert all((dest / name).read_bytes() == png for name in selected)
            filename = ('warder-235e-channel-' + style + '-%s.zip' if selector == '235E' else
                        'canalplus_' + selector[-2:].lower() + '_' + style + '_220x132_%s.zip') % sha(data)[:16]
            if package.get('parts'):
                old_names = {url.rsplit('/', 1)[-1] for url in package['parts']}
                url_root = package['parts'][0].rsplit('/', 1)[0] + '/'
                urls, records = [], []
                for number, start in enumerate(range(0, len(data), 18 * 1024 * 1024)):
                    part_name = filename + '.part%02d' % number
                    chunk = data[start:start + 18 * 1024 * 1024]
                    (directory / part_name).write_bytes(chunk)
                    urls.append(url_root + part_name)
                    records.append(dict(filename=part_name, bytes=len(chunk), sha256=sha(chunk)))
                    checksums[part_name] = sha(chunk)
                doc['parts'] = [p for p in doc['parts'] if p['filename'] not in old_names] + records
                package['parts'] = urls
            else:
                (directory / filename).write_bytes(data)
                package['url'] = package['url'].rsplit('/', 1)[0] + '/' + filename
                checksums[filename] = sha(data)
            package.update(filename=filename, bytes=len(data), sha256=sha(data), source_ref=SOURCE_REF)
            changed.add((selector, style))
            report.append(dict(catalog=source_id, selector=selector, filename=filename, sha256=sha(data), png_count=len(files),
                               cs_film_references=sorted(selected), style=style, changed_pngs=sorted(n for n in selected if files[n] != png),
                               approved_png_sha256=sha(png), untouched_png_count=len(files) - len(selected), receiver_install_verified=True))
        assert changed == {(selector, style) for selector in selectors for style in pngs}
        untouched = lambda d: [p for p in d['packages'] if not (p['selector_id'] in selectors and p['family'] in ('channel-transparent', 'channel-white', 'channel-black'))]
        assert untouched(doc) == untouched(old_doc), 'another package or colour changed'
        assert not sync.validate_publication_manifest(doc, source_id)
        doc['approved_cs_film_source'] = dict(repository='Evolution-by-Warder/PiconHub-Warder-Evolution', ref=SOURCE_REF)
        path.write_text(json.dumps(doc, indent=2, sort_keys=True) + '\n')
        (directory / 'SHA256SUMS').write_text('\n'.join(f'{digest}  {name}' for name, digest in sorted(checksums.items())) + '\n')
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
    assert before_code == {str(p): sha(p.read_bytes()) for p in protected}, 'runtime, release or updater changed'
    path = ROOT / 'reports/cs-film-approved-20261022.json'
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(dict(source_ref=SOURCE_REF, ipk_version_unchanged='1.0.13', protected_files=before_code, packages=report), indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, indent=2))
    print('PASS: approved CS Film / CS Horror transparent, white and black PNGs published; all other images, service references, membership and IPK unchanged')


if __name__ == '__main__':
    main()
