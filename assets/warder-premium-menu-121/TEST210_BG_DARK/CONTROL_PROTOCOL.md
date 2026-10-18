# TEST210 menu image background correction

- Source: the two exact TEST209 menu icon ZIPs on `warder-modernization-work`; all 124 unique existing PNGs preserved.
- Correction: pixels previously encoded as black RGBA `(0,0,0,128)` now use a black backdrop with peak PNG opacity 206, matching skin color `#31000000` (skin transparency 49/255, opacity 206/255).
- Edge treatment: 56 px smoothstep fade to alpha 0 at the outer frame; no hard square edge.
- Artwork RGB and all non-background pixels are unchanged; PNG dimensions remain 810 x 810 RGBA.
- Runtime correction: provide `standby.png` as a byte-identical alias of `deep_standby.png` in each archive root.
- Archive validation: ZIP CRC test, all 125 PNG entries per ZIP decoded and checked for 810 x 810 RGBA, per-image SHA-256 recorded in `manifest.csv`.
- Result SHA-256: `menuIcons.zip` 08b44a95be718123268121896022d06ffbff075b2e327e06889211e2b650cf0b; `menuIconsBig.zip` f2a088bad8b59a8f8e1d411c985ac71885641030d070a8c6d2b945ec4615c627.
- Hardware display remains confirmed only by the owner’s next receiver test; these checks establish package contents, not receiver rendering.
