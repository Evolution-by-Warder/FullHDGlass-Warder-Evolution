# FullHDGlass – Warder Evolution 1.0.87 (aktuálna ostrá verzia)

**Ostré vydanie: 23. november 2026.** Vlastník potvrdil opravy na prijímači **Octagon SF8008** a prikázal vydať stabilnú verziu.

## Opravené sťahovanie SAT piconov

- Predtým program nesprávne hlásil chýbajúce rozlíšenie/farbu/režim alebo „Neplatné umístění pikonů“ aj pri správnom výbere. Rozlišuje teraz kontrolu nastavení a bezpečnosť cieľového adresára.
- Rozpoznáva presne existujúcu cestu `/usr/share/enigma2/hdg17_files/picon → /usr/share/enigma2/picon`; ostatné nebezpečné alebo nepripojené symbolické odkazy zostávajú blokované.
- Ak je na internom úložisku aspoň **512 MiB pracovného priestoru nad 64 MiB systémovou rezervou**, sťahovanie sa spustí bez zbytočného upozornenia. Pri menšom priestore sa upozornenie zobrazí; pri kritickom nedostatku pokračovanie nie je možné.
- Zachovaná je kontrola skutočnej veľkosti každého archívu, SHA-256, bezpečné PNG zápisy, čistenie dočasných súborov a všetky existujúce picony/nastavenia.

**Test SF8008:** 19,2°E – 145 aktualizovaných piconov, 0 chýb; 23,5°E – 184 piconov; následné odstránenie zbytočného upozornenia potvrdené používateľom.

## Oficiálny Release a aktualizácia

[Release v1.0.87](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/v1.0.87) · [Stiahnuť IPK 1.0.87](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/download/v1.0.87/enigma2-plugin-skins-fullhdglass_1.0.87_all.ipk) · [Úplné poznámky](warder-1.0.87-release-notes.md)

- **Balík:** `enigma2-plugin-skins-fullhdglass_1.0.87_all.ipk`
- **Veľkosť:** 18 394 364 B
- **SHA-256:** `099925944074f9d1e7678d4d6e0ac3ca4b85a90a95940a9850b7d6cd2ce6a04c`
- **Vydávací workflow:** [#45245269154](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/45245269154), **COMPLETED / SUCCESS** vrátane koncového `verify-production-release-state.py`.
- **Aktualizačné kanály:** `update-production.json` aj `update-test.json` obsahujú 1.0.87 s rovnakým overeným SHA-256 a lokalizovanými poznámkami v desiatich jazykoch.
- **Zachované ostré verzie na návrat:** 1.0.86, 1.0.85, 1.0.84. Migračná 1.0.18 zostáva samostatne chránená.

Po aktualizácii **reštartujte Enigma2**.
