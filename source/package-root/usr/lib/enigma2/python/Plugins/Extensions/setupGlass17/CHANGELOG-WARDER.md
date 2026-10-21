## 1.0.11

- Replaced seven black channel picons in both Canal+ SK and CZ with the exact approved PNGs from the full 23.5E package: Canal+ Action, Film Europe HD, Sport1 HD, Sport2 HD, Canal+ Sport 2, Cartoon Network and TV Lux HD.
- Added the two missing SK HD identities; black packages contain SK 228 and CZ 231 PNGs.

## 1.0.10

- Invalidate obsolete plugin bytecode during upgrades and derive Python payload timestamps from their source bytes, preventing stale catalogue imports after GUI restart.
- Display the actual package failure reason in the download result.
- Verified real 23.5E black downloads and selective replacement of Jednotka, Osem and Seznam picons.

## 1.0.9

- Updated the approved Televizia Osem picons in all three full 23.5E packages, including both service reference aliases.
- Pinned the skin downloader to the updated verified catalogue.

## 1.0.8

- Canal+ SK and CZ downloads now contain their complete existing FastScan PNG sets (226 and 231 per style), replacing the incomplete eight-channel bundles.
- Verified all three colour selections and replacement of existing transparent files using the actual receiver installer.

## 1.0.7

- Updated approved Seznam white and black picons in the full 23.5E packages, including both service reference aliases.
- Pinned the skin downloader to the updated verified catalogue.

# FullHDGlass17 Warder Evolution

## 1.0.6
- Release the receiver-confirmed test250 radio behavior: DVB/AAC radio, RDS, DAB and WDR.
- Keep radio backgrounds visible on the physical television and OpenWebif while InfoBar is open.
- Use an opaque black radio channel-selection background and the full approved image in its preview.
- Preserve DAB caption and equalizer transparency; resolve native DAB identity and current station picons.
- Retire temporary audio/GUI diagnostics and remove the identified probe on upgrade.
- Synchronize stable and test update manifests with the same installable release and SHA-256.

## 1.0.5-test238
- Set the radio InfoBar background directly at service start and whenever the InfoBar opens, avoiding cached visibility state.


## 1.0.5-test235
- Resolve install-time paths from the filesystem root so opkg can apply the selected InfoBar variant regardless of its working directory.

## 1.0.5-test234
- Use the precomposed radio InfoBar artwork in InfoBar-3 as well, which is the permanent InfoBar variant active on the receiver.

## 1.0.5-test233
- Apply the selected InfoBar variant during package installation so preserved old skin.xml files use the new radio background after GUI restart.

## 1.0.5-test231
- Precompose the radio background with the existing InfoBar artwork for receiver OSDs that do not blend separate OSD layers; retain the original TV artwork and service-specific switching.

## 1.0.5-test229
- Return the radio RDS screen below the InfoBar so channel navigation stays visible; show the approved radio background at the InfoBar glass layer across all InfoBar variants.
- Keep the equalizer canvas transparent and enable alpha testing for the receiver TV output.

## 1.0.5-test228
- Put the radio-only RDS screen above the InfoBar so its approved background remains visible during the InfoBar.
- Restore transparent equalizer clearing and prefer the receiver service-state marker during TV/radio transitions.

## 1.0.5-test227
- Clear the animated radio spectrum canvas transparently instead of painting an opaque black rectangle behind the bars.

## 1.0.5-test226
- Keep the radio background conditional and give InfoBar-3 a full-screen canvas so the background widget can render without covering TV services.

## 1.0.5-test225
- Add the radio background widget to InfoBar-3, the permanent Extra InfoBar variant selected by the plugin.

## 1.0.5-test224
- Drive the radio InfoBar background directly from the active service and reapply visibility whenever the InfoBar opens.

## 1.0.5-test223
- Add the radio background to every selectable full-screen InfoBar variant; the setup plugin replaces the base InfoBar with one of these variants.

## 1.0.5-test222
- Synchronize the radio InfoBar background directly at service start and read the active service in the skin converter.

## 1.0.5-test221
- Keep the approved radio background visible beneath the temporary InfoBar on radio services.

## 1.0.5-test220
- Fix executable permissions of package pre-install scripts so opkg can run upgrades.

## 1.0.5-test219
- Restore the approved full-screen radio background on the receiver OSD while keeping the OpenWebif composite path.
- Simplify the displayed skin branding to “FullHDGlass · Warder Evolution” throughout setup and radio labels.

## 1.0.5-test218
- Show the Canal+ SK and Canal+ CZ operator logos beside their separate FastScan table selectors.

## 1.0.5-test217
- Clarify that Canal+ SK and Canal+ CZ are separate selected FastScan tables.

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
