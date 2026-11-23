# FullHDGlass – Warder Evolution 1.0.86 (aktuálna ostrá verzia)

**Opravné vydanie schválené vlastníkom 23. novembra 2026.** Predchádzajúca verzia 1.0.85 zostáva dostupná na návrat. Vydanie 1.0.86 rieši zlyhania SAT picon balíkov spôsobené malým dočasným úložiskom `/tmp`.

## Hlavná oprava

- Pri sťahovaní piconov pre **13°E** a **19,2°E** sa objavovalo hlásenie `insufficient temporary space for Warder channel package`, hoci pracovný HDD/SSD mohol mať dostatok miesta.
- Overovaný ZIP sa teraz dočasne uloží **na zvolené médium s piconmi**, nie do malého `/tmp`. PNG sa zapisujú bezpečne a priebežne do cieľového adresára; ZIP sa po operácii odstráni.
- Zachovaná kontrola **SHA-256**, bezpečnosť ciest a ZIP/PNG, atómová inštalácia a rezerva **64 MiB** voľného miesta pre systém. Ak na vybranom médiu skutočne chýba miesto, operácia sa bezpečne odmietne.
- Zlepšenia 1.0.85 pre výber kanálov, picony, EPG, GLES a konfiguračný diagnostický riadok ostávajú bez zmeny. Zachované sú grafické balíky, Warder Radio Live aj používateľské nastavenia.

## Aktuálna inštalácia a bezpečný návrat

[Oficiálny Release 1.0.86](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/v1.0.86) · [IPK 1.0.86](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/download/v1.0.86/enigma2-plugin-skins-fullhdglass_1.0.86_all.ipk) · [Úplné poznámky](warder-1.0.86-release-notes.md)

- **IPK:** `enigma2-plugin-skins-fullhdglass_1.0.86_all.ipk`.
- **Veľkosť IPK:** **18 393 684 B**.
- **SHA-256:** `40ff2a80fbe32b7c7b69c2b61335fca64d6e00bbc37489e4e5efe2972561f6c2`. Overené na oficiálnom Release assete, v `main/packages/*.sha256` aj v `update-production.json` a `update-test.json`.
- **Oficiálne publikovanie:** [GitHub Actions #45184862599](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/45184862599) dokončené **SUCCESS** vrátane `verify-production-release-state.py`. Vydávací commit `6f66f7e744987e6ad968b4df2c84c0c6a24acad6`.
- **Aktualizácia:** publisher `publish-warder-stable.yml` najprv vytvorí nemenný Release, potom aktualizuje `update-production.json` a `update-test.json`.
- **Predchádzajúce ostré verzie:** 1.0.85 / 1.0.84 / 1.0.83. Chránený migračný bootstrap 1.0.18 a historický TEST 1.0.72 sa nezapočítavajú do štyroch ostrých verzií.
- **Kompatibilita:** automatické testy OpenATV a OpenPLi sú povinnou podmienkou. Fyzické otestovanie nového ZIP pracovného adresára na konkrétnom prijímači ešte nie je doložené.

Po aktualizácii **reštartujte Enigma2**. Vydanie je **skutočne publikované a koncová kontrola SHA/IPK/feed/Release úspešne prešla**.
