"""Original online broadcaster images for an independently selected Radio Browser country.

This is a TEST-only source fallback while reviewed immutable 224-country logo
release is unpublished. It does NOT claim that each image is one of the 40,837
independently reviewed PNGs. No GUI-thread HTTP, no satellite/TV picons, and
all download work is bounded to the active country and external PATHS device.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from concurrent.futures import ThreadPoolExecutor,as_completed
from contextlib import nullcontext

from . import warderRadioLive as live
from . import warderRadioCountryBouquets as books
from . import warderRadioWorld as world
from . import warderRadioPackages as country_package

OWNER='.warder-radio-online-source.json'
PNG=re.compile(r'^4097_0_2_(?:[0-9A-F]{1,8}_){6}[0-9A-F]{1,8}\.png$')
SHA=re.compile(r'^[0-9a-f]{64}$')
BATCH=48
WORKERS=6

def _read(path,maxsize):
    if path.is_symlink() or not path.is_file() or path.stat().st_size>maxsize:
        return None
    try:
        obj=json.loads(path.read_text(encoding='utf-8'))
        return obj if isinstance(obj,dict) else None
    except (OSError,ValueError,UnicodeError):
        return None

def _write(path,body):
    fd,tmp=tempfile.mkstemp(prefix='.warder-online-stage-',dir=str(path.parent))
    try:
        with os.fdopen(fd,'wb') as f:
            f.write(body)
            f.flush();os.fsync(f.fileno())
        os.replace(tmp,str(path))
    finally:
        if os.path.exists(tmp):os.unlink(tmp)

def selected(code, directory):
    """Use active receiver radio country, retained across GUI reboot."""
    from . import warderRadioCountry as country
    return country.active_country(directory) == code


def _verified_rows(root,directory,code):
    cached=world.cached_country(root,code)
    if cached:
        src=root/world.WORLD_NAME
        _,raw,manifest=country_package.verified_country(src,code)
        doc=json.loads(raw)
        return doc['stations'],hashlib.sha256(raw).hexdigest()
    from . import warderRadioCountry as country
    if country.active_country(directory)!=code:
        return None,None
    file=Path(directory)/live.DATA_FILE
    doc=_read(file,24*1024*1024)
    rows=doc.get('stations') if isinstance(doc,dict) else None
    if not isinstance(rows,list) or not rows:return None,None
    if any(not isinstance(r,dict) or r.get('countrycode')!=code
           or not PNG.fullmatch(str(r.get('stem',''))+'.png') for r in rows):
        return None,None
    try:
        proof=json.dumps(rows,ensure_ascii=False,sort_keys=True).encode()
    except (TypeError,ValueError):
        return None,None
    return rows,hashlib.sha256(proof).hexdigest()

def sync_online_country(root,directory,code,logos=None,max_batch=BATCH,
                        require_external=True):
    """Bounded one-batch source refresh; subsequent ticks resume exact cursor."""
    root=Path(root);directory=Path(directory)
    if (not isinstance(code,str) or not re.fullmatch(r'[A-Z]{2}',code)
        or not world._safe_directory(root) or
        (require_external and root.stat().st_dev==Path('/').stat().st_dev)):
        return {'changed':False,'skipped':'unsafe-storage'}
    if not selected(code,directory):
        return {'changed':False,'skipped':'country-not-selected'}
    if not isinstance(max_batch,int) or not 1<=max_batch<=BATCH:
        raise ValueError('Bad online fallback batch size')
    rows,source_sha=_verified_rows(root,directory,code)
    if rows is None:
        return {'changed':False,'skipped':'country-catalogue-not-ready'}
    path=root/'picon'
    if path.is_symlink() or (path.exists() and not path.is_dir()):
        return {'changed':False,'skipped':'unsafe-picons'}
    if not path.exists():path.mkdir(mode=0o755)
    folder=path/'radio'
    if folder.is_symlink() or (folder.exists() and not folder.is_dir()):
        return {'changed':False,'skipped':'unsafe-online-picons'}
    if not folder.exists():folder.mkdir(mode=0o755)
    target=folder/code
    if target.is_symlink() or (target.exists() and not target.is_dir()):
        return {'changed':False,'skipped':'unsafe-country-picons'}
    if not target.exists():target.mkdir(mode=0o755)
    owner=target/OWNER
    state=_read(owner,4*1024*1024) if owner.exists() else None
    if owner.exists() and (not isinstance(state,dict) or
        state.get('owner')!='WarderRadioOnline' or state.get('country')!=code):
        return {'changed':False,'skipped':'user-owned-online-logos'}
    known=dict(state.get('files',{})) if state else {}
    if any(not isinstance(n,str) or not PNG.fullmatch(n)
           or not isinstance(h,str) or not SHA.fullmatch(h)
           or not (target/n).is_file() or (target/n).is_symlink()
           or hashlib.sha256((target/n).read_bytes()).hexdigest()!=h
           for n,h in known.items()):
        return {'changed':False,'skipped':'modified-online-logo'}
    unexpected=set(p.name for p in target.iterdir())-set(known)-{OWNER}
    if unexpected:
        return {'changed':False,'skipped':'foreign-online-files'}
    if state and state.get('source_sha256')==source_sha:
        start=state.get('cursor',0)
        if type(start) is not int or not 0<=start<=len(rows):
            return {'changed':False,'skipped':'unsafe-online-cursor'}
    else:start=0
    if start>=len(rows):
        return {'changed':False,'skipped':'already-scanned','country':code,
                'logos':len(known)}
    block=rows[start:start+max_batch]
    # Source PNG cache is temporary on external PATHS, not an extra growing
    # radio/station-logo-cache directory retained after switching countries.
    scratch=tempfile.TemporaryDirectory(
        prefix='.warder-radio-logo-source-',dir=str(root)) if logos is None else nullcontext()
    with scratch as temporary:
        if logos is None:
            _,logo_type=live._plugin()
            logos=logo_type(temporary)
        candidates={}
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            jobs={pool.submit(logos.get,row):row for row in block
                  if row.get('favicon') and PNG.fullmatch(row.get('stem','')+'.png')
                  and row.get('countrycode')==code}
            for task in as_completed(jobs):
                row=jobs[task]
                try:
                    loc=task.result()
                    if not loc:continue
                    src=Path(loc)
                    if src.is_symlink() or not src.is_file() or src.stat().st_size>512*1024:
                        continue
                    raw=src.read_bytes()
                    if not raw.startswith(b'\x89PNG\r\n\x1a\n'):continue
                    rendered=live._picon_png(raw,224,224)
                    if not 512<len(rendered)<512*1024:continue
                    candidates[row['stem']+'.png']=rendered
                except (ValueError,KeyError,OSError,TypeError,ImportError):
                    continue
    # Only exact SHA-verified station names, and never overwrite a personal PNG.
    count=0
    for name,data in candidates.items():
        file=target/name
        if file.is_symlink():continue
        if file.exists():
            if name not in known:continue
            if hashlib.sha256(file.read_bytes()).hexdigest()!=known[name]:
                continue
        else:
            try:
                with os.fdopen(os.open(str(file),os.O_CREAT|os.O_EXCL|os.O_WRONLY|
                                      getattr(os,'O_NOFOLLOW',0),0o644),'wb') as f:
                    f.write(data);f.flush();os.fsync(f.fileno())
            except (OSError,FileExistsError):
                continue
        known[name]=hashlib.sha256(data).hexdigest()
        count+=1
    next_cursor=start+len(block)
    # Persist progress after every bounded batch; no repeated image downloads.
    _write(owner,(json.dumps({'schema':1,'owner':'WarderRadioOnline',
        'country':code,'source_sha256':source_sha,'files':known,
        'cursor':next_cursor,'total_stations':len(rows)},
        sort_keys=True)+'\n').encode())
    return {'changed':count>0,'country':code,'new_online_logos':count,
        'logos':len(known),'scanned':next_cursor,'total':len(rows),
        'incomplete':next_cursor<len(rows),'source':'verified-online-radio-browser'}
