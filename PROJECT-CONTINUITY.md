# Infobar follow-up1.0.28

Owner confirmed RDS logo works in1.0.27, but OK infobar remains default. g17PicRef2/3 retained separate old lookups. Both now delegate file lookup to g17PicRef and use native radio fallback before default. Preserve their original timers, cache and animations.13 tests pass including actual changed handlers for both variants. Expected main08e5de87b1d7b374092a345f0e3f27ac14b532f7; publish1.0.28 after CI; receiver confirmation pending.

# Published radio picon repair1.0.27 — 27October2026

CI40472607046 success. Source0635b15b815f0b7529c5720a058fa36f41866b7b, activatedb31d2ba13776a05c557c5b0687920a63483cae3d on main/work. Stable Latest and production updater offer1.0.27. IPK14198444 bytes SHA25696f2f2e368ece20f2054b7008854aac24ecb79fbc8f05b36ff3b9c95ddd28be4.12 radio renderer tests,22 layout tests, full artwork/package checks and1329 payload files verified. Existing picon directory first; existing legacy dimension directories read for radio only; native reference/name lookup before default. Exact custom path retains precedence, TV and native DAB preserved. XML and graphics baseline unchanged. Receiver test pending: BAYERN3 AAC radio with RDS should show existing station logo in bottom panel and infobar. No redownload/move required. Full evidence docs/RADIO-PICON-1.0.27.json. GSU r90 receiver acceptance is recorded in GSU repository.

# Completed production — 27 October 2026

FullHDGlass1.0.26 successfully published and active in production updater. CI40464125832 success; source81fd43b9a917e1e3e7b1b621b5555c11e3eafd88; activation22df05850e94da74dbe001b536c57e7e8852f6bb. IPK14198238 bytes SHA25652d68d8637bce1d03f1c35b4fa1cd49a675c986d8e154efdce660fec9888c6df. Owner confirmed FullHDGlass1.0.26, GSU13.40-r88 and PiconHub0.1.25 OK. No exhaustive all-hardware validation claimed. Separate new GSU cosmetic request: opaque system and channel signal meter backgrounds, tracked in GSU repository as r90.

Final scope: all three backgrounds of provider/satellite PNGs220x132 are in original piconProv.zip/piconSat.zip, roots piconProv/piconSat. Six archive bytes unchanged from1.0.24. Channel220 uses picon. No retired directories created; existing unmatched user files preserved; only byte-equal obsolete copies removed after successful installation. Renderer cache invalidation and canonical preference included. Each setup launch schedules a fresh update check3s after layout, HTTPS runs in native child, offline silent, close cancels timer/worker, manual check cancels duplicate automatic offer. Existing consent, validation and3-second GUI restart retained. Native visual/runtime confirmation pending. Bridge1.0.18 remains unchanged.

# Published 1.0.23 — canonical Help bundle and stale-preview fix

Stable release v1.0.23, release ID424592424. IPK14196996 bytes SHA2569192e250d5e94062c7232a9b74a8b7397fed8c2ef5f599f0d083a7099f788cbd. Canonical g17_setup_pict.zip27041172 bytes SHA2560bf966980978558170d43429b7ee8de312d0eb15d29978393a3c610af0bd2c31, all252 original names, manual and automatic downloads share identical content. Source1961f3753a2817419b0c0253f86511929f328245. All build/artwork/payload tests passed. Publication URL allowlist was corrected with19 regression tests and activation completed only after independently checking public raw IPK and ZIP bytes. Original bridge1.0.18 remains unchanged. Receiver visual confirmation pending. Provider/satellite directory unification remains the next explicitly discussed follow-up; do not claim done or remove unmatched user files.

# Final 1.0.23 architecture — canonical original Help bundle

Owner explicitly rejected a separate prepared Help bundle. Build now produces `g17_setup_pict.zip` with all 252 original names under `g17_setup_pict/`. Publisher verifies the release ZIP, stages the same bytes at the original raw download path and atomically updates only the Help entry in assets/warder/downloads.json alongside it. It verifies raw bytes before activating the IPK feed. Original artwork build input is pinned at 81ff0fb83709344d696c73ed70530ef09651916b (original ZIP SHA872d59...). Both automatic assets and manual Nápoveda share this canonical content. Prepared per-image copies remain in configured hdg17_files/preview; native GUI receives RAM copies for responsiveness. Superseded 1.0.23 builds were held before publication via source-head guard; keep version1.0.23 if still unpublished.

# 1.0.23 — stale preview correction

Receiver diagnostics: 1.0.22 help ZIP verified; helper resolves 50x-0,196-1,197-1,9-1; 66-0 unavailable. On-screen picture stays stale despite different selections. Replaced Twisted scheduling with native eTimer/eConsoleAppContainer; retain single asynchronous worker, debounce, timeout and stale-generation rejection. Clear previous bitmap using existing verified fully transparent 40x40 asset. Do not fall back to a missing source path. Background alpha now follows original bubble shading, zero outside; informative mask remains byte-exact. New visual verification pending receiver.

# 1.0.22 — translucent help artwork

Owner requested every auxiliary bubble illustration to retain its contour and informative content with subtly translucent background. Prepared background alpha230/255, protected foreground unchanged, native alpha blend; style revision invalidates old extracted PNGs. Optional help ZIP is versioned with this release; no in-menu pixel processing and no IPK growth from preview ZIP. Native visual confirmation pending.

# Aktuálne vydanie — FullHDGlass1.0.21 (26. 10. 2026)

**Stabilné Latest1.0.21 je vydané a overene aktívne v update-production.json.** Zdroj f13415af0d8c57bf85a29a3b50b17c2f5d15cd88; workflow40362507691 aj radio40362507737 success. Overené všetky252 pomocné ilustrácie, gettext, radiové/grafické baseline a1327 súborov IPK. Balík14 196 202 bajtov; SHA256cc9fb7789d1a3c8c7b43b95a2aed4072753a0506aba31e3a68c9e076bb35be3a. Skutočný release aj raw balík overené publisherom, API releaseasset digest a live feed zhodné.

Všetky13 spoločné nastavovacie/výberové layouty a vlastné dialógy majú jemný presvit #1a102136 ako GSU. Dedené výbery a skupiny používajú tieto spoločné layouty. Banner je orezaný na164px, zachovaná geometria, náhľady, nepriehľadný výber/posuvník. Hlavné menu s LiveTV zachované; WarderSettingsPig bráni jeho návratu v režime nastavení aj po natívnom onShow. Natívny vzhľad ešte čaká na potvrdenie používateľom.

Staré update.json/update-test.json sú zámerne stále bridge1.0.18 s pôvodným hashom. Existujúce preview ZIPy a migračné balíky nemazať ani neprepisovať. Aktuálny native feed je update-production.json. Dokumentácia/README a strojový záznam docs/SETTINGS-GLASS-1.0.21.json sú uložené. Týmto je implementačná úloha pripravená na prijímačové vizuálne overenie; ďalšie zmeny podľa používateľovej spätnej väzby.

## Implementačné a historické poznámky

# Finálna aktualizácia1.0.21 — návrat do nastavení bez LiveTV

Verzia1.0.20 prešla CI40360019022 a je overene publikovaná. Záverečné čítanie natívneho OpenATV Screen.show ukázalo, že po onShow callbackoch zavolá renderer.onShow; samotný prepínač režimu preto nebráni opätovnému Pigu po návrate z popupu. Finálna1.0.21 používa iba v konfigurácii WarderSettingsPig, ktorý pri každom onShow rešpektuje parent.isMainMenu, inak obnoví plnú TV a skryje malý widget. Natívne Pig nemeníme globálne. Regresný test simuluje opakované resume v nastaveniach a návrat do menu.

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

Pripravené PNG sa trvalo ukladajú do `preview/` v nastavenej ceste skinu (napr. `/media/hdd/hdg17_files/preview/`). Po reštarte sa znovu použijú bez sťahovania či rozbaľovania archívu. Pomocný proces pred zobrazením pripraví malú RAM kópiu, aby čítanie disku neblokovalo menu. Pôvodné pomocné obrázky ani používateľské súbory sa neprepisujú.

Owner follow-up pending: investigate and unify provider/satellite directories piconProv vs piconProv_220x132 and piconSat vs piconSat_220x132. Current infobars select both paths, so do not delete directories blindly. User notes same 220x132 content duplicated; preferred canonical names are the original folders without dimension suffix. Complete active Help fix first.
