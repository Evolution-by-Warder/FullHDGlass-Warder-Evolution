FullHDGlass 1.0.60-test3 opravuje zobrazenie názvov programov v CoolTVGuide a položiek nastavení na displeji prijímača.

Oprava bola pripravená podľa dodaného balíka Coolman V8.0 pre Python 3. Názvy v úzkych bunkách sa už nezalamujú do odrezaných riadkov: zobrazujú sa v jednom riadku s výpustkou. Plný názov a popis programu zostávajú v detaile. Pôvodné dáta programov, časovanie, výber, rozmery buniek, písmo a farebné stavy sa zachovávajú. Oprava funguje ako adaptér FullHDGlass; neprepisuje súbory nainštalovaného CoolTVGuide.

Na displeji sa dopĺňajú zdroje entry/value a ich staršie aliasy v situácii, keď všeobecný systémový súhrn použije šablónu nastavení. Zobrazenie sleduje pohyb v nastaveniach a po zatvorení odstráni svoje odbery zmien. Šablóna pre displej 132×64 používa správne väzby na zdroje StaticText. Rozloženie sa nemení.

Balík obsahuje aj opravu pádu pri štarte, časovej osi EPG, okien CoolTVGuide/CoolTinyGuide a zoznamov z predchádzajúcich testov. Prešli hostiteľské regresné testy; zobrazenie treba potvrdiť na prijímači. Aktualizačné profily sa nemenia.
