"""Verify only optional key guards changed the two audited native screens."""
from pathlib import Path
import json
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
class Tests(unittest.TestCase):
    def test_exact_guarded_screen_delta(self):
        text = (ROOT / "source/package-root/usr/share/enigma2/hd_glass17/skin.xml").read_text()
        record = json.loads((ROOT / "design/openatv81-optional-menu-keys-20261124/skin-edits.json").read_text())
        self.assertEqual({e["name"] for e in record["edits"]}, {"QuickMenu", "InformationNetwork"})
        keys = {"QuickMenu": {"key_blue"}, "InformationNetwork": {"key_blue", "key_menu", "key_info"}}
        for edit in record["edits"]:
            self.assertEqual(text.count(edit["updated_screen"]), 1)
            old = ET.fromstring(edit["original_screen"])
            new = ET.fromstring(edit["updated_screen"])
            self.assertEqual(old.attrib, new.attrib)
            found = set()
            for element in new.iter():
                if element.get("conditional") in keys[edit["name"]]:
                    key = element.get("conditional")
                    self.assertTrue(element.get("source") == key or (edit["name"] == "QuickMenu" and element.tag == "ePixmap" and key == "key_blue"))
                    found.add(key)
                    del element.attrib["conditional"]
            self.assertEqual(found, keys[edit["name"]])
            self.assertEqual(ET.tostring(old), ET.tostring(new))

if __name__ == "__main__":
    unittest.main()
