#!/usr/bin/env python3
"""Install the pinned approved graph textures into the owned skin directory."""
import base64,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def materialize(root=ROOT):
 record=json.loads((root/'design/openpli-graph-epg/atv-assets.json').read_text())
 target=root/'source/package-root/usr/share/enigma2/hd_glass17/epg/atv';target.mkdir(parents=True,exist_ok=True)
 for name,item in record['assets'].items():
  assert Path(name).name==name
  data=base64.b64decode(item['base64'],validate=True);assert hashlib.sha256(data).hexdigest()==item['sha256']
  (target/name).write_bytes(data)
 license_path=root/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/OPENATV-EPG-LICENSE.txt'
 license_path.write_bytes((root/'design/openpli-graph-epg/OPENATV-LICENSE.txt').read_bytes())
 print('Materialized %s pinned ATV graph textures'%len(record['assets']))
if __name__=='__main__':materialize()
