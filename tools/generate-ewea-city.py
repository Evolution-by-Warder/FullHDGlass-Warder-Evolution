#!/usr/bin/env python3
"""Generate the Enhanced Weather country/city database from the authoritative r12 city_Code-17.txt."""

from pathlib import Path
import re
import sys

def generate(source):
    rows = source.read_text(encoding="utf-8").splitlines()
    output = []
    country = None
    first = True
    for row in rows:
        if row.startswith("#"):
            country = row[1:].strip()
            if country:
                if not first:
                    output.append("")
                output.append("# " + country)
                first = False
            continue
        if not row.startswith("om|") or not country:
            continue
        parts = row.split("|")
        if len(parts) < 6 or not parts[3]:
            continue
        code = parts[3]
        admin = parts[4]
        if code == "CZ":
            match = re.search(r"\\((?:.*?),\\s*(\\d+)\\)$", parts[1])
            if match:
                admin += " [" + match.group(1) + "]"
        output.append("q|%s|%s||%s|%s" % (parts[2], code, country, admin))
    return "\n".join(output) + "\n"

def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: generate-ewea-city.py SOURCE DEST")
    source = Path(sys.argv[1])
    destination = Path(sys.argv[2])
    destination.write_text(generate(source), encoding="utf-8")

if __name__ == "__main__":
    main()
