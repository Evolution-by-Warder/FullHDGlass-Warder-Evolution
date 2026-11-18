"""Optional on-demand language catalogs; no network I/O on the Enigma2 GUI thread.

The package carries a SHA-256 manifest generated from the exact source commit.
Only files whose digest is in that manifest may be installed. Existing catalogues
are never removed; the English source text works offline without a catalogue.
"""
import hashlib
import json
import os
import re
import struct
import sys
import tempfile
from urllib.request import Request, urlopen

HERE = os.path.dirname(os.path.abspath(__file__))
LOCALE = os.path.join(HERE, "locale")
MANIFEST = os.path.join(HERE, "warder-locale-manifest.json")
BASE = "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/"
DOMAINS = frozenset(("setupGlass17", "helpTxt", "weather", "netatmo", "eWeather"))
LANGUAGES = frozenset(("al", "cs", "de", "el", "es", "et", "fa", "fr", "hu",
                       "it", "lt", "nl", "pl", "pt", "ro", "ru", "sk", "tr", "uk", "zh"))
MAX_BYTES = 1024 * 1024


def normalize(language):
    code = str(language or "en").replace("-", "_").split("_", 1)[0].lower()
    return {"sq": "al", "gr": "el", "cz": "cs", "ua": "uk", "cn": "zh"}.get(code, code)


def _manifest():
    with open(MANIFEST, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if data.get("schema") != 1 or not re.fullmatch(r"[0-9a-f]{40}", data.get("ref", "")):
        raise ValueError("Invalid pinned source revision")
    if not isinstance(data.get("files"), dict):
        raise ValueError("Invalid language inventory")
    return data


def _valid_mo(content):
    # GNU gettext MO magic, either byte order; parse fully before installation.
    if len(content) < 28 or content[:4] not in (bytes.fromhex("de120495"), bytes.fromhex("950412de")):
        return False
    import gettext
    import io
    try:
        gettext.GNUTranslations(io.BytesIO(content))
        return True
    except (OSError, ValueError, EOFError, UnicodeError, IndexError, struct.error):
        return False


def sync(language):
    language = normalize(language)
    if language not in LANGUAGES:
        return 0
    data = _manifest()
    entries = data["files"].get(language, {})
    if not isinstance(entries, dict):
        raise ValueError("Invalid language entries")
    changed = 0
    for domain, digest in sorted(entries.items()):
        if domain not in DOMAINS or not re.fullmatch(r"[a-f0-9]{64}", str(digest)):
            raise ValueError("Invalid catalogue signature")
        target_dir = os.path.join(LOCALE, language, "LC_MESSAGES")
        target = os.path.join(target_dir, domain + ".mo")
        if os.path.isfile(target):
            with open(target, "rb") as stream:
                if hashlib.sha256(stream.read()).hexdigest() == digest:
                    continue
        remote_path = "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/locale/{}/LC_MESSAGES/{}.mo".format(language, domain)
        url = BASE + data["ref"] + "/" + remote_path
        request = Request(url, headers={"User-Agent": "FullHDGlass-locale/1", "Accept": "application/octet-stream"})
        with urlopen(request, timeout=12) as response:
            if response.geturl() != url:
                raise ValueError("Unexpected translation redirect")
            payload = response.read(MAX_BYTES + 1)
        if len(payload) > MAX_BYTES or hashlib.sha256(payload).hexdigest() != digest or not _valid_mo(payload):
            raise ValueError("Translation integrity failure: " + domain)
        os.makedirs(target_dir, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix=".warder-locale-", dir=target_dir)
        try:
            with os.fdopen(fd, "wb") as out:
                out.write(payload)
                out.flush()
                os.fsync(out.fileno())
            os.chmod(tmp, 0o644)
            os.replace(tmp, target)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
        changed += 1
    return changed


def _settings_language():
    try:
        with open("/etc/enigma2/settings", "r", encoding="utf-8", errors="replace") as stream:
            for line in stream:
                if line.startswith("config.osd.language="):
                    return line.partition("=")[2].strip()
    except OSError:
        pass
    return "en"


def main(argv):
    if len(argv) == 2 and argv[1] == "--selected":
        language = _settings_language()
    elif len(argv) == 3 and argv[1] == "--language":
        language = argv[2]
    else:
        return 2
    try:
        sync(language)
        return 0
    except (OSError, ValueError, KeyError, TypeError):
        # Offline is normal. English fallback is always available.
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
