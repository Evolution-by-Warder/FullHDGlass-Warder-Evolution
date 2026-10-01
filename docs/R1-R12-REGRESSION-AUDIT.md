# FullHDGlass17 9.50 r1-r12 cumulative regression audit

Authoritative functional reference: the original `enigma2-skin-fullhdglass17_9.50-r12_all.ipk`
supplied by the maintainer/user, plus the preserved r7-r12 changelogs and receiver observations.
The Warder branch must preserve the cumulative r12 behaviour while keeping Warder safety and
OpenATV/Python modernization.

## Source coverage

- r7, r9, r10 and r12: preserved SK/EN changelog files are available.
- r8 and r11: maintainer-published changelogs were recovered from the FullHDGlass17 forum thread.
- r1-r6: separate standalone changelog files were not present in the available Library/forum search.
  Their cumulative end state is therefore verified against the supplied original r12 IPK instead of
  inventing missing release notes. r7 explicitly requires preservation of the working r6 weather
  fixes, including current temperature and static weather icon support in Infobar.

## Cumulative requirements now guarded

### r1-r6 inherited baseline
- Preserve the original FullHDGlass17 visual/GUI structure and legacy functionality represented by r12.
- Preserve the working weather fixes inherited by r7, including current temperature and static
  weather icon support in Infobar.
- Do not reintroduce obsolete/insecure network or destructive lifecycle implementation merely to
  match old source; preserve the functional result with Warder-safe implementation.

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
