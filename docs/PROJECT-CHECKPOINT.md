# FullHDGlass Warder Evolution — PROJECT CHECKPOINT

Updated: 2026-10-01
Purpose: durable recovery checkpoint so the project can be resumed exactly after loss of chat/context.

## Current stable baseline

- Project: FullHDGlass17 Warder Evolution.
- Visible/new branding: **FullHDGlass Warder Evolution** (without `17` in visible branding).
- Stable package baseline: **1.0.4**.
- Package: `enigma2-skin-fullhdglass17-warder-evolution_1.0.4_all.ipk`.
- SHA256 of stable 1.0.4 package: `9ceb1713fa237d39f13b4baf728852323086205528c5622df7def58b5812c0bd`.
- Published 1.0.4 baseline commit: `57fb8e5ae86bb46b0f91e2b614c2f6db649a6989`.
- Latest branding/update-text commit at checkpoint time: `665527299043fef079d75079d412c28cee8dd7e3`.

## LOCKED — approved graphics and structure

Existing approved skin graphics, visual layout, element dimensions, coordinates/positions, screen composition and established directory/runtime structure are **LOCKED**. ChatGPT, Work, automation or a future recovery session must NOT independently redesign, redraw, regenerate, resize, reposition, reorganize, rename, replace or otherwise "improve" them.

New work must adapt to the already approved design and structure — the approved design/structure must not be changed merely to accommodate new work. Any intentional change to approved graphics, layout, dimensions, coordinates or structural organization requires **Štefan's explicit approval first**. No inferred permission and no silent optimization.

## Binding compatibility rule — DO NOT RENAME

The following legacy/runtime identifiers containing `17` are compatibility identifiers and MUST remain unchanged unless a future migration is deliberately designed and tested:

- package identity `enigma2-skin-fullhdglass17`
- runtime path/name `hd_glass17`
- `setupGlass17`
- `g17_setup_pict`
- `extraScreens17`
- `/etc/enigma2/skin_user-hdg17.xml`

Visible branding may say **FullHDGlass Warder Evolution**, but runtime compatibility identifiers above are not branding and must not be cosmetically renamed.

## Authorship / branding policy

- Modify branding only for our new/Warder Evolution material where appropriate.
- Preserve legitimate original author credits; do not erase historical authorship.
- Do not globally replace every historical author name with Warder.
- Donate text/button is removed/disabled for now where it belongs to our current UI cleanup decision.
- Public repository must not expose historical original HDGlass FTP snapshot/archive/provenance, credentials, private inventories or GOLDEN metadata.

## Updater architecture — binding

- No GitHub Releases dependency.
- Updater assets are ordinary repository files served through raw GitHub HTTPS.
- Updater uses `eConsoleAppContainer`.
- Do **not** revert updater execution to `Screens.Console`.

## Installation/update expectations

Future package/update work must preserve the existing skin installation identity so an already installed FullHDGlass17 installation can be upgraded rather than creating an accidental parallel incompatible skin. Existing user settings/configuration must be preserved wherever technically compatible. Package metadata must remain suitable for Enigma2 package/appearance management.

## What has been completed

- Stable 1.0.4 package created and published.
- Updater baseline established.
- Visible project branding cleaned to FullHDGlass Warder Evolution while retaining compatibility identifiers containing `17`.
- Branding updates propagated through relevant public README/catalog/manifest/updater text in commits following 1.0.4.
- Public-repository cleanup policy established: do not publish private/original FTP archive material or credentials.
- Original authorship is to be respected; only new project material is Warder-branded.

## Current project state

The project is **ACTIVE / IN DEVELOPMENT**, not finished. Version 1.0.4 is the stable recovery baseline, not the final end of modernization.

## Next work / TODO

1. Continue modernization from the stable 1.0.4 baseline, not from older experimental states.
2. Review remaining visible UI strings/screens/assets for consistent **FullHDGlass Warder Evolution** branding while leaving compatibility identifiers untouched.
3. Verify Donate removal/disablement in all intended visible locations without damaging original author attribution.
4. Continue UI/skin modernization only in controlled batches; test each batch before publishing another package.
5. Before next release, verify upgrade-over-existing-install behavior and preservation of user settings/configuration.
6. Verify package visibility/behavior in Enigma2 package/appearance management on the target receiver/image.
7. Re-test updater end-to-end using the current `eConsoleAppContainer` + raw GitHub asset architecture.
8. Create a new package/version only after the above batch is validated; keep 1.0.4 as known-good rollback/recovery baseline.

## Recovery rule

If chat/context is lost: start by reading this checkpoint, inspect current `main`, compare changes after commit `665527299043fef079d75079d412c28cee8dd7e3`, and preserve all LOCKED graphics/structure, binding compatibility/authorship/updater rules above. Do not restart the project from the original HDGlass source, do not redesign approved graphics/layout without Štefan's explicit approval, and do not rename the legacy `17` runtime identifiers merely to match visible branding.


## Current TEST candidate — 2026-10-01

- Stable recovery baseline remains **1.0.4** and is not replaced by development work.
- Working branch: `warder-modernization-work`.
- Current receiver-test candidate identity: runtime **1.0.5-test1**, package version **9.50+warder1.0.5-test1**.
- Stable `update.json` remains pinned to 1.0.4; TEST packages are not published through the stable updater channel.
- TEST packaging is guarded by `tools/build-test-ipk.sh`, `tools/verify-test-ipk.sh`, `tools/test-package-lifecycle.sh` and `.github/workflows/build-test-ipk.yml`.
- The legacy 1.0.4 source-recovery workflow is now manual/read-only and uploads its recovered tree only as a temporary artifact. It must never overwrite the modernized `source/` tree.
- Static/build success is not receiver acceptance. Only physical validation on the target GigaBlue Quad 4K Pro / OpenATV 8.x may establish RECEIVER PASS.


## CURRENT TEST CHECKPOINT — 2026-10-01 — TEST19

This section supersedes older development-status/TODO text above where they conflict. Stable 1.0.4 remains the rollback baseline; current active development is TEST19.

- Working branch: `warder-modernization-work`. `main` is TABU: no writes, merges, rebases or force-pushes. No force-push/rebase anywhere.
- Exact FullHDGlass17 9.50-r12 is the functional authority for r1-r12 behavior. Preserve all r1-r12 fixes; do not invent replacement behavior where r12 already defines it.
- Primary receiver: GigaBlue Quad 4K Pro / OpenATV 8.x. Default picon path: `/usr/share/enigma2/picon/`.
- TEST18 weather-city flow is receiver-verified PASS: city selector works; confirming a city does not crash; selected city's weather data/icon/temperature refresh immediately in the skin without GUI restart. Keep this behavior locked unless explicitly changing it.
- TEST19 restores the r11/r12 PIG menu-navigation fix for all four variants: `with PIG`, `simply PIG`, `PIG2`, `PIG4`. Root cause of TEST18 regression was two `Listbox` widgets bound to `source="menu"` on each PIG screen. Authoritative r12 uses one navigable menu `Listbox` plus one display-only `Label` using `g17MenuCurrentText`.
- The TEST19 source change covers 32 PIG screen definitions: four PIG variants across `Menu`, `menu_mainmenu`, `menu_information`, `menu_setup`, `menu_scan`, `menu_system`, `menu_harddisk`, `menu_shutdown`.
- TEST19 PIG navigation is receiver-verified PASS on GigaBlue Quad 4K Pro for all four PIG variants, including menu/submenu movement.
- TEST19 source implementation commit: `6413f6e713ef421cdc044426ca07f8e67028b3fe`. Regression-gate correction commit: `c198111c1a298a95ca39cc84c1d361f7f5e9d2a9`.
- GitHub Actions build #78 / run `36920908109` completed successfully. CI publication advanced branch HEAD to `258b684615977345cbf9f26239b302e75be93499` before this checkpoint update.
- Published package: `packages/test/enigma2-skin-fullhdglass17-warder-evolution_1.0.5-test19_all.ipk`. SHA256: `82771315e88a63e058eb08557ef67194f022653f0be6288450a7b24402b67731`. `update-test.json` points to TEST19.
- Receiver installation was performed manually through Telnet because TEST18 PIG navigation prevented reaching the updater. Download succeeded (11,422,936 bytes), then `opkg --force-reinstall --force-overwrite install /tmp/test19.ipk` and `init 4 && init 3` were used.
- Important remaining issue: receiver `opkg` output during TEST19 installation displayed upgrade target as `enigma2-skin-fullhdglass17 (1.0.5)`, despite repository control/version files containing `1.0.5-test19`. Investigate and fix package version normalization/metadata next. Do not treat this as solved yet.
- Receiver-testing rule: never mark a receiver feature PASS without actual user receiver output/screenshot/confirmation. Shell testing instructions must be one short command at a time.

### Immediate next work

1. Investigate why `opkg` reports `1.0.5` rather than `1.0.5-test19`, while preserving the updater/version ordering behavior.
2. Continue systematic r1-r12 regression review from exact r12, without reopening already receiver-verified TEST18 weather or TEST19 PIG behavior unless evidence of regression appears.
3. Keep updater behavior: auto-check only after opening FullHDGlass17 settings (not receiver boot/skin startup), with the established delayed/modal-safe flow.

## TEST20 package-version correction — candidate, not receiver-verified yet

- TEST18 weather/city and TEST19 PIG receiver PASS checkpoints remain locked and unchanged.
- CI #78 artifact was independently extracted and verified by SHA256 `82771315e88a63e058eb08557ef67194f022653f0be6288450a7b24402b67731`; its embedded control really contains `Version: 1.0.5-test19`. Therefore the TEST19 builder/publication did not strip the suffix.
- Root cause is opkg version parsing/presentation: the final hyphen component is package revision. With `1.0.5-test19`, opkg parses base version `1.0.5` and revision `test19`; the target OpenATV install message exposed only the base part.
- TEST20 changes package metadata only: runtime/updater identity is `1.0.5-test20`, while IPK control metadata is `Version: 1.0.5-test20-1`. This leaves `1.0.5-test20` in opkg's base-version component and uses numeric package revision `1`.
- Build/verification gates now explicitly enforce the separation between runtime/updater version and package metadata version. Package filename remains keyed to runtime identity: `..._1.0.5-test20_all.ipk`.
- TEST20 must not be marked receiver PASS until the physical GigaBlue confirms the opkg presentation and normal operation.

### TEST20 CI publication status

- Corrected workflow commit: `815e097ef80b8a14ead21af806af649bbdb8d906`.
- GitHub Actions build #80 / run `36923438508`: **SUCCESS**.
- CI publication commit: `7b69e392c3c96ca811d46d300f8c939e273d5b73`.
- Published package: `packages/test/enigma2-skin-fullhdglass17-warder-evolution_1.0.5-test20_all.ipk`.
- SHA256: `32ed703e06955c7e2675b5997ea10fc510e7269aeb71b5d327fe17b5e1b1869c`.
- Extracted final IPK verified: control `Version: 1.0.5-test20-1`; payload runtime version `1.0.5-test20`; `update-test.json` version `1.0.5-test20`.
- CI/static/package validation is PASS. Receiver validation of the corrected opkg display is still pending and must not be marked PASS until physically confirmed.


## TEST20 receiver acceptance — 2026-10-01

Physical receiver validation on GigaBlue Quad 4K Pro / OpenATV completed successfully.

- Downloaded published TEST20 package successfully: 11,422,940 bytes.
- Receiver install output explicitly reported: `Upgrading enigma2-skin-fullhdglass17 (1.0.5-test19) to enigma2-skin-fullhdglass17 (1.0.5-test20) on root`.
- Upgrade preserved existing settings; the differing conffile was safely placed at `/etc/enigma2/skin_user-hdg17.xml-opkg` rather than overwriting the user's active file.
- GUI restarted with `init 4 && init 3` and returned normally.
- `opkg status enigma2-skin-fullhdglass17` reports `Version: 1.0.5-test20-1` and `Status: install ok installed`.
- **TEST20 package-version correction: RECEIVER PASS.** The earlier TEST19 display defect is closed.
- TEST18 weather/city PASS and TEST19 all-four-PIG-variants PASS remain locked; TEST20 made packaging/version-gate changes only.


## TEST21 — OpenATV MediaScanner MessageBoxModal — RECEIVER / VISUAL PASS (2026-10-01)
- Physical receiver: GigaBlue Quad 4K Pro / OpenATV 8.x.
- TEST21 installed over TEST20; existing FullHDGlass17 settings preserved.
- CI #83 completed successfully; published TEST21 SHA256: `3acfc75d73ac70db5cb136c7b03f1dabe1aea8b449fb12040889d09aa5e7b46b`.
- Verified real workflow: Software management -> Install local extensions -> media selection -> MediaScanner modal -> OpkgInstaller list.
- `MessageBoxModal` now uses FullHDGlass17 visual language instead of generic image fallback. Question icon, message text and selectable list render correctly.
- Existing `OpkgInstaller` screen remained unchanged and visually correct.
- User explicitly approved the receiver result as OK. TEST21 is RECEIVER / VISUAL PASS.
- Locked prior passes remain valid: TEST18 weather/city, TEST19 PIG variants, TEST20 package-version metadata.


## Night checkpoint — 2026-10-02 — TEST22 through TEST28

This is the authoritative continuation point. Do not restart completed analysis.

### Locked receiver passes
- TEST22: OpenATV compatibility screens QuickEPG, GraphicalEPG, GraphicalEPGPIG, GraphicalInfoBarEPG and RassInteractive — receiver install/runtime PASS.
- TEST23: native FullHD graphical EPG fullscreen worked; PIG was gray.
- TEST24: GraphicalEPGPIG LIVE PIG fixed; fullscreen and 15 EPG rows work — RECEIVER PASS.
- TEST25: installed; introduced automatic GUI restart after successful updater install; initial 3s MessageBox/eTimer race was subsequently hardened.
- TEST26: updater automatic GUI restart physically confirmed; failed update must not auto-restart. RECEIVER PASS. EPG LIVE PIG, 15 rows, event detail, current green/future dark and selection also confirmed.
- TEST27: RECEIVER PASS. Removed duplicate top-left bouquet title such as `SK - CZ`; LIVE PIG, 15 rows, narrow picon-only rail, event grid, event detail and updater behavior remained correct.
- TEST27 runtime `1.0.5-test27`; SHA256 `1bb41f3e8b648be1f493d29127c0de289f5afc288cc6e4f1db01810ae3b9a373`; publication commit `3b6e2f14d54a3569407d53e2338d1828f3353560`.

### GraphicalEPGPIG behavior to preserve
- FullHDGlass startup sets OpenATV GraphicalEPG service-title mode to `picon` and picon width 60 via runtime `.value` only; no `save()`.
- Bouquet/title suppression is scoped to FullHDGlass17 GraphicalEPGPIG through the patched `EPGSelection.setTitle()`.
- Do not restore station names beside picons or the top-left bouquet title.
- Target remains FullHDGlass design, LIVE PIG top-left, selected-event detail top-right, 15 rows, narrow picon-only rail, grid immediately after picons, current event green, future dark, clear selection and current-time line.

### TEST28 — CI PASS / published, but receiver FAIL for bottom action row
Intended footer:
- RED = selected-event description via `infoKeyPressed()`.
- GREEN = timer (`graph_green = "timer"`).
- YELLOW = prime time (`graph_yellow = "gotoprimetime"`).
- BLUE = EPG Search (`graph_blue = "epgsearch"`).
- Overrides are scoped to FullHDGlass17 GraphicalEPGPIG/runtime and non-persistent.
- Skin XML contains `key_red`, `key_green`, `key_yellow`, `key_blue` at y=930 and intentionally removes old `primetime`, `change_bouquet`, `jump`, `page` widgets from GraphicalEPGPIG.

TEST28 build history:
- `11293609d63f31b6ea00efe291c1c8edb44152c0` initial build; regression failure after broad skin replacement.
- `e025179e93ddd9ded7f9d56c8c074670a5c3dd20` repaired screen scope.
- `a944dc80defac7aeaae76205c156b5ad16a29978` partial regression alignment.
- `e9e85bfea3ba2ceee81c4c9696e33affd06c2a63` scoped legacy footer gate to non-PIG GraphicalEPG.
- `eef74937702ea12a7b4d4e15cde50e5c36bb2af8` restored all four key widgets; CI run `36944491321` SUCCESS.
- publication commit `afc33192dc343a9c8f6558a652fa42a7182e090f`.
- runtime `1.0.5-test28`; package SHA256 `213d1e74168e0b057c201e2178eba4124b8ce2e3cbf7a40b53180fbbdbe194e1`.

Updater note:
- TEST27 briefly reported itself current immediately after TEST28 publication although repository manifest already had TEST28. A later check succeeded without code changes. Treat as transient raw/manifest caching unless it recurs.

Physical TEST28 result:
- GraphicalEPGPIG still renders correctly (LIVE PIG, event detail, 15 rows, picon-only grid).
- The entire intended bottom colored action row is absent on the physical GigaBlue. User supplied a current receiver screenshot on 2026-10-02 proving no red/green/yellow/blue labels render.
- Therefore **TEST28 bottom action row = RECEIVER FAIL**. TEST28 is NOT receiver PASS.
- XML presence alone is insufficient: OpenATV is not populating/rendering these `key_*` widgets in this screen as assumed.

### Exact next task
Continue from this branch HEAD and make the next TEST build (normally TEST29) fixing the physically missing bottom action row. Investigate the real OpenATV GraphicalEPGPIG source/action-label lifecycle rather than merely repositioning the XML widgets. Receiver acceptance requires all four visible and functional: red event description, green timer, yellow prime time, blue EPG Search.

Preserve every locked TEST24/26/27 behavior. Run CI and publish through the established test workflow, then validate on the physical GigaBlue Quad 4K Pro. Never claim receiver PASS from XML/static tests.

After EPG footer acceptance, next major feature: General Radio Artwork for DVB radio + DAB+ + IPTV/internet radio where metadata exists, while preserving the already-working DAB+ slideshow.


## Shared Warder asset backend — architecture locked 2026-10-02

This is a project rule, not a FullHDGlass17-only implementation detail.

- Trezor contains the authoritative 100% preservation copy of the old FullHDGlass17 FTP. **Do not modify or reorganize the Trezor originals.**
- The old FTP directory layout is historical source material only. It MUST NOT dictate the new public Git layout.
- Runtime assets are to be migrated from Trezor to a logical, consistent, reusable Warder Git asset hierarchy intended for multiple consumers, including FullHDGlass17, PiconHub and future Warder plugins.
- Do not duplicate the same canonical asset merely because several plugins consume it. Consumers must resolve shared assets through stable manifest IDs/metadata.
- The common hierarchy must separate asset class and variants, e.g. service picons, provider picons, satellite picons, CAM picons, terrestrial DVB-T/T2, skin-specific UI, weather and shared helpers. Picon variants should consistently distinguish transparent/black/white and dimensions where applicable.
- The manifest/catalog is the stable runtime contract. Each downloadable item should expose a stable ID plus type/category, variant/dimensions where relevant, version/revision, SHA256, size, canonical URL/parts and compatibility metadata when needed.
- FullHDGlass17 runtime must ultimately have no dependency on the obsolete FTP. All legacy FTP/server download paths are to be audited and redirected to the Warder HTTPS/Git manifest/backend.
- Migration phase 1 is preservation: map 100% of old FTP functionality/data from the Trezor source to the new backend and verify old-source -> canonical-asset -> manifest -> plugin coverage 1:1.
- Migration phase 2 is modernization: update stale content separately. Current DVB-T/T2 picons are the expected area most likely to need fresh data; do not mix this content update with preservation migration.
- Existing receiver/user picons and settings must not be deleted or overwritten arbitrarily by this migration.
- Existing assets currently under `assets/warder/downloads/` and `downloads.json` are an intermediate implementation. Reorganize them only through a controlled migration with manifest compatibility so existing TEST/update behavior is not broken.
- Target conceptual layout:
  - `assets/picons/services/{transparent,black,white}/`
  - `assets/picons/providers/{transparent,black,white}/`
  - `assets/picons/satellites/{transparent,black,white}/`
  - `assets/picons/cam/{transparent,black,white}/`
  - `assets/picons/terrestrial/{dvb-t,dvb-t2}/`
  - `assets/skin/fullhdglass17/...`
  - `assets/shared/{weather,helpers,...}/`
- PiconHub should consume the same canonical picon assets rather than maintaining a FullHDGlass17-specific duplicate set.

### Work order
1. Finish and receiver-validate TEST29 GraphicalEPGPIG footer.
2. Inventory every legacy FullHDGlass17 download/FTP endpoint and every preserved Trezor asset.
3. Produce a 1:1 migration map and identify genuinely missing/current-content gaps.
4. Build the shared Warder asset hierarchy + manifest compatibility layer.
5. Redirect FullHDGlass17 downloads to the shared backend and regression-test all download menu functions.
6. Update DVB-T/T2 content as a separate modernization pass.
7. Continue with General Radio Artwork and remaining final compatibility/release audit.


## RADIO authoritative checkpoint — 2026-10-04 — TEST191

This section supersedes older Radio TODO/status text above where it conflicts.

- Working branch remains `warder-modernization-work`; `main` remains TABU.
- Current Radio receiver-test checkpoint is **TEST191**.
- TEST171 TOP/BOTTOM composition: PHYSICAL PASS / locked.
- TEST178 cover geometry `606,145 / 704x640`: PHYSICAL PASS / locked.
- TEST179 matcher: PHYSICAL PASS to tested scope; TEST180 controlled catalogue-credit relaxation retained. HUNTR/X itself was not physically exercised.
- Approved no-cover fallback is locked at `/usr/share/enigma2/hd_glass17/warder-radio-no-cover.png`, repository blob `a5c18ecc9572472cd9867aacac6c4e70f4f8a16e`.
- TEST183 classic DVB Radio without RDS: PHYSICAL PASS; service types 0x02 and 0x0A recognized.
- TEST187 moving equalizer: PHYSICAL PASS; TEST188 speed is 140 ms and visuals/geometry are locked.
- TEST189 and TEST190 SLS approaches are documented failures and must not be restored.
- TEST191 uses OpenATV 8 native DAB MOT slideshow metadata via `iServiceInformation.sTagPreviewImage` for `idServiceDAB`.
- TEST191 DAB SLS: **PHYSICAL PASS** on GigaBlue Quad 4K Pro / OpenATV 8, explicitly observed on Schwarzwaldradio, ENERGY and SCHLAGERPARADIES. Picon, station, DAB technical line, provider and moving equalizer remained intact.
- Published TEST191 package: `packages/test/enigma2-skin-fullhdglass17-warder-evolution_1.0.5-test191_all.ipk`.
- TEST191 SHA256: `a99e309776615c2cc8ded5467d552ba3669fdc88e97860f39a4f89acfc43109e`.
- GitHub Actions run `37220612169`: SUCCESS; publication commit `2f9b396a0fa8905e54e833d3861cb67606ed825c`.
- `update-test.json`, package control metadata and runtime version are aligned at TEST191 (`1.0.5-test191`; control `1.0.5-test191-1`).
- Detailed Radio lock/diagnostic rules live in `docs/RADIO-WORK-CHECKPOINT.md`.

Remaining Radio closure requirement: perform and explicitly approve one combined **WHOLE RADIO PASS** regression (TV -> Radio -> TV, normal RDS cover, no-RDS fallback, DAB SLS, equalizer, WebIF). Do not declare the entire Radio project final before that combined receiver confirmation.


## RADIO CLOSED — WHOLE RADIO PHYSICAL PASS — 2026-10-04

User explicitly approved the final TEST191 combined receiver regression with **“beriem”**.

Observed physical sequence/evidence:
- DAB SLS: SCHLAGERPARADIES transmitted slideshow rendered in the locked center frame; DAB technical metadata, picon, provider and moving equalizer remained intact.
- Normal RDS artwork: BAYERN 3 / Fast Boy — Music Sounds rendered the matched real cover and correct Radio lower information.
- No-cover case: 1LIVE rendered the approved Warder no-cover fallback with no fabricated song/artwork.
- Return to TV: TV JOJ HD returned to the normal TV InfoPanel with no Radio TOP/background/artwork/equalizer leakage.

**WHOLE RADIO = PHYSICAL PASS / LOCKED on TEST191.** The Radio feature baseline is now closed/accepted for the physically tested receiver path. Preserve all locks documented in `docs/RADIO-WORK-CHECKPOINT.md`; reopen only on new physical regression evidence or an explicitly approved enhancement.

TEST191 package remains `packages/test/enigma2-skin-fullhdglass17-warder-evolution_1.0.5-test191_all.ipk`, SHA256 `a99e309776615c2cc8ded5467d552ba3669fdc88e97860f39a4f89acfc43109e`, workflow run `37220612169` SUCCESS.


## Post-Radio regression / download-backend audit — 2026-10-04

Started immediately after TEST191 WHOLE RADIO PHYSICAL PASS. No Radio code changed.

### Git/runtime audit findings
- TEST191 publication, manifest and runtime/control versions remain aligned.
- Existing non-selected Warder asset downloads already use HTTPS manifest metadata, SHA256 verification, redirect-prefix checks and safe ZIP extraction.
- **Legacy fallback retained:** satellite-selected `downloadMenu.downMulti()` still contains the isolated `https://picon.cz/download/<position>/` route, while the new Warder transparent/black/white backend is persistently published and enabled on the working branch. Physical receiver validation is still required before retiring the fallback.
- This is the active exception to the project rule that FullHDGlass17 must ultimately have no obsolete/external picon download dependency. Do not silently remove it until the canonical Warder replacement dataset exists.
- Current Warder catalog explicitly marks these families unavailable: `picon_400x240`, `picon_220x132`, `picon-black`, `picon_50x30-black`, `picon-white`, `picon_50x30-white`, `piconOled`, `ZZPicon-v`.
- Available Warder families already include provider/satellite/CAM black+white, provider/satellite 220x132, help/UI/menu assets, weather assets, large ChannelSelection graphics and architecture-specific 7zip helpers.
- `assets/warder/downloads.json` is the current runtime download contract; `assets/catalog.json` records available/unavailable families. This remains an intermediate backend pending the shared canonical Warder asset hierarchy migration.

### Next concrete work
1. Preserve TEST191 Radio unchanged.
2. Preserve the completed Warder selector/source/collision inventory and deterministic transparent/black/white package contract.
3. Receiver-test the working-branch Warder manifest/runtime path, including selective/FULL behaviour and retry handling.
4. Retire or further isolate `downMulti()` picon.cz fallback only after physical receiver acceptance; unresolved legacy output families remain separate work.
5. Treat DVB-T/T2 content refresh as a separate modernization pass, not part of preservation migration.


## Warder picon assimilation — locked UX/work order — 2026-10-05

Architecture decision: FullHDGlass17 is the single user-facing Warder ecosystem surface. Do not launch or require a separate Chocholousek/PiconHub plugin. Preserve useful proven behaviour by assimilating it into FullHDGlass-owned GUI/runtime and Warder/PiconHub data.

### Locked GUI behaviour
- Keep one FullHDGlass Download Menu. Picon configuration is represented by clickable rows inside that screen.
- Configuration values are NOT changed with left/right arrows. Pressing OK on a row opens a small chooser/popup; confirming returns to the same Download Menu.
- Satellite/position selection uses a multi-select popup. Other scalar choices use a small single-choice popup.
- Picon rows, in user-flow order: positions/groups; resolution; colour/style; destination; update method.
- Default update method is receiver-driven synchronization with TV lists.
- Update-method chooser must expose user-selectable selective/synchronised and FULL semantics after the original Chocholousek meanings have been verified; do not invent semantics merely from the labels.
- Preserve the FullHDGlass visual selection language: inactive/unselected item = red X; an active/prepared selection/action = green arrow.
- The green arrow means the item participates in the prepared action, not merely that its value differs from a default.
- Preserve the existing lower-menu multi-selection workflow for ordinary FullHDGlass assets.
- Preserve blue Start Download visibility semantics: hidden when there is no executable action; visible as soon as at least ONE executable action exists. The user never has to select/configure every row.
- One press of Start Download executes the prepared picon operation together with any ordinary selected FullHDGlass assets.

### Smart synchronization contract
- Primary identity is the exact Enigma2 service reference, never fuzzy channel/provider names.
- Default selective mode reads the receiver's real Enigma2 TV bouquets/services and requests only picons needed by those services.
- Selected orbital positions/groups may filter the receiver-derived set; selecting 23.5E must not imply downloading every 23.5E provider.
- Provider/group names in PiconHub are routing/storage metadata, not the primary service identity.
- PiconHub runtime structure is picons/<position>/<provider>/{transparent,white,black}/<service-reference>.png.
- Same-service duplicates with identical payload are safe deterministic dedupe; conflicting different payloads must not be silently guessed.
- Manual/FULL operation remains a user-selectable alternative/fallback.
- Keep legacy picon.cz/downMulti only as a fallback until the already-enabled working-branch Warder path is receiver-tested; do not remove the fallback prematurely.

### Implementation work order
1. Keep TEST191 Radio fully locked and untouched; main remains TABU.
2. Build/test pure FullHDGlass-native receiver service parser/planner in warderPiconSync.py.
3. Verify exact historical Chocholousek selective/FULL behaviour and provenance/licensing before adapting concepts/code.
4. Build Warder/PiconHub service-reference index suitable for efficient receiver requests, including position/group/style and conflict metadata.
5. Add small OK-driven chooser screens and position multi-select while preserving the existing FullHDGlass look.
6. Add the five picon configuration rows and green-arrow prepared-state rendering without disturbing ordinary asset rows.
7. Extend existing toDown/reactivate/startDown execution planning so one prepared picon action is sufficient to expose the blue Start Download button and can run in the same batch as ordinary assets.
8. Implement verified HTTPS Warder fetch/install with atomic writes, destination safety, exact-match validation and useful missing/conflict reporting.
9. Add static/unit fixtures for bouquets, service-reference normalization, namespace/position mapping, filtering, dedupe/conflicts and action-state semantics.
10. Build a TEST candidate only at a receiver-testable milestone; CI/build PASS is not PHYSICAL PASS.
11. After physical receiver validation, retire the obsolete fixed all-satellite runtime path; retain historical evidence/fallback only as appropriate.

Current first implementation commit: 0f9dda187eb134b94ad9da75d9ce96feac269dbd (warderPiconSync.py).
## WARDER CHANNEL-PICON MIGRATION CHECKPOINT — 2026-10-05

This section supersedes older picon-migration TODO/status text where it conflicts.

- Production data backend is persistently published on `main` at commit `c78047bd5c0bdfdd522cec69673fa95ac2376da6`; production runtime/source was not copied there.
- Work-branch Warder runtime points at the verified production manifest. This remains development state until physical receiver acceptance and a separately approved production runtime cut-over.
- Preserved Chocholousek/Trezor legacy numeric-ID migration is **370/399 mapped** against pinned Trezor commit `9cdda4ab414e7d50a97ca9285db8ebbb75fba615`.
- The remaining **29/399** IDs are explicitly unresolved and fail closed. No nearby orbital/provider alias may be guessed and no retired-host fallback is allowed.
- `downMulti()` retains the established GUI, destination and 7-Zip installation semantics but resolves mapped legacy IDs through packaged `legacyPiconArchives.json`.
- The resolver validates schema, exact Trezor commit, 370/29 counts and no-guess/no-fallback policy, then caches the validated archive map for the screen lifetime.
- CI pins the exact unresolved ID set and exact filename-to-URL relation. The full channel-picon workflow run `37299973444` is SUCCESS, including deterministic materialization, publication-shaped payload, split candidate, runtime migration and two-phase cut-over gates.
- `main` remained exactly `c78047bd5c0bdfdd522cec69673fa95ac2376da6` after that validation; the one-time publication gate is closed.
- OpenATV `PackageAction` blank-list skin fix is present on the work branch and guarded by the full r12 regression suite, but has not yet been receiver-validated. Do not claim physical PASS before the later TEST-IPK checkpoint.
- No public Release. Radio TEST191 remains locked and outside this work.


## NIGHT CHECKPOINT — 2026-10-05 — TEST196

This section is the authoritative continuation point for the current Warder picon-download UI/runtime work. It supersedes older TEST192–TEST195 status where they conflict.

### TEST196 build checkpoint
- Working branch: `warder-modernization-work`; `main` remains TABU.
- Runtime version: `1.0.5-test196`.
- Final source commit: `f1dd3d42558f3001fb63285642b36eff2be182d4`.
- TEST package publication commit: `91ccf2400e2c02b67c7cfff43e1489ba58486b93`.
- GitHub Actions run: `37356322990` — SUCCESS. Job `build-test-ipk` and checkout/static preflight/build/package inspection/test publication/artifact upload all completed successfully.
- Package: `packages/test/enigma2-skin-fullhdglass17-warder-evolution_1.0.5-test196_all.ipk`.
- SHA256: `9a9f1e35c3bf0186a6aa82aceb9674d63c2f7aac09da65fd46333873a5fe43a4`.
- Status: **BUILD PASS ONLY**. TEST196 has NOT yet received REAL RECEIVER PASS.

### Locked receiver evidence inherited from TEST193–TEST195
- TEST193 restored setupGlass17 import/registration on the physical GigaBlue Quad 4K Pro / OpenATV 8.
- Empty satellite-position selection is receiver-verified: it does not mean ALL.
- One-position and two-position selection are receiver-verified.
- The old false `Missing upstream: 1135; Celkom: 198` regression is receiver-verified fixed: with 16.0E + 23.5E / 220x132 / Transparent / TV-list sync, 198 picons were updated while 1135 represented selected services rather than missing upstream picons.
- Preserve the callback safety fix for `warderPositionAnswer()`; never reintroduce the missing-`answer` TypeError.

### TEST196 intended picon workflow
- Localized main rows: satellite positions, picon resolution, picon colour, picon location and update method.
- Resolution choices include 50x30, 220x132, 400x240 and the verified large 710x682 ChannelSelection package.
- Location presets are independent of resolution and include `/usr/share/enigma2/picon`, common HDD/USB/SD/MMC paths, `/picon`, plus a custom directory browser.
- Four update modes are implemented: TV-list synchronization, TV+RADIO synchronization, replace-all for the selected context, and incremental copy.
- “All” remains constrained by the user-selected satellite-position/context and must never silently mean all satellites globally.
- Successful completed work resets transient task selections to the safe/default state; failure/cancel must preserve the retry state. UI text, status icons and internal state must remain consistent.

### Auxiliary picon variant rule — corrected from earlier assumption
Do NOT force Transparent/Black/White symmetry. The actual current `downloads.json` catalog is authoritative:
- Provider: Transparent + Black + White.
- Satellite: Transparent + Black + White.
- CAM: Black + White only.
- Weather: Black + White only.
No missing transparent CAM/Weather package may be invented merely for UI symmetry. Auxiliary selectors show background variant only, not a channel-picon resolution suffix.

### OLED receiver finding — pending diagnosis
On TEST195 physical receiver testing, selecting **OLED picon** produced the localized error that the 7zip tool is missing and can be downloaded from Download Menu. This is a real receiver finding and remains pending until diagnosed. Do not hide the error blindly: verify the OLED archive format, extractor path, 7z/7za/7zr detection and the existing FullHDGlass 7zip install mechanism. If extractor is truly absent, fail safely and direct the user to the real installer; if present, fix detection. OLED graphics/semantics are otherwise out of scope.

### TEST196 visual/UI requirements already implemented for receiver validation
- Five Warder-row icons were updated; they must be judged on the physical receiver against the established FullHDGlass visual language.
- Satellite-position icon should have the same optical footprint as neighboring icons.
- Colour icon communicates black/white choice with the approved diagonal split direction.
- Do not redesign unrelated FullHDGlass graphics.

### Immediate next work
1. Install TEST196 through the established TEST updater on the physical GigaBlue Quad 4K Pro / OpenATV 8.
2. Confirm FullHDGlass17/setupGlass17 still opens and established appearance/settings are preserved.
3. Receiver-test the new resolution, colour, location/custom-browser and four update-method selectors, including Cancel/Exit/reopen safety.
4. Verify missing external mounts are not created on the system disk.
5. Verify selected satellite positions constrain all four update modes.
6. Verify Provider/Satellite expose three real variants and CAM/Weather only Black+White.
7. Verify success reset, failure preservation, cancel preservation and repeated attempts.
8. Verify downloaded picons physically exist/use the selected destination and render where applicable.
9. Re-test OLED/7zip behavior and diagnose before changing it.
10. Do not declare TEST196 REAL RECEIVER PASS until the physical receiver evidence above is complete.

### Separate known issue, not closed
`/etc/enigma2/g17.txt` was previously observed contaminated with repeated `WarderProgramInfo metadata: could not convert string to float: '8.0/10'\n`. Keep this as a separate bug; do not lose it or conflate it with TEST196 picon work.

Radio TEST191 WHOLE RADIO PHYSICAL PASS remains locked and must not be modified by this work.
