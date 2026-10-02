# FullHDGlass17 9.50 r1-r12 cumulative regression audit

Authoritative functional reference: the original `enigma2-skin-fullhdglass17_9.50-r12_all.ipk`
supplied by the maintainer/user, plus the preserved r7-r12 changelogs and receiver observations.
The Warder branch must preserve the cumulative r12 behaviour while keeping Warder safety and
OpenATV/Python modernization.

## Source coverage

- r7, r9, r10 and r12: preserved SK/EN changelog files are available.
- r8 and r11: maintainer-published changelogs were recovered from the FullHDGlass17 forum thread.
- r4: a preserved maintainer audit note explicitly covers the original open/_exit behaviour, all Open-Meteo UI setText() updates, city/region/country, city-search results, saving the selected location, WMO descriptions, dates, sunrise/sunset, wind and Open-Meteo error text.
- r1-r3 and r5-r6: separate standalone changelog files were not present in the available sources. Their cumulative end state is therefore verified against the supplied original r12 IPK instead of inventing missing release notes. r7 explicitly requires preservation of the working r6 weather fixes, including current temperature and static weather icon support in Infobar.

## Cumulative requirements now guarded

### r1-r3 inherited baseline
- Preserve the original FullHDGlass17 visual/GUI structure and legacy functionality represented by r12.
- Do not reintroduce obsolete/insecure network or destructive lifecycle implementation merely to
  match old source; preserve the functional result with Warder-safe implementation.

### r4
- Preserve the original Open-Meteo screen open/exit lifecycle.
- Preserve the Open-Meteo UI update path (setText() outputs) represented by the r12 implementation.
- Preserve city, region/country and city-search result handling.
- Preserve saving the selected location.
- Preserve WMO condition descriptions, dates, sunrise/sunset, wind and other weather values.
- Preserve a visible Open-Meteo error message instead of an unhandled exception.

### r5-r6 inherited baseline
- Preserve the cumulative weather fixes carried forward into r7.
- Preserve working current temperature and static weather icon support in Infobar.

### r7
- Open-Meteo location management.
- Country-grouped city database and synchronized weather location handling.
- Add/edit/delete user locations, alphabetical grouping and duplicate protection.

### r8
- Complete Slovakia database: 4,208 locations.
- Complete Czechia database: 6,258 locations.
- Preserve all originally supported other countries.
- Country -> city/municipality navigation.
- Right-pane `/etc/my_city_Code.txt` navigation.
- Quick saved-city selection from Weather for City.
- Weather refresh after location change without GUI restart.
- Case- and diacritic-insensitive local search, then online fallback.
- Provider/API-key rows removed from the user-facing weather setup.

### r9
- Enhanced Weather legacy migration to Open-Meteo.
- Empty geocoding-result and incomplete-coordinate guards.
- No `list index out of range` on missing location.
- Meaningful invalid-location error handling.

### r10
- Preserve r8/r9 weather workflow and improve both Classic and Enhanced Open-Meteo.
- Legacy Enhanced Weather names ending in `station` migrate safely.
- Open-Meteo condition text localization with English fallback.
- Upgrade/reinstall cleanup remains safe.

### r11
- PIG navigation fix applies to all four variants: with PIG, simply PIG, PIG2, PIG4.
- All eight affected menu screens use one navigational Listbox; passive selected-item display must
  not compete for navigation.
- Remote movement and OK activation follow the actually selected item.
- Nested menus and FullHDGlass17 setup remain reachable.

### r12
- Opkg/Installing Software screen reaches the final state and retains Close/Log controls.
- Obsolete FullHDGlass17 dove spinner is not installed/used.
- Upgrade/reinstall cleanup does not depend on missing backup files.
- r11 PIG fixes and all earlier cumulative functionality remain preserved.

## Warder additions that must remain

- OpenATV ScreenSaver startup fix: movable picture remains smaller than the 1920x1080 desktop.
- User/image-owned files are not destructively replaced.
- Existing FullHDGlass17 settings survive upgrade.
- Atomic writes, argv-safe command execution, Python 3/OpenATV compatibility and package lifecycle
  hardening remain in force.

## TEST4 audit result

The original r12 location database contains 51 country codes and 11,010 locations. TEST4 restores
that complete set while retaining the full SK/CZ data. The top-level Slovak receiver UI is restored
to `Slovensko`, `Česko`, `Krajiny Európy`; the Europe group then exposes the remaining countries.

Permanent CI gate: `tools/test-r12-regressions.py`.

TEST4 workflow run `36873574739` on exact commit
`e56957f7247ba99c7bb2e6edbcab9b9acbcf7ded`: **SUCCESS**.

- r1-r12 regression gate: PASS
- locations: SK=4208, CZ=6258, TOTAL=11010, COUNTRIES=51
- lifecycle static semantics: PASS
- package lifecycle guardrail: PASS
- runtime safety guardrail: PASS
- version ordering: PASS
- XML parse gate: PASS
- TEST IPK integrity: PASS
- package: `enigma2-skin-fullhdglass17-warder-evolution_1.0.5-test4_all.ipk`
- package SHA256: `27cc709817f0aba8242f0f8ffd8bb3c84de84d90660a681d3d033bf681cefbbd`
- artifact ID: `11168192606`
- artifact ZIP SHA256: `2eb5f18c9026621475f1e7bddfb3964ed3ba78f14b82d3bbe466d7b5864baf51`

Receiver validation is still required for dynamic GUI behaviour. Static/CI PASS is not a substitute
for receiver confirmation.

## TEST4 r4 revalidation

After adding explicit r4 Open-Meteo regression assertions, workflow run `36875836272` on commit `9c605e3623bbcb0de953b47be118b68c796523af` completed successfully. The cumulative r1-r12 gate, 11,010-location/51-country gate, lifecycle, runtime safety, XML and package integrity gates all PASS. Rebuilt TEST4 IPK SHA256: `b0f804929f189fab66f4f0c720a488cdd82c0dce358cbd876774e5412b02a9f6`; artifact ID `11168722243`; artifact ZIP SHA256 `42a71e19c5378381215111fad1c13c76f672f7096ed2c71604ecaa44f6e49fb0`.

## TEST4 full weather localization validation

The r10 language requirement is now enforced end-to-end rather than only at Python source level.
Classic Weather and Enhanced Weather share one canonical Open-Meteo/WMO vocabulary. Every non-English
weather catalog shipped by FullHDGlass17 contains the complete guarded WMO vocabulary; Enhanced
Weather catalogs are guarded likewise. The TEST builder recompiles every PO catalog to MO before
staging the package, preventing stale binary catalogs from reaching a receiver.

Workflow run `36879533776` on exact build commit
`dee61c163fc6e66cf372806c2caea1c116494e8e`: **SUCCESS**.

- r1-r12 regression gate: PASS
- locations: SK=4208, CZ=6258, TOTAL=11010, COUNTRIES=51
- compiled Slovak Classic/Enhanced Weather catalogs inside final IPK: PASS
- lifecycle/runtime/XML/version/package integrity gates: PASS
- package: `enigma2-skin-fullhdglass17-warder-evolution_1.0.5-test4_all.ipk`
- package SHA256: `e366d9b51f6b592040a7365d0135732b4d3c1c56653fc712f8744a8f5c745d8c`
- artifact ID: `11170761103`
- artifact ZIP SHA256: `4e4d37e74993f6981c544916f5cc636d83b8c2b779aecfdbc3a7f733cb828392`

Receiver validation remains required for the rendered weather text and dynamic UI behaviour.


## Current Warder parity checkpoint

The later TEST4 audit series additionally locked the following r11/r12 and OpenATV ownership
behaviour into permanent CI regression checks:

- all four PIG menu variants retain their r12 menu IDs and PIG geometry switching;
- all eight affected menu screens remain present with one navigational Listbox;
- Infobar service-start/event-update weather integration remains wired;
- standard picon discovery/fallback remains available without Warder creating or retargeting
  image-owned `/usr/share/enigma2/picon*` links;
- a blank/corrupt legacy picon path cannot crash setupGlass17;
- legacy spinner repair is non-destructive and only runs when the saved image spinner exists;
- setup save/restore remains available and generated FullHDGlass state uses atomic writes;
- upgrade/reinstall lifecycle preserves Enigma2 settings and the FullHDGlass user overlay;
- Opkg/package-manager screens retain the r12 software-installation surface, including the Opkg
  red and blue key sources and log widget;
- Warder updater uses argv-safe opkg/dpkg execution, SHA256 verification, and both the requested
  package URL and the final redirected URL must stay inside the official Warder `main/packages/`
  channel.

Latest fully green build before the PIG/Opkg parity-gate extension: workflow run `36884898392`
on exact commit `f4b8d05e6fd1e76094bc44ff9b95c4c4fe6f8cc7`: **SUCCESS**.

- r1-r12 regression gate: PASS
- locations: SK=4208, CZ=6258, TOTAL=11010, COUNTRIES=51
- lifecycle static semantics: PASS
- package lifecycle guardrail: PASS
- runtime safety guardrail: PASS
- XML parse gate: PASS
- TEST IPK integrity: PASS
- package: `enigma2-skin-fullhdglass17-warder-evolution_1.0.5-test4_all.ipk`
- package SHA256: `3a7ebd5c22be1e8cb1b5c7b3ae1bc05cc069b948264fb4106bcbf036ea0fae19`
- artifact ID: `11174635755`
- artifact ZIP SHA256: `31147522776798828f40cdd8eb5d86e9f8cc2f285eca86e7cb7794bd683c0366`

Receiver validation remains separate and is required before any receiver PASS is recorded.

## TEST20 packaging regression guard

The TEST package gate now distinguishes the skin runtime/updater identity from opkg's package revision syntax. Runtime/updater versions retain `1.0.5-testXX`; IPK control metadata appends numeric revision `-1`, so the final hyphen is reserved for opkg package revision and the visible/base version remains `1.0.5-testXX`. This is packaging-only and must not alter the receiver-verified TEST18 weather or TEST19 PIG implementation.

### TEST20 CI result

Workflow #80 / run `36923438508` completed SUCCESS on commit `815e097ef80b8a14ead21af806af649bbdb8d906`. The final published TEST20 IPK SHA256 is `32ed703e06955c7e2675b5997ea10fc510e7269aeb71b5d327fe17b5e1b1869c`. Final-package inspection confirms control `Version: 1.0.5-test20-1` and runtime `1.0.5-test20`. Receiver confirmation remains separate.


### TEST20 physical receiver result

GigaBlue Quad 4K Pro / OpenATV receiver validation is **PASS**. The real install transition was displayed as `1.0.5-test19 -> 1.0.5-test20`, GUI restarted normally, and installed package status reports raw control version `1.0.5-test20-1` with `install ok installed`. This closes the package-version presentation regression without reopening the already receiver-approved TEST18 weather/city or TEST19 PIG behavior.


### TEST21 physical receiver result — PASS (2026-10-01)
GigaBlue Quad 4K Pro / OpenATV 8.x confirmed the previously missing OpenATV MediaScanner `MessageBoxModal` is now skinned consistently with FullHDGlass17. The real local-extension workflow was visually checked through media selection, “The following files were found...” modal and the existing installer list. The installer screen was not changed. User explicitly approved the result as OK. TEST21 is locked as RECEIVER / VISUAL PASS; TEST18–TEST20 remain locked.
