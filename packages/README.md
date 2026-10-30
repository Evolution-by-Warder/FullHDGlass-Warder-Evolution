# Update packages

`packages/` contains only the current production version, one previous production version, and any package still required by an active migration feed. Matching short and compatibility filenames contain identical IPK bytes.

- Current production: **1.0.42**, offered by `update-production.json` and the native `update-test.json`.
- Previous production: **1.0.41**.
- Required legacy bridge: **1.0.18**, still served by `update.json`.

The updater downloads verified IPKs through their raw GitHub URLs. Releases provide installation downloads and checksum files. Auxiliary ZIPs belong in `assets/warder/downloads/`.

`packages/test/` is ignored by Git and contains transient local/CI build output only. Test downloads are CI artifacts or explicitly published candidates; superseded test IPKs are not retained in the working tree.

After a production activation, remove obsolete package versions and their checksums while preserving every active feed target and the previous production version. Record the removal in `reports/`. Git history is preserved. Trezor is excluded from housekeeping.

[Cleanup evidence](../reports/package-cleanup-20261030.json) · [Auxiliary structure](../docs/AUXILIARY-ASSETS.md)
