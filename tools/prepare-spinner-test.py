#!/usr/bin/env python3
"""Prepare an isolated receiver candidate in a disposable build checkout.

Production source/feeds are unchanged in git. Add only the skin's own native
spinner folder, a manual ownership-checked rollback helper, and test identity.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / 'design/spinner-repair'
PAYLOAD = ROOT / 'source/package-root'
PLUGIN = PAYLOAD / 'usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
VERSION = '1.0.46-test1'


def main():
    if (PLUGIN / 'version').read_text().strip() != '1.0.45':
        raise ValueError('Candidate must be prepared from the reviewed production version')
    spinner = PAYLOAD / 'usr/share/enigma2/hd_glass17/spinner'
    if spinner.exists() or spinner.is_symlink():
        raise ValueError('Existing spinner must not be overwritten')
    record = json.loads((DESIGN / 'candidate.json').read_text())
    spec = importlib.util.spec_from_file_location('png_optimizer', ROOT / 'tools/optimize-png.py')
    optimizer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(optimizer)
    packed = []
    for entry in record['frames']:
        raw = (DESIGN / 'frames' / entry['name']).read_bytes()
        if hashlib.sha256(raw).hexdigest() != entry['sha256']:
            raise ValueError('Reviewed candidate frame changed')
        encoded = optimizer.optimize(raw)
        if encoded[25] != 6:
            raise ValueError('Truecolor RGBA must not be converted back to a palette')
        packed.append((entry['name'], encoded))
    spinner.mkdir(parents=True)
    inventory = []
    for name, raw in packed:
        (spinner / name).write_bytes(raw)
        inventory.append({'name': name, 'sha256': hashlib.sha256(raw).hexdigest()})
    marker = {'schema': 1, 'product': 'FullHDGlass-spinner-candidate', 'version': VERSION,
              'frames': inventory, 'native_image_spinner_replaced': False}
    (spinner / '.warder-spinner-candidate.json').write_text(json.dumps(marker, indent=2) + '\n')
    shutil.copyfile(ROOT / 'tools/spinner-candidate-control.py', PLUGIN / 'warderSpinnerCandidate.py')
    control = ROOT / 'source/control/control'
    control.write_text(control.read_text().replace('Version: 1.0.45-1\n', 'Version: ' + VERSION + '-1\n', 1))
    plugin = PLUGIN / 'plugin.py'
    plugin.write_text(plugin.read_text().replace('text="1.0.45"', 'text="' + VERSION + '"'))
    (PLUGIN / 'version').write_text(VERSION + '\n')
    for name in ('history.txt', 'history.txtSk'):
        path = PLUGIN / name
        path.write_text('FullHDGlass ' + VERSION + ' — spinner test\n'
                        '18 original dove frames transcoded to RGBA 128x88; below the stock hardware-surface threshold. Native per-skin loading, no system spinner symlinks. Receiver confirmation pending.\n\n' + path.read_text())
    print('Prepared isolated %s; production updater files and system spinner paths untouched' % VERSION)


if __name__ == '__main__':
    main()
