# FullHDGlass17 Warder Evolution — RADIO work checkpoint

Branch: `warder-modernization-work`  
`main` is TABU.

Updated: 2026-10-04  
Authoritative physical checkpoint: **TEST191**.

## Current RADIO acceptance state

1. **TOP/BOTTOM composition — PHYSICAL PASS / LOCKED**
   - Receiver-approved reference: TEST171.
   - TOP yellow `#FFE16A`; date left, clock centered, brand right.
   - BOTTOM keeps picon, station, song/RDS line, blue technical line, equalizer and provider.
   - `RdsInfoDisplay zPosition="-2"` remains required.
   - Radio ownership/lifecycle must stay separated from InfoPanel; TV must never receive Radio TOP.

2. **COVER geometry — PHYSICAL PASS / LOCKED**
   - Receiver-approved reference: TEST178.
   - Renderer: `WarderRadioArtwork`.
   - Position: `606,145`.
   - Size: `704,640`.
   - Preserve frame line -> thin visible background gap -> artwork on all four sides.
   - Do not change geometry without new physical receiver evidence.

3. **SONG MATCHER — PHYSICAL PASS to tested scope / LOCKED**
   - TEST179 approved normal-song matching and rejection of non-song RDS entries.
   - TEST180 added controlled catalogue-credit relaxation.
   - Preserve strict matching; never fabricate artist/title/artwork.
   - HUNTR/X was not physically exercised during TEST180, so do not claim that specific case as receiver-verified.

4. **APPROVED NO-COVER FALLBACK — LOCKED**
   - File: `/usr/share/enigma2/hd_glass17/warder-radio-no-cover.png`.
   - Repository blob SHA: `a5c18ecc9572472cd9867aacac6c4e70f4f8a16e`.
   - Text: `ŽIADNY OBAL`, `COVER NIE JE DOSTUPNÝ`, `COVER IS NOT AVAILABLE`.
   - Used when no valid cover/SLS is available. Never invent metadata.

5. **RADIO WITHOUT RDS — PHYSICAL PASS / LOCKED**
   - Receiver-approved reference: TEST183.
   - Classic DVB radio service type 0x02 (`"2"`) and 0x0A (`"A"`) are recognized.
   - Physical BBC English test confirmed Radio background/TOP, fallback, picon, station, equalizer area and provider.
   - RDS text may arrive with a short normal delay; this is not a defect unless it never arrives or becomes excessive.

6. **MOVING EQUALIZER — PHYSICAL PASS / VISUAL LOCK**
   - TEST187 proved the receiver path using legacy FullHDGlass17 `eCanvas` sizing in `applySkin`.
   - TEST188 changed animation interval only: 200 ms -> **140 ms**.
   - Geometry remains x1470 y838, size 350x126, 18 independently moving deterministic bars.
   - Do not remove explicit `eCanvas.setSize` receiver-proven pattern.
   - Do not redesign equalizer visuals unless explicitly requested.

7. **DAB metadata + SLS — PHYSICAL PASS / LOCKED on TEST191**
   - TEST189 legacy RASS polling: PHYSICAL FAIL.
   - TEST190 `evUpdatedRassSlidePic` / `showRassSlidePicture()`: PHYSICAL FAIL; DAB-over-DVB path emitted no legacy RASS event.
   - TEST191 uses the actual OpenATV 8 DAB slideshow path: current DAB service `iServiceInformation.sTagPreviewImage`.
   - Warder renders that native MOT slideshow image inside the locked center artwork frame and gives active DAB SLS priority over catalogue/fallback.
   - Physical receiver PASS confirmed on:
     - Schwarzwaldradio — transmitted “Wetter melden” SLS.
     - ENERGY — transmitted NRJ “HIT MUSIC ONLY!” SLS.
     - SCHLAGERPARADIES — transmitted current-program/moderator SLS.
   - During all three physical tests the picon, station, DAB technical line, provider and moving equalizer remained present.
   - Preserve passive `radio.mvi` fallback behavior.

## TEST191 authoritative build checkpoint

- Runtime version: `1.0.5-test191`.
- Control version: `1.0.5-test191-1`.
- Published package: `packages/test/enigma2-skin-fullhdglass17-warder-evolution_1.0.5-test191_all.ipk`.
- Package SHA256: `a99e309776615c2cc8ded5467d552ba3669fdc88e97860f39a4f89acfc43109e`.
- Build workflow run: `37220612169` — SUCCESS.
- CI publication commit: `2f9b396a0fa8905e54e833d3861cb67606ed825c`.
- `update-test.json` points to TEST191 and carries the same SHA256.
- Static gates, XML parse, lifecycle/package/runtime guardrails, r1-r12 regression gate, TEST93 radio master SHA/geometry, compiled Slovak weather catalogs and final IPK integrity all passed.

## Diagnostics retained

- `/tmp/warder-radio-artwork/`
- `/tmp/warder-radio-artwork.log`
- `/tmp/warder-radio-current`
- `/tmp/warder-radio-service-events.log`
- `/tmp/warder-radio-webif-hook.log`
- `/tmp/warder-radio-webif-error.log`
- TEST191 logs `DAB_SLS_SHOW ... path=...` when native DAB SLS is detected.

## Binding constraints

- Preserve TEST171 TOP/BOTTOM composition.
- Preserve TEST178 cover geometry.
- Preserve approved fallback graphic.
- Preserve TEST179/180 controlled matcher behavior.
- Preserve TEST183 non-RDS radio classification.
- Preserve TEST187 receiver-proven eCanvas equalizer lifecycle/sizing and TEST188 140 ms interval.
- Preserve TEST191 native DAB `sTagPreviewImage` SLS path.
- No eCanvas/writeText implementation for Radio TOP.
- No black masks/patches.
- TV -> Radio -> TV must remain clean.
- TMDB remains unchanged.
- Never mark a new behavior PHYSICAL PASS without explicit receiver confirmation.

## WHOLE RADIO PASS — PHYSICAL PASS / LOCKED — 2026-10-04

User explicitly approved the final combined TEST191 receiver regression with **“beriem”**.

Physical evidence in the final pass confirms:
- DAB SLS: SCHLAGERPARADIES displayed the transmitted programme/moderator slideshow while DAB metadata, picon, provider and moving equalizer remained correct.
- Normal RDS artwork: BAYERN 3 / Fast Boy — Music Sounds displayed the matched real cover with station/RDS metadata, provider and moving equalizer.
- No-cover path: 1LIVE displayed the approved Warder fallback with station/picon/provider and moving equalizer, without invented metadata.
- Return to TV: TV JOJ HD displayed the normal TV InfoPanel after leaving Radio; Radio TOP/background/artwork/equalizer were absent.

Therefore **WHOLE RADIO = PHYSICAL PASS / LOCKED on TEST191** for the tested receiver path. Radio is closed as an accepted feature baseline. Future work must preserve this state and may reopen it only for new physical regression evidence or an explicitly approved enhancement.

WebIF remains governed by its existing implementation/regression guards; this final screenshot sequence specifically proves the on-receiver TV -> Radio modes -> TV lifecycle.
