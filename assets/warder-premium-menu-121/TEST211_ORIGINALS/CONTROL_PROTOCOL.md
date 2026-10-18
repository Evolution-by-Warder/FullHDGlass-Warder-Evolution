# TEST211 original menu image delivery

- Source collection: owner-provided `WARDER_121_ORIGINALY_JEDNOTNE_POZADIE_BEZ_DEGRADACIE(2).zip` and approved six-image ZIP.
- Existing 121 PNG payloads are preserved byte-for-byte from the owner-provided source; every file is 810 × 810 RGBA. No resampling, RGB edits, alpha ramps, or generated images were applied.
- The original collection’s outer-corner matte is black alpha 128. The six approved replacement artworks have black alpha 145. Existing fades to alpha zero were removed by packaging the original pixels directly.
- Updated runtime mappings: `plugin_selection.png` ← `Prehliadac_pluginov.png`; `e.png` ← `Rozsirene_pocasie.png`; `information.png` ← `Informacie.png`; `shutdown.png` ← `Vypnut.png`; `deep_standby.png` and `standby.png` ← `Pohotovostny_rezim.png`; `restart_enigma.png` ← `Restartovat_GUI.png`. `shutdown.png` and standby artwork have different SHA-256 hashes. `timer_edit.png` uses the original `powertimer_edit.png`.
- Both runtime ZIPs passed CRC validation; all 125 PNG entries in each archive decode as 810 × 810 RGBA.
- `downloads.json` points to immutable TEST211 part paths and records each full archive size and SHA-256.
- Receiver-side rendering and actual menu display have not been tested on hardware.
