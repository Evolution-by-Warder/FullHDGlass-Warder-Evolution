"""Reverse only recorded OpenATV 8.1 bindings before older graphic checks."""
import json

def revert_skin(root, text):
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
