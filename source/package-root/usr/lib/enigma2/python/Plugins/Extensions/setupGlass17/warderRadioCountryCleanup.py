"""Delete ONLY verified Warder-owned logos of countries no longer selected.

The receiver keeps one active radio country. The online source or signed ZIP
for a different country must not accumulate on external PATHS. Cleanup runs
only in off-GUI workers, after an authoritative country selection, and never
deletes custom/edited/unknown PNGs, TV/SAT picons or other user directories.
"""
import json
import os
from pathlib import Path
import re
import shutil
import tempfile

from . import warderRadioPackages as packages
from . import warderRadioWorld as world

COUNTRY = re.compile(r'^[A-Z]{2}$')


def prune_inactive(paths_root, active_code, enigma_directory=None,
                   require_external=True, selected=None):
    root = Path(paths_root)
    if (not isinstance(active_code, str) or not COUNTRY.fullmatch(active_code)
            or not world._safe_directory(root)
            or (require_external and root.stat().st_dev == Path('/').stat().st_dev)):
        return {'changed': False, 'skipped': 'unsafe-storage'}
    from . import warderRadioCountry as country
    directory = Path(enigma_directory) if enigma_directory is not None else country.DIRECTORY

    def still_active():
        if country.active_country(directory) != active_code:
            return False
        return selected is None or selected(active_code) is True

    if not still_active():
        return {'changed': False, 'skipped': 'country-superseded'}

    parent = root / 'picon' / 'radio'
    if parent.is_symlink() or not parent.is_dir():
        return {'changed': False, 'skipped': 'no-managed-radio-picons'}

    removed = []
    protected = []
    for folder in sorted(parent.iterdir(), key=lambda entry: entry.name):
        cc = folder.name
        if cc == active_code or not COUNTRY.fullmatch(cc):
            continue
        if not still_active():
            return {'changed': bool(removed), 'skipped': 'country-superseded',
                    'removed': removed, 'protected': protected}
        # Names alone NEVER authorize deletion. Only own SHA-signed PNG files.
        if not packages._owned_country_dir(folder, cc):
            protected.append(cc)
            continue

        # Move the complete owned folder to a private stage on the same mount
        # so new GUI/download writes cannot race with file removal.
        quarantine = Path(tempfile.mkdtemp(
            prefix='.warder-prune-'+cc+'-', dir=str(parent)))
        quarantine.rmdir()
        try:
            os.replace(str(folder), str(quarantine))
            if not still_active() or not packages._owned_country_dir(quarantine, cc):
                if not folder.exists():
                    os.replace(str(quarantine), str(folder))
                protected.append(cc)
                continue
            shutil.rmtree(str(quarantine))
            removed.append(cc)
        except OSError:
            if quarantine.exists() and not folder.exists():
                try:
                    os.replace(str(quarantine), str(folder))
                except OSError:
                    pass
            protected.append(cc)
    return {'changed': bool(removed), 'active': active_code,
            'removed': removed, 'removed_countries': len(removed),
            'protected': protected}
