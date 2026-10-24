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
import time
from unittest.mock import patch
import unittest
import zipfile
import zlib

ROOT=Path(__file__).resolve().parents[1]
PLUGIN=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
spec=importlib.util.spec_from_file_location('warder_help_art',PLUGIN/'warderHelpArt.py')
art=importlib.util.module_from_spec(spec);spec.loader.exec_module(art)
parser=argparse.ArgumentParser();parser.add_argument('--bundle');parser.add_argument('--prebuilt');args,remaining=parser.parse_known_args()
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

    def test_prepared_preview_needs_no_pixel_work_and_cache_invalidates_on_source_change(self):
        from unittest.mock import patch
        import time
        raw=art.encode_png(882,300,bytes([0,0,0,255])*(882*300))
        ready=art.encode_png(882,300,bytes([16,33,54,255])*(882*300))
        digest=hashlib.sha256(raw).hexdigest()
        mask=base64.b64encode(zlib.compress(bytes(882*300//8))).decode('ascii')
        revision=hashlib.sha256((art._STYLE+':'+mask).encode('ascii')).hexdigest()[:12]
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'original.png';p.write_bytes(raw)
            prepared=Path(folder)/'prepared.zip';cache=Path(folder)/'cache'
            with zipfile.ZipFile(prepared,'w') as archive:
                archive.writestr(digest+'-'+revision+'.png',ready)
            with patch.object(art,'_INDEX',{'images':{digest:{'mask':mask}}}), patch.object(art,'_PREBUILT',str(prepared)), patch.object(art,'_CACHE_DIR',str(cache)), patch.object(art,'render',side_effect=AssertionError('GUI must not render PNGs')):
                begin=time.perf_counter();target=art.cached_path(str(p));cold=time.perf_counter()-begin
                self.assertNotEqual(target,str(p));self.assertEqual(Path(target).read_bytes(),ready)
                with patch('builtins.open',side_effect=AssertionError('Warm lookup must not reread source')):
                    self.assertEqual(art.cached_path(str(p)),target)
                Path(target).unlink()
                self.assertEqual(art.cached_path(str(p)),target)
                self.assertEqual(Path(target).read_bytes(),ready)
                p.write_bytes(b'new custom source')
                self.assertEqual(art.cached_path(str(p)),str(p))
                print('Prepared cold preview lookup: %.3f ms on build host (not a receiver timing)'%(cold*1000))

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
            timings=[]
            for sequence,name in enumerate(names):
                raw=archive.read(name);digest=hashlib.sha256(raw).hexdigest();entry=index['images'][digest]
                original=Image.open(io.BytesIO(raw)).convert('RGBA').tobytes()
                _,_,decoded=art.decode_png(raw)
                self.assertEqual(bytes(decoded),original,name)
                result=art.render(raw,entry)
                if args.prebuilt:
                    revision=hashlib.sha256((art._STYLE+':'+entry['mask']).encode('ascii')).hexdigest()[:12]
                    with zipfile.ZipFile(args.prebuilt) as prepared:
                        self.assertEqual(len(prepared.namelist()),236)
                        prepared_image=Image.open(io.BytesIO(prepared.read(digest+'-'+revision+'.png'))).convert('RGBA')
                        self.assertEqual(prepared_image.size,(882,300),name)
                        self.assertEqual(prepared_image.tobytes(),Image.open(io.BytesIO(result)).convert('RGBA').tobytes(),name)
                    source=Path(folder)/'lookup.png';source.write_bytes(raw)
                    with patch.object(art,'_PREBUILT',args.prebuilt), patch.object(art,'_CACHE_DIR',str(Path(folder)/'prepared-cache')), patch.object(art,'render',side_effect=AssertionError('Menu must never render')):
                        begin=time.perf_counter();target=art.cached_path(str(source));timings.append(time.perf_counter()-begin)
                        self.assertIsNotNone(target,name)
                        self.assertNotEqual(target,str(source),name)
                        self.assertEqual(Image.open(target).convert('RGBA').tobytes(),Image.open(io.BytesIO(result)).convert('RGBA').tobytes(),name)
                image=Image.open(io.BytesIO(result));self.assertEqual(image.size,(882,300))
                styled=image.convert('RGBA').tobytes();mask=zlib.decompress(base64.b64decode(entry['mask']))
                # No pixel is erased: original alpha and full diagram geometry survive.
                self.assertEqual(styled[3::4],original[3::4],name)
                before_image=Image.frombytes('RGBA',(882,300),original)
                lookup=[min(255,value+offset) for offset in (16,33,54) for value in range(256)]
                navy=before_image.convert('RGB').point(lookup)
                foreground=Image.frombytes('L',(882,300),bytes(255 if mask[i>>3]&(128>>(i&7)) else 0 for i in range(882*300)))
                expected=Image.composite(before_image.convert('RGB'),navy,foreground)
                self.assertEqual(image.convert('RGB').tobytes(),expected.tobytes(),name)
                for left,top,right,bottom in entry['preserved_regions']:
                    for y in range(top,bottom):
                        begin=(y*882+left)*4;end=(y*882+right)*4
                        self.assertEqual(styled[begin:end],original[begin:end],name)
                if sequence==0:
                    p=Path(folder)/'original.png';p.write_bytes(raw);cache=Path(folder)/'cache'
                    cache.mkdir()
                    legacy_revision=hashlib.sha256(entry['mask'].encode('ascii')).hexdigest()[:12]
                    legacy=cache/(digest+'-'+legacy_revision+'.png');legacy.write_bytes(b'old erased version')
                    target=art.themed_path(str(p),str(cache));self.assertNotEqual(target,str(p))
                    self.assertNotEqual(target,str(legacy))
                    before=Path(target).stat().st_mtime_ns
                    self.assertEqual(art.themed_path(str(p),str(cache)),target)
                    self.assertEqual(Path(target).stat().st_mtime_ns,before)
                    self.assertEqual(p.read_bytes(),raw)
            if timings:print('Prepared preview lookups on build host: mean %.3f ms, max %.3f ms; receiver timing unverified'%(sum(timings)/len(timings)*1000,max(timings)*1000))
            print('Verified all 252 help illustrations: exact original RGB content, opaque navy background and cache invalidation')


if __name__=='__main__':unittest.main(argv=[__file__]+remaining)

