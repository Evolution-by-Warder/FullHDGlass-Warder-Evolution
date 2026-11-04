#!/usr/bin/env python3
"""Read back every immutable uploaded part, with bounded retries and progress."""
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
import argparse,hashlib,json,subprocess,time,urllib.request

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'reports/unchanged622-publication-20261104.json'

def fetch(url):
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Warder-production-verification/20261104'}),timeout=30) as response:
                assert response.status==200
                return response.read()
        except Exception:
            if attempt==4:raise
            time.sleep(1+attempt)

def git_tree(ref):
    raw=subprocess.check_output(['git','ls-tree','-rz',ref,'--','assets/warder/downloads/picons/channels/'],cwd=ROOT)
    return {item.split(b'\t',1)[1].decode():item.split(b'\t',1)[0].decode().split()[2] for item in raw.split(b'\0') if item}

def main(ref,reuse=None):
    assert len(ref)==40 and all(c in '0123456789abcdef' for c in ref)
    report=json.loads(REPORT.read_text())
    root='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/'+ref+'/assets/warder/downloads/picons/channels/'
    def verify(part):
        raw=fetch(root+part['filename'])
        assert len(raw)==part['bytes'] and hashlib.sha256(raw).hexdigest()==part['sha256'],part['filename']
        return part['filename']
    completed=[];pending=list(report['new_parts']);reused=[];old_ref=None
    if reuse:
        old=json.loads(reuse.read_text());proof=old['public_verification'];old_ref=proof['ref']
        assert proof['all_sizes_and_sha256_match'] and proof['manifest_matches'] and proof['verified_parts']==len(old['new_parts'])
        subprocess.run(['git','fetch','--no-tags','--depth=1','--filter=blob:none','origin',ref,old_ref],cwd=ROOT,check=True)
        old_tree=git_tree(old_ref);new_tree=git_tree(ref)
        old_parts={p['filename']:p for p in old['new_parts']}
        pending=[]
        for part in report['new_parts']:
            name=part['filename'];path='assets/warder/downloads/picons/channels/'+name
            previous=old_parts.get(name)
            if previous==part and old_tree[path]==new_tree[path]:reused.append(name)
            else:pending.append(part)
        completed.extend(reused)
        print('REUSED FULLY SHA256-VERIFIED IDENTICAL GIT BLOBS:',len(reused),'new readbacks:',len(pending),flush=True)
    progress=ROOT/'reports'/('unchanged622-readback-progress-'+ref[:12]+'.json')
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures=[pool.submit(verify,item) for item in pending]
        for future in as_completed(futures):
            completed.append(future.result())
            progress.write_text(json.dumps({'ref':ref,'completed':completed,'reused_source_ref':old_ref},indent=2)+'\n')
            if (len(completed)-len(reused))%5==0:print('SHA256 VERIFIED',len(completed),'/',len(report['new_parts']),'including',len(reused),'identical verified blobs',flush=True)
    raw=fetch(root+'manifest.json')
    assert hashlib.sha256(raw).hexdigest()==report['manifest_sha256']
    report['public_verification']={'ref':ref,'mode':'RAW_IMMUTABLE_COMMIT_FULL_BYTES_WITH_IDENTICAL_BLOB_REUSE' if reused else 'RAW_IMMUTABLE_COMMIT_FULL_BYTES','verified_parts':len(completed),'all_sizes_and_sha256_match':True,'manifest_matches':True,'newly_downloaded_parts':len(pending),'reused_sha256_verified_git_blobs':len(reused),'reuse_source_ref':old_ref}
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PUBLIC SHA256 VERIFIED:',len(completed),'complete parts and catalogue',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--ref',required=True);parser.add_argument('--reuse',type=Path)
    args=parser.parse_args();main(args.ref,args.reuse)
