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
- **SHA-256 a veľkosť:** musia sa doplniť až z úspešne publikovaného ostrého artefaktu. Autoritatívne hodnoty sú v `update-production.json` a `main/packages/*.sha256`; nevydávajte testovací checksum za ostrý.
- **Aktualizácia:** publisher `publish-warder-stable.yml` najprv vytvorí nemenný Release, potom aktualizuje `update-production.json` a `update-test.json`.
- **Predchádzajúce ostré verzie:** 1.0.85 / 1.0.84 / 1.0.83. Chránený migračný bootstrap 1.0.18 a historický TEST 1.0.72 sa nezapočítavajú do štyroch ostrých verzií.
- **Kompatibilita:** automatické testy OpenATV a OpenPLi sú povinnou podmienkou. Fyzické otestovanie nového ZIP pracovného adresára na konkrétnom prijímači ešte nie je doložené.

Po aktualizácii **reštartujte Enigma2**. Vydanie sa považuje za zverejnené až po úspešnej koncovej kontrole SHA/IPK/feed/Release.
