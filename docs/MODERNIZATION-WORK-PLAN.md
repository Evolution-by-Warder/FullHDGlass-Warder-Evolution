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
