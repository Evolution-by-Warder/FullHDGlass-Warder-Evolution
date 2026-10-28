#!/usr/bin/env python3
"""Keep the physical-TV MPEG2 radio still synchronized with the scenic JPEG."""
import argparse
import hashlib
import io
import json
import math
from pathlib import Path
import subprocess
from PIL import Image, ImageChops, ImageStat
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'source/package-root/usr/share/enigma2/hd_glass17'
RECORD=ROOT/'design/radio-lyrics/video-background.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compare(master, video):
    raw=subprocess.check_output(['ffmpeg','-hide_banner','-loglevel','error','-f','mpegvideo',
                                 '-i',str(video),'-frames:v','1','-f','image2pipe','-vcodec','png','pipe:1'])
    with Image.open(master) as image:expected=image.convert('RGB')
    with Image.open(io.BytesIO(raw)) as image:actual=image.convert('RGB')
    if expected.size != (1920,1080) or actual.size != expected.size:
        raise ValueError('Radio video and JPEG must both be 1920x1080')
    rms=ImageStat.Stat(ImageChops.difference(expected,actual)).rms
    error=sum(v*v for v in rms)/3
    psnr=99.0 if error == 0 else 10*math.log10(255*255/error)
    if psnr < 30:
        raise ValueError('Radio video differs from the JPEG (PSNR %.2f dB)'%psnr)
    return round(psnr,3)


def verify():
    record=json.loads(RECORD.read_text())
    master=ASSETS/'warder-radio-background.jpg';video=ASSETS/'radio.mvi'
    if digest(master)!=record['master_sha256'] or digest(video)!=record['video_sha256']:
        raise ValueError('Radio JPEG/MVI changed without rebuilding and recording their pair')
    psnr=compare(master,video)
    print('PASS: physical-TV radio.mvi and screenshot JPEG are synchronized (%.3f dB)'%psnr)


def build():
    master=ASSETS/'warder-radio-background.jpg';video=ASSETS/'radio.mvi'
    command=['ffmpeg','-y','-loglevel','error','-i',str(master),'-frames:v','1',
             '-c:v','mpeg2video','-q:v','5','-f','mpeg2video',str(video)]
    subprocess.run(command,check=True)
    psnr=compare(master,video)
    record={'schema':1,'master':'warder-radio-background.jpg','master_sha256':digest(master),
            'video':'radio.mvi','video_sha256':digest(video),'format':'MPEG2 elementary stream',
            'size':[1920,1080],'decoded_psnr_db':psnr,
            'purpose':'One scenic source for both physical HDMI video plane and OpenWebif; no static UI frames in either.',
            'runtime_overrides_added':False}
    RECORD.write_text(json.dumps(record,indent=2)+'\n')
    verify()


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build',action='store_true')
    args=parser.parse_args()
    build() if args.build else verify()
