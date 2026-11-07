# PR #51 – Enigma2 receiver acceptance matrix
Status: **NOT EXECUTED**. This is a manual test protocol, not evidence of passing tests.
Branch: `work/channelselection-primetime-overlap-20261107`.

## Preconditions
- Install a clearly labelled test build on a non-production receiver or backup image.
- Record receiver model, Enigma2 image and version, display resolution, skin variant, selected background, user font-size setting and installed test commit.
- Back up settings before testing. Never replace the approved base `skin.xml`.
- Leave Prime Time OFF first (default); verify current channel-list presentation is unchanged.
- Repeat key checks on both OpenATV and OpenPLi. GitHub Actions do **not** substitute for a receiver test.

## Layout coverage
**58 of 58 ChannelSelection definitions:** base `ChannelSelection` and each `ChannelSelection-N` definition present in the working tree. Enumerate these directly from `hdg17Screens.xml` at test time; do not infer layout names from contiguous numbering.

For **every** layout:
1. Record screenshot with Prime Time **OFF** on selected row and an unselected row.
2. Use long EPG titles containing spaces, very long uninterrupted words and accented Unicode; also test remaining-time labels at their widest.
3. Test enlarged user font settings without changing those settings in source, and empty/partial/full progress.
4. Enable Prime Time at 20:25 and confirm the existing event region is reused (not an added panel); check picons, logos and progress bars are not covered.
5. Select a different channel, then a marker, directory and a channel with no EPG. Confirm no stale text/animation or wrong-channel event survives.
6. Disable Prime Time again and verify the original EPG display returns.
7. Record **PASS / FAIL / NOT TESTED**, screenshot and observed defect; any failed required check blocks release.

## Time and locale
- Before 20:25, exactly 20:25:00 and after 20:25:00, confirm today's vs. following day's lookup.
- Repeat with another user-selected clock time.
- Check local time-zone handling and both DST transition days where applicable.
- Confirm an event covering the requested instant is shown; a missing event must be reported as unavailable, never as an invented event.

## Other menu families — separate smoke tests
| Menu family | Scope | Required checks | State |
| --- | --- | --- | --- |
| EPGSelection (and EPGSelectionMulti) | Separate EPG-list geometry | Long multilingual titles, selected row, large fonts, progress/text collision | NOT TESTED |
| MovieSelection (and MovieSelectionSP) | Native movie list | Long recording names, dates/durations, selected row | NOT TESTED |
| EventView | Event detail text | Extended description, line wrapping, scrolling, large fonts | NOT TESTED |
| ChannelSelectionRadio | Radio-specific layout | Long station names, programme titles, icons and empty EPG | NOT TESTED |

Do **not** copy `fieldMargins=26` blindly to unrelated list widgets. Fix only independently reproduced overlaps.

## Compatibility and release gate
- GitHub Actions must finish and any failing jobs must be triaged, including the known native Positioner animation regression in OpenATV 8.0-next.
- Test against all **three approved backgrounds** and check that no graphics have been silently replaced.
- Actual receiver test evidence required for OpenATV and OpenPLi, including a layout with enlarged fonts.
- Final review confirms the approved base `skin.xml` remains byte-identical to `main`.
- Draft PR remains unmerged; **no production IPK** without explicit owner approval.
