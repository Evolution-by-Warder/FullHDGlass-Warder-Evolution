from pathlib import Path
import json,hashlib,ast,os,stat,shutil,tempfile,zipfile,importlib.util,io
from PIL import Image
SHA=lambda b:hashlib.sha256(b).hexdigest();M=json.load(open('sky-output/manifest.json'));spec=importlib.util.spec_from_file_location('sync','warderPiconSync.py');sync=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync);assert sync.validate_publication_manifest(M)==[]
tr=ast.parse(Path('live-receiver-plugin.py').read_bytes());fn=next(n for n in ast.walk(tr)if isinstance(n,ast.FunctionDef)and n.name=='_warderInstallChannelArchive');scope=dict(warderPiconSync=sync,os=os,shutil=shutil,tempfile=tempfile,zipfile=zipfile,stat=stat);exec(compile(ast.Module(body=[fn],type_ignores=[]),'current-1.0.72-receiver','exec'),scope);install=scope[fn.name];checks=[]
for folder,report in [('resume-output','batch-20261108.json'),('delta-output','source-delta-batch-20261108.json'),('rtp-output','rtp-rebrand-batch-20261108.json'),('sky-output','sky-boxoffice-batch-20261108.json')]:
 for c in json.load(open(Path(folder)/report))['packages']:
  p=next(p for p in M['packages']if p['selector_id']==c['selector']and p['resolution']==c['resolution']and p['family']==c['family']);actual_folder='sky-output'if c['selector']=='282E'else folder;raw=(Path(actual_folder)/(p['filename']+'.local')).read_bytes();assert SHA(raw)==p['sha256']
  with tempfile.TemporaryDirectory()as t:
   root=Path(t);dest=root/'picon';dest.mkdir();sentinel=dest/'1_0_1_EEEE_FFFE_1_820000_0_0_0.png';buf=io.BytesIO();Image.new('RGBA',tuple(map(int,p['resolution'].split('x'))),(20,170,90,255)).save(buf,format='PNG');owner=buf.getvalue();sentinel.write_bytes(owner);archive=root/'candidate.zip';archive.write_bytes(raw);wanted=set(c['updated_members']);assert sentinel.name not in wanted;done,_=install(object(),str(archive),str(dest),wanted);assert done==wanted
   for n,h in c['updated_members'].items():assert SHA((dest/n).read_bytes())==h
   assert sentinel.read_bytes()==owner
  checks.append({'filename':p['filename'],'selected_pngs_installed':len(wanted),'valid_unrelated_user_png_preserved':True})
protected=[]
base=json.load(open('resume-manifest.json'))
for p in M['packages']:
 if p['selector_id']not in('CANALPLUS_SK','CANALPLUS_CZ'):continue
 assert p in base['packages'];raw=(Path('archives')/p['filename']).read_bytes();assert SHA(raw)==p['sha256']and len(raw)==p['bytes'];assert zipfile.ZipFile(io.BytesIO(raw)).testzip()is None;protected.append({'filename':p['filename'],'sha256':p['sha256']})
assert len(checks)==72 and sum(c['selected_pngs_installed']for c in checks)==153 and len(protected)==18
report={'status':'PASS','manifest_validator':'PASS','receiver_ref':'12247acc20f699606f6d40f3783e4162b92674b9','receiver_installer_ast_sha256':SHA(ast.dump(fn,include_attributes=False).encode()),'installer_archives':len(checks),'installed_new_pngs':153,'valid_unrelated_user_png_preserved_in_every_test':True,'protected_canal_packages_sha256_crc':protected,'checks':checks,'hardware_receiver_tested':False};Path('continuation-install-checks.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS install72 installation cases /153new PNG +valid userPNG sentinel;18CANAL SHA/CRC; final manifest')
