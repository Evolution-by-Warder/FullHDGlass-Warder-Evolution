"""Exercise the released receiver engine against the three live terrestrial packages."""
import hashlib,importlib,io,json,os,pathlib,sys,tempfile,types
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen
R=pathlib.Path('assets/warder/downloads/picons/dvb-t-skcz');doc=json.loads(pathlib.Path('assets/warder/downloads/picons/channels/manifest.json').read_text());records=json.loads((R/'catalog/variants.json').read_text())['records'];removed=json.loads((R/'catalog/removals.json').read_text());assert len(records)==2531 and not set(removed)&set(records)
root=pathlib.Path('.picon-runtime/plugin/src/Plugins/Extensions/WarderPiconHub').resolve();pkg=types.ModuleType('dtt_verify');pkg.__path__=[str(root)];sys.modules[pkg.__name__]=pkg;e=importlib.import_module(pkg.__name__+'.warder_engine');s=e.sync
assert s.validate_publication_manifest(doc)==[],s.validate_publication_manifest(doc)
packages=[p for p in doc['packages'] if p.get('selector_id')=='DVB-T-SK-CZ'];assert len(packages)==3 and all(p['png_count']==2531 for p in packages);partmeta={p['filename']:p for p in doc['parts']};urls=[u for p in packages for u in p['parts']]
def read(url):
 entry=partmeta[url.rsplit('/',1)[1]]
 with urlopen(url,timeout=60) as response:raw=response.read(entry['bytes']+1)
 assert len(raw)==entry['bytes'] and hashlib.sha256(raw).hexdigest()==entry['sha256'];return url,raw
with ThreadPoolExecutor(max_workers=8) as pool:downloads=dict(pool.map(read,urls))
def opener(url):return io.BytesIO(json.dumps(doc).encode()) if url==s.RUNTIME_MANIFEST_URL else io.BytesIO(downloads[url])
results={}
for style in ('transparent','white','black'):
 with tempfile.TemporaryDirectory() as temp:
  target=pathlib.Path(temp)/'picon';target.mkdir();(target/'user.png').write_bytes(b'user file preserved')
  prefs=s.default_preferences(str(target));prefs=s.set_task_position_bindings(prefs,[s.task_binding_for_package_selector('DVB-T-SK-CZ')]);prefs.update(resolution='220x132',style=style,update_mode=s.UPDATE_MODE_INCREMENTAL,prepared=True)
  result=e.PiconRunner(opener=opener,lock_path=temp+'/lock',enigma2_dir=temp+'/enigma2').run([prefs]);assert result=={'added':2531,'changed':0,'removed':0},result
  assert (target/'user.png').read_bytes()==b'user file preserved'
  assert not any((target/n).exists() for n in removed)
  for n,r in records.items():assert hashlib.sha256((target/n).read_bytes()).hexdigest()==r[style]
  results[style]=dict(result,all_file_sha256_verified=True,user_file_preserved=True,retired_files_absent=True)
print(json.dumps(dict(public_parts_verified=len(downloads),native_engine_installation=results),indent=2))
