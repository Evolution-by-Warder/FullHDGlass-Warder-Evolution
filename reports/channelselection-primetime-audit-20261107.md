# Channel Selection / EPG / Movie list overlap audit – 7 Nov 2026

Source: FullHDGlass-Warder-Evolution, working branch `work/channelselection-primetime-overlap-20261107`. Static inspection, **not** a receiver rendering test.

| Screen family | Screen definitions | `picServiceEventProgressbar` service-list entries | Separate `render="Progress"` widgets | Resolution |
| --- | ---: | ---: | ---: | --- |
| ChannelSelection, including default | 58 | 58 | 38 | Text/progress field margin candidate in 57 templates; base handled by generated runtime skin; pending receiver tests |
| EPGSelection | 10 | 0 | 0 | Uses different Enigma2 EPG list geometry; must test separately instead of blindly applying ChannelSelection patch |
| MovieSelection | 4 | 0 | 0 | Uses different native list; no ChannelSelection-style progress attribute; test long titles separately |
| EventView | 3 | 0 | 0 | No ChannelSelection progress attribute; test long event descriptions separately |
| ChannelSelectionRadio | 1 | 0 | 0 | No equivalent progress attribute in inspected XML; separate verification |

EPGSelectionMulti, MovieSelectionSP, ChannelSelection_summary and other specialized views were also identified. Do **not** infer they are fixed from the ChannelSelection count.

## Prime Time integration

`g17ShowExtraEpg` reused in 24 ChannelSelection variants (including base); `g17ShowExtEpg` in 21. The last 13 variants now use a gated original EPG text cell and an identically positioned `WarderPrimeTime` label: `ChannelSelection-18, -14, -13, -12, -11, -10, -9, -2, -3, -4, -6, -8, -1`. **All 58/58 have source-level candidate display paths.** The last 13 are checked by `tools/test_warder_primetime_placements.py`. This is not proof of correct live painting.

The default is OFF and the time is user-configurable, initialized to 20:25. The 45 existing-renderer paths insert one row only when enabled, borrowing an existing EPG row; the other 13 reuse an original EPG cell by hiding its old label only while Prime Time is enabled. Receiver behavior remains unverified.

## Acceptance checks before release

- Long EPG names including no-space Unicode strings, extreme remaining-time widths and selected/unselected rows
- Large user-configured fonts, inherited font sizes, progress bar at empty/partial/full, multiple video resolutions
- All 58 ChannelSelection layouts, plus a separate smoke test of EPGSelection/MovieSelection/EventView/Radio
- Prime Time selected service update, no EPG, day rollover and local daylight-saving transitions
- OpenATV 8.0 / 8.0-next / master and OpenPLi; test on actual receiver, in addition to GitHub CI
- Preserve approved base `skin.xml`, all user settings, existing channel-list decorations and graphical assets

No production merge or IPK publication is authorized as part of this working branch.
