#!/usr/bin/env python3
"""Append approved DAB radio picons to owning satellite ZIPs, preserving originals."""
import argparse
import base64
import concurrent.futures
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import struct
import zipfile
from urllib.request import Request, urlopen

REPO = 'Evolution-by-Warder/FullHDGlass-Warder-Evolution'
PICON_REPO = 'Evolution-by-Warder/PiconHub-Warder-Evolution'
PICON_REF = 'ebd5c4b4ee41d9ac6b37ac635a321fca74f3dc50'
DIRECTORY = 'assets/warder/downloads/picons/channels/'
LIVE_ROOT = 'https://raw.githubusercontent.com/' + REPO + '/main/' + DIRECTORY
REFERENCE = re.compile(r'^4115(?:_[0-9A-F]+){9}\.png$')
HEX = re.compile(r'^[0-9a-f]{40}$')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git_sha(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def public(url):
    if not url.startswith('https://raw.githubusercontent.com/'):
        raise ValueError('Only public raw GitHub assets are accepted')
    with urlopen(Request(url, headers={'User-Agent': 'Warder-DAB-publication', 'Cache-Control': 'no-cache'}), timeout=60) as response:
        if response.geturl() != url:
            raise ValueError('Unexpected asset redirect')
        return response.read(100 * 1024 * 1024 + 1)

class GitHub:
    def __init__(self, token=None):
        self.token = token

    def api(self, method, path, payload=None):
        headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'Warder-DAB-publication'}
        if self.token:
            headers['Authorization'] = 'Bearer ' + self.token
        data = None if payload is None else json.dumps(payload).encode()
        if data is not None:
            headers['Content-Type'] = 'application/json'
        with urlopen(Request('https://api.github.com/repos/' + REPO + path, data=data, headers=headers, method=method), timeout=90) as response:
            return json.load(response)

    def blob(self, data):
        value = self.api('POST', '/git/blobs', {'content': base64.b64encode(data).decode(), 'encoding': 'base64'})
        if value['sha'] != git_sha(data):
            raise ValueError('Uploaded Git blob differs')
        return value['sha']

def position(name):
    if not REFERENCE.fullmatch(name):
        raise ValueError('Invalid exact DAB reference')
    return int(name.split('_')[6], 16) >> 16

def approved_artwork():
    prefix = 'https://raw.githubusercontent.com/' + PICON_REPO + '/' + PICON_REF + '/picons/DAB/'
    raw = public(prefix + 'catalog/release.json')
    document = json.loads(raw)
    if document.get('status') != 'verified' or set(document['packages']) != {'transparent', 'white', 'black'}:
        raise ValueError('DAB catalog is not approved')
    result = {}
    for style, package in document['packages'].items():
        if not re.fullmatch(r'https://raw\.githubusercontent\.com/' + re.escape(PICON_REPO) + r'/[0-9a-f]{40}/picons/DAB/packages/[a-z0-9-]+\.zip', package['url']):
            raise ValueError('Untrusted DAB package')
        data = public(package['url'])
        if len(data) != package['bytes'] or sha(data) != package['sha256']:
            raise ValueError('DAB archive integrity failure')
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            names = archive.namelist()
            if len(names) != len(set(names)) or set(names) != set(package['files']):
                raise ValueError('DAB package members mismatch')
            for name in names:
                orbital = position(name)
                image = archive.read(name)
                if sha(image) != package['files'][name] or image[:8] != b'\x89PNG\r\n\x1a\n' or struct.unpack('>II', image[16:24]) != (220, 132):
                    raise ValueError('DAB image integrity failure')
                result.setdefault((orbital, style), {})[name] = image
    return result, sha(raw)

def append_archive(original, additions):
    """Preserve all original bytes before the central directory and every file."""
    with zipfile.ZipFile(io.BytesIO(original)) as archive:
        members = archive.infolist()
        if len({i.filename for i in members}) != len(members):
            raise ValueError('Duplicate original archive member')
        for item in members:
            if PurePosixPath(item.filename).is_absolute() or '..' in PurePosixPath(item.filename).parts or '\\' in item.filename:
                raise ValueError('Unsafe original archive member')
        before = {i.filename: sha(archive.read(i)) for i in members if not i.is_dir()}
        central_offset = archive.start_dir
        for name, image in additions.items():
            position(name)
            if name in before and before[name] != sha(image):
                raise ValueError('Existing DAB artwork differs: ' + name)
    missing = {name: image for name, image in additions.items() if name not in before}
    if not missing:
        return original, 0, len(before)
    output = io.BytesIO(original)
    with zipfile.ZipFile(output, 'a', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, image in sorted(missing.items()):
            item = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            item.external_attr = 0o100644 << 16
            item.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(item, image)
    data = output.getvalue()
    if data[:central_offset] != original[:central_offset]:
        raise ValueError('Original compressed payload changed')
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        if len(archive.namelist()) != len(set(archive.namelist())):
            raise ValueError('Duplicate output member')
        for name, digest in before.items():
            if sha(archive.read(name)) != digest:
                raise ValueError('Original picon changed: ' + name)
        for name, image in additions.items():
            if archive.read(name) != image:
                raise ValueError('DAB picon differs: ' + name)
    return data, len(missing), len(before)

def run(publish=False):
    token = os.environ.get('GITHUB_TOKEN') if publish else None
    if publish and not token:
        raise ValueError('Publication requires the repository workflow token')
    github = GitHub(token)
    head = github.api('GET', '/git/ref/heads/main')['object']['sha']
    if not HEX.fullmatch(head):
        raise ValueError('Invalid source revision')
    manifest_raw = public('https://raw.githubusercontent.com/' + REPO + '/' + head + '/' + DIRECTORY + 'manifest.json')
    document = json.loads(manifest_raw)
    metadata = {p['filename']: p for p in document['parts']}
    artwork, source_hash = approved_artwork()
    packages = [p for p in document['packages'] if p['selector_id'] in ('192E', '235E') and p['resolution'] == '220x132']
    if len(packages) != 6:
        raise ValueError('Expected six satellite/style packages')
    entries, report, replacement_parts = [], [], []
    replaced_part_names = set()
    for package in packages:
        selector = package['selector_id']
        style = package['family'].removeprefix('channel-')
        additions = artwork[(int(selector[:-1]), style)]
        old_parts = []
        for url in package['parts']:
            if not url.startswith(LIVE_ROOT) or '/' in url[len(LIVE_ROOT):]:
                raise ValueError('Untrusted native part URL')
        def download(url):
            name = url.rsplit('/', 1)[1]
            raw = public('https://raw.githubusercontent.com/' + REPO + '/' + head + '/' + DIRECTORY + name)
            if len(raw) != metadata[name]['bytes'] or sha(raw) != metadata[name]['sha256']:
                raise ValueError('Native part integrity failure')
            return raw
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            old_parts = list(pool.map(download, package['parts']))
        original = b''.join(old_parts)
        if len(original) != package['bytes'] or sha(original) != package['sha256']:
            raise ValueError('Native archive integrity failure')
        data, added, preserved = append_archive(original, additions)
        if not added:
            report.append({'selector': selector, 'style': style, 'added': 0, 'preserved': preserved})
            continue
        digest = sha(data)
        filename = 'warder-' + selector.lower() + '-220x132-' + style + '-' + digest[:16] + '.zip'
        part_size = len(old_parts[0])
        urls = []
        for index, offset in enumerate(range(0, len(data), part_size)):
            raw = data[offset:offset + part_size]
            name = filename + '.part%02d' % index
            replacement_parts.append({'filename': name, 'bytes': len(raw), 'sha256': sha(raw)})
            unchanged = index < len(old_parts) and raw == old_parts[index]
            blob = git_sha(raw) if unchanged or not publish else github.blob(raw)
            entries.append({'path': DIRECTORY + name, 'mode': '100644', 'type': 'blob', 'sha': blob})
            urls.append(LIVE_ROOT + name)
        replaced_part_names.update(url.rsplit('/', 1)[1] for url in package['parts'])
        previous_hash = package['sha256']
        package.update(filename=filename, bytes=len(data), sha256=digest, parts=urls, png_count=package['png_count'] + added,
                       approved_dab_radio={'source_commit': PICON_REF, 'catalog_sha256': source_hash, 'added': added, 'preserved': preserved})
        report.append({'selector': selector, 'style': style, 'added': added, 'preserved': preserved, 'before_sha256': previous_hash, 'sha256': digest, 'bytes': len(data)})
    print(json.dumps(report, indent=2), flush=True)
    if not entries:
        print('All approved DAB picons are already present; no publication needed.')
        return
    document['parts'] = sorted([p for p in document['parts'] if p['filename'] not in replaced_part_names] + replacement_parts, key=lambda p: p['filename'])
    document['approved_dab_radio_source'] = {'repository': PICON_REPO, 'ref': PICON_REF, 'catalog_sha256': source_hash, 'packages': report,
        'owner_direction': 'DAB radio services belong to their owning satellite packages; explicit instruction 27 October 2026.'}
    evidence = {'schema': 1, 'base_skin_commit': head, 'base_manifest_sha256': sha(manifest_raw), 'dab_commit': PICON_REF, 'packages': report}
    texts = {DIRECTORY + 'manifest.json': json.dumps(document, ensure_ascii=False, indent=2) + '\n',
             DIRECTORY + 'SHA256SUMS': ''.join(p['sha256'] + '  ' + p['filename'] + '\n' for p in sorted(document['packages'], key=lambda p: p['filename'])),
             'assets/warder/dab-satellite-integration.json': json.dumps(evidence, indent=2) + '\n'}
    if not publish:
        Path('/tmp/dab-satellite-publication-report.json').write_text(json.dumps(evidence, indent=2) + '\n')
        print('Validated dry run; repository unchanged.')
        return
    for path, text in texts.items():
        entries.append({'path': path, 'mode': '100644', 'type': 'blob', 'sha': github.blob(text.encode())})
    source = github.api('GET', '/git/commits/' + head)
    tree = github.api('POST', '/git/trees', {'base_tree': source['tree']['sha'], 'tree': entries})
    commit = github.api('POST', '/git/commits', {'message': 'Include approved DAB radio picons in full 19.2E and 23.5E packages', 'parents': [head], 'tree': tree['sha']})
    if github.api('GET', '/git/ref/heads/main')['object']['sha'] != head:
        raise ValueError('Main advanced; rerun against the new manifest instead of overwriting it')
    github.api('PATCH', '/git/refs/heads/main', {'sha': commit['sha'], 'force': False})
    print('Published satellite DAB catalog:', commit['sha'], flush=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publish', action='store_true')
    run(parser.parse_args().publish)
