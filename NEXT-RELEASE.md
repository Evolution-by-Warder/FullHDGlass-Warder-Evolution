# Pending next FullHDGlass release

## Shared radio metadata recognition

Prepared on branch `fix/radio-compound-artist-20261031`. Merge that pending source into the next authorized release before publishing.

**Do not create a new version or IPK solely for this change.** The owner explicitly requested holding publication on 31 October 2026. Production remains 1.0.49; updater manifests and package controls remain unchanged.

A receiver supplied `KARMEN PAL - BALAZ-Pustam ta`. The old parser split it into `KARMEN PAL` and `BALAZ-Pustam ta`; the fix recognizes the verified complete artist Karmen Pál-Baláž and the separate title Pustam ta. It applies to both full stream titles and already separated native artist/title tags.

The shared helper is used by cover and lyrics lookup. Exact recording identity, guest credits and Live/Remix suffixes remain enforced. Unknown hyphenated names retain the old conservative parsing rules. The malformed negative cache is left intact and no longer blocks the repaired identity.

Validation: 121 lyrics/artwork checks and 79 stream metadata checks passed. Live lookup from the original malformed pair returned a verified 600×600 cover and 1,259 characters of original lyrics from Hudba.sk. Only metadata, counts and text hashes are stored; no lyrics are published. Physical receiver confirmation of the pending fix is not claimed.

Public release description: Presnejšie rozpoznávanie zložených mien interpretov pri vyhľadávaní obalov a textov piesní.

GSU/PiconHub History formatting remains deferred to their next functional changes in their own repositories.

Pending source commit: `95990e2dd78a29a1070b48dab28517342754c7f5`.

## Legacy r12.2 installation report — investigate before migration

Owner supplied the actual `enigma2-skin-fullhdglass17_9.50-r12.2_all.ipk` after a Vu+ Uno 4K SE / OpenATV 8.0.1 user reported loss of the skin selection entry after a direct update. The supplied legacy removal hook preserves `upgrade` and `disappear`, but `remove` deletes the skin XML, plugin and g17 components and returns exit code 0. This behavior was reproduced only in isolated rewritten temporary roots.

Current replacement metadata also matches legacy 9.50-r12.2, while the 1.0.18 bridge is a downgrade from that version. Review actual opkg transaction ordering and migration protection before recommending a direct replacement. Do not claim the exact receiver root cause without installed package status and file checks.

Await read-only receiver outputs: `opkg --version`; `opkg status enigma2-skin-fullhdglass17`; `opkg status enigma2-plugin-skins-fullhdglass-warder-evolution`; `ls -l /usr/share/enigma2/hd_glass17/skin.xml`.

Evidence: `reports/r12-upgrade-analysis-20261031.json`. No runtime/package/feed changes or new IPK were made for this investigation. The pending compound-artist fix above remains deferred.

### Receiver status follow-up

Screenshot `hd glass.jpg` shows opkg 0.10.0 / libsolv 0.7.40 and native FullHDGlass **1.0.47-1** in **install ok half-installed** state. The legacy status query printed nothing. The final skin.xml `ls` command is visible at the prompt without an execution result, so file existence remains unconfirmed. Installation incompleteness is confirmed; the original failure cause and exact transaction stage are still unknown. Request the completed `ls` and `df -h / /tmp` output before further diagnosis. See `reports/r12-upgrade-followup-20261031.json`.

### Receiver recovery outcome

Later screenshots confirmed missing skin.xml, about 2.5 GB available on root
and 352 MB in /tmp. A controlled reinstall/upgrade to 1.0.49 completed its
configuration successfully and reported that existing settings were preserved.
After GUI restart the forum user confirmed that the skin was available again.
This establishes recovery on that receiver, not the original failure cause.

## Spinner choice

Prepared on `feature/spinner-choice-20261031`. The owner requested two menu
entries, exactly **Holubica** and **HDGlass - bakussa**, and easy future extension.
Credit the supplied animation to **bakussa** by name only.

The existing approved dove remains the default. A source registry generates
the runtime catalog and native PNG sets; later themes need no menu/controller
rewrite. The contributed twenty-frame animation is proportionally prepared as
104×104 truecolor RGBA, below the reviewed native allocation threshold. Originals
are preserved in the canonical auxiliary-asset structure, outside Releases.

Selection uses the skin's own spinner folder after save and GUI restart. Cancel
does not apply it. Install hooks restore the saved choice after package updates.
System/user spinner paths remain untouched and retain their native precedence.
No additional playback timer, drawing worker or diagnostic logs are introduced.

See `docs/SPINNERS.md` and `reports/spinner-choice-20261031.json` for extension
instructions, checks and receiver-test limits. Do not publish a replacement
1.0.49 IPK with these changed bytes. The current public package/feed is unchanged;
include the pending radio identity fix when a new release is authorized.

Prepared spinner source commit: `5b62d9087a82bc50e9994b33e0b110609ee85a10`.
