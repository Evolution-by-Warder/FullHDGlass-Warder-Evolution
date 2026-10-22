#!/usr/bin/env python3
"""Exercise actual SATLIST and runtime bindings after retiring missing positions."""
import ast,importlib.util,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
RETIRED={'125W','110W','31E','749E','850E','851E'};PREFIX={'(12.5W)','(11.0W)','(3.1E)','(74.9E)','(85.0E)','(85.1E)'}
s=importlib.util.spec_from_file_location('sync',P/'warderPiconSync.py');sync=importlib.util.module_from_spec(s);s.loader.exec_module(sync)
node=next(n for n in ast.parse((P/'txt.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SATLIST' for t in n.targets))
for legacy in [False,True]:
 scope={'L':legacy};exec(compile(ast.Module(body=[node],type_ignores=[]),'actual-SATLIST','exec'),scope);rows=scope['SATLIST']
 assert not any(row[0].split(' ',1)[0] in PREFIX for row in rows)
 assert all(sync.task_binding_for_display_label(row[0]) for row in rows)
 assert any(row[0].startswith('(75.0E)') for row in rows)
 assert any(row[0].startswith('(45.0W)') for row in rows)
for sid in RETIRED:assert sync.task_binding_for_package_selector(sid) is None
numeric={k:v for k,v in sync._SELECTOR_ID_TO_POSITION.items() if re.fullmatch(r'\d+[EW]',k)};assert len(numeric)==45,numeric
for sid in ['750E','800E','160E','235E','450W','CANALPLUS_SK','CANALPLUS_CZ']:assert sync.task_binding_for_package_selector(sid)
manifest_path=ROOT/'assets/warder/downloads/picons/channels/manifest.json'
if manifest_path.exists():
 doc=json.loads(manifest_path.read_text());assert not {p['selector_id'] for p in doc['packages']}&RETIRED
 assert not sync.validate_publication_manifest(doc,sync.runtime_publication()['manifest_url'])
 for sid in numeric:
  for style in ['transparent','white','black']:
   prefs=sync.set_task_position_bindings(sync.default_preferences(),[sync.task_binding_for_package_selector(sid)]);prefs.update(resolution='220x132',style=style,update_mode=sync.UPDATE_MODE_INCREMENTAL)
   q=sync.build_runtime_queue(prefs,publication=sync.runtime_publication());plan=sync.plan_runtime_packages(doc,q);assert plan['state']=='ready',(sid,style,plan)
   assert sync.build_download_jobs(doc,plan)['state']=='ready'
print('PASS: six retired positions absent from both menus/bindings/links; 45 supported positions and 135 real receiver download plans retained')
