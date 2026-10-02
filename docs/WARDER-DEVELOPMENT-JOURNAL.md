# FullHDGlass17 Warder Evolution — Development Journal

> **MANDATORY STARTUP RULE:** Before making ANY project change, read this file first from branch `warder-modernization-work`, then fetch the current branch HEAD and the current versions of every file that will be modified. Update this journal in the same commit as the work. Never work from memory alone.

## Repository rules
- Working repository: `Evolution-by-Warder/FullHDGlass-Warder-Evolution`
- Working branch only: `warder-modernization-work`
- `main` is immutable/TABU. No merge to main unless the maintainer explicitly changes this rule.
- Never force-push or rebase.
- Preserve original FullHDGlass17 identity/character and existing compatibility names.
- Do not weaken unrelated regression guards.
- Physical receiver PASS is recorded only after the maintainer tests it on hardware.

## Target state — GraphicalEPGPIG
Approved geometry/functionality; do not redesign while working on Program Info:
- fullscreen FullHDGlass graphical EPG
- programme preview/detail area above guide
- 15 rows
- narrow picon-only station rail; no station names
- EPG grid immediately after picons
- current programme green, future dark
- current-time line and selection retained
- RED opens Warder PROGRAM INFO
- GREEN timer
- YELLOW date/time
- BLUE EPG search
- colour-key captions always follow active Enigma2 OSD language.

## Target state — PROGRAM INFO
Visual authority is the maintainer-supplied reference screenshot (2026-10-02).
- Large FullHDGlass dark/translucent information panel.
- Upper-left: **real image/poster/still belonging to the selected programme**.
- **NO live PIG/video in PROGRAM INFO.**
- **NO enlarged station picon as fake programme artwork.**
- Artwork/enrichment should be resolved from the selected EPG programme title using a reliable external match. **Approved external sources are ČSFD, IMDb and TMDB.** Any of these may provide programme artwork and/or metadata when the match is reliable.
- If no reliable artwork match exists, leave artwork empty rather than showing a wrong image.
- Amber programme title.
- Station picon and station name remain separate from programme artwork.
- Date/time/duration from authoritative EPG data.
- Right side: large programme description.
- Left metadata may show Station, Genre, Year, Country, Duration, Broadcast, Format, Age restriction, but **only fields backed by reliable data**.
- Rating only when reliably sourced.
- Never invent metadata and never guess an uncertain title match.
- Bottom RED/GREEN/YELLOW/BLUE actions visible and functional.
- All button captions and new Warder UI labels follow active Enigma2 OSD language. Do not hardcode Slovak or English globally.
- Warder-owned translations for new strings must take precedence where legacy FullHDGlass gettext has a semantic collision (known example: PROGRAM INFO was incorrectly translated to CSFD).

## Data/source policy for PROGRAM INFO
1. EPG is authoritative for selected event identity, title, broadcast time, duration and EPG descriptions.
2. Normalize the EPG title only for searching; retain the original title for display.
3. External lookup must be silent — no foreign GUI, chooser, browser or user prompt.
4. Accept external metadata/artwork only after a reliable match.
5. An uncertain match means: show EPG data only and leave external-only fields/artwork empty.
6. Cache successful external results so opening PROGRAM INFO is responsive and does not repeatedly query providers.
7. Station picon is station identity only, never programme artwork.

## Completed / verified development history
- TEST32: GraphicalEPGPIG physically tested; colour keys/actions worked and RED opened custom PROGRAM INFO.
- TEST34: PROGRAM INFO opened on receiver; basic title/time/descriptions/actions worked. Preview was not correct yet.
- TEST35: service wrapper normalization/callback/station-picon fixes.
- TEST36: translucent Program Info direction physically tested; no GSOD. Mute icon seen in screenshots is a normal receiver mute indicator and must be ignored.
- TEST37: narrower metadata column and softer button backgrounds.
- TEST38: attempted localization and FullHDGlass poster renderer. Receiver test exposed two regressions: GraphicalEPGPIG RED became CSFD because of legacy gettext collision; Program Info bottom captions disappeared.
- TEST39 commit `a0024e9c6a65d84ff9368ffb47fa60e889e729ff`: bottom captions converted to StaticText source/render Label; temporarily hardcoded PROGRAM INFO. This hardcoding was immediately rejected as contrary to language policy.
- TEST40 commit `9cc195941125b56b0efd5e1622f1cd63a12b5823`: restored environment-language policy and moved Program Info closer to approved reference.
- TEST41 commit `1b81852437d5692eceeac53d7b454abb56efd8db`: removed live PIG from PROGRAM INFO. Programme artwork remains through the existing `g17Poster2` title-driven renderer.
- TEST42: inspected the actual FullHDGlass poster pipeline. `g17Poster2` already has cache plus TMDB and IMDb poster lookup; its TMDB path previously trusted result #1 blindly. TEST42 adds an exact normalized-title gate across the first five TMDB results before any poster is downloaded. This is the first external-enrichment reliability guard; metadata enrichment is still pending.
- TEST43: added a silent cached PROGRAM INFO metadata provider using the already-approved TMDB source. It rejects fuzzy matches and ambiguous exact-name movie/TV collisions; only a unique exact normalized title can populate genre/year/country/rating. Provider/network failure returns EPG-only data without GSOD. ČSFD and IMDb remain approved sources for subsequent provider expansion.
- TEST44 correction commit `54cba4f96c35f0e460b5f84a431184b10402d94a`: the provider now really disambiguates multiple exact-title candidates using EPG-description overlap. A weak or tied contextual result returns no external enrichment. This corrects the implementation mismatch found by the mandatory HEAD audit. Provider-ID/detail enrichment remains the next step.\n- TEST45 code commit `ef762c4fb9ff0b459da3e9d3c0bc29c096ec8d09`: after the exact/context identity is verified, the provider now fetches TMDB detail plus external IDs and retains both TMDB provider ID and IMDb ID. Detail data may enrich year, country, genre, runtime, rating, overview and artwork paths; network/detail failure falls back to the already verified search result. No second fuzzy IMDb title search is performed.\n- TEST46 batch: completed the verified TMDB detail fields in the provider, exposed external runtime in PROGRAM INFO without replacing authoritative EPG duration, consolidated stale TEST43/44 regression guards to the current provider contract, bumped package to `1.0.5-test46-1`, and requested TEST46 revision 142. Artwork is not yet switched from legacy title-only g17Poster2 to the verified provider identity; that remains mandatory before receiver validation of artwork.\n- DreamOS compatibility fix already present: tolerant preinst layout detection and eTimer `timeout.connect` with legacy callback fallback.
- Original FullHDGlass17 DreamOS-compatible r12.2 IPK/DEB were separately rebuilt from user-supplied r12.1 packages; receiver PASS is not assumed without hardware confirmation.

## Current state at this checkpoint
Current development target is TEST46 batch lineage.
Known intended code state:
- PROGRAM INFO contains no `session.VideoPicture` Pig.
- Programme-artwork widget uses `posterTitle` / `g17Poster2`.
- Station picon remains separate.
- Bottom actions use StaticText Sources rendered as Labels.
- Warder new UI strings are selected from active `config.osd.language` before falling back to legacy gettext, avoiding the CSFD collision for SK/CZ.
- GraphicalEPGPIG approved geometry must remain unchanged.

## TODO — ordered, do not skip
### P0 — Finish PROGRAM INFO external enrichment
- Inspect existing FullHDGlass poster/search/cache code and any existing IMDb/CSFD integration already shipped in the project before adding new dependencies.
- Implement a silent provider layer for programme artwork and metadata.
- Prefer reuse of existing FullHDGlass infrastructure where technically suitable.
- Define reliable title matching using EPG title plus available contextual evidence (year/episode/description where available).
- Fetch/cache real programme artwork.
- Populate only reliably sourced metadata: genre, year, country, format, age restriction and rating when available.
- Never fabricate missing values.
- Never use live video or station picon as artwork.
- Provider/network failure must degrade to EPG-only display without GSOD.

### P0 — Localization
- Keep every colour-key caption tied to active Enigma2 language.
- Remove any temporary hardcoded-language workaround.
- Prevent legacy gettext semantic collisions for Warder-only strings.
- Extend proper translations as needed without changing approved geometry.

### P1 — Receiver validation
After CI publishes the next TEST package, verify on GigaBlue Quad 4K Pro:
- RED label in GraphicalEPGPIG is correct for active environment language and never incorrectly becomes CSFD.
- PROGRAM INFO opens without GSOD.
- real programme image corresponds to selected programme when a reliable match exists.
- no live PIG and no fake enlarged station picon.
- title/station/time/duration/description correct.
- external metadata appears only when reliable.
- four bottom buttons visible, translated and functional.
- guide geometry unchanged.

## Mandatory work procedure for every future session/change
1. Read this journal first.
2. Fetch current `warder-modernization-work` HEAD.
3. Re-read files to be modified from that exact HEAD.
4. Identify the next unchecked TODO; do not improvise unrelated redesigns.
5. Make the smallest coherent change toward the documented target.
6. Add/update regression guards for the contract changed.
7. Preserve all previously approved geometry/behaviour unless the maintainer explicitly changes it.
8. Commit with no force push.
9. Update **this journal in the same commit**: exact commit intent, what changed, what remains, and whether CI/receiver verification exists.
10. Never call something receiver-PASS until the maintainer physically confirms it.

## Next action
Continue P0 in larger batches: replace the PROGRAM INFO legacy title-only artwork lookup with artwork from the same verified provider identity/cache; then use retained IMDb ID for cross-provider enrichment and add ČSFD only with reliable matching. After static regression/CI passes, publish one consolidated receiver-test package rather than many tiny tests. Approved sources remain ČSFD, IMDb and TMDB. Do not redesign GraphicalEPGPIG and do not reintroduce live PIG.

- TEST46 CI publication verified: `1.0.5-test46`, SHA-256 `620b0ccc716063c817a6ecf6532dd92fcce0cca64772286012c385514fc39252`; receiver screenshot showed the programme-artwork area still empty and redundant station identity beside the title/lower metadata layout too wide.
- TEST47 batch implements the maintainer screenshot correction: PROGRAM INFO artwork now comes only from the same verified TMDB provider identity/cache (backdrop preferred, poster fallback); station picon + station name moved directly below artwork; duplicate lower Station/service row removed; left metadata column narrowed and description expanded to x=535 width=1170. GraphicalEPGPIG remains untouched. Package/runtime `1.0.5-test47`, CI revision 149. Receiver PASS pending physical test.
