import importlib.util,pathlib,unittest
spec=importlib.util.spec_from_file_location('batches',pathlib.Path(__file__).with_name('push-picon-archive-batches.py'))
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
def part(n,size):return {'filename':f'warder-130e-220x132-transparent-0123456789abcdef.zip.part{n:02d}','bytes':size}
class Tests(unittest.TestCase):
 def test_all_parts_appear_once_and_no_pack_exceeds_limit(self):
  rows=[part(0,6),part(1,4),part(2,7),part(3,2),part(4,3)]
  groups=p.batches(rows,10)
  self.assertEqual([x for g in groups for x in g],rows)
  self.assertTrue(all(sum(x['bytes'] for x in g)<=10 for g in groups));self.assertEqual(len(groups),3)
 def test_one_oversized_part_is_rejected_before_any_write(self):
  with self.assertRaises(AssertionError):p.batches([part(0,11)],10)
 def test_duplicate_or_unsafe_part_name_is_rejected(self):
  with self.assertRaises(AssertionError):p.batches([part(0,4),part(0,4)],10)
  with self.assertRaises(AssertionError):p.batches([{'filename':'../../update-production.json','bytes':1}],10)
 def test_empty_and_exact_boundary_are_handled_without_empty_commits(self):
  self.assertEqual(p.batches([],10),[])
  self.assertEqual(p.batches([part(0,10),part(1,10)],10),[[part(0,10)],[part(1,10)]])
if __name__=='__main__':unittest.main()
