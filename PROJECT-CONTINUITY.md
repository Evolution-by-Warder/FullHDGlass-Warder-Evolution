# FullHDGlass17 Warder Evolution — Project Continuity

## Authoritative working state
- Repository: Evolution-by-Warder/FullHDGlass-Warder-Evolution
- Working branch: `warder-modernization-work`
- `main` is TABU: no merge, push, edit or runtime-development switch to main.
- Checkpoint before this continuity commit: `9ed08e31eab3134b573552fbbaa5c59754aad6b6`
- Current workstream: Warder download backend / legacy FTP migration / channel-picon cut-over.

## Radio — LOCKED
Full Radio implementation is PHYSICAL PASS on TEST191 and must not be modified without explicit approval or new receiver regression evidence.

Locked:
- artwork renderer: `WarderRadioArtwork`
- position: `606,145`
- size: `704,640`
- approved background/TOP/BOTTOM basis: TEST171
- equalizer, DAB SLS, fallback artwork, matcher
- clean TV -> Radio -> TV behavior

Do not return Radio TOP to eCanvas/writeText. Radio runtime is out of scope for backend work.

## Legacy FTP migration
`assets/warder/legacy-ftp-migration.tsv` is the migration registry.
Historical inventory: 27 files = 19 asset families + 8 archive-only skin/package/changelog files.

Routes:
- 18 WARDER_MANIFEST
- 1 NOT_EXPOSED
- 8 ARCHIVE_ONLY
- 0 LEGACY_FTP

18/18 Warder-routed current SHA256 values match `assets/warder/downloads.json`.
Missing preserved source: `weatherIcons/piconWeather.zip` = SOURCE_PRESERVED_TARGET_MISSING / NOT_EXPOSED. Never invent a payload.
SH4 `7zip-s` is not published and must never be advertised/invented.

## Runtime network policy
Runtime endpoint audit is enforced by CI.
Classified hosts include Warder GitHub, functional APIs and one isolated legacy picon source.
The remaining legacy channel-picon dependency is `https://picon.cz/download/%s/` in `downMulti()`.
Do NOT remove or switch it until the Warder replacement is persistently published and separately validated.

## Channel-picon migration
SATLIST: exactly 57 selectors.
- 40 MATCHED
- 38 READY
- 2 collision-blocked: 08W, 160E
- 17 MISSING

Collision policy:
- same SHA: deterministic dedupe
- different SHA: HARD FAIL
- no silent conflict resolution

Eligible source families:
- channel-transparent
- channel-black
- channel-white

Unresolved:
- channel-400x240
- channel-220x132
- channel-black-50x30
- channel-white-50x30
- channel-oled

38 READY x 3 eligible families = 114 deterministic packages.

## Verified build evidence
Historical verified workflow run: `37222927731`
- conclusion: SUCCESS
- source PiconHub commit: `2827fed5b2e6ae4697f08ca57a8c2298079d410f`
- artifact: `warder-channel-picons-2827fed5`
- artifact id: 11311027106
- size: 615370960 bytes
- digest: `sha256:ed2e2ae42bf95e6e5db4500034c59136bd82a791c05e99e6f1b9d73670ebee95`
- expires: 2026-10-18T18:06:02Z

This Actions artifact is temporary build evidence, NOT a persistent receiver backend.

## Latest backend hardening commits
- `1fb8c51f6e30ae04ae7c020ae0f76b27f197d786` — add persistent picon publication payload validator
- `9645439ef08227788f6b1dcef09ae8fffcfd8461` — gate picon builds on publication payload integrity
- `1cbb5f1635de194b76f0102a7abf29c07648c153` — gate TEST builds on unpublished picon runtime lock
- `5a91e8a19c664e9a7499d39900a7c06f218cff94` — separate picon publication from runtime cutover
- `9ed08e31eab3134b573552fbbaa5c59754aad6b6` — trigger hardened channel-picon build

New `tools/validate-picon-publication.py` requires:
- exactly 114 packages
- 114 unique selector/family pairs
- exact manifest <-> ZIP set
- canonical Warder HTTPS URLs
- physical size match
- SHA256 match

Publication and runtime cut-over are deliberately separate gates.
Current recorded publication state remains NOT_PUBLISHED and runtime_cutover=false.

## Next work
Continue autonomously in large batches:
1. Inspect the workflow run triggered by `9ed08e31...`; if failed, inspect logs, fix and rerun until successful.
2. Establish a safe persistent publication mechanism for all 114 ZIPs + manifest without touching `main`.
3. Verify published objects independently by count, size, SHA256, canonical URL and manifest consistency.
4. Only after persistent publication is proven may the publication contract become PUBLISHED.
5. Keep runtime_cutover=false and keep picon.cz active until a separate explicit cut-over change is safe and validated.
6. Extend CI so incomplete/stale/mismatched publication cannot pass.
7. Prefer real validators/tools/fixes over prose-only work.
8. Never modify locked TEST191 Radio.
9. Never modify main.
10. Stop only for physical receiver test, destructive action, architecture decision, Release, or a real blocker.

## TEST build rule
When user asks `daj mi test`: trigger TEST build; inspect run/jobs/gates; fix any failure and rerun; wait for SUCCESS; verify IPK, update-test.json, TEST version and SHA256; only then say it is ready to install. PHYSICAL PASS is declared only by the user's receiver test.

## 2026-10-05 channel-picon backend continuation
- Split publication candidate run 37262475228: SUCCESS.
- Artifact 11324632930, 1,230,749,855 bytes, digest sha256:55a14f5f13b2c05a6e471406ea762e2496fd6680c8cbc5a7a956fc7bf9d9bce2, expires 2026-10-19T04:13:52Z.
- Existing Warder raw-GitHub multipart delivery model selected for channel-picon publication preparation; no Release required at this stage.
- Per-part integrity added: each .partNN must have manifest bytes + SHA256 and SHA256SUMS; exact part set enforced.
- First per-part run 37262643909 failed correctly because generator omitted the new part metadata from final JSON; validator blocked publication. Generator fixed in e01e71eeb20e4b2d96d1fdd494af63348e93022c.
- Retry triggered by 25d550e1fd97c1b2c97ae076ba733bf16aa8c235; run 37262827959 pending/in progress at checkpoint time.
- Verified split build evidence recorded in assets/warder/channel-picon-build.json by 9b9a42e12c1152c96224a56927c7ee5f419f65fb.
- Publication remains NOT_PUBLISHED and runtime_cutover=false. picon.cz remains the runtime fallback. Radio TEST191 and main remain untouched.

## 2026-10-05 authoritative lean publication hardening
- Historical split candidate SUCCESS remains run 37262475228 / artifact 11324632930.
- Runs 37262643909 and 37262827959 correctly failed publication gates while per-part metadata writer was incomplete/broken; source package materialization itself passed.
- Run 37262963590 confirmed the old preparer syntax defect; superseded by clean rewrite a07ea75a712b8bb10b45b442ec84d32a5a2a7363.
- Workflow compile gate corrected and artifact duplication removed in 808be036c4b5badf49df12392078c95dbbd5c54c.
- Authoritative lean rebuild trigger: 87ce10d6c6a93aa2e43b2850429af1dfbd5b531f, run 37263153529.
- Production validator now pins exactly the stable main raw path and raw-github-parts delivery (d5900d63571bab66a543e380f9f044bc5c078fe2).
- Publication contract remains PREPARED_NOT_PUBLISHED; runtime_cutover=false; main and Radio TEST191 untouched.

## 2026-10-05 full-reassembly channel-picon checkpoint
- Authoritative full-integrity SUCCESS: run 37263263434, head e2daca746f6de236019e7a6946dec741cadb8188.
- Artifact 11325098173, 615397302 bytes, digest sha256:09fc63bae59cff85ab12ad5dc88c425699e2f4008cef91d4c4e424a4650dda79, expires 2026-10-19T04:24:32Z.
- Contract: 114 packages materialized as 124 persistent raw-GitHub parts.
- Integrity chain PASS: source package size/SHA256, every part size/SHA256, canonical ordered part URLs, streamed reassembly of every package back to its full byte count and SHA256.
- Build evidence promoted in 19579d13b11ab17424d39a3f15dac4d60c4b895e.
- Cut-over validator now requires full reassembly PASS evidence (ba0b54cf7b5ad32a2119023ba94d1d8122265f38).
- State remains BUILT_NOT_PUBLISHED / PREPARED_NOT_PUBLISHED; runtime_cutover=false.
- Remaining architectural boundary: physically persist ~615 MB split payload + manifest under stable main assets/warder/downloads/picons/channels, then separately validate and enable runtime cut-over.
- main remains TABU and untouched; picon.cz remains the single isolated channel-picon runtime fallback; Radio TEST191 remains locked and untouched.
