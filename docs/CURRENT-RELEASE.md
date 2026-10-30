# FullHDGlass Warder Evolution 1.0.44

Po inštalácii alebo aktualizácii skin potichu stiahne náš IPTV rádio bouquet `userbouquet.warder.radio` a zaradí ho do zoznamu rádií. Používateľ nemusí bouquet importovať ručne.

Sťahovanie prebieha v samostatnom procese s nižšou prioritou a časovým limitom. Inštalátor na sieť nečaká; nezobrazuje ďalšie okná ani nezapisuje diagnostické logy. Pri výpadku internetu zostane zachovaný pôvodný obsah a skin opakuje pokus v rámci existujúceho šesťhodinového intervalu. Kontrola aktualizácie ostáva raz za sedem dní.

Nový bouquet sa vytvorí až po overení SHA-256, štruktúry a počtu staníc. Do `bouquets.radio` sa pridáva iba jeho vlastný odkaz; existujúce poradie, ostatné rádio a TV zoznamy zostávajú zachované. Opakované spustenie nevytvára duplicity. Vlastný súbor používateľa s rovnakým názvom, symbolické odkazy a súbežné úpravy sa neprepisujú.

Po bežnom reštarte GUI skin načíta aj dáta, ktoré už stiahol inštalátor. Prvé spustenie kontroléra je približne minútu po štarte. Riadna aktualizácia z 1.0.43; schválená grafika a oprava virtuálnej klávesnice zostávajú zachované.

Overené automatickými testami; táto nová funkcia zatiaľ nie je potvrdená na fyzickom prijímači.
