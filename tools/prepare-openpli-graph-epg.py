#!/usr/bin/env python3
"""Stage the isolated OpenPLi guide test, keeping all production channels frozen."""
import hashlib,importlib.util,json,sys
from pathlib import Path
from sync_header_version import sync_headers
ROOT=Path(__file__).resolve().parents[1]
VERSION='1.0.64-test2'
P=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
def main():
 import runpy
 runpy.run_path(str(ROOT/"tools/materialize-atv-epg-assets.py"),run_name="__main__")
 before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('update*.json')}
 current=(P/'version').read_text().strip();assert current in ('1.0.63',VERSION)
 (P/'version').write_text(VERSION+'\n')
 path=ROOT/'source/control/control';text=path.read_text();old='Version: '+current+'-1\n';assert text.count(old)==1;path.write_text(text.replace(old,'Version: '+VERSION+'-1\n',1))
 for filename,notes in [('history.txt','OpenPLi: FullHDGlass graphical Multi EPG with the shared programme detail on red.\nCopied OpenATV cell/timeline painters and pinned original textures; corrected window decoration, 180-minute span and 60-pixel picon column. Native timer and zap handling retained.'),('history.txtSk','OpenPLi: grafické Multi EPG FullHDGlass so spoločným detailom programu pod červeným.\nPrevzaté vykresľovanie buniek a časovej osi OpenATV s pôvodnými podkladmi; opravené okno, rozsah 180 minút a stĺpec piconov 60 px. Zachované natívne časovače a prepínanie.')]:
  path=P/filename;text=path.read_text();heading='FullHDGlass '+VERSION+' — 02.11.2026\n'
  if not text.startswith(heading):path.write_text(heading+notes+'\n\n'+text)
 sync_headers(ROOT/'source/package-root')
 spec=importlib.util.spec_from_file_location('approved_helpers',ROOT/'tools/prepare-bitrate-stable-release.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);module.VERSION=VERSION;module.main()
 assert before=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('update*.json')}
 print('Prepared '+VERSION+'; all update feeds unchanged')
if __name__=='__main__':main()
