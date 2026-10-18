# TEST212 — skin-matched menu backgrounds

- Source: owner-provided 121-image archive and approved six-image archive.
- Background-only change: exact edge-connected black matte pixels changed to PNG alpha 206, matching the skin's `#31000000` transparency setting. RGB channels are unchanged; non-background pixels are unchanged. No fade to alpha zero is used.
- Every runtime PNG is 810 × 810 RGBA. Each ZIP contains 125 unique PNG paths and passed CRC/decode checks.
- OpenATV `data/menu.xml` maps `deep_standby` to Deep Standby (shown in this skin as Vypnúť) and `standby` to Standby (Pohotovostný režim). Therefore `deep_standby.png` and `shutdown.png` use the approved power-button `Vypnut.png`; `standby.png` uses the distinct approved `Pohotovostny_rezim.png`.
- `downloads.json` now serves immutable TEST212 split archives and matching SHA-256 values.
- Test on receiver is pending; package-level checks do not confirm the rendered receiver output.
