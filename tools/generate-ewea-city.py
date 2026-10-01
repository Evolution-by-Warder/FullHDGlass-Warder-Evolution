#!/usr/bin/env python3
"""Generate the r12 Enhanced Weather city database from city_Code-17.txt."""

from pathlib import Path
import re
import sys


def generate(source):
    rows = source.read_text(encoding="utf-8").splitlines()
    output = []
    for index, (code, country) in enumerate((("SK", "Slovakia"), ("CZ", "Czechia"))):
        if index:
            output.append("")
        output.append("# " + country)
        for row in rows:
            if not row.startswith("om|"):
                continue
            parts = row.split("|")
            if len(parts) < 6 or parts[3] != code:
                continue
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
