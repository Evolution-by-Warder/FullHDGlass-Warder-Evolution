# FullHDGlass – Warder Evolution 1.0.82

Stable integration release from [PR #131](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/131), based on the complete 1.0.80 source plus the tested Radio Live, unified radio screensaver and subsequent IPTV InfoBar correction.

## Skin and receiver behavior
- Retains all twelve previously integrated and approved skin fixes, including FastScan EPG/name overlap, OpenATV 8.1 GLES performance policy, channel-list fullscreen, EMC/EPG spacing, settings/main-menu integration and date/weather widgets.
- Preserves approved SAT picon catalogues, Canal+ SK/CZ precedence, existing menu graphics and 24-frame spinner options.
- Repairs the combined `g17ServiceNum / NumberAndName` converter used by InfoBar 76 and other layouts: an IPTV bouquet-number or platform lookup exception must no longer remove the playing service name. A missing decoder name can fall back to the service-reference name. The standard native `ServiceName / Name` converter and DVB prefix behavior remain unchanged.
- Keeps user settings, downloaded assets, external PATHS folders, bouquets and internal flash protection under the existing guarded package migration.

## Radio
- Unified OLED-style radio screensaver for native DVB radio, DAB/DAB+, IPTV radio and Warder Radio Live, with selectable 0/10/20/30/60-second activation; native RDS/RT+, original station picons and cover artwork supported where available.
- Preserves the Radio Live country/bouquet and logo architecture, including safe local activation, verified country ZIP downloads to external storage and original selected-country logos. Source-feed availability and actual logos depend on independently verified upstream packages; do not promise all original station logos are available.
- Radio-specific packaging does not place the full 224-country catalogue in internal flash.

## Validation and limits
- Integration, OpenATV 8.0/8.0-next/master, OpenPLi 9.2/develop, GLES/EPG, Radio Live, country switching, storage, native screen compatibility, Prime Time and unified saver automated jobs all passed for the merged candidate.
- TEST153 was built successfully and exercised with offline IPTV converter regression tests. **The exact InfoBar 76 IPTV correction has not yet been confirmed on the reporting VU+ Duo 4K SE**, and CI cannot replace on-device testing of every layout/image. Do not claim otherwise.
- Normal `1.0.82-1` version deliberately exceeds `1.0.81-test153-1` to support native upgrades from the final test package.

Install via the verified FullHDGlass updater or official GitHub Release. Restart Enigma2 GUI after installation. Back up custom settings before major image changes or manual package removal.
