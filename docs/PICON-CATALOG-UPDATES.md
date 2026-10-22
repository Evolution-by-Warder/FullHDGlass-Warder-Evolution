# Picon catalogue updates after 1.0.13

Stable native channel-picon downloads (all positions and providers in the 220x132
channel catalogue, including Canal+ SK, Canal+ CZ and full 23.5E) use:

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

Users on 1.0.12 or earlier need the one-time upgrade to 1.0.13. Later approved
channel-picon changes need only another download from the skin; choose replacement
mode to overwrite existing PNGs. This does not enable automatic background file
installation. Legacy archive-only resolutions and pinned auxiliary assets retain
their separate existing migration policies.

Verification:

- `tools/test-live-picon-catalog.py` changes a served catalogue twice for each
  style in one receiver instance, with no code/version change, and checks that
  corrupt downloads cannot overwrite installed PNGs.
- `tools/test-picon-native-sync.py` uses the actual receiver manifest loader,
  archive downloader and selective installer against the public approved backend.
- `tools/test-complete-canalplus-install.py` checks both complete production
  packages in all three styles with the receiver queue and installer.
