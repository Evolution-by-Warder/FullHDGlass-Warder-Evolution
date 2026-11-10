"""Review-only current Chefi.ro logo; immutable Warder template; no recolouring."""
from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json
B=Path(__file__).resolve().parent; O=B/'review';O.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
masters={'white':'c6ae4a808a65ffc8e6458336fccbfe4216de1e832ec0a9abf800907f2f783589','black':'61e69f7fc46e340453bf74ccd7af6ac9d8eba9f8e232884659e1ea99f6abf3fe'}
src=Image.open(B/'chefi-official.png').convert('RGBA');box=src.getchannel('A').getbbox();mark=src.crop(box)
# Explicit review geometry from existing source-candidates renderer: 204x116 fit on220x132.
mark.thumbnail((204,116),Image.Resampling.LANCZOS)
outputs=[]
for style in ('transparent','white','black'):
 if style=='transparent': native=Image.new('RGBA',(220,132))
 else:
  p=B/'templates'/f'{style}-sablona.png';assert sha(p)==masters[style];native=Image.open(p).convert('RGBA')
 native.alpha_composite(mark,((220-mark.width)//2,(132-mark.height)//2))
 for size in ((50,30),(220,132),(400,240)):
  im=Image.new('RGBA',size) if style=='transparent' else Image.open(B/'templates'/f'{style}-sablona.png').convert('RGBA').convert('RGBa').resize(size,Image.Resampling.LANCZOS).convert('RGBA')
  fresh=src.crop(box);scale=min((204*size[0]/220)/fresh.width,(116*size[1]/132)/fresh.height);fitted=(round(fresh.width*scale),round(fresh.height*scale));fresh=fresh.convert('RGBa').resize(fitted,Image.Resampling.LANCZOS).convert('RGBA');im.alpha_composite(fresh,((size[0]-fresh.width)//2,(size[1]-fresh.height)//2))
  p=O/f'{size[0]}x{size[1]}-{style}.png';im.save(p)
  t=Image.open(p);t.load();assert t.size==size and t.mode=='RGBA' and t.getchannel('A').getbbox()
  outputs.append({'file':p.name,'sha256':sha(p),'size':list(size),'mode':t.mode,'alpha_extrema':list(t.getchannel('A').getextrema())})
canvas=Image.new('RGB',(1260,820),(128,128,128));d=ImageDraw.Draw(canvas)
for row,size in enumerate(('50x30','220x132','400x240')):
 for col,style in enumerate(('transparent','white','black')):
  x=col*420;y=row*270;d.text((x+8,y+6),size+' '+style+' | UNAPPROVED DRAFT',fill='white');im=Image.open(O/(size+'-'+style+'.png'));canvas.paste(im,(x+(420-im.width)//2,y+25+(240-im.height)//2),im)
canvas.save(O/'preview.png')
report={'status':'OWNER_ARTWORK_REVIEW_REQUIRED_NOT_IN_PACKAGES','station':'Chefi.ro','reference':'1_0_16_5_A_16E_1860000_0_0_0','source_url':'https://assets.antenaplay.ro/2026/06/05/IX530VlrOnRp27KMRAnV.png','official_catalog':'https://antenaplay.ro/live','source_sha256':sha(B/'chefi-official.png'),'source_size':list(src.size),'source_alpha_bbox':list(box),'source_colours_preserved':True,'no_recolour_or_redraw':True,'templates_immutable':masters,'geometry':'Every size from original alpha bounds; proportional204x116 fit at220x132; premultipliedLANCZOS. Original golden glow and shadow preserved.','output_count':9,'new_approved_references':0,'production_package_changes':0,'does_not_reduce_open_count':True,'visual_review':'Original golden glow and all colours retained. Detailed lettering is small at50x30; visual owner review required for new artwork.','outputs':outputs}
(O/'review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Prepared9 review variants; no package changes')
