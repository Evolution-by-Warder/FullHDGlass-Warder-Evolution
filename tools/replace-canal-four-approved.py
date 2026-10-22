#!/usr/bin/env python3
"""Publish the twelve user-approved PNGs, preserving all unrelated package bytes."""
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
import struct
import tempfile
from urllib.request import urlopen
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE_REF = 'f64caf688aae368c1b876d49f99e012fbc5cf0a1'
BASE_REF = '26ec75283aee4912bceba730348afcc17992ba52'
PKG = ROOT / 'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
DELIVERY = ROOT / 'assets/warder/downloads/picons/channels'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    source = ROOT / '.approved-picons'
    approval = json.loads((source / 'migration/canal-four-approved-20261022/manifest.json').read_text())
    rows = approval['picons']
    assert len(rows) == 4
    approved = {}
    for style in ('transparent', 'white', 'black'):
        approved[style] = {}
        for row in rows:
            name = row['filename']
            pngs = [(source / 'picons/23.5e' / ('canal-plus-' + country) / style / name).read_bytes()
                    for country in ('sk', 'cz')]
            assert pngs[0] == pngs[1]
            assert sha(pngs[0]) == row['styles'][style]['sha256']
            assert pngs[0][:8] == b'\x89PNG\r\n\x1a\n'
            assert struct.unpack('>II', pngs[0][16:24]) == (220, 132)
            approved[style][name] = pngs[0]
    spec = importlib.util.spec_from_file_location('sync', PKG / 'warderPiconSync.py')
    sync = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sync)
    tree = ast.parse((PKG / 'plugin.py').read_bytes())
    method = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == '_warderInstallChannelArchive')
    scope = dict(warderPiconSync=sync, os=os, shutil=shutil, stat=stat, tempfile=tempfile, zipfile=zipfile)
    exec(compile(ast.Module(body=[method], type_ignores=[]), str(PKG / 'plugin.py'), 'exec'), scope)
    installer = scope['_warderInstallChannelArchive']
    report = []
    cache = {}
    for suffix, source_id in (('', 'production'), ('test-candidate', 'test-candidate')):
        directory = DELIVERY / suffix
        manifest = directory / 'manifest.json'
        doc = json.loads(manifest.read_text())
        before = copy.deepcopy(doc)
        sums = directory / 'SHA256SUMS'
        checksums = {line.split()[-1]: line.split()[0] for line in sums.read_text().splitlines()}
        changed = set()
        for package in doc['packages']:
            selector, family = package['selector_id'], package['family']
            if selector not in ('235E', 'CANALPLUS_SK', 'CANALPLUS_CZ') or family not in ('channel-transparent', 'channel-white', 'channel-black'):
                continue
            style = family.removeprefix('channel-')
            selected = approved[style]
            if package['sha256'] not in cache:
                urls = package.get('parts') or [package['url']]
                chunks = []
                for url in urls:
                    relative = url.split('/assets/', 1)[1]
                    stable_url = 'https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/' + BASE_REF + '/assets/' + relative
                    with urlopen(stable_url, timeout=120) as response:
                        chunks.append(response.read())
                cache[package['sha256']] = b''.join(chunks)
            old = cache[package['sha256']]
            assert sha(old) == package['sha256'] and len(old) == package['bytes']
            original = zipfile.ZipFile(io.BytesIO(old))
            old_files = {n: original.read(n) for n in original.namelist()}
            assert len(old_files) == len(original.namelist()) == package['png_count']
            if selector != '235E':
                assert selected.keys() <= old_files.keys(), 'Canal+ must replace existing identities'
            output = io.BytesIO()
            with zipfile.ZipFile(output, 'w') as archive:
                archive.comment = original.comment
                for entry in original.infolist():
                    archive.writestr(entry, selected.get(entry.filename, old_files[entry.filename]))
                for name in sorted(selected.keys() - old_files.keys()):
                    entry = zipfile.ZipInfo(name, date_time=(2026, 10, 22, 0, 0, 0))
                    entry.compress_type = zipfile.ZIP_DEFLATED
                    entry.create_system = 3
                    entry.external_attr = 0o100644 << 16
                    archive.writestr(entry, selected[name])
            data = output.getvalue()
            result = zipfile.ZipFile(io.BytesIO(data))
            assert set(result.namelist()) == old_files.keys() | selected.keys()
            assert all(result.read(n) == (selected[n] if n in selected else old_files[n]) for n in result.namelist())
            # Run the actual receiver replacement installer on an existing picon directory.
            with tempfile.TemporaryDirectory() as temp:
                archive_path, dest = Path(temp) / 'archive.zip', Path(temp) / 'picon'
                archive_path.write_bytes(data)
                dest.mkdir()
                for name in selected:
                    (dest / name).write_bytes(b'obsolete picon')
                installed, available = installer(None, str(archive_path), str(dest))
                assert installed == available == set(result.namelist())
                assert all((dest / n).read_bytes() == png for n, png in selected.items())
            filename = ('warder-235e-channel-%s-%s.zip' if selector == '235E' else
                        'canalplus_' + selector[-2:].lower() + '_%s_220x132_%s.zip') % (style, sha(data)[:16])
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
            package.update(filename=filename, bytes=len(data), sha256=sha(data), png_count=len(result.namelist()),
                           included_references=sorted(n[:-4] for n in result.namelist()), source_ref=SOURCE_REF)
            changed.add((selector, family))
            report.append(dict(catalog=source_id, selector=selector, style=style, filename=filename,
                               sha256=sha(data), png_count=len(result.namelist()),
                               replaced=sorted(selected.keys() & old_files.keys()), added=sorted(selected.keys() - old_files.keys()),
                               approved_pngs={n: sha(png) for n, png in selected.items()},
                               untouched_png_count=len(old_files.keys() - selected.keys()), receiver_install_verified=True))
        expected = {(selector, 'channel-' + style) for selector in ('235E', 'CANALPLUS_SK', 'CANALPLUS_CZ') for style in ('transparent', 'white', 'black')}
        assert changed == expected
        untouched = lambda d: [p for p in d['packages'] if (p['selector_id'], p['family']) not in expected]
        assert untouched(doc) == untouched(before)
        assert not sync.validate_publication_manifest(doc, source_id), sync.validate_publication_manifest(doc, source_id)
        doc['approved_canal_four_source'] = dict(repository='Evolution-by-Warder/PiconHub-Warder-Evolution', ref=SOURCE_REF)
        manifest.write_text(json.dumps(doc, indent=2, sort_keys=True) + '\n')
        sums.write_text('\n'.join(f'{digest}  {name}' for name, digest in sorted(checksums.items())) + '\n')
    path = ROOT / 'reports/canal-four-approved-20261022.json'
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
