#!/usr/bin/env python3
import importlib.util
import os
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE = os.path.join(ROOT, "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPiconSync.py")
spec = importlib.util.spec_from_file_location("warderPiconSync", MODULE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

assert m.normalize_service_reference("1:0:1:1328:CA2:3:EB0000:0:0:0:") == "1_0_1_1328_CA2_3_EB0000_0_0_0"
assert m.normalize_service_reference("#SERVICE 1:0:1:1328:CA2:3:EB0000:0:0:0:") == "1_0_1_1328_CA2_3_EB0000_0_0_0"
assert m.normalize_service_reference("garbage") == ""
assert m.service_orbital_position("1:0:1:1328:CA2:3:EB0000:0:0:0:") == "23.5e"
assert m.service_orbital_position("1:0:1:1:1:1:C00000:0:0:0:") == "19.2e"

with tempfile.TemporaryDirectory() as d:
    with open(os.path.join(d, "bouquets.tv"), "w") as h:
        h.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.warder.tv" ORDER BY bouquet\n')
    with open(os.path.join(d, "userbouquet.warder.tv"), "w") as h:
        h.write("#NAME Warder test\n")
        h.write("#SERVICE 1:0:1:1328:CA2:3:EB0000:0:0:0:\n")
        h.write("#DESCRIPTION Skylink sample\n")
        h.write("#SERVICE 1:0:1:1:1:1:C00000:0:0:0:\n")
        h.write("#SERVICE 1:0:1:1328:CA2:3:EB0000:0:0:0:\n")
    refs = m.bouquet_services(d)
    assert refs == [
        "1_0_1_1328_CA2_3_EB0000_0_0_0",
        "1_0_1_1_1_1_C00000_0_0_0",
    ]
    req = m.build_sync_request(d, ["23.5e"], "transparent", "220x132")
    assert req["mode"] == "sync-tv-lists"
    assert [x["service_reference"] for x in req["services"]] == ["1_0_1_1328_CA2_3_EB0000_0_0_0"]
    assert req["services"][0]["position"] == "23.5e"

print("Warder picon sync parser/planner: PASS")
