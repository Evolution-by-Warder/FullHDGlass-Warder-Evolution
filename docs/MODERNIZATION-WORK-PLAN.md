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


## OpenATV system utilities batch — 2026-10-01

Status: **SOURCE/STATIC REVIEW — RECEIVER TEST REQUIRED**

Reviewed current OpenATV screen contracts for DAB scan, Device Manager, Flash Manager, MultiBoot Manager, Network Services, Picon Settings and network restart.

Results:
- `DABScan` deliberately aliases `ServiceScan`; existing Warder `ServiceScan` remains authoritative.
- Device-manager action/mount/setup classes derive from current `Setup`; existing Warder `Setup` remains the fallback. The dedicated current `DeviceManager` screen was already present.
- `FlashOnline` was reconciled to current `FlashManager` widgets and modernized to the Warder FHD geometry; `FlashImage` now has a dedicated Warder FHD screen.
- `MultiBootManager` and `KexecInit` embedded low-resolution OpenATV layouts now have dedicated Warder FHD screens. Slot-manager subclasses continue to use current `Setup`.
- `uShareSelection` and `NetworkLogScreen` now have dedicated Warder FHD screens. Network service setup classes continue to use the common current `Setup` contract.
- `PiconSettings` derives from current `Setup`; no duplicate standalone layout is required.
- legacy `RestartNetwork` explicitly selects skin name `DUMMY`; a zero-size Warder `DUMMY` compatibility screen is provided, while current `RestartNetworkNew` uses the Processing singleton.
- No item in this batch is marked RECEIVER PASS.


## OpenATV tuner / update / restore batch — 2026-10-01

Status: **SOURCE/STATIC REVIEW — RECEIVER TEST REQUIRED**

Reviewed current OpenATV runtime contracts for CI, Auto DiSEqC, scan/tuner configuration, backup/restore, software update, task/job screens, Opkg/package feeds, factory reset and power-loss handling.

Changes and decisions:
- added dedicated Warder FHD `AutoDiseqc` and `SelectSatsEntryScreen` layouts from current runtime widget contracts;
- added current `SoftwareUpdate` FHD layout including feed traffic-light widgets, feed message, activity slider and indexed templated package list;
- added current `RunSoftwareUpdate` FHD progress/log layout;
- `SoftwareUpdateSummary` intentionally reuses the existing Setup-summary `entry` / `value` contract; no duplicate full-screen layout added;
- modernized current backup/restore helper UI with dedicated `installedPlugins` and `RestorePlugins` FHD layouts;
- `BackupScreen` and `RestoreScreen` are intentionally zero-size execution helpers in current OpenATV and were not visually expanded;
- current CI PIN, FactoryReset and multiple service/setup classes intentionally resolve through the common `Setup` contract;
- existing Task/Job and Opkg/package-feed layouts were retained where the current runtime contract is already represented;
- `PowerLost` is not a Screen class and therefore requires no skin definition;
- no item in this batch is marked RECEIVER PASS.


## OpenATV UI / locale / plugin-management batch — 2026-10-01

Status: **SOURCE/STATIC REVIEW — RECEIVER TEST REQUIRED**

Reviewed current OpenATV HDMI-CEC, video mode, input-device, locale, date/time, parental-control, sleep-timer, skin-selection, plugin-browser, quick-menu and button-setup runtime contracts.

Results:
- HDMI-CEC, keyboard/input-device/remote-control, locale settings, date/time, parental control, sleep timer and plugin-browser setup classes are current `Setup` derivatives where appropriate; the common Warder Setup layout remains authoritative.
- added a dedicated current `LocaleSelection` FHD screen with indexed flag/native/name/package/status list contract and current action labels.
- existing Warder PluginBrowser/List/Grid layouts already represent the current browser contract and were retained.
- added dedicated FHD `PackageAction` and `PackageActionLog` layouts; current `PluginAction` and `PluginActionLog` intentionally fall back to those skin names.
- `PackageActionSummary` / `PluginBrowserSummary` remain front-panel summary contracts, not full-screen modernization targets.
- `AutoVideoMode` is a runtime event screen without visual widgets. `AutoVideoModeLabel` has only `content` and `restxt`; no new full-screen layout was introduced without a confirmed current default-skin placement requirement.
- existing VideoSetup, InputDeviceSelection, SkinSelection, QuickMenu and ButtonSetup family layouts were retained where already present.
- no item in this batch is marked RECEIVER PASS.


## OpenATV EPG / movie / timer / dialogs / information batch — 2026-10-01

Status: **SOURCE/STATIC REVIEW — RECEIVER TEST REQUIRED**

Reviewed current OpenATV ChannelSelection, EPG, MovieSelection, recording/timer, MessageBox/ChoiceBox/TextBox/VirtualKeyboard and Information screen families.

Results:
- current `SingleEPG` intentionally selects `EPGSelection`; no duplicate layout required.
- current `EPGBouquetSelector` falls back to `BouquetSelector`; a Warder alias was added so the current preferred screen name resolves directly while preserving the established visual layout.
- ChannelSelectionSetup, MovieSelectionSetup, RecordingSettings, SchedulerEdit, RecordTimerEdit and InstantRecordTimerEdit are current `Setup` derivatives; common Warder Setup remains authoritative.
- legacy TimerEntry/TimerLog wrappers map to the current Timers implementation; existing Warder timer overview/log coverage remains in place.
- current ChoiceBoxNew intentionally selects `ChoiceBox`; existing Warder ChoiceBox remains authoritative.
- current Information subclasses all fall back to `Information`, but many add MENU/INFO/yellow/blue actions. Dedicated Warder FHD aliases were added for the full current Information family so every preferred current skin name resolves directly while retaining the generic information geometry and complete action row.
- `InformationPicture` remains separately specialized for image display.
- no item in this batch is marked RECEIVER PASS.


## OpenATV subtitle / event / playback overlay batch — 2026-10-01

Status: **SOURCE/STATIC REVIEW — RECEIVER TEST REQUIRED**

Reviewed current OpenATV AudioSelection, SubtitleDisplay, EventView, PVRState and InfoBarGenerics visual/runtime contracts.

Results:
- `SubtitleSelection` intentionally selects the existing `AudioSelection` skin; no duplicate screen required.
- added a dedicated full-screen transparent `SubtitleDisplay` overlay using the current single `subtitles` widget contract.
- current EventViewSimple / EventViewEPGSelect / EventViewMovieEvent all resolve to the existing Warder `EventView`; its current channel/datetime/duration/EPG/action widgets remain the shared authority.
- existing Warder PVRState and TimeshiftState definitions were retained.
- `ExtensionsList` is a ChoiceBox specialization and continues through ChoiceBox fallback.
- added dedicated current `BufferIndicator` and `VideoMode` overlay definitions from their exact current runtime widget contracts.
- `HideVBILine` and `AutoVideoMode` have no skin widgets and do not require decorative definitions.
- SecondInfoBar requires separate receiver-facing visual review before changing its established FullHDGlass behavior; no blind replacement was made.
- no item in this batch is marked RECEIVER PASS.


## OpenATV wizard / location / logs / standby / network helpers batch — 2026-10-01

Status: **SOURCE/STATIC REVIEW — RECEIVER TEST REQUIRED**

Reviewed current Console, HarddiskSetup, LocationBox, LogManager, NetworkSetup, ServiceScan, Standby, Wizard, fallback-tuner and SoftcamSetup screen contracts.

Results:
- added direct current-name aliases for `PlaybackLocationBox` and `TimeshiftLocationBox` using the established Warder LocationBox geometry.
- added direct current-name aliases `WizardStart`, `WizardLanguage` and `WizardVideo` over the existing FullHDGlass StartWizard/VideoWizard layouts, preserving the established wizard visual character while resolving current OpenATV preferred names.
- added dedicated Warder FHD `LogManager` and `LogManagerViewLog` layouts from their current runtime widgets.
- NetworkAdapterSetup, NetworkWiFiSetup, DNSSettings, SetupFallbacktuner, CardserverSetup, AutocamSetup and StreamRelaySetup are current Setup derivatives and continue through the common Warder Setup contract.
- NetworkInformation derives from the already-covered InformationNetwork family.
- Standby2 intentionally selects `Standby`; TryQuitMainloop is a MessageBox specialization or zero-size runtime helper and was not duplicated.
- existing Console, HarddiskSelection, ServiceScan, WizardInstall and SoftcamSetup coverage was retained.
- no item in this batch is marked RECEIVER PASS.


## OpenATV remaining core utilities + CAM information batch — 2026-10-01

Status: **SOURCE/STATIC REVIEW — RECEIVER TEST REQUIRED**

Reviewed current OpenATV BoxPortal, CronTimer, DVD, Dish, FixedMenu, FlashExpander, Help/Input, OSDCalibration, Playback, QuadPiP, RTL-SDR, SD swap, Scart, ScreenSaver, TagEditor, Time/Timeshift, Toast, UnhandledKey, VolumeControl, CCcamInfo, OSCamInfo, ImageBackup, SwapManager and storage helpers.

Changes and decisions:
- added direct Warder FHD coverage for BoxPortal, CronTimers, FixedMenu, XMLHelp, ScreenSaver, TagEditor, ToastScreen and UnhandledKey.
- CronTimersConfig, FlashExpander, OSDCalibration, PlaybackSettings, RTLSDRSetup, Time, TimeshiftSettings and volume-adjust settings are Setup-derived and remain on the common Warder Setup contract.
- QuadPiP intentionally selects PictureInPicture; existing Warder PiP geometry remains authoritative.
- existing DVDPlayer/ChapterZap, Dish, InputBox, NumericalTextInputHelpDialog, Mute/Volume, ImageBackup and Swap coverage was retained.
- current CCcamInfo and OSCamInfo were identified as a significant direct-coverage gap. Added Warder FHD layouts for CCcam main/ECM/text/submenu/server views and OSCam capabilities/log/entitlement-detail views from their exact runtime widget contracts.
- additional complex CCcam/OSCam list screens remain queued for contract-specific templates rather than receiving blind generic layouts.
- no item in this batch is marked RECEIVER PASS.


## OpenATV CAM management completion batch — 2026-10-01

Status: **SOURCE/STATIC REVIEW — RECEIVER TEST REQUIRED**

Completed current OpenATV CCcamInfo / OSCamInfo / SoftcamSetup runtime reconciliation.

Results:
- completed direct Warder FHD coverage for CCcam Share View, Remote Receiver, Extended Shares, Config Switcher and Menu Configuration screens in addition to the previously added main/ECM/info/submenu/server screens.
- completed OSCam direct coverage with the main `OSCamInfo` dashboard, entitlements, entitlement details, capabilities and log screens.
- modernized the existing Warder `SoftcamSetup` to a 1500x840 FHD layout while preserving the current OpenATV `config` and live ECM `info` widgets.
- the Softcam action row now exposes the current runtime red/green base Setup actions, yellow Restart action and blue Info action; Info opens the native OSCamInfo or CCcamInfo path selected by current OpenATV.
- CardserverSetup remains a Setup-derived screen; AutocamSetup and StreamRelaySetup remain on the common Setup contract with their current yellow/blue dynamic actions.
- static presence audit confirms all 16 CAM screen names reviewed in this batch resolve in Warder skin.xml.
- global duplicate-name audit reports pre-existing duplicate screen names elsewhere in the historical skin/plugin sections; no new CAM duplicate was introduced. These legacy duplicates require a separate precedence/ownership audit before removal.
- no item in this batch is marked RECEIVER PASS.


## Duplicate ownership + storage utility batch — 2026-10-01

Status: **SOURCE/STATIC REVIEW — RECEIVER TEST REQUIRED**

Audited all duplicate screen names reported by the static skin inventory and rechecked current ImageBackup, FlashManager, SwapManager, SDswap and DeviceManager runtime coverage.

Duplicate ownership results:
- ChannelSelection_summary, MenuSummary, InfoBarMoviePlayerSummary, DVDSummary, SetupSummary, SimpleSummary and g17SetupSummary pairs are intentional display-ID variants (`id="1"` / `id="2"`) for different front-panel displays; they are not redundant and remain untouched.
- duplicate RSS reader screens and EPGRefreshConfiguration were true same-name/same-target historical alternatives without hardware IDs. The redundant second definitions were removed, retaining the Warder/Prive variants.
- FilterListScreen remains an unresolved plugin-ownership collision between a generic filter layout and a VideoDB full-screen layout. It was deliberately not removed until plugin ownership/precedence is proven.
- PlaylistItemSetup was not actually duplicated; the previous duplicate report came from the broad historical audit context.

Storage/system results:
- current ImageBackup, FlashOnline/FlashImage, Swap and DeviceManager contracts remain covered.
- DeviceManager Setup-derived action/setup classes remain on common Setup.
- added a direct Warder FHD `SDswap` screen for the current runtime red/green/yellow NAND/SD switching actions.
- DevicesPanelSummary is a front-panel summary using SetupSummary behavior and does not require a new full-screen layout.
- no item in this batch is marked RECEIVER PASS.


## Plugin ownership + global static gate — 2026-10-01

Status: **STATIC GATE PARTIAL PASS — RECEIVER TEST REQUIRED**

Resolved the remaining known same-target plugin precedence conflicts and ran a broader skin.xml static inventory.

Results:
- both historical `FilterListScreen` definitions belong to the VideoDB skin block, but the later 1920x1080 definition is the coherent member of the full-screen VideoDB suite and uses the packaged `hd_glass17/videodb/*` assets. The obsolete 800x550 definition was removed.
- the same precedence issue existed for `PlaylistItemSetup`: the old narrow legacy definition was removed and the coherent 1920x1080 VideoDB definition retained.
- the old empty self-closing `SubtitleDisplay` placeholder was removed; the current functional full-screen definition with the runtime `subtitles` widget remains authoritative.
- after cleanup, remaining duplicate screen names are intentional front-panel display variants using `id="1"` and `id="2"`.
- asset gate: all 137 unique skin.xml pixmap/backgroundPixmap/selectionPixmap references under `hd_glass17/` resolve to files present in the branch tree.
- the static scan also found 11 historical `forgroundColor` misspellings. These are queued for targeted ownership/context correction rather than blind global replacement.
- this gate does not constitute XML parser/runtime or receiver acceptance; no RECEIVER PASS is claimed.


## Static gate follow-up — VideoDB attributes + core batch — 2026-10-01

Status: **STATIC REVIEW PASS — RECEIVER TEST REQUIRED**

- corrected all 11 remaining historical `forgroundColor` misspellings in the VideoDB block to the current Enigma2/OpenATV `foregroundColor` attribute; current OpenATV `lib/python/skin.py` was checked before changing the attributes.
- reviewed the next OpenATV core batch against current master: BoxPortal, ButtonSetup, CronTimer, FactoryReset, FixedMenu, FlashExpander, HDMICEC, HarddiskSetup, ImageBackup and InputDeviceSetup.
- FactoryReset, FlashExpander, HDMICECSetup, KeyboardSelection, InputDeviceSetup and RemoteControlType are Setup-derived in current OpenATV and intentionally remain on the shared Warder Setup unless a verified specialized runtime requirement appears.
- InputDeviceSelection, HarddiskSelection, ImageBackup, BoxPortal, ButtonSetup/ButtonSetupSelect, CronTimers and FixedMenu already have direct or appropriate shared coverage in the current skin.
- no RECEIVER PASS is claimed.


## Core Screens reconciliation batch — 2026-10-01

Status: **STATIC REVIEW PASS — RECEIVER TEST REQUIRED**

Current OpenATV master was checked for LogManager, OSDCalibration, ParentalControlSetup, PiPSetup, QuadPiP, QuickMenu, RTLSDRSetup, Recording, RestartNetwork, Satconfig, ScanSetup, ScriptRunner, SetupFallbacktuner, SleepTimer, SwapManager, TaskList, TaskView, Time and TimeDateInput.

Results:
- `OSDCalibration` intentionally carries its own resolution-specific embedded pixel-accurate skin and explicitly refuses the standard Setup skin; no external override was added.
- `RTLSDRSetup`, `RecordingSettings`, `SetupFallbacktuner`, `SleepTimer` and `Time` are current Setup-derived screens and remain on the shared Warder Setup path.
- `ParentalControlSetup` and `ParentalControlChangePin` already expose Setup fallback in their current runtime skinName lists.
- `QuadPiP` deliberately uses `PictureInPicture`; `RestartNetwork` deliberately uses runtime skinName `DUMMY`.
- direct current coverage was confirmed for LogManager/LogManagerViewLog, PiPSetup/PictureInPicture, QuickMenu, NimSetup/NimSelection/SelectSatsEntryScreen, ScanSetup/ScanSimple, ScriptRunner, Swap, TaskList/TaskListScreen and TaskView/JobView.
- `TimeDateInput` is a legacy third-party compatibility screen with a small explicit `config` + red/green contract. It is recorded as a fallback-gap candidate, but no speculative override was added in this batch.
- no RECEIVER PASS is claimed.


## Input compatibility reconciliation — 2026-10-01

Status: **STATIC REVIEW PASS — RECEIVER TEST REQUIRED**

- audited current OpenATV AudioSelection, ChoiceBox, Ci, Console, DVD, EventView, HelpMenu, InputBox, LocationBox, MessageBox, TimeDateInput and MinuteInput ownership/skinName behavior.
- confirmed `SubtitleSelection -> AudioSelection` and `PermanentPinEntry -> ParentalControlChangePin/Setup`; no duplicate aliases were added.
- added FHD `PinInputPopup` using the verified current `service/text/tries/input` contract.
- added FHD `TimeDateInput` using the verified current `config`, `key_red` and `key_green` sources; this closes the recorded third-party compatibility fallback gap.
- added FHD `MinuteInput` using its verified current `minutes` widget contract.
- `HelpMenu` remains under active review because current `ShowRemoteControl` dynamically creates remote-control indicator widgets; it must not be replaced by a partial speculative layout.
- no RECEIVER PASS is claimed.


## Playback / video / utility reconciliation — 2026-10-01

Status: **STATIC REVIEW PASS — RECEIVER TEST REQUIRED**

- audited current OpenATV PVRState, Playback, Processing, ScreenSaver, SkinSelection, Standby, SubtitleDisplay, TagEditor, Toast, UnhandledKey, VideoMode, VirtualKeyBoard, VolumeControl and Wizard modules.
- confirmed PlaybackSettings, SkinSelection and VolumeAdjustSettings are Setup-derived and remain on shared Warder Setup.
- confirmed ScreenSaver runtime fallback `[ScreenSaver, Screensaver]`, VirtualKeyboard/VirtualKeyBoard compatibility and existing direct coverage for the active PVR/timeshift, processing, standby, subtitle, tag, toast, unhandled-key and virtual keyboard screens.
- added FHD `AutoVideoModeLabel` for the current autostart-instantiated resolution notification using its verified `content/restxt` widget contract.
- `AutoVideoMode` itself has no GUI widgets and is not given a speculative external screen.
- `VolumeAdjustServiceSelection` has a current embedded skin and fallback aliases; no duplicate external override was added without a demonstrated need.
- Wizard family remains a specialized runtime path and is not collapsed into generic Setup.
- no RECEIVER PASS is claimed.


## Post-change global static gate — 2026-10-01

Status: **PASS WITH RUNTIME TEST PENDING**

- current skin contains 615 screen definitions / 608 unique names.
- the only duplicate names are the seven previously audited front-panel summary families: ChannelSelection_summary, MenuSummary, InfoBarMoviePlayerSummary, DVDSummary, SetupSummary, SimpleSummary and g17SetupSummary; their id variants remain intentionally preserved.
- zero `forgroundColor` misspellings remain.
- all newly added PinInputPopup, TimeDateInput, MinuteInput and AutoVideoModeLabel names occur exactly once.
- internal asset reference recheck found no missing Warder skin asset. PositionGauge `pointer="hd_glass17/pointer.png:13,3"` uses the Enigma2 pointer syntax (asset plus hotspot coordinates); the actual `hd_glass17/pointer.png` file is present.
- external DreamExplorer pointer remains plugin-owned and was not copied or rewritten.
- no RECEIVER PASS is claimed.


## Remaining OpenATV core-screen reconciliation — 2026-10-01

Status: **STATIC REVIEW PASS — RECEIVER TEST REQUIRED**

- audited the remaining current OpenATV core screen families not covered by the earlier passes: backup/restore, button/CCcam, device/storage, flash/multiboot, locale/input devices, network services/mounts, OSCam/opkg, parental control, recording/software update, swap/tasks, timers/timeshift and wizard families.
- added FHD `FlashManager` using its verified current list/description/color/help contract; existing `FlashOnline` remains separately preserved.
- added FHD `Dishpip` using the current rotor/tuner widget contract while preserving the existing `Dish` screen.
- added `NetworkInadynLog` compatibility layout matching the verified current `NetworkLogScreen` infotext contract and runtime fallback order.
- confirmed BackupScreen/RestoreScreen and BackupHelper deliberately use tiny/zero-size embedded worker screens and should not be converted into visible dialogs.
- confirmed DevicesPanelSummary aliases to SetupSummary; ChkrootInit aliases to KexecInit; QuadPiP aliases to PictureInPicture; PackageFeedEditor inherits VirtualKeyboard; no duplicate layouts were added for those cases.
- OSDCalibration intentionally owns a pixel-perfect resolution-aware embedded skin and is left untouched.
- current wizard compatibility names WizardInstall/InstallWizard, WizardStart/StartWizard, WizardLanguage and WizardVideo/VideoWizard are already present.
- no RECEIVER PASS is claimed.


## Core-screen post-reconciliation gate — 2026-10-01

Status: **PASS — RUNTIME TEST STILL REQUIRED**

- skin now contains 618 screen definitions / 611 unique names.
- duplicate-name set is unchanged and limited to the seven previously audited front-panel summary families.
- zero `forgroundColor` misspellings remain.
- FlashManager, Dishpip and NetworkInadynLog each occur exactly once.
- all directly referenced internal Warder pixmap/background/selection assets resolve to files in the package tree.
- no RECEIVER PASS is claimed.


## setupGlass17 runtime / custom component audit — 2026-10-01

Status: **STATIC REVIEW IN PROGRESS — RECEIVER TEST REQUIRED**

- inventoried all packaged setupGlass17 Python screens and their embedded-skin ownership. The plugin intentionally owns a mixture of full-HD setup screens, compact selectors/positioning overlays and dynamically generated screens; these must not be mechanically moved into the global skin.
- confirmed the current OpenATV `Components.Element.cached` decorator remains available, so the custom converter family's cached-property usage is valid.
- audited the first custom renderer/converter batches for Python-2-only constructs and obsolete timer/navigation patterns. No `has_key`, `iteritems`, `xrange`, `unicode` or `basestring` use was found in the checked batches.
- `NavigationInstance.instance` remains a current OpenATV-supported global and is therefore not rewritten in g17EmptyEpg/g17Prov.
- legacy `eTimer.timeout.get().append(...)` occurs only as compatibility fallback behind the modern `.timeout.connect(...)` path in the checked renderer code; it is retained intentionally for cross-image compatibility.
- setupGlass17 embedded layouts use the expected Enigma2 `halign`/`valign` skin attributes and contain no `forgroundColor` typo.
- no RECEIVER PASS is claimed.


## Python 3 helper modernization — 2026-10-01

Status: **STATIC REVIEW PASS — RECEIVER TEST REQUIRED**

- completed the next custom renderer/converter compatibility pass and verified that every `g17*` renderer/converter referenced directly by the global skin exists in the package tree.
- retained legacy custom components that are not referenced by the global skin because they can be selected dynamically by FullHDGlass17 extra-screen/style/runtime paths; no destructive cleanup was performed.
- confirmed the two `unichr()` fallbacks in g17ServiceNum/g17HDDstate are guarded by `ISP38 == False`; current Python 3/OpenATV execution imports `DG` from the Python-3 helper instead.
- modernized `setupGlass17/py38.py`: removed its unnecessary external `six` dependency, uses native Python 3 `dict.items()` and `chr()`, corrected the script/style DOTALL regex for current Python `re`, and removed an invalid text `.decode()` fallback.
- this change does not alter screen geometry, skin authorship, package identity or the locked 1.0.4 artifact.
- no RECEIVER PASS is claimed.


## Weather ownership + package hygiene audit — 2026-10-01

Status: **STATIC REVIEW PASS — RECEIVER TEST REQUIRED**

- verified weather runtime ownership before removing any legacy provider code: `weather.py/WeatherScreen` remains actively instantiated for the classic FullHDGlass17 weather modes, while `E_weather.py/mainmenu` is a separate enhanced Open-Meteo path. OpenWeatherMap code is therefore still runtime-active and is not removed as dead code.
- MSN branches are effectively disabled by `chMSN() == False`, but broad removal is deferred until the classic WeatherScreen data contract is deliberately migrated; no speculative provider cleanup was performed.
- found and removed an accidentally packaged `setupGlass17/__pycache__/plugin.cpython-313.pyc` build artifact from the Architecture: all package tree.
- added repository `.gitignore` rules for `__pycache__/`, `*.py[cod]` and `*$py.class` to prevent generated Python bytecode from re-entering future packages.
- no RECEIVER PASS is claimed.


## Custom converter Python 3 runtime reconciliation — 2026-10-01

Status: **STATIC REVIEW PASS — RECEIVER TEST REQUIRED**

- compared Warder custom converter behavior with current OpenATV converter contracts instead of treating legacy timer callbacks as automatically obsolete; current OpenATV still supports the callback-list path.
- aligned `g17ConditionalShowHide` with current ConditionalShowHide semantics: an unavailable boolean source is hidden rather than shown, semicolon/comma token separators are accepted, numeric blink intervals are honored, and converter change propagation is retained. The FullHDGlass17 `par114` behavior remains intact.
- fixed Python-2 integer-division assumptions in `g17ClockToText` and `g17EventTime`; minute/duration formatting now uses integer division on Python 3.
- fixed the same integer-formatting issue in `g17extServiceName` for frequency, symbol rate and orbital-position text. These expressions feed `%d` and therefore must not produce Python-3 floats.
- no visual geometry, original authorship, package identity, main branch or locked 1.0.4 artifact was changed.
- no RECEIVER PASS is claimed.


## Renderer numeric + weather transport audit — 2026-10-01

Status: **STATIC REVIEW PASS — RECEIVER TEST REQUIRED**

- continued the full Python 3 numeric audit across custom renderers rather than limiting it to converters.
- fixed integer-only EPG minute formatting and font fallback arithmetic in `g17ShowExtraEpg`; its description truncation ratio is now explicitly floating-point only where proportional division is intended.
- fixed `g17ShowTP` symbol-rate formatting so Python 3 does not leak a decimal `.0` into the transponder text.
- fixed `g17MetrixHDRunningText` line-height/page geometry arithmetic to preserve the original Python 2 integer-coordinate behavior on Python 3.
- reviewed Open-Meteo and classic WeatherScreen HTTP bytes/text handling. Open-Meteo explicitly decodes responses; the classic current Python 3 path decodes the cached current-weather response before text-file output, while JSON forecast parsing accepts its bytes response. No speculative transport rewrite was made.
- floating-point divisions intentionally used for scaling, astronomy, network-rate calculation, orbital decimal display and MiniTV framebuffer scaling were retained.
- no visual design, original authorship, package identity, main branch or locked 1.0.4 artifact was changed.
- no RECEIVER PASS is claimed.


## Package lifecycle + updater hardening — 2026-10-01

Status: **STATIC REVIEW PASS — RECEIVER TEST REQUIRED**

- audited package identity and lifecycle scripts. The package remains `enigma2-skin-fullhdglass17`, runtime skin path remains `/usr/share/enigma2/hd_glass17`, and the generated `/etc/enigma2/skin_user-hdg17.xml` overlay is declared as a conffile and additionally preserved/restored across upgrades.
- confirmed lifecycle scripts do not delete `/etc/enigma2/settings`, do not perform broad `rm -rf` cleanup, do not remove picon directories and do not replace the image spinner.
- confirmed updater remains raw GitHub HTTPS + SHA256 + `eConsoleAppContainer`; it does not use `Screens.Console`.
- hardened update metadata validation: package downloads are now accepted only from HTTPS URLs and only when the manifest provides an exact 64-character hexadecimal SHA256. The install path revalidates these invariants and checksum comparison is mandatory rather than optional.
- `update.json` still points to the locked 1.0.4 package and its approved SHA256; no release metadata was advanced during modernization work.
- no RECEIVER PASS is claimed.

- follow-up gate removed the final unused `Screens.Console` import from setupGlass17; command execution that remains in the plugin uses `Components.Console` where appropriate, while the Warder package updater itself remains on `eConsoleAppContainer`.


## Package URL authority correction — 2026-10-01

Status: **STATIC REVIEW PASS — RECEIVER TEST REQUIRED**

- revalidated the updater and locked 1.0.4 manifest against the repository that now owns the project: `Evolution-by-Warder/FullHDGlass-Warder-Evolution`.
- corrected the updater manifest raw URL from the obsolete `PiconHub-Warder` repository path to `Evolution-by-Warder`; transport remains raw GitHub HTTPS and the installer remains `eConsoleAppContainer`.
- corrected only the repository owner component of the locked 1.0.4 `package_url`; version `1.0.4`, package filename and approved SHA256 `9ceb1713fa237d39f13b4baf728852323086205528c5622df7def58b5812c0bd` remain unchanged.
- no stable release was created and `main` was not modified.
- no RECEIVER PASS is claimed.


## Package lifecycle final gate / test-build boundary — 2026-10-01

Status: **STATIC/PACKAGE GATE PASS — TEST PACKAGE VERSION REQUIRES EXPLICIT APPROVAL**

- package identity remains `enigma2-skin-fullhdglass17`; runtime compatibility identifiers and `/usr/share/enigma2/hd_glass17` ownership remain unchanged.
- `/etc/enigma2/skin_user-hdg17.xml` remains a conffile and is preserved across upgrades; lifecycle scripts leave `/etc/enigma2/settings`, user picon directories and image spinner ownership untouched.
- preinst/postinst/postrm were re-read from the working branch; no destructive wildcard cleanup or broad picon/spinner removal is present, and postrm exits without cleanup for package-upgrade lifecycle states.
- updater source remains raw GitHub HTTPS + mandatory 64-hex SHA256 + `eConsoleAppContainer`; no `Screens.Console` updater path was reintroduced.
- updater and `update.json` now use the authoritative `Evolution-by-Warder/FullHDGlass-Warder-Evolution` raw repository path. Locked 1.0.4 version, filename and approved SHA256 are unchanged.
- the final updater-source gate found and fixed a literal escaped-newline corruption in `Writelog()` that would have produced invalid Python source. A follow-up scan found no remaining source-level `:\\n\\t`, `;\\n\\t` or `pass\\n\\t` corruption patterns in `plugin.py`.
- global skin geometry/assets were not changed by the package-lifecycle batch; the previously completed 618/611 screen gate, seven intentional front-panel duplicate families, zero `forgroundColor` typos, zero missing internal assets and zero packaged bytecode-artifact results therefore remain applicable.
- no stable release was created, `main` was not modified and no RECEIVER PASS is claimed.
- the source tree is ready for a TEST IPK build boundary, but the locked runtime/package version remains 1.0.4. Creating a distinguishable test package requires an explicit approved test-version identifier rather than silently mutating the locked 1.0.4 identity.


## Receiver TEST build 1 — 2026-10-01

Status: **BUILD-READY — TEST VERSION 1.0.5-test1 — RECEIVER PASS NOT CLAIMED**

- explicit approval was received to create a distinguishable TEST version while keeping stable 1.0.4 locked.
- runtime test version is `1.0.5-test1`; opkg package version is `9.50+warder1.0.5-test1`.
- package identity remains `enigma2-skin-fullhdglass17`; runtime skin path/name and compatibility identifiers are unchanged.
- stable `update.json` intentionally remains on 1.0.4 and its approved SHA256; the test build is not advertised through the stable updater channel.
- added `tools/build-test-ipk.sh`, which refuses to build unless both package and runtime versions contain `-test`, refuses unexpected package identity, rejects packaged Python bytecode artifacts, stages lifecycle metadata, builds with `opkg-build` or `dpkg-deb`, and emits a SHA256 sidecar.
- expected test artifact name: `packages/test/enigma2-skin-fullhdglass17-warder-evolution_1.0.5-test1_all.ipk`.
- this checkpoint is build-ready only. A generated IPK must still pass archive/control/payload inspection before receiver installation, and only the physical GigaBlue Quad 4K Pro / OpenATV 8.x test can establish RECEIVER PASS.
