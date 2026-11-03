"""Reverse only recorded OpenATV 8.1 bindings before older graphic checks."""
import json

def revert_skin(root, text):
    # The OpenPLi guide is an exact registered addition. Remove only that block
    # before checking the unchanged historical OpenATV graphic baseline.
    path = root / 'design/openpli-graph-epg/layout.json'
    if path.exists():
        import hashlib
        for item in json.loads(path.read_text())['additions']:
            addition = item['inserted_text']
            assert hashlib.sha256(addition.encode()).hexdigest() == item['sha256']
            assert text.count(addition) == 1, item['name']
            text = text.replace(addition, '', 1)
    path = root / 'design/openatv81-bindings/skin-edits.json'
    if path.exists():
        for edit in json.loads(path.read_text())['edits']:
            assert text.count(edit['updated_screen']) == 1, edit['name']
            text = text.replace(edit['updated_screen'], edit['original_screen'], 1)
    path = root / 'design/openatv81-compatibility/skin-edits.json'
    if path.exists():
        for edit in json.loads(path.read_text())['edits']:
            assert text.count(edit['updated_screen']) == 1, edit['name']
            text = text.replace(edit['updated_screen'], edit['original_screen'], 1)
    return text
