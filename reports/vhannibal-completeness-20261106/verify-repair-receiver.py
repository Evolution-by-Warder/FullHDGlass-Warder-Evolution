from pathlib import Path
import json,ast,hashlib,zipfile,io,stat,shutil,tempfile,os,importlib.util
B=Path('audit-output/approved-repairs');doc=json.load(open(B/'manifest.json'));spec=importlib.util.spec_from_file_location('sync',Path('audit-cache/warderPiconSync.py'));sync=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync)
assert sync.validate_publication_manifest(doc)==[]
tree=ast.parse(Path('audit-cache/receiver-plugin.py').read_bytes());fn=next(n for n in ast.walk(tree)if isinstance(n,ast.FunctionDef)and n.name=='_warderInstallChannelArchive');scope=dict(warderPiconSync=sync,os=os,shutil=shutil,tempfile=tempfile,zipfile=zipfile,stat=stat);exec(compile(ast.Module(body=[fn],type_ignores=[]),'pinned-receiver-plugin','exec'),scope);install=scope[fn.name]
aliases={x['path'].rsplit('/',1)[-1]:x['original_filename']for x in json.load(open(B/'reused-git-blobs.json'))};meta={x['filename']:x for x in doc['parts']};proof=json.load(open(B/'approved-reuse-repairs.json'));checks=[]
for changed in proof['packages']:
 p=next(p for p in doc['packages']if p['sha256']==changed['sha256']);jobs=sync.build_download_jobs(doc,{'state':'ready','packages':[p]});assert jobs['state']=='ready'and len(jobs['jobs'])==1
 chunks=[]
 for part in jobs['jobs'][0]['parts']:
  n=part['filename'];path=B/n
  if n in aliases:path=Path('audit-cache')/aliases[n]
  elif not path.exists():path=Path('audit-cache')/n
  data=path.read_bytes();assert len(data)==part['bytes']and hashlib.sha256(data).hexdigest()==part['sha256'];chunks.append(data)
 raw=b''.join(chunks);assert len(raw)==p['bytes']and hashlib.sha256(raw).hexdigest()==p['sha256']
 with tempfile.TemporaryDirectory()as temp:
  root=Path(temp);arc=root/'candidate.zip';arc.write_bytes(raw);dest=root/'picon';dest.mkdir();sentinel=dest/'1_0_1_1234_2222_1_2EE0000_0_0_0.png';sentinel.write_bytes(b'OWNER_UNRELATED_FILE');wanted=set(changed['updated_members']);installed,available=install(object(),str(arc),str(dest),wanted)
  assert installed==wanted
  for n,h in changed['updated_members'].items():assert hashlib.sha256((dest/n).read_bytes()).hexdigest()==h
  assert sentinel.read_bytes()==b'OWNER_UNRELATED_FILE';checks.append({'selector':p['selector_id'],'resolution':p['resolution'],'family':p['family'],'installed_pngs':len(installed),'unrelated_user_file_preserved':True})
 print('RECEIVER_PASS',p['selector_id'],p['resolution'],p['family'],len(wanted),flush=True)
report={'status':'PASS','production_manifest_validator':'PASS','receiver_source_ref':'603218ea8fa51176f686f14f303509a4c64dc7e1','changed_archives_installed':len(checks),'installed_updated_png_entries':sum(x['installed_pngs']for x in checks),'all_chunk_and_archive_sha256_verified':True,'checks':checks};(B/'receiver-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='checks'}),flush=True)
