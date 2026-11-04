from pathlib import Path
import importlib.util, io, json, zipfile
from PIL import Image

p=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('publication',p/'publish-unchanged622-20261104.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
source=p.parent/'.approved-source'
if not source.exists():source=p.parent.parent/'source-repo'
plan,art=m.approved_inputs(source)
assert len(art)==1244
first=plan['mappings'][0]
sentinel=next(iter(art.values()))
buf=io.BytesIO()
with zipfile.ZipFile(buf,'w') as z:
 z.writestr(first['reference'],b'existing-approved-png-must-survive')
 z.writestr('1_0_1_DEAD_BEEF_1_820000_0_0_0.png',sentinel)
checks=0
for selector in sorted({x['selector_id'] for x in plan['mappings']}):
 for resolution in plan['sizes']:
  for style in plan['styles']:
   package={'selector_id':selector,'resolution':resolution,'family':'channel-'+style}
   packed,evidence=m.patch_archive(buf.getvalue(),package,plan['mappings'],art)
   if packed is None:
    assert all(x['reference']==first['reference'] for x in plan['mappings'] if x['selector_id']==selector)
    continue
   with zipfile.ZipFile(io.BytesIO(packed)) as z:
    assert z.read(first['reference'])==b'existing-approved-png-must-survive'
    assert z.read('1_0_1_DEAD_BEEF_1_820000_0_0_0.png')==sentinel
    for name in evidence['added']:
     row=next(x for x in plan['mappings'] if x['reference']==name)
     assert row['selector_id']==selector
     raw=z.read(name);assert raw==m.HELPER.resized(art[row['source_pixel_key'],style],resolution)
     assert Image.open(io.BytesIO(raw)).size==tuple(map(int,resolution.split('x')))
    assert not {x['reference'] for x in plan['excluded']}.intersection(z.namelist())
   checks+=1
assert checks>=174
print('PASS:',checks,'satellite/style/size cases; 1244 approved hashes; all existing bytes preserved; blocked references absent; no cross-satellite aliases')
