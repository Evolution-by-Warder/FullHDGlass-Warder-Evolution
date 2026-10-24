"""Small, prepared type previews; no full screenshot decoding in the list."""
import hashlib
import os
import tempfile
import zipfile
from functools import lru_cache

_BUNDLE=os.path.join(os.path.dirname(__file__), 'warder-infobar-types.zip')


@lru_cache(maxsize=1)
def _cache_dir():
    with open(_BUNDLE,'rb') as stream:
        revision=hashlib.sha256(stream.read()).hexdigest()[:16]
    folder=os.path.join(tempfile.gettempdir(),'warder-infobar-types-'+revision)
    os.makedirs(folder,mode=0o700,exist_ok=True)
    return folder


@lru_cache(maxsize=128)
def thumbnail_path(type_id):
    try:
        name='type-%d.png'%int(type_id)
        target=os.path.join(_cache_dir(),name)
        if os.path.isfile(target):return target
        with zipfile.ZipFile(_BUNDLE) as source:
            raw=source.read(name)
        handle,temp_path=tempfile.mkstemp(prefix='.type-',dir=_cache_dir())
        try:
            with os.fdopen(handle,'wb') as stream:stream.write(raw)
            os.replace(temp_path,target)
        finally:
            if os.path.exists(temp_path):os.unlink(temp_path)
        return target
    except (OSError,ValueError,KeyError,zipfile.BadZipFile):
        return ''
