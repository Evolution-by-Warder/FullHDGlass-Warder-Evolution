#!/usr/bin/env python3
"""Package the UI candidate without changing artwork, translations or feeds."""
import argparse
import shutil
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[1]
PLUGIN=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--help-previews',type=Path)
    args=parser.parse_args()
    version=(PLUGIN/'version').read_text().strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+(?:-test\d+)?',version):raise SystemExit('Numbered stable or TEST version required')
    # Verify the actual decoded TV background, not only the OpenWebif JPEG.
    subprocess.run(['python3',str(ROOT/'tools/build-radio-background.py')],check=True)
    control=ROOT/'source/control'
    if 'Version: '+version+'-1\n' not in (control/'control').read_text():raise SystemExit('Control version mismatch')
    spec=importlib.util.spec_from_file_location('stable_archive',ROOT/'tools/build-release-ipk.py')
    archive=importlib.util.module_from_spec(spec);spec.loader.exec_module(archive)
    optimizer_spec=importlib.util.spec_from_file_location('png_optimizer',ROOT/'tools/optimize-png.py')
    optimizer=importlib.util.module_from_spec(optimizer_spec);optimizer_spec.loader.exec_module(optimizer)
    output=ROOT/'packages/test';output.mkdir(parents=True,exist_ok=True)
    package_id=next(line.split(':',1)[1].strip() for line in (control/'control').read_text().splitlines() if line.startswith('Package:'))
    if package_id not in ('enigma2-skin-fullhdglass17','enigma2-plugin-skins-fullhdglass-warder-evolution'):raise SystemExit('Unexpected package identity')
    prefix=package_id if package_id.startswith('enigma2-plugin-') else 'enigma2-skin-fullhdglass-warder-evolution'
    package=output/(prefix+'_'+version+'_all.ipk')
    with tempfile.TemporaryDirectory() as folder:
        work=Path(folder);(work/'debian-binary').write_bytes(b'2.0\n')
        archive.archive(control,work/'control.tar.gz')
        payload=work/'payload'
        shutil.copytree(ROOT/'source/package-root',payload)
        compression=optimizer.optimize_tree(payload)
        archive.archive(payload,work/'data.tar.gz',payload=True)
        subprocess.run(['ar','rcsD',str(package),'debian-binary','control.tar.gz','data.tar.gz'],cwd=work,check=True)
    checksum=hashlib.sha256(package.read_bytes()).hexdigest()
    package.with_suffix('.ipk.sha256').write_text(checksum+'  '+package.name+'\n')
    download=output/('enigma2-plugin-skins-fullhdglass_'+version+'_all.ipk')
    download.write_bytes(package.read_bytes())
    download.with_suffix('.ipk.sha256').write_text(checksum+'  '+download.name+'\n')
    info={'version':version,'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
          'package':package.name,'sha256':checksum,'bytes':package.stat().st_size,
          'stable_feed_modified':False,'receiver_validated':False,'scope':'small IPK with optional asynchronous preview downloads', 'png_compression':{'files':len(compression),'saved_bytes':sum(x['before']-x['after'] for x in compression),'lossless':True}}
    (output/'settings-ui-build.json').write_text(json.dumps(info,indent=2)+'\n')
    print(download);print(checksum)


if __name__=='__main__':main()

