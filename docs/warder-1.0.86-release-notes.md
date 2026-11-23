# FullHDGlass – Warder Evolution 1.0.86

**Ostré opravné vydanie – 23. november 2026.** Nadväzuje na potvrdenú verziu 1.0.85. Opravuje nedostatok dočasného priestoru pri sťahovaní veľkých SAT picon balíkov.

## Oprava SAT piconov: 13°E, 19,2°E a ďalšie veľké balíky

- Používateľ nahlásil chybové hlásenia `insufficient temporary space for Warder channel package` pri pozíciách **13°E** a **19,2°E**; balík **23,5°E** sa stiahol na 100 %. Toto hlásenie nepreukazuje poškodenie archívov ani nedostatok miesta na zvolenom HDD.
- Doteraz sa pracovný ZIP povinne sťahoval do `/tmp`, ktoré môže byť na Enigma2 prijímačoch malé a nezávislé od voľného miesta na HDD/SSD. V 1.0.86 sa pracovný ZIP vytvára **priamo v už overenom cieľovom adresári piconov** na používateľom vybranom úložisku.
- PNG sa z ZIPu čítajú postupne a ukladajú pomocou dočasného súboru a atómového nahradenia; nevyžaduje sa rozbalenie celého archívu do pamäte alebo iného adresára.
- Pred stiahnutím zostáva konzervatívna kontrola voľného miesta pre veľkosť balíka a rozbalenie. Navyše sa musí ponechať **64 MiB (približne 67 MB) voľného miesta** pre systém.
- Zachované sú kontroly manifestu, URL, veľkosti jednotlivých častí, **SHA-256**, bezpečnosti PNG a zákazu nebezpečných ciest či symlinkov. Pracovný ZIP sa automaticky odstráni po dokončení alebo chybe. Existujúce používateľské picony sa hromadne nemažú.
- Ak na vybranom médiu naozaj nie je dostatok miesta, sťahovanie sa bezpečne zastaví s príslušným hlásením.

## Čo zostáva zachované

- Všetky opravy 1.0.85: správne rozostupy staníc, veľkosti piconov a EPG, rolovanie dlhých názvov programov, diagnostický riadok „Máš zvolené“ aj nápoveda Picon Setup.
- Schválené originálne obrázky, SAT/rádiové balíky, servisné referencie, nastavenia ciest, existujúca konfigurácia a Warder Radio Live zostávajú bez zmeny. Nie sú pridané ani nahradené grafické súbory.
- Kompatibilita sa overuje v automatických kontrolách OpenATV a OpenPLi. **Fyzické prijímačové potvrdenie opravy práve na 13°E a 19,2°E ešte nebolo dodané.** Zdrojové a automatizované testy nie sú náhradou za každú kombináciu boxu, image a úložiska.

## Aktualizácia

Balík: `enigma2-plugin-skins-fullhdglass_1.0.86_all.ipk`.

Oficiálny [GitHub Release 1.0.86](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/v1.0.86) a [priame stiahnutie IPK 1.0.86](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/download/v1.0.86/enigma2-plugin-skins-fullhdglass_1.0.86_all.ipk) sú platné až po úspešnom vydaní.

Ostré aktualizačné kanály `update-production.json` a `update-test.json` sa aktualizujú až po overení finálneho vydania a jeho SHA-256; pôvodný migračný `update.json` a jeho balík 1.0.18 zostávajú chránené.

Po aktualizácii reštartujte Enigma2.
