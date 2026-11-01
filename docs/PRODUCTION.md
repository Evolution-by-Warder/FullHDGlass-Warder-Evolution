# FullHDGlass 1.0.61 — production

The owner approved 1.0.60-test3 on 1 November 2026 and explicitly requested a normal release. Version 1.0.61 contains the approved repairs for complete menu rows, long headers, EPG timeline, CoolTVGuide captions/window framing and live setup receiver-display text. The bound layout callback startup correction is preserved.

The public IPK passed the release workflow and independent download/payload verification. Runtime code, layouts, graphics and helpers are identical to TEST3 apart from version labels; localized History is updated. Native package ordering accepts upgrades from 1.0.59 and all 1.0.60-test builds.

Production activation verifies the immutable public IPK and checksum before publishing exactly the same bytes to main/packages and advancing both main native update profiles together. The historical modernization test profile mirrors production. main/update.json stays at the unchanged legacy 1.0.18 bridge. Exact release and activation status is recorded in PRODUCTION.json and reports/stable61-public-20261101.json; actual installed updater checks are recorded in reports/stable61-live-updater-20261101.json.

Existing settings, graphics, approved LCD4linux/Quick Menu behavior, bitrate helpers and original author credits remain. This release does not claim exhaustive physical receiver validation.
