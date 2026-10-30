# Managed IPTV radio bouquet

`warderRadioUpdate.py` owns only `/etc/enigma2/userbouquet.warder.radio`, its single previous-version backup and the scheduling state `warder-radio-update.json` plus its lock. Radio index registration appends only the exact managed bouquet reference to `bouquets.radio`. No television index or personal bouquet is modified.

Package `postinst` launches `python3 -B .../warderRadioUpdate.py --refresh` with stdin/stdout/stderr redirected to `/dev/null`, in the background. It does not wait for network access or restart Enigma. The worker has a 90-second total deadline, 15-second HTTP timeouts, a 4 MiB bouquet bound and lower CPU priority. Source manifest and bouquet are read at the same validated immutable revision before SHA-256 and structural validation. No network or file import runs on the GUI thread.

If no managed file exists, the validated download is published with an exclusive hard link from a complete temporary file, so a concurrently created user file cannot be overwritten. Existing managed files retain checksum checks, atomic replacement and one previous-version backup. An existing file with a different header is left alone. Symlink or non-regular managed/index paths are skipped. Temporary download files are removed after publication or errors.

The index keeps its original bytes and ordering; a missing final newline is added only before our appended entry. An existing reference is recognized with LF or CRLF line endings. Repeated imports cannot duplicate the entry. Missing registration for an existing managed bouquet can be repaired without a network request when the weekly check is not due.

The active FullHDGlass session controller checks after 60 seconds, then wakes hourly. Actual network checks remain due once per seven days after success, or six hours after a failed attempt. Missing/unset system time postpones access. After GUI startup the controller reloads bouquet data once after a successful/unchanged check, including data installed by postinst; subsequent reloads occur only on changes. It never zaps, stops playback or restarts the receiver.

Automated checks: `PYTHONDONTWRITEBYTECODE=1 python3 tools/test-radio-weekly-update.py -v`. Physical receiver validation of first import remains pending until the owner confirms it. The vault is outside this work and is not accessed.
