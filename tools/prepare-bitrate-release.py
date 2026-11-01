#!/usr/bin/env python3
"""Stage the bitrate repair while preserving public feeds and approved artwork."""
import hashlib
from pathlib import Path
import subprocess
import sys
from sync_header_version import sync_headers
ROOT=Path(__file__).resolve().parents[1]
PLUGIN=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
VERSION='1.0.54-test4'
def main():
    before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('update*.json')}
    if (PLUGIN/'version').read_text().strip()!=VERSION:
        subprocess.run([sys.executable,str(ROOT/'tools/prepare-dab-cover-release.py')],check=True)
        path=ROOT/'source/control/control'; text=path.read_text()
        assert 'Version: 1.0.53-1\n' in text
        path.write_text(text.replace('Version: 1.0.53-1\n','Version: '+VERSION+'-1\n',1))
        (PLUGIN/'version').write_text(VERSION+'\n')
        for name,note in {
            'history.txtSk':'Rýchlejší nábeh merania bitrate bez úvodných núl.\nSamostatné programy pre ARM, MIPS32r2 a AArch64; odstránený starý ARM program.',
            'history.txt':'Faster bitrate startup with immediate TS video measurement.\nARM, guarded MIPS32r2 and AArch64 helpers; obsolete ARM helper removed.',
        }.items():
            path=PLUGIN/name
            path.write_text('FullHDGlass '+VERSION+' — 01.11.2026\n'+note+'\n\n'+path.read_text())
    sync_headers(ROOT/'source/package-root')
    assert before=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('update*.json')}
    print('Prepared '+VERSION+'; published feeds unchanged')
if __name__=='__main__':main()
