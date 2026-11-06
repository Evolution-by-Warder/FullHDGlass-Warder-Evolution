#!/usr/bin/env python3
"""Render review-only V9 repairs from exact audited upstream bytes. Never publish."""
import concurrent.futures,gzip,hashlib,importlib.util,io,json,os,re,sys,urllib.request,zipfile
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
OUT=Path(os.environ.get('WARDER_REVIEW_OUT','candidate-v9-review'));OUT.mkdir(exist_ok=True)
SHA=lambda v:hashlib.sha256(v).hexdigest()
PIN='76f2f4be11a30144ece35492dfb188a54bd747d4'
MASTER_HASH={'black':'61e69f7fc46e340453bf74ccd7af6ac9d8eba9f8e232884659e1ea99f6abf3fe','white':'c6ae4a808a65ffc8e6458336fccbfe4216de1e832ec0a9abf800907f2f783589'}
def get(url,digest,path):
 if path.exists()and SHA(path.read_bytes())==digest:return path.read_bytes()
 for attempt in range(3):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'Warder-Reference-Audit/1.0','Referer':'https://www.vhannibal.net/'})
   v=urllib.request.urlopen(req,timeout=120).read();assert SHA(v)==digest,(url,SHA(v),digest);path.write_bytes(v);return v
  except Exception:
   if attempt==2:raise

def render(arg):
 source_digest,raw=arg
 spec=importlib.util.spec_from_file_location('frozen_v9',OUT/'renderer.py');mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
 src=Image.open(io.BytesIO(raw)).convert('RGBA');assert src.size==(220,132)and src.getchannel('A').getbbox()
 fitted,scale,bbox=mod.fit_logo(src);variants={'transparent':fitted};qc={}
 for style in('black','white'):
  master=Image.open(OUT/(style+'-sablona.png')).convert('RGBA');result=mod.classify_and_render(fitted,master,style);variants[style]=result.image;qc[style]={'status':result.status,'reason':result.reason,'changed_pixels':result.changed_pixels,'protected_pixels':result.protected_pixels}
 directory=OUT/'assets'/source_digest;directory.mkdir(parents=True,exist_ok=True);hashes={}
 for size in((50,30),(220,132),(400,240)):
  for style,im in variants.items():
   im=im.copy()if size==im.size else im.convert('RGBa').resize(size,Image.Resampling.LANCZOS).convert('RGBA');path=directory/(f'{size[0]}x{size[1]}-{style}.png');im.save(path)
   with Image.open(path)as check:check.load();assert check.size==size and check.getchannel('A').getbbox()
   hashes[path.name]=SHA(path.read_bytes())
 return {'source_sha256':source_digest,'qc':qc,'outputs':hashes,'scale':scale,'source_bbox':bbox,'status':'REVIEW'if any(x['status']=='REVIEW'for x in qc.values())else'QC_PASS_OWNER_REVIEW_REQUIRED'}

def main():
 inputpath=ROOT/'repair-input.json.gz';doc=json.loads(gzip.decompress(inputpath.read_bytes()));cache=OUT/'upstream.zip';archive=get(doc['picon_source_url'],doc['picon_source_sha256'],cache)
 get(f'https://raw.githubusercontent.com/Evolution-by-Warder/PiconHub-Warder-Evolution/{PIN}/tools/rebuild_master_catalog.py','f931d3eb703021fa90d6c7934e6902cd1ecb49dd7a8e69e087072a9bf00d1722',OUT/'renderer.py')
 for style,digest in MASTER_HASH.items():get(f'https://raw.githubusercontent.com/Evolution-by-Warder/PiconHub-Warder-Evolution/e90a1fe3a2734b555f48f343284f9103530180fb/plugin/artwork/templates/picons/{style}-sablona.png',digest,OUT/(style+'-sablona.png'))
 held=[];groups={};bindings=[]
 with zipfile.ZipFile(io.BytesIO(archive))as z:
  assert z.testzip()is None;members={Path(n).stem:n for n in z.namelist()if n.endswith('.png')}
  for row in doc['rows']:
   if not(row['frame_deviation']or row['source_changed']or row['status']!='COVERED_9_VALID'):continue
   reason=None;r=row['reference'];name=row['name']or'';typ=int(r.split('_')[2],16)
   assert typ not in(2,10),'radio mutation forbidden'
   if row['canonical_source']:reason='PROTECTED_CANAL_ARTWORK_PRESERVED_REQUIRES_CANONICAL_REPAIR_APPROVAL'if row['bad_slots']else'PROTECTED_CANAL_GRAPHIC_PRESERVED'
   elif row['position']=='23.5e':reason='HOLD_INDEPENDENT_235E_CANONICAL_IDENTITY_CHECK'
   elif row['prior_hold']:reason='PRIOR_IDENTITY_OR_ARTWORK_HOLD: '+row['prior_hold']
   elif typ in(0,3,12)or not name.strip()or re.match(r'^(?:test|service|\d+$|\d+[HV] |spare|temp|feed|data|dvb-nip|dn2-|dsns|quadrille|dmd|ssu|association|ita 99|ebu \d|hs1\b|f\d{4})',name,re.I):reason='TECHNICAL_OR_UNCONFIRMED_PROGRAMME_IDENTITY'
   elif not row['source_reference']:reason='NO_UNAMBIGUOUS_ORIGINAL_PICON'
   elif row['source_empty']or row['source_size']!=[220,132]:reason='EMPTY_OR_NONSTANDARD_ORIGINAL_REQUIRES_REVIEW'
   if reason:held.append({**row,'reason':reason});continue
   raw=z.read(members[row['source_reference']]);assert SHA(raw)==row['source_sha256'];groups.setdefault(SHA(raw),raw);bindings.append(row)
 results=[]
 with concurrent.futures.ProcessPoolExecutor(max_workers=6)as pool:
  for i,result in enumerate(pool.map(render,groups.items()),1):
   results.append(result)
   if i%100==0:print('RENDERED',i,len(groups),flush=True)
 assets={x['source_sha256']:x for x in results}
 for row in bindings:row['render_status']=assets[row['source_sha256']]['status']
 summary={'status':'REVIEW_ONLY_NO_PRODUCTION_PUBLICATION','input_sha256':SHA(inputpath.read_bytes()),'production_sha':doc['production_sha'],'source_archive_sha256':doc['picon_source_sha256'],'master_sha256':MASTER_HASH,'unique_artworks':len(results),'candidate_pngs':sum(len(x['outputs'])for x in results),'candidate_references':len(bindings),'qc_pass_references':sum(x['render_status']=='QC_PASS_OWNER_REVIEW_REQUIRED'for x in bindings),'qc_review_references':sum(x['render_status']=='REVIEW'for x in bindings),'held_references':len(held),'canonical_packages_changed':0,'radio_pngs_changed':0,'owner_approval_required':True}
 for style,digest in MASTER_HASH.items():assert SHA((OUT/(style+'-sablona.png')).read_bytes())==digest
 report={'summary':summary,'assets':results,'bindings':bindings,'held':held};(OUT/'candidate-index.json.gz').write_bytes(gzip.compress(json.dumps(report,separators=(',',':')).encode(),mtime=0));(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 with zipfile.ZipFile(OUT/'v9-review-assets.zip','w',compression=zipfile.ZIP_STORED)as z:
  for path in sorted((OUT/'assets').glob('*/*.png')):z.write(path,path.relative_to(OUT))
  z.write(OUT/'candidate-index.json.gz','candidate-index.json.gz');assert z.testzip()is None
 sample=[]
 for x in results:
  names=sorted({r['name']for r in bindings if r['source_sha256']==x['source_sha256']});sample.append((x,names))
 for start in range(0,len(sample),20):
  page=sample[start:start+20];canvas=Image.new('RGB',(720,160*len(page)),(120,120,120));draw=ImageDraw.Draw(canvas)
  for i,(x,names)in enumerate(page):
   draw.text((4,i*160+3),' / '.join(names)[:100]+' ['+x['status']+']',fill='white')
   for j,style in enumerate(('transparent','white','black')):
    im=Image.open(OUT/'assets'/x['source_sha256']/('220x132-'+style+'.png')).convert('RGBA');canvas.paste(im,(j*240+10,i*160+24),im)
  canvas.save(OUT/f'review-sheet-{start//20+1:03d}.png')
 summary['asset_zip_sha256']=SHA((OUT/'v9-review-assets.zip').read_bytes());summary['asset_zip_bytes']=(OUT/'v9-review-assets.zip').stat().st_size;(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
