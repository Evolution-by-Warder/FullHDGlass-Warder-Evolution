"""Install all 224 independent Warder Radio country bouquets (offline, SHA-pinned).

Each country is a separate Enigma2 radio bouquet in bouquets.radio. Never edit,
replace or delete another bouquet or the existing single-country fallback.
Run only in the off-GUI worker after a validated external radio-world install.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

from . import warderRadioWorld as world
from . import warderRadioPackages as packages

OWNER='.warder-radio-bouquet-countries.json'
NAME=re.compile(r'^userbouquet\.warder-country-([A-Z]{2})\.radio$')
SHA=re.compile(r'^[0-9a-f]{64}$')
START=b'# WARDER COUNTRY BEGIN (managed v1)\n'
END=b'# WARDER COUNTRY END (managed v1)\n'
MAX_INDEX_BYTES=512*1024
MIN_FREE=24*1024*1024

def filename(code):
    if not isinstance(code,str) or not re.fullmatch(r'[A-Z]{2}',code):
        raise ValueError('Bad Warder Radio country')
    return 'userbouquet.warder-country-'+code+'.radio'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def block(codes):
    lines=[START]
    for code in sorted(codes):
        name=filename(code)
        lines.append(('#SERVICE 1:7:2:0:0:0:0:0:0:0:FROM BOUQUET "'+
                      name+'" ORDER BY bouquet\n').encode('ascii'))
    lines.append(END)
    return b''.join(lines)

def country_bouquet(raw,code,label):
    """Preserve every signed service identity and country row unchanged."""
    if not isinstance(raw,bytes) or not raw.startswith(b'#NAME ') or b'\x00' in raw:
        raise ValueError('Not a trusted radio bouquet')
    first,sep,body=raw.partition(b'\n')
    if not sep or len(body)<20:
        raise ValueError('Invalid radio country body')
    if (not isinstance(label,str) or not label or len(label)>180 or
        '\r' in label or '\n' in label):
        raise ValueError('Invalid country label')
    return ('#NAME Warder Radio - '+label+'\n').encode('utf-8')+body

def _read(owner_path):
    if owner_path.is_symlink():raise ValueError('Linked country ownership document')
    if not owner_path.exists():return None
    if not owner_path.is_file() or owner_path.stat().st_size>32768:
        raise ValueError('Unsafe country ownership document')
    try:doc=json.loads(owner_path.read_text(encoding='utf-8'))
    except (ValueError,OSError,UnicodeError):
        raise ValueError('Invalid country ownership document')
    if (not isinstance(doc,dict) or doc.get('owner')!='WarderCountryBouquets-v1'
        or not isinstance(doc.get('files'),dict)
        or not 1<=len(doc['files'])<=250 or
        any(not NAME.fullmatch(f) or not isinstance(h,str)
                or not SHA.fullmatch(h) for f,h in doc['files'].items())):
        raise ValueError('Untrusted country ownership')
    return doc

def _write(path,data):
    fd,temp=tempfile.mkstemp(prefix='.warder-country-stage-',dir=str(path.parent))
    try:
        with os.fdopen(fd,'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temp,0o644)
        os.replace(temp,str(path))
    finally:
        if os.path.exists(temp):os.unlink(temp)

def publish(paths_root,enigma_directory,require_external=True,min_free=MIN_FREE):
    """Publish 224 radio bouquet files and one managed index block atomically.

    Idempotent; refuses modified/unowned files, unknown index modifications,
    internal-flash fallback, missing world and unsupported incomplete snapshots.
    Existing personal bouquets retain byte content and relative order.
    """
    root=Path(paths_root)
    etc=Path(enigma_directory)
    if (not world._safe_directory(root) or
        (require_external and root.stat().st_dev == Path('/').stat().st_dev) or
        etc.is_symlink() or not etc.is_dir()):
        return {'changed':False,'skipped':'unsafe-storage'}
    folder=root/world.WORLD_NAME
    if not world._owner_ok(folder):
        return {'changed':False,'skipped':'missing-verified-world'}
    index=world._json_file(folder/'index.json',world.MAX_INDEX)
    countries=world._verify_index(index)
    if len(countries)!=224 or index.get('station_count')!=48219:
        return {'changed':False,'skipped':'incomplete-country-world'}
    names={filename(code):code for code in countries}
    owner_path=etc/OWNER
    old=_read(owner_path)
    current_files=old['files'] if old is not None else {}
    if old is not None and set(current_files)!=set(names):
        return {'changed':False,'skipped':'different-owned-country-list'}
    index_path=etc/'bouquets.radio'
    if (index_path.is_symlink() or
        (index_path.exists() and (not index_path.is_file()
         or index_path.stat().st_size>MAX_INDEX_BYTES))):
        return {'changed':False,'skipped':'unsafe-radio-index'}
    original=index_path.read_bytes() if index_path.exists() else b'#NAME Bouquets (Radio)\n'
    if b'\x00' in original:
        return {'changed':False,'skipped':'binary-radio-index'}
    existing=(START in original or END in original)
    if existing and (original.count(START)!=1 or original.count(END)!=1
                     or original.index(START)>original.index(END)):
        return {'changed':False,'skipped':'modified-managed-block'}
    if existing and not old:
        return {'changed':False,'skipped':'unowned-managed-index'}
    if not existing and old and any(not (etc/name).is_file() or
           digest((etc/name).read_bytes()) != hash for name,hash in current_files.items()):
        return {'changed':False,'skipped':'missing-managed-index'}
    # A completed but unindexed interrupted stage can be safely finished
    # only when every ownership-recorded country file remains byte-identical.
    if existing and original.split(START,1)[1].split(END,1)[0] != block(countries).split(START,1)[1].split(END,1)[0]:
        return {'changed':False,'skipped':'modified-managed-index'}
    # Reject unexpected same bouquet names appearing outside our block.
    external=original
    if existing:
        left,tail=original.split(START,1)
        _,right=tail.split(END,1)
        external=left+right
    if any(name.encode('ascii') in external for name in names):
        return {'changed':False,'skipped':'country-name-conflicts'}
    proposed={}
    count=0
    for code,metadata in sorted(countries.items()):
        raw,payload,manifest=packages.verified_country(folder,code)
        if len(raw)!=manifest['files']['bouquets/'+code+'.radio']['bytes']:
            raise ValueError('Invalid signed country bouquet size')
        cooked=country_bouquet(raw,code,metadata['name'])
        proposed[filename(code)]=cooked
        count+=manifest['stations']
    if count!=48219:
        raise ValueError('Station refs missing')
    for name,data in proposed.items():
        target=etc/name
        if target.is_symlink() or (target.exists() and not target.is_file()):
            return {'changed':False,'skipped':'unsafe-country-path'}
        if target.exists() and (name not in current_files or
                                digest(target.read_bytes())!=current_files[name]):
            return {'changed':False,'skipped':'user-modified-country-bouquet'}
    if etc.stat().st_dev == Path('/').stat().st_dev:
        available=os.statvfs(str(etc))
        free=available.f_bavail*available.f_frsize
        required=sum(len(data) for name,data in proposed.items() if not (etc/name).exists())
        if free < max(min_free,required+8*1024*1024):
            return {'changed':False,'skipped':'flash-space-guard',
                    'required_bytes':required,'free_bytes':free}
    new_index=(external if external.endswith(b'\n') else external+b'\n')+block(countries)
    hashes={name:digest(data) for name,data in proposed.items()}
    if (old and hashes==old['files'] and existing and
        original==new_index and all((etc/n).is_file() for n in names)):
        return {'changed':False,'skipped':'already-current','countries':224,
                'stations':48219}
    changed=0
    # Write files before referring to them; existing source data are immutable.
    for name,data in proposed.items():
        target=etc/name
        if not target.exists() or target.read_bytes()!=data:
            _write(target,data)
            changed+=1
    # Record ownership before the root index becomes visible; preserves recovery.
    owner={'schema':1,'owner':'WarderCountryBouquets-v1',
           'world_sha256':world._json_file(folder/world.OWNER,world.MAX_OWNER)['archive_sha256'],
           'files':hashes,'countries':224,'station_count':48219}
    _write(owner_path,(json.dumps(owner,sort_keys=True,ensure_ascii=False)+'\n').encode())
    _write(index_path,new_index)
    return {'changed':True,'countries':224,'stations':48219,
            'files_written':changed,'indexed_countries':224}

def selected_from_native_path(path):
    if not isinstance(path,str) or len(path)>1024:return None
    match=re.search(r'FROM BOUQUET "(userbouquet\.warder-country-([A-Z]{2})\.radio)"',path)
    return match.group(2) if match and match.group(1)==filename(match.group(2)) else None

def selected_country(directory):
    info=Path(directory)/'.warder-radio-selected-country.json'
    if not info.is_file() or info.is_symlink():return None
    try:
        if info.stat().st_size>512:return None
        doc=json.loads(info.read_text(encoding='utf-8'))
        owner=_read(Path(directory)/OWNER)
        code=doc.get('country')
        if owner is None or filename(code) not in owner['files']:return None
        return code
    except (OSError,ValueError,TypeError,AttributeError):
        return None

def remember_selection(directory,code):
    folder=Path(directory)
    owner=_read(folder/OWNER)
    if owner is None or filename(code) not in owner['files']:
        return False
    old=selected_country(folder)
    if old==code:return False
    _write(folder/'.warder-radio-selected-country.json',
           (json.dumps({'country':code,'schema':1})+'\n').encode())
    return True
