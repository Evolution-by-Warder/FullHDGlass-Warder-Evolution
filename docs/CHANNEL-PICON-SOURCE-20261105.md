# FullHDGlass 1.0.69 — channel-list picon source

The 1.0.68 update applied the separate 50x30 lookup to every FullHDGlass user.
That changed existing image-controlled picon selection for users with a
different or older small set. The owner requested an immediate correction.

## Setting and default

Open **Plugins → FullHDGlass Warder Evolution → CHANNEL SELECTION**
(Slovak **VÝBER KANÁLOV**). **Channel-list picon source** is the second row,
immediately after **Type**. Change it with left/right and save.

| Choice | Behavior |
| --- | --- |
| System setting — default | The image's original native lookup, as before 1.0.68 |
| Prefer 50x30 | Skin `picon_50x30`, then `picon` per missing service, then native lookup |

Existing installations do not have the new `par231` preference, so an upgrade
defaults to **system**. The updater does not infer an opt-in from existing small
folders or overwrite image picon paths/settings. A deliberately saved **mini**
choice persists through later upgrades. The native default also restores the
previous large-preview lookup; the shared large-preview fallback from 1.0.68
is retained with the explicit mini mode.

The existing numeric registry now appends entry 231 without moving entries
1–230. Native save/cancel and `hdg17.conf` backup/restore include the choice.
Changing it participates in the normal save/restart prompt. Menu labels,
choices and help are translated into the ten supported UI languages.

## Validation

The regression suite covers both source modes with real temporary folders,
existing native callbacks and template painters, selected previews, an absent
preference callback, mode changes and per-service fallback. The settings suite
executes the actual registry declaration, menu branch, save/cancel and backup
restore callbacks. The exact setting statements are scope-bound in the audit
ledger; the original controller fingerprint remains enforced.

The package is built over immutable 1.0.68 and verifies that all other payload
bytes remain unchanged. The new setting tests also run against the extracted
final IPK. Physical receiver feedback for 1.0.69 is pending; the earlier user's
confirmation concerns the opt-in behavior initially shipped in 1.0.68.
