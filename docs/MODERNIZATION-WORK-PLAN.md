# FullHDGlass Warder Evolution — Modernization Work Plan

Status: ACTIVE
Primary target: OpenATV 8.x / GigaBlue Quad 4K Pro / 1920x1080
Working branch: `warder-modernization-work`

## Project boundary

This document applies to **FullHDGlass-Warder-Evolution**.

The legacy FullHDGlass17 maintained by Shamann is a separate maintenance-only line. It receives only compatibility/functionality repairs. New development, modernization and new functionality belong here.

## Mandatory audit — every screen

Every skin-defined screen must be inventoried and reviewed. Do not stop after representative screenshots.

Track each screen as:
- PASS
- FIXED
- NEEDS TEST
- NOT APPLICABLE

For every screen check:
- FHD geometry and use of available 1920x1080 space
- obsolete compact layouts
- widget position and size
- overlapping labels/values/controls
- clipping and truncation
- row height and spacing
- long/localized strings
- list/config-list and value-column width
- scrollbars
- action/key labels
- progress/status areas
- PIG/video areas
- zPosition, transparency and layering
- current OpenATV/Enigma2 source/widget/renderer compatibility
- navigation, OK and action behavior

Known visual examples requiring review include GUI/Skin setup, OpenATV Information and Receiver Information. MetrixHD screenshots are a functional/geometry reference only; **do not copy its visual design**.

## DAB+ / Radio

Implement/review native current OpenATV DAB+ station artwork/slide handling for Warder Evolution. Preserve normal TV/radio behavior and use current Enigma2/OpenATV mechanisms rather than a legacy hack. See Issue #2.

## Lessons that must be carried forward from legacy maintenance

### Menu APIs
Review Menu, menu_mainmenu, menu_information, menu_setup, menu_scan, menu_system, menu_harddisk and menu_shutdown. Verify every source against current Enigma2. Do not inherit invalid legacy references such as `source="title"`. No SkinError is acceptable.

### Package lifecycle
Audit `postinst`, `postrm` and upgrade/remove behavior. `postrm upgrade` must not delete or restore files belonging to the newly installed version. Defaults are installed only when user configuration does not already exist.

Test separately:
- clean install
- upgrade
- force reinstall
- uninstall

### User-data preservation
Normal upgrades must preserve compatible user settings, city/weather/provider configuration and user-managed files. Configuration schema changes require explicit migration handling.

### Picons and filesystem
Avoid destructive shell operations. Preserve existing picon directories, user files and unrelated symlinks. Clearly separate project-managed content from user-managed content. Never remove a non-empty user directory such as piconWeather merely as cleanup.

### Download/extraction safety
For ZIP/7z or other downloaded archives:
- prevent path traversal
- reject/safely handle symlink entries
- validate extraction result
- never report partial/corrupt extraction as success
- clean temporary files safely
- prefer safe APIs over shell command construction

### Python 3
Project-wide syntax/static checks are mandatory. Eliminate SyntaxWarning-producing regex strings and review obsolete Python 2 compatibility constructs, imports, converters and renderers against the current Enigma2 Python environment.

### Spinner
Do not inherit the old FullHDGlass17 wait*.png / skin_default spinner-symlink replacement mechanism. Any future Warder Evolution spinner must be deliberately designed and non-destructive.

## Validation gate

Before a receiver test candidate:
- all active Python sources compile cleanly
- all skin XML parses
- no missing directly referenced skin image
- internal imports/targets checked where practical
- package shell scripts syntax checked
- package identity/version/maintainer validated
- payload/archive integrity validated

Static/build PASS never replaces receiver testing.

## Receiver acceptance

On GigaBlue Quad 4K Pro / OpenATV 8.x verify as applicable:
- clean install
- upgrade from previous release
- configuration preservation
- expected GUI restart/restoration sequence
- all menu families without SkinError/crash
- city/weather/provider state
- picon content and symlinks
- real archive download/extraction when changed
- Enigma2 log for regressions

## Permanent feedback rule

Every useful defect, compatibility weakness or obsolete mechanism discovered while maintaining legacy FullHDGlass17 must be added to this Warder Evolution review/test plan so known technical debt is not inherited.

## Release discipline

Do not call a development build a release merely because static/build checks pass. Real receiver testing and explicit approval are required before promoting a new release checkpoint.


## Baseline reconciliation — 2026-10-01

Repository inspection confirms that the existing Warder Evolution implementation must be continued rather than rebuilt.

- Stable recovery baseline: **1.0.4**.
- Stable package: `packages/enigma2-skin-fullhdglass17-warder-evolution_1.0.4_all.ipk`.
- Published 1.0.4 commit: `57fb8e5ae86bb46b0f91e2b614c2f6db649a6989`.
- Current main contains 15 commits after that publication; they are documentation/branding/runtime-URL/checkpoint updates and must be preserved.
- Current repository checkpoint explicitly requires continuation from 1.0.4 and forbids restarting from original HDGlass source.
- Compatibility identifiers containing `17` remain binding and must not be renamed casually.
- Current updater architecture (raw GitHub assets + eConsoleAppContainer) is preserved unless a deliberate replacement is designed and approved.

### Conflict resolved for modernization work

The old checkpoint locks approved graphics/layout/coordinates. The new project requirement is to repair screens whose legacy geometry is no longer suitable for current OpenATV 8.x. Therefore:

- existing approved visual identity and graphics remain the design baseline;
- geometry is **not** to be changed arbitrarily;
- geometry/layout changes are permitted where the exhaustive screen audit demonstrates overlap, clipping, unreadable density, obsolete screen dimensions, or incompatibility with current OpenATV;
- such changes must preserve Warder Evolution visual identity and be receiver-tested before release.

### Missing work versus the 1.0.4 baseline

The following are not evidenced as completed by the 1.0.4 checkpoint and therefore remain active work:

1. exhaustive screen inventory with PASS/FIXED/NEEDS TEST/NOT APPLICABLE status;
2. FHD modernization of obsolete/crowded system and information screens;
3. DAB+ station artwork/slide support review and implementation;
4. carry-forward of post-r12 legacy findings: current Menu source compatibility, safe postinst/postrm lifecycle, non-destructive defaults/user-data handling, picon/symlink preservation, safe archive extraction, Python 3 warning cleanup, and spinner legacy audit;
5. complete static/build validation gate for the current source tree;
6. real GigaBlue Quad 4K Pro / OpenATV 8.x acceptance testing before the next stable release.

Do not publish a new stable version until these work items have been reconciled and the relevant receiver tests pass.


## Resolution and asset modernization rule

The current production and receiver-validation target remains **1920x1080 Full HD**, but new work must avoid creating an unnecessary FHD-only dead end.

- Preserve the established FullHDGlass/Warder Evolution visual identity; do not redesign graphics merely for novelty.
- Layout geometry is maintainable code: screen size, widget coordinates, font size, row height, spacing, list widths and other geometry may be changed whenever required for readability, current OpenATV content, accessibility, or compatibility.
- Existing raster assets may be repaired, rescaled, regenerated at a technically appropriate resolution, or converted to a more suitable format when necessary for clean rendering or future resolution profiles. Preserve their visual character unless an intentional redesign is separately approved.
- Prefer source/master assets with enough quality to derive multiple output resolutions instead of repeatedly upscaling already-small runtime files.
- Keep resolution-dependent geometry and assets separable wherever practical so a future **2560x1440 (WQHD)** profile can be introduced without rewriting skin logic or changing runtime compatibility identifiers.
- Do not claim WQHD runtime support until it is implemented and tested on a suitable Enigma2/OpenATV target. The requirement now is architectural readiness.
- When touching a screen for another fix, also check whether its geometry, fonts and assets create avoidable obstacles to a future higher-resolution profile.

## Integration rule

All new Warder Evolution functionality and all applicable fixes discovered during legacy FullHDGlass maintenance are to be integrated into this working line in controlled batches. Do not blindly copy a legacy patch: reconcile it with the Warder Evolution source, current OpenATV APIs, non-destructive package lifecycle rules, and the resolution-readiness rule above. Each integrated batch must remain traceable in Git and must pass the applicable static checks before receiver testing.


## Execution batch 1 — source recovery before code changes

Status: **IN PROGRESS**

Repository reconciliation confirms that the current default branch does not expose the unpacked Enigma2 runtime source tree: the post-1.0.4 changes are documentation, manifests, assets and updater metadata, while the stable runtime implementation is carried by the packaged 1.0.4 IPK. Therefore implementation work must not invent source paths or reconstruct screens from memory.

Required sequence for this batch:

1. Recover/unpack the exact stable 1.0.4 package payload as the implementation baseline.
2. Verify package payload identity and preserve all binding runtime identifiers.
3. Import the recovered source into the working line in a clearly documented source tree without changing runtime behavior.
4. Run a baseline static inventory before functional edits: XML screens, Python modules, control scripts, graphics/assets and compatibility symlinks.
5. Apply the already-known repair set only after baseline recovery: menu-source compatibility, safe package upgrade lifecycle, user-data preservation, safe archive extraction, non-destructive picon handling, Python 3 cleanup, and custom-spinner retirement after dependency/use audit.
6. Then continue the full screen/FHD audit and DAB+ work.

No release version bump is permitted merely for source recovery. Receiver-visible behavior changes remain test-build work until the GigaBlue/OpenATV acceptance pass is complete.


## Execution batch 2 — resolved project rules and validation matrix

Status: **ACTIVE**

The 2026-09-15 checkpoint's blanket geometry lock is superseded only where Štefan has now explicitly approved functional modernization: graphics keep their established visual character, while layout geometry, typography and asset resolution/format may be changed when required by current Enigma2/OpenATV behavior, readability, FHD use, or future resolution readiness. Binding runtime identifiers, authorship rules and updater architecture remain locked.

### Mandatory repair matrix for the next implementation package

| Area | Required result | Validation |
| --- | --- | --- |
| Menu source compatibility | no obsolete source dependency that can raise SkinError on current OpenATV | open all menu families + log check |
| PIG menu variants | exactly one navigational menu list; helper/current-selection display must be passive | PIG/PIG2/PIG4 navigation |
| Opkg screen | current named widgets for activity/package/status/progress/log; Close/Log usable | package operation on receiver |
| Package lifecycle | upgrade must not run destructive remove cleanup; defaults must not overwrite existing config | clean install + upgrade + force reinstall + uninstall |
| User data | preserve compatible weather/city/provider/skin settings | compare settings before/after upgrade |
| Picon handling | preserve user dirs/files and unrelated symlinks | filesystem before/after diff |
| Archive extraction | reject traversal/symlink abuse and partial/corrupt success | negative archive tests |
| Python 3 | no known invalid regex/SyntaxWarning and no obsolete active constructs found by static pass | compile/static pass |
| Spinner | audit all references first; remove obsolete FullHDGlass custom-spinner override and unused assets only after dependency check; leave OpenATV/Enigma2 system spinner in control | source/asset reference scan + install/upgrade + GUI restart |
| Weather/cities | retain existing Open-Meteo/city behavior and immediate refresh | functional regression test |
| DAB+ | investigate native current Enigma2/OpenATV slide/background mechanism without copying Metrix visuals | real DAB+ service test |
| FHD screens | modernize obsolete/crowded geometry and fonts while preserving Warder visual identity | 1920x1080 screen audit |
| Future resolution | avoid unnecessary FHD-only assumptions; keep derivable high-quality assets where practical | source review; no WQHD support claim yet |
| Updater | keep raw GitHub + SHA256 + eConsoleAppContainer architecture | end-to-end update test |

### Release discipline

The next implementation output is a **test build**, not a stable release. Stable 1.0.4 remains rollback/recovery baseline until the complete static gate and real GigaBlue Quad 4K Pro / OpenATV 8.x acceptance matrix pass and Štefan explicitly approves publication.


## Current OpenATV DAB+ source reconciliation — 2026-10-01

Status: **SOURCE/STATIC PASS — RECEIVER TEST REQUIRED**

Current OpenATV implements DAB slideshow handling natively through `DABSlideDisplay` in `Screens/RdsDisplay.py`, instantiated by `InfoBarRdsDecoder`. It reads the service preview image, scales the slide in GUI space, and calls `reserveRadioTextArea()` against the active `RdsInfoDisplay`.

Warder Evolution already defines the runtime widgets required by current `RdsInfoDisplay`: `RadioText`, `RtpText`, and `RassLogo`. Its full-screen 1920x1080 RDS layout provides a stable radio-text boundary for the native DAB slide display.

Therefore:
- do not add a legacy DAB renderer, file-copy hack, MPEG still-picture workaround, or Metrix-specific implementation;
- keep current OpenATV's native `DABSlideDisplay` in control;
- preserve the Warder RDS visual character;
- real DAB+ service validation remains mandatory on the receiver, including SLS appearance, station changes, fallback/no-slide behavior, and RDS text coexistence;
- this finding is not a RECEIVER PASS.
