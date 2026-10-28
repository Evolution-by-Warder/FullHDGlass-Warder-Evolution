"""Curate measured terrestrial identities without guessing unknown SDT identities."""
import csv,hashlib,io,json,re,zipfile
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent; W=R.parent
load=lambda p:json.loads(p.read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
legacy=load(R/'catalog/legacy-images.json');sat=load(R/'catalog/satellite-logo-candidates.json');rows=load(R/'catalog/measured-comparison.json')
radio=load(W/'iptv-radio-skcz/catalog/preview-review.json')['records']
frames={s:Image.open(W/'iptv-radio-skcz/templates'/f'{s}-sablona.png').convert('RGBA') for s in ('white','black')}
# Exact approved artwork identities, visually reviewed against contact sheets.
S={'Sport 1 SK HD HEVC':415,'Sport 2 HD HEVC':376,'JOJ Sport HD HEVC':455,'JOJ Sport2 HD HEVC':681,'JOJ Svet HEVC':420,'JOJ KRIMI':644,'Prima LOVE SK HD':367,'Markiza Klasik HEVC':289,'Markiza Krimi HEVC':716,'VIXEN HEVC':578,'Doma':734,'Prima Cool SK':181}
L={'Eurosport 1 HD':186,'Eurosport 2 HD':55,'Film+ HD':51,'Slagr Original':116,'CS Mystery':184,'JOJ Family':151,'Televize pres antenu':78,'Praha TV':156,'Seznam.cz TV':14,'Prima SHOW':30,'Prima STAR':70,'Nova Gold':43,'TV Noe HD':153,'Tv NOE':153,'Noe TV':153,'TV Poprad':180,'Kezmarska Televizia':149,'TV Reduta':170,'TA3':122}
RAD={'Cesky Impuls':'Český Impuls','Radio Cas':'Radio Čas','Radio Cas Rock':'Rádio Čas Rock (192 kbps)'}
# Primary source confirms national programme presence; raw SDT names are retained separately.
PL='https://plustelka.sk/technicke-informacie'; CRA='https://www.digistranky.cz/naladte-si/programova-nabidka'; M24='https://www.multiplex24.cz/images/document/20260103-l7RIZWTQ.pdf'
RENAMES={'Nova Gold':'Nova Krimi','RTVS 24 HD':'STVR 24 HD','RTVS Sport HD HEVC':'STVR Šport HD HEVC'}
SK_RAD=[('Rádio Slovensko',1020,7),('Rádio Regina Západ',1021,None),('Rádio Regina Stred',1022,None),('Rádio Regina Východ',1023,None),('Rádio Devín',1024,None),('Rádio_FM',1025,31),('Rádio Patria',1026,76),('Rádio Patria',1027,76),('Radio Slovakia International',1028,198),('Rádio Litera',1031,145),('Rádio Junior',1032,190)]
for name,sid,lid in SK_RAD:
 rows.append(dict(country='SK',scope='national',multiplex='MUX 1 radio',name=name,sid=sid,tsid=257,onid=8895,kind='Radio',programme_url='https://www.radia.sk/frekvencie',reference_evidence='Existing legacy receiver tuple; cached measurement corroboration for 1020-1023,1028,1032. Not a new receiver scan.',has_legacy_tuple=True))
def tupleof(name):
 p=Path(name).stem.split('_');return tuple(int(p[i],16) for i in (3,4,5))
def canon(r,stype=None):return f"1_0_{stype or ('2' if isradio(r) else '1')}_{r['sid']:X}_{r['tsid']:X}_{r['onid']:X}_EEEE0000_0_0_0.png"
def isradio(r):return 'radio' in r['kind'].lower() or 'rádio' in r['kind'].lower() or r['name'].startswith('Rock Zone') or r['name'].startswith('CRo ')
def compose(raw):
 im=Image.open(io.BytesIO(raw)).convert('RGBA');assert im.size==(220,132);bb=im.getbbox();assert bb
 logo=im.crop(bb);logo.thumbnail((192,104),Image.Resampling.LANCZOS);out={'transparent':raw}
 for s,frame in frames.items():
  im=frame.copy();im.alpha_composite(logo,((220-logo.width)//2,(132-logo.height)//2));b=io.BytesIO();im.save(b,format='PNG',compress_level=9);out[s]=b.getvalue()
 return out
legacy_by_tuple={}
for l in legacy:
 for f in l['references']:legacy_by_tuple.setdefault(tupleof(f),[]).append((l['id'],f))
base=zipfile.ZipFile(R/'assets/baseline-transparent.zip');delta={};curated=[];seen=set()
for r in rows:
 t=(r['sid'],r['tsid'],r['onid']);refs=legacy_by_tuple.get(t,[]);oldids=sorted({i for i,f in refs});n=r['name'];specific=False;art=None;origin=None
 if re.match(r'^(Service [1-5]|Test-[12]|Regio \|)',n):status='technical-placeholder-no-station-logo'
 elif n=='TV Doktor HD' and r['sid']==1000:status='conflicting-regional-identity-needs-verification'
 elif n in S:
  p=Path(next((p for p in sat[S[n]]['paths'] if '/canal-plus-sk/' in p),sat[S[n]]['paths'][0])); art={s:(W/str(p).replace('/transparent/',f'/{s}/')).read_bytes() for s in ('transparent','white','black')};origin=str(p);specific=True;status='mapped'
 elif n in RAD or n in [v[0] for v in SK_RAD]:
  target=RAD.get(n,n);rr=next((x for x in radio if x['country']==r['country'] and x['name']==target),None)
  if rr:art={s:(W/'iptv-radio-skcz'/rr['files']['220x132/'+s]['path']).read_bytes() for s in ('transparent','white','black')};origin='Approved IPTV SK/CZ: '+target;specific=True;status='mapped'
  elif refs and any(i!=0 for i,f in refs):status='mapped-existing';origin='legacy:'+str(next(i for i,f in refs if i!=0))
  else:status='missing-approved-artwork'
 elif n in L:art=compose((R/legacy[L[n]]['path']).read_bytes());origin='legacy:'+str(L[n]);specific=n in ('Nova Gold','Seznam.cz TV','Prima SHOW','Prima STAR');status='mapped'
 elif n in ('Kanal 1 HD','CRo POHODA T2','UKRAJINSKE RADIO','RIK','Nickelodeon','MusicBox Classic HD HEVC'):
  path=R/'assets/official'/({'Kanal 1 HD':'kanal1','CRo POHODA T2':'pohoda','UKRAJINSKE RADIO':'ukrajinske-radio','RIK':'rik','Nickelodeon':'nickelodeon','MusicBox Classic HD HEVC':'musicbox-classic'}[n]+'.png')
  if path.exists():art=compose(path.read_bytes());origin='official-operator-artwork:'+path.name;specific=True;status='mapped'
  else:status='missing-approved-artwork'
 elif n=='4ka Infokanal':status='legacy-artwork-needs-brand-verification'
 elif refs and any(i!=0 for i,f in refs):status='mapped-existing';origin='legacy:'+str(next(i for i,f in refs if i!=0))
 else:status='missing-approved-artwork'
 if r['country']=='SK' and r['scope']=='national':authority=PL if 'radio' not in r['multiplex'] else 'https://www.radia.sk/frekvencie';confirmation='operator-confirmed' if not n.startswith('RTVS ') else 'stale-measurement-only'
 elif r['country']=='CZ' and r['multiplex']!='MUX 24':authority=CRA;confirmation='operator-confirmed' if n not in ('Hit TV','Test-1','Test-2') else 'measurement-only'
 elif r['country']=='CZ':authority=M24;confirmation='operator-confirmed' if n not in ('Paramount Network','Info TV Brno a Jizni Morava') and not n.startswith('Regio ') else 'measurement-only'
 else:authority=r['multiplex_url'];confirmation='measurement-only-regional'
 # Current aliases present in primary operator are safe. Regional measurements remain visibly separate.
 r.update(display_name=RENAMES.get(n,n),authority_url=authority,broadcast_confirmation=confirmation,legacy_image_ids=oldids,artwork_status=status,artwork_source=origin,canonical_filename=canon(r),receiver_reference_policy='TV type 1 and EEEE0000 are documented renderer fallback aliases; codec does not determine actual SDT service type.')
 targets=[canon(r)] + ([canon(r,'1')] if isradio(r) else [])
 if specific:targets+= [f for i,f in refs]
 if art:
  for name in set(targets):
   if name in base.namelist() and not specific:continue
   for s,png in art.items():
    im=Image.open(io.BytesIO(png));assert im.size==(220,132);im.verify();delta[s+'/'+name]=png
  r['artwork_status']='covered-by-curated-delta';r['delta_targets']=sorted(set(targets));curated.append({k:r[k] for k in ('country','name','display_name','sid','tsid','onid','artwork_source','delta_targets')})
 elif status=='mapped-existing' and canon(r) not in base.namelist():
  i=next(i for i,f in refs if i!=0);art=compose((R/legacy[i]['path']).read_bytes())
  for s,png in art.items():delta[s+'/'+canon(r)]=png
  r['artwork_status']='covered-by-curated-delta';r['delta_targets']=[canon(r)];curated.append({k:r[k] for k in ('country','name','display_name','sid','tsid','onid','artwork_source','delta_targets')})
# Explicit operator additions without a verified triple are never assigned an invented reference.
for country,mux,n,url in [('CZ','MUX 24','Prima Sport','https://www.multiplex24.cz/detail-aktuality/novy-televizni-program-prima-sport-od-17-srpna-2026'),('CZ','MUX 24','Šláger Muzika',M24),('CZ','Regional 12/8','NOE+',CRA),('CZ','Regional 4/8','TV Brno 1',CRA)]+[('CZ','MUX 24 regional',n,M24) for n in ['POLAR HD','TVS','LTV Plus','TV V1','ZAK TV','JTV','rtm plus Liberecko','TV Morava','Praha TV','TV Brno 1','i-Vysočina','Ústecká TV']]+[('CZ','Regional 12/8',n,CRA) for n in ['Óčko Black','Óčko Expres']]:
 rows.append(dict(country=country,scope='regional' if mux.startswith('Regional') else 'national',multiplex=mux,name=n,display_name=n,authority_url=url,broadcast_confirmation='operator-confirmed',artwork_status='needs-current-terrestrial-reference',sid=None,tsid=None,onid=None))
# Art reused at multiple transmitters is one station identity, not a new station per filename.
identities={(r['country'],r['display_name']) for r in rows if not r['artwork_status'].startswith('technical-')}
report=dict(schema=1,date='2026-10-28',measured_service_tuples=198,sk_radio_legacy_reference_rows=11,additional_operator_entries_without_reference=sum(r.get('sid') is None for r in rows),rows=len(rows),distinct_named_identities_including_unconfirmed=len(identities),historical_png_files=2674,historical_distinct_images=203,delta_reference_files=len(delta)//3,curated_service_rows=len(curated),new_reference_files=len({k.split('/')[1] for k in delta}-set(base.namelist())),changed_existing_reference_files=sum(1 for k,v in delta.items() if k.startswith('transparent/') and k.split('/')[1] in base.namelist() and base.read(k.split('/')[1])!=v),pending_rows=sum(r['artwork_status'] in ('missing-approved-artwork','legacy-artwork-needs-brand-verification','conflicting-regional-identity-needs-verification','needs-current-terrestrial-reference') for r in rows),warning='This is an operator/measurement audit, not a physical nationwide receiver scan. Regional measurement-only entries and missing references are explicitly labelled. Historical filenames are preserved. No logo is invented.')
(R/'catalog/station-list.json').write_text(json.dumps({'summary':report,'stations':rows},ensure_ascii=False,indent=2)+'\n')
with (R/'catalog/station-list.csv').open('w') as f:
 fields=['country','multiplex','display_name','sid','tsid','onid','artwork_status','broadcast_confirmation','artwork_source','canonical_filename','authority_url','programme_url'];cw=csv.DictWriter(f,fields,extrasaction='ignore');cw.writeheader();cw.writerows(rows)
(R/'catalog/delta-index.json').write_text(json.dumps({k:sha(v) for k,v in sorted(delta.items())},indent=2)+'\n');(R/'catalog/curated-mappings.json').write_text(json.dumps(curated,ensure_ascii=False,indent=2)+'\n');(R/'catalog/summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(R/'delta.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for k,v in sorted(delta.items()):z.writestr(k,v)
# Visual proof: every unique delta image in all three styles.
unique={sha(v):(k,v) for k,v in delta.items() if k.startswith('transparent/')};items=list(unique.values());sheet=Image.new('RGB',(660,len(items)*154),(29,40,56));draw=ImageDraw.Draw(sheet)
for i,(key,raw) in enumerate(items):
 for j,s in enumerate(('transparent','white','black')):
  im=Image.open(io.BytesIO(delta[s+'/'+key.split('/')[1]])).convert('RGBA');sheet.paste(im,(j*220,i*154),im)
 draw.text((3,i*154+132),key.split('/')[1],fill='white')
sheet.save(R/'assets/delta-review.png');print(json.dumps(report,indent=2));print('delta_bytes', (R/'delta.zip').stat().st_size)
