# FullHDGlass17 Warder Evolution

## 1.0.5-test216
- Pin the corrected Canal+ channel manifest to an immutable commit, avoiding stale branch cache responses.

## 1.0.5-test214
- Pinned Canal+ provider archives to the verified immutable commit so downloads cannot use a stale branch cache.

## 1.0.5-test213
- Compiled the existing Slovak and Czech Picon menu translations into the installed message catalogs.
- Re-uploaded complete black and white Canal+ provider bundles after verifying their remote byte counts and SHA-256 hashes.

## 1.0.5-test212
- Restored the original resolution menu: 50 x 30, 220 x 132, 400 x 240 and 710 x 682.
- Restored the original resolution help text and kept Canal+ SK/CZ as channel selector entries.
- Preserved the original three provider and satellite logo choices and localized menu labels.
- Added the Canal+ SK and Canal+ CZ provider logos as combined packages for each provider logo style.

## 1.0.5-test211
- Replaced the combined 23.5E Skylink selector with separate Canal+ SK and Canal+ CZ entries.
- Added Canal+ channel picons and selector icons from approved artwork.

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
- Keeps package identity `enigma2-skin-fullhdglass17` so existing installations are upgraded in place and remain registered in the system package manager.
- Keeps `/usr/share/enigma2/hd_glass17/skin.xml` as the standard Enigma2 skin entry, so the skin remains available in Skin Setup / appearance selection.
- Preserves `/etc/enigma2/settings`, the active `/etc/enigma2/skin_user.xml`, and the generated FullHDGlass17 user overlay during upgrades.
- Marks `/etc/enigma2/skin_user-hdg17.xml` as a configuration file and prevents removal cleanup from running during package upgrades.

## 1.0.5-test106
- Corrected the Radio OpenWebif /grab hook to the receiver-proven GrabScreenshot.render class on OpenWebif 2.4.0-git348.
- Preserved native TV/explicit screenshot modes and isolated Radio All compositing/fallback behavior.
