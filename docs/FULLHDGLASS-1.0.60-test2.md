FullHDGlass 1.0.60-test2 opravuje pád pri štarte spôsobený testovacou verziou test1.

Do zoznamu onLayoutFinish sa zapisuje viazaná metóda. Obyčajnú funkciu sa OpenATV pokúšalo vykonať cez exec(), čo spôsobilo TypeError už pri vytváraní systémovej notifikačnej obrazovky. Nový regresný test reprodukuje rovnakú výnimku a spúšťa skutočné Screen.createGUIScreen s opraveným spätným volaním.

Časová os grafického EPG používa jeden riadok rovnako vysoký ako celý vyhradený pás. Natívny predvolený riadok 30 bodov už neorezáva text Dnes a hodiny vo vyššom pásiku. Rovnaký pás sa nesmie zaokrúhľovať ako viacriadková ponuka.

CoolTVGuide a CoolTinyGuide používajú pri rozmere celej obrazovky okno bez dodatočného rámu a titulku. Tým sa odstráni posun a orezanie horného okraja a spodných tlačidiel. Zalamovanie názvov udalostí v úzkych bunkách vykresľovaných samotným CoolTVGuide nie je týmto potvrdené ako opravené; verejný upstream obsahuje iba starší skompilovaný plugin, nie zdroj používanej verzie.

Oprava neúplného posledného riadka bežných ponúk a krátkych hlavičiek z test1 zostáva zahrnutá. Balík je určený na odskúšanie, aktualizačné profily sa nemenia.
