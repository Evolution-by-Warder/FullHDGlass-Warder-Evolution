# FullHDGlass 1.0.62-test2 — OpenATV 8.1 / GLES / WQHD plugin preparation

This separate candidate extends 1.0.62-test1. Production remains 1.0.61 and its updater profiles remain unchanged. Test1 assets are immutable.

## Included changes

- setupGlass17-owned screens declare their 1920×1080 XML reference. Python-created fonts, points, sizes, list rows and MultiContent cells scale to the actual HD/FHD/WQHD/UHD desktop without patching global Enigma2 classes.
- Coverage includes configuration/download/picon/history/program-detail dialogs, weather, Netatmo, ECM, screen saver, user information and spinner selection. The header image fits the actual desktop. Native OLED/display-specific templates retain their reference.
- Spinner grid capacity uses scaled minimum cell/row dimensions and does not scale its actual native item width twice.
- Native vertical lists fit complete rows after layout and reopening, preserving allocated height when content row heights change. Horizontal/grid packing keeps its own rules.
- Four test1 native screen binding repairs remain included: PicturePlayer, PiP Dishpixmap, PositionerSetupLog and legacy Swap labels.
- Static checks now include imported/conditional resolution XML, relative imports, inheritance and finite loop-created fields. Dynamic generator calls and unresolved fields are explicitly reported; no blanket static coverage claim is made.

## Verification and limits

The original frozen controller/action fingerprint remains enforced through exact reviewed AST reversions in design/wqhd-compatibility/logic-edits.json. All 24 setup-style regressions pass. Nine new resolution-helper tests, actual OpenATV Screen.applySkin reference-scaling replay, expanded binding-audit semantics and the existing native regression suites gate the candidate.

The complete Python payload inventory is recorded in reports/gles-wqhd-inventory-20261102.json. Native interface checks use stable 8.0, 8.0-next and master. Generated XML and Python contracts cover 2560×1440; physical GLES/HDMI rendering on a receiver remains unverified. The main FullHDGlass skin keeps its approved FHD output declaration; this candidate prepares its plugins for other desktop resolutions and does not silently replace the primary skin with an untested WQHD variant.

No production updater manifest, approved radio/picon artwork or architecture-specific bitrate helper is changed. Next normal version is 1.0.63 after receiver acceptance.
