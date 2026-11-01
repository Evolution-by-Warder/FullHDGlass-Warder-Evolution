#!/usr/bin/env python3
"""Build the reviewed ARM helper; keep every legacy helper unchanged."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'tools/bitrate-helper/warder-bitrate.c'
output=ROOT/'source/package-root/usr/bin/warder-bitrate-arm'
output.parent.mkdir(parents=True,exist_ok=True)
compiler='arm-linux-gnueabihf-gcc'
subprocess.run([compiler,'-std=c99','-O2','-Wall','-Wextra','-Werror','-static','-Wl,--build-id=sha1',str(source),'-o',str(output)],check=True)
subprocess.run(['arm-linux-gnueabihf-strip','--strip-all',str(output)],check=True)
output.chmod(0o755)
data=output.read_bytes()
assert data[:6]==b'\x7fELF\x01\x01' and int.from_bytes(data[18:20],'little')==40,'ARM ELF32 required'
segments=subprocess.check_output(['arm-linux-gnueabihf-readelf','-l',str(output)],text=True)
assert 'INTERP' not in segments,'Helper must not require a receiver-specific dynamic loader'
# Exercise the ARM build of the parser tests, not only the native host build.
with tempfile.TemporaryDirectory() as folder:
    unit=str(Path(folder)/'unit-arm')
    subprocess.run([compiler,'-std=c99','-O2','-Wall','-Wextra','-Wno-unused-function','-static',str(ROOT/'tools/bitrate-helper/unit.c'),'-o',unit],check=True)
    subprocess.run(['qemu-arm',unit],check=True)
check=subprocess.run(['qemu-arm',str(output),'0','0','8191','5106'],capture_output=True,text=True)
assert check.returncode==2 and 'usage:' in check.stderr,'Packaged ARM helper must execute and reject invalid PIDs'
report={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'helper_sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'compiler':subprocess.check_output([compiler,'--version'],text=True).splitlines()[0],'architecture':'ARM EABI5, static','legacy_helpers_modified':False}
folder=ROOT/'packages/test';folder.mkdir(parents=True,exist_ok=True)
(folder/'bitrate-helper-build.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
