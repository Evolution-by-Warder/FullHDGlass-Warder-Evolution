# FullHDGlass Warder Evolution 1.0.23

- Načítavanie náhľadov používa natívny časovač a asynchrónny proces Enigmy, nezávisle od integrácie Twisted reactoru daného image.
- Pri zmene výberu sa vyčistí predchádzajúci obrázok; chýbajúci alebo chybný náhľad už nezostane nahradený nesúvisiacou starou nápovedou.
- Okolie bubliny je plne priehľadné. Tieňovanie a obrys bubliny zostávajú viditeľné, jej vnútro je jemne priehľadné. Texty, šípky a obsah ukážok zostávajú zachované.
- Obrázky sa naďalej sťahujú oddelene; IPK nezahŕňa veľký archív.

Diagnostika prijímača potvrdila neporušený archív 1.0.22 a úspešnú samostatnú prípravu viacerých rozdielnych obrázkov; časť starých požadovaných názvov nemá obrázok v pôvodnom archíve. Nové správanie na prijímači ešte vyžaduje potvrdenie.

Pripravené PNG sa trvalo ukladajú do `preview/` v nastavenej ceste skinu (napr. `/media/hdd/hdg17_files/preview/`). Po reštarte sa znovu použijú bez sťahovania či rozbaľovania archívu. Pomocný proces pred zobrazením pripraví malú RAM kópiu, aby čítanie disku neblokovalo menu. Pôvodné pomocné obrázky ani používateľské súbory sa neprepisujú.
