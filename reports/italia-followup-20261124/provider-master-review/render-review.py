#!/usr/bin/env python3
"""Reproduce review-only variants, preserving transparent source and original MASTER frames."""
import argparse, hashlib, io, json, zipfile
from pathlib import Path
from PIL import Image
import numpy as np
def sha(b): return hashlib.sha256(b).hexdigest()
p=argparse.ArgumentParser(); p.add_argument('--masters',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
folder=Path(__file__).parent
master_hashes={'white':'c6ae4a808a65ffc8e6458336fccbfe4216de1e832ec0a9abf800907f2f783589','black':'61e69f7fc46e340453bf74ccd7af6ac9d8eba9f8e232884659e1ea99f6abf3fe'}
frames={}
for s,h in master_hashes.items():
 raw=(a.masters/(s+'-sablona.png')).read_bytes();assert sha(raw)==h
 frames[s]=Image.open(io.BytesIO(raw)).convert('RGBA');assert frames[s].size==(220,132)
adapt={'CANALE 40.png','CANALE 40REG.png',"L'ALTRO CORRIERE.png",'MUXIP.png','ROMANTICA RADIO.png','TELERENT.png','VIDEOMEDIA-TN.png','VTS.png'}
records=[]
with zipfile.ZipFile(a.output,'w',zipfile.ZIP_DEFLATED) as z:
 for path in sorted((folder/'transparent').glob('*.png')):
  raw=path.read_bytes();src=Image.open(io.BytesIO(raw)).convert('RGBA');assert src.size==(220,132)
  rec={'name':path.name,'source_sha256':sha(raw),'white_contrast_adapted':path.name in adapt,'variants':{}}
  for s in ('transparent','white','black'):
   if s=='transparent': data=raw
   else:
    logo=src.copy()
    if s=='white' and path.name in adapt:
     x=np.array(logo);rgb=x[:,:,:3].astype(float);lo=rgb.min(axis=2);hi=rgb.max(axis=2)
     strength=np.clip((lo-150)/75,0,1)*np.clip((45-(hi-lo))/30,0,1)
     rgb=rgb*(1-strength[:,:,None])+np.array([32,36,42])*strength[:,:,None]
     x[:,:,:3]=rgb.round().astype(np.uint8);logo=Image.fromarray(x)
    image=Image.alpha_composite(frames[s],logo)
    buf=io.BytesIO();image.save(buf,'PNG',optimize=True);data=buf.getvalue()
   n=f'{s}/piconProv/{path.name}';z.writestr(n,data);rec['variants'][s]={'path':n,'sha256':sha(data)}
  records.append(rec)
 assert len(records)==16
 z.writestr('register.json',json.dumps({'status':'REVIEW_ONLY','count':16,'records':records,'master_sha256':master_hashes},ensure_ascii=False,indent=2))
with zipfile.ZipFile(a.output) as z:assert z.testzip() is None;assert sum(n.endswith('.png') for n in z.namelist())==48
