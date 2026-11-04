"""Exercise full build, preservation, adding aliases and both real installers on compact archives."""
from pathlib import Path
import copy,hashlib,importlib.util,io,json,tempfile,zipfile
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('canal_publisher',ROOT/'tools/publish-canal-owner-20261104.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
# Override only the fixture destination; use exact approved artwork and actual runtimes.
source=m.SOURCE;art=m.ART;source_root=m.ROOT
with tempfile.TemporaryDirectory() as tmp:
 root=Path(tmp);m.ROOT=root;m.DATA=root/'assets/warder/downloads/picons/channels';m.DATA.mkdir(parents=True);m.REPORT=root/'reports/canal-owner-publication-20261104.json';m.SOURCE=source;m.ART=art
 runtime=root/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17';runtime.mkdir(parents=True)
 for name in ['warderPiconSync.py','plugin.py']:(runtime/name).symlink_to(source_root/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'/name)
 doc=json.loads((source_root/'assets/warder/downloads/picons/channels/manifest.json').read_text());plan=json.loads((art/'publication-plan.json').read_text());parts={p['filename']:p for p in doc['parts']};fixture={};old=io.BytesIO();Image.new('RGBA',(220,132),'red').save(old,format='PNG');preserved=old.getvalue()
 original_families={p['selector_id'] for p in doc['packages'] if p['selector_id'] in plan['target_selectors']};assert len(original_families)==5
 for p in doc['packages']:
  if p['selector_id'] not in plan['target_selectors']:continue
  mappings=[r for r in plan['references'] if p['selector_id'] in r['target_selectors']];names=[r['reference'] for r in mappings][1:];names+=['1_0_19_FFFC_C82_3_'+mappings[0]['namespace']+'_0_0_0.png']
  b=io.BytesIO()
  with zipfile.ZipFile(b,'w',zipfile.ZIP_DEFLATED) as z:
   for n in names:z.writestr(n,preserved)
  raw=b.getvalue();h=m.sha(raw);filename=f'warder-{p["selector_id"].lower()}-{p["resolution"]}-{p["family"][8:]}-{h[:16]}.zip';part=filename+'.part00';fixture[m.RAW+part]=raw;parts[part]=dict(filename=part,bytes=len(raw),sha256=h);p.update(filename=filename,parts=[m.RAW+part],bytes=len(raw),sha256=h,png_count=len(names))
  if 'included_references' in p:p['included_references']=[n[:-4] for n in names]
 doc['parts']=list(parts.values());(m.DATA/'manifest.json').write_text(json.dumps(doc));(m.DATA/'SHA256SUMS').write_text('')
 m.fetch=lambda url,head=False:fixture[url]
 m.build();report=json.loads(m.REPORT.read_text());assert report['changed_packages']==45 and report['skin_actual_installer_checks']==report['piconhub_actual_engine_checks']==45
 assert all(len(r['added'])==1 and r['unrelated_pngs_preserved']==1 for r in report['packages']);assert sum(len(r['added'])+len(r['replaced']) for r in report['packages'])==261
 print('COMPACT ARCHIVE REGRESSION PASSED: 45 actual skin installs, 45 actual hub installs, added references and unrelated PNG preservation')
