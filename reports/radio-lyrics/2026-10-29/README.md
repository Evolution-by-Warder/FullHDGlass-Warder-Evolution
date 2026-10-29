# SK/CZ lyrics-source check — 29 October 2026

**Corrected after the TEST9 notice-filter finding.** The original TEST8 summary counted a Hudba.sk missing-text notice as a success twice for Lucie Bílá — Láska je láska. Those two records share the exact SHA256 of the independently reproduced 41-character notice. `validated-summary.json` excludes them; `results.json` retains the original raw observations unchanged.

Twelve predefined songs (six Slovak, six Czech), two rounds per source: 96 independent lookups through the four current TEST8 adapters. Selection combines owner-reported failures and familiar songs; it is a small convenience sample, not a representative airplay or full-catalogue coverage survey.

| Current adapter | Distinct songs found, out of 12 (either round) | Successful lookups, out of 24 | Median time to found text |
| --- | ---: | ---: | ---: |
| Hudba.sk | 6 | 11 | 3.540 s |
| LRCLIB | 7 | 13 | 3.815 s |
| Youradio | 6 | 12 | 6.850 s |
| lyrics.ovh | 2 | 4 | 4.474 s |

Together the sources found 10/12 songs. LRCLIB uniquely contributed Alan Murin — Prepáč and Damiens — Stýská se mi; Hudba.sk uniquely contributed Karel Gott — Trezor; Youradio uniquely contributed Faraon — Šlapací kolo. lyrics.ovh added no unique result in this sample. Majself — Posledný hráč and Júlia Hečková — Taliansky muzikál remained absent from all current adapters.

At least one HTTP/transport/parsing error occurred in 9/24 LRCLIB lookups and 1/24 for each other adapter. These counts include mixed attempts with a valid miss followed by a failing optional query; they do not mean each service was wholly unreachable.

## Interpretation and proposed priority

For clearly labelled SK/CZ music formats, such as Rádio KIKS Československo and Fun Rádio Československé hity, the strongest starting combination in this corrected sample is LRCLIB plus Hudba.sk: LRCLIB found more distinct songs (7 versus 6), while successful Hudba.sk responses were a little faster. Keep both available without waiting for one to time out; retain Youradio for complementary catalogue coverage. lyrics.ovh is a lower-priority backup here. The earlier recommendation based on seven Hudba.sk songs is superseded.

This is a measured recommendation, not a released priority change. TEST8 already starts its alternatives after at most 750 ms (or an earlier primary miss), so merely swapping the first source can save only that initial head start; it cannot create missing texts or eliminate network failures. Do not turn this into a slow sequential wait-for-each-server chain. A station's preferred format is a hint, not proof of every song's language.

## Method and limits

- Fresh lookup for every trial; no local result cache and no local provider backoff carried between trials.
- One sequential worker per provider; the four provider workers run concurrently from the same host. At least 1.1 s between request starts on a host; Retry-After respected.
- Uses the pinned TEST8 helper's exact identity matcher, parsers, URL variants and per-source request limits. Results measure our current adapters, not every page potentially present on each website.
- No radio/receiver was involved. Timing includes HTTP/body download and parsing from the measurement host, not latency guaranteed on a receiver.
- The median above includes successful lookups only; misses are separately recorded in results.json. A fast miss is not a fast successful match.
- The data stores only artist, title, timing, status, size and hashes. No song lyrics or downloaded HTML are committed.

Reproduce from a checkout with the TEST8 helper:
```sh
python3 reports/radio-lyrics/2026-10-29/benchmark.py --helper-dir source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17 --output /tmp/warder-lyrics-benchmark --rounds 2
```

The helper source commit and file SHA256 values are embedded in results.json. This report changes no runtime, update feed or package.
