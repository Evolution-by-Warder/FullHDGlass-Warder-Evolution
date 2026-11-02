#!/usr/bin/env python3
"""Stage an isolated OpenPLi test; preserve every production feed and helper."""
import importlib.util
from pathlib import Path
from sync_header_version import sync_headers

ROOT=Path(__file__).resolve().parents[1]
VERSION='1.0.62-test3'
PLUGIN=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'

def main():
    current=(PLUGIN/'version').read_text().strip()
    if current not in ('1.0.62-test2',VERSION):raise ValueError('Unexpected candidate base version')
    (PLUGIN/'version').write_text(VERSION+'\n')
    path=ROOT/'source/control/control';text=path.read_text()
    old='Version: '+current+'-1\n'
    if text.count(old)!=1:raise ValueError('Unexpected control version')
    path.write_text(text.replace(old,'Version: '+VERSION+'-1\n',1))
    notes={
        'history.txt':'OpenPLi: corrected native colour-caption bindings and complete virtual keyboard.\nLegacy replacements of image-owned Enigma2 files are disabled on OpenPLi.\n',
        'history.txtSk':'OpenPLi: opravené väzby farebných tlačidiel a kompletná virtuálna klávesnica.\nZablokované staré prepisovanie systémových súborov Enigma2 na OpenPLi.\n'}
    heading='FullHDGlass '+VERSION+' — 02.11.2026\n'
    for name,body in notes.items():
        path=PLUGIN/name
        if not path.read_text().startswith(heading):path.write_text(heading+body+'\n'+path.read_text())
    sync_headers(ROOT/'source/package-root')
    spec=importlib.util.spec_from_file_location('approved_helpers',ROOT/'tools/prepare-bitrate-stable-release.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    module.VERSION=VERSION
    module.main()

if __name__=='__main__':main()
