"""Review-only official BloombergHT brand variants on immutable MASTER V9 templates."""
import json,hashlib,io,sys,importlib.util
from pathlib import Path
import subprocess,numpy as np
from PIL import Image,ImageDraw
B=Path('bht-review');O=Path('workrepo/reports/vhannibal-followup-20261106/bloomberght-review');O.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('frozen_v9',B/'renderer.py');mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
SHA=lambda b:hashlib.sha256(b).hexdigest();sources=json.load(open('bloomberght-sources/sources.json'));source_by_name={p['file']:p for p in sources['assets']};outputs=[];masters={'white':'c6ae4a808a65ffc8e6458336fccbfe4216de1e832ec0a9abf800907f2f783589','black':'61e69f7fc46e340453bf74ccd7af6ac9d8eba9f8e232884659e1ea99f6abf3fe'};logos={}
for style in ('transparent','white','black'):
 # Fresh official SVG rendering for each variant. Do not feed another output into the next test.
 name='bht-logo-white.svg'if style=='black'else'bht-logo-black.svg';raw=(Path('bloomberght-sources')/name).read_bytes();assert SHA(raw)==source_by_name[name]['sha256'];raster=B/(style+'-fresh-source.png');subprocess.run(['inkscape',str(Path('bloomberght-sources')/name),'--export-type=png','--export-width=782','--export-height=200','--export-filename='+str(raster)],check=True,capture_output=True);src=Image.open(raster).convert('RGBA');logo,scale,bbox=mod.fit_logo(src);logos[style]=logo.copy()
a=np.array(logos['transparent']);b=np.array(logos['white']);assert np.array_equal(a,b)
c=np.array(logos['black']);assert np.array_equal(a[:,:,3],c[:,:,3]),'official variants have different geometry'
mask=(a[:,:,:3].max(2).astype(int)-a[:,:,:3].min(2).astype(int)>24)&(a[:,:,3]>0)
# Provider supplies both text colours. Guard chromatic edge RGBA against resampling blend with its neighbouring neutral text.
guarded=int(np.any(a[mask]!=c[mask],axis=1).sum());c[mask]=a[mask];assert np.array_equal(a[mask],c[mask]);logos['black']=Image.fromarray(c,'RGBA')
for style in ('transparent','white','black'):
 logo=logos[style]
 if style=='transparent':native=logo.copy()
 else:
  template=(B/(style+'-sablona.png')).read_bytes();assert SHA(template)==masters[style];native=Image.alpha_composite(Image.open(io.BytesIO(template)).convert('RGBA'),logo)
 for size in ((50,30),(220,132),(400,240)):
  im=native.copy()if size==native.size else native.convert('RGBa').resize(size,Image.Resampling.LANCZOS).convert('RGBA');file=f'{size[0]}x{size[1]}-{style}.png';im.save(O/file);test=Image.open(O/file);test.load();assert test.size==size and test.getchannel('A').getbbox();outputs.append({'filename':file,'sha256':SHA((O/file).read_bytes()),'source_svg':'bht-logo-white.svg'if style=='black'else'bht-logo-black.svg','operation':'FRESH_OFFICIAL_SVG_FIT_AND_MASTER_COMPOSITE_PROTECTED_CHROMATIC_RGBA','source_alpha_nonempty':True})
canvas=Image.new('RGB',(1260,820),(128,128,128));d=ImageDraw.Draw(canvas)
for row,size in enumerate(('50x30','220x132','400x240')):
 for col,style in enumerate(('transparent','white','black')):
  x=col*420;y=row*270;d.text((x+8,y+6),size+' '+style+' | REVIEW ONLY',fill='white');im=Image.open(O/(size+'-'+style+'.png'));canvas.paste(im,(x+(420-im.width)//2,y+25+(240-im.height)//2),im)
canvas.save(O/'preview.png')
report={'status':'OWNER_ARTWORK_REVIEW_REQUIRED_NOT_IN_PACKAGES','source':'../sources/sources.json','references':['1_0_19_29CE_A2E8_42E_1A40000_0_0_0','1_0_19_2AFA_A92B_42E_1A40000_0_0_0'],'new_unique_artwork':1,'review_pngs':9,'target_reference_variants_if_approved':18,'official_dark_light_geometry_identical':True,'official_chromatic_rgba_preserved':True,'resampled_chromatic_edge_pixels_restored_to_fresh_original':guarded,'template_sha256':masters,'immutable_v9_fit_renderer_sha256':SHA((B/'renderer.py').read_bytes()),'production_package_changes':0,'does_not_reduce_open_count':True,'outputs':outputs};(O/'review.json').write_text(json.dumps(report,indent=2)+'\n');print('BHT REVIEW PASS9, protected chromatic pixels',int(mask.sum()),flush=True)
