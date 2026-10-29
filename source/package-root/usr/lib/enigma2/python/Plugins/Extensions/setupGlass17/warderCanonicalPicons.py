"""One verified complete archive per style, using original picon directories."""
import os
import shutil
import tempfile


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


def install(screen,row,variant,get_assets,translate):
    kind={'aux-prov':'provider','aux-sat':'satellite'}.get(row)
    root={'provider':'piconProv','satellite':'piconSat'}.get(kind)
    if not root or variant not in ('transparent','black','white'):raise ValueError('Invalid auxiliary selection')
    error,assets=get_assets()
    if error:raise ValueError(error)
    suffix={'transparent':'220','black':'b','white':'w'}[variant]
    asset=dict(assets.get(root+'-'+suffix,{}))
    expected='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/'+('providers' if kind=='provider' else 'satellites')+'/'+variant+'/'+root+'.zip'
    if asset.get('delivery')!='canonical-220x132-v1' or asset.get('resolution')!=[220,132] or asset.get('root')!=root or asset.get('filename')!=root+'.zip' or asset.get('url')!=expected or asset.get('publication_source_id')!='fullhd-production' or not 0<int(asset.get('png_count',0))<10000:raise ValueError('Canonical picon catalogue unavailable or invalid')
    destination=screen._warderAuxiliaryDestination(root)
    archive=None;stage=None;previous=screen.zzz
    try:
        fd,archive=tempfile.mkstemp(prefix='warder-picons-',suffix='.zip',dir='/tmp');os.close(fd)
        screen._warderFetchAuxiliaryArchive(asset,archive)
        stage=tempfile.mkdtemp(prefix='warder-picons-',dir='/tmp');screen._safeExtractZip(archive,stage)
        screen.zzz=stage+os.sep
        updated,total=screen.cprmFiles(root)
        if updated!=asset['png_count'] or total!=asset['png_count']:raise OSError('Canonical picon installation incomplete')
        remove_verified_duplicates(screen,os.path.dirname(destination),root)
        return translate('SUCCESSFUL')+': '+translate('Provider logos' if kind=='provider' else 'Satellite logos')+' — %d/%d (220×132)'%(updated,total)
    finally:
        screen.zzz=previous
        if archive:
            try:os.unlink(archive)
            except OSError:pass
        if stage:
            # The whole directory belongs to this one operation, including
            # nested archive entries left behind by an interrupted extraction.
            shutil.rmtree(stage,ignore_errors=True)
