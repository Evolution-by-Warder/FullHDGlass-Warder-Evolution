# SuperMusic — TEST13 verification

SuperMusic is integrated in the radio lyrics worker in **1.0.38-test13**.

- Source: `83d4c2132c4d8a538c34574b5491aa0942363164`.
- Build [40873174108](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/40873174108): **259 tests passed**, 1,353 installed files verified.
- [Live comparison](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/40873173998): SuperMusic accepted **7/12 selected recordings**, including **Instinct — Dozadu**. This is a small regression sample, not a catalogue coverage estimate.
- Search links use the canonical `idpiesne` query. The worker maintains the public visitor session across requests, bounds validation work, and checks artist, title and recording before extracting chord-free text.
- No shared API token or external Python package is required. Production feeds remain at **1.0.37**; TEST13 is an isolated prerelease.
- Public IPK independently downloaded: **14515418 bytes**, SHA-256 `5598f065261b4d935d63003c818280e315ec91e047700e1ccdc3ddaf2f1008b3`.
- Owner confirmed TEST13 functional on the receiver on 29 October 2026; production promotion authorized as 1.0.39. Detailed evidence and per-source outcomes: [RADIO-SUPERMUSIC-TEST13.json](RADIO-SUPERMUSIC-TEST13.json).

[Download TEST13 IPK](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/download/radio-lyrics-1.0.38-test13/enigma2-plugin-skins-fullhdglass-warder-evolution_1.0.38-test13_all.ipk)
