# Stable 1.0.61 — 1 November 2026

The owner explicitly approved the current TEST3 and requested a normal release and all release records. Version 1.0.61 promotes its row fitting, header/timeline, CoolTVGuide caption and setup display fixes. Preserve the corrected bound callback that prevents the TEST1 startup failure. The approved adapters, graphics and helpers are unchanged apart from version labels and localized History.

Build and regression workflow runs before publication; production activation verifies immutable public release bytes and updates both native main profiles together. The historical modernization test profile must mirror production. Keep main/update.json at its immutable 1.0.18 migration bridge. Exact final evidence is recorded in reports/stable61-public-20261101.json and docs/PRODUCTION.json. No blanket physical hardware compatibility claim is made.

Earlier records below are historical and superseded by this release where applicable. The broader OpenATV 8.1 audit and separate PiconHub/GSU pending work remain separate.

---

# Stable 1.0.55 — 1 November 2026

Owner confirmed fast bitrate startup and measured video/audio on GigaBlue, including FTA and encrypted CANAL+ services. Stable v1.0.55 is public/latest and both native update profiles now point to its verified raw main/packages IPK. Public package SHA256: 9164c640b58e579f76ceaaeb7c57cd4e0e036ec73db23d549eccaad4727319db; 17204826 bytes. Build: f712696ce3d2688fe363b09023b43cd74bfcc4a2; workflow 41292891930. Promotion workflow 41293148989 succeeded without rebuilding. See reports/bitrate-stable55-20261101.json.

The normal version 1.0.55 intentionally follows 1.0.54-test5 so native package ordering accepts the upgrade. Receiver-approved helper bytes are identical to test5. Diagnostic logging is disabled by default. The legacy update.json migration bridge remains 1.0.18. MIPS and Dreambox physical validation remains pending. Do not replace any published IPK bytes.

---

# Update channel repair — 29 October 2026

Owner reported that installed TEST2 did not see production 1.0.41. TEST2 selects warder-modernization-work/update-test.json, which incorrectly remained at legacy 1.0.18. The native TEST feed now mirrors the verified production manifest, and the publisher advances both native channels together. main/update.json alone remains the primary historical migration bridge; installer refusal of unprepared legacy packages remains. Actual TEST2 IPK updater methods and worker were compared with the regression path; automatic and manual offers passed. Runtime, package bytes, version, colour frames and settings unchanged. Details: docs/UPDATE-CHANNEL-REPAIR-2026-10-29.json.

# Published production 1.0.41 — 29 October 2026

All three owner-authorized production updates are live: FullHDGlass 1.0.41, PiconHub 0.1.32 and GSU 13.40-r92. FullHDGlass source 75d295371858880ce708f54c222ce026eebf6e6a; updater activation b55499059a435308dc4482c3fd6799ac21df4168. CI 40919233098 passed 381 tests, 1,402 installed-payload checks, all 252 help illustrations and live lyrics probes. Public release IPK independently downloaded and identical to the tested local package; production publisher verified raw-GitHub delivery before activating update-production.json. Original TEST2 colours/84 columns/motion retained, rejected colour previews never published. Legacy bridge and existing picon assets preserved. Exact evidence: docs/PRODUCTION.json and docs/RADIO-PRODUCTION-1.0.41.json. No exhaustive new device/CPU claim.

# Production 1.0.41 — 29 October 2026

Owner explicitly requested production deployment of all three plugins and full records. Keep original TEST2 colours, 84 columns, 3px bars/1px gaps, transparency and motion; rejected brighter previews were restored and never published. Promote FullHDGlass 1.0.41, PiconHub 0.1.32 and GSU 13.40-r92 so package managers upgrade from the numbered candidates normally. Existing publisher guards, verified public bytes, SHA256 and final feed readback remain mandatory. FullHDGlass retains the shared PiconHub cleanup engine; approved artwork and live picon assets are preserved. Latest production status/evidence: docs/PRODUCTION.json. Authorization does not imply exhaustive new receiver testing.

# Candidate 1.0.40-test2 — radio GUI load fix, 29 October 2026

Owner reports severe GUI unresponsiveness after switching to radio on TEST1 and explicitly requests minimal CPU use while keeping the approved appearance. The old 20fps eCanvas path issued thousands of individual fillRect calls per second, each creating a native painter and invalidating a region. TEST2 replaces it with pre-rendered transparent 350x126 frames through ePixmap, one update per 100ms, no runtime geometry/colour computation, single-shot rearming after work, native-parent visibility checks, shared lazy 48-frame decode cache (8.1 MiB RGBA pixel budget). All approved columns/spacing/positions preserved. See `docs/RADIO-SPECTRUM-PERFORMANCE-2026-10-29.md`. TEST1 is unsuitable following this receiver report; TEST2 requires receiver confirmation. Production feeds remain 1.0.39.

# Candidate 1.0.40-test1 — spectrum and ecosystem runtime cleanup, 29 October 2026

Owner approved the 84-column, 3px / 1px, transparent 350x126 animated colour spectrum and requested replacing it in the skin, then auditing all three Warder receiver plugins for unnecessary logs and transient files. Implemented on `feature/radio-spectrum-refinement`. Production remains 1.0.39; no physical receiver confirmation or feed activation is claimed. See `docs/RUNTIME-CLEANUP-2026-10-29.md`, its source hashes, and `design/radio-spectrum/approval.json`. The shared engine is byte-identical to the PiconHub cleanup candidate recorded in `warderRadioCore/SOURCE.json`.

---

# Published production 1.0.39 — 29 October 2026

Latest stable release and built-in production updater are active. Source `f2ce83c7b20d1213979d8c044bacf51f90fe916d`; activation `58e3bd3a263b9df4c779dbef22290556a11815ad`. Build **40877231891** passed **362 tests** and verified **1,353 installed files**; independent radio guard **40877231870** passed. Both public delivery paths were independently downloaded and matched: **14,515,826 bytes**, SHA256 `7bec211d1ad8ce2864a01c19a63f719de983345258eecfece03669efb898f246`. Legacy 1.0.18 bridge, user settings and satellite automation remain unchanged. Full evidence: [RADIO-PRODUCTION-1.0.39.json](docs/RADIO-PRODUCTION-1.0.39.json). TEST13 receiver confirmation and exact promotion scope are retained below.

---

# Production promotion — 29 October 2026

Owner confirmed SuperMusic in **1.0.38-test13** functional on the receiver, then requested documenting all work and a normal version delivered through the built-in updater. **1.0.39** retains the accepted runtime and approved radio graphics, updating version labels/history only. The next patch number permits a normal package-manager upgrade from TEST13.

Source of the accepted candidate: `83d4c2132c4d8a538c34574b5491aa0942363164`; candidate build 40873174108 passed 259 tests and verified 1,353 payload files. SuperMusic accepted 7 of 12 selected songs in comparison 40873173998; this is not a catalogue coverage estimate. Production approval and receiver scope: `docs/PRODUCTION-APPROVAL.json`. Publication runs full settings/radio checks, validates the exact IPK and advances `update-production.json` only after public byte verification. Exact final production source/package/hash/run are recorded in `docs/PRODUCTION.json` and `docs/LIVE-UPDATE-STATE.json`. Preserve the legacy 1.0.18 bridge and the existing satellite automation.

Current production records above supersede dated statuses below; historical validation limits remain historical.

---

# Produkčné IPTV rádiá SK/CZ — 28. októbra 2026

FullHDGlass **1.0.36** a PiconHub **0.1.30** sú vydané a aktívne v aktualizačných kanáloch. Skin CI **40687770330** úspešné, zdroj `e672afb9cf46ab61e8ee154ecf618b22e235c861`. Verejné IPK má 14 271 200 bajtov, SHA256 `e2a7e43c6cb7fe129c12f7c3bb511bbbdfd2a075ac051ad708adaec29a7d811c`. Deväť spoločných modulov v oboch verejných IPK je identických.

Bouquet 321 položiek (88 SK, 233 CZ), audio skúška pre 286 URL; picony 213 položiek / 229 referencií × 9 variantov. 108 položiek bez vhodného overeného piconu. Spoločné dáta sú v PiconHub main/picons/IPTV-SK-CZ. Všetkých deväť živých variantov nainštalovaných do dočasných priečinkov cez skutočný PiconRunner; nesúvisiace picony zachované. Fyzický test týchto verzií na prijímači sa netvrdí. [Presné overenie](docs/IPTV-SK-CZ-1.0.36.json).

---

# Published infobar follow-up1.0.28

Stable Latest and production updater verified. CI40475278006 and radio guard40475278052 succeeded. IPK14198502 bytes SHA25649d41833ac81fd728d4db9f47eb8047b4d5f3bb990a079d12682b02bc5233413. g17PicRef2/3 share original/legacy radio paths with primary renderer and use native radio fallback before default; their timers/animations retained.13 renderer tests and22 layout checks passed before publication. Owner confirmed RDS in1.0.27, but1.0.28 OK-infobar receiver test still pending. Separate radio-source research is saved in PiconHub plugin/research/RADIO-SOURCES.md and RADIO-SOURCE-AUDIT.json. No PiconHub runtime source enabled by that research.

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

### 2026-10-28: weekly radio catalogue

Owner authorized weekly source merging in PiconHub and silent weekly receiver-side refresh in FullHDGlass. PiconHub main commit 310136ed124108b4b400f1f64a6fcc16b5ec0e0e; workflow 40730407663 passed. Own 88 SK / 233 CZ entries are untouched and first; 5,120 foreign entries follow. Source attribution is in repository documentation, not the bouquet UI. Satellite automation is unchanged. FullHDGlass 1.0.37 adds a native child worker, persistent weekly timestamp, six-hour failure backoff, SHA256 validation, atomic replacement with backup and GUI-thread bouquet reload without service navigation. Only an already installed Warder bouquet is managed. Receiver testing remains outstanding.

### 2026-10-28: radio lyrics candidate

Owner explicitly requested implementation of the approved blue/amber studio layout, retaining tall artwork height while narrowing its sides, centered album/lyrics group, picon and station/RDS/DAB fields left in the footer, animated spectrum above transport type at right. Lyrics must be automatic, plain text, no user button, no karaoke. Font sharpness through radio layers is a material receiver acceptance condition. Baseline production is 1.0.37 at 744075b582e26b36b5a1a25e6f00fd8450ac5123. Candidate is 1.0.38-test1 in feature/radio-lyrics-layout with feeds unchanged. See design/radio-lyrics/implementation.json and docs/CURRENT-RELEASE.md.

### Radio TEST2: physical background mismatch

Physical receiver report: OpenWebif looks correct while an old central cover frame remains visible on TV. Confirmed by decoding TEST1 source radio.mvi: it still contained the old framed studio image. Fixed source radio.mvi by MPEG2 encoding of the current clean 1920x1080 JPEG. Added SHA256-pair and decoded-image similarity checks to both the active package builder and full IPK verifier. Preserve native passive-radio background ownership; no config.misc.radiopic or RdsInfoDisplay startup override. Candidate 1.0.38-test2; physical HDMI confirmation pending.

Radio TEST2 also restores the original selected InfoPanel PNG in the radio conditional branch. TEST1 accidentally emitted only WarderTVOnly for full-frame panel pixmaps, producing text without a backing after OK. Restored WarderRadioOnly with alpha blending; keep the TV branch and native fields unchanged. All real full-frame templates are checked in tools/test-radio-background.py.
