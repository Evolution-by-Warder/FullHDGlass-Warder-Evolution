# FullHDGlass17 Warder Evolution — remaining picon download migration inventory

Updated: 2026-10-04  
Branch: `warder-modernization-work`  
`main` is TABU.

## Purpose

This is the authoritative inventory for the last runtime channel-picon path that still depends on picon.cz. It is preservation/migration work only; it does not authorize changes to the preserved original archive/Trezor or to a Warder Master Registry.

## Runtime call chain

`downloadMenu` -> user selects one of the satellite-selectable channel-picon families -> `satSelectorScr` -> selected `SATLIST` entries -> `downloadMenu.downMulti(k, Ddir)` -> `https://picon.cz/download/<legacy-id>/` -> temporary `/tmp/a.7z` -> 7zip extraction -> `cprmFiles(Ddir)`.

The picon.cz URL exists only in this satellite-selected channel-picon path. The ordinary Warder asset path already uses `assets/warder/downloads.json`, HTTPS, SHA256, redirect checks and safe ZIP extraction.

## Satellite-selected channel-picon families

The menu and `destDir()` mapping prove these legacy SATLIST columns:

| Menu family | selector value | SATLIST column | destination |
| --- | ---: | ---: | --- |
| 400x240 channel picons | 3 | 3 | `picon_400x240` |
| 220x132 channel picons | 9 | 9 | `picon_220x132` |
| black channel picons | 5 | 5 | `picon` |
| black 50x30 channel picons | 4 | 4 | `picon_50x30` |
| white channel picons | 7 | 7 | `picon` |
| white 50x30 channel picons | 6 | 6 | `picon_50x30` |
| OLED channel picons | 8 | 8 | `piconOled` |

These correspond to catalog families currently marked unavailable:
`picon_400x240`, `picon_220x132`, `picon-black`, `picon_50x30-black`, `picon-white`, `picon_50x30-white`, `piconOled`.

`ZZPicon-v` is also unavailable in the Warder catalog, but it is **not** part of the SATLIST/`downMulti()` satellite path and must be migrated separately.

## SATLIST coverage

The current code contains 59 selectable rows:
- 4 provider/package aliases at the top: Freesat 0.8W, Digi/Telly 0.8W, Antiksat 16.0E, Skylink 23.5E.
- 1 DVB-T sk/cz row.
- 54 orbital-position rows from 45.0W through 85.1E.

Each SATLIST row contains:
`(display label, cleanup namespace, satellite-picon key, 400x240 legacy id, black-50x30 legacy id, black legacy id, white-50x30 legacy id, white legacy id, OLED legacy id, 220x132 legacy id)`.

The numeric values in columns 3..9 are **legacy picon.cz download identifiers**, not stable Warder asset IDs. They must not become the identity of the new backend.

## Migration rule

Do not replace picon.cz with guessed per-position URLs. The Warder backend must key the new assets by stable family + satellite/provider identity and provide filename, byte size and SHA256 in a Warder-owned manifest. Runtime must consume only that manifest.

Required target hierarchy:

`assets/warder/downloads/picons/channels/<family>/<satellite-key>/...`

Recommended stable family IDs:
- `channel-400x240`
- `channel-220x132`
- `channel-black`
- `channel-black-50x30`
- `channel-white`
- `channel-white-50x30`
- `channel-oled`

DVB-T sk/cz must remain explicitly distinguishable from orbital satellite positions. Provider/package aliases must also remain separate identities even where they share an orbital position.

## Source-of-truth constraint / blocker

This repository does **not** currently contain the channel-picon archives required to populate those seven families. It contains the already-migrated provider/satellite/CAM/weather/UI archives, but no canonical per-position channel-picon payloads.

Therefore runtime picon.cz removal is blocked until the authoritative preserved channel-picon source / Warder Master picon dataset is available in the migration workspace. Do not synthesize archives, silently substitute another picon set, or repoint the legacy IDs to unrelated files.

When the canonical payload is available:
1. inventory every archive without modifying it;
2. map each archive to stable family + SATLIST identity;
3. verify archive integrity;
4. compute byte size + SHA256;
5. publish Warder-owned assets/parts;
6. extend the manifest;
7. replace `downMulti()` with manifest-driven downloads;
8. add CI guards forbidding runtime picon.cz access;
9. physically test representative satellite, provider alias and DVB-T selections on receiver.

## Locked unrelated baseline

TEST191 WHOLE RADIO is PHYSICAL PASS / LOCKED. This migration must not modify Radio code or its accepted visuals/lifecycle.
