# FullHDGlass Warder Evolution — checked-in source

Current implementation: **1.0.15**. `package-root/` is the receiver filesystem payload and `control/` contains package metadata and executable installation scripts.

The original extraction baseline was stable 1.0.4, SHA256 `9ceb1713fa237d39f13b4baf728852323086205528c5622df7def58b5812c0bd`. Subsequent committed changes bring this tree to the current release; do not mistake the extraction origin for the current version.

Build with `python3 tools/build-release-ipk.py`. Current IPK SHA256: `f06208c40d8798301ed5499c2c0f8110b270fb3dacfd92c88005d204bc73fa0d`. Its 1,296 packaged files matched the checked-in blobs on 2026-10-23.

Preserve approved graphics and runtime compatibility identifiers. See `PROJECT-CONTINUITY.md` and `docs/BACKUP-RESTORE.md`.
