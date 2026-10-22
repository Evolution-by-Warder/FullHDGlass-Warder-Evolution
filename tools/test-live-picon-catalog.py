#!/usr/bin/env python3
"""Exercise real receiver methods across catalogue-only updates, without a new IPK."""
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
from urllib.request import Request
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / 'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
spec = importlib.util.spec_from_file_location('sync', PKG / 'warderPiconSync.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)
PUBLICATION = sync.runtime_publication()
MANIFEST = 'https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/channels/manifest.json'
assert PUBLICATION['manifest_url'] == MANIFEST and PUBLICATION['publication_source_id'] == 'production'
NAME = '1_0_1_334C_C93_3_EB0000_0_0_0.png'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def png(level):
    def chunk(name, data):
        return struct.pack('>I', len(data)) + name + data + struct.pack('>I', zlib.crc32(name + data) & 0xffffffff)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 220, 132, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress((b'\x00' + bytes([level, 40, 80]) * 220) * 132)) + chunk(b'IEND', b''))


def publication(style, level):
    image = png(level)
    data = io.BytesIO()
    with zipfile.ZipFile(data, 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(NAME, image)
    data = data.getvalue()
    filename = 'canalplus_cz_' + style + '_' + sha(data)[:16] + '.zip'
    url = PUBLICATION['package_root'] + filename
    doc = dict(schema=1, generated_from=dict(repository='Evolution-by-Warder/PiconHub-Warder-Evolution', ref='f64caf688aae368c1b876d49f99e012fbc5cf0a1'),
               delivery='direct', packages=[dict(selector_id='CANALPLUS_CZ', family='channel-' + style, resolution='220x132',
               filename=filename, bytes=len(data), sha256=sha(data), url=url, png_count=1)])
    assert not sync.validate_publication_manifest(doc)
    return doc, url, data, image


class Response(io.BytesIO):
    def __init__(self, data, url):
        super().__init__(data)
        self.url = url
    def geturl(self):
        return self.url


class Server:
    def __init__(self):
        self.responses = {}
        self.requests = []
    def open(self, request, timeout):
        self.requests.append(request)
        return Response(self.responses[request.full_url], request.full_url)


server = Server()
names = {'_warderRunChannelQueue', '_warderLoadChannelManifest', '_warderFetchChannelJob',
         '_warderInstallChannelArchive', '_warderRemoveStaleChannelPicons'}
scope = dict(warderPiconSync=sync, os=os, shutil=shutil, tempfile=tempfile, zipfile=zipfile,
             stat=stat, hashlib=hashlib, json=json, Request=Request, urlopen=server.open, _=lambda s: s)
tree = ast.parse((PKG / 'plugin.py').read_bytes())
methods = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name in names]
assert len(methods) == len(names)
for method in methods:
    exec(compile(ast.Module(body=[method], type_ignores=[]), 'receiver', 'exec'), scope)
Receiver = type('Receiver', (), {name: scope[name] for name in names})


def run(receiver):
    for _ in range(4):
        result = receiver._warderRunChannelQueue()
        if result is not None:
            return result
    raise AssertionError('download queue did not complete')


def main():
    code_before = sha((PKG / 'warderPiconSync.py').read_bytes()), sha((PKG / 'plugin.py').read_bytes()), (PKG / 'version').read_bytes()
    for style in ('transparent', 'white', 'black'):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / 'picon'
            destination.mkdir()
            unrelated = destination / '1_0_1_1_1_1_C00000_0_0_0.png'
            unrelated.write_bytes(b'unrelated position')
            receiver = Receiver()
            prefs = sync.set_task_position_bindings(sync.default_preferences(str(destination)), [sync.task_binding_for_package_selector('CANALPLUS_CZ')])
            prefs.update(resolution='220x132', style=style, update_mode=sync.UPDATE_MODE_REPLACE_ALL, prepared=True)
            receiver.warderPiconPrefs = prefs
            receiver.warderChannelQueue = None
            for level in (100, 160):
                doc, url, archive, image = publication(style, level)
                server.responses.update({MANIFEST: json.dumps(doc).encode(), url: archive})
                before = sum(r.full_url == MANIFEST for r in server.requests)
                assert run(receiver).startswith('SUCCESSFUL')
                assert sum(r.full_url == MANIFEST for r in server.requests) == before + 1
                assert (destination / NAME).read_bytes() == image
                assert unrelated.read_bytes() == b'unrelated position'
            # A new catalogue cannot bypass archive checksum validation.
            doc, url, archive, image = publication(style, 200)
            server.responses.update({MANIFEST: json.dumps(doc).encode(), url: archive + b'corruption'})
            installed = (destination / NAME).read_bytes()
            result = run(receiver)
            assert not result.startswith('SUCCESSFUL') and 'oversized' in result, result
            assert (destination / NAME).read_bytes() == installed
            server.responses[url] = archive[:-1] + bytes([archive[-1] ^ 1])
            result = run(receiver)
            assert 'integrity mismatch' in result, result
            assert (destination / NAME).read_bytes() == installed
            # Reject an unapproved source before the first network request.
            before = len(server.requests)
            try:
                receiver._warderLoadChannelManifest('https://example.com/manifest.json')
            except ValueError:
                pass
            else:
                raise AssertionError('untrusted manifest accepted')
            assert len(server.requests) == before
            invalid = copy.deepcopy(doc)
            invalid['packages'][0]['url'] = 'https://example.com/evil.zip'
            server.responses[MANIFEST] = json.dumps(invalid).encode()
            try:
                receiver._warderLoadChannelManifest(MANIFEST)
            except ValueError:
                pass
            else:
                raise AssertionError('untrusted archive accepted')
            assert (destination / NAME).read_bytes() == installed
    requests = [r for r in server.requests if r.full_url == MANIFEST]
    assert all(r.get_header('Cache-control') == 'no-cache' and r.get_header('Pragma') == 'no-cache' for r in requests)
    assert code_before == (sha((PKG / 'warderPiconSync.py').read_bytes()), sha((PKG / 'plugin.py').read_bytes()), (PKG / 'version').read_bytes())
    print('PASS: three styles update twice in the same receiver instance without a code/version change; fresh catalogue per operation; corrupt archives and untrusted URLs rejected without overwriting installed picons')


if __name__ == '__main__':
    main()
