#!/usr/bin/env python3
"""Resume exact approved-artwork reuse on PR50; no logo rendering or production write."""
import json,hashlib,zipfile,io,copy,ast,os,stat,shutil,tempfile,importlib.util
from pathlib import Path
from PIL import Image,ImageDraw
B=Path('.');O=Path('delta-output');O.mkdir(exist_ok=True)
SHA=lambda b:hashlib.sha256(b).hexdigest()
GIT=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
BASE=json.load(open('resume-output/manifest.json'));LIVE=json.load(open('main-manifest.json'));M=copy.deepcopy(BASE)
P={(p['selector_id'],p['resolution'],p['family']):p for p in BASE['packages']};PM={p['filename']:p for p in BASE['parts']};aliases=[];newparts=[];proof=[];changes={};refs=[]
plans=json.load(open('delta-plans.json'))
cache={}
def arc(p):
 n=p['filename']
 if n not in cache:
  raw=(Path('archives')/n).read_bytes();assert len(raw)==p['bytes']and SHA(raw)==p['sha256'];z=zipfile.ZipFile(io.BytesIO(raw));assert z.testzip()is None and len(z.namelist())==len(set(z.namelist()));cache[n]=(raw,z)
 return cache[n]
imgs=[]
for target,sel,donor,dsel,name in plans:
 assert int(target.split('_')[2],16)not in(2,10)
 evidence=[]
 for size in ('50x30','220x132','400x240'):
  for style in ('transparent','white','black'):
   family='channel-'+style;p=P[sel,size,family];src=P[dsel,size,family];_,z=arc(src);data=z.read(donor+'.png');im=Image.open(io.BytesIO(data)).convert('RGBA');im.load();assert im.size==tuple(map(int,size.split('x')))and im.getchannel('A').getbbox()
   _,dst=arc(p);exists=target+'.png'in dst.namelist()
   if exists:
    # Only Güneydoğu's original native size exists; preserve it exactly.
    assert name=='GUNEYDOGU TV'and size=='220x132';oldim=Image.open(io.BytesIO(dst.read(target+'.png'))).convert('RGBA');assert oldim.tobytes()==im.tobytes();operation='PRESERVE_EXISTING_PIXEL_IDENTICAL'
   else:changes.setdefault(p['filename'],{})[target+'.png']=data;operation='COPY_APPROVED_PNG_BYTES'
   evidence.append({'size':size,'family':family,'source_package':src['filename'],'source_reference':donor,'sha256':SHA(data),'operation':operation})
   if size=='220x132':imgs.append((name+' / '+style,im.copy()))
 refs.append({'reference':target,'name':name,'selector':sel,'donor':donor,'variants':evidence,'rendered_pixels':0})
for n,updates in sorted(changes.items()):
 p=next(p for p in BASE['packages']if p['filename']==n);raw,z=arc(p);buf=io.BytesIO(raw)
 with zipfile.ZipFile(buf,'a')as out:
  assert not(set(updates)&set(z.namelist()));out.start_dir=len(raw)
  for member,data in sorted(updates.items()):
   info=zipfile.ZipInfo(member,(2026,11,8,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;out.writestr(info,data,compresslevel=9)
 packed=buf.getvalue();assert packed[:len(raw)]==raw;check=zipfile.ZipFile(io.BytesIO(packed));assert check.testzip()is None;assert set(check.namelist())==set(z.namelist())|set(updates);assert len(check.namelist())==len(set(check.namelist()))
 for old in z.namelist():assert z.read(old)==check.read(old)
 for member,data in updates.items():assert check.read(member)==data
 h=SHA(packed);newname=f"warder-{p['selector_id'].lower()}-{p['resolution']}-{p['family'][8:]}-{h[:16]}.zip";urls=[]
 for i,u in enumerate(p['parts']):
  old=u.rsplit('/',1)[-1];meta=PM[old];data=(Path('cache')/meta['sha256']).read_bytes();assert SHA(data)==meta['sha256'];new=newname+f'.part{i:02d}';aliases.append({'path':'assets/warder/downloads/picons/channels/'+new,'mode':'100644','type':'blob','sha':GIT(data)});newparts.append({**meta,'filename':new});urls.append(u.rsplit('/',1)[0]+'/'+new)
 tail=packed[len(raw):];assert len(tail)<4194304;tailname=newname+f'.part{len(urls):02d}';(O/tailname).write_bytes(tail);urls.append(p['parts'][0].rsplit('/',1)[0]+'/'+tailname);newparts.append({'filename':tailname,'bytes':len(tail),'sha256':SHA(tail)})
 q=next(x for x in M['packages']if x['filename']==n);q.update(filename=newname,bytes=len(packed),sha256=h,parts=urls,png_count=len(check.namelist()));q['vhannibal_source_delta_20261108']={'report':'reports/vhannibal-followup-20261106/source-delta-batch-20261108.json','references':sorted(x[:-4]for x in updates)}
 if 'included_references'in q:q['included_references']=sorted(set(q['included_references'])|{x[:-4]for x in updates})
 proof.append({'selector':p['selector_id'],'resolution':p['resolution'],'family':p['family'],'before_filename':n,'filename':newname,'before_sha256':p['sha256'],'sha256':h,'updated_members':{x:SHA(v)for x,v in updates.items()},'preserved_members':len(z.namelist()),'old_prefix_preserved':len(raw),'new_tail_bytes':len(tail)})
 (O/(newname+'.local')).write_bytes(packed)
parts={x['filename']:x for x in BASE['parts']+newparts};used={u.rsplit('/',1)[-1]for p in M['packages']for u in p['parts']};M['parts']=sorted([parts[n]for n in used],key=lambda p:p['filename'])
protected=lambda m:[p for p in m['packages']if p['selector_id']in('CANALPLUS_SK','CANALPLUS_CZ')]
assert len(protected(M))==18 and protected(M)==protected(BASE)==protected(LIVE)
M['vhannibal_source_delta_20261108']={'new_references':12,'added_png_entries':108,'changed_archives':36,'rendered_artworks':0,'production_merged':False,'report':'reports/vhannibal-followup-20261106/source-delta-batch-20261108.json'}
raw=(json.dumps(M,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode();(O/'manifest.json').write_bytes(raw)
# Preserve all existing checksum lines and append names for the new immutable parts.
import subprocess
sums=Path('resume-output/SHA256SUMS').read_text();sums={x.split()[-1]:x.split()[0]for x in sums.splitlines()if x.strip()};sums.update({p['filename']:p['sha256']for p in M['parts']});sums['manifest.json']=SHA(raw);(O/'SHA256SUMS').write_text(''.join(h+'  '+n+'\n'for n,h in sorted(sums.items())))
spec=importlib.util.spec_from_file_location('sync',Path('warderPiconSync.py'));sync=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync);assert sync.validate_publication_manifest(M)==[]
tr=ast.parse(Path('receiver-plugin.py').read_bytes());fn=next(n for n in ast.walk(tr)if isinstance(n,ast.FunctionDef)and n.name=='_warderInstallChannelArchive');scope=dict(warderPiconSync=sync,os=os,shutil=shutil,tempfile=tempfile,zipfile=zipfile,stat=stat);exec(compile(ast.Module(body=[fn],type_ignores=[]),'current-receiver','exec'),scope);install=scope[fn.name]
for change in proof:
 p=next(p for p in M['packages']if p['filename']==change['filename']);jobs=sync.build_download_jobs(M,{'state':'ready','packages':[p]});assert jobs['state']=='ready'
 with tempfile.TemporaryDirectory()as temp:
  root=Path(temp);dest=root/'picon';dest.mkdir();sentinel=dest/'OWNER_SENTINEL';sentinel.write_bytes(b'PRESERVE');arcpath=O/(p['filename']+'.local');wanted=set(change['updated_members']);installed,available=install(object(),str(arcpath),str(dest),wanted);assert installed==wanted
  for n,h in change['updated_members'].items():assert SHA((dest/n).read_bytes())==h
  assert sentinel.read_bytes()==b'PRESERVE'
 change['receiver_install']='PASS'
assert len(refs)==12 and len(proof)==36 and sum(len(p['updated_members'])for p in proof)==108
report={'status':'PASS_WORKING_CANDIDATE_ONLY','date':'2026-11-08','base_production_sha':'12247acc20f699606f6d40f3783e4162b92674b9','base_candidate_sha':'20aa8c68c8e9c4b55a6ce1a9a3d1b441d4d464c9','new_references':12,'added_png_entries':108,'changed_zip_archives':36,'untouched_png_entries_byte_identical':sum(p['preserved_members']for p in proof),'protected_canal_packages_unchanged':18,'radio_changes':0,'new_or_rendered_artworks':0,'manifest_validator':'PASS','references':refs,'packages':proof}
(O/'source-delta-batch-20261108.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(O/'aliases.json').write_text(json.dumps(aliases))
canvas=Image.new('RGB',(720,160*((len(imgs)+2)//3)),(128,128,128));d=ImageDraw.Draw(canvas)
for i,(label,im)in enumerate(imgs):x=i%3*240;y=i//3*160;d.text((x+2,y+2),label,fill='white');canvas.paste(im,(x+8,y+23),im)
canvas.save(O/'approved-reuse-preview.png');print({k:v for k,v in report.items()if k not in('references','packages')},flush=True)
