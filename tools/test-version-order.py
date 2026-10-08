#!/usr/bin/env python3
import ast
import re
from pathlib import Path

def warder_version_tuple(value):
    try:
        value = str(value).strip().lstrip("vV")
        match = re.match(r"^(\d+)\.(\d+)\.(\d+)(?:-test(\d+)(?:-auxstage\d+)?)?$", value, re.IGNORECASE)
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
assert v("1.0.5-test204-auxstage1") == v("1.0.5-test204")
assert v("1.0.5-test203-auxstage1") < v("1.0.5-test204")
assert v("1.0.5-test204") < v("1.0.5-test205")
assert v("1.0.5-test204-auxstage1") < v("1.0.5")
assert v("1.0.5-test204-auxstageX") == (0, 0, 0, 0, 0)
assert v("1.0.5") < v("1.0.6")
assert v("v1.0.5") == v("1.0.5")
assert v("broken") == (0, 0, 0, 0, 0)

# Exercise the parser in plugin.py itself so the test cannot pass while the
# installed runtime comparator still rejects the AUXSTAGE suffix.
root = Path(__file__).resolve().parents[1]
plugin_path = root / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py"
plugin_tree = ast.parse(plugin_path.read_text(encoding="utf-8"))
version_node = next(
    node for node in ast.walk(plugin_tree)
    if isinstance(node, ast.FunctionDef) and node.name == "_warderVersionTuple"
)
namespace = {"re": re}
module = ast.Module(body=[version_node], type_ignores=[])
exec(compile(ast.fix_missing_locations(module), str(plugin_path), "exec"), namespace)

class VersionScreen:
    _warderVersionTuple = namespace["_warderVersionTuple"]

p = VersionScreen()._warderVersionTuple
assert p("1.0.5-test204-auxstage1") == p("1.0.5-test204")
assert p("1.0.5-test204-auxstage1") < p("1.0.5-test205")
assert p("1.0.5-test204-auxstage1") < p("1.0.5")
print("Warder version ordering: PASS")
