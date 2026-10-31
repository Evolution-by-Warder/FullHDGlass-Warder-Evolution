# Pending next FullHDGlass release

Prepared together on branch `fix/settings-section-titles-20261031`. Merge that pending source into the next authorized release before publishing.

**Hold publication.** The owner requested preparing these changes together and waiting for further observations. Do not create a new version, IPK or updater activation until requested. Production remains 1.0.47.

## DAB slideshow and song cover

- Native DAB/DAB+ only: broadcast slideshow above a separate current-song cover.
- Both slots share the original horizontal centre and preserve image aspect. Slideshow slot: (316,146,420,340); cover slot: (316,506,420,340).
- The existing one-window geometry and cover behavior remain for satellite and IPTV radio.
- Slideshow consumes the current native broadcast picture and only decodes changed images. It performs no internet lookups or cache writes. The existing song-cover lookup remains a single instance with its original identity, caching and retry policy.
- If no broadcast slide is available, its window stays hidden; cover lookup continues. If a cover is unavailable, its existing approved placeholder is used.
- Station/mode changes and disposal reject stale size/decode callbacks.
- Radio header, lyrics, picons, equalizer and approved graphics remain intact.

## Common settings header

- Removed section names below the date, such as História, from eight settings layouts and the three shared dialogs.
- Kept the logo, date, clock, version, controller titles, actions and body content.
- The separate radio-mode caption remains unchanged.

## Verification

- DAB dual artwork: 11 controller/layout checks.
- Existing lyrics/artwork: 117 checks; stream metadata: 77 checks.
- OpenATV screen compatibility: 8 checks; History/radio title: 8 checks; keyboard: 6 checks.
- Runtime cleanup: 9 checks; runtime safety guard passed.
- Header cleanup was already validated with 22 settings checks and 5 shared-dialog checks.
- Exact reviewed XML additions reverse to the unchanged original graphics/layout baseline. Source syntax remains Python 3.9 compatible.
- No physical receiver test of these pending changes is claimed. No IPK was built or published.

Public release description: V DAB režime sa obrázky stanice a obal skladby zobrazujú samostatne. Čistejšia hlavička nastavení bez názvov rubrík pod dátumom.
