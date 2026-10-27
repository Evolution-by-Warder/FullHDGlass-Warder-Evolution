#!/usr/bin/env python3
import importlib.util
import io
from pathlib import Path
import unittest
import zipfile

spec=importlib.util.spec_from_file_location('publication',Path(__file__).with_name('append-dab-satellite-picons.py'))
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
NAME='4115_0_2_1019_C98_3_EB0000_1019_100D_10BC.png'

def archive(files):
    out=io.BytesIO()
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in files.items():z.writestr(name,data)
    return out.getvalue()

class IntegrationTests(unittest.TestCase):
    def test_existing_files_are_preserved_and_radio_is_added(self):
        old=archive({'1_0_1_1_1_1_EB0000_0_0_0.png':b'original','notes.txt':b'credits'})
        data,added,preserved=module.append_archive(old,{NAME:b'approved'})
        self.assertEqual((added,preserved),(1,2))
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            self.assertEqual(z.read(NAME),b'approved');self.assertEqual(z.read('notes.txt'),b'credits')
    def test_repeating_identical_integration_is_a_no_op(self):
        old=archive({NAME:b'approved'});self.assertEqual(module.append_archive(old,{NAME:b'approved'}),(old,0,1))
    def test_conflicting_existing_logo_is_not_silently_replaced(self):
        with self.assertRaisesRegex(ValueError,'differs'):module.append_archive(archive({NAME:b'old'}),{NAME:b'new'})
    def test_position_comes_from_the_exact_namespace(self):
        self.assertEqual(module.position(NAME),235)
        self.assertEqual(module.position(NAME.replace('EB0000','C00000')),192)
        with self.assertRaises(ValueError):module.position('../../station.png')

if __name__=='__main__':unittest.main()
