# FullHDGlass 1.0.45

Kompatibilita s aktuálnym OpenATV po refaktorovaní EPG a systémových obrazoviek.

- MultiEPG znova vytvára všetky štyri farebné popisy a pripája ich k skutočnému novému ovládaču mriežky. Červené otvorí náš PROGRAM INFO, zelené časovač, žlté dátum/čas a modré vyhľadávanie EPG. Ošetrené opakované stlačenie aj návrat z PROGRAM INFO. Starší ovládač zostáva podporovaný.
- Nové nastavenia EPG používajú aktuálnu štruktúru a platné identifikátory akcií. Zachované rozloženie GraphicalEPGPIG, PIG, počet riadkov a picony. Bežné GraphicalEPG správne vykresľuje zdroje farebných popisov.
- Video kodeky používajú autoritatívnu tabuľku OpenATV vrátane AVS2; zachované staršie tabuľky a náhradné načítanie z ovládača.
- Rodičovská ochrana a zmena PIN obsahujú nové povinné popisy a pätičku; staršie systémy si zachovajú pôvodný zoznam. Správca balíkov zobrazí novú modrú voľbu vyhľadávania a MENU. Textový dialóg zobrazí nové červené ukončenie. Spoločné Setup zobrazí voliteľnú voľbu MENU.

Kontrola aktuálnych rozhraní OpenATV je povinnou podmienkou zostavenia a beží aj denne na Gite. Nepridáva diagnostiku ani prácu na prijímači. Podrobnosti a overené revízie sú v [zázname kontroly](OPENATV-COMPATIBILITY-20261030.md).

Inštalačný súbor má výhradne krátky názov. Aktualizátor ponúkne 1.0.45 ako bežnú aktualizáciu. Schválená animácia rádia, klávesnica, picony a rádio bouquet zostávajú zachované.

Overené automatickými kontrolami; nové opravy ešte vyžadujú potvrdenie na fyzickom prijímači.
