# Dynamic Radio Browser bouquets and picons — source-only candidate

## Radio Live TEST129: výber krajiny a predvolená krajina podľa jazyka

Tento návrh nahrádza starý režim, ktorý predbežne synchronizoval všetky krajiny. Zostáva jeden **Warder Radio Live** na prvom mieste v rádiových bouquetoch. Obsahuje vždy iba **jednu aktívnu krajinu**.

- **Prvé spustenie:** `warderRadioCountry.initial_country()` číta `config.osd.language` zo systémových nastavení Enigma2. Napríklad `sk→SK`, `cs→CZ`, `de→DE`, `en→GB`, `fr→FR`, `it→IT`, `pl→PL`; neznámy jazyk má bezpečný predvolený výber `SK`.
- **MENU → Vybrať krajinu (Warder Radio Live):** natívny hook `PluginDescriptor.WHERE_CHANNEL_CONTEXT_MENU` len pre hrateľnú stanicu v našom zozname (nie globálny systémový patch). Zoznam krajín pochádza z lokálneho katalógu už nainštalovaného Radio pluginu.
- **Zachovanie nastavení:** súbor `/etc/enigma2/warder-radio-live-country.json` ukladá aktívnu krajinu nezávisle od jazyka systému. Po zmene jazyka alebo reštarte zostane posledný úspešný výber.
- **Bezpečný prechod:** nové rádio sa sťahuje na pozadí; aktívny bouquet sa zmení až po overení celej krajiny. Neúspešné, prerušené alebo prázdne sťahovanie ponechá predchádzajúcu krajinu a jej stanice. Bounded pages pre veľké krajiny; viac než 4000 staníc momentálne vyžaduje osobitné riešenie.
- **Žiadny celosvetový prefetch:** picony sa doťahujú podľa potreby z existujúcej Radio Browser cache. Pôvodný Warder Radio Streams sa odstráni len po úspešnom nasadení online dát aktívnej krajiny.
- **Testy:** `tools/test-radio-country.py` (14 scenárov) spolu s `tools/test-radio-live.py` (42 scenárov) sú v cielenej CI zelené. Pre test129 sa overilo 56/56 offline scenárov a SHA256 IPK. Natívne ovládanie MENU a načítanie bouquetu na prijímači zostávajú na fyzický test.



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
- Failed image retrieval is eligible for retry after 15 minutes, and repeated row renders cannot keep postponing the pending worker. Missing mount points do not permanently block retries.
- The image folder is created, if needed, by the background worker after checking that its parent is on actual external storage. The GUI does not create picon folders.
- Malformed Radio Browser UUIDs, credential-bearing URLs and invalid stream addresses are discarded before bouquet publication.

## Validation

Offline regression suite: `python3 tools/test-radio-live.py -v`. CI workflow: `.github/workflows/radio-live-safety.yml`. **30/30 focused tests passed** on the working branch after hardening of UUID/stream validation, retries, optional-country fallback and disk cache initialization.

First receiver test of 1.0.81-test124 on 2026-11-19 showed only the original Warder Radio Streams bouquet. Receiver repair 1.0.81-test125 now also starts the live import from postinst, forces a retry after the prior test124 failed-first-import cooldown, reloads the radio index after postinst has registered the live file, and records a sanitized error/status for `warderRadioLive.py --diagnose`. Its standalone package builder and publishing workflow are separate from production update feeds; 30/30 focused tests and IPK SHA-256 verification passed. **The fix still requires a fresh physical receiver retest.**

Native receiver acceptance is **not yet confirmed**. Before merging or releasing, physically check the live bouquet and visible picon renders on GigaBlue Quad 4K Pro / OpenATV 8.1 and Octagon SF8008 (including fallback), the active PATHS destination and Own Picons, startup/offline cases, scrolling performance, and 7-day refresh behavior. Full OpenATV/OpenPLi workflow failures unrelated to this change must be evaluated separately; a passing focused test is not a release authorization.

## Files

- `warderRadioLive.py`: new isolated bridge, synchronization, safety checks, on-demand background loader.
- `warderRadioUpdate.py`: starts/stops the optional new controller when companion Radio plugin exists, preserving existing updater.
- `warderChannelPicons.py`: queue a request only after a real native picon miss.
- `tools/test-radio-live.py`: offline regressions.
