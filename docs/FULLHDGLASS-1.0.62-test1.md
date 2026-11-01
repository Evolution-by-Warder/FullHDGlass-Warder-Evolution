# FullHDGlass 1.0.62-test1 — OpenATV 8.1

Samostatná testovacia verzia nadväzuje na ostrú 1.0.61. Produkčné aktualizácie zostávajú na 1.0.61.

- Opravené texty a farebné popisy tlačidiel v prehliadači obrázkov PicturePlayer. Neprítomné modré tlačidlo nevytvára chybnú väzbu.
- Opravené pripojenie ikony pohybu paraboly pri PiP k natívnemu logickému zdroju.
- Opravené farebné tlačidlá denníka nastavenia motora. Nová animačná politika OpenATV 8.1 už pri otvorení nepracuje s tlačidlom ako s textovým zdrojom.
- Opravené popisy tlačidiel staršieho správcu swapu na OpenATV 8.0; novší správca naďalej používa natívne rozloženie Setup.

Rozloženie, veľkosti, fonty a pôvodná grafika dotknutých obrazoviek sú zachované. Predchádzajúce opravy ponúk, CoolTVGuide, displeja, LCD4linux a Rýchleho menu zostávajú zahrnuté.

Automatické kontroly porovnávajú OpenATV 8.0, vetvu 8.0-next používanú pre 8.1 a aktuálny master. Testy používajú skutočné Python triedy; natívne C++ widgety a časovače nahrádzajú testovacie objekty. Fyzické overenie na prijímači, GLES a rôznych rozlíšeniach ešte nie je potvrdené.

Po ručnej inštalácii testovacieho IPK reštartujte GUI.
