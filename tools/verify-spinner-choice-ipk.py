#!/usr/bin/env python3
"""Verify real packaged catalog hashes and switch the extracted native frames."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/version').read_text().strip()
PACKAGE = ROOT / ('packages/test/enigma2-plugin-skins-fullhdglass_' + VERSION + '_all.ipk')
PREFIX = 'usr/share/enigma2/hd_glass17/'
PLUGIN = 'usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/'


def main():
    expected_feeds = json.loads((ROOT / 'packages/test/spinner-choice-feed-isolation.json').read_text())
    assert expected_feeds == {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('update*.json')}
    with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['ar', 'p', str(PACKAGE), 'control.tar.gz'])), mode='r:gz') as archive:
        control_files = {m.name.removeprefix('./'): m for m in archive if m.isfile()}
        metadata = archive.extractfile(control_files['control']).read().decode()
        assert ('Version: ' + VERSION + '-1\n') in metadata
        preinst = archive.extractfile(control_files['preinst']).read()
        assert preinst == (ROOT / 'source/control/preinst').read_bytes()
        assert b'warder_prepare_legacy_obsolete_files' in preinst
    with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['ar', 'p', str(PACKAGE), 'data.tar.gz'])), mode='r:gz') as archive:
        files = {m.name.removeprefix('./'): m for m in archive if m.isfile()}
        assert PREFIX + 'skin.xml' in files
        assert archive.extractfile(files[PLUGIN + 'version']).read().decode().strip() == VERSION
        assert not any(name.startswith(('etc/enigma2/spinner/', 'usr/share/enigma2/skin_default/spinner/')) for name in files)
        data = json.loads(archive.extractfile(files[PLUGIN + 'warder-spinners.json']).read())
        assert PLUGIN + 'warderSpinnerOnline.py' in files
        assert PLUGIN + 'warderSpinnerScreen.py' in files
        assert PLUGIN + 'warderInstallHealth.py' in files
        assert not any('/preview-library/' in name or '/spinners/online/archives/' in name for name in files)
        for theme_id, theme in data['themes'].items():
            for entry in theme['frames']:
                name = PREFIX + 'spinner-themes/' + theme_id + '/' + entry['name']
                assert hashlib.sha256(archive.extractfile(files[name]).read()).hexdigest() == entry['sha256'], name
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skin = root / 'hd_glass17'
            for name, member in files.items():
                if name.startswith((PREFIX + 'spinner/', PREFIX + 'spinner-themes/')):
                    path = skin / name.removeprefix(PREFIX)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(archive.extractfile(member).read())
            helper = root / 'warderSpinner.py'
            helper.write_bytes(archive.extractfile(files[PLUGIN + 'warderSpinner.py']).read())
            catalog = root / 'warder-spinners.json'
            catalog.write_bytes(archive.extractfile(files[PLUGIN + 'warder-spinners.json']).read())
            spec = importlib.util.spec_from_file_location('packaged_spinner_choice', helper)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            assert module.apply('bakussa', skin, catalog)
            assert len(list((skin / 'spinner').iterdir())) == 20
            assert module.apply('dove', skin, catalog)
            assert len(list((skin / 'spinner').iterdir())) == 18
            assert not list(skin.glob('.warder-spinner-*'))
    raw = PACKAGE.read_bytes()
    from bitrate_package import validate_helpers
    assert 0 < len(raw) < validate_helpers(ROOT)
    report = {'schema': 1, 'version': VERSION, 'package': PACKAGE.name, 'bytes': len(raw),
              'sha256': hashlib.sha256(raw).hexdigest(), 'packaged_frame_hashes_verified': True,
              'packaged_helper_switches_both_directions': True, 'updater_manifests_unchanged': True,
              'system_spinner_replaced': False, 'receiver_test': False}
    (ROOT / 'packages/test/spinner-choice-verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print('PASS: actual packaged frames, catalog, native switching and updater isolation')


if __name__ == '__main__':
    main()
