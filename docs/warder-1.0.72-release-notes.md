# FullHDGlass – Warder Evolution 1.0.72

Stable release based on receiver-approved TEST61 (2026-11-08) and previous production version 1.0.71.

## Approved fixes
- **IPTV resolution:** if Enigma2 service width or height metadata is temporarily unavailable, use the active decoder resolution as a fallback. Keep the original DVB path and display genuine dimensions without fixed presets.
- **InfoBar 76 CAID:** reserve 1020 px for the CAID information row so it does not overlap the colored indicators.
- **CAID scrolling:** display all CAID, SID and VPID data in a continuous wraparound marquee when it exceeds the available width, with a short separator and a gently accelerated 220 ms interval. Other InfoBars retain their behavior.
- Keep the existing TEST77 Prime Time/EPG improvements and original settings unchanged.
- Keep the safe migration from original FullHDGlass 9.50 family delivered in v1.0.71.

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
