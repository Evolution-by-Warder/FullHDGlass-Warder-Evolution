# FullHDGlass Warder Evolution — TEST256

- Nápovedné obrázky majú vnútorné odsadenie a zachovaný pôvodný pomer strán. Zmestia sa medzi oddeľovaciu čiaru a spodný rám, bez presahu do tlačidiel.
- Bežná zvolená hodnota sa neopakuje v spodnom strede. Viditeľná zostáva priamo v riadku nastavenia.
- Užitočná ukážka skutočne naformátovaného dátumu a náhľad konkrétnej farby zostávajú zachované.
- Zachováva čistú pätu a názvy rozhrania aj súboru IPK bez 17 z TEST255. Vnútorná identita balíka sa nemení, existujúca inštalácia sa aktualizuje na mieste.

```sh
opkg install /tmp/enigma2-skin-fullhdglass-warder-evolution_1.0.16-test256_all.ipk
```

Reštartovať GUI. Overiť nápovedné obrázky v ECM, SIEŤ a MENU, okraje rámu, čistý stred päty a náhľady dátumu/farby. Zobrazenie TEST256 na prijímači zatiaľ nie je potvrdené.

Kontroly: 17 testov vrátane odsadenia náhľadov, pomeru strán, spoločného načítania obrázkov vo všetkých konfiguračných skupinách, odstránenia duplicitnej hodnoty a zachovania callbackov. Ďalej runtime-safety, rádiový/grafický základ a úplná zhoda obsahu IPK. Aktualizačné feedy zostávajú 1.0.15. Pôvodné obrázky ani ich obsah sa nemenia, opravuje sa ich rozloženie.
