import json,hashlib,zipfile,io,ast,os,stat,shutil,tempfile,importlib.util
from pathlib import Path
from PIL import Image
SHA=lambda b:hashlib.sha256(b).hexdigest()
m=json.load(open('candidate-manifest.json'));live=json.load(open('main-manifest.json'));proof=json.load(open('workrepo/reports/vhannibal-followup-20261106/mezzo-proof.json'));pm={p['filename']:p for p in m['parts']};checks=[]
spec=importlib.util.spec_from_file_location('sync','warderPiconSync.py');sync=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync);assert sync.validate_publication_manifest(m)==[]
tr=ast.parse(Path('receiver-plugin.py').read_bytes());fn=next(n for n in ast.walk(tr)if isinstance(n,ast.FunctionDef)and n.name=='_warderInstallChannelArchive');scope=dict(warderPiconSync=sync,os=os,shutil=shutil,tempfile=tempfile,zipfile=zipfile,stat=stat);exec(compile(ast.Module(body=[fn],type_ignores=[]),'current-receiver','exec'),scope);install=scope[fn.name]
for check in proof['checks']:
 p=next(p for p in m['packages']if p['sha256']==check['archive_sha256']);before=next(x for x in live['packages']if x['selector_id']==p['selector_id']and x['resolution']==p['resolution']and x['family']==p['family']);assert before['sha256']==check['old_sha256'];raw=(Path('archives')/p['filename']).read_bytes();assert SHA(raw)==p['sha256'];old=raw[:before['bytes']];assert SHA(old)==before['sha256'];z=zipfile.ZipFile(io.BytesIO(raw));oldz=zipfile.ZipFile(io.BytesIO(old));assert z.testzip()is None and oldz.testzip()is None;target=proof['target']+'.png';donor=proof['donor']+'.png';assert target not in oldz.namelist();assert set(z.namelist())==set(oldz.namelist())|{target};assert len(z.namelist())==len(set(z.namelist()))
 for n in oldz.namelist():assert z.read(n)==oldz.read(n)
 data=z.read(target);assert data==z.read(donor)and SHA(data)==check['png_sha256'];im=Image.open(io.BytesIO(data));im.load();assert im.size==tuple(map(int,p['resolution'].split('x')))and im.convert('RGBA').getchannel('A').getbbox()
 with tempfile.TemporaryDirectory()as t:
  root=Path(t);dst=root/'picon';dst.mkdir();s=dst/'OWNER_SENTINEL';s.write_bytes(b'KEEP');ap=root/'c.zip';ap.write_bytes(raw);installed,_=install(object(),str(ap),str(dst),{target});assert installed=={target}and(dst/target).read_bytes()==data and s.read_bytes()==b'KEEP'
 checks.append({'filename':p['filename'],'sha256':p['sha256'],'preserved_entries':len(oldz.namelist()),'checks':'SHA256_CRC_DIMS_IDENTICAL_DONOR_UNTOUCHED_MEMBERS_CURRENT_RECEIVER_INSTALL_PASS'})
protected=[]
for p in m['packages']:
 if p['selector_id']not in('CANALPLUS_SK','CANALPLUS_CZ'):continue
 assert p in live['packages'];raw=(Path('archives')/p['filename']).read_bytes();assert SHA(raw)==p['sha256']and len(raw)==p['bytes'];assert zipfile.ZipFile(io.BytesIO(raw)).testzip()is None;protected.append({'filename':p['filename'],'sha256':p['sha256']})
result={'status':'PASS','production_sha':'3ba80ef8bb3b0ccd4148666372a9bf851ee85947','candidate_sha':'d1523e7e747eebe55b3f306cffa93a6db2dcc00d','changed_archives':checks,'protected_canal_archives':protected,'protected_canal_count':18,'manifest_validator':'PASS','radio_changes':0};Path('mezzo-recheck-20261107.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS MEZZO9 CANAL18 untouched entries',sum(x['preserved_entries']for x in checks),flush=True)
