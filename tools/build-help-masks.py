#!/usr/bin/env python3
"""Rebuild help-background metadata from the pinned original help ZIP.

Build dependencies: Pillow, numpy, scipy. Receiver needs only the Python stdlib.
This writes masks/provenance; it never rewrites an original help illustration.
"""
from pathlib import Path
from PIL import Image
from scipy import ndimage
import numpy as np
import argparse,base64,hashlib,io,json,tempfile,zipfile,zlib

parser=argparse.ArgumentParser()
parser.add_argument('--bundle',required=True)
parser.add_argument('--output',default=str(Path(__file__).resolve().parents[1]/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warder-help-masks.json'))
args=parser.parse_args()
raw=Path(args.bundle).read_bytes()
assert hashlib.sha256(raw).hexdigest()=='872d59dfccf090344a37ed46e277dd091cd9ec671db128fa421c748f4f6eb8ef'
temporary=tempfile.TemporaryDirectory()
root=Path(temporary.name)
with zipfile.ZipFile(io.BytesIO(raw)) as archive:
    for name in archive.namelist():
        if name.endswith('.png'):
            (root/Path(name).name).write_bytes(archive.read(name))
paths=sorted(root.glob('*.png'))
assert len(paths)==252
a=np.stack([np.asarray(Image.open(p).convert('RGB')) for p in paths]);base=a[next(i for i,p in enumerate(paths) if p.name=='10-0.png')].astype('int16')
counts=(np.abs(a.astype('int16')-base).max(axis=3)>10).sum(axis=(1,2))
refs=np.argsort(counts)[:45];subset=a[refs].astype('float32');neutral=subset.max(axis=3)-subset.min(axis=3)<5;shade=subset.mean(axis=3);shade[~neutral]=np.nan
model=np.nanmedian(shade,axis=0);model=np.nan_to_num(model,nan=0).astype('int16')
entries={};stats=[]
for p in sorted(root.glob('*.png')):
 rgba=np.asarray(Image.open(p).convert('RGBA'));rgb=rgba[:,:,:3].astype('int16')
 spread=rgb.max(axis=2)-rgb.min(axis=2)
 threshold=np.where(spread<=25,32,12)
 mask=np.abs(rgb-model[:,:,None]).max(axis=2)>threshold
 # Fill photo/screenshot interiors so their black/grey detail remains intact.
 protected=np.zeros(mask.shape,bool);regions=[]
 photo_mask=np.abs(rgb-model[:,:,None]).max(axis=2)>12
 labels,count=ndimage.label(ndimage.binary_closing(photo_mask,iterations=1))
 for i,box in enumerate(ndimage.find_objects(labels),1):
  if box is None:continue
  ys,xs=box;area=int((labels[box]==i).sum());w=xs.stop-xs.start;h=ys.stop-ys.start
  if area>=3000 and w>=80 and h>=50 and area/(w*h)>.2:
   mask[ys,xs]=True;protected[ys,xs]=True;regions.append([xs.start,ys.start,xs.stop,ys.stop])
 # Detached, dark-grey fragments outside the informative core belong to
 # the decorative bubble contour, not to screenshots or text/arrow anchors.
 spread=rgb.max(axis=2)-rgb.min(axis=2)
 anchor=(spread>8)|(rgb.max(axis=2)>180)|protected
 near=ndimage.binary_dilation(anchor,iterations=4)
 labels,count=ndimage.label(mask)
 for i,box in enumerate(ndimage.find_objects(labels),1):
  if box is None:continue
  ys,xs=box;component=labels[box]==i
  inside_core=xs.start>=190 and xs.stop<=670 and ys.start>=45 and ys.stop<=225
  if not inside_core and not near[box][component].any():
   mask[box][component]=False
 mask=ndimage.binary_dilation(mask,iterations=1)
 packed=np.packbits(mask.flatten()).tobytes();encoded=base64.b64encode(zlib.compress(packed,9)).decode()
 raw=p.read_bytes();digest=hashlib.sha256(raw).hexdigest()
 if digest in entries:
  entries[digest]['names'].append(p.name)
 else:
  entries[digest]={'name':p.name,'names':[p.name],'mask':encoded,'foreground_pixels':int(mask.sum()),'preserved_regions':regions}
 stats.append((int(mask.sum()),p.name))
out={'schema':1,'width':882,'height':300,'source_bundle_sha256':'872d59dfccf090344a37ed46e277dd091cd9ec671db128fa421c748f4f6eb8ef','image_count':252,'unique_image_count':len(entries),'images':entries}
Path(args.output).write_text(json.dumps(out,separators=(',',':'))+'\n')
print('Rebuilt masks for 252 paths /',len(entries),'unique original images')
temporary.cleanup()
