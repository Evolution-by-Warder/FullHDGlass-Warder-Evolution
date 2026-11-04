from pathlib import Path
import importlib.util,json,io,zipfile,hashlib
from PIL import Image
p=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('publish11',p/'publish-warder-approved11-20261104.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
root=p.parent/'.approved-source';plan=json.load(open(root/m.PROVENANCE/'publication-plan.json'));art={(d['slug'],sty):(root/e['path']).read_bytes() for d in plan['artwork'] for sty,e in d['outputs'].items()};assert len(art)==33
sentinel=next(iter(art.values()));buf=io.BytesIO()
with zipfile.ZipFile(buf,'w') as z:z.writestr('1_0_1_DEAD_BEEF_1_820000_0_0_0.png',sentinel)
count=0;pngs=0
for selector in sorted({d['selector_id'] for d in plan['mappings']}):
 for res in ('50x30','220x132','400x240'):
  for sty in ('transparent','white','black'):
   package=dict(selector_id=selector,resolution=res,family='channel-'+sty);packed,e=m.patch_archive(buf.getvalue(),package,plan['mappings'],art)
   with zipfile.ZipFile(io.BytesIO(packed)) as z:
    assert z.read('1_0_1_DEAD_BEEF_1_820000_0_0_0.png')==sentinel
    for mapping in plan['mappings']:
     if mapping['selector_id']!=selector:continue
     raw=z.read(mapping['reference']);assert raw==m.resized(art[(mapping['slug'],sty)],res);assert Image.open(io.BytesIO(raw)).size==tuple(map(int,res.split('x')));pngs+=1
   count+=1
# A provider package receives no unrelated references; a present exact approved reference is updated.
assert m.patch_archive(buf.getvalue(),dict(selector_id='SKYLINK',resolution='220x132',family='channel-white'),plan['mappings'],art) is None
mapping=plan['mappings'][0];b=io.BytesIO()
with zipfile.ZipFile(b,'w') as z:z.writestr(mapping['reference'],sentinel);z.writestr('unrelated.png',sentinel)
packed,e=m.patch_archive(b.getvalue(),dict(selector_id='SKYLINK',resolution='220x132',family='channel-white'),plan['mappings'],art)
with zipfile.ZipFile(io.BytesIO(packed)) as z:assert z.read(mapping['reference'])==art[(mapping['slug'],'white')];assert z.read('unrelated.png')==sentinel
assert count==63 and pngs==99
print('PASS: 63 package cases, 99 approved PNG variants, untouched PNG preservation, provider exact-reference scope, no inferred aliases')
