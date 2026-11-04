#!/usr/bin/env python3
"""Verify activated public URLs against the already SHA256-verified Git blobs."""
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
import hashlib,json,os,subprocess,time,urllib.request

ROOT=Path(__file__).resolve().parents[1]
REPO='Evolution-by-Warder/FullHDGlass-Warder-Evolution'
PREFIX='assets/warder/downloads/picons/channels/'
RAW='https://raw.githubusercontent.com/'+REPO+'/main/'+PREFIX
REPORT=ROOT/'reports/unchanged622-publication-20261104.json'

def request(url,method='GET'):
    headers={'User-Agent':'Warder-picon-production-integrity/20261104'}
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=headers,method=method),timeout=90) as response:
                return response.status,dict(response.headers),response.read() if method!='HEAD' else b''
        except Exception:
            if attempt==2:raise
            time.sleep(1+attempt)

def tree(ref):
    raw=subprocess.check_output(['git','ls-tree','-rz',ref,'--',PREFIX],cwd=ROOT)
    result={}
    for item in raw.split(b'\0'):
        if not item:continue
        metadata,path=item.split(b'\t',1)
        mode,kind,digest=metadata.decode().split()
        if kind=='blob':result[path.decode()]={'sha':digest}
    return result


def verify():
    report=json.loads(REPORT.read_text())
    proof=report['public_verification']
    assert proof['all_sizes_and_sha256_match'] and proof['manifest_matches']
    assert proof['verified_parts']==len(report['new_parts'])
    assert proof['ref']==os.environ['VERIFIED_PARTS_REF']
    subprocess.run(['git','fetch','--no-tags','--depth=1','--filter=blob:none','origin',os.environ['VERIFIED_PARTS_REF']],cwd=ROOT,check=True)
    source=tree(os.environ['VERIFIED_PARTS_REF']);production=tree(os.environ['GITHUB_SHA'])
    for part in report['new_parts']:
        before=source[PREFIX+part['filename']];after=production[PREFIX+part['filename']]
        assert before['sha']==after['sha']
    # The full public bytes were SHA256-checked before activation. Matching Git
    # blob IDs prove that the activated commit contains those exact same bytes.
    # Check all actual main URLs as well, without downloading 2.6 GB a second time.
    def public_head(part):
        status,headers,_=request(RAW+part['filename'],method='HEAD')
        assert status==200
        length=next(value for key,value in headers.items() if key.lower()=='content-length')
        assert int(length)==part['bytes'],part['filename']
        return part['filename']
    verified=[]
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures=[pool.submit(public_head,p) for p in report['new_parts']]
        for future in as_completed(futures):
            verified.append(future.result())
            if len(verified)%40==0:print('PUBLIC MAIN URLS VERIFIED',len(verified),'/',len(futures),flush=True)
    status,_,raw=request(RAW+'manifest.json')
    assert status==200 and hashlib.sha256(raw).hexdigest()==report['manifest_sha256']
    report['production_main_verification']={'status':'PRODUCTION_MAIN_VERIFIED','main_commit':os.environ['GITHUB_SHA'],'verified_parts_ref':os.environ['VERIFIED_PARTS_REF'],'matching_verified_git_blobs':len(verified),'public_main_headers_verified':len(verified),'part_sizes_match':True,'live_manifest_sha256_matches':True,'full_part_sha256_proof':proof}
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PRODUCTION VERIFIED:',len(verified),'matching SHA256-verified Git blobs, public main URLs, sizes and live catalogue',flush=True)

if __name__=='__main__':verify()
