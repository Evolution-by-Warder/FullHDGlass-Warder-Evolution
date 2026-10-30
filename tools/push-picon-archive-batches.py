#!/usr/bin/env python3
"""Push large picon publications in bounded packs; commit the catalogue last."""
from pathlib import Path
import argparse,json,re,subprocess,time

ROOT=Path(__file__).resolve().parents[1]
DIRECTORY='assets/warder/downloads/picons/channels/'
DEFAULT_LIMIT=512*1024*1024

def batches(parts,limit=DEFAULT_LIMIT):
    seen=set();result=[];group=[];size=0
    for part in sorted(parts,key=lambda p:p['filename']):
        name=part['filename'];length=part['bytes']
        assert re.fullmatch(r'warder-[a-z0-9]+-\d+x\d+-(black|white|transparent)-[0-9a-f]{16}\.zip\.part\d{2}',name),name
        assert name not in seen and 0<length<=limit
        seen.add(name)
        if group and size+length>limit:
            result.append(group);group=[];size=0
        group.append(part);size+=length
    if group:result.append(group)
    assert sum(len(g) for g in result)==len(parts)
    return result

def git(*args,capture=False):
    return subprocess.run(['git',*args],cwd=ROOT,check=True,text=True,stdout=subprocess.PIPE if capture else None).stdout

def push(branch):
    head=git('rev-parse','HEAD',capture=True).strip()
    for attempt in range(3):
        completed=subprocess.run(['git','push','origin',f'HEAD:{branch}'],cwd=ROOT)
        if completed.returncode==0:return
        remote=git('ls-remote','origin',f'refs/heads/{branch}',capture=True).strip().split()
        # A transport disconnect can lose the successful server response.
        if remote and remote[0]==head:return
        if attempt<2:time.sleep(2)
    raise RuntimeError('Bounded publication push failed; keep the last complete catalogue active')

def commit_files(paths,message,branch):
    git('add','--sparse','--',*paths)
    staged=git('diff','--cached','--name-only',capture=True).splitlines()
    assert set(staged)<=set(paths),staged
    if not staged:return
    git('diff','--cached','--check')
    git('commit','-m',message)
    push(branch)

def publish(report_path,branch):
    assert branch=='release/picons-assimilated-20261030'
    report=json.loads((ROOT/report_path).read_text())
    assert report['status']=='VERIFIED_PUBLICATION_CANDIDATE'
    assert report['receiver_selective_installer_checks']==report['receiver_planner_checks']==report['piconhub_planner_checks']==report['changed_packages']
    groups=batches(report['new_parts'])
    for i,group in enumerate(groups,1):
        names=[]
        for part in group:
            name=DIRECTORY+part['filename']
            if (ROOT/name).exists():
                assert (ROOT/name).stat().st_size==part['bytes']
                names.append(name)
            else:
                # A complete candidate reused after a transport interruption
                # keeps its archive blobs outside the sparse working tree.
                assert git('ls-files','--error-unmatch','--',name,capture=True).strip()==name
        if names:
            commit_files(names,f'Stage verified picon archive parts {i}/{len(groups)}',branch)
        print('PUSHED',i,'of',len(groups),'bounded archive batches',flush=True)
    # Readers see a catalogue only after every referenced new part exists.
    commit_files([DIRECTORY+'manifest.json',DIRECTORY+'SHA256SUMS',report_path],
                 'Publish complete verified picon catalogue after all archive parts',branch)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--report',required=True);parser.add_argument('--branch',required=True)
    args=parser.parse_args();publish(args.report,args.branch)
