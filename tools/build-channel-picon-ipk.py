#!/usr/bin/env python3
"""Apply the reviewed picon delta to the exact published 1.0.68 payload."""
import argparse
import copy
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import tarfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
VERSION = '1.0.69'
BASE_SHA = '28f83dd386dd81e7e4427bbf943ea2bccbffd9e774682b453940d851590061a2'
BASE_URL = 'https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/download/v1.0.68/enigma2-plugin-skins-fullhdglass_1.0.68_all.ipk'
PLUGIN = 'usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/'
CHANGED = tuple(PLUGIN+n for n in ('plugin.py','warderDialogSkins.py','version','history.txt','history.txtSk','warderChannelPicons.py','warderUiText.py')) + ('usr/lib/enigma2/python/Components/Renderer/g17RefTV3.py',)
REPORT = ROOT/'reports/channel-picons-1.0.69'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unpack(raw):
    assert raw[:8] == b'!<arch>\n'
    offset, members = 8, {}
    while offset < len(raw):
        header=raw[offset:offset+60]
        assert len(header)==60 and header[-2:]==b'`\n'
        size=int(header[48:58]); name=header[:16].decode().strip().rstrip('/')
        assert name not in members
        members[name]=raw[offset+60:offset+60+size]
        assert len(members[name])==size
        offset+=60+size+size%2
    assert set(members)=={'debian-binary','control.tar.gz','data.tar.gz'}
    assert members['debian-binary']==b'2.0\n'
    return members


def read_files(raw):
    with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as archive:
        return {m.name.removeprefix('./'):archive.extractfile(m).read() for m in archive if m.isfile()}


def rewrite(raw, replacements, additions=None):
    output=io.BytesIO(); seen=set(); preserved={}
    additions=additions or {}
    with gzip.GzipFile(fileobj=output,mode='wb',filename='',mtime=0) as compressed:
        with tarfile.open(fileobj=compressed,mode='w',format=tarfile.GNU_FORMAT) as target:
            with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as source:
                for member in source:
                    info=copy.copy(member); name=member.name.removeprefix('./')
                    assert name not in additions
                    data=source.extractfile(member).read() if member.isfile() else None
                    if name in replacements:
                        assert member.isfile()
                        data=replacements[name]; info.size=len(data)
                        info.mtime=int(sha(data)[:8],16)&0x7fffffff
                        seen.add(name)
                    elif member.isfile():
                        preserved[name]=sha(data)
                    target.addfile(info,io.BytesIO(data) if data is not None else None)
            for name,data in additions.items():
                info=tarfile.TarInfo('./'+name)
                info.size=len(data); info.mode=0o644; info.uid=info.gid=0
                info.mtime=int(sha(data)[:8],16)&0x7fffffff
                target.addfile(info,io.BytesIO(data))
    assert seen==set(replacements)
    return output.getvalue(),preserved


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--baseline',type=Path)
    args=parser.parse_args()
    raw=args.baseline.read_bytes() if args.baseline else urllib.request.urlopen(BASE_URL,timeout=120).read()
    assert sha(raw)==BASE_SHA
    old=unpack(raw); before=read_files(old['data.tar.gz'])
    payload=ROOT/'source/package-root'
    assert (payload/PLUGIN/'version').read_text().strip()==VERSION
    replacements={name:(payload/name).read_bytes() for name in CHANGED}
    additions={}
    for name,data in dict(replacements,**additions).items():
        if name.endswith('.py'):compile(data,name,'exec')
    control=read_files(old['control.tar.gz'])
    original_control=control['control'].decode()
    assert original_control.count('Version: 1.0.68-1\n')==1
    new_control=original_control.replace('Version: 1.0.68-1\n','Version: '+VERSION+'-1\n')
    assert new_control==(ROOT/'source/control/control').read_text()
    data,preserved=rewrite(old['data.tar.gz'],replacements,additions)
    meta,preserved_controls=rewrite(old['control.tar.gz'],{'control':new_control.encode()})
    actual=read_files(data)
    assert set(actual)==set(before)
    assert all(sha(actual[name])==digest for name,digest in preserved.items())
    assert all(actual[name]==value for name,value in dict(replacements,**additions).items())
    assert all(read_files(meta)[name]==control[name] for name in preserved_controls)
    result=bytearray(b'!<arch>\n')
    for name,value in [('debian-binary',b'2.0\n'),('control.tar.gz',meta),('data.tar.gz',data)]:
        result.extend(('%-16s%-12s%-6s%-6s%-8s%-10s`\n'%(name+'/',0,0,0,'100644',len(value))).encode())
        result.extend(value)
        if len(value)%2:result.extend(b'\n')
    assert len(result)<len(raw)+65536
    output=ROOT/'packages'; output.mkdir(exist_ok=True)
    package=output/('enigma2-plugin-skins-fullhdglass_'+VERSION+'_all.ipk')
    package.write_bytes(result)
    package.with_suffix('.ipk.sha256').write_text(sha(result)+'  '+package.name+'\n')
    # Replay the regression suite against these extracted, actually shipped files.
    installed=REPORT/'installed'; installed.mkdir(parents=True,exist_ok=True)
    for name,value in dict(replacements,**additions).items():
        path=installed/name; path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(value)
    proof=dict(version=VERSION,source_commit=os.environ.get('GITHUB_SHA'),baseline_sha256=BASE_SHA,
        sha256=sha(result),bytes=len(result),changed_payload_files=sorted(replacements),
        added_payload_files=[],unchanged_payload_files_verified=len(preserved),
        unchanged_control_files_verified=len(preserved_controls),
        all_other_payload_bytes_preserved=True,physical_receiver_tested=False)
    (REPORT/'ipk-verification.json').write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps(proof),flush=True)


if __name__=='__main__':main()

