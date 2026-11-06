from pathlib import Path
import json,gzip,collections,hashlib,io,zipfile,copy,functools,re
from PIL import Image
B=Path('audit-cache');O=Path('audit-output/approved-repairs');O.mkdir(exist_ok=True);M=json.load(open('manifest.json'));packages={(p['selector_id'],p['resolution'],p['family']):p for p in M['packages']};plans={x['reference']:x for x in json.load(open('plans.json'))};led={x['reference']:x for x in json.loads(gzip.decompress(Path('audit-output/source-reference-ledger.json.gz').read_bytes()))};candidates=json.load(open('audit-output/new-reference-reuse-candidates.json'));manifest=copy.deepcopy(M);spec={x['filename']:x for x in M['parts']};SHA=lambda v:hashlib.sha256(v).hexdigest();V=[(s,'channel-'+f)for s in('50x30','220x132','400x240')for f in('transparent','white','black')]
def norm(s):return re.sub('[^a-z0-9]','',re.sub(r'\b(?:hd|sd)\b','',s.casefold()))
@functools.lru_cache(maxsize=6)
def arc(filename):
 p=next(p for p in M['packages']if p['filename']==filename);raw=b''.join((B/u.rsplit('/',1)[-1]).read_bytes()for u in p['parts']);assert SHA(raw)==p['sha256'];z=zipfile.ZipFile(io.BytesIO(raw));assert z.testzip()is None;return raw,z
changes=collections.defaultdict(dict);evidence=[]
for c in candidates:
 if c['scope']!='SATELLITE_TV' or not c['pixel_exact_prior_refs']or c['names']==['Service 13232']:continue
 r=c['reference'];meta=led[r]['service'];position=meta['position'];target=next(p['selector_id']for p in M['packages']if p['warder_key']==position and p['selector_id']not in{'ANTIKSAT','DIGI_TELLY','FREESAT','SKYLINK','CANALPLUS_SK','CANALPLUS_CZ','DVB-T-SK-CZ'})
 options=c['pixel_exact_prior_refs'];options.sort(key=lambda q:(norm(plans[q]['name'])not in{norm(n)for n in c['names']},plans[q]['position']!=position,q));old=options[0];plan=plans[old];canonical=plan.get('canal_source_reference');source_selector='CANALPLUS_SK'if canonical else plan['selector'];source_ref=canonical or old
 selected=[]
 for size,family in V:
  if canonical:
   pp=packages[(source_selector,size,family)];_,z=arc(pp['filename'])
   if source_ref+'.png'not in z.namelist():pp=packages[('CANALPLUS_CZ',size,family)];_,z=arc(pp['filename'])
  else:pp=packages[(source_selector,size,family)];_,z=arc(pp['filename'])
  data=z.read(source_ref+'.png');im=Image.open(io.BytesIO(data));im.load();assert im.size==tuple(map(int,size.split('x')))and im.convert('RGBA').getchannel('A').getbbox()
  for sel in([target,'SKYLINK']if target=='235E'else[target]):
   p=packages[(sel,size,family)];_,dest=arc(p['filename']);assert r+'.png'not in dest.namelist(),'not genuinely missing';changes[p['filename']][r+'.png']=data
  selected.append({'resolution':size,'family':family,'source_package':pp['filename'],'source_reference':source_ref,'sha256':SHA(data)})
 evidence.append({'operation':'EXACT_APPROVED_NINE_VARIANT_REUSE','reference':r,'name':meta['name'],'position':position,'provider':meta['provider'],'current_lamedb_sha256':meta['lamedb_sha256'],'source_reference':old,'source_name':plan['name'],'canonical_source':canonical,'original_pixel_match':led[r]['rgba_sha256'],'source_archive_sha256':'011f4f931088e6a3a6be1e4fe69a22b1909caf522384de371d27cc64b7dbd052','variants':selected})
# Exact existing full-reference transparent originals repair twelve blank derivatives.
for sid in('F79','F7A'):
 for typ in('1','16','19'):
  r=f'1_0_{typ}_{sid}_19C8_FBFF_820000_0_0_0';p=packages[('130E','220x132','channel-transparent')];_,z=arc(p['filename']);raw=z.read(r+'.png');im=Image.open(io.BytesIO(raw)).convert('RGBA');assert im.getchannel('A').getbbox();derivatives=[]
  for size in('50x30','400x240'):
   q=packages[('130E',size,'channel-transparent')];_,dest=arc(q['filename']);before=dest.read(r+'.png');assert Image.open(io.BytesIO(before)).convert('RGBA').getchannel('A').getbbox()is None
   out=io.BytesIO();im.convert('RGBa').resize(tuple(map(int,size.split('x'))),Image.Resampling.LANCZOS).convert('RGBA').save(out,format='PNG');data=out.getvalue();changes[q['filename']][r+'.png']=data;derivatives.append({'resolution':size,'family':'channel-transparent','sha256':SHA(data),'before_sha256':SHA(before)})
  evidence.append({'operation':'REPAIR_EMPTY_TRANSPARENT_DERIVATIVE','reference':r,'name':'Sky Adventure','source_reference':r,'source_native_sha256':SHA(raw),'variants':derivatives})
# Preserve every byte outside changes. New ZIPs reuse existing archive prefixes.
parts=[];proof=[]
for filename,updates in sorted(changes.items()):
 p=next(x for x in M['packages']if x['filename']==filename);assert p['selector_id']not in('CANALPLUS_SK','CANALPLUS_CZ','DVB-T-SK-CZ');raw,z=arc(filename);buf=io.BytesIO(raw)
 with zipfile.ZipFile(buf,'a')as out:
  out.filelist=[copy.copy(i)for i in out.filelist if i.filename not in updates];out.NameToInfo={i.filename:i for i in out.filelist};out.start_dir=len(raw)
  for n,data in sorted(updates.items()):
   info=zipfile.ZipInfo(n,(2026,11,6,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;out.writestr(info,data,compresslevel=9)
 packed=buf.getvalue();assert packed[:len(raw)]==raw
 with zipfile.ZipFile(io.BytesIO(packed))as check:
  assert check.testzip()is None and len(check.namelist())==len(set(check.namelist()))
  assert set(check.namelist())==set(z.namelist())|set(updates)
  for n in z.namelist():assert check.read(n)==updates.get(n,z.read(n))
  for n,data in updates.items():assert check.read(n)==data
 digest=SHA(packed);newname='warder-'+p['selector_id'].lower()+'-'+p['resolution']+'-'+p['family'].removeprefix('channel-')+'-'+digest[:16]+'.zip';urls=list(p['parts']);off=len(raw)
 for i in range(off,len(packed),4*1024*1024):
  data=packed[i:i+4*1024*1024];n=newname+f'.part{len(urls):02d}';(O/n).write_bytes(data);urls.append(p['parts'][0].rsplit('/',1)[0]+'/'+n);parts.append({'filename':n,'bytes':len(data),'sha256':SHA(data)})
 q=next(x for x in manifest['packages']if x['filename']==filename);q.update(filename=newname,parts=urls,bytes=len(packed),sha256=digest,png_count=len(set(z.namelist())|set(updates)));q['completeness_repairs_20261106']={'report':'reports/vhannibal-completeness-20261106/approved-reuse-repairs.json','updated_references':sorted(Path(n).stem for n in updates)}
 if 'included_references'in q:q['included_references']=sorted(set(q['included_references'])|{Path(n).stem for n in updates})
 proof.append({'selector':p['selector_id'],'resolution':p['resolution'],'family':p['family'],'before_archive_sha256':p['sha256'],'sha256':digest,'updated_members':{n:SHA(v)for n,v in updates.items()},'old_prefix_preserved':len(raw)})
used={u.rsplit('/',1)[-1]for p in manifest['packages']for u in p['parts']};manifest['parts']=sorted([x for x in M['parts']+parts if x['filename']in used],key=lambda x:x['filename']);assert len(manifest['parts'])==len(used)
assert [p for p in M['packages']if p['selector_id']in('CANALPLUS_SK','CANALPLUS_CZ')]==[p for p in manifest['packages']if p['selector_id']in('CANALPLUS_SK','CANALPLUS_CZ')]
summary={'new_current_references_repaired':sum(x['operation']=='EXACT_APPROVED_NINE_VARIANT_REUSE'for x in evidence),'existing_reference_derivatives_repaired':sum(x['operation']=='REPAIR_EMPTY_TRANSPARENT_DERIVATIVE'for x in evidence),'changed_packages':len(proof),'updated_png_entries':sum(len(x)for x in changes.values()),'new_part_bytes':sum(x['bytes']for x in parts),'canonical_canal_packages_changed':0,'radio_references_changed':0,'publication':'WORKING_BRANCH_ONLY_PENDING_OWNER_APPROVAL'}
manifest['vhannibal_completeness_repairs_20261106']=summary;(O/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n');(O/'approved-reuse-repairs.json').write_text(json.dumps({'summary':summary,'references':evidence,'packages':proof},ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary),flush=True)
