#!/usr/bin/env python3
"""Update only the selector runtime over the exact published 1.0.66 payload."""
from pathlib import Path
import argparse,ast,copy,gzip,hashlib,io,json,subprocess,tarfile,urllib.request
ROOT=Path(__file__).resolve().parents[1]
BASE_URL='https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/download/v1.0.66/enigma2-plugin-skins-fullhdglass_1.0.66_all.ipk'
BASE_SHA='6e207f7440331fa2fd1fac219cdd691377596bf4ee46bd15e0922f0fd5a1d7c9'
PREFIX='usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/'
ALLOWED=['plugin.py','txt.py','version','warderDialogSkins.py','warderPiconSync.py','history.txt','history.txtSk']
sha=lambda b:hashlib.sha256(b).hexdigest()
def unpack(raw):
 assert raw[:8]==b'!<arch>\n';offset=8;out={}
 while offset<len(raw):
  h=raw[offset:offset+60];size=int(h[48:58]);name=h[:16].decode().strip().rstrip('/');out[name]=raw[offset+60:offset+60+size];offset+=60+size+size%2
 assert set(out)=={'debian-binary','control.tar.gz','data.tar.gz'} and out['debian-binary']==b'2.0\n';return out

def rewrite(raw,replacements):
 out=io.BytesIO();seen=set();preserved={}
 with gzip.GzipFile(fileobj=out,mode='wb',filename='',mtime=0) as gz:
  with tarfile.open(fileobj=gz,mode='w',format=tarfile.GNU_FORMAT) as dest:
   with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as old:
    for m in old:
     info=copy.copy(m);name=m.name.removeprefix('./');data=old.extractfile(m).read() if m.isfile() else None
     if name in replacements:
      assert m.isfile();data=replacements[name];info.size=len(data);info.mtime=int(sha(data)[:8],16)&0x7fffffff;seen.add(name)
     elif m.isfile():preserved[name]=sha(data)
     dest.addfile(info,io.BytesIO(data) if data is not None else None)
 assert seen==set(replacements),(seen,set(replacements));return out.getvalue(),preserved

def read_files(raw):
 with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as a:return {m.name.removeprefix('./'):a.extractfile(m).read() for m in a if m.isfile()}

def main():
 a=argparse.ArgumentParser();a.add_argument('--baseline',type=Path);args=a.parse_args();raw=args.baseline.read_bytes() if args.baseline else urllib.request.urlopen(BASE_URL,timeout=120).read();assert sha(raw)==BASE_SHA;old=unpack(raw);old_files=read_files(old['data.tar.gz']);payload=ROOT/'source/package-root';plugin=payload/PREFIX;version=(plugin/'version').read_text().strip();assert version=='1.0.67'
 replacements={PREFIX+n:(plugin/n).read_bytes() for n in ALLOWED}
 for n,b in replacements.items():
  if n.endswith('.py'):compile(b,n,'exec')
 control=read_files(old['control.tar.gz']);old_control=control['control'].decode();assert 'Version: 1.0.66-1\n' in old_control;new_control=old_control.replace('Version: 1.0.66-1\n','Version: '+version+'-1\n');assert new_control==(ROOT/'source/control/control').read_text();new_data,preserved=rewrite(old['data.tar.gz'],replacements);new_meta,preserved_controls=rewrite(old['control.tar.gz'],{'control':new_control.encode()});actual=read_files(new_data);assert actual.keys()==old_files.keys();assert all(sha(actual[n])==h for n,h in preserved.items());assert all(actual[n]==b for n,b in replacements.items())
 # Legacy receiver preferences may refer to existing SATLIST row indices.
 for legacy in [False,True]:
  tables=[]
  for text in [old_files[PREFIX+'txt.py'].decode(),replacements[PREFIX+'txt.py'].decode()]:
   node=next(n for n in ast.parse(text).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SATLIST' for t in n.targets));scope={'L':legacy};exec(compile(ast.Module(body=[node],type_ignores=[]),'packaged-SATLIST','exec'),scope);tables.append(scope['SATLIST'])
  assert tables[1]==tables[0]
 out=bytearray(b'!<arch>\n')
 for name,b in [('debian-binary',b'2.0\n'),('control.tar.gz',new_meta),('data.tar.gz',new_data)]:
  out.extend(('%-16s%-12s%-6s%-6s%-8s%-10s`\n'%(name+'/',0,0,0,'100644',len(b))).encode());out.extend(b)
  if len(b)%2:out.extend(b'\n')
 d=ROOT/'packages';d.mkdir(exist_ok=True);p=d/('enigma2-plugin-skins-fullhdglass_'+version+'_all.ipk');p.write_bytes(out);p.with_suffix('.ipk.sha256').write_text(sha(out)+'  '+p.name+'\n')
 record={'status':'VERIFIED_SOURCE_DELTA_PACKAGE','version':version,'baseline_sha256':BASE_SHA,'sha256':sha(out),'bytes':len(out),'changed_payload_files':sorted(replacements),'unchanged_payload_files_verified':len(preserved),'unchanged_control_files_verified':len(preserved_controls),'all_radio_epg_artwork_and_other_payload_preserved':True,'installed_identity':'enigma2-plugin-skins-fullhdglass-warder-evolution','physical_receiver_tested':False};r=ROOT/'reports/selector-presentation-20261105';r.mkdir(parents=True,exist_ok=True);(r/'ipk-verification.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record),flush=True)
if __name__=='__main__':main()
