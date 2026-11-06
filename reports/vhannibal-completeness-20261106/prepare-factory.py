from pathlib import Path
import json,gzip,collections,hashlib
O=Path('audit-output');rows=json.loads(gzip.decompress((O/'joined-reference-ledger.json.gz').read_bytes()));source={x['reference']:x for x in json.loads(gzip.decompress((O/'source-reference-ledger.json.gz').read_bytes()))};plans={x['reference']:x for x in json.load(open('plans.json'))};masters={};sourcecurrent={x['reference']:x for x in json.loads(gzip.decompress((O/'official-1.zip.picons.json.gz').read_bytes()))if x['reference']};byuid=collections.defaultdict(list)
for r,x in sourcecurrent.items():byuid[tuple(r.split('_')[3:7])].append(x)
for path in (O/'master').glob('*.gz'):
 d=json.loads(gzip.decompress(path.read_bytes()))
 for r in d['rows']:
  if not r['v9_outer_edge_exact']:masters.setdefault(r['reference'],set()).add(d['selector'])
exceptions={x['reference']:x.get('hold_reason')for x in json.load(open('audit-cache/exceptions.json'))};candidate=[]
changed=set(json.load(open(O/'source-summary.json'))['same_ref_changed_pixels'])
for row in rows:
 if not row['current_satellite_nonradio']:continue
 r=row['reference'];x=sourcecurrent.get(r);uid=byuid.get(tuple(r.split('_')[3:7]),[])
 if not x and len(uid)==1:x=uid[0]
 p=plans.get(r,{})
 candidate.append({**{k:row[k]for k in ('reference','name','provider','position','selector','status','missing_slots','bad_slots')},'source_reference':x['reference']if x else None,'source_sha256':x['sha256']if x else None,'source_empty':x.get('empty')if x else None,'source_size':x.get('size')if x else None,'source_changed':r in changed,'frame_deviation':row['selector']in masters.get(r,set()),'prior_hold':exceptions.get(r)if r not in plans else None,'canonical_source':p.get('canal_source_reference')})
doc={'schema':1,'production_sha':'603218ea8fa51176f686f14f303509a4c64dc7e1','picon_source_url':'https://www.vhannibal.net/download_setting.php?action=download&id=1','picon_source_sha256':'011f4f931088e6a3a6be1e4fe69a22b1909caf522384de371d27cc64b7dbd052','rows':candidate};raw=gzip.compress(json.dumps(doc,separators=(',',':')).encode(),mtime=0);Path('audit-output/repair-input.json.gz').write_bytes(raw);print('input',len(candidate),'bytes',len(raw))
