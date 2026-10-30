import importlib.util,io,pathlib,unittest,zipfile
from PIL import Image

spec=importlib.util.spec_from_file_location('publisher',pathlib.Path(__file__).with_name('publish-picons-assimilated-20261030.py'))
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
REF='1_0_19_1447_7EE_2_11A0000_0_0_0.png'
ALIAS='1_0_1_1447_7EE_2_11A0000_0_0_0.png'
OTHER='1_0_19_1447_7EE_2_C00000_0_0_0.png'
def png(colour):
 b=io.BytesIO();Image.new('RGBA',(220,132),colour).save(b,format='PNG');return b.getvalue()
def archive(entries):
 b=io.BytesIO()
 with zipfile.ZipFile(b,'w') as z:
  for n,v in entries.items():z.writestr(n,v)
 return b.getvalue()
class Tests(unittest.TestCase):
 def setUp(self):
  self.old=png('blue');self.new=png('red');self.map={'slug':'disney','identity':list(p.identity(REF)),'selector_id':'282E','reference':REF,'references':[REF,ALIAS]};self.pkg={'selector_id':'282E','family':'channel-white','resolution':'220x132'};self.art={('disney','white'):self.new}
 def run_patch(self,entries,pkg=None):return p.patch_archive(archive(entries),pkg or self.pkg,[self.map],self.art)
 def test_adds_both_verified_types_and_preserves_other_satellite(self):
  raw,r=self.run_patch({OTHER:self.old})
  with zipfile.ZipFile(io.BytesIO(raw)) as z:
   self.assertEqual(z.read(OTHER),self.old);self.assertEqual(z.read(REF),self.new);self.assertEqual(z.read(ALIAS),self.new)
  self.assertEqual(r['replaced'],[]);self.assertEqual(len(r['added']),2)
 def test_existing_approved_alias_is_reused_without_replacement(self):
  raw,r=self.run_patch({ALIAS:self.old,OTHER:self.new})
  with zipfile.ZipFile(io.BytesIO(raw)) as z:
   self.assertEqual(z.read(ALIAS),self.old);self.assertEqual(z.read(REF),self.old);self.assertEqual(z.read(OTHER),self.new)
  self.assertEqual(r['added'],[REF])
 def test_complete_existing_art_is_noop_even_if_different(self):
  self.assertIsNone(self.run_patch({REF:self.old,ALIAS:self.old}))
 def test_no_unverified_provider_membership_is_added(self):
  self.assertIsNone(self.run_patch({OTHER:self.old},dict(self.pkg,selector_id='SKYLINK')))
 def test_unsafe_archive_is_rejected(self):
  with self.assertRaises(AssertionError):self.run_patch({'../'+OTHER:self.old})
 def test_unverified_cross_satellite_alias_is_rejected(self):
  self.map['references'].append(OTHER)
  with self.assertRaises(AssertionError):self.run_patch({})
 def test_deterministic_sizes_and_pixel_dimensions(self):
  self.assertEqual(self.run_patch({})[0],self.run_patch({})[0])
  for size in ('50x30','400x240'):
   raw,_=self.run_patch({},dict(self.pkg,resolution=size))
   with zipfile.ZipFile(io.BytesIO(raw)) as z,Image.open(io.BytesIO(z.read(REF))) as im:self.assertEqual(im.size,tuple(map(int,size.split('x'))))

if __name__=='__main__':unittest.main()
