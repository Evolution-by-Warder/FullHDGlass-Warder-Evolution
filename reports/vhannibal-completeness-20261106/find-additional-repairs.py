from pathlib import Path
import json,gzip,collections,re
O=Path('audit-output');rows=json.loads(gzip.decompress((O/'joined-reference-ledger.json.gz').read_bytes()));plans={x['reference']:x for x in json.load(open('plans.json'))};allsource={x['reference']:x for x in json.loads(gzip.decompress((O/'source-reference-ledger.json.gz').read_bytes()))};current={x['reference']:x for x in json.loads(gzip.decompress((O/'official-1.zip.picons.json.gz').read_bytes()))if x['reference']};old={}
for p in O.glob('PICON*.picons.json.gz'):
 for x in json.loads(gzip.decompress(p.read_bytes())):
  if x['reference']:old[x['reference']]=x
pixels=collections.defaultdict(set)
for d in json.load(open('audit-cache/source-dispositions.json')):
 src=d.get('source_reference');target=d.get('current_reference')
 if src in old and target in plans:pixels[old[src]['rgba_sha256']].add(target)
byuid=collections.defaultdict(list)
for r,x in current.items():byuid[tuple(r.split('_')[3:7])].append(x)
existing={x['reference']for x in json.load(open('audit-output/new-reference-reuse-candidates.json'))};extra=[]
for row in rows:
 if row['status']not in('MISSING_VARIANTS','EMPTY_OR_INVALID_PNG')or row['reference']in existing or not row['name']:continue
 r=row['reference'];source=current.get(r)or old.get(r);options=byuid.get(tuple(r.split('_')[3:7]),[])
 if not source and len({x['rgba_sha256']for x in options})==1 and options:source=options[0]
 if not source:continue
 matches=sorted(pixels.get(source['rgba_sha256'],[]))
 if not matches:continue
 print(r,row['name'],row['present_slots'],'=>',[(s,plans[s]['name'],plans[s].get('canal_source_reference'))for s in matches][:8])
 extra.append({'reference':r,'scope':'SATELLITE_TV','names':[row['name']],'pixel_exact_prior_refs':matches,'prior_names':sorted({plans[x]['name']for x in matches}),'source_reference':source['reference'],'original_pixel_digest':source['rgba_sha256']})
(O/'additional-reuse-candidates.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2))
