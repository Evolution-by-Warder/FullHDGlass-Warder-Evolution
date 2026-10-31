#!/usr/bin/env python3
"""Stage an isolated spinner-choice IPK; never change updater manifests."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
VERSION = '1.0.50-test1'


def main():
    before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('update*.json')}
    version = PLUGIN / 'version'
    old = version.read_text().strip()
    if old not in ('1.0.49', VERSION):
        raise ValueError('Unexpected spinner candidate base')
    control = ROOT / 'source/control/control'
    text = control.read_text()
    if 'Version: ' + old + '-1\n' not in text:
        raise ValueError('Control version mismatch')
    if old != VERSION:
        control.write_text(text.replace('Version: ' + old + '-1\n', 'Version: ' + VERSION + '-1\n', 1))
        version.write_text(VERSION + '\n')
        for name, body in {
            'history.txtSk': 'Výber animácie čakania: Holubica alebo HDGlass - bakussa.\nUložený výber zostáva zachovaný po aktualizácii.',
            'history.txt': 'Waiting animation selection: Dove or HDGlass - bakussa.\nThe saved choice is preserved after updates.',
        }.items():
            path = PLUGIN / name
            path.write_text('FullHDGlass ' + VERSION + ' — 31.10.2026\n' + body + '\n\n' + path.read_text())
    assert before == {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('update*.json')}
    out = ROOT / 'packages/test'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'spinner-choice-feed-isolation.json').write_text(json.dumps(before, indent=2) + '\n')
    print('Prepared ' + VERSION + '; production, test and legacy updater manifests unchanged')


if __name__ == '__main__':
    main()
