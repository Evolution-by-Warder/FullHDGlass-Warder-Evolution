"""Remove proven obsolete images and migrate old logos without erasing uncertain regional services."""
from pathlib import Path
import hashlib,io,json,zipfile
from PIL import Image
R=Path(__file__).parent;W=R.parent
load=lambda p:json.loads(p.read_text());sha=lambda b:hashlib.sha256(b).hexdigest()
legacy=load(R/'catalog/legacy-images.json');sat=load(R/'catalog/satellite-logo-candidates.json');radios=load(W/'iptv-radio-skcz/catalog/preview-review.json')['records'];index=load(R/'catalog/delta-index.json');z=zipfile.ZipFile(R/'delta.zip');delta={n:z.read(n) for n in z.namelist()};z.close();baseline=zipfile.ZipFile(R/'assets/baseline-transparent.zip')
ended={
0:('Generic historical test card','technical-placeholder','No station identity; real named replacements take priority'),
5:('NASA TV UHD','closed','https://www.nasa.gov/news-release/nasa-accelerates-space-exploration-earth-science-for-all-in-2024/'),
19:('Sport 5','closed','https://www.lupa.cz/aktuality/operatori-vyrazuji-z-nabidek-stanici-sport-5/'),
27:('O2 TV Free','closed','https://www2.mediaguru.cz/pozemni-vysilani-muze-byt-resenim-pro-streamovany-sport'),
29:('ČT3','closed','https://www.ceskatelevize.cz/tv-program/01.01.2023/'),
39:('Barrandov News','closed','https://digital.rozhlas.cz/televizni-stanice-barrandov-news-definitivne-ukoncila-vysilani-nekolikrat-8373104'),
46:('Naživo','closed','https://www.lupa.cz/aktuality/kulturni-televize-nazivo-definitivne-skoncila-jeji-licence-zanikla/'),
50:('Family Barrandov','former-name-of-closed-channel','https://digital.rozhlas.cz/televizni-stanice-barrandov-news-definitivne-ukoncila-vysilani-nekolikrat-8373104'),
144:('Rádio Pyramída','closed','https://www.stvr.org/media/a542/file/item/sk/0002/programovy_koncept_stvr_2025.WEZw.pdf'),
148:('Sporty TV','replaced-by-Prima-Sport','https://www.skupinaprima.cz/skupina-prima-spousti-novy-sportovni-kanal-prima-sport-divakum-nabidne-spickove-svetove-i-domaci-prenosy/'),
158:('TUTY TV','closed','https://ktkdigi.cz/aktualni-informace/ukonceni-kanalu-tuty-tv/'),
189:('Paramount Network CZ','closed','https://www.ceskenoviny.cz/zpravy/paramount-prestane-v-cr-vysilat-paramount-network-a-vetsinu-kanalu-mtv-a-nick/2763708')}
# Changes of branding apply to all aliases of that logo, not only the latest measured tuple.
radio_migrations={7:'Rádio Slovensko',11:'Rádio Regina Východ',31:'Rádio_FM',33:'Radio Proglas',42:'Rádio Čas Rock (192 kbps)',44:'Rádio Dechovka 256 kbps',57:'Rádio Čas Rock (192 kbps)',62:'Český rozhlas Dvojka',68:'Impuls Ráááádio',71:'Radiožurnál Sport',76:'Rádio Patria',77:'Rádio Regina Stred',94:'Rádio Regina Západ',114:'Český rozhlas Plus',115:'Český rozhlas Radiožurnál',127:'Český rozhlas Radio Wave',135:'Český rozhlas Rádio Junior',140:'Český rozhlas Jazz',145:'Rádio Litera',179:'Rádio Devín',190:'Rádio Junior',191:'Český rozhlas Vltava',197:'Radio Čas',198:'Radio Slovakia International',201:'Český rozhlas D-dur'}
sat_migrations={112:734,175:644};migrations=[]
for oldid,name in radio_migrations.items():
 row=next((r for r in radios if r['name']==name),None)
 if not row:continue
 art={s:(W/'iptv-radio-skcz'/row['files']['220x132/'+s]['path']).read_bytes() for s in ('transparent','white','black')}
 for ref in legacy[oldid]['references']:
  # Current measured tuple correction (e.g. swapped Regina regions) wins over historical visual identity.
  if 'transparent/'+ref in delta:continue
  for s,b in art.items():delta[s+'/'+ref]=b
 migrations.append(dict(legacy_image_id=oldid,current_identity=name,reference_files=len(legacy[oldid]['references']),source='approved-iptv-sk-cz-artwork'))
for oldid,newid in sat_migrations.items():
 p=Path(sat[newid]['paths'][0]);art={s:(W/str(p).replace('/transparent/',f'/{s}/')).read_bytes() for s in ('transparent','white','black')}
 for ref in legacy[oldid]['references']:
  if 'transparent/'+ref in delta:continue
  for s,b in art.items():delta[s+'/'+ref]=b
 migrations.append(dict(legacy_image_id=oldid,current_artwork_path=str(p),reference_files=len(legacy[oldid]['references'])))
removed={};dispositions=[]
for oldid,(name,state,source) in ended.items():
 refs=[];replaced=[]
 for ref in legacy[oldid]['references']:
  if 'transparent/'+ref in delta:replaced.append(ref)
  else:removed[ref]=dict(identity=name,legacy_image_id=oldid,reason=state,source=source);refs.append(ref)
 dispositions.append(dict(identity=name,legacy_image_id=oldid,status=state,source=source,deleted_files=refs,updated_reused_references=replaced))
# Wrong obsolete JOJ graphics on the contemporary Infokanal tuple cannot remain as a valid station picon.
for l in legacy:
 for ref in l['references']:
  p=Path(ref).stem.split('_')
  if tuple(int(p[i],16) for i in (3,4,5))==(2001,258,8895) and 'transparent/'+ref not in delta:removed[ref]=dict(identity='Infokanal',reason='wrong-historical-JOJ-logo-on-current-information-service',source='https://plustelka.sk/technicke-informacie')
assert not set(removed)&{n.split('/')[1] for n in delta}
for n,b in delta.items():
 with Image.open(io.BytesIO(b)) as im:assert im.size==(220,132);im.verify()
allnames=(set(baseline.namelist())-set(removed))|{n.split('/')[1] for n in delta};assert len(allnames)==len(set(allnames))
with zipfile.ZipFile(R/'delta.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n,b in sorted(delta.items()):z.writestr(n,b)
(R/'catalog/delta-index.json').write_text(json.dumps({n:sha(b) for n,b in sorted(delta.items())},indent=2)+'\n')
(R/'catalog/removals.json').write_text(json.dumps(removed,ensure_ascii=False,indent=2)+'\n');(R/'catalog/obsolete-stations.json').write_text(json.dumps(dispositions,ensure_ascii=False,indent=2)+'\n');(R/'catalog/logo-migrations.json').write_text(json.dumps(migrations,ensure_ascii=False,indent=2)+'\n')
report=load(R/'catalog/summary.json');report.update(cleanup_requested=True,deleted_reference_files=len(removed),obsolete_image_groups=len(ended),delta_reference_files=len(delta)//3,new_reference_files=len(allnames-set(baseline.namelist())),changed_existing_reference_files=sum(n.split('/')[1] in baseline.namelist() and sha(b)!=sha(baseline.read(n.split('/')[1])) for n,b in delta.items() if n.startswith('transparent/')),final_png_files_per_variant=len(allnames),warning='Closed programmes and obsolete logos are removed or replaced. Uncertain regional services remain visibly pending rather than being falsely claimed closed.')
(R/'catalog/summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');station=load(R/'catalog/station-list.json');station['summary']=report
for row in station['stations']:
 if row['name']=='Paramount Network':row['artwork_status']='removed-confirmed-closed';row['broadcast_confirmation']='confirmed-closed-stale-measurement';row['authority_url']=ended[189][2]
station['retired_programmes']=dispositions;(R/'catalog/station-list.json').write_text(json.dumps(station,ensure_ascii=False,indent=2)+'\n')
# Split the transfer payload; GitHub blob requests stay comfortably below 16 MiB.
raw=(R/'delta.zip').read_bytes();parts=[]
for i,o in enumerate(range(0,len(raw),6*1024*1024)):
 b=raw[o:o+6*1024*1024];p=R/f'delta.zip.part{i:02d}';p.write_bytes(b);parts.append(dict(filename=p.name,bytes=len(b),sha256=sha(b)))
(R/'catalog/delta-payload.json').write_text(json.dumps(dict(bytes=len(raw),sha256=sha(raw),parts=parts),indent=2)+'\n');print(json.dumps(report,indent=2));print('delta_bytes',len(raw))
