# FullHDGlass Warder Evolution — branch integration audit, 22 November 2026

## Scope and protected production
- Current protected `main` baseline: `7e72d6e2b6d70eeb095b770d34430b3f53af9a2b`; runtime `1.0.80`, production updater `1.0.80`. The twelve numbered November skin repairs are in main's source (see `WARDER_PROGRESS.md`).
- Main received **eleven SAT picon catalogue commits** after the radio development branch forked. The integration retains the current main catalog `assets/warder/downloads/picons/channels/manifest.json` Git blob `7a7c6b4b96d9b8dc2da60a29c85ae1bd2069b715` and `SHA256SUMS` `e94b5342b8d3d82371ccfbc5898e397d7819a3bb` plus archive parts. **Never revert them to radio-branch copies.**
- Last validated radio feature commit `f831217977fff8ea5a3fcfc026ef8a799de68f0a` (TEST151). Integration branch `integration/fullhdglass-all-approved-radio-20261122` was created from current main and joined to this radio feature as a non-production two-parent commit `f0a3476d1299a9b9b7f91bda4786fbf73b5e8ba8`. Diff from main at creation: **76 code/config/test files**. Diff from latest radio feature to that commit: only main's newer SAT archives, metadata and audit. New draft [PR #131](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/131) targets main.
- No production IPK, version, tag, release, update feed, or receiver settings were altered by integration.

## Current branches and PRs (all 35 branch names checked)
| Cluster | Branches | Finding / required action |
| --- | --- | --- |
| Approved main | `main`, `automation/satellite-upload-20261119` | Identical heads at audit; newest SAT catalog must remain protected |
| Radio feature chain | `feature/dynamic-radio-bouquets-picons-20261119`, `fix/radio-country-native-group-marker-test136-20261119`, `fix/radio-country-large-catalog-progress-20261119`, `fix/radio-live-progressive-first-page-20261119`, `feature/radio-live-offline-country-bundles-20261119`, `feature/radio-live-world-bundle-installer-20261119`, `feature/unified-radio-screensaver-20261122` | Open draft PRs #124–130, **all included in the integration candidate**, not in main/release |
| Older comprehensive repair | `work/fullhdglass-all-repairs-20261117` | PR #115 diverged from main. Its EPG renderer and many changes are already present in main; missing **big-menu renderer fallback** restored to integration and corrected to currently approved IDs. Recovered integration test. Do not merge obsolete snapshot wholesale |
| Old own-picon fix | `fix/warder-private-picons-20261111` | PR #99 diverged; main-vs-branch diff is one stale test file, not a missing picon runtime. Do not overwrite modern main |
| Merged/behind main | `integration/fullhdglass-approved-repairs-no-ipk-20261118`, `fix/skin-i18n-21-languages-20261117`, `fix/spinner-mixed-24-frame-preserve-20261118`, `fix/global-picon-part-names-canalplus-20261118`, `fix/issue91-unified-telnet-messages-20261118` | Already integrated; no replay |
| Other superseded/test repair branches | `feat/warder-skin-settings-main-menu-20261117`, `fix/classic-channel-fullscreen-76-20261112`, `fix/date-format-preview-menu-20261110`, `fix/epg-fastscan-name-overlap-20261117`, `fix/epg-gles-runtime-gate-20261109`, `fix/menuiconsbig-plugin-id-mapping-20261117`, `fix/shared-emc-layout-20261112`, `fix/spinner-bakussa-image-default-20261112`, `fix/uv-wind-help-bubbles-20261117`, `fix/warder-mainmenu-approved-icon-bindings-20261117`, `fix/warder-storage-flash-guard-20261117`, `feat/cam-transparent-skin-downloads-20261117`, `audit/menu-icons-ids-and-dedup-20261117` | Source repairs are recorded as main-integrated in the original 12-point audit. Branch diffs do not authorize replaying old installer or graphic snapshots |
| Ancillary/test/asset | `repair/canal-tv5-transparent-20261117`, `repair/skylink-tv5-transparent-20261117`, `test/personal-skin-1080-r2-20261118`, `test/personal-skin-1080-r3-20261118`, `diagnostics/dns-warder-20261118-2042`, `warder-modernization-work` | Historical/asset/test branches, not a newer skin runtime to merge |
| Integration candidate | `integration/fullhdglass-all-approved-radio-20261122` | Current consolidated draft PR #131; no changes to main |

## Receiver confirmation and tests
- TEST151 physical receiver: owner confirmed one saver for DVB, DAB and Warder Radio Live, RDS/RT+, picons (including selected-country Live logos), covers and delay setting.
- Shared integrated offline QA [run #45021634747](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/45021634747) PASS for the first combined source, including exact current-main satellite hash guards, radios, country changes, EPG/Prime Time, storage and spinner tests.
- Test maintenance: `test-channel-picon-settings.py` now models the named `radioSaverDelay` in its config object; `test_warder_primetime_placements.py` validates the actual identical native/gated ChannelSelection-12 60,854 / 1370,40 geometry; the archived 1.0.79 two-file Neutrino package job is scoped to that version (current Neutrino compatibility tests remain active).
- PR #115 big-menu fallback was restored **without** superseding user-downloaded icons, using exact approved Enigma2 menu IDs; test `test_warder_menu_icon_bindings.py` expanded. Only actual existing stock artwork can be used; no unapproved logos added.
- Current full compatibility workflow failures **must not be mislabeled as all runtime failures**: OpenPLi tests include an outdated pre-1.0.80 skin hash; several setup-style historical widget/banner baselines no longer match main; Prime Time originally had stale ChannelSelection-12 geometry; OpenATV tests used an incomplete named-config mock; a Neutrino workflow incorrectly assumed every subsequent version is exactly 1.0.79. The live runtime/graphical UI still needs broad receiver verification beyond TEST151.

## Constraints and next steps
1. Finish full OpenATV/OpenPLi/test-style consistency checks; distinguish stale test expectations from real regression **before** editing runtime or updating a visual approval hash.
2. Verify installation/upgrade from stable 1.0.80 to one isolated integrated test candidate while retaining PATHS, downloaded SAT picons, user settings, bouquet state and external storage guards.
3. Confirm radio SK→CZ/UK→US hidden list refresh on-device and older OpenATV without GLES.
4. Review/retire PR #99/#115 only after mapping residual differences; retain historical branches until verified.
5. **Explicit owner approval needed** for merging PR #131 into protected main and for any production IPK/tag/update-feed publication. Keep 1.0.80 production untouched until then.

