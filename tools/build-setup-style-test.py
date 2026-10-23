#!/usr/bin/env python3
"""Package the UI candidate without changing artwork, translations or feeds."""
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
    version=(PLUGIN/'version').read_text().strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+-test\d+',version):raise SystemExit('TEST version required')
    control=ROOT/'source/control'
    if 'Version: '+version+'-1\n' not in (control/'control').read_text():raise SystemExit('Control version mismatch')
    spec=importlib.util.spec_from_file_location('stable_archive',ROOT/'tools/build-release-ipk.py')
    archive=importlib.util.module_from_spec(spec);spec.loader.exec_module(archive)
    output=ROOT/'packages/test';output.mkdir(parents=True,exist_ok=True)
    package=output/('enigma2-skin-fullhdglass-warder-evolution_'+version+'_all.ipk')
    with tempfile.TemporaryDirectory() as folder:
        work=Path(folder);(work/'debian-binary').write_bytes(b'2.0\n')
        archive.archive(control,work/'control.tar.gz')
        archive.archive(ROOT/'source/package-root',work/'data.tar.gz',payload=True)
        subprocess.run(['ar','rcsD',str(package),'debian-binary','control.tar.gz','data.tar.gz'],cwd=work,check=True)
    checksum=hashlib.sha256(package.read_bytes()).hexdigest()
    package.with_suffix('.ipk.sha256').write_text(checksum+'  '+package.name+'\n')
    info={'version':version,'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
          'package':package.name,'sha256':checksum,'bytes':package.stat().st_size,
          'stable_feed_modified':False,'receiver_validated':False,'scope':'settings presentation only'}
    (output/'settings-ui-build.json').write_text(json.dumps(info,indent=2)+'\n')
    print(package);print(checksum)


if __name__=='__main__':main()
