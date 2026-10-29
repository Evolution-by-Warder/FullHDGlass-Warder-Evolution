# FullHDGlass Warder Evolution — production

Version **1.0.41** is the owner-authorized production promotion of the TEST2 radio renderer and ecosystem runtime cleanup, approved 29 October 2026. The owner retained the current 84 columns, 3px/1px geometry, original colours, transparency and motion; brighter preview variants were rejected and restored before this release.

Stable 1.0.41 upgrades normally from both production 1.0.39 and candidate 1.0.40-test2. A plain 1.0.40 would sort below the TEST2 package in Debian/opkg-style version ordering, so the patch number advances to 1.0.41.

The built-in updater remains `main/update-production.json`, using verified raw-GitHub IPK bytes and SHA256. Feeds activate only after automated checks, every installed-payload byte and independent public download verification. The primary legacy 1.0.18 bridge in main/update.json remains unchanged. The native TEST channel update-test.json follows the verified stable release, so installed TEST2 clients also receive 1.0.41. Existing picon archives and the authoritative live catalogue are preserved.

Package/runtime identities, saved settings, existing lyrics/artwork, RDS/DAB ownership and original author credits remain. This production authorization does not claim exhaustive new physical receiver or CPU measurements. Exact source, release and validation are in [PRODUCTION.json](PRODUCTION.json).
