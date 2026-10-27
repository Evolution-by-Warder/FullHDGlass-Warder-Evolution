#!/usr/bin/env python3
import importlib.util,io,unittest,warnings,zipfile
from pathlib import Path
spec=importlib.util.spec_from_file_location('publisher',Path(__file__).with_name('publish-regional-radio.py'));p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
A='1_0_2_133A_CA2_3_EB0000_0_0_0.png';ALIAS='1_0_A_133A_CA2_3_EB0064_0_0_0.png';B='1_0_2_133B_CA2_3_EB0000_0_0_0.png';DAB='4115_0_2_1019_C98_3_EB0000_1019_100D_10BC.png'
def archive(items):
 out=io.BytesIO()
 with warnings.catch_warnings():
  warnings.simplefilter('ignore',UserWarning)
  with zipfile.ZipFile(out,'w') as z:
   for n,b in items:z.writestr(n,b)
 return out.getvalue()
def unpack(raw):
 with zipfile.ZipFile(io.BytesIO(raw)) as z:return {n:z.read(n) for n in z.namelist()}
class PublicationTests(unittest.TestCase):
 def test_replace_only_matching_station_and_preserve_dab_bytes(self):
  result,r=p.patch_archive(archive([(A,b'old'),(B,b'keep'),(DAB,b'dab-unchanged')]),{A:b'approved'},True)
  self.assertEqual(unpack(result),{A:b'approved',B:b'keep',DAB:b'dab-unchanged'});self.assertEqual(r['replaced'],[A]);self.assertEqual(r['dab_pngs_preserved'],1)
 def test_service_type_and_namespace_aliases_receive_same_approved_art(self):
  result,r=p.patch_archive(archive([(ALIAS,b'old')]),{A:b'approved'})
  self.assertEqual(unpack(result),{A:b'approved',ALIAS:b'approved'});self.assertEqual(r['added'],[A])
 def test_full_satellite_adds_missing_authorized_reference(self):
  result,r=p.patch_archive(archive([(B,b'keep')]),{A:b'approved'},True)
  self.assertEqual(unpack(result),{A:b'approved',B:b'keep'});self.assertEqual(r['added'],[A])
 def test_provider_does_not_gain_a_station_it_does_not_carry(self):
  original=archive([(B,b'keep')]);result,r=p.patch_archive(original,{A:b'approved'})
  self.assertEqual(result,original);self.assertEqual(r['added'],[])
 def test_identical_art_preserves_entire_original_archive(self):
  original=archive([(A,b'approved')]);result,r=p.patch_archive(original,{A:b'approved'},True)
  self.assertEqual(result,original);self.assertEqual(r['replaced'],[])
 def test_unsafe_input_and_approved_paths_are_rejected(self):
  with self.assertRaises(ValueError):p.patch_archive(archive([('../'+A,b'bad')]),{A:b'approved'})
  with self.assertRaises(ValueError):p.patch_archive(archive([(A,b'old')]),{'../'+A:b'approved'})
 def test_duplicate_input_is_rejected(self):
  with self.assertRaises(ValueError):p.patch_archive(archive([(A,b'one'),(A,b'two')]),{A:b'approved'})
 def test_unrelated_identical_old_logo_does_not_define_service_identity(self):
  result,r=p.patch_archive(archive([(A,b'shared-old'),(B,b'shared-old')]),{A:b'new'})
  self.assertEqual(unpack(result)[B],b'shared-old')
 def test_explicit_canal_completion_adds_all_nine_carried_radio_references(self):
  art={'1_0_2_%X_CA2_3_EB0000_0_0_0.png'%sid:('approved-%d'%sid).encode() for sid in range(0x1350,0x1359)}
  for selector in ('CANALPLUS_SK','CANALPLUS_CZ'):
   original=archive([(B,b'unrelated-provider-tv')])
   result,r=p.patch_archive(original,art,p.complete_scope(selector,True))
   self.assertEqual(set(unpack(result)),set(art)|{B});self.assertEqual(unpack(result)[B],b'unrelated-provider-tv');self.assertEqual(len(r['added']),9)
   for name,data in art.items():self.assertEqual(unpack(result)[name],data)
 def test_canal_completion_does_not_expand_other_operator_archives(self):
  original=archive([(B,b'keep')]);result,r=p.patch_archive(original,{A:b'approved'},p.complete_scope('FREESAT',True))
  self.assertEqual(result,original);self.assertEqual(r['added'],[])
if __name__=='__main__':unittest.main()
