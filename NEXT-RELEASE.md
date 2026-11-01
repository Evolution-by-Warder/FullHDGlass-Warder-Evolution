# FullHDGlass 1.0.57 — owner approval — 1 November 2026

The owner confirmed test3 works and explicitly authorized a normal public release and activation in updates. Ship the approved font, compact installer and VideoEnhancementSetup repairs as 1.0.57 (native upgrade ordering after test builds).

The five-entry History request is included for FullHDGlass: two compact description rows per version preserve the existing 740-pixel list. Full source history is retained; processing/installation logs are not limited. PiconHub and GSU remain pending for their next functional releases.

The records below are historical and superseded where a later release or owner approval is documented.

---

# Pending owner request — History: five entries — 1 November 2026

At the next normal release, expand the displayed History from the latest 4 entries to the latest 5 entries in all three projects: FullHDGlass, PiconHub and GSU. This instruction supersedes the earlier four-entry limit recorded below.

Keep the existing compact layout, version/date headings, separators, localization and brief user-facing descriptions. Preserve the complete source history; only the number of entries shown in the UI changes. Do not apply the limit to installation or processing output.

Record this as pending work only. Do not create a new IPK, bump a version or change update feeds solely for this request. Include and verify five visible entries when preparing the next authorized release.

---

# Current receiver repair status — 31 October 2026

The recorded functional repairs and four-entry History presentation are included in the verified 1.0.51 repair package. See the receiver-repair documentation and public verification report. Published repair IPKs are immutable; stable update feeds remain unchanged. A final physical receiver retest of this package is pending.

The following entries are preserved as historical investigation and approval records; their earlier IPK holds do not override the owner's later instruction to combine and repair the recorded issues.

---

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

## Spinner receiver test available

Owner asked how to test on their receiver. Isolated **1.0.50-test1** is now published as prerelease `spinner-choice-1.0.50-test1`, with exactly one short IPK and its checksum. Source: `dd233e61d31050949bcd5fb2c4768dc411524f5a`. Production and native TEST updater manifests remain 1.0.49; the legacy bridge remains 1.0.18. New spinner/menu receiver confirmation is pending. See `reports/spinner-choice-test-release-20261031.json`.


## Separate spinner preview library — owner hold on IPKs

The owner authorized preparing all source collections, then clarified that each spinner must have its own named directory and be reviewed individually. They explicitly requested no new IPK yet.

Prepared branch: `feature/spinner-preview-library-20261031`, frozen preview-assets commit `0ea1295bb32ffa78fb43b8f29fe2b4c0b86197c2`. It contains 154 directories: 12 licensed SpinKit designs plus 83 sequences from the supplied TechKings ZIP, 58 from Spinner Pack 2.1 and one separate football sequence. All 1,988 native PNG frames, individual GIFs, source metadata and original archives were checked. A downloaded final ZIP was checked against every frame checksum. The root HTML gallery shows one spinner at a time. Source files and derived assets remain outside the install payload. See `reports/spinner-preview-library-20261031.json`.

The owner also approved the blue bakussa derivative with trailing 17 removed and the original caption centered. That review variant is preserved at `fb405579a9ba145a22a371790642452d3133c0ec`; the already published receiver-test IPK remains unchanged. Before shipping updated bakussa frames, handle previously installed bakussa hashes during private-folder upgrade cleanup (including the old twenty-frame tail) and test migration to the new artwork. Do not replace bytes in an already published IPK.

Production and native TEST feeds remain 1.0.49. Pending compound-artist recognition stays deferred for the next authorized production release. No further Trezor changes were made for the preview collection.

## Owner review complete — duplicates removed

Owner finished reviewing the complete spinner library and requested removing duplicates. Original review entry 9 (Circle Fade) is removed, entry 8 (Circle) is kept, and original entry 146 (Taube) is removed as a duplicate of the installed Dove. Active collection: **152** folders / **1,958** native frames. Current cleaned assets: branch `review/spinner-library-20261031`, commit `62ef4033be67693619d5ab98d2f8266bed309dc7`. Folders, group/combined catalogues and viewing ZIPs were cleaned; remaining images and original source archives are preserved. Original review numbers stay recorded in metadata, while the finished-review gallery can use its current list positions. Policy is reapplied by generators to prevent duplicates returning.

Original review entry 31 (`019-techkings-spinner-24`) remains pending a brighter variant. The blue centered-caption bakussa derivative is already approved as noted above. No new IPK, updater change or Trezor change was authorized or made for this cleanup. See `reports/spinner-owner-review-20261031.json`.

## Spinner quality audit before integration

The owner requested checking quality and sizes of every reviewed spinner. Audit commit: `63f150879ec69c2252fa6d81448eaeb66c5db26c` on `audit/spinner-quality-20261031`; full results are in `reports/spinner-quality-20261031/README.md` and `audit.json` on that branch. See the local summary `reports/spinner-quality-summary-20261031.json`.

All 152 candidates / 1,958 RGBA PNG frames and 152 GIF durations/loops passed integrity checks. Reconstructed all 1,779 community frames from the three unchanged original archives and found no pixel differences. Native PNG total: 11,793,706 bytes (11.25 MiB). The largest decoded frame set is 56 × 43,264 bytes = 2,422,784 bytes before auxiliary graphics buffers and overhead; no receiver CPU measurement is claimed.

Quality is uneven: 18 small raster sources, 12 sets with opaque source backgrounds, 7 low-contrast dark-background candidates. Original review 31 needs its already requested brighter variant. Entries 113 (Katze2) and 122 (PapierFlieger) are too small after fitting the original movement canvas; review scale and movement together, not per-frame cropping. Entry 24 intentionally approaches from tiny to large. Entry 11 reaches the canvas border in five frames; add fitting reserve before integration. Preserve deliberate held-frame timing in 107/109/115/121/137/138/147. Full-background artwork such as Love must not have its background blindly erased.

This is an audit and a pending work record only. No candidate was removed or redrawn, no IPK was built, no feeds/runtime changed, and Trezor remains untouched. The owner's IPK hold still applies.

## User receiver report — OpenATV 7.6 / VU+ Uno 4K SE

On 31 October the owner relayed a successful second-receiver report on OpenATV 7.6: GSU directly replaced its previous version; FullHDGlass and PiconHub worked after Telnet reinstallation, while their first installation/upgrade attempt had not completed the expected replacement. The original PiconHub predecessor was Chocholousek. Exact installed versions and transaction logs were not supplied. Record this as user-reported operation after recovery and a migration investigation item, not a proven root cause or a blanket compatibility guarantee. See `reports/openatv-76-user-receiver-20261031.json`. No IPK or runtime changes were made for this record.

## Installation repair and spinner choice must ship together

Owner instruction on 31 October: include the spinners when the installation repair is released; do not issue a skin release containing only the installer repair.

Prepared installer source is on `fix/install-transition-20261031`. The verified opkg 0.10.0 / libsolv 0.7.40 reproduction and a guarded direct replacement of the exact supplied 9.50-r12.2 are documented in `docs/INSTALL-TRANSITION-20261031.md`; transaction evidence is in `reports/install-transition-20261031/`. Unknown legacy removal scripts remain protected. Postinst and updater now verify critical payload, and the updater also requires a fully installed package state after opkg exits.

Release checklist: combine this repair with the already prepared native spinner selector and approved blue centered-caption bakussa. Complete the approved online spinner design: one separately verified ZIP per spinner, a small extendable catalog, static thumbnails with name/author in the selection list, and downloading only the selected animation. No animated previews are requested. Keep the bundled Dove usable offline, bound transient thumbnail storage, retain the existing native playback path, and preserve the user's cancel/save semantics. Apply the earlier approved duplicate exclusions and pending artwork checks. The online spinner implementation is not yet complete.

The deferred shared radio identity fix listed above also remains part of the next authorized production release. Perform the required combined receiver/package checks before publication. Current production IPK and feeds remain unchanged; no new product IPK was built or issued for this investigation. Public release notes should use only a general description such as improved installation reliability and a choice of waiting animations.

Prepared source commit: `680bab699ff934b92b891a771ed465ce8d71e53c`. Related skin source: `680bab699ff934b92b891a771ed465ce8d71e53c`; related PiconHub source: `487e46aef74323cb81ce7af554a90dd74cf36468`.
