#!/usr/bin/env python3
"""Build reviewed static ARM/MIPSel helpers and probe their actual targets."""
import hashlib
import json
from pathlib import Path
import re
import resource
import subprocess
import tempfile
import tarfile
from urllib.request import urlopen
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'tools/bitrate-helper/warder-bitrate.c'
folder=ROOT/'packages/test';folder.mkdir(parents=True,exist_ok=True)
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
ZIG_URL='https://ziglang.org/download/0.13.0/zig-linux-x86_64-0.13.0.tar.xz'
ZIG_SHA='d45312e61ebcc48032b77bc4cf7fd6915c11fa16e4aad116b66c9468211230ea'
def soft_mips_compiler():
    work=Path(tempfile.gettempdir())/'warder-bitrate-zig-0.13'
    binary=work/'zig-linux-x86_64-0.13.0/zig'
    if not binary.exists():
        work.mkdir(parents=True,exist_ok=True)
        with urlopen(ZIG_URL,timeout=60) as response:raw=response.read()
        assert hashlib.sha256(raw).hexdigest()==ZIG_SHA,'Pinned compiler archive checksum mismatch'
        archive=work/'zig.tar.xz';archive.write_bytes(raw)
        # The exact upstream archive is verified before any extraction.
        with tarfile.open(archive) as source:source.extractall(work)
    binary.chmod(0o755)
    licenses=ROOT/'source/package-root/usr/share/doc/fullhdglass'
    licenses.mkdir(parents=True,exist_ok=True)
    (licenses/'bitrate-musl-COPYRIGHT').write_bytes((binary.parent/'lib/libc/musl/COPYRIGHT').read_bytes())
    (licenses/'bitrate-zig-LICENSE').write_bytes((binary.parent/'LICENSE').read_bytes())
    return [str(binary),'cc','-target','mipsel-linux-musl','-mcpu=mips32r2+soft_float','-msoft-float','-g0']
targets={}
for name,prefix,emulator,machine,extra in (
    ('arm','arm-linux-gnueabihf','qemu-arm',40,[]),
    ('mipsel','mipsel-linux-gnu','qemu-mipsel',8,[]),
    ('aarch64','aarch64-linux-gnu','qemu-aarch64',183,[]),
):
    output=ROOT/('source/package-root/usr/bin/warder-bitrate-'+name)
    output.parent.mkdir(parents=True,exist_ok=True)
    compiler_command=soft_mips_compiler() if name=='mipsel' else [prefix+'-gcc']
    flags=['-std=c99','-O2','-Wall','-Wextra','-static']+extra
    subprocess.run([*compiler_command,*flags,'-Werror','-Wl,--build-id=sha1',str(source),'-o',str(output)],check=True)
    subprocess.run([prefix+'-strip','--strip-all',str(output)],check=True)
    output.chmod(0o755);data=output.read_bytes()
    assert data[:4]==b'\x7fELF' and data[4]==(2 if name=='aarch64' else 1) and data[5]==1 and int.from_bytes(data[18:20],'little')==machine,'Wrong helper ELF target'
    if name=='mipsel':assert int.from_bytes(data[36:40],'little')&0xf0000000==0x70000000,'MIPS32r2 required'
    segments=subprocess.check_output([prefix+'-readelf','-l',str(output)],text=True)
    assert 'INTERP' not in segments,'Helper must not need the receiver dynamic loader'
    notes=subprocess.check_output([prefix+'-readelf','-n',str(output)],text=True)
    minimum=re.search(r'OS: Linux, ABI: (\d+)\.(\d+)\.(\d+)',notes)
    assert minimum or name=='mipsel','Explicit minimum Linux ABI note required'
    minimum_kernel=list(map(int,minimum.groups())) if minimum else [3,2,0]
    if name=='mipsel':
        abi=subprocess.check_output([prefix+'-readelf','-A',str(output)],text=True)
        assert 'FP ABI: Soft float' in abi,'MIPSel helper must not require an FPU'
    probes={}
    with tempfile.TemporaryDirectory() as work:
        unit=str(Path(work)/('unit-'+name))
        subprocess.run([*compiler_command,*flags,'-Wno-unused-function',str(ROOT/'tools/bitrate-helper/unit.c'),'-o',unit],check=True)
        for cpu in (['24Kc','24Kf'] if name=='mipsel' else ['default']):
            command=[emulator]+([] if cpu=='default' else ['-cpu',cpu])+['-r','.'.join(map(str,minimum_kernel)),unit]
            test=subprocess.run(command,capture_output=True,text=True,timeout=30)
            cli=subprocess.run(command[:-1]+[str(output),'0','0','8191','5106'],capture_output=True,text=True,timeout=30)
            missing=subprocess.run(command[:-1]+[str(output),'0','0','5101','5106'],capture_output=True,text=True,timeout=30)
            probes[cpu]={'passed':test.returncode==0 and cli.returncode==2 and 'usage:' in cli.stderr and missing.returncode==2 and 'open /dev/dvb/' in missing.stderr,'returncode':test.returncode,'cli_checked':cli.returncode==2,'missing_device_checked':missing.returncode==2 and 'open /dev/dvb/' in missing.stderr}
            print(name,cpu,test.stdout.strip(),test.stderr.strip()[:120])
    requires_fpu=name=='mipsel' and not probes['24Kc']['passed']
    assert all(probe['passed'] for probe in probes.values()),'Target parser/rate or CLI test failed'
    if name=='mipsel':assert not requires_fpu,'Both no-FPU and FPU MIPS CPUs must work'
    execution=[emulator]+(['-cpu','24Kf' if requires_fpu else '24Kc'] if name=='mipsel' else [])+['-r','.'.join(map(str,minimum_kernel))]
    check=subprocess.run(execution+[str(output),'0','0','8191','5106'],capture_output=True,text=True,timeout=30)
    assert check.returncode==2 and 'usage:' in check.stderr,'Packaged helper must execute and reject invalid PIDs'
    report={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'helper_sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'compiler':subprocess.check_output([*compiler_command,'--version'],text=True).splitlines()[0],'architecture':name+', static little endian','minimum_kernel':minimum_kernel,'requires_fpu':requires_fpu if name=='mipsel' else None,'qemu_probes':probes,'legacy_helpers_modified':False}
    if name=='mipsel':report.update(toolchain_url=ZIG_URL,toolchain_archive_sha256=ZIG_SHA,libc='musl, software floating point')
    (folder/('bitrate-helper-build.json' if name=='arm' else 'bitrate-helper-'+name+'-build.json')).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    if name=='mipsel':targets[name]={'isa':'mips32r2','byteorder':'little','minimum_kernel':minimum_kernel,'requires_fpu':requires_fpu}
path=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderBitrateTargets.json'
path.write_text(json.dumps(targets,indent=2)+'\n')
