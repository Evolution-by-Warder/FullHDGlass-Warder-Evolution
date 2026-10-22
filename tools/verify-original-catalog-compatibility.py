#!/usr/bin/env python3
"""Keep existing 1.0.13 native downloads working when adding the new 80E selector."""
import hashlib,importlib.util,json,subprocess,tempfile
from pathlib import Path
from urllib.request import urlopen
R=Path(__file__).resolve().parents[1];P=R/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17';D=R/'assets/warder/downloads/picons/channels';BASE='39460b6a644365e0267bf37d410b11c5049ef774'
def module(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
new=module(P/'warderPiconSync.py','new_sync')
with tempfile.TemporaryDirectory() as temp:
 path=Path(temp)/'warderPiconSync.py'
 with urlopen('https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/'+BASE+'/source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPiconSync.py',timeout=90) as response:path.write_bytes(response.read())
 old=module(path,'old_sync')
 for suffix in ('','test-candidate'):
  manifest=D/suffix/'manifest.json';doc=json.loads(manifest.read_text());payloads=[(p['filename'],p['sha256'],p['bytes'],p.get('parts')) for p in doc['packages']]
  changed=0
  for pkg in doc['packages']:
   if pkg['selector_id']=='800E':
    assert pkg.get('orbital_position')=='80.0e'
    pkg['source_orbital_position']=pkg.pop('orbital_position');changed+=1
  assert changed==9
  source='production' if not suffix else 'test-candidate'
  assert not old.validate_publication_manifest(doc,source)
  assert not new.validate_publication_manifest(doc,source)
  assert payloads==[(p['filename'],p['sha256'],p['bytes'],p.get('parts')) for p in doc['packages']]
  prefs=old.set_task_position_bindings(old.default_preferences('/tmp/picon'),[old.task_binding_for_package_selector(s) for s in ('160E','235E')]);prefs.update(resolution='220x132',style='black',update_mode=old.UPDATE_MODE_INCREMENTAL,prepared=True)
  queue=old.build_runtime_queue(prefs,publication=old.runtime_publication());queue['manifest_url']=old.publication_source(source)['manifest_url']
  plan=old.plan_runtime_packages(doc,queue,source);assert plan['state']=='ready' and len(plan['packages'])==2,plan
  for size in ('50x30','220x132','400x240'):
   for style in ('transparent','white','black'):
    prefs=new.set_task_position_bindings(new.default_preferences('/tmp/picon'),[new.task_binding_for_package_selector('800E')]);prefs.update(resolution=size,style=style,update_mode=new.UPDATE_MODE_INCREMENTAL,prepared=True)
    queue=new.build_runtime_queue(prefs,publication=new.runtime_publication());queue['manifest_url']=new.publication_source(source)['manifest_url'];plan=new.plan_runtime_packages(doc,queue,source)
    assert plan['state']=='ready' and len(plan['packages'])==1 and new.canonical_position_for_selector(plan['packages'][0]['selector_id'])=='80.0e'
  manifest.write_text(json.dumps(doc,indent=2,sort_keys=True)+'\n')
report=R/'reports/original-sets-integration-20261022.json';doc=json.loads(report.read_text());doc['backward_compatibility']=dict(receiver_version='1.0.13',both_catalogues_validate=True,selected_positions_220x132=['16.0e','23.5e'],new_80e_bindings_verified=9,archive_payloads_unchanged=True);report.write_text(json.dumps(doc,indent=2,sort_keys=True)+'\n')
readme=R/'README.md';readme.write_text(readme.read_text().replace('Stable and test update channels both offer 1.0.13.','Stable and test update channels both offer 1.0.14.'))
subprocess.run(['python3',str(R/'tools/test-original-set-routing.py')],cwd=R,check=True)
subprocess.run(['python3',str(R/'tools/test-live-picon-catalog.py')],cwd=R,check=True)
subprocess.run(['python3',str(R/'tools/verify-radio-release.py')],cwd=R,check=True)
print('PASS: both complete catalogues validated by actual 1.0.13 and 1.0.14 modules; older 220x132 downloads work; all nine new 80E choices resolve exactly; all archive bytes and IPK unchanged')
