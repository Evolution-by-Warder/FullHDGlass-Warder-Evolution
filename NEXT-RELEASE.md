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
