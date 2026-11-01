"""Check every new helper before packaging, including its exact size allowance."""
import hashlib
import json
from pathlib import Path
import struct
SPECS={'arm':(1,40,512*1024),'mipsel':(1,8,1024*1024),'aarch64':(2,183,1024*1024)}
def validate_helpers(root):
    root=Path(root);payload=root/'source/package-root'
    plugin=payload/'usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
    budget=16*1024*1024
    if not (plugin/'warderBitrateCompat.py').exists():return budget
    source_sha=hashlib.sha256((root/'tools/bitrate-helper/warder-bitrate.c').read_bytes()).hexdigest()
    assert not (payload/'usr/bin/btrGen17-arm').exists(),'Obsolete ARM helper must not be packaged'
    for name,(elf_class,machine,limit) in SPECS.items():
        path=payload/('usr/bin/warder-bitrate-'+name)
        raw=path.read_bytes()
        assert 0<len(raw)<=limit,'Unexpected helper size: '+name
        assert raw[:4]==b'\x7fELF' and raw[4]==elf_class and raw[5]==1
        assert int.from_bytes(raw[18:20],'little')==machine
        if elf_class==1:
            phoff=struct.unpack_from('<I',raw,28)[0];entry,count=struct.unpack_from('<HH',raw,42)
        else:
            phoff=struct.unpack_from('<Q',raw,32)[0];entry,count=struct.unpack_from('<HH',raw,54)
        assert count and phoff+entry*count<=len(raw)
        assert 3 not in [struct.unpack_from('<I',raw,phoff+i*entry)[0] for i in range(count)],'Static helper required'
        report_name='bitrate-helper-build.json' if name=='arm' else 'bitrate-helper-'+name+'-build.json'
        report=json.loads((root/'packages/test'/report_name).read_text())
        assert report['source_sha256']==source_sha and report['helper_sha256']==hashlib.sha256(raw).hexdigest()
        assert path.stat().st_mode&0o111==0o111
        budget+=len(raw)
    targets=json.loads((plugin/'warderBitrateTargets.json').read_text())
    report=json.loads((root/'packages/test/bitrate-helper-mipsel-build.json').read_text())
    assert targets['mipsel']['minimum_kernel']==report['minimum_kernel']
    assert targets['mipsel']['requires_fpu']==report['requires_fpu']
    return budget
