# Dynamic Radio Browser bouquets and picons — source-only candidate

Status: **draft PR #124**. No release, installer, feed, version bump, or deployed receiver change.

## Runtime ownership

- The existing `userbouquet.warder.radio` and its once-per-week updater remain unchanged; the new managed file is **`userbouquet.warder.live.radio`**.
- Radio Browser is the only online station source. The bridge imports the installed `Plugins.Extensions.WarderRadio.radio_browser.RadioBrowser` client and the existing `station_logos.StationLogos` normalizer/cache.
- The first live sync uses Slovakia, Czechia, and the valid two-letter selected Radio plugin country (if different), up to three paged requests per country. This is a bounded first version, *not* a mirror of the entire world catalogue.
- A stable Enigma2 service identity is derived from the Radio Browser UUID. Stream URL changes preserve the picon stem. Only our managed `userbouquet.warder.live.radio` and its own sidecars may be replaced.
- The managed bouquet records its own SHA-256; modified owned files with the same `#NAME` header are not overwritten.
- The receiver's personal bouquets and Radio plugin settings/favourites/history are not touched. Network failures keep the last working live bouquet.
- Timed network and logo download workers are spawned outside Enigma's GUI thread. The online catalogue refresh attempts at most once per day after success or six hours after failure.

## Picons on demand

- Standard native Enigma2 service lists cannot render an HTTP image directly. The bridge therefore asynchronously materializes only requested PNGs to the normal FullHDGlass PATHS picon folder for native lookup.
- ServiceList/picon lookup requests missing live-radio picons through an in-memory queue without networking or filesystem reads on each row.
- An initial small prefetch covers 12 entries per selected country; as the user scrolls, the requested visible stations take priority. The currently playing radio is also eligible.
- The existing Radio plugin validates the remote logo and stores a bounded cache. The bridge writes two Enigma2 filename variants (4097 and 1) using the stable UUID-derived reference.
- Files already owned by the user or an approved picon pack are **never overwritten**. Only unchanged bridge-owned PNGs may be refreshed after seven days.
- The bridge skips auto-writing when FullHDGlass is using **Own Picons** and requires PATHS to point to a real external disk, to avoid filling the image flash.
- A bounded receiver-side registry tracks generated files and safe cleanup, without deleting user-modified PNGs.

## Validation

Offline regression suite: `python3 tools/test-radio-live.py -v`. CI workflow: `.github/workflows/radio-live-safety.yml`.

Native receiver acceptance is **not yet confirmed**. Before merging or releasing, physically check the live bouquet and visible picon renders on GigaBlue Quad 4K Pro / OpenATV 8.1 and Octagon SF8008 (including fallback), the active PATHS destination and Own Picons, startup/offline cases, scrolling performance, and 7-day refresh behavior. Full OpenATV/OpenPLi workflow failures unrelated to this change must be evaluated separately; a passing focused test is not a release authorization.

## Files

- `warderRadioLive.py`: new isolated bridge, synchronization, safety checks, on-demand background loader.
- `warderRadioUpdate.py`: starts/stops the optional new controller when companion Radio plugin exists, preserving existing updater.
- `warderChannelPicons.py`: queue a request only after a real native picon miss.
- `tools/test-radio-live.py`: offline regressions.
