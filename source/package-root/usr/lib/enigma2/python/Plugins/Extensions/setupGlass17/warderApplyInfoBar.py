#!/usr/bin/env python
# Apply only the selected InfoBar screen after package extraction.
from __future__ import print_function
import os
import re
import sys

base = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.sep
skin_path = os.path.join(base, "usr/share/enigma2/hd_glass17/skin.xml")
plugin_dir = os.path.join(base, "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17")
variants_path = os.path.join(plugin_dir, "hdg17Screens.xml")
settings_path = os.path.join(base, "etc/enigma2/settings")
def log(message):
    # Installation status is reported by the package manager, not a disk log.
    return None

def read_lines(path):
    with open(path, "r") as handle:
        return handle.readlines()

def main():
    settings = {}
    try:
        for line in read_lines(settings_path):
            if "=" in line:
                key, value = line.rstrip("\r\n").split("=", 1)
                settings[key] = value
    except Exception:
        pass
    if settings.get("config.plugins.setupGlass17.par4", "True").strip().lower() in ("true", "1", "yes"):
        selected = "3"
    else:
        selected = settings.get("config.plugins.setupGlass17.par14", "1").strip()
    if selected not in ("1", "2", "3", "4", "5"):
        selected = "1"
    source = read_lines(variants_path)
    screen = []
    inside = False
    start = re.compile(r'^\s*<screen\s+name="InfoBar-' + re.escape(selected) + r'"(?:\s|>)')
    for line in source:
        if not inside and start.search(line):
            inside = True
            line = line.replace('name="InfoBar-' + selected + '"', 'name="InfoBar"', 1)
        if inside:
            screen.append(line)
            if "</screen>" in line:
                break
    if not screen or "</screen>" not in screen[-1]:
        raise RuntimeError("selected InfoBar-%s not found" % selected)
    original = read_lines(skin_path)
    output = []
    inside_old = False
    replaced = False
    for line in original:
        if not replaced and re.search(r'^\s*<screen\s+name="InfoBar"(?:\s|>)', line):
            output.extend(screen)
            inside_old = True
            replaced = True
        elif inside_old:
            if "</screen>" in line:
                inside_old = False
        else:
            output.append(line)
    if not replaced:
        raise RuntimeError("active InfoBar not found in skin.xml")
    new_data = "".join(output)
    old_data = "".join(original)
    if new_data == old_data:
        log("UNCHANGED variant=%s" % selected)
        return
    mode = os.stat(skin_path).st_mode & 0o7777
    temp = skin_path + ".warder-tmp"
    try:
        with open(temp, "w") as handle:
            handle.write(new_data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temp, mode)
        os.rename(temp, skin_path)
    finally:
        try: os.unlink(temp)
        except OSError: pass
    log("APPLIED variant=%s" % selected)

try:
    main()
except Exception as error:
    log("ERROR %r" % (error,))
    print("Warder InfoBar setup skipped: %r" % (error,))
