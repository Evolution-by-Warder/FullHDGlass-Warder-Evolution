# FullHDGlass Warder Evolution 1.0.37

Skin raz týždenne na pozadí obnoví existujúci bouquet **Warder Radio Streams** z nášho spoločného Gitu. Na začiatku sú naše slovenské a české rádiá, za nimi týždenne obnovená zahraničná časť.

Sťahovanie a kontrola prebiehajú v samostatnom procese. Úspešná zmena bezpečne nahradí súbor a obnoví bouquety bez hlášok, otvorenia okna, reštartu GUI alebo prepnutia prehrávanej stanice. Predchádzajúci súbor zostáva ako `.bak`. Ostatné bouquety sa nemenia.

Obnova spravuje iba existujúci `/etc/enigma2/userbouquet.warder.radio` s hlavičkou Warder Radio Streams; sama neimportuje nový bouquet. Pri chybe siete alebo kontroly zostáva posledný dobrý zoznam a ďalší pokus príde najskôr po šiestich hodinách. Čas poslednej úspešnej kontroly prežije reštart.

Overené automatickými skúškami vrátane chýb siete, neúplných údajov, SHA256, zachovania používateľských súborov, týždenného intervalu a oddelenia práce od GUI. Fyzické overenie novej funkcie na prijímači sa zatiaľ netvrdí.
