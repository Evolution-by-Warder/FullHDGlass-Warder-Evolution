# FullHDGlass – Warder Evolution 1.0.72

Stable release based on receiver-approved TEST61 (2026-11-08) and previous production version 1.0.71.

## Improvements and fixes

1. Corrected missing video-resolution information on selected IPTV streams.
2. Improved handling of IPTV services with incomplete video metadata.
3. Added an alternative decoder-resolution read when standard metadata is unavailable.
4. Preserved the standard resolution source whenever it returns valid values.
5. Displayed actual decoded video dimensions without hard-coded resolution presets.
6. Preserved progressive/interlaced indicators when Enigma2 supplies them.
7. Kept DVB resolution processing on its original code path.
8. Corrected CAID line text overlap with colored indicators in InfoBar 76.
9. Reserved a dedicated 1020-pixel text area for CAID information.
10. Added horizontal scrolling for lengthy CAID information.
11. Kept complete CAID, SID and VPID details accessible during scrolling.
12. Improved continuity of long-text scrolling with wraparound repetition.
13. Removed the long empty interval at the end of the previous scrolling cycle.
14. Adjusted scrolling speed to the receiver-approved 220 ms step interval.
15. Limited CAID layout and scrolling changes to InfoBar 76.
16. Added localized update descriptions based on the Enigma2 system language, with English fallback.
17. Preserved earlier EPG, Prime Time and safe 9.50 migration features without modifying their logic.

The entries above describe individual technical aspects of the receiver-approved IPTV and InfoBar 76 fixes, **not 17 separate bug reports**.

## Receiver validation
GigaBlue Quad 4K Pro, OpenATV, user screenshots / observations on 2026-11-08:
- IPTV 5336, 5643, 4213 and 4520: video size displayed correctly (1920x1080p on the tested streams).
- DVB-S2 Jednotka HD 23.5 E: video size displayed correctly (1920x1080i on initial testing; later screenshots 1920x1080p depending on the decoded source).
- Movie player: non-standard 628x480 resolution displayed.
- InfoBar 76 CAID badges no longer overlap the line; TEST61 scroll speed explicitly approved by the receiver tester.
Only the sampled receiver/services are validated; other images and stream formats are not claimed tested.

## Installation
Transfer `enigma2-plugin-skins-fullhdglass_1.0.72_all.ipk` to `/tmp`, run:

```sh
opkg install /tmp/enigma2-plugin-skins-fullhdglass_1.0.72_all.ipk
```

Restart GUI after successful installation. Do not force-remove the original FullHDGlass package; saved user settings should be preserved.

Package ID: `enigma2-plugin-skins-fullhdglass-warder-evolution`  
Version: `1.0.72-1`
