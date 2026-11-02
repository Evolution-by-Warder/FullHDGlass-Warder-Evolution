#!/usr/bin/env python3
"""Stage an isolated OpenPLi test; preserve every production feed and helper."""
import importlib.util
from pathlib import Path
from sync_header_version import sync_headers

ROOT=Path(__file__).resolve().parents[1]
VERSION='1.0.62-test5'
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
        'history.txt':'OpenPLi: fixed settings confirmation and information dialogs, including optional timer cleanup.\nNative yes/no selection and cancellation are preserved.\n',
        'history.txtSk':'OpenPLi: opravené potvrdzovacie a informačné okná nastavení vrátane voliteľného časovača.\nZachované natívne potvrdenie výberu a zrušenie.\n'}
    heading='FullHDGlass '+VERSION+' — 02.11.2026\n'
    for name,body in notes.items():
        path=PLUGIN/name
        text=path.read_text()
        previous='FullHDGlass 1.0.62-test3 — 02.11.2026\n'
        if previous not in text:
            previous_notes=('OpenPLi: corrected native captions and complete virtual keyboard.\nNative Enigma2 file ownership is preserved.\n' if name=='history.txt' else 'OpenPLi: opravené natívne tlačidlá a kompletná klávesnica.\nSystémové súbory Enigma2 zostávajú zachované.\n')
            text=previous+previous_notes+'\n'+text
        previous4='FullHDGlass 1.0.62-test4 — 02.11.2026\n'
        if previous4 not in text:
            previous4_notes=('OpenPLi: restored installed plugin list, descriptions, icons and launch actions.\nCorrected row heights in plugin browsing, downloads and removal.\n' if name=='history.txt' else 'OpenPLi: obnovený zoznam pluginov, popisy, ikony a spúšťanie.\nOpravená výška riadkov pri prehliadaní, sťahovaní a odstraňovaní pluginov.\n')
            text=previous4+previous4_notes+'\n'+text
        if not text.startswith(heading):text=heading+body+'\n'+text
        path.write_text(text)
    sync_headers(ROOT/'source/package-root')
    spec=importlib.util.spec_from_file_location('approved_helpers',ROOT/'tools/prepare-bitrate-stable-release.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    module.VERSION=VERSION
    module.main()

if __name__=='__main__':main()
