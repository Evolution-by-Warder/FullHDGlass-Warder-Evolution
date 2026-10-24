# FullHDGlass Warder Evolution — TEST259

Zrýchlenie náhľadov a pohybu v nastaveniach po hlásení z TEST258.

- Všetkých 252 pôvodných názvov má pripravený náhľad priamo v IPK (236 jedinečných obrázkov). Farbenie PNG sa vykonáva pri zostavení, nie pri pohybe v menu.
- Prvý výber iba rozbalí hotový PNG do existujúcej cache; opakovaný výber používa cache a odtlačok súboru v pamäti. Dekódované obrazové polia sa v pamäti menu nehromadia.
- Pri rýchlom listovaní sa čaká 120 ms na poslednú voľbu a medziľahlé náhľady sa preskočia. Zastaraný výsledok neprepíše aktuálnu voľbu.
- Ak pripravený súbor chýba, prepočet vykoná samostatný proces s nižšou prioritou. Menu na jeho dokončenie nečaká. Zatvorenie okna ukončí spracovanie a neskorší výsledok už widget nepoužije.
- Kompletné obrázky, veľkosť náhľadu, tmavomodré podfarbenie a odstránenie spodného obdĺžnika zostávajú ako v TEST258. IPK je väčší o pripravené náhľady; nie je potrebné znovu sťahovať pôvodnú pomocnú sadu.

```sh
opkg install /tmp/enigma2-skin-fullhdglass-warder-evolution_1.0.16-test259_all.ipk
```

Potom reštartovať GUI. Overiť rýchle opakované zmeny položiek v HDD/SSD, ECM a ďalších skupinách, okamžitý návrat/ukončenie počas listovania a zhodu náhľadu s poslednou voľbou. Skontrolovať prvé zobrazenie po reštarte aj opakované návštevy rovnakej voľby.

Testy zahŕňajú 18 kontrol rozloženia a pôvodnej konfigurácie, 8 kontrol asynchrónnej fronty a 7 obrazových kontrol. Celá pripravená sada sa porovnáva po bajtoch s pôvodným rendererom TEST258 a nezávisle po pixeloch vrátane alfa kanála a vnútorných náhľadov. Balík sa overuje proti zdrojovým súborom a overenému odvodenému archívu. Kontroly na zostavovacom počítači nepotvrdzujú rýchlosť konkrétneho prijímača.

Produkčné feedy zostávajú na 1.0.15; ide o ručne inštalovaný test.
