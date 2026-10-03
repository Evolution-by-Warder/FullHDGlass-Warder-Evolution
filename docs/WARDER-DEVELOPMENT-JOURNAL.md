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

- TEST59 version sync: runtime Warder version marker advanced from 1.0.5-test58 to 1.0.5-test59 to match control/build candidate.

- Receiver feedback after TEST58: aligned PROGRAM INFO station value with the metadata value column by moving channel x=245 to x=225 and widening it to 235. This addresses the visible 20px right shift of the station value. Physical receiver verification pending.

- TEST59 station alignment regression guard: updated the remaining stale TEST51 assertion to the receiver-requested channel geometry x=225 / width=235. Runtime layout already had this geometry; no runtime behavior changed in this commit.

- TEST60 receiver correction from physical TEST59 screenshots (2026-10-02): TEST59 is receiver-FAIL for the flat grey timeline strip, persistent upper-right busy fragment and slow first metadata load. GraphicalEPGPIG now uses one continuous dark FullHDGlass-style 1845px timeline surface with a restrained top highlight and bottom shadow; timeline text remains x=75 and approved EPG/list geometry is unchanged. The TEST59 in-screen spinner toggle is removed: spinner visibility is suppressed before WarderProgramInfo is opened and restored only after the screen closes, preventing an already-painted busy frame from being frozen in the upper-right corner. TMDB exact matching now uses search/multi (movie+TV together), stops after the first locale producing exact candidates and falls back cs-CZ → sk-SK → en-US only when needed, reducing the common cold lookup from six serial search requests to one while preserving exact matching, context disambiguation, backdrop-first artwork and cache schema v4. PROGRAM INFO channel remains x=225/235; artwork/rating geometry is unchanged. Receiver PASS pending physical test.

- TEST60 CI revision 191: Actions #195 stopped at Python compile preflight because the initial spinner-before-open edit malformed the RED handler (invalid `return spinnerWasEnabled = None`). Rebuilt the complete Warder PROGRAM INFO close/RED-handler block with correct indentation and spinner restore lifecycle. No design/provider/geometry change; same TEST60 candidate.

- TEST60 CI retrigger revision 191: bumped TEST-BUILD-REQUEST after the syntax-only RED-handler repair so the corrected candidate is rebuilt and republished by the TEST workflow. Receiver verification remains pending.

- TEST60 CI revision 192: Actions #196 passed the complete static preflight, then correctly rejected packaging because the runtime version file still declared 1.0.5-test59-1 while control declared 1.0.5-test60-1. Synced the runtime version marker to 1.0.5-test60-1 and retriggered the same TEST60 candidate. No runtime behavior or visual geometry changed.

- TEST61 receiver correction from physical TEST60 screenshots (2026-10-02): GraphicalEPGPIG dimensional timeline is receiver-PASS. PROGRAM INFO remains receiver-FAIL for cold lookup latency and metadata miss on “Baywatch - Pobrežná hliadka”. The persistent upper-right “fragment” is now identified from the layout itself as the right-aligned ratingMeta placeholder “-”, not the spinner; rating now starts blank while genre/year/country retain “-”. Provider cache advances to v5, network timeout is reduced to 2.5s, Slovak locale is tried before Czech/English, and spaced-dash broadcaster titles generate an exact primary-title candidate (e.g. “Baywatch”) while retaining exact normalized TMDB matching. Same-title movie/TV collisions may be resolved only by explicit EPG series wording; no fuzzy title/artwork matching is introduced. TMDB remains the sole external metadata service. Receiver verification pending.

- TEST61 CI revision 194: Actions #198 stopped in static regression preflight because one legacy assertion still expected the old cs-CZ → sk-SK locale order. Updated that guard to the TEST61 sk-SK → cs-CZ → en-US contract; runtime code unchanged. Retriggered TEST61.

- TEST61 CI revision 195: Actions #199 found a second stale provider regression token (`_norm(candidate) == wanted`) after TEST61 expanded exact matching across TMDB localized/original title/name fields. Updated the guard to the new exact `any(_norm(name or "") == wanted for name in names)` contract. Runtime unchanged; TEST61 retriggered.

- TEST61 CI revision 196: Actions #200 found the final stale cache-schema regression assertion still pinned to v4. Updated all remaining TEST regression expectations to cache schema v5. Runtime unchanged; TEST61 retriggered.

- TEST62 receiver correction from physical TEST61 screenshots (2026-10-02): GraphicalEPGPIG is receiver-PASS. Known exact metadata (Baywatch) is fast and correct, including artwork/metadata/rating. Unresolved titles remain EPG-only with blank artwork by design, but the first miss exposed the Enigma2 busy spinner and could wait through serial provider timeouts. Provider cache advances to v6; exact TMDB search now has a 3.0 s total deadline with at most 1.0 s per search request, while successful detail/artwork behavior remains unchanged. WarderProgramInfo also reasserts spinner-off while its silent worker is pending. No EPG geometry/design change. Receiver verification pending.

- TEST63 receiver correction from physical TEST62 screenshot (2026-10-02): TEST62 confirmed unresolved TMDB titles degrade correctly to EPG-only and the approved GraphicalEPGPIG remains PASS, but a stale Enigma2 busy-spinner framebuffer tile is still visible at the extreme upper-right of PROGRAM INFO. Because setSpinnerOnOff suppression alone does not erase an already painted tile, TEST63 adds only a small opaque Warder-owned cap over that reserved corner inside WarderProgramInfo. No EPG geometry, metadata matching, artwork logic, or Program Info content geometry changes. Receiver verification pending.

- TEST64 receiver-requested PROGRAM INFO polish: station picon enlarged from 120x72 to 180x90 and horizontally centred in the left metadata column. Station text/metadata rows, description, GraphicalEPGPIG and TMDB logic remain unchanged. TEST63 upper-right artifact is not claimed fixed. Receiver verification pending.

- TEST65 receiver-requested EPG polish: timeline_text now spans x=15..1860 so its native 60px service/date cell occupies the picon rail instead of being clipped at x=75 (the visible stray “Dn” symptom); event time positions remain aligned with the event grid. GraphicalEPGPIG selected-event fill is explicitly amber (#d69600) for both current and non-current selected events, with white selected text, using OpenATV EPGList's supported EntryBackgroundColorSelected/NowSelected skin attributes. 15 rows, PIG, picon rail, event geometry, green running-event state and buttons remain unchanged. Receiver verification pending.
\n- TEST66 receiver correction after physical TEST65: TEST64 station picon is confirmed PASS and retained. TEST65 selected-event colour and timeline date fragment are FAIL. OpenATV EPGList graphics mode renders selected events from epg/SelectedEvent.png (plus selected current/record/zap variants), so Warder now supplies amber selected-event graphics instead of relying on text-mode EntryBackgroundColorSelected. TimelineText generated 60px date cell is covered locally while native time labels remain visible. The failed TEST63 upper-right cap and repeated setSpinnerOnOff(0) workaround are removed because disabling animation can preserve an already painted frame; metadata remains asynchronous. Receiver verification pending.\n
- TEST66 CI #207: static preflight stopped on a regression-file syntax typo: the appended TEST66 guard contained literal backslash-n text. Runtime/package sources were not implicated. Corrected only the regression guard formatting and retriggered TEST66; receiver verification remains pending.

- TEST66 CI #208: complete static preflight and r1-r12 regression gate PASS. Build then correctly rejected a control/runtime version mismatch (control 1.0.5-test66-1, runtime 1.0.5-test66). Synced the runtime version marker to 1.0.5-test66-1 and retriggered the same TEST66 candidate; no runtime/visual behavior changed. Receiver verification pending.

- TEST66 CI #209: static preflight and r1-r12 gate PASS. Build script confirms runtime version must be the visible TEST identity and derives the numeric package revision itself (`EXPECTED_PKGVER=${RUNTIMEVER}-1`). Reverted the mistaken runtime marker from 1.0.5-test66-1 to 1.0.5-test66 and retriggered. No runtime/visual behavior changed; receiver verification pending.

- TEST66 physical receiver result (2026-10-02): GraphicalEPGPIG list and amber selected-event cell are PASS. Program Info upper-right spinner/artifact remains FAIL and can stay permanently painted for minutes. Repository inspection found the TEST66 published plugin still contained the old TEST62/63 `setSpinnerOnOff(0)` calls, spinner-state restore handler and opaque 55x55 cap despite the intended removal. TEST67 removes those legacy spinner manipulations and cap for real; metadata remains asynchronous. EPG PASS geometry/selection and TEST64 180x90 picon are retained unchanged. Receiver verification pending.

- TEST67 physical receiver result (2026-10-02): spinner tile still appears initially and later disappears. More importantly, EXIT/RED requires two presses while metadata is pending. TEST68 fixes Program Info lifecycle rather than masking pixels: close action now stops the metadata polling timer and marks the screen closed before calling Screen.close; worker completion never touches GUI directly, and poll ignores results after close. This guarantees first keypress closes independently of TMDB state and prevents late metadata application to a closed screen. EPG/list/amber selection and TEST64 picon remain unchanged. Receiver verification pending.

- TEST68 physical receiver result: FAIL. Spinner still appears and Program Info still needs two EXIT/RED presses. OpenATV source confirms the visible top-right tile is the core gRC busy spinner (wait*.png), not a Warder widget. TEST69 therefore suppresses the core spinner only for the lifetime of WarderProgramInfo and restores the user's configured spinner state on close. This is paired with the existing immediate close/timer stop lifecycle. Also corrected the non-modal MessageBox list font: it previously omitted `font`, unlike MessageBoxModal; set it explicitly to Regular;34 so updater Yes/No choices match the established FullHD dialog scale. EPG/list/selection/picon remain untouched. Receiver verification pending.

- TEST69 CI #213: runtime/package preflight reached and passed the full r1-r12 gate, then failed only because the TEST62 regression assertion still prohibited `setSpinnerOnOff(0)`. TEST69 intentionally reintroduces that call in a scoped onShown/onClose core-spinner guard after identifying the tile in OpenATV gRC. Updated the regression contract to require the scoped suppress/restore methods and retriggered; runtime and GUI code unchanged.

- TEST69 physical receiver result (2026-10-02): FAIL. The upper-right gRC busy tile remains visible and EXIT/RED still needs two presses. TEST70 removes the ineffective global setSpinnerOnOff lifecycle entirely. While asynchronous TMDB metadata is pending, Program Info now emits a lightweight 500 ms clock repaint so OpenATV gRC never reaches its no-display-output busy-tile path. Program Info's own ActionMap priority is raised from -1 to -2 and close hides the screen immediately before Screen.close, so the first EXIT/RED event owns and visibly closes this screen. EPG geometry/selection, Program Info geometry, 180x90 picon, rating/stars and TMDB exact-match rules are unchanged. Receiver verification pending.

- TEST70 CI #215: runtime/package preflight passed XML, lifecycle, runtime-safety, version-order and the r1-r12 gate, then failed only on an older regression assertion that still required the pre-TEST70 100 ms metadata timer. TEST70 intentionally uses 500 ms as the lightweight repaint heartbeat. Updated that stale assertion to 500 ms; runtime/GUI behavior unchanged. Receiver verification pending.

- TEST70 physical receiver result (2026-10-02): FAIL. Screenshot confirms the upper-right gRC tile is still visible. User also reports that the first RED press only makes the Program Info image blink and the second RED closes it. That blink is consistent with one Program Info closing while another identical instance remains stacked underneath, so TEST71 fixes the opening path rather than adding another spinner workaround: Graphical EPG now owns a per-screen _warderProgramInfoOpen guard set before openWithCallback and cleared only by the close callback (or immediately if opening raises). Duplicate RED delivery therefore cannot stack a second Program Info instance. Approved EPG/Program Info geometry, 180x90 picon, rating/stars and TMDB matching remain unchanged. Receiver verification pending.

- TEST71 physical receiver result (2026-10-02): PASS. User confirmed no upper-right spinner and one RED press closes Program Info normally. The duplicate-open guard is therefore the accepted fix and TEST71 is the stable Program Info checkpoint. Approved EPG/Program Info geometry, 180x90 picon, rating/stars and TMDB exact-match rules remain protected.

- TEST72 validation-only candidate: TEST71 remains the stable Program Info receiver-PASS checkpoint. TEST72 changes no runtime GUI behavior; it advances only the TEST package identity so a receiver still on TEST71 is offered an update and the updater confirmation MessageBox Yes/No font correction introduced in TEST69 can be physically verified. No EPG, Program Info, picon, rating/stars or TMDB code changed. Receiver verification pending.

- Post-TEST72 receiver diagnosis: updater confirmation still showed undersized Yes/No choices. Exact history comparison found TEST58 removed font="Regular;34" from both MessageBox and MessageBox-template, while TEST69 restored it only to MessageBox. Restored the missing font attribute to MessageBox-template as well, returning both choice-list definitions exactly to their pre-TEST58 font configuration. TEST71 Program Info receiver-PASS checkpoint and approved EPG/Program Info/TMDB behavior remain unchanged. Receiver verification pending.

- TEST73 candidate: restored the full development tree from TEST72 source after detecting that the preceding atomic tree commit had accidentally used an empty base-tree reference and therefore exposed only the two edited files. No force push/rebase was used. TEST73 carries the intended MessageBox-template font restoration on top of the complete TEST72 development source. Runtime version advanced to 1.0.5-test73 solely for receiver validation of normal-sized Yes/No choices; TEST71 Program Info PASS remains protected.

- TEST74 validation-only candidate: no runtime GUI code or skin geometry changed from TEST73. Version/build identity only, so a receiver after installing TEST73 can be offered TEST74 and the updater Yes/No confirmation will be rendered by the installed TEST73 MessageBox definitions. This is the valid physical test of the restored Regular;34 MessageBox-template font. TEST71 Program Info PASS remains protected. Receiver verification pending.

- TEST74 CI retrigger: initial Revision 215 commit did not start an Actions run. Bumped only TEST-BUILD-REQUEST to Revision 216; no runtime/package version/GUI behavior changed.

- TEST74 complete-tree recovery: rebuilt the candidate from the verified complete TEST73 source tree and overlaid only TEST74 package identity, build request, and journal. This restores `.github/workflows` and all project content without changing runtime GUI behavior. No force push/rebase used.

- Receiver physical PASS: with TEST73 installed, the updater prompt offering TEST74 renders the Yes/No choices at the intended normal FullHD size. User screenshot confirmed `Áno`/`Nie` are now correct. This validates the restored pre-TEST58 `font="Regular;34"` behavior for the effective MessageBox template. TEST74 itself was not required for this validation; the dialog was rendered by installed TEST73. Keep this MessageBox font configuration protected.

- MultiEPG / GraphicalEPG work item CLOSED / DONE (receiver verified): bottom color-key mapping is RED = Program Info / EPG selection details, GREEN = add timer, YELLOW = go to date/time, BLUE = EPG search. The approved 15-row GraphicalEPGPIG layout, picon-only station column, green current-event cells, amber selected-event cell, timeline and button mapping are complete and protected from further unrelated changes. This item belongs to MultiEPG/GraphicalEPG, not the main InfoBar.

- Radio / DAB modernization OPEN — TEST75 first implementation: preserve FullHDGlass17 · Warder Evolution identity while making the radio screen dynamic. Approved concept: prominent top header with weekday/date, live clock and larger Warder branding; central artwork priority will be exact current-song album cover, then native DAB+ slideshow (SLS), then existing Warder/OpenATV radio image fallback; bottom band keeps current RadioText/song and secondary station/DAB information. No fuzzy/random artwork. TEST75 starts with the receiver-testable native DAB slideshow-compatible shell and new header/bottom typography; album-cover lookup is the next implementation layer after this shell is physically verified. MultiEPG/Program Info/TMDB/MessageBox PASS areas remain protected and unchanged.

- Radio / DAB visual direction APPROVED by user: futuristic radio-studio composition with a recognizable broadcast/radio character (studio microphone/radio motif), illuminated globe and audio-spectrum/equalizer atmosphere, dark glass FullHDGlass17 styling with cyan/blue plus warm gold accents. Header remains weekday/date + live clock + “FullHDGlass17 · Warder Evolution”. Dynamic album artwork stays dominant in the centre and the lower station/song metadata panel remains. The approved visual mockup is preserved in the user's persistent Library as /FullHDGlass-Warder-Evolution/design/WARDER-RADIO-DAB-APPROVED-TEMPLATE.jpg and is the authoritative visual reference for subsequent Radio/DAB implementation work; do not replace it with the earlier OpenATV-logo mockups.

- TEST76 Radio/DAB real integration: the approved futuristic radio concept is now wired into receiver Radio mode, not just kept as a mockup. TEST packages generate and ship hd_glass17/radio.mvi with the Warder microphone + illuminated globe/equalizer motif and a clean central artwork area, replacing the generic image radio picture whenever the skin-owned radio.mvi is selected. RdsInfoDisplay adds a larger weekday/date + live-clock + Warder header, station picon/name, artist/title/album metadata and a 620x620 dynamic album-cover surface. RadioText is parsed only on explicit spaced artist-title separators; album lookup is asynchronous and accepts only exact normalized artist AND track matches from the iTunes song search endpoint. No fuzzy/random cover is allowed. If no exact album cover exists, the cover surface stays hidden so native OpenATV DAB+ SLS remains visible; if SLS is unavailable the Warder radio.mvi is the final fallback. Receiver physical verification pending.

- TEST77 Radio/DAB receiver candidate: TEST76 already contained the dynamic RdsInfoDisplay and deterministic build-time Warder radio.mvi, but the runtime did not explicitly point OpenATV config.misc.radiopic at that skin-owned file. TEST77 adds that missing integration at FullHDGlass17 session start and enables showradiopic. Resulting intended receiver flow is now explicit: TV → RADIO selects /usr/share/enigma2/hd_glass17/radio.mvi; RdsInfoDisplay overlays live Warder header/station/track metadata; exact current-song artwork may overlay it; when no exact artwork exists native DAB SLS remains eligible and the Warder radio.mvi is the final visual fallback. Protected MultiEPG/Program Info/TMDB/MessageBox code remains unchanged. Receiver physical verification pending.


- TEST78 EMERGENCY receiver recovery: physical TEST77 install on GigaBlue Quad 4K Pro / OpenATV 8.0.2 caused an immediate cyclic native Enigma2 restart after GUI restart. Receiver crash logs contain no Python traceback; Enigma reaches Python/DVB initialization and then exits/restarts. TEST77's only new session-start behavior forcibly assigned config.misc.radiopic and showradiopic. That override is removed completely. OpenATV already resolves config.misc.radiopic from the active GUI skin's radio.mvi, so TEST78 returns ownership to the native OpenATV path while retaining the TEST76 RdsInfoDisplay live metadata/exact artwork/DAB SLS logic and build-time hd_glass17/radio.mvi packaging. TEST77 is receiver FAIL and must not be treated as a valid candidate. TEST78 receiver verification pending; no receiver PASS recorded.


- TEST79 EMERGENCY receiver-proven recovery (2026-10-02): after TEST77 boot-loop, removing only the TEST77 config.misc.radiopic/showradiopic override did not recover Enigma2. A foreground /usr/bin/enigma2 run localized the crash to RdsInfoDisplay creation with TypeError: exec() arg 1 must be a string, bytes or code object. Replacing the custom RdsInfoDisplay XML with a minimal native widget set still crashed while the TEST76 Python monkey-patch was active. On the physical GigaBlue Quad 4K Pro / OpenATV 8.0.2 receiver, removing the entire TEST76 Warder Radio/DAB RdsInfoDisplay monkey-patch while keeping the minimal RdsInfoDisplay skin restored a normal Enigma2 boot. TEST79 makes exactly that receiver-proven recovery permanent: no WarderRdsInfoDisplay monkey-patch, no warder* RDS GUI components, minimal native RassLogo/RadioText/RtpText RdsInfoDisplay. The build-time hd_glass17/radio.mvi remains only as a passive packaged asset; no startup config override is restored. Protected MultiEPG/GraphicalEPGPIG, TEST71 Program Info/TMDB and TEST73 MessageBox behavior are unchanged. Radio/DAB feature work remains OPEN and must be redesigned without monkey-patching the native startup RdsInfoDisplay. TEST79 CI and post-install receiver reboot verification pending.


- TEST79 PHYSICAL PASS (2026-10-02): installed through the Warder updater on GigaBlue Quad 4K Pro / OpenATV 8.0.2. Enigma2 completed both post-update GUI starts without boot-loop. User then switched TV -> RADIO; Radio mode also opened normally. Receiver screenshot confirmed the passive Warder radio.mvi background plus live native data: current song text and DAB+/provider/bitrate information. TEST79 is the stable Radio/DAB recovery checkpoint.

- TEST80 Radio/DAB SAFE SKIN-ONLY candidate (2026-10-02): based on the receiver PASS and current OpenATV RdsDisplay implementation, no Python monkey-patch is reintroduced. Native RdsInfoDisplay keeps its original RadioText/RtpText/RassLogo components and native DABSlideDisplay remains responsible for SLS. The FullHDGlass17 skin adds only supported skin sources/renderers already used elsewhere in this skin: live date/time, Warder branding, CurrentService picon, service name and provider, while retaining native RadioText/RtpText. This is the first incremental step toward the approved Warder Radio/DAB layout. Dynamic exact album artwork is intentionally not reintroduced in TEST80; it will follow only through an isolated non-startup integration after this skin-only layer is physically verified.


- TEST80 PHYSICAL PASS (2026-10-02): installed through the Warder updater on GigaBlue Quad 4K Pro / OpenATV 8.0.2. Both automatic GUI starts completed normally. TV -> RADIO also completed without crash. Receiver screenshot confirmed the skin-only overlay in real Radio mode: Slovak weekday/date, live clock with seconds, FullHDGlass17 · Warder Evolution branding, Schwarzwaldradio picon/name, Bill Withers - Lovely Day native RadioText, DAB+ | DR Deutschland | 64 kbit/s native RtpText, and DAB over DVB provider. TEST80 is the new stable Radio/DAB UI checkpoint.

- TEST81 exact album-art candidate (2026-10-02): keeps TEST80 native RdsInfoDisplay untouched and adds a standalone Components.Renderer.WarderRadioArtwork used only from skin.xml in the central 560x560 artwork zone. It polls native RDS RadioText, parses only explicit spaced artist-title separators, performs network lookup in a daemon thread with 2.5 s timeout, and accepts artwork only when normalized artist AND track both match exactly. On track change the renderer hides immediately; on no exact match/error it remains hidden, so OpenATV's independent DABSlideDisplay/SLS remains visible behind it and passive radio.mvi remains the final fallback. No warder GUI components are injected into RdsInfoDisplay and no radiopic startup override returns. Receiver verification pending.

- TEST81 CI #227 correction (2026-10-02): static preflight stopped before package build because tools/test-r12-regressions.py contained a literal backslash-n before RADIO_ART, producing SyntaxError. Product/skin/renderer code was not implicated. Corrected only that test-file newline plus this journal entry; TEST81 functional implementation is unchanged.

- TEST81 CI retrigger (2026-10-02): revision 225 changes only TEST-BUILD-REQUEST so GitHub Actions reruns TEST81 after the #227 regression-test newline correction. Functional Radio/DAB implementation remains byte-for-byte unchanged.

- TEST81 CI PASS (2026-10-02): corrected run #228 completed successfully from bd3735ae42151ba067ffa3831e115c2cc500c626. Published 1.0.5-test81; IPK SHA-256 f03893a30868f7cb909a99c6c18180b953eaebabb2c48f6c965824758c70f699; publishing HEAD 0c795d6aa9d992ebe32d399c8ae4d6419015733f; artifact 11248494575. Physical install intentionally withheld because review found a rapid-track-change request race.

- TEST82 Radio artwork race hardening candidate (2026-10-02): keeps native RdsInfoDisplay untouched and changes only the isolated WarderRadioArtwork request state. _requestedKey is separate from current _key so a track arriving while a prior lookup is busy is requested on the next poll after the worker completes; a completed no-match is not repeatedly queried. Exact artist+track matching and DAB SLS/radio.mvi fallback behavior remain unchanged. Receiver verification pending.

- TEST82 PHYSICAL CHECKPOINT (2026-10-02): receiver screenshot after installation confirms Radio mode remains stable on real hardware. SCHLAGERPARADIES displayed station picon/name, native informational RadioText ('ACHTUNG ! Amazon Alexa spielt erneut falschen Sender ab...'), DAB+ | DR Deutschland | 64 kbit/s and provider DAB over DVB. Central exact-artwork renderer correctly stayed hidden because the RadioText was not an explicit artist-title pair, leaving the Warder/native fallback area visible. This is a physical PASS for boot/Radio stability and no-false-artwork behavior; exact album-art display remains pending a receiver sample carrying a valid artist - title RadioText.

- TEST83 Radio artwork parser candidate (2026-10-02): physical BAYERN 3 screenshots supplied the reproducible RadioText `Linkin Park: The Emptiness Machine` while the exact artwork field stayed empty. The isolated WarderRadioArtwork parser now accepts the explicit spaced colon form `Artist: Track` in addition to the existing spaced dash separators. Exact normalized artist AND track equality against the lookup result is unchanged, so this does not permit fuzzy/random artwork. Native RdsInfoDisplay remains untouched and native DAB SLS/passive radio.mvi fallbacks remain intact. Package 1.0.5-test83; receiver verification pending CI publication and physical test.

- TEST83 CI retrigger (2026-10-02): revision 228 changes only TEST-BUILD-REQUEST so Actions builds the already committed TEST83 colon-parser candidate. Functional Radio/DAB implementation is unchanged.

- TEST83 CI #231 correction (2026-10-02): checkout and every static gate passed, then build stopped before packaging because runtime setupGlass17/version was still 1.0.5-test82 while control was 1.0.5-test83-1. Corrected only runtime version to 1.0.5-test83 and bumped TEST-BUILD-REQUEST to revision 229. Radio artwork parser code is unchanged.

- TEST84 Radio artwork JPEG acceptance candidate (2026-10-02): receiver TEST83 still showed no exact album cover. Source audit found the JPEG signature guard rejected valid downloaded artwork before cache/display. The isolated renderer now validates the real JPEG SOI byte values with `payload.startswith(bytes((255, 216)))`. TEST83 colon parsing and strict normalized artist AND track equality are unchanged; native RdsInfoDisplay remains untouched; DAB SLS/passive radio.mvi fallbacks remain unchanged. Regression guard added. Package 1.0.5-test84; receiver verification pending CI publication and physical test. OpenWebif RADIO screenshot layering remains a separate tracked issue.

- TEST85 Radio artwork diagnostics candidate (2026-10-02): physical TEST84 receiver test on BAYERN 3 showed valid `Artist: Track` metadata but still no visible album artwork. Added diagnostic-only tracing to `/tmp/warder-radio-artwork.log` for lookup result count, rejected catalogue artist/title pairs, exact match, ready cache path, and caught exception class/message. Matching policy is unchanged: both normalized artist and track must still match exactly; no fuzzy/random artwork is allowed. No layout or native RdsInfoDisplay changes. Package 1.0.5-test85; receiver verification pending CI publication and diagnostic sample.

- TEST85 CI #235 correction (2026-10-02): all earlier static gates passed, then the legacy TEST83 source-text assertion failed because TEST85 diagnostics names the already-normalized catalogue values `gotArtist`/`gotTitle`. Exact behavior is unchanged. Updated only the regression assertion to require `gotArtist != wantArtist or gotTitle != wantTitle`, then bumped TEST-BUILD-REQUEST revision to 233 for a clean rebuild.

- Radio exact artwork physical PASS (2026-10-02): receiver screenshots on BAYERN 3 confirmed consecutive automatic exact-artwork display and track-change refresh: `Kelis: Milkshake` displayed the matching Kelis album artwork, followed by `Zartmann: Tau mich auf` displaying its matching artwork. This physically confirms RadioText parsing, exact lookup, JPEG download/acceptance, decode/display, and refresh on song change. Exact-only/no-fuzzy policy remains protected. TEST85 CI #236 itself failed only because a second duplicate legacy TEST83 source-text assertion remained later in the regression file; removed that duplicate and bumped build request to revision 234. OpenWebif RADIO framebuffer/background capture remains a separate issue.

- TEST86 explicit featuring-credit canonicalization candidate (2026-10-02): TEST85 receiver log for BAYERN 3 `Flo Rida feat. T-Pain: Low` returned catalogue candidates `Flo Rida` / `Low (feat. T-Pain)`, proving the same explicit guest credit is relocated between artist and title fields. Added a narrowly-scoped exact identity helper: `Artist feat. Guest` + `Title` may equal `Artist` + `Title (feat. Guest)` only when normalized main artist, base title, and guest all match exactly. Existing direct artist+title exact match remains first. No `&` aliasing, no Edit/Remix stripping, and no fuzzy/random matching; therefore the logged Peggy Gou `Wo, man` vs `Wo, man (Edit)` case remains rejected. TEST85 diagnostics retained. Package 1.0.5-test86; physical verification pending.

- TEST87 radio artwork metadata compatibility candidate (2026-10-02): receiver testing showed a title differing from the catalogue only by a comma. Added a narrow secondary equality gate: artist must remain exact and only commas may be ignored in the title. Version/remix/live/edit suffixes and fuzzy matching remain rejected. TEST86 feature-credit handling remains intact. Package 1.0.5-test87; physical verification pending.

- TEST88 RADIO startup responsiveness candidate (2026-10-02): priority moved to TV→RADIO startup latency before adding further metadata aliases. WarderRadioArtwork now performs its first metadata read after 100 ms instead of waiting 1.2 s, retries at 250 ms while usable artist/title metadata is absent, and settles to 750 ms once a valid song identity exists. Network lookup remains asynchronous and exact matching/canonicalization rules from TEST86/87 are unchanged. Native RdsInfoDisplay/DAB handling remains untouched. This can remove renderer-introduced waiting but cannot make broadcaster RDS arrive earlier. Package 1.0.5-test88; physical startup timing verification pending.

- TEST89 RADIO startup latency diagnostic candidate (2026-10-03): physical TEST88 TV→RADIO test still needed about 5 seconds before BAYERN 3 station/song information appeared, so no further blind timer reduction is being made. Added timestamped renderer diagnostics for START, first current SERVICE, first non-empty RADIOTEXT, first parsed SONG and REQUEST. Existing LOOKUP/READY diagnostics then expose network/artwork time. This is diagnostic-only apart from retaining TEST88 100/250/750 ms polling; exact matching, TEST86/87 canonicalization, native RdsInfoDisplay and DAB/SLS are unchanged. Package 1.0.5-test89; physical timing log pending.

- TEST89 full-path correction (2026-10-03): CI #244 correctly rejected the first diagnostic revision because the intended renderer START marker was not actually present. OpenATV source audit confirmed the physical RADIO key action enters `InfoBar.showRadioButton`, which then calls `toogleTvRadio()` on the GigaBlue family before `showRadio()`. Added a narrowly scoped wrapper around `InfoBar.showRadioButton` at FullHDGlass session start: it writes the physical RADIO-button epoch before calling the untouched original handler. WarderRadioArtwork reads that timestamp and reports RENDERER_START/SERVICE/RADIOTEXT/SONG/REQUEST relative to the physical key event; existing LOOKUP/READY completes the chain. Native RdsInfoDisplay is still untouched. Receiver timing verification pending.

- TEST89 CI correction revision 243: CI #245 again stopped safely at static preflight because the renderer source still contained the old literal escaped-newline comment, so the RADIO-button-relative `RENDERER_START` block had not been inserted. Replaced that exact malformed block by position with the real timestamp correlation code. No receiver package from #245 was published; functional intent unchanged.
