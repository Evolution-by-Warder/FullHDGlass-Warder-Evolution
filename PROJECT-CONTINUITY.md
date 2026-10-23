# Settings UI development checkpoint — 2026-10-23

The owner explicitly approved modernizing the settings UI as part of a shared Warder Evolution style. Work remains on `warder-modernization-work`; production `main`, update.json and update-test.json stay at 1.0.15.

The working payload is **1.0.16-test251**, a manual receiver-validation candidate. Eleven owned settings screen classes receive the shared presentation. A frozen AST fingerprint verifies unchanged controllers, configuration, actions and callbacks. Existing graphics/XML, radio baseline and download backend remain unchanged. System MessageBox/ChoiceBox/InputBox and positioning/OLED screens are outside this first candidate.

See [shared style](design/WARDER-UI-STANDARD.md), [inventory](design/settings-ui-inventory.json) and [candidate instructions](docs/SETTINGS-UI-TEST251.md). A native receiver test of this candidate is still required before production promotion.

## Stable recovery baseline — retained below

# FullHDGlass Warder Evolution — current recovery state

Updated: 2026-10-23 (Europe/Bratislava).

## Authoritative state

Repository: Evolution-by-Warder/FullHDGlass-Warder-Evolution.
Development branch: `warder-modernization-work`.
Published branch: `main`.
Before this documentation refresh both refs pointed to `cf521fc9c44b8fd18d76cd58639bf4e1bd2f3af1`. The backup inventory records their final exact heads, including this documentation refresh.

Current stable and test channel: **1.0.15**.
IPK: `packages/enigma2-skin-fullhdglass17-warder-evolution_1.0.15_all.ipk`.
SHA256: `f06208c40d8798301ed5499c2c0f8110b270fb3dacfd92c88005d204bc73fa0d`.
Both update JSON files publish the same version, URL and hash.

An independent download passed SHA256 verification. Every one of the 1,296 payload/control files matched its checked-in Git blob; no missing or extra packaged files were found. Translation source PO files remain in Git and are intentionally excluded by the release builder.

The checked-in `source/package-root/` and `source/control/` are the current 1.0.15 implementation. Their historical origin in the 1.0.4 extraction does not make 1.0.4 the current release.

## Published picon backend

Authoritative live catalog: `assets/warder/downloads/picons/channels/manifest.json`.
Delivery: persistent raw-GitHub multipart archives, recorded with size and SHA256.
Current catalog: **468 packages**, **45 satellite positions**, three channel styles (transparent/white/black), sizes **50x30, 220x132 and 400x240**.
Since release 1.0.13, content-only picon publication follows the live main catalog and does not require a new IPK.

The approved Network4/contrast publication was merged in PR #8 at `cf521fc9c44b8fd18d76cd58639bf4e1bd2f3af1`.
Its 72 changed live archives were independently downloaded, reassembled and checked against SHA256. Their 639 replaced PNGs and 72 added aliases matched the approved artwork exactly. All 138 applicable production/candidate receiver download plans passed.
Source artwork: PiconHub commit `09e6e6ed78f3dbd18daeefe3fb88108e14f4e9d7`.
Detailed original evidence remains in `reports/network4-publication-20261022.json`.

Historical statements such as NOT_PUBLISHED, 114 packages, runtime_cutover=false and an immediate requirement to install TEST196/205 are dated work history. They are not the current publication state or current installation instruction.

## Preserved implementation and limits

Preserve the receiver-approved radio baseline (test250, released as stable 1.0.6 and retained by current releases), graphics, XML geometry and original author credits. Preserve runtime identifiers `enigma2-skin-fullhdglass17`, `hd_glass17`, `setupGlass17`, `g17_setup_pict`, `extraScreens17` and the user overlay configuration.

This backup/documentation operation changes no receiver runtime, artwork, IPK or download archive bytes. It is not a new physical receiver test. Do not declare historical OLED/7zip, metadata-log or pending artwork observations resolved merely because the source and packages are safely stored; preserve their evidence until separately verified.

Old development journals and checkpoints remain as dated history. For current recovery and release state use this file and `docs/BACKUP-RESTORE.md`.

## Backup

The complete current repository is included in set `warder-backups-20261023`. Final snapshot refs, all checksums and offline restore evidence belong to the delivered `BACKUP-MANIFEST.json`, not to a temporary Actions artifact. See `docs/BACKUP-RESTORE.md`.
