#!/usr/bin/env python3
import importlib.util,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('activate',ROOT/'tools/activate-fullhdglass-1.0.65.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.C;old=m.payload((ROOT/'reports/fullhdglass-1.0.65/candidate.ipk').read_bytes());new=m.payload((ROOT/c['package']).read_bytes());assert old.keys()==new.keys()
prefix='usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/';compared=0
for name,value in old.items():
 if name in (prefix+'version',prefix+'history.txt',prefix+'history.txtSk'):continue
 other=new[name]
 if name in (prefix+'plugin.py',prefix+'warderDialogSkins.py'):
  pattern=rb'(<eLabel\b(?=[^>]*\bposition="1680,70")[^>]*\btext=")[^"<>]*(")'
  value=re.sub(pattern,rb'\1VERSION\2',value);other=re.sub(pattern,rb'\1VERSION\2',other)
 assert value==other,name
 compared+=1
assert new[prefix+'version'].decode().strip()==c['version']
for name in ('history.txt','history.txtSk'):assert new[prefix+name].decode().startswith('FullHDGlass '+c['version'])
print('PASS:',compared,'approved test2 payload files identical; only version, history and generated labels differ')
