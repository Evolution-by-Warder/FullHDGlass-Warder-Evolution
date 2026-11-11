"""Channel-list-only picons, with a per-service fallback to the shared set."""
from functools import wraps
from os.path import isdir, isfile, join
from re import sub


def reference_names(reference, alternative):
    resolved = alternative(reference)
    if not isinstance(resolved, str):
        return ()
    fields = resolved.split(':', 10)[:10]
    if len(fields) != 10 or any('/' in field or '\\' in field for field in fields):
        return ()
    # Canonical PNG files use uppercase hex reference components.
    fields = [field.upper() for field in fields]
    names = ['_'.join(fields)]
    # Match the image/legacy skin aliases without changing native search paths.
    for reftype in dict.fromkeys((fields[0], '1')):
        for service_type in dict.fromkeys((fields[2], '1', '19', '16')):
            for namespace in dict.fromkeys((fields[6], fields[6][:-4] + '0000')):
                variant = list(fields)
                variant[0], variant[2], variant[6] = reftype, service_type, namespace
                names.append('_'.join(variant))
    return tuple(dict.fromkeys(names))


def name_aliases(reference, get_name, sanitize):
    name = (get_name(reference) or '').replace('\x80', '').replace('\x86', '').replace('\x87', '')
    if not name or 'SID 0x' in name:
        return ()
    name = sanitize(name).lower()
    if not name or name == '__' or name in ('.', '..') or '/' in name or '\\' in name:
        return ()
    legacy = sub('[^a-z0-9]', '', name.replace('&', 'and').replace('+', 'plus').replace('*', 'star'))
    return tuple(dict.fromkeys(n for n in (name, legacy,
        sub(r'(fhd|uhd|hd|sd|4k)$', '', name).strip(),
        sub(r'(fhd|uhd|hd|sd|4k)$', '', legacy).strip()) if n))


def find_picon(reference, base, alternative, get_name, sanitize, prefer_mini=False, custom_folder=None):
    if not base:
        return ''
    references = reference_names(reference, alternative)
    if not references:
        return ''
    aliases = None
    folders = ('picon_50x30', 'picon') if prefer_mini else ('picon', 'picon_50x30')
    # Expert choice is authoritative: never silently mix two picon collections.
    directories = [custom_folder] if custom_folder is not None else [join(base, folder) for folder in folders]
    for directory in directories:
        if not isdir(directory):
            continue
        for name in references:
            path = join(directory, name + '.png')
            if isfile(path):
                return path
        if aliases is None:
            aliases = name_aliases(reference, get_name, sanitize)
        for name in aliases:
            path = join(directory, name + '.png')
            if isfile(path):
                return path
    return ''


def install(service_list, is_active, get_base, alternative, get_name, sanitize, prefer_mini=None, get_custom=None):
    """Wrap only ServiceList's imported lookup; keep the image renderer intact."""
    def wrap(original):
        @wraps(original)
        def lookup(reference, *args, **kwargs):
            if is_active():
                try:
                    return find_picon(
                        reference, get_base(), alternative, get_name, sanitize,
                        prefer_mini=bool(prefer_mini is not None and prefer_mini()),
                        custom_folder=get_custom() if get_custom is not None else None)
                except (AttributeError, OSError, TypeError, ValueError):
                    return ''
            return original(reference, *args, **kwargs)
        lookup._warder_channel_picons = True
        return lookup

    changed = False
    for name in ('getChannelSelectionPiconName', 'getPiconName'):
        original = getattr(service_list, name, None)
        if callable(original) and getattr(original, '_warder_channel_picons', False) is not True:
            setattr(service_list, name, wrap(original))
            changed = True
    return changed

