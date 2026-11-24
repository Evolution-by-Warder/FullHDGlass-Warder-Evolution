"""One verified complete archive per style, using original picon directories."""
import os
import shutil
import tempfile
import re
import struct
import zipfile


def remove_verified_duplicates(screen,base,root):
    """Delete equal copies only; preserve unmatched user files and symlinks."""
    legacy=os.path.join(base,root+'_220x132');canonical=os.path.join(base,root)
    if not os.path.isdir(legacy) or os.path.islink(legacy):return
    for name in os.listdir(legacy):
        source=os.path.join(legacy,name);target=os.path.join(canonical,name)
        if not name.lower().endswith('.png') or os.path.islink(source) or not os.path.isfile(source):continue
        if os.path.isfile(target) and not os.path.islink(target) and screen._warderFilesMatch(source,target):os.unlink(source)
    try:os.rmdir(legacy)
    except OSError:pass


# V2 is additive: old clients still receive the exact original v1 archive.
# Each extension is a separate complete ZIP, never a byte fragment.
_MAX_ARCHIVE = 32 * 1024 * 1024
_MAX_EXPANDED = 128 * 1024 * 1024
_RESERVE = 64 * 1024 * 1024
_PROVIDER_ROOT = 'https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/providers/'


def _positive_int(value, limit):
    if type(value) is not int or not 0 < value <= limit:
        raise ValueError('Invalid provider v2 size or count')
    return value


def _v2_plan(assets, suffix, variant):
    key = 'piconProv-' + suffix
    base = assets.get(key)
    spec = assets.get(key + '-v2')
    if not isinstance(base, dict) or not isinstance(spec, dict):
        raise ValueError('Invalid provider v2 catalogue')
    if spec.get('delivery') != 'canonical-220x132-v2' or spec.get('resolution') != [220,132] or spec.get('root') != 'piconProv':
        raise ValueError('Invalid provider v2 identity')
    if spec.get('base_asset_id') != key or spec.get('base_sha256') != base.get('sha256'):
        raise ValueError('Provider v2 base mismatch')
    extensions = spec.get('extensions')
    if not isinstance(extensions, list) or not 1 <= len(extensions) <= 4:
        raise ValueError('Invalid provider extension count')
    jobs = [dict(base)]
    for i, entry in enumerate(extensions, 1):
        if not isinstance(entry, dict):
            raise ValueError('Invalid provider extension')
        jobs.append(dict(entry))
    for i, job in enumerate(jobs):
        url = _PROVIDER_ROOT + variant + '/' + ('extension-%02d/' % i if i else '') + 'piconProv.zip'
        if (job.get('url') != url or job.get('publication_source_id') != 'fullhd-production'
                or job.get('root') != 'piconProv' or job.get('filename') != 'piconProv.zip'
                or job.get('parts') not in (None, []) or job.get('resolution') != [220,132]
                or not isinstance(job.get('sha256'), str) or not re.fullmatch(r'[0-9a-f]{64}', job['sha256'])):
            raise ValueError('Invalid provider archive identity')
        if i == 0 and job.get('delivery') != 'canonical-220x132-v1':
            raise ValueError('Invalid provider base archive')
        _positive_int(job.get('size'), _MAX_ARCHIVE)
        _positive_int(job.get('png_count'), 9999)
    count = _positive_int(spec.get('png_count'), 9999)
    expanded = _positive_int(spec.get('unpacked_size'), _MAX_EXPANDED)
    if count != sum(j['png_count'] for j in jobs):
        raise ValueError('Provider v2 count mismatch')
    return jobs, count, expanded


def _install_v2(screen, assets, suffix, variant, translate, progress, stage):
    jobs, expected_count, expanded = _v2_plan(assets, suffix, variant)
    destination = screen._warderAuxiliaryDestination('piconProv')
    # Staging is on the configured target, not RAM-backed /tmp or flash.
    base = os.path.dirname(destination)
    needed = 2 * expanded + max(j['size'] for j in jobs) + _RESERVE
    st = os.statvfs(base)
    if st.f_bavail * st.f_frsize < needed:
        raise OSError('Insufficient free space for provider archives')
    previous = screen.zzz
    work = tempfile.mkdtemp(prefix='.warder-provider-', dir=base)
    try:
        merged = os.path.join(work, 'merged')
        os.mkdir(merged)
        folder = os.path.join(merged, 'piconProv')
        os.mkdir(folder)
        seen = set()
        unpacked = 0
        done = 0
        total_bytes = sum(j['size'] for j in jobs)
        for i, job in enumerate(jobs):
            archive = os.path.join(work, 'part-%02d.zip' % i)
            if stage: stage('download')
            callback = (lambda current, total, offset=done: progress(offset + current, total_bytes)) if progress else None
            screen._warderFetchAuxiliaryArchive(job, archive, callback)
            done += job['size']
            if stage: stage('extract')
            # Existing fetch verifies SHA/CRC/root/member type. Enforce bounds
            # and disjoint names across all archives before installing anything.
            with zipfile.ZipFile(archive) as z:
                members = [entry for entry in z.infolist() if not entry.is_dir()]
                if len(members) != job['png_count']:
                    raise ValueError('Provider archive count mismatch')
                for entry in members:
                    name = entry.filename
                    parts = name.split('/')
                    if len(parts) != 2 or parts[0] != 'piconProv' or not parts[1].lower().endswith('.png') or '\\' in name or parts[1] in ('','.','..'):
                        raise ValueError('Unsafe provider archive member')
                    leaf = parts[1]
                    key = leaf.casefold()
                    if key in seen or not 0 < entry.file_size <= 1024 * 1024:
                        raise ValueError('Duplicate or oversized provider PNG')
                    unpacked += entry.file_size
                    if unpacked > expanded:
                        raise ValueError('Provider archive expansion exceeds declared size')
                    with z.open(entry) as inp:
                        header = inp.read(24)
                        if len(header) != 24 or header[:8] != b'\\x89PNG\\r\\n\\x1a\\n' or struct.unpack('>II',header[16:24]) != (220,132):
                            raise ValueError('Invalid provider PNG')
                        with open(os.path.join(folder, leaf), 'xb') as out:
                            out.write(header)
                            shutil.copyfileobj(inp, out, 128 * 1024)
                    seen.add(key)
            os.unlink(archive)
        if len(seen) != expected_count or unpacked != expanded:
            raise ValueError('Incomplete provider archive set')
        screen.zzz = merged + os.sep
        if stage: stage('copy')
        updated, total = screen.cprmFiles('piconProv')
        if updated != expected_count or total != expected_count:
            raise OSError('Canonical picon installation incomplete')
        remove_verified_duplicates(screen, base, 'piconProv')
        return translate('SUCCESSFUL') + ': ' + translate('Provider logos') + ' — %d/%d (220×132)' % (updated,total)
    finally:
        screen.zzz = previous
        shutil.rmtree(work, ignore_errors=True)


def install(screen,row,variant,get_assets,translate,progress=None,stage=None):
    kind={'aux-prov':'provider','aux-sat':'satellite'}.get(row)
    root={'provider':'piconProv','satellite':'piconSat'}.get(kind)
    if not root or variant not in ('transparent','black','white'):raise ValueError('Invalid auxiliary selection')
    if stage:stage("catalog")
    error,assets=get_assets()
    if error:raise ValueError(error)
    suffix={'transparent':'220','black':'b','white':'w'}[variant]
    if kind == 'provider' and root+'-'+suffix+'-v2' in assets:
        return _install_v2(screen,assets,suffix,variant,translate,progress,stage)
    asset=dict(assets.get(root+'-'+suffix,{}))
    expected='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/'+('providers' if kind=='provider' else 'satellites')+'/'+variant+'/'+root+'.zip'
    if asset.get('delivery')!='canonical-220x132-v1' or asset.get('resolution')!=[220,132] or asset.get('root')!=root or asset.get('filename')!=root+'.zip' or asset.get('url')!=expected or asset.get('publication_source_id')!='fullhd-production' or not 0<int(asset.get('png_count',0))<10000:raise ValueError('Canonical picon catalogue unavailable or invalid')
    destination=screen._warderAuxiliaryDestination(root)
    archive=None;stage_dir=None;previous=screen.zzz
    try:
        fd,archive=tempfile.mkstemp(prefix='warder-picons-',suffix='.zip',dir='/tmp');os.close(fd)
        if stage:stage("download")
        screen._warderFetchAuxiliaryArchive(asset,archive,progress)
        if stage:stage("extract")
        stage_dir=tempfile.mkdtemp(prefix='warder-picons-',dir='/tmp');screen._safeExtractZip(archive,stage_dir)
        screen.zzz=stage_dir+os.sep
        if stage:stage("copy")
        updated,total=screen.cprmFiles(root)
        if updated!=asset['png_count'] or total!=asset['png_count']:raise OSError('Canonical picon installation incomplete')
        remove_verified_duplicates(screen,os.path.dirname(destination),root)
        return translate('SUCCESSFUL')+': '+translate('Provider logos' if kind=='provider' else 'Satellite logos')+' — %d/%d (220×132)'%(updated,total)
    finally:
        screen.zzz=previous
        if archive:
            try:os.unlink(archive)
            except OSError:pass
        if stage_dir:
            # The whole directory belongs to this one operation, including
            # nested archive entries left behind by an interrupted extraction.
            shutil.rmtree(stage_dir,ignore_errors=True)
