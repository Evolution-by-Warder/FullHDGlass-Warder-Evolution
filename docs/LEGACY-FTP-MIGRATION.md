# Legacy HDGlass FTP -> Warder asset architecture

Updated: 2026-10-04  
Branch: `warder-modernization-work`  
`main` is TABU.

## Decision

The historical HDGlass FTP directory layout is preservation evidence, not the Warder runtime architecture.

Migration is modeled as:

`legacy file A` -> `logical service B` -> `legacy location C` -> `Warder location D`.

After a service is verified on the Warder backend, runtime code must depend only on the stable Warder service key and Warder manifest. The legacy FTP path is retained only in the migration registry and in the separately preserved original FTP snapshot.

The preserved FTP snapshot is never rewritten, reorganized, or used directly by receiver runtime.

## Target layout

- `assets/warder/downloads/picons/channels/` — channel picon packages, keyed by stable family + selector identity.
- `assets/warder/downloads/picons/providers/` — provider picons.
- `assets/warder/downloads/picons/satellites/` — satellite picons.
- `assets/warder/downloads/picons/cam/` — CAM picons.
- `assets/warder/downloads/weather/` — weather icon and weather-info families.
- `assets/warder/downloads/ui/` — help, previews, ExtraScreens, menu and ChannelSelection graphics.
- `assets/warder/downloads/helpers/` — runtime helper payloads where still required.

The runtime contract is `assets/warder/downloads.json`. Physical paths are implementation details behind stable service keys.

## Migration registry

`assets/warder/legacy-ftp-migration.tsv` records the recovered legacy path, logical service, stable runtime key, Warder target path, legacy SHA256, current SHA256 and migration state.

States:
- `MIGRATED_EXACT` — current Warder payload is byte-identical to the recovered FTP archive.
- `MIGRATED_REPACKED` — the logical payload has already been migrated but the archive bytes differ from the preserved FTP archive.
- `MIGRATED_REPACKED_SPLIT` — migrated payload is delivered as deterministic GitHub-sized parts.
- `SOURCE_PRESERVED_TARGET_MISSING` — source is known in the preserved FTP snapshot but the Warder target is not currently present.
- `ARCHIVE_ONLY` — historical package/changelog retained for preservation and not a runtime asset.

## Current audit result

The recovered FTP inventory contains 27 recorded files. Nineteen are downloadable asset families relevant to the old download menu, and eight are historical skin/skin-vip package or changelog files.

Of the 19 asset families:
- 18 already have a Warder logical destination.
- 2 are byte-identical migrations: `CHSPiconbig` and `animWeatherIcons`.
- 16 are migrated/repacked equivalents.
- 1 preserved source currently has no Warder payload: `weatherIcons/piconWeather.zip` (runtime key `weatherIcons`).

Important: `assets/catalog.json` currently labels `weatherIcons` as available although its declared Warder path is absent from the branch and `downloads.json` has no `weatherIcons` entry. Treat it as NOT READY until the preserved source is restored into the Warder tree and manifest.

The satellite-selected channel-picon path is a separate remaining legacy dependency: `downMulti()` still calls picon.cz by numeric SATLIST ID. It is not part of the captured HDGlass FTP snapshot. Do not mix that external picon.cz migration with the HDGlass FTP mirror migration.

## Runtime cut-over rule

A legacy service may be considered cut over only when:
1. its Warder target payload exists;
2. byte size and SHA256 are recorded in `downloads.json`;
3. receiver code resolves the stable service key through the Warder manifest;
4. no old FTP URL/path is required at runtime;
5. extraction/install behavior is preserved;
6. representative receiver test passes.

After all services satisfy this rule, old FTP routing can be deleted from runtime code. The preserved original FTP snapshot remains untouched as recovery/history only.

## Future replacement rule

A migrated legacy payload may later be replaced by a new Warder-generated version without changing the receiver-facing service key. Only the manifest metadata and payload change. This is the mechanism for gradually replacing old picons after the complete Warder download backend is stable.
