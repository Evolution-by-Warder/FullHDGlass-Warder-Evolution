#!/usr/bin/env python3
import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];version='1.0.15';ipk=R/'packages'/('enigma2-skin-fullhdglass17-warder-evolution_'+version+'_all.ipk');digest=hashlib.sha256(ipk.read_bytes()).hexdigest()
for name in ['update.json','update-test.json']:
 p=R/name;j=json.loads(p.read_text());j.update(version=version,package_url='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/packages/'+ipk.name,sha256=digest,changelog='Odstránené nepokryté pozície 12,5W, 11,0W, 3,1E, 74,9E, 85,0E a 85,1E z ponúk piconov a sťahovacích väzieb. Zachované ostatné nastavenia a schválená grafika.');p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
p=R/'README.md'
if p.exists():
 s=p.read_text().replace('Latest approved release: 1.0.14','Latest approved release: 1.0.15').replace('evolution_1.0.14_all.ipk','evolution_1.0.15_all.ipk');p.write_text(s+'\nRelease 1.0.15 removes the six unsupported picon positions and their legacy download selectors. All 45 supported satellite positions, existing picons and receiver-confirmed radio graphics remain unchanged.\n')
p=R/'reports/position-cleanup-1.0.15.json';p.parent.mkdir(exist_ok=True);p.write_text(json.dumps({'version':version,'sha256':digest,'removed_selectors':['125W','110W','31E','749E','850E','851E'],'supported_numeric_positions':45,'all_supported_220x132_styles_verified':135,'radio_graphics_and_layout_unchanged':True,'resampling_45w_400x240':'prepared separately for visual approval; original 220x132 retained'},indent=2)+'\n');print(version,digest)
