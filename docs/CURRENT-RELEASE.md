# FullHDGlass 1.0.38-test10 — spoločná oprava rádiového enginu

Jedna skúšobná verzia spája opravy chýbajúcich textov, obalov, poškodených údajov z vysielania a opakovania po výpadku zdrojov. Zachováva majiteľom schválenú kompaktnú grafiku rádia.

- Metadáta, texty a obaly používajú spoločnú identitu skladby. Číselný zápis `08 - názov - Pavel Roth` už nevytvára interpreta „08“. Explicitné overené varianty mien a kreditov riešia Žbirku/Limit, Neckářa, Hečkovcov, Táslera/IMT Smile a Martausovú/Magušinovú. Pravidlá a pôvod sú v `docs/RADIO-IDENTITY-RULES.md`.
- Pri rozpoznaných SK/CZ formátoch staníc, napríklad KIKS Československo a Fun Rádio Československé hity, sa Hudba.sk a LRCLIB skúšajú súčasne. Ostatné stanice zachovávajú prvý pokus LRCLIB; ďalšie zdroje začínajú najneskôr po 750 ms.
- Pripojené sú Ujdeto, Písničky-akordy a Tekstowo. Pri konkrétnej overenej skladbe Pavla Rotha sa používa aj jeho oficiálna stránka. Číta sa iba pôvodný text a overená dvojica interpret/názov; preklady, reklamy, akordové riadky a známe oznamy o chýbajúcom texte sa nezobrazujú ako text skladby.
- Čiastočný výpadok sa neukladá ako definitívne nenájdenie. Engine zopakuje pokus bez prepínania stanice, najviac po 5, 20, 60 a 60 sekundách; rešpektuje dlhšie obmedzenie servera. Staré negatívne záznamy cache sa preveria znova, platné pozitívne sa zachovajú.
- Obaly využívajú tie isté overené identity a jeden ohraničený záložný dotaz podľa názvu. Aj potom sa musí zhodovať celý interpret a verzia skladby; nesprávny prvý výsledok sa neprijme.

## Konkrétne overenie

Pri živých kontrolách sa podarilo získať texty Nenahraditeľná (Sima Martausová & For You), Ani ty ani já (David Koller), Biely kvet, Svatovítský chrám, Viac, Prepáč, Sľub a Krásnější než růže. Opravené vyhľadávanie stiahlo aj skutočné obaly pre Žbirku/Limit, Neckářa, Hečkovú/Hečkovcov a Pavla Rotha. Záznamy obsahujú iba stav, veľkosť a kontrolné súčty, nie celé texty alebo prevzaté obrázky.

Niektoré ďalšie zaslané skladby zostávajú bez overeného výsledku alebo pri kontrole narazili na výpadok zdroja. Rozšírenie zdrojov nezaručuje dostupnosť každej skladby. SuperMusic poskytol iba stránku vyžadujúcu JavaScript a nie je vydávaný za funkčný adaptér. Podrobnosti sú v `docs/RADIO-LYRICS-FIELD-CASES.json` a `docs/RADIO-COMBINED-ENGINE-CHECKS.json`.

## Prevádzkové limity

Sieťové operácie prebiehajú mimo GUI. Jeden helper vykonáva najviac jednu požiadavku na hostiteľa súčasne a celkovo najviac 22 požiadaviek, pri uvedenej konkrétnej skladbe Pavla Rotha 23. Ostáva 32-sekundový rozpočet plánovača a 45-sekundové vonkajšie ukončenie procesu. Texty majú limit 20 000 znakov, cache najviac 128 skladieb; skutočné nenájdenie sa drží 30 minút a kladný výsledok 14 dní.

Ide o izolovanú skúšobnú verziu. Produkčný kanál 1.0.37 sa nemení. Testy a živé kontroly zdrojov nenahrádzajú overenie prijímača s týmto balíkom.

Živá kontrola Písničky-akordy osobitne zaznamenáva nedostupnosť z GitHub runnera. Taký stav sa neoznačí za nájdený text a neblokuje zostavenie; presná identita, parser aj správanie pri výpadku sú povinné deterministické testy. Lokálne živé načítanie textu Davida Kollera bolo úspešné.
