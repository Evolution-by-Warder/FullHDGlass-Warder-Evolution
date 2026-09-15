# FullHDGlass Warder Evolution — PROJECT CHECKPOINT

Updated: 2026-09-15
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
