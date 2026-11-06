from pathlib import Path
import json,gzip,collections,csv
O=Path('audit-output');M=json.load(open('manifest.json'));PROVIDERS={'ANTIKSAT','DIGI_TELLY','FREESAT','SKYLINK','CANALPLUS_SK','CANALPLUS_CZ','DVB-T-SK-CZ'};V={(s,f)for s in('50x30','220x132','400x240')for f in('channel-transparent','channel-white','channel-black')};index={};globalidx=collections.defaultdict(list);position_selectors={p['warder_key']:p['selector_id']for p in M['packages']if p['selector_id']not in PROVIDERS};summaries=[]
for path in (O/'packages').glob('*.gz'):
 doc=json.loads(gzip.decompress(path.read_bytes()));p=doc['summary'];summaries.append(p);key=p['selector_id'];slot=(p['resolution'],p['family']);bad={x['member']for x in p['issues']}
 for row in doc['rows']:
  if row['reference']:
   row={**row,'selector':key,'resolution':p['resolution'],'family':p['family'],'package':p['filename'],'issue':row['member']in bad};index[(key,*slot,row['reference'])]=row;globalidx[row['reference']].append(row)
services=json.loads(gzip.decompress((O/'services.json.gz').read_bytes()));metadata={}
for r,rs in services.items():
 fresh=[x for x in rs if x['settings_source'].startswith('official-')and x['position']and x['service_type']not in(2,10)]
 if fresh:metadata[r]=sorted(fresh,key=lambda x:(x['settings_source']!='official-5.zip',x['settings_source']))[0]
led={x['reference']:x for x in json.loads(gzip.decompress((O/'source-reference-ledger.json.gz').read_bytes()))};historic=[]
base=Path('piconhub/plugin/artwork/provenance/vhannibal')
for p in [base/'import-report.tsv',base/'motor13-incremental/import-report.tsv.gz',base/'motor18oct-incremental/import-report.tsv.gz']:
 text=gzip.decompress(p.read_bytes()).decode()if p.suffix=='.gz'else p.read_text();items=list(csv.DictReader(text.splitlines(),delimiter='\t'));refs=set()
 for row in items:
  f=Path(row['filename']).stem.split('_')
  try:r='_'.join(f'{int(x,16):X}'for x in f)if len(f)==10 else None
  except ValueError:r=None
  if r:
   refs.add(r)
   if r not in led:led[r]={'reference':r,'scope':'HISTORICAL_REPORT_ONLY','historic_report_sources':[]}
   led[r].setdefault('historic_report_sources',[]).append(str(p))
 historic.append({'report':str(p),'rows':len(items),'valid_unique_refs':len(refs),'original_archive_retrieved':False})
allrefs=set(led)|set(metadata);rows=[]
for r in sorted(allrefs):
 x=led.get(r,{});meta=metadata.get(r);sel=position_selectors.get(meta['position'])if meta else None;slots={slot for slot in V if (sel,*slot,r)in index};bad=[f'{s}|{f}'for s,f in slots if index[(sel,s,f,r)]['issue']];missing=sorted(f'{s}|{f}'for s,f in V-slots)if meta else[]
 status=('COVERED_9_VALID'if len(slots)==9 and not bad else'EMPTY_OR_INVALID_PNG'if bad else'MISSING_VARIANTS')if meta else x.get('scope','UNKNOWN')
 rows.append({'reference':r,'name':meta['name']if meta else x.get('service',{}).get('name'),'provider':meta['provider']if meta else x.get('service',{}).get('provider'),'position':meta['position']if meta else x.get('service',{}).get('position'),'selector':sel,'scope':x.get('scope','SETTINGS_ONLY_NO_SOURCE_PNG'),'current_satellite_nonradio':meta is not None,'status':status,'present_slots':len(slots),'missing_slots':missing,'bad_slots':bad,'existing_selectors':sorted({p['selector']for p in globalidx.get(r,[])}),'source_png':r in led and x.get('sha256')is not None,'original_pixel_digest':x.get('rgba_sha256'),'historic_reports':x.get('historic_report_sources',[]),'current_settings_source':meta['settings_source']if meta else None})
summary={'packages_scanned':len(summaries),'packages_expected':len(M['packages']),'png_entries_scanned':sum(x['png_count']for x in summaries),'source_and_settings_reference_union':len(allrefs),'historical_reports':historic,'reference_status_counts':dict(collections.Counter(x['status']for x in rows)),'current_satellite_nonradio_references':len(metadata),'current_status_counts':dict(collections.Counter(x['status']for x in rows if x['current_satellite_nonradio'])),'png_issues':[{'package':x['filename'],'issues':x['issues']}for x in summaries if x['issues']]}
(O/'joined-reference-ledger.json.gz').write_bytes(gzip.compress(json.dumps(rows,separators=(',',':')).encode(),mtime=0));(O/'joined-summary.json').write_text(json.dumps(summary,indent=2));print({k:v for k,v in summary.items()if k not in('png_issues','historical_reports')});print('FIRST MISSING')
for x in [r for r in rows if r['current_satellite_nonradio']and r['status']!='COVERED_9_VALID'][:40]:print(x['reference'],x['name'],x['position'],x['present_slots'],x['bad_slots'])
