#!/usr/bin/env python3
"""Rebuild 48 transparent CAM picons from original Black/White archives.

Preserves White's original sizes: 45 x 150x90 and 3 x 153x90.
"""
import hashlib
import io
import json
from pathlib import Path
import zipfile
from collections import Counter
import numpy as np
import cv2
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CAM = ROOT / "assets/warder/downloads/picons/cam"
OUT = CAM / "transparent/piconCam.zip"
CATALOG = ROOT / "assets/warder/downloads.json"
URL = ("https://raw.githubusercontent.com/Evolution-by-Warder/"
       "FullHDGlass-Warder-Evolution/main/assets/warder/downloads/"
       "picons/cam/transparent/piconCam.zip")

def read_master(style):
    with zipfile.ZipFile(CAM / style / "piconCam.zip") as z:
        result = {}
        for name in z.namelist():
            if not name.lower().endswith(".png"):
                continue
            if not name.startswith("piconCam/") or name.count("/") != 1:
                raise ValueError("Unsafe source member " + name)
            result[name] = Image.open(io.BytesIO(z.read(name))).convert("RGBA")
        return result

def build():
    black, white = read_master("black"), read_master("white")
    if len(black) != 48 or set(black) != set(white):
        raise ValueError("Black/White CAM sets must contain exactly the same 48 names")
    if Counter(im.size for im in black.values()) != {(150,90):48}:
        raise ValueError("Unexpected Black dimensions")
    if Counter(im.size for im in white.values()) != {(150,90):45,(153,90):3}:
        raise ValueError("Unexpected White dimensions")
    names = sorted(black)
    imgs = np.stack([np.asarray(black[n])[:,:,:3] for n in names]).astype(np.float32)
    med = np.median(imgs,axis=0).astype(np.uint8)
    variation = np.percentile(imgs,95,axis=0)-np.percentile(imgs,5,axis=0)
    missing = (variation.max(axis=2)>38).astype(np.uint8)*255
    missing = cv2.dilate(missing,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7)))
    bg = cv2.inpaint(med,missing,8,cv2.INPAINT_TELEA).astype(np.float32)
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in names:
            arr=np.asarray(black[name]).copy()
            rgb=arr[:,:,:3].astype(np.float32)
            alpha=(np.clip((np.abs(rgb-bg).max(axis=2)-15)/80,0,1)*arr[:,:,3]).astype(np.uint8)
            binary=(alpha>12).astype(np.uint8)
            count,labels,stats,_=cv2.connectedComponentsWithStats(binary,8)
            for cid in range(1,count):
                if stats[cid,cv2.CC_STAT_AREA]<3:
                    alpha[labels==cid]=0
            arr[:,:,3]=alpha
            maxc,minc=rgb.max(axis=2),rgb.min(axis=2)
            neutral=(maxc-minc<16)&(rgb.mean(axis=2)<85)&(alpha>35)
            arr[neutral,:3]=[235,239,245]
            im=Image.fromarray(arr,"RGBA")
            if im.size != white[name].size:
                canvas=Image.new("RGBA",white[name].size,(0,0,0,0))
                canvas.paste(im,(0,0))
                im=canvas
            if im.getbbox() is None:
                raise ValueError("Empty CAM icon "+name)
            buf=io.BytesIO()
            im.save(buf,"PNG",optimize=True)
            info=zipfile.ZipInfo(name,(2020,1,1,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,buf.getvalue(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    data=OUT.read_bytes()
    sha=hashlib.sha256(data).hexdigest()
    with zipfile.ZipFile(OUT) as z:
        if z.testzip() or len(z.namelist())!=48:
            raise ValueError("Broken CAM archive")
        sizes=Counter(Image.open(io.BytesIO(z.read(name))).size for name in z.namelist())
        if sizes != {(150,90):45,(153,90):3}:
            raise ValueError("Dimensions wrong "+str(sizes))
        for name in z.namelist():
            im=Image.open(io.BytesIO(z.read(name))).convert("RGBA")
            if im.getchannel("A").getextrema() != (0,255):
                raise ValueError("Alpha channel missing in "+name)
    catalog=json.loads(CATALOG.read_text(encoding="utf-8"))
    catalog["assets"]["piconCam-220"] = {
        "filename":"piconCam-transparent.zip","size":len(data),
        "sha256":sha,"root":"piconCam","url":URL,
    }
    CATALOG.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"count":48,"sizes":{"150x90":45,"153x90":3},"bytes":len(data),"sha256":sha,"url":URL},indent=2))

if __name__=="__main__":
    build()
