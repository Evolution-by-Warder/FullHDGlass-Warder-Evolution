from pathlib import Path
import json,hashlib,ast,os,stat,shutil,tempfile,zipfile,importlib.util,io
from PIL import Image
H=lambda b:hashlib.sha256(b).hexdigest();O=Path('approved-output');M=json.load(open(O/'manifest.json'));spec=importlib.util.spec_from_file_location('sync','warderPiconSync.py');sync=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync);assert sync.validate_publication_manifest(M)==[];PM={p['filename']:p for p in M['parts']}
tree=ast.parse(Path('live-receiver-plugin.py').read_bytes());fn=next(n for n in ast.walk(tree)if isinstance(n,ast.FunctionDef)and n.name=='_warderInstallChannelArchive');scope=dict(warderPiconSync=sync,os=os,shutil=shutil,tempfile=tempfile,zipfile=zipfile,stat=stat);exec(compile(ast.Module(body=[fn],type_ignores=[]),'stable-1.0.72','exec'),scope);checks=[]
parts_by_hash={H(f.read_bytes()):f for folder in ['batch-output','resume-output','delta-output','rtp-output','sky-output','approved-output']for f in Path(folder).glob('*.part*')}
proof=json.load(open(O/'approved-artwork-six-batch-20261108.json'))
for c in proof['packages']:
 p=next(p for p in M['packages']if p['filename']==c['filename']);raw=(O/(p['filename']+'.local')).read_bytes();assert H(raw)==p['sha256'];parts=[]
 for u in p['parts']:
  meta=PM[u.rsplit('/',1)[-1]];path=next(q for q in [Path('cache')/meta['sha256'],parts_by_hash.get(meta['sha256'],Path('NO_SUCH_PART'))]if q.exists());data=path.read_bytes();assert H(data)==meta['sha256']and len(data)==meta['bytes'];parts.append(data)
 assert b''.join(parts)==raw;z=zipfile.ZipFile(io.BytesIO(raw));assert z.testzip()is None
 with tempfile.TemporaryDirectory()as t:
  dest=Path(t)/'picon';dest.mkdir();buf=io.BytesIO();Image.new('RGBA',tuple(map(int,p['resolution'].split('x'))),(12,123,234,127)).save(buf,format='PNG');sentinel=dest/'1_0_1_EEEE_FFFE_1_820000_0_0_0.png';sentinel.write_bytes(buf.getvalue());done,_=scope[fn.name](object(),str(O/(p['filename']+'.local')),str(dest),set(c['updated_members']));assert done==set(c['updated_members']);assert sentinel.read_bytes()==buf.getvalue()
  for n,h in c['updated_members'].items():assert H((dest/n).read_bytes())==h
 checks.append({'filename':p['filename'],'png_count_added':len(done),'parts_sha256_crc_installer_user_png':'PASS'})
protected=[];base=json.load(open('sky-output/manifest.json'))
for p in M['packages']:
 if p['selector_id']not in('CANALPLUS_SK','CANALPLUS_CZ'):continue
 assert p in base['packages'];raw=(Path('archives')/p['filename']).read_bytes();assert H(raw)==p['sha256']and len(raw)==p['bytes'];assert zipfile.ZipFile(io.BytesIO(raw)).testzip()is None;protected.append({'filename':p['filename'],'sha256':p['sha256']})
assert len(protected)==18;assert len(checks)==18 and sum(c['png_count_added']for c in checks)==54
for r in proof['references']:
 for v in r['variants']:
  im=Image.open(Path('workrepo')/v['approved_source_file']).convert('RGBA');v['alpha_extrema']=list(im.getchannel('A').getextrema());assert im.getchannel('A').getbbox()
proof.update(owner_approval={'date':'2026-11-08','scope':'Exact prepared BloombergHT2,BetfredTV1-3,SIS Racing/SISSP1; user personally reviewed ARTWORK_APPROVAL.md. SISSP identity is limited to this prepared artwork; no expansion of SP or unrelated aliases.','production_merge_authorized':False},current_installer_checks=checks,protected_canal_sha256_crc=protected,installer_ast_sha256=H(ast.dump(fn,include_attributes=False).encode()),hardware_receiver_tested=False)
(O/'approved-artwork-six-batch-20261108.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print('PASS:6 refs/54 exact approved PNG/18 ZIP;parts SHA/CRC/alpha/dimensions;stable installer+valid user sentinel;18protected SHA/CRC')
