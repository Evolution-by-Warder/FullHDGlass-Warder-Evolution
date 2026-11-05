# Reuse CANAL+ SK/CZ artwork across satellite and provider sets

The completed CANAL+ SK/CZ PNGs are copied byte for byte wherever the reviewed service mapping identifies the same station and variant. No artwork is rendered, resized or recreated.

| Verified scope | Result |
|---|---:|
| Original CANAL+ SK/CZ package variants preserved | 18 |
| Updated package variants | 144 |
| Satellite positions | 16 |
| Provider selectors | 4 |
| Replaced PNG entries | 5,486 |
| Added exact current-reference PNG entries | 2,046 |
| Original unrelated archive entries preserved | 241,880 |
| Rendered graphics | 0 |

Provider selectors: Antiksat, Digi/Telly, freeSAT and Skylink. Positions: 0.8W, 5W, 7W, 8W, 22W, 24.5W, 30W, 9E, 13E, 16E, 19.2E, 23.5E, 26E, 28.2E, 39E and 42E.

Jednotka and Dvojka use the same approved CANAL source in 23.5E, 0.8W, 16E and the matching provider packages. Existing native CANAL references in the full 23.5E package already matched; other current service types and aliases are synchronized while retaining their original exact filenames. Newly added references come from the supplied November 3 lamedb, including full namespaces and decimal-to-hex service types.

The 480 accepted service mappings retain HD/SD/UHD, country, language and regional labels. Another 161 name candidates are held for independent identity/variant evidence. These are candidate service mappings, not a count of unfinished artwork. In particular, a shared generic name does not justify mixing Czech Nova and Bulgarian NOVA, Hungarian and German RTL, German ONE and Egyptian ON E, or generic test services.

The original source is pinned to FullHDGlass catalogue commit `0a7f09b96cd73091d7ab53ca3976e8f1957b170b` and PiconHub source `b498c30b11f47f28bbc7a068d5bd671395ca4e8c`. Master/source reuse was recorded in [PiconHub master](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/commit/ea20b2328333763f0c06c18411c8c5dbe58d2a74), covering 1,815 PNG path changes. The guard also blocks ordinary Vhannibal writes to these reused identities across positions.

Validation: every original and resulting ZIP passed CRC checks; every changed PNG matched its canonical source bytes; every unrelated member retained its original bytes; all 18 CANAL source package objects remained identical. Published staged part Git object hashes are compared against the independently verified local part hashes. The receiver's production manifest validator passes. Original content-addressed archives remain available; no IPK changes are needed.

The detailed [verification.json](verification.json) lists every archive and reference, before/after hashes and identity evidence. [reuse-map.json](reuse-map.json) records the reviewed mapping; [held-candidates.json](held-candidates.json) records unresolved market/variant candidates. Radio-plugin work is separate and unchanged.
