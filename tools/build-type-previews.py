#!/usr/bin/env python3
"""Prepare small real Extra Infobar thumbnails from the pinned stock previews."""
import argparse
import hashlib
import io
from pathlib import Path
import re
import zipfile
from PIL import Image

SOURCE_SHA='0fca8510b5e1e7dd600548f706553b83a3993e91077382aba4c6363278eac230'


def build(bundle,output):
    raw=Path(bundle).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA:raise ValueError('Preview source SHA mismatch')
    count=0
    with zipfile.ZipFile(io.BytesIO(raw)) as source,zipfile.ZipFile(output,'w') as target:
        for name in sorted(source.namelist()):
            match=re.fullmatch(r'more_icons/scr_prew/screen-(\d+)\.png',name)
            if not match:continue
            with Image.open(io.BytesIO(source.read(name))) as image:
                image=image.convert('RGBA');image.thumbnail((174,98),Image.Resampling.LANCZOS)
                canvas=Image.new('RGBA',(174,98),(16,33,54,255));canvas.alpha_composite(image,((174-image.width)//2,(98-image.height)//2))
                stream=io.BytesIO();canvas.save(stream,format='PNG',optimize=True)
            info=zipfile.ZipInfo('type-'+match[1]+'.png',(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_STORED
            target.writestr(info,stream.getvalue());count+=1
    if count!=78:raise ValueError('Missing stock type previews')
    print('Prepared',count,'real type thumbnails:',Path(output).stat().st_size,'bytes')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--bundle',required=True);parser.add_argument('--output',required=True);args=parser.parse_args();build(args.bundle,args.output)
