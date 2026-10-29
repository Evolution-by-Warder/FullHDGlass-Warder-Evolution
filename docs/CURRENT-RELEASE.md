# FullHDGlass 1.0.38-test9 — správne rozpoznanie chýbajúceho textu

Pri skladbe Karel Gott — Léta prázdnin vrátila Hudba.sk vo svojom poli pre text iba oznam „Táto pieseň momentálne nemá pridaný text.“ TEST8 ho považoval za úspešný výsledok a ukončil súbežné hľadanie. TEST9 tento konkrétny oznam rozpozná ako chýbajúci text a umožní ostatným zdrojom pokračovať.

- Overenie platí pri načítaní zo zdroja aj pri čítaní staršej cache. Nesprávne uložený oznam sa znovu nezobrazí ako text piesne.
- Filter porovnáva celý známy oznam, toleruje veľkosť písmen, diakritiku, medzery a koncovú interpunkciu. Nezahadzuje dlhší skutočný text, ktorý obsahuje rovnakú vetu.
- Keď ostatné zdroje neodpovedajú, zostáva výsledok vhodný na opakovanie; nevytvára sa falošná pozitívna cache.
- Štyri nové regresné testy overujú čistý oznam, starú cache, neskorší platný výsledok z iného zdroja aj výpadok ostatných služieb. Používajú ilustračné texty, nie celé texty piesní.

## Rozsah vydania

Schválená grafika, geometria, prehrávanie, metadáta a vyhľadávanie obalov zostávajú ako v TEST8. Poradie zdrojov sa týmto vydaním nemení; regionálna priorita, nové zdroje a zlepšenie variantov mien sú ďalšie samostatné úpravy. Toto vydanie neznamená, že sa chýbajúce texty automaticky stali dostupnými.

Kontrola Fero Fabian — Tibetský mlynček nenašla text v štyroch aktuálnych adaptéroch ani nahrávku v slovenskom iTunes katalógu pri hľadaní celej dvojice, samotného názvu či interpreta. Samostatná požiadavka MusicBrainz sa nepodarila spracovať, preto ju nepovažujeme za potvrdené nenájdenie. Záznamy aj ďalšie prípady sú v `docs/RADIO-LYRICS-FIELD-CASES.json`; neobsahujú celé texty piesní ani prevzaté HTML.

Ide o izolovanú skúšobnú verziu. Produkčný kanál 1.0.37 sa týmto vydaním nemení. Zdroje zostávajú [LRCLIB](https://lrclib.net/docs), [lyrics.ovh](https://github.com/NTag/lyrics.ovh), [Hudba.sk](https://hudba.zoznam.sk/) a [Youradio](https://textypisni.youradio.cz/).
