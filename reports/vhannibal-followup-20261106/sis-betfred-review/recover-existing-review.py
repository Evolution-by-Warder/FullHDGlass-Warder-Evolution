from pathlib import Path
import zipfile,gzip,json,hashlib,io,importlib.util,sys,os
from PIL import Image,ImageDraw
B=Path('bht-review');O=Path('workrepo/reports/vhannibal-followup-20261106/sis-betfred-review');O.mkdir(exist_ok=True)
SHA=lambda b:hashlib.sha256(b).hexdigest();v=json.load(gzip.open('workrepo/reports/vhannibal-completeness-20261106/v9-review-index.json.gz'));rows={r['reference']:r for r in v['bindings']};assets={r['source_sha256']:r for r in v['assets']};z=zipfile.ZipFile('existing-native/existing-native-00.zip');srcz=zipfile.ZipFile('vhannibal-source-current.zip');members={Path(n).stem:n for n in srcz.namelist()if n.endswith('.png')}
spec=importlib.util.spec_from_file_location('review_renderer',B/'renderer.py');mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
master_hashes={'white':'c6ae4a808a65ffc8e6458336fccbfe4216de1e832ec0a9abf800907f2f783589','black':'61e69f7fc46e340453bf74ccd7af6ac9d8eba9f8e232884659e1ea99f6abf3fe'}
report=[];tiles=[]
for sid,label in [('13','SIS Racing (SISSP)'),('14','BETFRED TV1'),('15','BETFRED TV2'),('16','BETFRED TV3')]:
 ref=f'1_0_1_{sid}_65_1_300000_0_0_0';row=rows[ref];h=row['source_sha256'];directory=O/h;directory.mkdir(exist_ok=True);a=assets[h];checks=[]
 for size in ('50x30','220x132'):
  for style in ('transparent','white','black'):
   name=f'{size}-{style}.png';raw=z.read('assets/'+h+'/'+name);assert SHA(raw)==a['outputs'][name];(directory/name).write_bytes(raw);checks.append({'file':h+'/'+name,'sha256':SHA(raw),'source':'existing-native-00 artifact13499302234'})
 # The large all-size artifact is blocked by512MB limit. Reproduce only its three missing400x240 bytes from fresh original (never another review output).
 source=srcz.read(members[ref]);assert SHA(source)==h;(directory/'original-220x132.png').write_bytes(source)
 for style in ('transparent','white','black'):
  src=Image.open(io.BytesIO(source)).convert('RGBA');fitted,scale,bbox=mod.fit_logo(src)
  if style=='transparent':im=fitted
  else:
   raw=(B/(style+'-sablona.png')).read_bytes();assert SHA(raw)==master_hashes[style];result=mod.classify_and_render(fitted,Image.open(io.BytesIO(raw)).convert('RGBA'),style);im=result.image
  im=im.convert('RGBa').resize((400,240),Image.Resampling.LANCZOS).convert('RGBA');name='400x240-'+style+'.png';out=io.BytesIO();im.save(out,format='PNG');raw=out.getvalue();assert SHA(raw)==a['outputs'][name],('not identical to previous approved-for-review output',ref,name);(directory/name).write_bytes(raw);checks.append({'file':h+'/'+name,'sha256':SHA(raw),'source':'Fresh frozen original, exact previous index output SHA reproduced'})
 for item in checks:
  im=Image.open(O/item['file']);im.load();assert im.size==tuple(map(int,Path(item['file']).name.split('-')[0].split('x')))and im.convert('RGBA').getchannel('A').getbbox()
 for style in ('transparent','white','black'):tiles.append((label+' / '+style,Image.open(directory/('220x132-'+style+'.png')).convert('RGBA')))
 report.append({'reference':ref,'identity':label,'status':'EXISTING_V9_REVIEW_REQUIRES_OWNER_APPROVAL','prior_qc':a['qc'],'source_sha256':h,'nine_outputs_identical_to_frozen_index':True,'outputs':checks,'production_package_changes':0})
canvas=Image.new('RGB',(720,640),(128,128,128));d=ImageDraw.Draw(canvas)
for i,(label,im)in enumerate(tiles):x=i%3*240;y=i//3*160;d.text((x+4,y+2),label,fill='white');canvas.paste(im,(x+8,y+22),im)
canvas.save(O/'preview.png');(O/'review.json').write_text(json.dumps({'status':'PENDING_OWNER_APPROVAL_NOT_IN_ZIPS','references':report,'original_full_artifact_download_error':'2227856648>536870912 byte limit; no retry','smaller_artifact_id':13499302234,'smaller_artifact_sha256':'26e2448a32e8637eb803cc13fd5844357360654af0924a634200bd35a6d37658','reused_pngs':24,'reproduced_missing_400_outputs_matching_existing_sha':12,'all_36_outputs_match_existing_review_index':True,'no_qc_review_promoted_to_approved':True},ensure_ascii=False,indent=2)+'\n');print('PASS recovered36 existing review PNGs, all old SHA preserved; no package changes')
