#!/usr/bin/env python3
"""Publish an identical standalone IPK at the legacy URL for old radio updaters."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.request import Request, urlopen

SOURCE_REPO = 'Evolution-by-Warder/Radio-Warder-Evolution'
LEGACY_REPO = 'Evolution-by-Warder/FullHDGlass-Warder-Evolution'
VERSION = '0.1.0-test8'
PACKAGE = 'enigma2-plugin-extensions-warderradio'
TAG = 'warder-radio-v' + VERSION
SOURCE_FEED = 'https://raw.githubusercontent.com/' + SOURCE_REPO + '/main/update/testing.json'

sys.path.insert(0, str(Path('projects/warder-radio/src').resolve()))
from WarderRadio.warder_update import Release, download_release, validate_ipk

with urlopen(Request(SOURCE_FEED, headers={'User-Agent': 'WarderRadio-migration', 'Cache-Control': 'no-cache'}), timeout=20) as response:
    data = response.read(65537)
assert len(data) <= 65536
feed = json.loads(data)
assert feed['schema'] == 1 and feed['product'] == 'Warder Radio' and feed['channel'] == 'testing'
item = feed['release']
assert item['version'] == VERSION and item['tag'] == TAG
filename = PACKAGE + '_' + VERSION + '_all.ipk'
expected_url = 'https://github.com/' + SOURCE_REPO + '/releases/download/' + TAG + '/' + filename
assert item['url'] == expected_url
assert re.fullmatch('[a-f0-9]{64}', item['sha256'])
assert type(item['bytes']) is int and 0 < item['bytes'] < 32 * 1024 * 1024
release = Release(VERSION, expected_url, item['sha256'], item['bytes'])
legacy_url = 'https://github.com/' + LEGACY_REPO + '/releases/download/' + TAG + '/' + filename
with tempfile.TemporaryDirectory(prefix='warder-radio-migration-') as temporary:
    root = Path(temporary)
    package = download_release(release, root / filename)
    validate_ipk(package, release)
    notes = root / 'notes.md'
    notes.write_text('Warder Radio standalone repository migration.\n\n'
        'This is the identical verified IPK published at:\n' + expected_url + '\n\n'
        'Source and future updates: https://github.com/' + SOURCE_REPO + '\n\n'
        'Existing radio data is preserved. Install and restart the GUI to use the new updater.\n')
    sums = root / 'SHA256SUMS'; sums.write_text(item['sha256'] + '  ' + filename + '\n')
    present = subprocess.run(['gh', 'release', 'view', TAG], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if present.returncode != 0:
        subprocess.run(['gh', 'release', 'create', TAG, '--target', os.environ['GITHUB_SHA'],
                        '--prerelease', '--title', 'Warder Radio ' + VERSION + ' - repository migration',
                        '--notes-file', str(notes)], check=True)
    subprocess.run(['gh', 'release', 'upload', TAG, str(package), str(sums), '--clobber'], check=True)
    legacy_release = release._replace(url=legacy_url)
    mirrored = download_release(legacy_release, root / 'legacy-check.ipk')
    validate_ipk(mirrored, legacy_release)
    feed['release'] = dict(item, url=legacy_url)
    target = Path('projects/warder-radio/update/testing.json')
    target.write_text(json.dumps(feed, indent=2) + '\n')
    print('Both public IPKs have identical verified bytes; legacy migration feed prepared:', VERSION, item['sha256'])
