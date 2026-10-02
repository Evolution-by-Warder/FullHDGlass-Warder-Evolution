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

- TEST48 receiver-screenshot correction batch: GraphicalEPGPIG colour captions now use dedicated Warder StaticText sources instead of OpenATV/legacy `key_red` etc., so legacy CSFD refresh/gettext cannot overwrite RED; handler remains PROGRAM INFO. Verified artwork matching now strips explicit season/episode suffixes such as Roman-season + episode number and SxxExx, searches exact localized titles in cs-CZ/sk-SK/en-US, and still rejects non-exact candidates. PROGRAM INFO artwork pixmap scaling is enabled. TEST47 approved layout changes are retained: station identity below artwork, no duplicate station beside title, narrower left metadata and wider right description. Package/runtime `1.0.5-test48`, CI revision 150. Receiver PASS pending physical test.


- TEST49 repair batch: mandatory HEAD audit found TEST48 provider corruption introduced by a malformed regex edit: `warderProgramInfo.py` was syntactically invalid and contained duplicated provider code, so TEST48 is not a valid receiver candidate. TEST49 rebuilds the provider cleanly from the verified TEST47 contract, safely strips explicit episode suffixes (including `Přátelé VI (10)` / SxxExx), keeps exact localized TMDB matching, versions the provider cache so stale negative TEST46/47 cache entries cannot suppress the new lookup, and implements true backdrop-first/poster-fallback artwork with JPEG validation. TEST48 Warder-owned GraphicalEPGPIG colour sources are retained unchanged to isolate PROGRAM INFO from legacy CSFD gettext/state. Stale TEST38/40 g17Poster2 geometry assertions were consolidated into the current verified-artwork/layout contract without weakening unrelated r12 guards. Package/runtime `1.0.5-test49`, CI revision 151. Receiver PASS pending physical test.

- TEST49 CI correction: Actions run 36997377493 reached static preflight and failed only because the older TEST23 compatibility assertion still required legacy `key_red/key_green/key_yellow/key_blue` Label sources on GraphicalEPGPIG. That assertion is now narrowed to the intentional TEST48+ exception: GraphicalEPGPIG must use `warder_key_*` and must not expose legacy `key_*` Label sources; GraphicalEPG and all unrelated guards remain unchanged. This is a CI-test correction for the same TEST49 candidate, not a new receiver version. Revision 152 retriggers TEST49. Receiver PASS remains pending physical test.

- TEST49 CI correction revision 153: run 36997586611 passed XML, lifecycle, runtime-safety, version-order and the main r1-r12 gate, then exposed additional pre-TEST38 GraphicalEPGPIG assertions from TEST28/29/31 that still required legacy `key_*` colour sources. All remaining GraphicalEPGPIG-only legacy colour-source assertions were audited together and aligned to the intentional TEST48+ `warder_key_*` isolation; unrelated Opkg/other-screen key assertions and geometry guards are untouched. Same TEST49 receiver candidate; no functional skin/provider change. Receiver PASS pending physical test.

- TEST50: reduced the requested path to one deterministic action. On FullHDGlass GraphicalEPGPIG, RED now opens only WarderProgramInfo for the currently selected EPG event. The previous fallback to OpenATV `infoKeyPressed()` was removed because it could reopen the legacy/CSFD path when event extraction failed. Missing/invalid selection now does nothing instead of opening a foreign screen. PROGRAM INFO layout/provider contract remains unchanged. Receiver PASS pending physical test.

- TEST50 CI revision 155: run 36998189642 passed XML/lifecycle/runtime/version/main r1-r12 gates and then hit two stale TEST31 PROGRAM INFO geometry assertions (old divider 625,415 and description 665,425/1040x335). They are aligned to the already-approved TEST47+ geometry (divider 500,440; description 535,440/1170x320). No runtime or design change; same TEST50 candidate.

- TEST51 receiver correction from physical TEST50 screenshots: keep the now-confirmed Warder PROGRAM INFO screen and refine only its requested content. Slovak visible caption is unified to “Info o programe”. The station picon moves below the horizontal divider; beneath it is “Názov stanice:” plus the real service name, followed by EPG Duration and Broadcast. The unused external genre/year/country/rating/runtime rows are removed from the left block for now. Programme artwork remains the verified TMDB identity artwork in the existing upper-left field; provider cache schema advances to v3 so TEST51 retries artwork instead of inheriting stale TEST50 cache. No GraphicalEPGPIG geometry change. Receiver PASS pending physical test.

- TEST52: physical receiver screenshots confirmed inconsistent left metadata rows. PROGRAM INFO now always shows the same ordered block: station picon, Station name, Genre, Year, Country, Rating, EPG Duration, EPG Broadcast. Verified provider values fill Genre/Year/Country/Rating; unavailable values remain '-'. EPG Duration/Broadcast remain authoritative. Remaining stale TEST51 station geometry guards are aligned. Receiver PASS pending physical test.

- TEST53 visual consolidation from receiver feedback: PROGRAM INFO outer geometry now matches GraphicalEPGPIG (15,15 / 1890x1050); the cyan top line and separate translucent artwork backing rectangle are removed for one uniform panel surface. Programme artwork grows to 520x300. Verified rating moves to the upper-right under date/time with five star glyphs plus numeric/provider line. The description area grows to 1300x440 and the bottom separator/actions move down to y=890/925+, creating substantially more vertical reading space. Long-description automatic slow scrolling is intentionally deferred to the next runtime-safe step rather than faking it with an unverified Enigma2 widget API. Receiver PASS pending physical test.

- TEST53 CI revision 159: Actions #161 passed compile/XML/lifecycle/runtime/version/main r1-r12 gates and stopped on one remaining stale TEST47 divider-geometry assertion (500,440 / 2x320). Regression guard is aligned to TEST53 approved divider 500,425 / 2x440; remaining old bottom-divider geometry assertions are aligned in the same audit. No runtime/design change; same TEST53 candidate.

- TEST54 GraphicalEPGPIG visual cleanup from physical receiver comparison: remove the six static timeline0..timeline5 vertical grid lines from Warder GraphicalEPGPIG while preserving the red/current-time timeline_now marker and all approved geometry. Increase upper extended-description font from Prive3 27 to 31 and foreground from #cdcdcd to #eeeeee for readability. Current-event green is intentionally not hardcoded blindly in skin XML because GraphMultiEPG event colours are runtime/config driven; existing current-program green behavior is preserved until the exact renderer/config source is verified. PROGRAM INFO TEST53 work remains intact. Receiver PASS pending physical test.

- TEST55 GraphicalEPGPIG header polish: use the previously empty top-left header area for current weekday/date and live clock with seconds; add a restrained FullHDGlass17 · Warder Evolution identity at top-right. Fill the otherwise blank cap above the picon column with a compact EPG label while leaving timeline_text at x=75, so the renderer's time-grid geometry and the approved picon/list geometry remain untouched. TEST54 removal of static vertical grid lines and larger description remains intact. Receiver PASS pending physical test.

- TEST55 CI revision 162: Actions #164 passed compile/XML/lifecycle/runtime/version/main r1-r12 gates and stopped only on the older TEST23 assertion requiring timeline0..timeline5 on GraphicalEPGPIG. The guard is narrowed to the intentional TEST54+ contract: GraphicalEPGPIG must not contain those six static vertical lines, while GraphicalEPG still must contain them. No runtime/design change; same TEST55 receiver candidate.

- TEST55 CI revision 163: Actions #165 again passed compile/XML/lifecycle/runtime/version/main r1-r12 gates and stopped only on the older TEST26 assertion requiring timeline0 at 75,423. TEST26 is aligned to the intentional TEST54+ visual contract: no static timeline0, but timeline_now must remain at 75,423. No runtime/design change; same TEST55 candidate.

- TEST55 CI revision 164: Actions #166 passed XML/lifecycle/runtime/version and the main r1-r12 regression gate, then stopped on a stale TEST49 metadata assertion expecting CACHE_SCHEMA v2 while the provider is already intentionally v3. Guard aligned to the real v3 provider schema; no runtime/design/provider change. Same TEST55 candidate.

- TEST55 CI revision 165: Actions #167 reached the later TEST51 guard and failed because the regression script referenced PROVIDER without defining it. Added the authoritative warderProgramInfo.py read at test initialization. This is test-harness-only; no runtime/design change. Same TEST55 candidate.

- TEST55 CI revision 166: Actions #168 reached TEST54/55 checks and exposed another test-fixture omission: epg_pig was referenced before assignment. Added a local extraction of the GraphicalEPGPIG skin block immediately before those checks. Test-harness-only; runtime/design unchanged. Same TEST55 candidate.

- TEST56 receiver visual correction: remove the literal EPG cap above the picon rail and extend native timeline_text left from x=75 to x=15 (width 1815), matching the user's live screenshot request. PROGRAM INFO station picon enlarged to 120x72; station label/value reduced slightly to 24pt. Metadata rows are redistributed and duration/broadcast moved upward; broadcast value height increased to 82 so its second line is not clipped while retaining the unused space above the lower divider. Receiver PASS pending physical test.

- TEST57 PROGRAM INFO rating repair: receiver TEST55 screenshot confirmed the reserved upper-right rating area remained blank although TMDB metadata was otherwise present. Root cause: provider returns rating already formatted as e.g. 8.2/10, while UI attempted float(meta["rating"]), raising ValueError inside the metadata block. Parse the numeric component before '/', render five-star visualization under the clock, and show compact '8.2/10 · TMDB' below it. Stars increased slightly to 36pt; metadata reduced to 25pt. TEST56 geometry refinements retained. Receiver PASS pending physical test.

- TEST57 CI revision 169: Actions #171 passed XML/lifecycle/runtime/version/main r1-r12 gates and stopped only on the historical TEST24 timeline_text x-position guard. Aligned it to the approved TEST56 receiver correction (timeline_text x=15 width=1815) while keeping the 15-row grid at 15,423 / 1845x495. No runtime/design change; same TEST57 candidate.

- TEST57 CI revision 170: Actions #172 progressed through the same gates and exposed one more historical TEST26 timeline_text x=75 assertion. Updated that stale guard to the approved TEST56 x=15 / width=1815 geometry. Test-only correction; no runtime/design change.

- TEST57 CI revision 171: Actions #173 reached the PROGRAM INFO regression block and exposed two older TEST53 geometry assertions for stationPicon (50,445) and channel (245,515). Updated them to the receiver-requested TEST56 geometry: picon 50,435 / 120x72 and channel 245,520 / 215x34 / 24pt. Test-only correction; runtime remains TEST57.

- TEST57 CI revision 172: Actions #174 exposed the final duplicate approved-geometry lock still requiring timeline_text x=75. Updated it to TEST56 approved x=15 / 1815x36. No runtime/design change.

- TEST58 from physical TEST57 receiver screenshots: EPG correction now keeps native timeline labels at x=75 and extends only the vacated 60px visual strip above station picons (no literal EPG). PROGRAM INFO transient upper-right square identified as Enigma2 busy/spinner symptom while synchronous TMDB lookup blocks the GUI; metadata lookup moved to a daemon worker thread and applied on the GUI thread via eTimer polling. Bottom divider moved y=890→940, description and vertical separator gain 50px, footer buttons moved y=925/933→955/963 to use lower free space. Receiver PASS pending physical test.

- TEST58 header refinement: PROGRAM INFO now uses the same top-line visual language as GraphicalEPGPIG: weekday/date in Warder gold at x=30, live-style HH:MM:SS clock at x=435, and FullHDGlass17 · Warder Evolution signature at upper right. Replaces the previous single right-aligned date/time field; no other TEST58 geometry changed.

- TEST58 metadata normalization: physical receiver exposed EPG title “Česko Slovensko má talent X”. Added conservative stripping of a standalone trailing Roman-numeral edition/season suffix before TMDB search, while retaining exact normalized base-title matching (no fuzzy acceptance). Cache schema bumped v3→v4 so earlier negative cache entries cannot mask the corrected lookup.

- TEST58 CI guard maintenance: aligned remaining historical PROGRAM INFO separator assertion with approved 490px content height; runtime/design unchanged.

- TEST58 compatibility fix from r12.2 field report: removed explicit font="Regular;34" from the list widgets in MessageBox and MessageBox-template. Current OpenATV reference MessageBox templates leave the list font to the Enigma2 list component; this avoids the reported GSOD path while preserving geometry/itemHeight. MessageBoxModal is intentionally unchanged because the report and shared template path concern only MessageBox and MessageBox-template.

- TEST58 CI fix: repaired malformed _baseTitle regex introduced by the Roman-edition normalization commit; restored complete SxxExx rule plus standalone trailing Roman numeral rule. No fuzzy title matching added.

- TEST58 CI cleanup: removed the stale malformed tail left at EOF by the earlier failed regex replacement. _baseTitle remains defined once in its proper location; provider now compiles cleanly by inspection.

- TEST58 provider structural repair: CI exposed a duplicated stale provider body appended after the valid lookup() return. Removed the entire duplicate tail and retained one canonical _cachePath/_readCache/.../lookup implementation. This addresses the repeated unmatched-parenthesis failures at shifting line numbers rather than patching individual fragments.

- TEST58 provider cleanup completed deterministically: truncated all content after the first complete canonical lookup() implementation. Verified exactly one _cachePath and one lookup definition remain; removes both duplicated provider copies that CI showed at lines ~181 and ~321.

- TEST58 regression alignment: CI now reaches all Python/XML/runtime/r1-r12 gates successfully. Updated remaining stale Program Info geometry assertions to the intentional TEST58 footer/description layout (description 490px, divider y=940, button background y=955, label y=963).

- TEST58 async metadata regression guard: replaced stale synchronous warderProgramLookup assertion with guards for the intentional non-blocking worker call and eTimer polling. This preserves the busy/spinner fix instead of forcing the old GUI-blocking implementation.

- TEST58 CI syntax fix: converted accidentally literal \\n sequences in the three async metadata regression assertions into real Python newlines. No production/runtime code changed.

- TEST58 async metadata guard correction: matched the actual worker function name used by production code (worker, not _worker). Production code unchanged; guard now verifies threading.Thread(target=worker), daemon start and timer polling path.

- TEST58 metadata cache regression alignment: updated stale guard from CACHE_SCHEMA v3 to the intentional v4. v4 is required so prior negative cache entries cannot hide the new Roman-edition title normalization.

- TEST58 regression cleanup: removed stale undefined PROGRAM_INFO_PROVIDER alias in favor of the existing META provider source and corrected async worker assertion to inspect PLUGIN, where the Program Info class implementation actually lives. No runtime code changed.

- TEST59 receiver corrections from physical TEST58 screenshots: rebuilt GraphicalEPGPIG timeline header as one continuous 1845px #505050 strip from x=15 to the same right edge as the EPG list, while keeping timeline text aligned at x=75 and extending it to x=1860. PROGRAM INFO now temporarily suppresses the Enigma2 global busy spinner only while the background TMDB metadata worker is active and restores the user setting both when lookup completes and when the screen closes; this targets the upper-right spinner fragment seen on the receiver without disabling the user setting permanently. Package control advanced to 1.0.5-test59-1.
