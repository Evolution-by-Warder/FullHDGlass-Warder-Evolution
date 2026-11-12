import json,copy,zipfile,io,hashlib,urllib.request,struct,zlib
from pathlib import Path
from PIL import Image
B=Path(__file__).parent; O=B/'out'; H='975f3acf96fce0db7307388cbf5e171b0f315fa7'; P='assets/warder/downloads/picons/channels/'; R='reports/vhannibal-followup-20261106/catalog-batch-20261112-20/'
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,b):
 f=O/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b)
def get(p):return urllib.request.urlopen('https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/'+H+'/'+p,timeout=60).read()
m=json.loads((B/'manifest.json').read_text());base=copy.deepcopy(m)
a=[dict(name='Женский Журнал',reference='1_0_16_4AB1_13_70_1680000_0_0_0',sid=19121,donor_selector='549E',donor='1_0_16_D944_22C_70_2250000_0_0_0'),dict(name='В гостях у сказки',reference='1_0_16_4AB3_13_70_1680000_0_0_0',sid=19123,donor_selector='515E',donor='1_0_16_865_2_FF00_2032C1A_0_0_0')]
results=[];pngs=[]
for p in m['packages']:
 if p['selector_id']!='360E':continue
 raw=(B/p['filename']).read_bytes();assert sha(raw)==p['sha256'];before=zipfile.ZipFile(io.BytesIO(raw));assert before.testzip()is None
 buf=io.BytesIO(raw);buf.seek(0,2);old=copy.deepcopy(p)
 with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_DEFLATED)as z:
  z.filelist=copy.deepcopy(before.infolist());z.NameToInfo={i.filename:i for i in z.filelist};z.comment=before.comment
  for x in a:
   donor=next(d for d in m['packages']if d['selector_id']==x['donor_selector'] and d['resolution']==p['resolution'] and d['family']==p['family']);db=(B/donor['filename']).read_bytes();assert sha(db)==donor['sha256'];png=zipfile.ZipFile(io.BytesIO(db)).read(x['donor']+'.png');im=Image.open(io.BytesIO(png));im.load();assert im.size==tuple(map(int,p['resolution'].split('x')))and im.mode=='RGBA';im.verify() if False else None
   off=8
   while off<len(png):
    n=struct.unpack('>I',png[off:off+4])[0];assert zlib.crc32(png[off+4:off+8+n])&0xffffffff==struct.unpack('>I',png[off+8+n:off+12+n])[0];off+=12+n
   assert x['reference']+'.png'not in before.namelist();info=zipfile.ZipInfo(x['reference']+'.png',(2026,11,12,12,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,png)
   path=R+'png/'+p['resolution']+'/'+p['family']+'/'+x['reference']+'.png';save(path,png);pngs.append(dict(path=path,sha256=sha(png),bytes=len(png),reference=x['reference'],donor=x['donor'],donor_package=donor['filename'],resolution=p['resolution'],family=p['family'],alpha=list(im.getchannel('A').getextrema())))
 new=buf.getvalue();assert new[:len(raw)]==raw;after=zipfile.ZipFile(io.BytesIO(new));assert after.testzip()is None and len(after.namelist())==len(before.namelist())+2
 for n in before.namelist():assert before.read(n)==after.read(n)
 digest=sha(new);name='warder-360e-'+p['resolution']+'-'+p['family'].removeprefix('channel-')+'-'+digest[:16]+'.zip';tailname=name+'.part%02d'%len(p['parts']);tail=new[len(raw):];assert len(tail)<32*1024*1024
 save(P+tailname,tail);m['parts'].append(dict(filename=tailname,sha256=sha(tail),bytes=len(tail)))
 p.update(filename=name,sha256=digest,bytes=len(new),png_count=p['png_count']+2,parts=p['parts']+['https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/'+P+tailname]);p['catalog_batch20']={'added':2,'preserved':len(before.namelist()),'base_sha256':old['sha256'],'source_checkpoint':H}
 (B/'zips').mkdir(exist_ok=True);(B/'zips'/name).write_bytes(new);results.append(dict(old=old,new=p,tail=tailname,tail_sha256=sha(tail),prefix_byte_identical=True,preserved_members=len(before.namelist())))
assert len(pngs)==18 and len(results)==9
protected=[p for p in base['packages']if p['selector_id']in['CANALPLUS_CZ','CANALPLUS_SK']];assert len(protected)==18
for p in base['packages']:
 if p['selector_id']!='360E':assert p in m['packages']
m['catalog_batch20']={'new_references':2,'new_png':18,'changed_zip':9,'original_blocked_cases_unchanged':86,'source_checkpoint':H}
save(P+'manifest.json',(json.dumps(m,ensure_ascii=False,indent=2)+'\n').encode());save(P+'SHA256SUMS',get(P+'SHA256SUMS').rstrip()+b'\n'+''.join(r['tail_sha256']+'  '+r['tail']+'\n'for r in results).encode())
report=dict(status='LOCAL_PASS_REMOTE_AUDIT_PENDING',base=H,batch=20,batch19='OPEN_WITH_86_HOLDS',new_tv=2,new_png=18,changed_zip=9,completed_tv_total_pending_audit=50,integrated_png_total_pending_audit=447,original_open=86,production_unchanged=True,protected_canal=18,references=a,pngs=pngs,packages=results,evidence={'lamedb_url':'https://raw.githubusercontent.com/ciefp/ciefpsettings-enigma2/master/ciefp-E2-motor-75E-34W/lamedb','lamedb_sha256':sha((B/'lamedb').read_bytes()),'tuple':'36E ONID112 TSID19 SID19121 and19123; service_type22 MPEG4SD','independent_catalog':'https://www.lyngsat.com/muxes/Eutelsat-36D_Russia_11900-R.html','catalog_snapshot':'2026-08-21; retrieved indexed full transport 2026-11-12. Direct page403. Complete ONID112/TID19 and SID-to-name rows returned by search.','operator':['https://ntvplus.ru/channel/v-gostyah-u-skazki-380','https://ntvplus.tv/channel/women-s-magazine-573'],'donors':'Existing nine-valid production graphics, zero recorded V9 deviations; byte-for-byte reuse. No render.'})
save(R+'integration.json',(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode());save(R+'build.py',Path(__file__).read_bytes());save(R+'reference-register.json',(json.dumps(a,ensure_ascii=False,indent=2)+'\n').encode())
progress=get('WARDER_PROGRESS.md');save('WARDER_PROGRESS.md',('## 2026-11-12 — Independent catalog batch20: two36E references, remote audit pending\n\nTwo new exact references outside the86blocked batch19 cases: Женский Журнал SID19121 and В гостях у сказки SID19123, TSID19/ONID112. Existing approved nine-variant donor bytes reused unchanged. Added18PNG to nine360E working ZIPs, preserving every previous ZIP byte/member and all18protectedCANAL+packages. Main/production unchanged; PR50 unmerged.\n\nPayload awaiting independent remote audit; do not mark batch20 complete yet. On PASS, totals50TV/447integratedPNG; original86open unchanged. Batch19 remains open. Report `'+R+'integration.json`. BFBS/ALKAFEEL not revisited.\n\n').encode()+progress)
(B/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('Built',len(pngs),'PNG',len(results),'ZIPs',sum(f.stat().st_size for f in O.rglob('*')if f.is_file()),'upload bytes')
