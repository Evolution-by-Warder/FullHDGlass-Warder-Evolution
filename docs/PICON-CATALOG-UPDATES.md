# Picon catalogue updates after 1.0.14

Native channel-picon downloads for 50x30, 220x132 and 400x240 use one live
catalogue, including separate Canal+ SK and Canal+ CZ providers and full satellite
position packages:

`https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/channels/manifest.json`

Each download operation fetches and validates the current catalogue. The operation
then uses that snapshot until it completes, so a concurrent publication cannot
mix part hashes from two catalogue versions. A later operation reads the updated
catalogue, including in the same open download screen and without a GUI restart.

Picon-only publication must update the content-addressed archives, their manifest
records and SHA256SUMS together on an approval/work branch, verify them, and then
fast-forward main. Publish archives before or atomically with their catalogue.
Retain older content-addressed archives for in-flight downloads and older skins.
Do not overwrite the bytes behind an existing hash-based archive filename.

For this data-only publication, do not change the installed skin version,
warderPiconSync.py, update.json, update-test.json or any IPK. The optional TEST
catalogue and historical one-off release workflows do not control stable runtime.

The receiver accepts only the explicit official main catalogue and package root.
It validates the schema, package selection, sizes, paths, redirects, every part's
SHA-256 and the complete archive's SHA-256 before installing PNGs. There is no
fallback to an unvalidated or previously cached catalogue on an error.

Users need 1.0.14 for live downloads in all three supplied resolutions. Version
1.0.13 already supports the live catalogue for 220x132. Later approved
channel-picon changes need only another download from the skin; choose replacement
mode to overwrite existing PNGs. This does not enable automatic background file
installation. The separate 150x90 legacy option and pinned auxiliary assets retain their
existing migration policies.

Verification:

- `tools/test-live-picon-catalog.py` changes a served catalogue twice for each
  style in one receiver instance, with no code/version change, and checks that
  corrupt downloads cannot overwrite installed PNGs.
- `tools/test-picon-native-sync.py` uses the actual receiver manifest loader,
  archive downloader and selective installer against the public approved backend.
- `tools/test-complete-canalplus-install.py` checks both complete production
  packages in all three styles with the receiver queue and installer.

## Original satellite archive integration

The supplied source set covers 46 numeric satellite positions. Each supplied
50x30, 220x132 and 400x240 transparent, white and black archive is integrated
through an explicit position/selector binding. The supplied collection has no
transparent 400x240 archive for 68.5E. The existing 45W 220x132 packages remain
available. Menu positions 12.5W, 11.0W, 3.1E, 74.9E, 85.0E and 85.1E have no
matching supplied archive; never substitute a neighboring orbital position.

Import policy is append-only: an existing PNG filename always keeps its current
bytes. At 16.0E and 23.5E the release report records aggregate hashes of every
pre-existing PNG before and after integration. No approved picon, MASTER
background, skin layout or radio graphic is regenerated.

Provider membership continues to follow each existing 220x132 provider package.
New provider sizes use matching original artwork; a missing reference reuses the
approved provider PNG resized proportionally. Canal+ SK and CZ lists remain
separate. A generic position selection downloads the full matching position set,
not one provider's subset.

- Integration evidence: `reports/original-sets-integration-20261022.json`.
- Real receiver queue tests for two simultaneous positions and all nine size/style
  choices: `tools/test-original-set-routing.py`.
- Original integration tool: `tools/integrate-original-sets.py` (one-time migration;
  subsequent data-only updates do not run its version-changing runtime patch).
