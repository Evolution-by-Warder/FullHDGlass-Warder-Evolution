#!/usr/bin/env python3
"""Check the actual installed PNG format, rollback ownership and feed isolation."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'packages/test/enigma2-plugin-skins-fullhdglass_1.0.46-test1_all.ipk'
RECORD = json.loads((ROOT / 'design/spinner-repair/candidate.json').read_text())


def main():
    with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['ar', 'p', str(PACKAGE), 'data.tar.gz'])), mode='r:gz') as archive:
        files = {m.name.removeprefix('./'): m for m in archive if m.isfile()}
        root = 'usr/share/enigma2/hd_glass17/spinner/'
        marker = json.loads(archive.extractfile(files[root + '.warder-spinner-candidate.json']).read())
        assert [x['name'] for x in marker['frames']] == ['wait%d.png' % i for i in range(1, 19)]
        for entry, candidate in zip(marker['frames'], RECORD['frames']):
            raw = archive.extractfile(files[root + entry['name']]).read()
            assert hashlib.sha256(raw).hexdigest() == entry['sha256']
            assert raw[25] == 6
            with Image.open(io.BytesIO(raw)) as frame:
                assert frame.mode == 'RGBA' and frame.size == (128, 88)
                assert len(frame.tobytes()) == 45056 < 48000
                assert hashlib.sha256(frame.tobytes()).hexdigest() == candidate['rgba_sha256']
        assert not any(p.startswith(('etc/enigma2/spinner/', 'usr/share/enigma2/skin_default/spinner/')) for p in files)
        helper = 'usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderSpinnerCandidate.py'
        assert archive.extractfile(files[helper]).read() == (ROOT / 'tools/spinner-candidate-control.py').read_bytes()
    control_bytes = subprocess.check_output(['ar', 'p', str(PACKAGE), 'control.tar.gz'])
    with tarfile.open(fileobj=io.BytesIO(control_bytes), mode='r:gz') as archive:
        control = archive.extractfile('./control').read().decode()
        assert 'Package: enigma2-plugin-skins-fullhdglass-warder-evolution\n' in control
        assert 'Version: 1.0.46-test1-1\n' in control
        for name in ('preinst', 'postinst', 'prerm', 'postrm'):
            assert archive.extractfile('./' + name).read() == (ROOT / 'source/control' / name).read_bytes()
    assert json.loads((ROOT / 'update-production.json').read_text())['version'] == '1.0.45'
    assert json.loads((ROOT / 'update-test.json').read_text())['version'] == '1.0.45'
    assert PACKAGE.stat().st_size < 16 * 1024 * 1024
    raw = PACKAGE.read_bytes()
    proof = {'scope': 'Actual candidate IPK', 'version': '1.0.46-test1',
             'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
             'png_frames_verified': 18, 'png_color_type': 6, 'surface_bytes': 45056,
             'native_image_spinner_replaced': False, 'production_feed_changed': False,
             'physical_receiver_validated': False}
    (ROOT / 'packages/test/spinner-candidate-verification.json').write_text(json.dumps(proof, indent=2) + '\n')
    print('PASS: actual IPK has 18 below-threshold RGBA frames, owned rollback, unchanged system hooks and production feeds')


if __name__ == '__main__':
    main()
