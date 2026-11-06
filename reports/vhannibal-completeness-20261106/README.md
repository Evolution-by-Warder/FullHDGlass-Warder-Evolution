# Audit úplnosti Vhannibal – 6. 11. 2026

Stav je pracovný a vychádza z FullHDGlass main `603218ea8fa51176f686f14f303509a4c64dc7e1` a PiconHub main `e90a1fe3a2734b555f48f343284f9103530180fb`.

## Zdroje

- [Oficiálne sady Vhannibal](https://www.vhannibal.net/index.php) a [index alternatívnych stiahnutí](https://www.vhannibal.net/asd.php). Načítaných 54 odkazov, 27 rôznych ZIPov podľa SHA256. Jeden je aktuálny grafický Motor z 5. novembra (SHA256 `011f4f931088e6a3a6be1e4fe69a22b1909caf522384de371d27cc64b7dbd052`). Ostatných 26 sú nastavenia Motor, Hot Bird, Dual, Multi, Trial, regionálne DTT a DE/PL bez PNG. Ich `lamedb` tvoria 13 417 unikátnych služieb.
- [Historické importné výpisy](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/tree/e90a1fe3a2734b555f48f343284f9103530180fb/plugin/artwork/provenance/vhannibal) a [klasifikácia Motor z 3. novembra](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/tree/beb243b68317baf736e4c4a96ae3ad5eed38ec58/factory/temp/vhannibal-final-20261105). Staršie vydania sú v počte zastúpené inventúrami. Ich pôvodné PNG sa nepodarilo znovu získať.
- [Historických 3 388 kandidátov](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/45) zostáva doložených v samostatnom porovnaní: 3 198 prijatých, 179 výnimiek a 11 blokovaných vstupov. Znovu sa nepripočítavajú.

## Stav produkcie a pracovných opráv

Jednotka je unikátna platná **zdrojová** servisná referencia po deduplikácii archívov. Viac zdrojových referencií môže viesť na jednu prijatú cieľovú službu. Spracované majú dokumentované priradenie a deväť záznamov v ZIPoch. Vylúčené majú doložený dôvod v rámci dostupných zdrojov. Absencia z nastavení nepreukazuje globálne ukončenie vysielania. Staršie nepreverené alternatívy loga sa nezlučujú podľa názvu.

| Rozsah | Zdrojové | Spracované | Opravené | Vylúčené | Nevyriešené |
| --- | ---: | ---: | ---: | ---: | ---: |
| Všetky dostupné inventúry | 14 635 | 10 210 | 3 | 3 866 | 556 |
| Aktuálny Motor | 14 084 | 10 187 | 3 | 3 437 | 457 |

Aktuálny archív má aj štyri PNG s neplatnou číslovanou príponou. Tri majú identický CRC a veľkosť ako platný člen. Štvrtá je odlišná rádiová alternatíva mimo rozsahu tejto práce. Číslované názvy netvoria nové referencie.

- 498 centrálnych adresárov, 400 476 PNG položiek a 0 duplicitných názvov vnútri jednotlivých ZIPov. Všetkých 12 508 doteraz prijatých cieľových referencií je vo všetkých deviatich satelitných variantoch. Kontrola názvov a CRC v centrálnom adresári nenahrádza individuálnu vizuálnu kontrolu každého loga.
- Prienik deviatich variantov voči zjednoteniu referencií u providerov: ANTIKSAT 133/137, DIGI/TELLY 219/279, FREESAT 247/310, SKYLINK 455/455, CANAL+ SK 242/244 a CZ 247/247. Rozdiel sa eviduje samostatne, pretože môže predstavovať existujúcu politiku členstva alebo odlišný regionálny artwork.
- Všetkých 18 archívov CANAL+ SK/CZ prešlo fyzickým SHA256 a ZIP CRC. Overené sú aj SHA256 oboch MASTER V9 šablón. Zoznam publikovaných hashov je v [protected.json](protected.json).
- Konkrétne technické a identitné výnimky sú v [unresolved.json](unresolved.json). Súhrn dôvodov a vstupných hashov je v [audit-summary.json](audit-summary.json). Audit zatiaľ nepotvrdzuje 100 % správnosť a aktuálnosť použitých log.

## Opravy pripravené na schválenie

- **Quest Red, 28.2°E.** Pridaná presná referencia `1_0_1_B62_7F3_2_11A0000_0_0_0`. Identitu potvrdzuje nový multiplex a SID 2914. Všetkých deväť PNG je bitovou kópiou existujúcej grafiky z balíka 282E. [KingOfSat](https://en.kingofsat.net/news.php/datanews.php?pos=28.2E)
- **Karavan TV, 13.0°E.** Pridaná referencia `1_0_1_1C9D_332C_13E_820000_0_0_0` pre multiplex Harmonic 11137 H. Všetkých deväť PNG je bitovou kópiou existujúcej grafiky Karavan TV z 13.0°E. [Satindex](https://www.satindex.de/fhistory/2/11137/)
- **Viasat Kino, 1.9°E.** Na referencii `1_0_1_79_E_3_130000_0_0_0` bol v produkcii znak TV1000. Všetkých deväť variantov nahrádza už publikovaná bulharská grafika Viasat Kino. [Potvrdenie vysielateľa](https://viasatkino.bg/chesto-zadadavani-vuprosi)
- **SIKA TV, 26.0°E.** Do spracovaných patrí po samostatnom potvrdení SID 738 a TSID 8229, fyzickom overení deviatich PNG a úplnej zhode 220×132 Transparent so zdrojovým PNG. Grafiku už obsahuje živý balík. [KingOfSat](https://en.kingofsat.tv/freqs.php?aff=zap&filtre=no&hdtv=1&lim=200&ordre=freq&pos=26E&standard=All)

Mení sa 27 ZIPov, 18 pridaných PNG položiek a 9 nahradených. Všetky ostatné položky v dotknutých ZIPoch zostali bitovo identické. Overené boli SHA256 a CRC archívov, všetkých deväť rozmerovo správnych PNG na každú opravenú referenciu, validátor manifestu, CANAL guard a 27 skúšok skutočnej inštalačnej funkcie v dočasnom adresári so zachovaním používateľského súboru. [Presné referencie a SHA256](repairs.json)

## Otvorené

V súčte ostáva 556 nevyriešených zdrojových referencií. Členstvo v ZIPe ani zhodný názov stanice samy osebe nepotvrdzujú správnosť loga. Treba preveriť najmä chýbajúce väzby na overenú grafiku, staré aliasy typu služby, skutočné programové zmeny a prípady na chránenej pozícii 23.5°E. Providerové rozdiely majú samostatné rozhodnutie o členstve. Na zlúčenie pripravených opráv treba výslovný súhlas.
