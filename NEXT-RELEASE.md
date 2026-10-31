# Pending next FullHDGlass release

## Common settings header

Owner requested removing the redundant section names below the date (for example História) on 31 October 2026. The source layouts and their generator already include the change on branch `fix/settings-section-titles-20261031`. Merge that pending branch into the next authorized release source before publishing.

**Do not publish a new version or IPK solely for this change.** The owner explicitly asked to wait while looking for further improvements. Include it with the next authorized release.

- Removed the section-title label from eight settings layouts and the three shared message/choice/input dialogs.
- Preserved the logo, date, clock, version, screen/controller titles, actions and body content.
- The separate radio-mode caption remains unchanged.
- Production stays at 1.0.47; installed packages and updater manifests remain unchanged.

Public release description: Čistejšia hlavička obrazoviek nastavení bez názvov rubrík pod dátumom.

Pending source commit: `871f7f177f618b9c4e62ee59d77356c723a2c3b3`.

Validation: 22 settings layout/controller checks, 5 shared glass/dialog checks and 8 History/radio checks passed. Version files, package controls, release notes and all update feeds remain byte-identical to production 1.0.47. No IPK was built or published for this pending change.
