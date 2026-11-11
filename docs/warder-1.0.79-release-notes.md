# FullHDGlass – Warder Evolution 1.0.79

Stable update following the receiver-tested 1.0.78 improvements.

## Picons and downloads
- Simplified PATHS settings: optional read-only user channel-picon directory; Warder downloads remain in the skin-owned hdg17_files directories.
- Fixed provider and satellite logo downloads: verified installation into piconProv and piconSat, with per-set PNG counts.
- Preserved existing user collections and original HDGlass17 settings during updates.
- Simplified satellite-position selector: OK toggles a position, green confirms selection.
- Restarts the Enigma2 GUI three seconds after changing and immediately saving the user-picon source.

## Weather and interface
- Open-Meteo descriptions now use the Enigma2 language catalogue in current and forecast displays.
- Unified uppercase PATHS main-menu heading.
- Improved in-window download progress with verified success and failure reporting.

Validated on GigaBlue Quad 4K Pro with user feedback for channel, provider, satellite and CAM picons, custom channel picons, Slovak weather, GUI restart, and legacy hdg17.conf import.

**Note:** This release retains the existing installation and data directory scheme. Uninstall is different from upgrade; back up personal settings and picons before removing the package.
