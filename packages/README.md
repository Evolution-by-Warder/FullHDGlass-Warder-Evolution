# Update packages

FullHDGlass Warder Evolution update packages are stored as ordinary repository files and are downloaded directly through raw GitHub URLs.

GitHub Releases are intentionally not used for updater packages.

The active package URL and SHA-256 checksum are published in `/update.json`.

## TEST packages

Receiver-test builds are generated into `packages/test/` and are intentionally ignored by Git. They are CI artifacts, not stable updater assets. A TEST package must not be copied into this stable package directory or referenced by `update.json` until receiver acceptance and explicit release approval.

Current test candidate: `1.0.5-test1`. Stable remains `1.0.4`.
