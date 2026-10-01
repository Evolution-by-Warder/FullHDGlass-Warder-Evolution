# FullHDGlass17 Warder Evolution

## 1.0

- Established the FullHDGlass17 Warder Evolution release line.
- Python 3 compatibility cleanup and syntax fixes.
- Safer package installation/removal scripts.
- Restored missing menu icons.
- Removed obsolete legacy duplicate files and unsafe global HTTPS bypass.
- Reworked Enhanced Weather to use Open-Meteo JSON services.
- Removed the obsolete MSN weather fallback and modernized weather HTTPS access.
- Replaced the original FullHDGlass17 FTP self-updater with a GitHub-based Warder updater.
- Removed the legacy rotating PayPal donation banner from the setup header; original author credits remain unchanged.
- Added HTTPS package download, semantic version comparison and optional SHA256 verification.

## 1.0 final asset migration
- Replaced legacy FTP downloads for recovered FullHDGlass17 assets with HTTPS downloads from the Warder GitHub repository.
- Added SHA-256 verification for every Warder asset before extraction.
- Added a GitHub-hosted download catalog so asset URLs can be maintained without rebuilding the skin package.
- Removed embedded legacy FTP credentials from the plugin.
- Preserved external satellite/channel picon selection via picon.cz where the original FTP snapshot contained no equivalent package.

## Upgrade/install integration

- Keeps the package identity `enigma2-skin-fullhdglass17` so existing installations are upgraded in place and remain registered in the system package manager.
- Keeps `/usr/share/enigma2/hd_glass17/skin.xml` as the standard Enigma2 skin entry, so the skin remains available in Skin Setup / appearance selection.
- Preserves `/etc/enigma2/settings`, the active `/etc/enigma2/skin_user.xml`, and the generated FullHDGlass17 user overlay during upgrades.
- Marks `/etc/enigma2/skin_user-hdg17.xml` as a configuration file and prevents removal cleanup from running during package upgrades.
