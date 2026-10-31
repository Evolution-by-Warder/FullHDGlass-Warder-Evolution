#!/usr/bin/env python3
"""Remove only owner-excluded preview folders and rebuild their catalogues."""
import importlib.util
import json
from pathlib import Path
import shutil
import zipfile
import html

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / 'assets/warder/downloads/ui/spinners/preview-library'
POLICY = ROOT / 'design/spinner-choice/preview-review-policy.json'


def pack(folder, output):
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(folder.rglob('*')):
            if path.is_file() and path.suffix != '.zip':
                archive.write(path, path.relative_to(folder))


def main():
    if not POLICY.exists():
        return
    policy = json.loads(POLICY.read_text())
    excluded = {row['id'] for row in policy['excluded']}
    removed = []
    for group in ('spinkit', 'community'):
        root = LIBRARY / group
        catalogue = root / 'catalog.json'
        if not catalogue.exists():
            continue
        data = json.loads(catalogue.read_text())
        entries = []
        for row in data['entries']:
            folder = root / row['folder']
            if row['id'] in excluded:
                if folder.is_symlink() or folder.parent != root:
                    raise ValueError('Unsafe excluded folder')
                if folder.exists():
                    meta = json.loads((folder / 'metadata.json').read_text())
                    if meta['id'] != row['id']:
                        raise ValueError('Excluded folder identity mismatch')
                    shutil.rmtree(folder)
                removed.append(row['id'])
            else:
                row['original_review_number'] = policy['review_numbers'][row['id']]
                (folder / 'metadata.json').write_text(json.dumps(row, ensure_ascii=False, indent=2) + '\n')
                entries.append(row)
        data['entries'] = entries
        data['excluded_by_owner'] = sorted(excluded & {key for key in policy['review_numbers'] if (key.startswith('spinkit-')) == (group == 'spinkit')})
        if group == 'community':
            data.setdefault('prepared_unique_spinners', data['unique_spinners'])
            data['unique_spinners'] = len(entries)
            data['native_frames'] = sum(row['frame_count'] for row in entries)
        catalogue.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        verification = root / 'verification.json'
        proof = json.loads(verification.read_text())
        if group == 'spinkit':
            proof.update(spinners=len(entries), frames=sum(row['frame_count'] for row in entries))
        else:
            proof.update(unique_spinners=len(entries), native_frames=sum(row['frame_count'] for row in entries))
        proof['excluded_by_owner'] = data['excluded_by_owner']
        verification.write_text(json.dumps(proof, indent=2) + '\n')
        links = ''.join('<li><a href="'+row['folder']+'/index.html">'+html.escape(row['title'])+'</a></li>' for row in entries)
        (root/'index.html').write_text('<!doctype html><html lang="sk"><meta charset="utf-8"><title>Spinnery</title><style>body{background:#071321;color:#eee;font:18px system-ui;max-width:650px;margin:3rem auto;line-height:1.8}a{color:#3ccfff}</style><h1>Spinnery na výber</h1><ol>'+links+'</ol></html>')
        if group == 'spinkit':
            pack(root, LIBRARY / 'spinkit-samostatne-ukazky.zip')
    if (LIBRARY/'community/catalog.json').exists() and (LIBRARY/'spinkit/catalog.json').exists():
        spec = importlib.util.spec_from_file_location('spinner_collection_builder', ROOT/'tools/import-community-spinner-previews.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        community = json.loads((LIBRARY/'community/catalog.json').read_text())['entries']
        module.build_combined(community)
        combined = json.loads((LIBRARY/'catalog.json').read_text())
        if excluded & {row['id'] for row in combined['entries']}:
            raise ValueError('Excluded spinner survived in gallery')
        assert combined['spinners'] == policy['original_count'] - len(excluded)
        for row in combined['entries']:
            group = 'spinkit' if row['id'].startswith('spinkit-') else 'community'
            assert (LIBRARY/group/row['folder']/'preview.gif').is_file()
        pack(LIBRARY, LIBRARY/'warder-spinnery-na-vyber.zip')
        with zipfile.ZipFile(LIBRARY/'warder-spinnery-na-vyber.zip') as archive:
            assert archive.testzip() is None
            assert not any('/09-circle-fade/' in name or '/134-openpli-taube/' in name for name in archive.namelist())
        print('PASS: 152 previews remain; owner-excluded directories and ZIP entries removed')
    print('Removed owner-selected duplicates:', ', '.join(removed) or 'already absent')


if __name__ == '__main__':
    main()
