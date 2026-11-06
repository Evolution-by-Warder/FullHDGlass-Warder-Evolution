# Vhannibal completeness audit — 2026-11-06

Status: IN PROGRESS. This is not a completeness certificate.

Authorized scope: satellite TV picons only; no Warder Radio or radio-picon changes. All fixes and reports stay on this working branch. No merge, release or production publication without owner approval.

Verified starting points:
- FullHDGlass main: 603218ea8fa51176f686f14f303509a4c64dc7e1
- PiconHub main: e90a1fe3a2734b555f48f343284f9103530180fb
- PiconHub warder-master-production: a740b6da429b8d93eb0f3123158d81b8724f9d19
- Trezor main: 342e111a9b4adff06121c317d04ba2cfe4f82595
- GSU main: c3978f69303de59391c1ff43b2563592526e97e2

Read root AGENTS.md and WARDER_PROGRESS.md. Open satellite PR #45 records only the historical 3388-candidate comparison; it does not establish full source coverage. Production catalogue has 498 packages / 1804 parts (5,946,489,105 bytes). Reconciled existing plans independently materialize 12508 accepted references.

New evidence: official Vhannibal site offers a November 5 picon release and Motor settings, newer than the previous November 3 source snapshot. Original current picon ZIP downloaded successfully. Next: discover all official source sets, parse every reference and lamedb/transponder/provider record; inspect the real production archives in all nine variants, retain unresolved identities explicitly, protect approved CANAL+ SK/CZ bytes.

The Trezor recursive tree (604 entries, not truncated) contains no Vhannibal-named source archive. Historical Vhannibal imports are documented in PiconHub provenance for September 13 and October 18; original byte availability still to be established.

## Source and physical-audit checkpoint

- Downloaded and CRC-parsed all 26 advertised official downloads: one November 5 picon archive plus 25 settings sets across all six site sections. Also downloaded both identical November 3 original picon copies and both identical matching settings copies from the owner's prior files. SHA-256 inventories are being persisted with the final audit.
- November 5: 14,088 PNG items, 14,084 valid unique reference names. November 3: 14,081 PNG items, 14,078 valid names. Union: 14,104 valid names; 26 new names, 20 removed, 41 same-reference RGBA changes. Radio references are counted as out of scope and never modified.
- Full union classification across all 25 current settings sets: 10,338 exact satellite non-radio matches; 2,237 satellite radio; 367 non-satellite; 1,162 lack exact current settings evidence (not treated as proven obsolete). Latest Motor has precedence over older regional metadata.
- Physical checks have found fully transparent production PNGs for Sky Adventure (13E) and TV5MONDE EUROPE HD (19.2E/0.8W), including legacy service-type aliases. Missing/empty members are real defects, not filename-only candidates.
- Sampled production White archives also contain legacy Chocholousek frames alongside approved MASTER V9 frames. Thus file/reference coverage alone cannot certify V9 artwork compliance. Full background census is required and visual/editorial uncertainty must remain visible.
- Frozen renderer and both current MASTER files have been downloaded and their exact documented SHA-256 digests verified. No source/logo or master is invented or altered.
- Ongoing: all 498 production packages / 1,804 parts are downloaded and decoded incrementally. Safe repairs will copy complete existing nine-variant approved station graphics; ambiguous identities or new compositions remain held for review.
