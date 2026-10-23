#!/usr/bin/env python3
"""Test native PNG decoding, safe caching and all 252 approved illustrations."""
import argparse
import base64
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import struct
import tempfile
import unittest
import zipfile
import zlib

ROOT=Path(__file__).resolve().parents[1]
PLUGIN=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
spec=importlib.util.spec_from_file_location('warder_help_art',PLUGIN/'warderHelpArt.py')
art=importlib.util.module_from_spec(spec);spec.loader.exec_module(art)
parser=argparse.ArgumentParser();parser.add_argument('--bundle');args,remaining=parser.parse_known_args()
BUNDLE=Path(args.bundle) if args.bundle else None


def png_chunk(tag,data):
    return struct.pack('>I',len(data))+tag+data+struct.pack('>I',zlib.crc32(tag+data)&0xffffffff)


def filtered_png():
    width,height=882,300;stride=width*4;rows=[];previous=bytes(stride);expected=[]
    for y in range(height):
        row=bytes((x*7+y*17)%256 if x%4!=3 else 255 for x in range(stride));expected.append(row)
        mode=y%5;data=bytearray(stride)
        for x,value in enumerate(row):
            left=row[x-4] if x>=4 else 0;above=previous[x];upper_left=previous[x-4] if x>=4 else 0
            # Independently compute the PNG filter predictor.
            candidates=(left,above,upper_left);p=left+above-upper_left
            distances=[abs(p-c) for c in candidates]
            paeth=candidates[distances.index(min(distances))]
            predictor=(0,left,above,(left+above)//2,paeth)[mode]
            data[x]=(value-predictor)&255
        rows.append(bytes([mode])+data);previous=row
    raw=(b'\x89PNG\r\n\x1a\n'+png_chunk(b'IHDR',struct.pack('>IIBBBBB',width,height,8,6,0,0,0))
         +png_chunk(b'IDAT',zlib.compress(b''.join(rows)))+png_chunk(b'IEND',b''))
    return raw,b''.join(expected)


class HelpArtTests(unittest.TestCase):
    def test_all_five_png_filters_have_exact_known_pixel_values(self):
        raw,expected=filtered_png();width,height,decoded=art.decode_png(raw)
        self.assertEqual((width,height),(882,300));self.assertEqual(bytes(decoded),expected)

    def test_palette_and_transparency_decode_without_pillow(self):
        data=(b'\x89PNG\r\n\x1a\n'+png_chunk(b'IHDR',struct.pack('>IIBBBBB',882,300,8,3,0,0,0))
              +png_chunk(b'PLTE',bytes([10,20,30,100,110,120]))+png_chunk(b'tRNS',bytes([0,255]))
              +png_chunk(b'IDAT',zlib.compress((b'\x00'+bytes([0,1])*441)*300))+png_chunk(b'IEND',b''))
        _,_,rgba=art.decode_png(data)
        self.assertEqual(rgba[:8],bytes([10,20,30,0,100,110,120,255]))
        self.assertEqual(rgba[-8:],rgba[:8])

    def test_unknown_or_missing_image_falls_back_without_changes(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'custom.png';p.write_bytes(b'custom help artwork')
            self.assertEqual(art.themed_path(str(p),str(Path(folder)/'cache')),str(p))
            self.assertEqual(p.read_bytes(),b'custom help artwork')
            missing=str(Path(folder)/'missing.png')
            self.assertEqual(art.themed_path(missing),missing)

    def test_bad_mask_falls_back_and_does_not_leave_temporary_files(self):
        raw,_=filtered_png();digest=hashlib.sha256(raw).hexdigest();old=art._INDEX
        try:
            art._INDEX={'images':{digest:{'mask':base64.b64encode(b'bad zlib').decode()}}}
            with tempfile.TemporaryDirectory() as folder:
                p=Path(folder)/'original.png';p.write_bytes(raw);cache=Path(folder)/'cache'
                self.assertEqual(art.themed_path(str(p),str(cache)),str(p))
                self.assertFalse(list(cache.glob('*')))
                self.assertEqual(p.read_bytes(),raw)
        finally:art._INDEX=old

    def test_index_covers_the_entire_approved_bundle(self):
        data=art._index();self.assertEqual(data['image_count'],252);self.assertEqual(len(data['images']),236)
        self.assertEqual(len({name for x in data['images'].values() for name in x['names']}),252)
        for digest,entry in data['images'].items():
            self.assertEqual(len(digest),64);self.assertGreater(entry['foreground_pixels'],100)
            self.assertLess(entry['foreground_pixels'],882*300*.5)
            mask=zlib.decompress(base64.b64decode(entry['mask']))
            self.assertEqual(len(mask),882*300//8)

    @unittest.skipIf(BUNDLE is None,'Pass --bundle for all original illustrations')
    def test_all_original_content_pixels_and_safe_cache_with_independent_decoder(self):
        from PIL import Image
        raw_bundle=BUNDLE.read_bytes();index=art._index()
        self.assertEqual(hashlib.sha256(raw_bundle).hexdigest(),index['source_bundle_sha256'])
        with zipfile.ZipFile(io.BytesIO(raw_bundle)) as archive,tempfile.TemporaryDirectory() as folder:
            names=[n for n in archive.namelist() if n.lower().endswith('.png')]
            self.assertEqual(len(names),252)
            for sequence,name in enumerate(names):
                raw=archive.read(name);digest=hashlib.sha256(raw).hexdigest();entry=index['images'][digest]
                original=Image.open(io.BytesIO(raw)).convert('RGBA').tobytes()
                _,_,decoded=art.decode_png(raw)
                self.assertEqual(bytes(decoded),original,name)
                result=art.render(raw,entry);image=Image.open(io.BytesIO(result));self.assertEqual(image.size,(882,300))
                styled=image.convert('RGBA').tobytes();mask=zlib.decompress(base64.b64decode(entry['mask']))
                self.assertEqual(styled[0::4],original[0::4],name)
                self.assertEqual(styled[1::4],original[1::4],name)
                self.assertEqual(styled[2::4],original[2::4],name)
                expected_alpha=bytes(original[i*4+3] if mask[i>>3]&(128>>(i&7)) else 0 for i in range(882*300))
                self.assertEqual(styled[3::4],expected_alpha,name)
                for left,top,right,bottom in entry['preserved_regions']:
                    for y in range(top,bottom):
                        begin=(y*882+left)*4;end=(y*882+right)*4
                        self.assertEqual(styled[begin:end],original[begin:end],name)
                if sequence==0:
                    p=Path(folder)/'original.png';p.write_bytes(raw);cache=Path(folder)/'cache'
                    target=art.themed_path(str(p),str(cache));self.assertNotEqual(target,str(p))
                    before=Path(target).stat().st_mtime_ns
                    self.assertEqual(art.themed_path(str(p),str(cache)),target)
                    self.assertEqual(Path(target).stat().st_mtime_ns,before)
                    self.assertEqual(p.read_bytes(),raw)
            print('Verified all 252 help illustrations: exact original RGB content, masked background and cache')


if __name__=='__main__':unittest.main(argv=[__file__]+remaining)
