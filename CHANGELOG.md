# Changelog

## FullHDGlass Warder Evolution 1.0

- Established the Warder Evolution release line.
- Python 3 compatibility cleanup and syntax fixes.
- Safer installation and removal scripts.
- Repaired missing menu graphics.
- Removed obsolete duplicate legacy files and unsafe global HTTPS bypass.
- Reworked Enhanced Weather to use Open-Meteo JSON services.
- Removed the obsolete MSN weather fallback and modernized weather HTTPS access.
- Replaced the original FTP skin updater with the Warder GitHub update service.
- Added HTTPS package download, version comparison and SHA256 package verification.
- Migrated downloadable FullHDGlass runtime assets to the Warder GitHub asset catalog.
- Added SHA-256 verification for every downloaded Warder asset before extraction.
- Removed embedded legacy FTP credentials from the plugin.
- Removed the legacy rotating PayPal donation banner from the setup header.
- Preserved original FullHDGlass author credits; Warder identifies only the Evolution continuation and new maintenance work.
- Preserved the existing external satellite/channel picon download path for categories not supplied by the Warder asset catalog.
- Kept the package identity `enigma2-skin-fullhdglass17`, so an existing FullHDGlass installation is upgraded in place and remains registered in the system package manager.
- Kept `/usr/share/enigma2/hd_glass17/skin.xml` as the standard Enigma2 skin entry, so FullHDGlass remains available in Skin Setup / appearance selection.
- Preserved `/etc/enigma2/settings`, `/etc/enigma2/skin_user.xml`, and the generated FullHDGlass user overlay during upgrades.
- Marked `/etc/enigma2/skin_user-hdg17.xml` as a package configuration file and prevented removal cleanup from running during upgrade transitions.
