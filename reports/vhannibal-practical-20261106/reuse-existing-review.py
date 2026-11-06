"""Select and inspect existing PR47 PNGs without re-rendering any image."""
from pathlib import Path
import gzip,json,zipfile,hashlib,io,numpy as np
from PIL import Image,ImageDraw,ImageFont
B=Path('existing-review');O=Path('existing-review-batches');O.mkdir(exist_ok=True)
archives=list(B.rglob('v9-review-assets.zip'));assert len(archives)==1
z=zipfile.ZipFile(archives[0]);assert hashlib.sha256(archives[0].read_bytes()).hexdigest()=='a052bff2326580b12dbf1f87bfee38cf2ce796e5730d5b701a7598d4c67cc9e5'
idx=json.loads(gzip.decompress(z.read('candidate-index.json.gz')));names={r['source_sha256']:[]for r in idx['assets']}
for row in idx['bindings']:names[row['source_sha256']].append(row['name'])
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',11);metrics=[];sheets=[];pack=0;packbytes=0;bundle=None
try:
 for ai,a in enumerate(idx['assets']):
  if bundle is None:bundle=zipfile.ZipFile(O/f'existing-native-{pack:02d}.zip','w',compression=zipfile.ZIP_STORED)
  group={};monochrome=False
  for size in('50x30','220x132'):
   for style in('transparent','white','black'):
    name=f'assets/{a["source_sha256"]}/{size}-{style}.png';v=z.read(name);assert hashlib.sha256(v).hexdigest()==a['outputs'][f'{size}-{style}.png'];bundle.writestr(name,v);packbytes+=len(v)
    im=Image.open(io.BytesIO(v)).convert('RGBA');im.load();group[size+'-'+style]=im
  tr=np.array(group['220x132-transparent']);solid=tr[:,:,3]>=192;rgb=tr[:,:,:3][solid];chroma=(rgb.max(axis=1).astype(int)-rgb.min(axis=1).astype(int))if len(rgb)else np.array([])
  monochrome=bool(len(rgb)>0 and np.mean(chroma<=18)>=.985)
  # This is a triage metric only. It never promotes a REVIEW graphic to PASS.
  metrics.append({'source_sha256':a['source_sha256'],'names':sorted(set(names[a['source_sha256']])),'prior_status':a['status'],'neutral_artwork':monochrome,'solid_pixels':int(solid.sum()),'neutral_fraction':float(np.mean(chroma<=18))if len(chroma)else 0})
  sheets.append((a,group))
  if len(sheets)==24 or ai==len(idx['assets'])-1:
   canvas=Image.new('RGB',(1120,100*len(sheets)),(128,128,128));d=ImageDraw.Draw(canvas)
   for i,(art,g)in enumerate(sheets):
    label=str(ai-len(sheets)+i+2)+' '+', '.join(sorted(set(names[art['source_sha256']])));d.text((4,i*100+2),label[:160],font=font,fill='white')
    for j,style in enumerate(('transparent','white','black')):
     im=g['220x132-'+style];im=im.resize((110,66),Image.Resampling.LANCZOS);canvas.paste(im,(j*370+5,i*100+22),im);small=g['50x30-'+style];canvas.paste(small,(j*370+125,i*100+40),small)
   page=(ai//24)+1;canvas.save(O/f'contact-{page:03d}.png');sheets=[]
  if packbytes>300*1024*1024:bundle.close();bundle=None;pack+=1;packbytes=0
finally:
 if bundle is not None:bundle.close()
(O/'native-triage.json.gz').write_bytes(gzip.compress(json.dumps(metrics,separators=(',',':')).encode(),mtime=0));(O/'summary.json').write_text(json.dumps({'source_run':42206982364,'source_artifact':13498420081,'existing_graphic_groups':len(idx['assets']),'existing_pngs_selected':6*len(idx['assets']),'regenerated_pngs':0,'native_bundles':len(list(O.glob('*.zip'))),'contact_sheets':len(list(O.glob('contact-*.png'))),'neutral_groups':sum(x['neutral_artwork']for x in metrics),'approval':'TRIAGE_ONLY_NO_REVIEW_PROMOTED'},indent=2))
print((O/'summary.json').read_text())
