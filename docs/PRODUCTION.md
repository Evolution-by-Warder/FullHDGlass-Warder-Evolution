# FullHDGlass Warder Evolution — ostrá prevádzka

Schválené vlastníkom **24. októbra 2026** spolu s PiconHubom **0.1.25**. Produkčná verzia skinu: **1.0.17**, bez označenia test.

## Schválený základ a číslo verzie

Vydanie vychádza z používateľom prijatého TEST270. Zachováva jeho funkcie, grafiku, banner, geometriu aj nastavenia. Mení verziu runtime, verziu IPK a zobrazené číslo v hlavičkách na 1.0.17. Vývojové testovacie vydania a ich tagy ostávajú zachované.

[Produkčné vydanie](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/v1.0.17) · [IPK](https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/packages/enigma2-skin-fullhdglass-warder-evolution_1.0.17_all.ipk)

Presný zdrojový commit, veľkosť a SHA256 vzniknú pri overenom zostavení a sú zapísané v [PRODUCTION.json](PRODUCTION.json). Schválenie a totožnosť východiskového TEST270 sú v [PRODUCTION-APPROVAL.json](PRODUCTION-APPROVAL.json).

## Aktualizácie a náhľady

Oba existujúce aktualizačné kanály sa prepnú na 1.0.17 až po overení verejného IPK. Verzia 1.0.17 je vyššia než 1.0.16-test270 v prijímačovom aktualizátore aj v správcovi balíkov. Nie je potrebné vynútenie downgrade ani zavedenie epochy.

Základný IPK zostáva malý, s limitom pod 16 MiB. Nápoveda (24 621 325 bajtov) a typy infobaru (2 584 364 bajtov) sa naďalej dopĺňajú na pozadí a overujú podľa SHA256. Už uložené náhľady fungujú bez siete. TEST263 zostáva nemenným zdrojom týchto archívov a nesmie sa odstrániť.

## Zachovaný stav

Spoločný banner, nižší horizont zemegule, čitateľné sekundy, dvojriadková verzia a zarovnanie hlavičky. Schválená menšia ikona, jednotné nepriehľadné konfiguračné a aktualizačné dialógy, opravy callbackov výberových okien, existujúce ovládanie, rádio, piconový katalóg a nastavenia zostávajú zachované. Pôvodné autorské údaje Shamann a kompatibilné runtime identifikátory sa nemenia.

## Overenie a obnova

Produkčné zostavenie kontroluje každý súbor payloadu, bezstratovú kompresiu PNG, metadáta balíka, hlavičky, ovládače, cache Pythonu, poradie verzií a nezávislé archívy náhľadov. Verejné IPK sa overí podľa veľkosti a SHA256 pred zmenou aktualizačných feedov. Finálny produkčný záznam viaže tieto kontroly na konkrétny zdrojový commit a workflow.

Používateľ prijal aktuálny skin do ostrej prevádzky. Nejde o tvrdenie o novom úplnom fyzickom teste všetkých funkcií, boxov a image. Historické výsledky a crash logy zostávajú viazané na svoje verzie. Historická recovery 1.0.15, testovacie vydania, zdroje a kontrolné súčty ostávajú dostupné.
