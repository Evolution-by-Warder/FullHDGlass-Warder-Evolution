# FullHDGlass – Warder Evolution 1.0.83

Stable radio-country production integration release, continuing 1.0.82 without altering its approved skin art, SAT picons, layouts, IPTV InfoBar 76 converter or unified OLED radio screensaver.

## Warder Radio Live: full public 224-country source
- Switches the radio country source from the old isolated TEST feed to the official stable `Radio-Warder-Evolution/main/assets/radio-country/latest.json`.
- The official immutable country data release `radio-country-20261122` contains **224 countries, 48,219 station services, 40,837 original station PNG logos**. Each of its **225 assets** was checked against the published byte counts and SHA-256 metadata before the production feed was made visible.
- Downloads a small world bouquet/catalogue ZIP (~6.66 MB) only onto the external skin-managed `hdg17_files/radio-world` directory, verifies its checksum and safely installs it as an owned snapshot; no full-world original-logo payload is installed to internal flash.
- Downloads only the active selected country's station-logo ZIP to the configured external `hdg17_files/picon/radio/CC`, verifies SHA-256 and station/service identities, and prevents a late download for an old country from overwriting the user's current selection.
- The existing background 14-day refresh cadence, offline country activation and guarded preservation of user/custom/TV/SAT picons remain unchanged.

## Compatibility and storage
- Keeps all approved 1.0.82 graphics, dynamic DVB/DAB/IPTV radio screensaver, date/weather, EPG/GLES policy and protected user settings.
- World and country original ZIPs are NOT part of the IPK. Radio data syncing requires a writable external PATHS storage destination; if none is configured, the updater safely skips the large data copy rather than filling internal flash.
- FullHDGlass 1.0.83-1 normally upgrades from stable 1.0.82-1 and TEST153.
- Existing on-receiver limitations from 1.0.82 (including the unconfirmed receiver-specific IPTV InfoBar 76 report) are not newly claimed to be fixed or physically verified.

Install through the verified FullHDGlass updater or the official `1.0.83` IPK. Restart Enigma2 after updating.
