#!/usr/bin/env python3
"""Complete missing verified Vhannibal slots; preserve existing station artwork."""
from pathlib import Path
from collections import defaultdict,Counter
from concurrent.futures import ThreadPoolExecutor
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
import json,hashlib,io,urllib.request,copy,importlib.util,os,argparse
from PIL import Image
sha=lambda b:hashlib.sha256(b).hexdigest()
blob=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
PROVIDERS={'ANTIKSAT','DIGI_TELLY','FREESAT','SKYLINK','CANALPLUS_SK','CANALPLUS_CZ','DVB-T-SK-CZ'}
IMMUTABLE={'CANALPLUS_SK','CANALPLUS_CZ','DVB-T-SK-CZ'}
def reference(n):
 p=Path(n).stem.split('_')
 if len(p)!=10:return None
 try:return '_'.join(f'{int(x,16):X}' for x in p)
 except ValueError:return None
def fetch(u):
 for i in range(4):
  try:return urllib.request.urlopen(u,timeout=120).read()
  except Exception:
   if i==3:raise

def run(root,inputs,caches,write=True):
 config=json.load(open(inputs/'live-config.json'));plans=json.load(open(inputs/'plans.json'));art=json.load(open(inputs/'asset-index.json'));assets={a['asset_id']:a for a in art};data=root/'assets/warder/downloads/picons/channels';mf=data/'manifest.json';raw=mf.read_bytes();assert sha(raw)==config['base_manifest_sha256'];before=json.loads(raw);doc=copy.deepcopy(before);meta={p['filename']:p for p in before['parts']};selected_selectors={r['selector'] for r in plans}|PROVIDERS;packages=[p for p in before['packages'] if p['selector_id'] in selected_selectors and p['selector_id']!='DVB-T-SK-CZ'];cache=caches[0];cache.mkdir(parents=True,exist_ok=True);paths={}
 # All requests and all raw bytes are pinned to the input catalogue snapshot.
 def part_get(u):
  n=u.rsplit('/',1)[-1];spec=meta[n]
  for folder in caches:
   p=folder/n
   if p.exists() and p.stat().st_size==spec['bytes'] and sha(p.read_bytes())==spec['sha256']:paths[n]=p;return
  b=fetch(u.replace('/main/','/'+config['catalogue_base']+'/'));assert len(b)==spec['bytes'] and sha(b)==spec['sha256'];p=cache/n;p.write_bytes(b);paths[n]=p
 urls={u for p in packages for u in p['parts']}
 with ThreadPoolExecutor(max_workers=12) as pool:
  for i,_ in enumerate(pool.map(part_get,sorted(urls)),1):
   if i%50==0:print('PARTS',i,len(urls),flush=True)
 def archive(p):
  raw=b''.join(paths[u.rsplit('/',1)[-1]].read_bytes() for u in p['parts']);assert len(raw)==p['bytes'] and sha(raw)==p['sha256'];z=ZipFile(io.BytesIO(raw));assert z.testzip() is None;assert len(z.namelist())==len(set(z.namelist()));return raw,z
 wanted={r['reference']:r for r in plans};native={};canal=defaultdict(dict);membership=defaultdict(set);position_selectors={p['warder_key']:p['selector_id'] for p in packages if p['selector_id'] not in PROVIDERS and p['resolution']=='220x132'}
 # Native production bytes and protected CANAL bytes are canonical inputs, never
 # reconstructed from a station name or from a visually similar upstream logo.
 for p in packages:
  canonical=p['selector_id'] in ('CANALPLUS_SK','CANALPLUS_CZ');native_full=p['resolution']=='220x132' and p['selector_id'] not in PROVIDERS;provider_index=p['resolution']=='220x132' and p['selector_id'] in PROVIDERS
  if not (canonical or native_full or provider_index):continue
  _,z=archive(p)
  with z:
   for n in z.namelist():
    if not n.endswith('.png'):continue
    r=reference(n)
    if not r:continue
    if provider_index:membership[p['selector_id']].add(r)
    if canonical:
     b=z.read(n);v=(p['resolution'],p['family']);old=canal[v].get(r);assert old is None or old==b;canal[v][r]=b
    if native_full and r in wanted and wanted[r]['position']==p['warder_key']:native[(r,p['family'])]={'raw':z.read(n),'archive_sha256':p['sha256'],'package':p['filename']}
 assetsdir=inputs/'assets';assetsdir.mkdir(exist_ok=True)
 def get_asset(item):
  o=item;p=assetsdir/o['file']
  if p.exists():assert sha(p.read_bytes())==o['sha256'];return
  u='https://raw.githubusercontent.com/Evolution-by-Warder/PiconHub-Warder-Evolution/'+config['source_ref']+'/factory/temp/vhannibal-final-20261105/assets/'+o['file'];b=fetch(u);assert sha(b)==o['sha256'];p.write_bytes(b)
 with ThreadPoolExecutor(max_workers=12) as pool:list(pool.map(get_asset,[o for a in art for o in a['outputs'].values()]))
 sized={};native_proof={};guardplan=[];changes=[];newparts=[];partproof={};changedkeys=set();extra_holds=[];prefix_reused=0;coverage={}
 def png(row,family,res):
  if row['choice']=='PROTECTED_CANAL_REUSE':return canal[(res,family)][row['canal_source_reference']]
  if row['choice']=='CURRENT_NATIVE_REUSE':original=native[(row['reference'],family)]['raw']
  else:original=(assetsdir/assets[row['asset_id']]['outputs'][family.removeprefix('channel-')]['file']).read_bytes()
  if res=='220x132':return original
  key=(sha(original),res)
  if key not in sized:
   with Image.open(io.BytesIO(original)) as im:
    im.load();size=tuple(map(int,res.split('x')));out=io.BytesIO();im.convert('RGBA').convert('RGBa').resize(size,Image.Resampling.LANCZOS).convert('RGBA').save(out,format='PNG');sized[key]=out.getvalue()
  return sized[key]
 def provider_member(row,selector):
  if row['reference'] in membership.get(selector,set()):return True
  labels=config['bouquet_names'];names={labels.get(x,'').casefold().strip() for x in row['bouquets']};allowed={'DIGI_TELLY':{'telly'},'FREESAT':{'freesat','free sat'},'ANTIKSAT':{'antiksat','antik sat'},'SKYLINK':{'skylink'}}
  return bool(names&allowed.get(selector,set()))
 for number,p in enumerate(packages,1):
  if p['selector_id'] in IMMUTABLE:continue
  family=p['family'];res=p['resolution'];full=p['selector_id'] not in PROVIDERS;selected=[r for r in plans if position_selectors.get(r['position'])==p['selector_id']] if full else [r for r in plans if provider_member(r,p['selector_id'])]
  if not selected:continue
  raw,z=archive(p)
  with z:
   members={reference(n):n for n in z.namelist() if n.endswith('.png') and reference(n)};assert len(members)==p.get('png_count',len(members));updates={};rows={};oldhashes={}
   for r in selected:
    ref=r['reference'];n=members.get(ref,ref+'.png')
    if ref in members and r['choice']!='PROTECTED_CANAL_REUSE':continue
    b=png(r,family,res)
    if ref in members and z.read(n)==b:continue
    if ref in members:oldhashes[n]=sha(z.read(n))
    updates[n]=b;rows[n]=r
   if full:
    desired={r['reference'] for r in selected};available=set(members)|{reference(n) for n in updates};assert desired<=available;coverage['|'.join((p['selector_id'],res,family))]=len(desired)
   if not updates:print('UNCHANGED',p['selector_id'],res,family,flush=True);continue
   output=io.BytesIO(raw)
   with ZipFile(output,'a') as out:
    out.filelist=[copy.copy(x) for x in out.filelist if x.filename not in updates];out.NameToInfo={x.filename:x for x in out.filelist};out.start_dir=len(raw)
    for n,b in sorted(updates.items()):
     info=ZipInfo(n,(2026,11,5,0,0,0));info.compress_type=ZIP_DEFLATED;info.external_attr=0o100644<<16;out.writestr(info,b,compresslevel=9)
   packed=output.getvalue()
   with ZipFile(io.BytesIO(packed)) as test:
    assert test.testzip() is None;assert len(test.namelist())==len(set(test.namelist()));assert set(test.namelist())==set(z.namelist())|set(updates)
    for n in z.namelist():assert test.read(n)==updates.get(n,z.read(n)),n
    for n,b in updates.items():assert test.read(n)==b
   digest=sha(packed);filename='warder-'+p['selector_id'].lower()+'-'+res+'-'+family.removeprefix('channel-')+'-'+digest[:16]+'.zip';chunks=[];offset=0
   for u in p['parts']:
    v=paths[u.rsplit('/',1)[-1]].read_bytes()
    assert packed[offset:offset+len(v)]==v;chunks.append(v);offset+=len(v);prefix_reused+=len(v)
   chunks.extend(packed[start:start+4*1024*1024] for start in range(offset,len(packed),4*1024*1024));urls=[];prefix=p['parts'][0].rsplit('/',1)[0]+'/'
   for i,b in enumerate(chunks):
    n=filename+'.part%02d'%i;urls.append(prefix+n);newparts.append({'filename':n,'bytes':len(b),'sha256':sha(b)});partproof[n]=blob(b)
    if write and (not config.get('reuse_existing_git_blobs') or i>=len(p['parts'])):(data/n).write_bytes(b)
   q=next(x for x in doc['packages'] if x['filename']==p['filename']);q.update(filename=filename,sha256=digest,bytes=len(packed),parts=urls,png_count=len(members)+len(updates)-len(oldhashes))
   if 'included_references' in q:q['included_references']=sorted(set(members)|{reference(n) for n in updates})
   q['vhannibal_complete_20261105']={'source_ref':config['source_ref'],'added':len(updates)-len(oldhashes),'verified_canal_replacements':len(oldhashes),'method':'FILL_MISSING_SLOTS_REUSE_CANONICAL_BYTES'}
   records=[]
   for n,b in sorted(updates.items()):
    r=rows[n];rec={'reference':r['reference'],'member':n,'name':r['name'],'source_choice':r['choice'],'sha256':sha(b),'before_sha256':oldhashes.get(n)};records.append(rec);check={'path':'packages/'+p['selector_id']+'/'+n,'selector_id':p['selector_id'],'position':r['position'],'reference':r['reference'],'station_names':[r['name']],'content_sha256':sha(b),'resolution':res,'family':family}
    if r['choice']=='PROTECTED_CANAL_REUSE':check.update(operation='CANAL_CANONICAL_REUSE',source_reference=r['canal_source_reference'])
    elif r['position']=='23.5e' and r['choice']=='CURRENT_NATIVE_REUSE' and res in ('50x30','400x240'):
     source=native[(r['reference'],family)];k='|'.join((r['reference'],family,res));native_proof[k]={'reference':r['reference'],'png_sha256':sha(b),'source_native_sha256':sha(source['raw']),'source_archive_sha256':source['archive_sha256']};check.update(operation='PRESERVED_NATIVE_SIZE_DERIVATIVE',source_reference=r['reference'],source_native_sha256=sha(source['raw']))
    guardplan.append(check)
   changes.append({'selector':p['selector_id'],'resolution':res,'family':family,'before_archive_sha256':p['sha256'],'archive_sha256':digest,'added':len(updates)-len(oldhashes),'replaced_by_verified_canal':len(oldhashes),'unrelated_preserved':len(z.namelist())-len(oldhashes),'changes':records});changedkeys.add((p['selector_id'],res,family));print('COMPLETE_PACKAGE',number,len(packages),p['selector_id'],res,family,len(updates)-len(oldhashes),len(oldhashes),flush=True)
 # Complete the existing Skylink provider's missing 50/400 package slots from
 # its authoritative 220 roster. No new service membership is inferred.
 known_slots={(p['selector_id'],p['resolution'],p['family']) for p in doc['packages']};canal_uid=defaultdict(set)
 for (res,family),rows in canal.items():
  if res=='220x132':
   for r in rows:canal_uid[tuple(r.split('_')[3:7])].add(r)
 evidence=json.load(open(inputs/'guard/reuse-evidence.json'));approved_uid={tuple(c['reference'].split('_')[3:7]):c for c in evidence['candidates']}
 for parent in [p for p in list(doc['packages']) if p['selector_id']=='SKYLINK' and p['resolution']=='220x132']:
  previous=next(p for p in before['packages'] if p['selector_id']=='SKYLINK' and p['resolution']=='220x132' and p['family']==parent['family'])
  if parent['sha256']==previous['sha256']:srcraw,z=archive(previous)
  else:
   srcraw=b''.join((paths.get(u.rsplit('/',1)[-1]) or data/u.rsplit('/',1)[-1]).read_bytes() for u in parent['parts']);assert sha(srcraw)==parent['sha256'];z=ZipFile(io.BytesIO(srcraw))
  with z:
   sourceimages={reference(n):z.read(n) for n in z.namelist() if n.endswith('.png') and reference(n)}
  family=parent['family']
  for res in ('50x30','400x240'):
   if ('SKYLINK',res,family) in known_slots:continue
   output=io.BytesIO();records=[]
   with ZipFile(output,'w') as out:
    for r,original in sorted(sourceimages.items()):
     uid=tuple(r.split('_')[3:7]);canonical_ref=approved_uid.get(uid,{}).get('source_reference')
     if canonical_ref is None:
      candidates=[]
      for candidate in canal_uid.get(uid,[]):
       if all(candidate in canal.get((size,f),{}) for size in ('50x30','220x132','400x240') for f in ('channel-transparent','channel-white','channel-black')):candidates.append(candidate)
      signatures={tuple(sha(canal[(size,f)][rr]) for size in ('50x30','220x132','400x240') for f in ('channel-transparent','channel-white','channel-black')) for rr in candidates}
      if len(signatures)==1 and candidates:
       canonical_ref=candidates[0];extension={'reference':r,'source_reference':canonical_ref,'identity_evidence':'EXISTING_SKYLINK_NATIVE_ROSTER_AND_UNIQUE_COMPLETE_CANAL_UID_SIGNATURE'};evidence['candidates'].append(extension);approved_uid[uid]=extension
     if canonical_ref is not None:
      b=canal[(res,family)][canonical_ref];check={'operation':'CANAL_CANONICAL_REUSE','source_reference':canonical_ref}
     else:
      key=(sha(original),res)
      if key not in sized:
       with Image.open(io.BytesIO(original)) as im:
        im.load();dest=io.BytesIO();im.convert('RGBA').convert('RGBa').resize(tuple(map(int,res.split('x'))),Image.Resampling.LANCZOS).convert('RGBA').save(dest,format='PNG');sized[key]=dest.getvalue()
      b=sized[key];proofkey='|'.join((r,family,res));native_proof[proofkey]={'reference':r,'png_sha256':sha(b),'source_native_sha256':sha(original),'source_archive_sha256':parent['sha256']};check={'operation':'PRESERVED_NATIVE_SIZE_DERIVATIVE','source_reference':r,'source_native_sha256':sha(original)}
     n=r+'.png';info=ZipInfo(n,(2026,11,5,0,0,0));info.compress_type=ZIP_DEFLATED;info.external_attr=0o100644<<16;out.writestr(info,b,compresslevel=9);check.update(path='packages/SKYLINK/'+n,selector_id='SKYLINK',reference=r,content_sha256=sha(b),resolution=res,family=family);guardplan.append(check);records.append({'reference':r,'member':n,'name':'Existing Skylink roster reference','source_choice':'EXISTING_PROVIDER_NATIVE_ROSTER_SIZE_REUSE','sha256':sha(b),'before_sha256':None})
   packed=output.getvalue()
   with ZipFile(io.BytesIO(packed)) as check:assert check.testzip() is None and len(check.namelist())==len(sourceimages)
   digest=sha(packed);filename='warder-skylink-'+res+'-'+family.removeprefix('channel-')+'-'+digest[:16]+'.zip';urls=[];prefix=parent['parts'][0].rsplit('/',1)[0]+'/'
   for i,start in enumerate(range(0,len(packed),4*1024*1024)):
    b=packed[start:start+4*1024*1024];n=filename+'.part%02d'%i;urls.append(prefix+n);newparts.append({'filename':n,'bytes':len(b),'sha256':sha(b)});partproof[n]=blob(b)
    if write:(data/n).write_bytes(b)
   q=copy.deepcopy(parent);q.update(resolution=res,filename=filename,sha256=digest,bytes=len(packed),parts=urls,png_count=len(sourceimages));q['vhannibal_complete_20261105']={'source_ref':config['source_ref'],'new_size_slot_from_native_roster':True,'source_native_archive_sha256':parent['sha256']};doc['packages'].append(q);known_slots.add(('SKYLINK',res,family));changes.append({'selector':'SKYLINK','resolution':res,'family':family,'before_archive_sha256':None,'archive_sha256':digest,'added':len(sourceimages),'replaced_by_verified_canal':0,'unrelated_preserved':0,'changes':records});changedkeys.add(('SKYLINK',res,family));print('CREATED_PROVIDER_SIZE','SKYLINK',res,family,len(sourceimages),flush=True)
 (inputs/'guard/reuse-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')

 # The additional size-copy proof can only reproduce a published native PNG for
 # the identical full reference. It cannot approve upstream/renamed artwork.
 guarddir=inputs/'guard';(guarddir/'published-native-reuse.json').write_text(json.dumps(native_proof,indent=2)+'\n');spec=importlib.util.spec_from_file_location('guard',guarddir/'guard.py');guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard);decisions=guard.validate_plan(guardplan);assert all(x['allowed'] for x in decisions),[x for x in decisions if not x['allowed']][:5]
 for p,q in zip(before['packages'],doc['packages']):
  if (p['selector_id'],p['resolution'],p['family']) not in changedkeys:assert p==q
 assert [p for p in before['packages'] if p['selector_id'] in ('CANALPLUS_SK','CANALPLUS_CZ')]==[p for p in doc['packages'] if p['selector_id'] in ('CANALPLUS_SK','CANALPLUS_CZ')]
 refs={u.rsplit('/',1)[-1] for p in doc['packages'] for u in p['parts']};doc['parts']=sorted([x for x in before['parts']+newparts if x['filename'] in refs],key=lambda x:x['filename']);assert len({x['filename'] for x in doc['parts']})==len(doc['parts'])
 # Verify every accepted programme is present in all nine full-position slots.
 for row in plans:
  selector=position_selectors[row['position']]
  assert all('|'.join((selector,size,family)) in coverage for size in ('50x30','220x132','400x240') for family in ('channel-transparent','channel-white','channel-black')),('Missing full-position slot',selector)
 summary={'status':'ALL_USABLE_SOURCE_REFERENCES_PUBLISHED_WITH_TERMINAL_EXCEPTIONS','source_ref':config['source_ref'],'source_png_items':14081,'accepted_current_references':len(plans),'terminal_reference_exceptions':config['terminal_reference_exceptions'],'changed_packages':len(changes),'added_png_entries':sum(x['added'] for x in changes),'verified_canal_png_replacements':sum(x['replaced_by_verified_canal'] for x in changes),'unrelated_entries_preserved':sum(x['unrelated_preserved'] for x in changes),'old_compressed_prefix_bytes_reused':prefix_reused,'original_canal_packages_preserved':18,'native_size_reuse_proofs':len(native_proof),'full_position_coverage':coverage,'changes':changes}
 doc['vhannibal_complete_20261105']={k:v for k,v in summary.items() if k not in ('changes','full_position_coverage')};(inputs/'live-verification.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');(inputs/'part-git-shas.json').write_text(json.dumps(partproof,sort_keys=True,indent=2)+'\n')
 final=(json.dumps(doc,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
 if config.get('expected_manifest_sha256'):assert sha(final)==config['expected_manifest_sha256'],'Independent catalogue reproduction differs'
 if write:
  mf.write_bytes(final);sums=data/'SHA256SUMS';values={l.split()[-1]:l.split()[0] for l in sums.read_text().splitlines() if l.strip()};values.update({x['filename']:x['sha256'] for x in newparts});values['manifest.json']=sha(final);sums.write_text(''.join(h+'  '+n+'\n' for n,h in sorted(values.items())))
 print('LIVE_COMPLETE',json.dumps({k:v for k,v in summary.items() if k not in ('changes','full_position_coverage')}),flush=True)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--root',type=Path,required=True);a.add_argument('--inputs',type=Path,required=True);a.add_argument('--cache',type=Path,action='append',required=True);r=a.parse_args();run(r.root,r.inputs,r.cache)
