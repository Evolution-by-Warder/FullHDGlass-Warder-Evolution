#!/usr/bin/env python3
"""Get each FullHDGlass CAM ZIP over its actual GitHub URL and check integrity."""
import hashlib
import io
import json
import pathlib
import sys
import urllib.request
import zipfile
from collections import Counter
from PIL import Image

ROOT=pathlib.Path(__file__).resolve().parents[1]
CATALOG=ROOT/'assets/warder/downloads.json'
ASSETS=json.loads(CATALOG.read_text(encoding='utf-8'))['assets']
BASE="https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/"

def verify(branch='main'):
    for key,expected_count,expected_size in (
        ('piconCam-b',48,{(150,90):48}),
        ('piconCam-w',48,{(150,90):45,(153,90):3}),
        ('piconCam-220',48,{(150,90):45,(153,90):3}),
    ):
        asset=ASSETS[key]
        url=asset['url']
        if key=='piconCam-220' and branch!='main':
            url=url.replace(BASE+'main/',BASE+branch+'/')
        # This is an actual network GET, not a static source check.
        req=urllib.request.Request(url,headers={'User-Agent':'FullHDGlass-CAM-link-audit/1.0'})
        with urllib.request.urlopen(req,timeout=45) as response:
            status=response.status
            content=response.read(2*1024*1024)
            if status!=200:
                raise AssertionError((key,'HTTP',status))
        if len(content)!=asset['size'] or hashlib.sha256(content).hexdigest()!=asset['sha256']:
            raise AssertionError((key,'downloaded archive differs from manifest'))
        with zipfile.ZipFile(io.BytesIO(content)) as z:
            names=[n for n in z.namelist() if n.endswith('.png')]
            if z.testzip() is not None or len(names)!=expected_count:
                raise AssertionError((key,'broken or incomplete archive'))
            if set(names)!=set('piconCam/'+n for n in (x.split('/')[-1] for x in names)):
                raise AssertionError((key,'invalid target directory'))
            sizes=Counter(Image.open(io.BytesIO(z.read(n))).size for n in names)
            if sizes != expected_size:
                raise AssertionError((key,'dimensions',sizes))
            if key=='piconCam-220':
                for n in names:
                    a=Image.open(io.BytesIO(z.read(n))).convert('RGBA').getchannel('A')
                    if a.getextrema()!=(0,255):
                        raise AssertionError((n,'alpha background not transparent'))
        print('PASS',key,'HTTP',status,'PNG',len(names),'sizes',dict(sizes),
              'bytes',len(content),'SHA256',asset['sha256'],'URL',url)
if __name__=='__main__':
    verify(sys.argv[1] if len(sys.argv)>1 else 'main')
