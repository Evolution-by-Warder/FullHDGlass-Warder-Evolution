#!/usr/bin/env python3
"""Read-only independent audit of actual published SAT provider picon ZIPs."""
import hashlib
import json
import tempfile
from pathlib import Path, PurePosixPath
from urllib.request import Request, urlopen
from zipfile import ZipFile

PREFIX = ("https://raw.githubusercontent.com/Evolution-by-Warder/"
          "FullHDGlass-Warder-Evolution/main/"
          "assets/warder/downloads/picons/providers/")
EXPECTED = {
    "transparent": (11655483, "8ce25f4964370b93bad33a83459d357f9cff105d"),
    "white": (29626904, "2a6fbbe893608fb53a8d5d5cc69e4db7d8fbd8f7"),
    "black": (28400191, "70a488b0d4393936e26914396d3fe4d483afbb4e"),
}
NAMES = ("BSKYB.png", "COSMOTE TV.png", "SKY DIGITAL.png")


def check():
    result = {}
    with tempfile.TemporaryDirectory(prefix="warder-sat-provider-qa-") as temp:
        for style, (expected_bytes, expected_blob) in EXPECTED.items():
            url = PREFIX + style + "/piconProv.zip"
            target = Path(temp) / (style + ".zip")
            sha256, size = hashlib.sha256(), 0
            request = Request(url, headers={"User-Agent": "Warder-SAT-QA/1"})
            with urlopen(request, timeout=150) as response, target.open("wb") as out:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    size += len(chunk)
                    if size > 55 * 1024 * 1024:
                        raise ValueError(style + ": unsafe ZIP size")
                    sha256.update(chunk)
                    out.write(chunk)
            if size != expected_bytes:
                raise ValueError(style + ": published ZIP size changed")
            sha1 = hashlib.sha1()
            sha1.update(("blob %d\0" % size).encode("ascii"))
            with target.open("rb") as data:
                while chunk := data.read(1024 * 1024):
                    sha1.update(chunk)
            if sha1.hexdigest() != expected_blob:
                raise ValueError(style + ": Git blob SHA mismatch")
            with ZipFile(target) as archive:
                members = archive.infolist()
                broken = archive.testzip()
                if broken:
                    raise ValueError(style + ": corrupt archive member " + broken)
                names = {PurePosixPath(entry.filename).name.casefold(): entry.filename
                         for entry in members if (not entry.is_dir()
                         and entry.filename.lower().endswith(".png"))}
                result[style] = {
                    "bytes": size, "sha256": sha256.hexdigest(),
                    "git_blob_sha1": sha1.hexdigest(),
                    "png_count": len(names), "zip_members": len(members),
                    "crc_valid": True,
                    "named_pngs": {name: names.get(name.casefold()) for name in NAMES},
                }
    return {"source": "FullHDGlass production raw provider ZIPs",
            "mode": "READ_ONLY_NO_PUBLICATION", "styles": result}


if __name__ == "__main__":
    findings = check()
    Path("sat-provider-audit.json").write_text(
        json.dumps(findings, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8")
    print("SAT_PROVIDER_QA=" + json.dumps(findings, ensure_ascii=False, sort_keys=True))
