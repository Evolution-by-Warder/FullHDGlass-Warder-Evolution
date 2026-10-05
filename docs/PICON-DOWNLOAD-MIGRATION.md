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

Historical pre-publication note: runtime picon.cz removal was blocked until the authoritative Warder Master dataset and deterministic packages were available. That prerequisite has now been satisfied for the published transparent/black/white Warder backend; picon.cz remains only as the reviewed legacy fallback while receiver cut-over is validated. Do not synthesize missing families or repoint legacy IDs to unrelated files.

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


## Cross-repository source verification — 2026-10-04

The authoritative sources have now been checked rather than inferred.

### Trezor / Chocholousek originals

`Evolution-by-Warder/Trezor/archives/chocholousek-picons/PROJECT-CONTINUITY.md` confirms:
- Trezor is the immutable original/recovery archive.
- `Evolution-by-Warder/PiconHub-Warder-Evolution` is the maintained working picon repository.
- Chocholousek migration scope is 2,202 selectable archives + 1 preview = 2,203 total, across 8 resolutions, 21 backgrounds/styles and 58 satellite/provider/DTT targets.
- The source catalogue is `id_for_permalinks(240624).log`; the exact generated source manifest is archived losslessly in Trezor.
- Original archives must never be edited, internally renamed, recompressed or replaced by corrected picons.
- Windows acquisition/preservation is incomplete; bulk picon.cz acquisition was explicitly stopped after the source began returning anti-abuse HTML instead of archives.

Therefore Trezor is a provenance/reference source, **not** a runtime asset server and not a place to generate modified FullHDGlass payloads.

### Warder Master / PiconHub production

The live `warder-master-production` branch of `Evolution-by-Warder/PiconHub-Warder-Evolution` was inspected. It already contains maintained per-service PNG data organized by orbital/provider identity and variants such as:
- `picons/0.8w/digi-hu/{transparent,black,white}/...`
- `picons/0.8w/digi/{transparent,black,white}/...`
- `picons/0.8w/digislovakia/{transparent,black,white}/...`

This confirms that PiconHub is the correct maintained-data authority for building future FullHDGlass channel-picon packages. It must not be confused with the immutable Chocholousek archive.

### Important format gap

PiconHub's maintained tree currently proves transparent/black/white service-reference PNG variants, but that alone does **not** prove availability of every legacy FullHDGlass output family (400x240, 220x132, 50x30, OLED) or the exact legacy archive membership expected by each SATLIST selection.

Consequently:
- black/white source data can be mapped from Warder Master where identities match;
- no 400x240/220x132/50x30/OLED archive is to be fabricated merely by resizing/rerendering unless a separate project rule explicitly authorizes that transformation;
- Chocholousek originals may be used for provenance/comparison and recovery, but never overwritten;
- Vhannibal remains enrichment/diff only and cannot become the authority for this migration.

### Migration architecture now fixed

`Chocholousek originals (Trezor, immutable provenance) -> Warder Master Registry / maintained PiconHub data -> generated FullHDGlass download packages -> FullHDGlass Warder manifest/runtime`.

The old picon.cz numeric SATLIST IDs remain migration evidence only. They are not Warder identities.

### Next implementation batch

Before touching `downMulti()`, derive a machine-readable SATLIST-to-Warder mapping table and audit which of the 59 selectors have authoritative maintained data for transparent/black/white. Mark unresolved selectors/families explicitly; do not fill gaps by assumption. This mapping becomes the input to deterministic package generation and later manifest publication.


## Machine-readable SATLIST mapping — 2026-10-04

Created `assets/warder/picon-satlist-mapping.tsv` from the live legacy SATLIST and the live `warder-master-production` PiconHub tree. It preserves every legacy family ID while introducing a stable Warder key and an evidence-based state.

Current selector coverage: **40 MATCHED / 17 MISSING = 57 total selectors**. MATCHED means an authoritative maintained provider/orbital tree exists in Warder Master; it does not claim that all seven legacy output resolutions/families are already packaged. MISSING means no matching maintained tree was established and must not be silently aliased to a nearby orbital position.

Special identities are preserved: provider/package selectors are separate from orbital selectors; 1.0W vs 0.8W, 4.8E vs 4.9E, 74.9E vs 75.0E, and 85.0E vs 85.1E are not collapsed. DVB-T SK/CZ remains unresolved rather than guessed.


## Warder Master variant coverage audit — 2026-10-04

Created `assets/warder/picon-warder-master-coverage.tsv` by enumerating the live `warder-master-production` tree for all 40 MATCHED selectors.

**Result: all 40/40 matched selectors contain all three maintained variants: transparent, black and white.** Across those selector scopes the tree contains 9671 transparent + 9671 black + 9671 white PNG path entries (29013 PNG entries total). Counts are source-path counts, not a claim of globally unique service references: selectors such as the full 0.8W orbital tree can contain the same service-reference filename under multiple provider subtrees.

Two examples show why packaging must deduplicate by service-reference filename at generation time: 0.8W has 929 PNG paths per variant but 722 distinct service-reference filenames across its provider subtrees; 16.0E has 581 paths per variant but 560 distinct filenames. The package generator must use deterministic collision handling and must fail/report when two same-variant files with the same service-reference filename have different bytes; it must never silently choose one.

This audit proves source readiness only for the maintained transparent/black/white variants. It does not authorize synthetic 400x240, 220x132, 50x30 or OLED output. Those legacy families remain unresolved until their authoritative source/transformation rule is established.


## Collision audit — 2026-10-04

Completed blob-SHA collision analysis for transparent/black/white across all 40 MATCHED selector scopes. Results are stored in `assets/warder/picon-collision-audit.tsv` and the unresolved identities in `assets/warder/picon-collision-conflicts.tsv`.

- 38/40 matched selectors are collision-free by service-reference filename.
- Only the aggregate orbital selectors **0.8W** and **16.0E** contain duplicate filenames across provider subtrees.
- Across all three variants there are 480 duplicate-name cases: **465 are byte-identical and safe to deduplicate**, while **15 are true byte conflicts**.
- Those 15 variant-level conflicts reduce to only **5 service-reference identities**: 3 at 0.8W and 2 at 16.0E, repeated consistently across transparent/black/white.
- 0.8W conflicts are provider-specific (Digi Slovakia/Freesat vs MagioSat/Slovak Telekom, plus Freesat vs Telly). 16.0E conflicts are A1 Broadcasting vs Antiksat.

Packaging rule is now concrete: identical SHA duplicates may collapse automatically; different-SHA duplicates must remain unresolved and make aggregate-package generation fail until an explicit provider-aware precedence/identity rule is approved. Provider-specific selectors (Freesat, Digi/Telly, Antiksat) remain independently packageable and must not inherit aggregate-orbit ambiguity.


## Deterministic package-plan implementation — 2026-10-04

Added `tools/generate-picon-package-plan.py` and `assets/warder/picon-download-manifest.schema.json`. The planner is intentionally non-destructive: it does not download, resize, rerender, package, publish or switch receiver runtime. It consumes only the audited mapping/coverage/collision tables and emits a stable JSON build plan.

CI now executes the planner as a preflight gate and asserts the current audited state: **57 selectors = 38 READY + 2 collision-BLOCKED (0.8W, 16.0E) + 17 MISSING_SOURCE**. READY currently means transparent/black/white only. All unresolved legacy 400x240/220x132/50x30/OLED families remain blocked by policy.

The manifest schema requires HTTPS URL, byte size and SHA256 and limits the first publishable families to `channel-transparent`, `channel-black` and `channel-white`. No receiver runtime has been switched to this manifest yet.
