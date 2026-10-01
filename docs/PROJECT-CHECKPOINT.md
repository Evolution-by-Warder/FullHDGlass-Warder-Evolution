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
