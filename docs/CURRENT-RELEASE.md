# FullHDGlass – Warder Evolution 1.0.88 (aktuálna ostrá verzia)

**23. november 2026 – oprava natívnych posuvníkov nastavení.** Podkladom sú dve snímky od českého používateľa. Majiteľ projektu výslovne schválil vydanie ako 1.0.88.

## Natívne nastavenia obrazu a displeja

- Pri dlhších názvoch v češtine (vrátane „Nastavení korekce obrazu“ a „Nastavení displeje“) sa posuvník prekrýval s textom.
- `Components.ConfigList` pri veľkých obrazovkách FullHDGlass používal predvolené oddeľovanie 200 px. Pomocník v širokých zoznamoch (aspoň 1200 px) bezpečne rezervuje 55 % šírky pre názov, s najmenej 450 px ponechanými pre hodnotu/posuvník.
- Úzke pluginové okná a náhľadové dialógy sa nemenia; používateľské nastavenia a systémové moduly image nie sú upravované.
- Zostávajú všetky opravy 1.0.87 vrátane bezpečného sťahovania SAT piconov a 64 MiB systémovej rezervy.

**Overenie:** PR [#157](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/157); kontrolný [1.0.88-test1](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/45249486600) prešiel 6/6 cielených testov a kontrolou IPK/SHA. Opakovaný vizuálny test českého používateľa ešte nie je potvrdený; nepovažuje sa za prijímačovo overenú opravu.

## Oficiálna publikácia a aktualizácie

[Oficiálny Release v1.0.88](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/v1.0.88) · [Stiahnuť IPK 1.0.88](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/download/v1.0.88/enigma2-plugin-skins-fullhdglass_1.0.88_all.ipk) · [Poznámky k vydaniu](warder-1.0.88-release-notes.md).

**Publikovanie overené 23. novembra 2026:** PR #157 bol zlúčený do `main` (squash commit `e595a1aae8a49d2fcee7b54973927e8581a513bc`), všetkých **24/24** automatických kontrol na finálnom HEAD prešlo. Kanonický vydávací [workflow #45252364033](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/45252364033) skončil **COMPLETED / SUCCESS** vrátane koncového `verify-production-release-state.py`.

- **IPK:** `enigma2-plugin-skins-fullhdglass_1.0.88_all.ipk`
- **Veľkosť:** 18 394 974 bajtov
- **SHA-256:** `0da1f61a4e675ffc7b548d423430e9673230551d5bbc24e77598d5128d687c28`
- **Verejný Release:** `v1.0.88`, nie draft ani prerelease
- **Aktualizácia:** `update-production.json` aj `update-test.json` → `1.0.88`, rovnaký SHA-256 ako vydaný asset, lokalizované poznámky v 10 jazykoch
- **Zachovaná predchádzajúca verzia:** `1.0.87` a všetky jej schválené opravy

Nie je doložené následné fyzické pretestovanie oboch obrazoviek českým používateľom; táto skúška zostáva požiadavkou na následné overenie bez blokovania výslovne schváleného vydania.

**Po aktualizácii reštartujte Enigma2.**
