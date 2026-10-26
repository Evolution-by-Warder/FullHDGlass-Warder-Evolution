# FullHDGlass 1.0.20 — jemná priehľadnosť nastavení (26. 10. 2026)

Aktuálna úloha používateľa: všetky nastavovacie a výberové obrazovky bez LiveTV majú mať jemnú priehľadnosť ako schválený GSU. Nový balík1.0.20 zachováva identitu enigma2-plugin-skins-fullhdglass-warder-evolution, runtime paths/setupGlass17 a existujúcu migračnú verziu1.0.18.

Spoločná vrstva: CLEAR root, jedna výplň #1a102136 pod obsahom, banner orezaný na164px cez WarderSettingsHeader, nepriehľadné okraje a spodná lišta. Pôvodná bitmapa a preview artwork sa nemenia. Menia sa iba prezentácia a riadené skrytie/obnova rendereru Pig pri prepínaní hlavného menu a nastavení. Výberový riadok a posuvníky zostávajú nepriehľadné.

Rozsah:10 konkrétnych layoutov +3 vlastné dialógy; dedené výbery a všetky skupiny konfigurácie používajú spoločné layouty. Pôvodné pomocné TV overlaye a hlavné menu s LiveTV sa neprestavujú. Fyzické zobrazenie novej priehľadnosti zatiaľ nebolo potvrdené používateľom.

Vydávanie1.0.20: build-settings-ui workflow publikuje stabilný native IPK a publish-native-skin.py overí verejné release/raw bajty pred aktualizáciou výhradne update-production.json. update.json/update-test.json zostávajú na overenom bridge1.0.18, jeho IPK sa neprepisuje ani znovu nevydáva. Preview ZIPy zostávajú na nemenných URL. main musí zodpovedať explicitnému expected_main_sha a vydávacia vetva zdrojovému revision; všetko fast-forward, bez force/rebase.

Podrobnosti a poznámky pre používateľa: docs/CURRENT-RELEASE.md. Staršie záznamy nižšie sú historické a nie sú pokynom vrátiť verziu alebo migrovať znova.

## Predchádzajúca produkcia

# Current installed-skins production state — 24 October 2026

FullHDGlass **1.0.19** uses the owner-authorized package identity `enigma2-plugin-skins-fullhdglass-warder-evolution` for native installed Skin Packages. Existing users first receive bridge **1.0.18**, then the new identity through `update-production.json`. See docs/PACKAGE-TRANSITION.md and docs/PRODUCTION.json for exact published identities.

The question about removing 17 from runtime paths was informational only. `hd_glass17`, `setupGlass17`, XML paths and configuration keys are not renamed. All older current-version statements below are historical. Production acceptance and limits remain documented; no physical receiver test of this migration is claimed.

## Previous production record

# Authoritative production state — 24 October 2026

The owner accepted the current FullHDGlass skin and PiconHub plugin for production, and explicitly requested production numbering without test. **FullHDGlass 1.0.17** is the production release; **PiconHub 0.1.25** is its approved companion.

FullHDGlass preserves TEST270 behavior/artwork and changes the runtime, package-control and displayed version labels to 1.0.17. Both updater feeds advance only after public package verification. Separate preview archives retain their immutable TEST263 URLs. Exact package identity and source revision are recorded in docs/PRODUCTION.json after the verified build; approval and the frozen TEST270 baseline are in docs/PRODUCTION-APPROVAL.json. See docs/PRODUCTION.md.

Owner acceptance and automated checks are recorded; no new exhaustive physical receiver test is claimed. This current section supersedes every older current/candidate-version statement below. Preserve historical 1.0.15 recovery and all dated receiver evidence.

## Historical checkpoints — superseded for current release selection

# Current settings release: TEST266

Fixes ChoiceBox onLayoutFinish crashes on OpenATV by registering a bound method instead of a lambda. Regression tests reproduce the exact receiver dispatch. Includes the shared Warder skull logos, shortened plugin-list title and existing TEST264 message text visibility fix. No receiver run of TEST266 is claimed. Both supplied crash logs identify the same callback TypeError. Earlier checkpoints below are historical.

# TEST264 update-content fix — 24 October 2026

Current candidate 1.0.16-test264 fixes receiver-reported invisible update dialog text. The ScrollLabel outer eWidget is raised above the opaque panel; native confirmation and timers are preserved. Regression coverage checks full question content, outer container zPosition and callback result. TEST263 was published in both native update feeds at 69b351cffa8e9df97f351aa78e05d6c5e9f4e014; the owner requested this correction and delivery through the same updater. TEST264 reuses the verified TEST263 external preview assets and small-package design. No physical receiver validation is claimed.

# Settings UI checkpoint — 24 October 2026

Repository Evolution-by-Warder/FullHDGlass-Warder-Evolution, branch warder-modernization-work.

TEST260 appearance and TEST259 responsiveness were confirmed by the owner on the receiver.
Current candidate: **1.0.16-test263**, separating optional preview ZIPs from the small IPK with SHA256-verified background caching. The owner authorized the full collected batch on 24 October.
See docs/SETTINGS-UI-BATCH261.md for the approved list and docs/SETTINGS-UI-TEST263.md for delivery notes.

New owned dialogs are private to setupGlass17, not global Enigma2 overrides. Configuration moves exclusively to WHERE_PLUGINMENU; the old setup-menu branch is removed. Native session-start and optional ECM/weather entries are retained. Exact reviewed AST changes in design/settings-batch261-logic.json normalize to the original frozen controller fingerprint; all unreviewed controller mutations still fail. Original radio/graphics source hashes remain unchanged; new settings-only assets are independently pinned. Build-time PNG compression changes IDAT only, preserves all RGBA pixels and metadata, and is verified independently in the package. No Pillow dependency is added on the receiver. Preview I/O and rendering now always run in the child process, avoiding synchronous HDD/ZIP access in GUI; type thumbnails are pre-extracted by the downloader thread. Optional archives are verified, persistent downloads in the selected data directory, not IPK content.

The owner explicitly authorized TEST263 for the built-in updater on 24 October 2026. tools/publish-settings-update.py verifies the public small IPK and preview assets before atomically activating both feeds. A physical receiver run of TEST263 is not claimed.

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
