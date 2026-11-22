"""Exactly one active Warder Radio Live bouquet, chosen by OSD or saved preference.

The signed bundled Radio Browser world offers 224 country choices, but the
receiver registers only ONE live bouquet. An earlier experimental TEST141
224-folder index is retired only when all managed files and the managed
index block remain byte-identical. User and TV/SAT bouquets are untouched.
"""
from pathlib import Path
from . import warderRadioBundledWorld as bundled
from . import warderRadioCountry as country
from . import warderRadioCountryBouquets as old_country


def migrate_old_test_country_folders(directory):
    directory = Path(directory)
    index = directory / 'bouquets.radio'
    if index.is_symlink() or not index.is_file() or index.stat().st_size > old_country.MAX_INDEX_BYTES:
        return {'changed': False, 'skipped': 'unsafe-radio-index'}
    before = index.read_bytes()
    if old_country.START not in before and old_country.END not in before:
        return {'changed': False, 'skipped': 'no-old-country-roots'}
    if before.count(old_country.START) != 1 or before.count(old_country.END) != 1:
        return {'changed': False, 'skipped': 'ambiguous-country-roots'}
    owner_path = directory / old_country.OWNER
    try:
        owner = old_country._read(owner_path)
    except (ValueError, OSError):
        return {'changed': False, 'skipped': 'unsafe-old-ownership'}
    if owner is None:
        return {'changed': False, 'skipped': 'unowned-old-country-roots'}
    tracked = owner['files']
    if len(tracked) != 224:
        return {'changed': False, 'skipped': 'incomplete-old-country-roots'}
    country_codes = []
    for name, sha in tracked.items():
        match = old_country.NAME.fullmatch(name)
        if not match:
            return {'changed': False, 'skipped': 'unexpected-old-country-file'}
        country_codes.append(match.group(1))
        path = directory / name
        if path.is_symlink() or not path.is_file() or old_country.digest(path.read_bytes()) != sha:
            return {'changed': False, 'skipped': 'modified-old-country-file'}
    if len(set(country_codes)) != 224:
        return {'changed': False, 'skipped': 'duplicate-country-code'}
    expected = old_country.block(country_codes)
    if before.count(expected) != 1:
        return {'changed': False, 'skipped': 'modified-country-index'}
    selected = old_country.selected_country(directory)
    if selected and selected != country.active_country(directory):
        choice = country.request_country(selected, directory)
        if not choice.get('accepted'):
            return {'changed': False, 'skipped': 'country-choice-not-preserved'}
    updated = before.replace(expected, b'', 1)
    if not updated.startswith(b'#NAME '):
        return {'changed': False, 'skipped': 'invalid-radio-index'}
    # Remove the obsolete block only after all SHA/identity checks above.
    old_country._write(index, updated)
    for name in tracked:
        target = directory / name
        if target.is_file() and not target.is_symlink() and old_country.digest(target.read_bytes()) == tracked[name]:
            target.unlink()
    if owner_path.is_file() and not owner_path.is_symlink():
        owner_path.unlink()
    marker = directory / '.warder-radio-selected-country.json'
    if marker.is_file() and not marker.is_symlink():
        marker.unlink()
    return {'changed': True, 'retired_country_roots': 224, 'selected': selected}


def sync(paths_root, directory, require_external=True, source_archive=bundled.SOURCE):
    """Verify 224-country catalogue on external PATHS; register one live bouquet."""
    directory = Path(directory)
    if directory.is_symlink() or not directory.is_dir():
        return {'changed': False, 'skipped': 'unsafe-enigma-directory'}
    result = bundled.sync_world(
        paths_root, require_external=require_external, source_archive=source_archive)
    if not (result.get('changed') or result.get('skipped') == 'already-current'):
        return result
    migrated = migrate_old_test_country_folders(directory)
    result['old_test_bouquets'] = migrated
    if migrated.get('skipped') not in (None, 'no-old-country-roots'):
        return {'changed': False, 'skipped': 'old-country-migration-blocked',
                'cause': migrated.get('skipped')}
    initial = country.bootstrap(directory)
    result['initial_country'] = country.active_country(directory)
    result['live_country_bouquet'] = initial
    result['changed'] = bool(
        result.get('changed') or migrated.get('changed') or initial.get('changed'))
    result['country_choices'] = 224
    result['active_bouquets'] = 1
    return result
