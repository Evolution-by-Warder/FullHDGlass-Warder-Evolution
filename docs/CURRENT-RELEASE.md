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

Oficiálny Release, SHA-256 a stav produkčného/testovacieho aktualizačného kanála sa potvrdzujú až po skončení kanonického publikačného workflow. Aktuálnu verziu na stiahnutie určuje súbor `update-production.json`.

**Po aktualizácii reštartujte Enigma2.**
