#!/usr/bin/env python3
"""Protect alias scope, exact approved bytes and unrelated data in publication."""
import importlib.util
import io
from pathlib import Path
import unittest
import zipfile
from PIL import Image

spec=importlib.util.spec_from_file_location('publisher',Path(__file__).with_name('publish-magenta-league-picons-20261030.py'))
p=importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)

CANONICAL='1_0_1_12F_157C_13E_820000_0_0_0.png'
OLD_ALIAS='1_0_19_12F_157C_13E_820000_0_0_0.png'
OTHER_POSITION='1_0_1_12F_157C_13E_5A0000_0_0_0.png'


def png(colour):
    out=io.BytesIO()
    Image.new('RGBA',(220,132),colour).save(out,format='PNG')
    return out.getvalue()


def archive(entries):
    out=io.BytesIO()
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in entries.items():z.writestr(name,data)
    return out.getvalue()


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.approved=png((40,100,200,150))
        self.old=png((200,20,50,255))
        self.art={('magenta-sport1league','white'):self.approved}
        self.mapping={'slug':'magenta-sport1league','reference':CANONICAL,'identity':[0x12F,0x157C,0x13E,130],'selector_id':'130E'}
        self.package={'selector_id':'130E','family':'channel-white','resolution':'220x132'}

    def test_exact_220_bytes_alias_and_unrelated_png_preserved(self):
        before=archive({OLD_ALIAS:self.old,OTHER_POSITION:self.old})
        packed,report=p.patch_archive(before,self.package,[self.mapping],self.art)
        with zipfile.ZipFile(io.BytesIO(packed)) as z:
            self.assertEqual(z.read(OLD_ALIAS),self.approved)
            self.assertEqual(z.read(CANONICAL),self.approved)
            self.assertEqual(z.read(OTHER_POSITION),self.old)
        self.assertEqual(report['added'],[CANONICAL])
        self.assertEqual(report['unrelated_preserved'],1)

    def test_provider_without_verified_membership_gets_no_new_station(self):
        self.package['selector_id']='CANALPLUS_SK'
        self.assertIsNone(p.patch_archive(archive({OTHER_POSITION:self.old}),self.package,[self.mapping],self.art))

    def test_provider_existing_logical_alias_is_updated(self):
        self.package['selector_id']='SKYLINK'
        packed,_=p.patch_archive(archive({OLD_ALIAS:self.old}),self.package,[self.mapping],self.art)
        with zipfile.ZipFile(io.BytesIO(packed)) as z:self.assertEqual(z.read(CANONICAL),self.approved)

    def test_ordinary_magenta_sport_is_preserved(self):
        ordinary='1_0_1_41C_4_AA_5A0000_0_0_0.png'
        packed,_=p.patch_archive(archive({OLD_ALIAS:self.old,ordinary:self.old}),self.package,[self.mapping],self.art)
        with zipfile.ZipFile(io.BytesIO(packed)) as z:
            self.assertEqual(z.read(ordinary),self.old)
            self.assertEqual(z.read(CANONICAL),self.approved)

    def test_already_current_package_is_noop(self):
        self.assertIsNone(p.patch_archive(archive({CANONICAL:self.approved}),self.package,[self.mapping],self.art))

    def test_other_resolutions_keep_rgba_and_deterministic_bytes(self):
        for size in ['50x30','400x240']:
            a=p.resized(self.approved,size)
            self.assertEqual(a,p.resized(self.approved,size))
            with Image.open(io.BytesIO(a)) as image:
                self.assertEqual(image.size,tuple(map(int,size.split('x'))))
                self.assertEqual(image.mode,'RGBA')

    def test_rendering_is_repeatable_and_unsafe_zip_is_rejected(self):
        data=archive({OLD_ALIAS:self.old})
        self.assertEqual(p.patch_archive(data,self.package,[self.mapping],self.art)[0],p.patch_archive(data,self.package,[self.mapping],self.art)[0])
        with self.assertRaises(AssertionError):
            p.patch_archive(archive({'../'+OLD_ALIAS:self.old}),self.package,[self.mapping],self.art)


if __name__=='__main__':unittest.main()
