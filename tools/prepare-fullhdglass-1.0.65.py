#!/usr/bin/env python3
"""Promote the approved test2 code, preserving feeds until public verification."""
import hashlib,importlib.util,json,runpy,sys
from pathlib import Path
from urllib.request import urlopen
from sync_header_version import sync_headers
ROOT=Path(__file__).resolve().parents[1]
C=json.loads((ROOT/'docs/FULLHDGLASS-1.0.65-STABLE.json').read_text())
def main():
 before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('update*.json')}
 out=ROOT/'reports/fullhdglass-1.0.65';out.mkdir(parents=True,exist_ok=True)
 with urlopen(C['candidate_url'],timeout=60) as r:raw=r.read(25000000)
 assert hashlib.sha256(raw).hexdigest()==C['candidate_sha']
 (out/'candidate.ipk').write_bytes(raw)
 runpy.run_path(str(ROOT/'tools/materialize-atv-epg-assets.py'),run_name='__main__')
 p=ROOT/C['runtime'];current=(p/'version').read_text().strip();assert current=='1.0.63'
 (p/'version').write_text(C['version']+'\n')
 control=ROOT/'source/control/control';s=control.read_text();old='Version: '+current+'-1\n';assert s.count(old)==1;control.write_text(s.replace(old,'Version: '+C['version']+'-1\n',1))
 for name,lang in [('history.txt','en'),('history.txtSk','sk')]:
  path=p/name;path.write_text('FullHDGlass '+C['version']+' — 03.11.2026\n'+C['notes_i18n'][lang]+'\n\n'+path.read_text())
 sync_headers(ROOT/'source/package-root')
 spec=importlib.util.spec_from_file_location('stable_helpers',ROOT/'tools/prepare-bitrate-stable-release.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.VERSION=C['version'];m.main()
 assert before=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('update*.json')}
 print('Prepared FullHDGlass '+C['version']+'; feeds remain unchanged until verification')
if __name__=='__main__':main()
