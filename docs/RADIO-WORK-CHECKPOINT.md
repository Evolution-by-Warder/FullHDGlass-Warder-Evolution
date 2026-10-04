# FullHDGlass17 Warder Evolution — RADIO work checkpoint

Branch: `warder-modernization-work`  
`main` is TABU.

## Mandatory completion order

1. COVER — PHYSICAL PASS on TEST178. Locked geometry: position 606,145; size 704,640. Preserve the thin visible background gap between frame and artwork on all four sides. Do not change without new physical evidence.
2. SONG MATCHER — PHYSICAL PASS on TEST179. Receiver test found correct artwork for normal songs and correctly rejected non-song RDS entries (Studio-Hotline, Internet URL, BAYERN 3 slogan). Chris de Sarandy / Good Old Days remained blank because the catalogue returned only unrelated Hurts Like This results; do not loosen matching for missing catalogue data. Lock TEST179 matcher unless new physical evidence shows a wrong artwork.
3. RADIO WITHOUT RDS — mandatory before RADIO can be closed:
   - keep the normal RADIO screen and TOP;
   - show all service data available from `session.CurrentService`;
   - at minimum: picon + station/service name + provider;
   - do not open or attach the real InfoPanel screen;
   - reuse CurrentService/InfoPanel-type service sources;
   - do not invent song/artist/artwork when RDS metadata is absent;
   - equalizer may remain visible.
4. MOVING EQUALIZER — individual bars should move naturally/independently.
5. DAB — physically verify picon, station/service name, provider, DAB text, SLS and passive `radio.mvi` fallback.
6. Only after physical receiver verification of all above may RADIO be marked PHYSICAL PASS / locked.

## Locked constraints

- TEST171 TOP/BOTTOM composition is the approved reference.
- Preserve Radio ownership/lifecycle separation from InfoPanel.
- Preserve `RdsInfoDisplay` zPosition `-2`.
- Preserve DAB SLS/passive `radio.mvi` fallback.
- Do not use eCanvas/writeText for Radio TOP.
- No black masks/patches.
- TV must never receive Radio TOP.
- Do not declare PHYSICAL PASS without explicit receiver confirmation.
