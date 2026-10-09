#!/usr/bin/env python3
"""Regression for OpenATV eConsoleAppContainer's executable/argv contract."""
import ast
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_PATH = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py"
PLUGIN = PLUGIN_PATH.read_text(encoding="utf-8")
TREE = ast.parse(PLUGIN)


def dotted_name(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return dotted_name(node.value) + "." + node.attr
    return None


start_method = next(
    node for node in ast.walk(TREE)
    if isinstance(node, ast.FunctionDef) and node.name == "_warderStartAuxiliaryComposite"
)
launch_calls = [
    node for node in ast.walk(start_method)
    if isinstance(node, ast.Call)
    and isinstance(node.func, ast.Attribute)
    and node.func.attr == "execute"
    and dotted_name(node.func.value) == "self.warderAuxWorker"
]
assert len(launch_calls) == 1, "expected one auxiliary eConsoleAppContainer launch"
call = launch_calls[0]
assert [dotted_name(arg) for arg in call.args] == [
    "sys.executable", "sys.executable", "worker_path", "request_path", "result_path"
], "OpenATV requires executable as both command and child argv[0]"


def openatv_execute(arguments):
    """Mirror python_console.i -> execute(cmdline, argv+1) -> execvp(cmd, argv)."""
    executable = arguments[0]
    child_argv = arguments[1:]
    return subprocess.run(
        child_argv,
        executable=executable,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        timeout=10,
    )


with tempfile.TemporaryDirectory(prefix="warder-econsole-argv-test-") as temp_dir:
    temp = Path(temp_dir)
    worker = temp / "worker.py"
    request = temp / "request.json"
    result = temp / "result.json"
    worker.write_text(
        "import json, sys\n"
        "with open(sys.argv[2], 'w') as stream:\n"
        "    json.dump(sys.argv, stream)\n",
        encoding="utf-8",
    )
    # All-string JSON is also a valid Python expression. With the old call,
    # Python ran this request file as its script, exited 0, and left result empty.
    request_data = {
        "row": "aux-prov",
        "variant": "black",
        "destination_base": "/tmp/picons",
        "downloads_manifest_url": "https://example.invalid/downloads.json",
        "descriptor_path": "/tmp/auxiliaryProduction.json",
    }
    request.write_text(json.dumps(request_data, sort_keys=True, separators=(",", ":")), encoding="utf-8")
    result.write_text("", encoding="utf-8")

    broken = openatv_execute((sys.executable, str(worker), str(request), str(result)))
    assert broken.returncode == 0
    assert broken.stdout == ""
    assert result.read_text(encoding="utf-8") == ""

    result.write_text("", encoding="utf-8")
    fixed = openatv_execute((sys.executable, sys.executable, str(worker), str(request), str(result)))
    assert fixed.returncode == 0, fixed.stderr
    assert json.loads(result.read_text(encoding="utf-8")) == [str(worker), str(request), str(result)]

print("OpenATV eConsoleAppContainer executable/argv regression: PASS")
