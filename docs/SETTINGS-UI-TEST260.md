# FullHDGlass Warder Evolution — TEST260

Spoločná grafická hlavička FullHDGlass by Warder v štýle PiconHubu.

- Schválený modrý banner s menším emblémom. Dátum, deň, živý čas a menšie biele sekundy sú natívne prvky; vpravo je tyrkysové číslo verzie. Dátum a deň používajú existujúcu lokalizáciu skinu.
- Rovnaká hlavička v jedenástich vlastných nastavovacích obrazovkách vrátane výberov, histórie, prehliadača priečinkov a miest. Názov otvorenej ponuky zostáva viditeľný v hlavičke.
- Hlavička zaberá 164 px; hlavné menu je posunuté len o 32 px. Rozdelenie úvodnej obrazovky, veľkosť TV náhľadu, pomocné obrázky 1029×350 a spodné tlačidlá zostávajú zachované. Konfiguračný zoznam zobrazuje o jeden riadok menej; všetky ďalšie položky sú dostupné posúvaním.
- Pôvodné veľkosti ovládacích prvkov vo výberoch sú zachované. Absolútne pozície zostávajú rovnaké, kde je na hlavičku dostatok miesta. Samostatne sú upravené a testované dynamické náhľady deviatich ikon a centrovanie jediného tlačidla výsledku.
- Zrýchlené načítavanie náhľadov z prijímačom overenej TEST259 sa nemení. Nepribúda spracovanie grafiky pri listovaní. Banner sa načíta pri otvorení obrazovky.
- Pôvodné rádio/grafické súbory zostávajú byte-for-byte nezmenené. Nový súbor je výslovne povolený len pre nastavenia a pripnutý samostatným SHA256. PiconHub sa nemení.

```sh
opkg install /tmp/enigma2-skin-fullhdglass-warder-evolution_1.0.16-test260_all.ipk
```

Potom reštartovať GUI. Overiť čitateľnosť hlavičky a všetky tri pravé stĺpce, otvorenie jednotlivých výberov, dlhé zoznamy s posuvníkom, deväť ikon v náhľade, históriu/výsledok a vyhľadávanie miest. Skontrolovať, že ovládanie menu zostáva svižné. Systémové MessageBox, ChoiceBox a InputBox majú naďalej natívne systémové rozloženie.

Kontroly nie sú testom na prijímači. Produkčné aktualizačné feedy zostávajú na 1.0.15; toto je ručne inštalovaný grafický test.
