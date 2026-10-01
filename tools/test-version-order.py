#!/usr/bin/env python3
import re

def warder_version_tuple(value):
    try:
        value = str(value).strip().lstrip("vV")
        match = re.match(r"^(\d+)\.(\d+)\.(\d+)(?:-test(\d+))?$", value, re.IGNORECASE)
        if not match:
            return (0, 0, 0, 0, 0)
        major, minor, patch = (int(match.group(i)) for i in (1, 2, 3))
        test_no = match.group(4)
        if test_no is None:
            return (major, minor, patch, 1, 0)
        return (major, minor, patch, 0, int(test_no))
    except (TypeError, ValueError):
        return (0, 0, 0, 0, 0)

v = warder_version_tuple
assert v("1.0.4") < v("1.0.5-test1")
assert v("1.0.5-test1") < v("1.0.5-test2")
assert v("1.0.5-test2") < v("1.0.5")
assert v("1.0.5") < v("1.0.6")
assert v("v1.0.5") == v("1.0.5")
assert v("broken") == (0, 0, 0, 0, 0)
print("Warder version ordering: PASS")
