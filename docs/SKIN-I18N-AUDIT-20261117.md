# FullHDGlass — jazykový audit 17. 11. 2026

## Aktuálny stav — 18. 11. 2026

**Zostáva 0 nevyplnených referenčných prekladových položiek** vo všetkých 20 cieľových jazykoch a piatich katalógových doménach. Formálne pokrytie referenčných kľúčov je **60 320/60 320 (100 %)**: 20 jazykov × (552 setupGlass17 + 195 helpTxt + 108 weather + 42 netatmo + 2 119 eWeather). Angličtina tvorí zdrojový jazyk, spolu teda **21 jazykov**.

Tabuľka počíta aktívne neprázdne preklady z referenčných katalógov, ktoré majú rovnakú hodnotu priamo v binárnom GNU gettext katalógu. Angličtina používa zdrojové texty. Historické kľúče mimo referenčného inventára sú v katalógoch zachované.

| Jazyk | setupGlass17 | helpTxt | weather | netatmo | eWeather |
|---|---:|---:|---:|---:|---:|
| en | zdroj 552 | zdroj 195 | zdroj 108 | zdroj 42 | zdroj 2119 |
| al | 552/552 | 195/195 | 108/108 | 42/42 | 2119/2119 |
| cs | 552/552 | 195/195 | 108/108 | 42/42 | 2119/2119 |
| de | 552/552 | 195/195 | 108/108 | 42/42 | 2119/2119 |
| el | 552/552 | 195/195 | 108/108 | 42/42 | 2119/2119 |
| es | 552/552 | 195/195 | 108/108 | 42/42 | 2119/2119 |
| et | 552/552 | 195/195 | 108/108 | 42/42 | 2119/2119 |
| fa | 552/552 | 195/195 | 108/108 | 42/42 | 2119/2119 |
| fr | 552/552 | 195/195 | 108/108 | 42/42 | 2119/2119 |
| hu | 552/552 | 195/195 | 108/108 | 42/42 | 2119/2119 |
| it | 552/552 | 195/195 | 108/108 | 42/42 | 2119/2119 |
| lt | 552/552 | 195/195 | 108/108 | 42/42 | 2119/2119 |
| nl | 552/552 | 195/195 | 108/108 | 42/42 | 2119/2119 |
| pl | 552/552 | 195/195 | 108/108 | 42/42 | 2119/2119 |
| pt | 552/552 | 195/195 | 108/108 | 42/42 | 2119/2119 |
| ro | 552/552 | 195/195 | 108/108 | 42/42 | 2119/2119 |
| ru | 552/552 | 195/195 | 108/108 | 42/42 | 2119/2119 |
| sk | 552/552 | 195/195 | 108/108 | 42/42 | 2119/2119 |
| tr | 552/552 | 195/195 | 108/108 | 42/42 | 2119/2119 |
| uk | 552/552 | 195/195 | 108/108 | 42/42 | 2119/2119 |
| zh | 552/552 | 195/195 | 108/108 | 42/42 | 2119/2119 |

- Nezávislé porovnanie všetkých katalógov na commite `5194ca6` potvrdilo 32 505 chýbajúcich položiek v pôvodnom inventári. Predchádzajúci úvod auditu uvádzal o 189 viac, pretože nezohľadnil už skompilovanú taliansku nápovedu.
- Súbežne pribudlo 945 historických nápovied v holandčine, poľštine, portugalčine, rumunčine a ukrajinčine. Všetkých päť katalógov je zahrnutých vo výpočte.
- Rozšírený inventár obsahuje aj 43 kľúčov z priamych volaní gettext v zdrojových moduloch. Všetkých 20 jazykov má 35 nových prekladov nastavení, 6 nápovied a 2 texty rozšíreného počasia. Spolu pribudlo 860 prekladov. Skontrolovala sa úplnosť kľúčov, hlavičky UTF-8, placeholdery a načítanie skompilovaných katalógov.
- [Testy sťahovania a uchovávania jazykov](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/44256787078) prešli. Priamy test piatich gréckych katalógov na commite `095497e` overil SHA-256, načítanie v gettext a druhú synchronizáciu bez prenosu. Fyzická skúška na prijímači zatiaľ neprebehla.
- Historické eWeather získalo 30 615 prekladov v 15 jazykoch. Každý z 20 prekladových jazykov teraz obsahuje v zdroji aj binárnom katalógu všetkých 2 119 referenčných kľúčov.

## Dokončenie zostávajúcich katalógov helpTxt – 18. 11. 2026

- Pracovná vetva bola pred zápismi overená; päť doteraz nedokončených jazykov `tr, et, hu, al, fa` získalo po **189 nových, obsahovo preložených nápovedách**, spolu **945 nových textov**. Šesť predtým spracovaných nových nápovied v každom jazyku bolo zachovaných. Každý jazyk má presne **195/195** platných referenčných kľúčov.
- Pre každý z piatich jazykov boli uložené úplné zdrojové katalógy `helpTxt.po` a skutočné binárne **GNU gettext `helpTxt.mo`**, vždy s **196 záznamami vrátane hlavičky**. Binárne veľkosti: tr 25 477 B, et 24 654 B, hu 27 540 B, al 26 598 B, fa 32 690 B.
- Zosilnené regresné testy overujú úplnosť všetkých dvadsiatich nápovedných katalógov, súlad skutočných prekladov `.po ↔ .mo`, načítanie cez Python `gettext.GNUTranslations`, prítomnosť hlavičky, jazykové kódy vrátane historicky platného skráteného kódu `ru`, a zachovanie placeholderov `%s/%d`.
- Doplnený je tiež **nezávislý regresný test pokrytia všetkých piatich domén × 20 jazykov** proti referenčným kľúčom. Referenčné počty sú 552, 195, 108, 42 a 2 119; celkový počet je 60 320. Regresné testy blokujú v budúcnosti stratu aj jedinej referenčnej lokalizovanej položky.
- Posledný potvrdený úspešný beh pôvodnej aj kompletnej nápovednej regresie: [GitHub Actions #44272724702](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/44272724702). Výsledok najnovšieho rozšíreného testu všetkých piatich domén musí byť overený samostatne (zatiaľ sa nepredpokladá automatický PASS).
- **Nulový počet chýbajúcich prekladov** je meranie prítomnosti lokalizovaných hodnôt a binárnej funkčnosti; **nie je potvrdením štylistickej bezchybnosti ani reálnej skúšky na Enigma2 prijímači**. Zostáva fyzický test, vizuálna kontrola dlhých RTL textov v perzštine, terminologická korektúra rodilými hovoriacimi a schválenie pred vydaním.
- Nič sa nezlučovalo do `main`, nevydalo sa IPK, testovací/ostrý balík, feed ani release. Verzia a grafika bez zmeny.

## Staršie záznamy

Cieľ: 21 jazykov (20 prekladových katalógov a anglický zdrojový text). Stav: **čiastočne dokončené**. Vyplnený prekladový záznam nie je záruka správnosti jazykovej formulácie; kontrola na prijímači ešte neprebehla.

## Hlavné nastavenia

| Jazyk | Chýbajúce položky v hlavnom katalógu |
|---|---:|
| Slovenský (sk) | 0 |
| Český (cs) | 0 |
| Ruský (ru) | 0 |
| Litovský (lt) | 0 |
| Čínsky (zh) | 0 |
| Grécky (el) | 0 |
| Albánsky (al) | 0 |
| Nemecký (de) | 0 |
| Španielsky (es) | 0 |
| Estónsky (et) | 0 |
| Perzský (fa) | 0 |
| Francúzsky (fr) | 0 |
| Maďarský (hu) | 0 |
| Taliansky (it) | 0 |
| Holandský (nl) | 0 |
| Poľský (pl) | 0 |
| Portugalský (pt) | 0 |
| Rumunský (ro) | 0 |
| Turecký (tr) | 0 |
| Ukrajinský (uk) | 0 |

**Hlavné nastavenia: všetkých 20 prekladových katalógov obsahuje 517/517 správ podľa slovenského referenčného inventára a 0 prázdnych `msgstr`; angličtina je zdrojový jazyk.** V 17 jazykoch bol doplnený doteraz chýbajúci kľúč `FastScan tables selected`.

## Gréčtina

| Oblasť | Preložené |
|---|---:|
| Nastavenia setupGlass17 | 517/517 |
| Nápoveda helpTxt | 189/189 |
| Počasie weather | 108/108 |
| Netatmo | 42/42 |
| Historické eWeather | 2 117/2 117 |

**Grécke eWeather:** aktuálne 2 117/2 117 skutočných prekladov; zostáva 0 prázdnych položiek.

## Inventár vedľajších katalógov
Údaje sú **prítomné preložené kľúče / referenčný počet**: nápoveda 189, počasie 108, Netatmo 42 a rozšírené počasie eWeather 2 117. Znak **—** znamená, že pre daný jazyk úplne chýba samostatný katalóg `.po`; nie je to dokončený preklad. Kontrola sa týka súborov pracovnej vetvy a nenahrádza jazykovú ani fyzickú validáciu.

| Jazyk | helpTxt | weather | netatmo | eWeather |
|---|---:|---:|---:|---:|
| al | — | 108/108 | 42/42 | — |
| cs | 189/189 | 108/108 | 42/42 | 2117/2117 |
| de | — | 108/108 | 42/42 | — |
| el | 189/189 | 108/108 | 42/42 | 2117/2117 |
| es | — | 108/108 | 42/42 | — |
| et | — | 108/108 | 42/42 | 96/2117 |
| fa | — | 108/108 | 42/42 | — |
| fr | — | 108/108 | 42/42 | — |
| hu | — | 108/108 | 42/42 | — |
| it | — | 108/108 | 42/42 | — |
| lt | 189/189 | 108/108 | 42/42 | 2117/2117 |
| nl | — | 108/108 | 42/42 | — |
| pl | — | 108/108 | 42/42 | — |
| pt | — | 108/108 | 42/42 | — |
| ro | — | 108/108 | 42/42 | — |
| ru | 189/189 | 108/108 | 42/42 | — |
| sk | 189/189 | 108/108 | 42/42 | 2117/2117 |
| tr | — | 108/108 | 42/42 | — |
| uk | — | 108/108 | 42/42 | — |
| zh | 189/189 | 108/108 | 42/42 | — |

Pri gréčtine zostáva **0 nepreložených fráz eWeather**; všetkých 189 kľúčov helpTxt je už preložených. Pri estónčine obsahuje eWeather iba 96 z 2 117 kľúčov, teda **2 021 chýba**. Väčšina ďalších jazykov potrebuje celé chýbajúce doplnkové katalógy.

## Čo je zapísané

- Technický resolver pre 21 jazykov v štandardnom GNU gettext, bezpečný anglický fallback a zachovanie vypínača prekladov.
- Nové katalógy .po/.mo pre gréčtinu a doplnené preklady pre ostatné jazyky.
- Nové hlavné preklady v 14 ďalších jazykoch vrátane úplného dokončenia nemčiny, francúzštiny, holandčiny, španielčiny, taliančiny, estónčiny a poľštiny, portugalčiny, rumunčiny, ukrajinčiny, turečtiny, maďarčiny, albánčiny a perzštiny, nezmenené existujúce vyplnené hodnoty.
- Kontroly python3 syntaktiky, binárnych katalógov a regresné CI testy dokončených jazykov (DE/FR/NL/ES/IT/ET/PL/PT/RO/UK/TR/HU/AL/FA) v `tools/test-warder-catalog-integrity.py`. Opravený chybný test, ktorý považoval hlavičku gettext `msgid ""` za nepreloženú frázu. CI run 44203581996 z 18. 11. 2026 **zlyhal**: dve chýbajúce grécke hlavné msgid a nezhodné či poškodené čínske `.mo`. Chyby boli lokalizované a opravené; nový CI beh treba potvrdiť.
- V nasledujúcom behu bolo doplnených 39 chýbajúcich gréckych helpTxt a 249 gréckych eWeather fráz; katalógy .mo boli znova skompilované a zachovali sa predchádzajúce preklady.
- Opravený vážne poškodený súbor `tools/test-warder-catalog-integrity.py` (duplicitné a rozbité časti testov). Nová verzia kontroluje všetkých 20 hlavných jazykov, zhodu kľúčov, čitateľnosť a obsah všetkých existujúcich .mo, zhodu printf argumentov aj úplnosť gréckeho helpTxt. Čaká sa na výsledok aktuálneho GitHub Actions.
- Pre nemčinu, francúzštinu a španielčinu boli vytvorené kompletné samostatné katalógy Netatmo (každý 42/42) vrátane skutočných jazykových textov a 16 svetových strán podľa príslušných národných skratiek. Spolu 126 nových prekladov, nové `.mo`.
- V ďalšom behu pribudlo 170 skutočných gréckych meteorologických prekladov eWeather a šesť kompletných katalógov Netatmo (it/nl/pl/pt/ro/hu), 6 × 42 položiek vrátane lokalizovaných smerov vetra tam, kde sa národné skratky líšia od medzinárodných. Skompilované binárne GNU gettext `.mo` boli overené párovým dekódovaním; kontrolu v GitHub Actions treba potvrdiť osobitne.
- Zdrojové zmeny bez zostavenia alebo vydania IPK.

- Oprava CI: grécky setupGlass17 získal 2 chýbajúce kľúče (517/517), opravili sa 2 historické čínske katalógy (`zh/helpTxt`, `zh/weather`) vrátane nesprávnych plural pravidiel, 11 nepravdivých fuzzy textov a 9 prázdnych textov čínskej nápovedy. Aktualizované oba čínske a grécky binárny `.mo`; CI musí znova prebehnúť.

- Nové kompletné preklady Netatmo pre ru/uk/tr/zh: **168 nových textov**, aktualizované binárne GNU gettext `.mo` a doplnené regresné kontroly. Čínske helpTxt doplnené o **20 chýbajúcich viacriadkových textov** na plných 189/189; ostatné preklady ostali zachované. Nový CI beh ešte treba potvrdiť.

- Ďalších **160 originálne preložených gréckych viet** v eWeather (vtedy 1 174/2 117; zostávalo 943). Všetky staršie preklady zachované, binárny katalóg `.mo` preložený z aktuálneho `.po`; test kontroluje skutočné pokrytie. Overenie nového CI behu ešte čaká na výsledok.

- Dokončené posledné štyri samostatné katalógy Netatmo: albánčina, estónčina, litovčina a perzština, spolu **168 nových prekladov** s lokalizovanými 16 smermi vetra. Všetkých 20 jazykov má teraz katalóg Netatmo 42/42; jazyková kontrola rodenými hovoriacimi a fyzické skúšky ešte neprebehli. Všetky nové `.mo` boli skompilované; nové CI čaká na overenie.


- Dávka 18. 11. 2026: 200 ďalších gréckych meteorologických fráz (1 374/2 117), opravených 7 nesprávnych alebo anglických estónskych eWeather textov (vrátane smerov ENE/WSW/WNW); znova zostavené oba `.mo` katalógy. Aktualizovaný regresný test. CI beh `44213410552` na staršom commite `3f82090` skončil úspešne; nový beh bude potrebné overiť samostatne.

- Dávka 18. 11. 2026: 200 nových gréckych meteorologických textov eWeather (1 574/2 117), vrátane búrkových prehánok, nočných zrážok a teplotných zmien; všetky predchádzajúce preklady zachované, znovu vytvorený GNU gettext UTF-8 .mo s kontrolou počtu kľúčov a printf argumentov. V tejto dávke treba ešte potvrdiť nový GitHub Actions CI beh.

- Doplnených ďalších 100 gréckych fráz eWeather dňa 18. 11. 2026 (2 117/2 117). Skontrolovaný inventár, aktualizované regresné testy a skompilovaný aktuálny GNU gettext `.mo`; výsledok CI nového commitu sa ešte čaká.

- Dávka 18. 11. 2026: doplnených ďalších 165 originálnych gréckych meteorologických viet (eWeather 1839/2 117, zostáva 278). Zachovaných 1 674 doteraz preložených položiek, aktualizovaný GNU gettext UTF-8 .mo a kontrola súladu kľúčov a printf argumentov. Nový CI beh je potrebné overiť po commite.

- Dávka 18. 11. 2026: ďalších 150 autenticky preložených gréckych fráz eWeather (aktuálne 1989/2 117, zostáva 128); aktualizované zdrojové .po a kompilované .mo, lokálne validované počty kľúčov aj zhodné printf argumenty; aktuálny GitHub Actions CI ešte nie je potvrdený.

- Dávka 18. 11. 2026: dokončených posledných 128 gréckych eWeather viet. Katalóg má **2 117/2 117 preložených kľúčov a nula prázdnych správ**, vygenerovaný binárny GNU gettext .mo (UTF-8), kontrola zhody kľúčov, formátovacích argumentov a počtov. Jazyková korektúra rodeným hovoriacim a CI nového commitu zatiaľ nie sú potvrdené.

- Dávka 18. 11. 2026: tri nové kompletné katalógy `weather` pre es/it/pt, každý **108/108**, spolu **324 nových skutočných prekladov**. Zachovaných 108 referenčných kľúčov, nula prázdnych `msgstr`, overené printf argumenty a úplný spätný binárny prechod cez vytvorené UTF-8 GNU gettext `.mo`; doplnené regresné testy. CI a fyzické testovanie treba osobitne potvrdiť.

## Stále chýba

Doplniť chýbajúce jazykové katalógy podľa tabuľky (weather je teraz 108/108 vo všetkých 20 jazykoch), 2 021 estónskych eWeather kľúčov; následne kontrola kontextu a jazykovej kvality, úspešné CI a fyzický test na OpenATV/OpenPLi.

## Voliteľné jazykové katalógy – 18. 11. 2026

**Implementácia v pracovnej vetve, bez vydania IPK:** ostrý zostavovací skript `tools/build-release-ipk.py` je upravený tak, aby do budúcej zostavy pridal iba anglické `.mo` (ak sú k dispozícii) a malý manifest SHA-256. Ostatné `.mo` zostávajú v zdrojovom repozitári, odkiaľ sa stiahnu iba pre jazyk zvolený v Enigma2. Zdrojové `.po` sa naďalej nebalí.

- Manifest je vytvorený počas zostavenia z aktuálnych `.mo` a pripnutý na konkrétny 40-znakový Git commit. Sťahovač overuje SHA-256, binárny gettext formát, veľkostný limit a cieľový URL pred atómovým nahradením súboru.
- `postinst` spustí iba neblokujúcu synchronizáciu aktuálneho jazyka; pri ďalšom otvorení obrazovky v novom jazyku môže gettext resolver spustiť doťahovanie na pozadí. Neúspech siete nezablokuje inštaláciu, pôvodné stiahnuté katalógy sa neodstraňujú a anglický zdrojový fallback zostáva.
- Doplnený `tools/test-warder-locale-on-demand.py` a kontroly v `.github/workflows/verify-skin-i18n.yml`. Fyzický test na Enigma2 boxe ani úspech najnovšieho CI zatiaľ nie je potvrdený.
- **Pokrytie prekladov sa týmto nemení:** setupGlass17 20 × 517/517, Netatmo 20 × 42/42; gréčtina eWeather 2117/2117, estónčina 96/2117 (zostáva 2021). Chýbajúce katalógy helpTxt, weather, eWeather ostatných jazykov sú stále rozpracované, nie „hotové“ vďaka anglickému fallbacku.
- **Žiadne vydanie, IPK, feed, zlúčenie do main ani zmena verzie.** Nová politika balenia sa prejaví až pri budúcom schválenom zostavení.

## Dávka 18. 11. 2026 – tri ďalšie jazyky weather

- **324 skutočných nových prekladov** pre meteorologický katalóg `weather`: turečtina (`tr`) 108/108, albánčina (`al`) 108/108 a perzština (`fa`) 108/108. Všetky referenčné kľúče zo slovenského inventára zachované, žiadne prázdne `msgstr`; vrátane smerov vetra, zrážok, búrok, systémových a chybových hlásení.
- Vytvorených **3 UTF-8 `.po` a 3 binárne GNU gettext `.mo`**, doplnené automatické porovnanie kľúčov, čitateľnosti `.mo`, neporušených placeholderov a test známych prekladov.
- **Aktuálne weather 20 × 108/108, Netatmo 20 × 42/42, hlavný setupGlass17 20 × 517/517.** Celkovo naďalej chýba **2 646 kľúčov helpTxt** (14 úplne chýbajúcich katalógov) a **33 776 kľúčov eWeather** (15 úplne chýbajúcich katalógov plus 2 021 v estónčine). Počty označujú obsah `.po`, nie fyzické jazykové overenie.
- V novej logike voliteľných jazykov opravené generovanie koncového riadka JSON manifestu po skutočnom zlyhaní CI testu `test_package_contains_only_english_and_digest_inventory`. Zostáva potvrdiť nový beh GitHub Actions aj kontrolu na Enigma2 prijímači.
- Bez IPK, feedu, release, zlúčenia do `main` a zmeny čísla verzie.

## Doplňujúci audit weather – 18. 11. 2026

Pri nezávislom opätovnom čítaní všetkých 20 katalógov `weather.po` sa ukázalo, že starší audit nesprávne stotožnil **prítomnosť kľúča** s **neprázdnym prekladom**. Zistených 32 prázdnych prekladov bolo opravených a existujúce hodnoty zostali zachované:

| Jazyk | Doplnené prázdne položky | Skutočný stav po oprave |
|---|---:|---:|
| de | 6 | 108/108 |
| et | 1 | 108/108 |
| fr | 1 | 108/108 |
| hu | 6 | 108/108 |
| pl | 6 | 108/108 |
| ro | 6 | 108/108 |
| uk | 6 | 108/108 |

Chýbali najmä `Location`, správy o čítaní dát z webu, `Mishmash in the data` a `Attempt`. Opravené príslušné `.po` a nanovo zostavené binárne GNU gettext `.mo`. V teste `tools/test-warder-catalog-integrity.py` bola pridaná povinná kontrola všetkých 20 jazykov proti presným 108 referenčným kľúčom, neprázdnym textom a zhode načítaného `.mo` s `.po`.

**Súhrn celej dávky:** 324 nových prekladov (`al`, `fa`, `tr`) + 32 doplnených starších prázdnych viet = **356 skutočne doplnených viet**. Merané pokrytie `weather` je **2 160/2 160** naprieč 20 jazykmi, 0 prázdnych `msgstr`. Hlavné nastavenia: 20 × 517/517. Netatmo: 20 × 42/42.

**Zostáva 36 422 chýbajúcich jazykových položiek:** `helpTxt` 2 646 (14 chýbajúcich jazykových katalógov) a `eWeather` 33 776 (15 chýbajúcich jazykových katalógov a 2 021 chýbajúcich estónskych viet). Úplnosť nie je synonymum jazykovej korektnosti; korektúra rodenými hovoriacimi a testy na prijímačoch stále chýbajú. Výsledok najnovšej GitHub CI kontroly musí byť potvrdený samostatne. Bez IPK, feedu, verzie a zlúčenia.

## Dávka 18. 11. 2026 – estónske eWeather (+120)

- Na aktuálnom HEAD pracovnej vetvy bolo pred zmenou zistených 96/2 117 estónskych fráz eWeather; pribudlo **120 nových skutočných estónskych prekladov**, najmä sneh, dážď, búrky, zmeny teploty a zimné podmienky. Starých 96 fráz zostalo bez zmeny.
- Nový stav **estónske eWeather: 216/2 117**, zostáva **1 901**. Binárny UTF-8 GNU gettext súbor `et/LC_MESSAGES/eWeather.mo` bol zostavený z aktuálneho `.po` (217 gettext správ vrátane hlavičky). Doplnený regresný test konkrétnych formulácií a gettext binárneho načítania.
- Stav ostatných jazykových katalógov sa v tejto dávke nemenil. **Celkovo zostáva 36 302 chýbajúcich položiek:** helpTxt 2 646 a eWeather 33 656. Hlavné nastavenia 20 × 517/517, weather 20 × 108/108 a Netatmo 20 × 42/42 podľa predchádzajúceho auditu.
- Údaje sú merané podľa prítomnosti konkrétnych textov v katalógoch; jazyková korektúra rodeným hovoriacim, výsledok najnovšej CI a fyzické testy prijímača zostávajú samostatnou úlohou.
- Žiadna IPK, release, feed, zlúčenie do main ani zmena verzie.

## Dávka 18. 11. 2026 – ďalších 170 estónskych fráz eWeather

- Overený aktuálny HEAD a obsah katalógov; z pôvodných **216/2 117** sa estónske eWeather posunulo na **386/2 117**, zostáva **1 731**. Nové preklady pokrývajú napríklad zimné zrážky, snehové a dažďové prehánky, oblačnosť, ochladenie, búrky a ovládacie texty počasia. Doterajšie správne preklady sa neprepisovali.
- Aktualizovaný `et/LC_MESSAGES/eWeather.po`, samostatne zostavený binárny gettext UTF-8 `eWeather.mo` (387 záznamov vrátane hlavičky) a rozšírený regresný test v `tools/test-warder-catalog-integrity.py` na 386 kľúčov aj overenie známych estónskych formulácií.
- **Zostáva presne 36 132 neobsadených položiek podľa existujúceho inventára**: helpTxt 2 646 a eWeather 33 486. Ostatné evidované katalógy: hlavné nastavenia 20 × 517/517, weather 20 × 108/108, Netatmo 20 × 42/42. Nové čísla vyjadrujú pokrytie kľúčov, nie jazykovú kontrolu rodenými hovoriacimi.
- Testy GitHub Actions nového commitu a fyzické testy na Enigma2 sú ešte potrebné; žiadny úspech CI bez overenia netvrdíme. Žiadna IPK, feed, release, zmena verzie ani zlúčenie do main.

## Dávka 18. 11. 2026 – 170 estónskych prekladov, oprava metodiky inventára

- Na aktuálnej pracovnej vetve pridaných **170 nových estónskych skutočných prekladov** eWeather: oblačnosť, dážď, popoludňajšie búrky, teplo, vlhkosť a premenlivé počasie. Zachovaných všetkých 386 dovtedajších preložených záznamov.
- Estónsky `eWeather.po` má teraz **556 neprázdnych správ**: **555/2 117** sa zhoduje s referenčným inventárom a navyše je zachovaný historický estónsky záznam `Select city`, ktorý v slovenskom referenčnom inventári nefiguruje. Zostáva teda **1 562 referenčných fráz**, nie o jednu menej, ako uvádzali predchádzajúce audity.
- Zostavený `et/LC_MESSAGES/eWeather.mo` (557 správ vrátane hlavičky), rozšírená kontrola gettext načítania, presných referenčných kľúčov a historického `Select city`. Predchádzajúci CI beh `44250310144` zlyhal preto, že test nesprávne požadoval neprítomnosť tohto historického kľúča; regresný test je opravený. Úspech nového CI behu treba potvrdiť po jeho ukončení.
- **Presne zostáva 35 963 referenčných prekladových položiek**: `helpTxt` 2 646 (14 jazykov), `eWeather` 33 317 (15 × 2 117 absentujúcich katalógov + 1 562 estónskych). Hlavné nastavenia, weather a Netatmo majú podľa skoršieho auditu všetky plánované vyplnené referenčné kľúče. Vyplnenie neznamená jazykovú korektúru rodeným hovoriacim.
- Fyzické overenie na prijímačoch zostáva otvorené. Žiadne vydanie IPK, feed, release, zmena verzie ani zlúčenie do `main`.

## Veľká dávka 18. 11. 2026 – estónske eWeather (+290)

- Z HEAD pracovnej vetvy načítaný referenčný inventár 2 117 fráz a existujúcich **555 referenčných estónskych prekladov** (+ jeden historický `Select city`). Doplnených **290 nových skutočných estónskych prekladov** počasia, vrátane zrážok, vysokých teplôt, búrok, vlhkosti, oblačnosti, slnka a vetra. Žiadne predchádzajúce texty neboli prepísané.
- **Estónske eWeather: 845/2 117 referenčných fráz** (zostáva **1 272**), plus pôvodný extra kľúč `Select city`. `et/eWeather.po` spolu obsahuje 846 preložených kľúčov a hlavičku; nanovo zostavený `et/eWeather.mo` obsahuje 847 gettext záznamov.
- Rozšírený regresný test všetkých 845 referenčných kľúčov v `tools/test-warder-catalog-integrity.py`, pričom historický extra kľúč sa zachováva a nezapočítava do pokrytia.
- **Celkom ešte chýba 35 673 referenčných prekladov**: helpTxt **2 646**, eWeather **33 027** (15 × 2 117 úplne chýbajúcich jazykových katalógov + 1 272 estónskych viet). Pokrytie hlavných nastavení, weather a Netatmo sa touto dávkou nemení.
- CI pre najnovší commit treba overiť samostatne; bez skutočnej jazykovej korektúry rodenými hovoriacimi a fyzických testov prijímača nie je bod 9 uzavretý. Žiadna IPK, feed, release, zlúčenie do `main` ani zmena verzie.

## Druhá veľká dávka 18. 11. 2026 – estónske eWeather (+220)

- Do `et/eWeather.po` doplnených **220 ďalších skutočných estónskych prekladov** meteorologických fráz. Doterajších 845 referenčných a jeden historický kľúč ostali zachované.
- **Spolu v dnešnom behu: 510 nových estónskych fráz** (290 + 220). Aktuálne pokrytie eWeather v estónčine: **1 065/2 117**, zostáva **1 052**. Zdrojové `.po` má 1 066 neprázdnych správ vrátane extra historického kľúča `Select city`. Reálny binárny UTF-8 GNU gettext `.mo` bol opätovne vytvorený so 1 067 záznamami vrátane hlavičky.
- Rozšírený regresný test `tools/test-warder-catalog-integrity.py` meria presne 1 065 referenčných kľúčov, zachováva historickú položku a kontroluje gettext hodnoty. Výsledok nového GitHub Actions CI treba potvrdiť samostatne.
- **Zostáva 35 453 referenčných jazykových položiek** celkovo: `helpTxt` 2 646 a `eWeather` 32 807 (15 úplne chýbajúcich katalógov × 2 117 a 1 052 estónskych fráz). Hlavné nastavenia 20 × 517/517, weather 20 × 108/108 a Netatmo 20 × 42/42 ostávajú podľa posledného inventára kompletné.
- Žiadne IPK, feed, release, zlúčenie do main, zmena verzie či neschválené grafiky. Jazyková korektúra a fyzický test na prijímačoch zostávajú otvorené.

## Veľká dávka 18. 11. 2026 – estónske eWeather (+250)

- Predchádzajúci HEAD a audit overené, doplnených **250 nových skutočných estónskych prekladov** meteorologických predpovedí. Zachovaných všetkých doterajších 1 065 referenčných viet a historický samostatný kľúč `Select city`.
- **Estónske eWeather teraz 1 315/2 117** referenčných fráz; **802 zostáva**. Celkovo `eWeather.po` obsahuje 1 316 neprázdnych položiek vrátane extra historického kľúča, `eWeather.mo` má 1 317 GNU gettext záznamov vrátane hlavičky. Oba súbory aktualizované na GitHube.
- Regresný test aktualizovaný na presných 1 315 referenčných správ a kontrolné estónske formulácie; výsledok posledného CI treba osobitne potvrdiť.
- **Zostáva spolu 35 203 referenčných položiek**: `helpTxt` **2 646**, `eWeather` **32 557** (15 úplne chýbajúcich katalógov × 2 117 + 802 estónskych fráz). Hlavné nastavenia, weather a Netatmo bez zmeny, 20 jazykov s kompletne vyplnenými referenčnými kľúčmi podľa predchádzajúceho auditu.
- Jazyková korektúra a fyzický test prijímača zostávajú otvorené. Žiadna IPK, release, feed, zmena verzie ani zlúčenie do main.

## Veľká dávka 18. 11. 2026 – nemecké a francúzske nápovedy (2 × 189)

- Vytvorené **nové samostatné kompletné katalógy `de/helpTxt.po` a `fr/helpTxt.po`**, každý s presne **189 skutočne preloženými zhodnými referenčnými `msgid`**. Súbežne boli vytvorené aj ich skompilované **GNU UTF-8 `helpTxt.mo`** (190 záznamov v každom, vrátane hlavičky). Bez zmeny existujúcich prekladov, grafiky alebo runtime správania.
- Zachované technické názvy, súbory, lokálne cesty, jednotky a tlačidlá (Enigma2, IMDb, TMDb, ECM, PID, PIP, OLED, Picon, Netatmo, `skin.xml`, `satellites.xml`, `hdg17.conf`, `piconProv`, HDD/SSD, Mb/s, kb/s atď.). Reálne nápovedy obsahujú aj rozsiahlejšie vysvetlenia funkcií, nie anglický fallback.
- Kódy jazykov v gettext hlavičkách: **`de_DE`** a **`fr_FR`**, platný `charset=UTF-8` a pravidlá plurálu. Prvá chyba unikajúcich nových riadkov v hlavičke `de` bola pred uzavretím tejto dávky opravená.
- Priamo validované obe `.mo` ako GNU gettext binárne tabuľky: magic `0x950412de`, presne 190 záznamov pre každú, byte rozsahy, UTF-8 a **190/190 presných dvojíc kľúč/hodnota `.mo` ↔ `.po`** vrátane hlavičiek. Rozšírený `tools/test-warder-catalog-integrity.py` o kontrolu 189 referenčných kľúčov, nevyplnených položiek, metadata, gettext načítania a vzoriek pre `de` aj `fr`; kontrola placeholderov beží cez existujúci všeobecný test. Nový CI beh čaká na konečný výsledok, nie je vopred označený ako PASS.
- Aktuálne `helpTxt` existuje pre **8 z 20 lokalizovaných jazykov**: `cs, de, el, fr, lt, ru, sk, zh`; **12 chýbajúcich jazykov × 189 = 2 268 referenčných fráz**. Estónske `eWeather` bolo medzičasom samostatne rozšírené na **1 315/2 117** (zostáva **802**); `eWeather` chýba pre ďalších 15 jazykov (15 × 2 117 = 31 755). **Zostáva teda eWeather 32 557 a helpTxt 2 268, spolu presne 34 825 referenčných prekladových položiek.**
- Hlavné `setupGlass17` (**20 × 517/517**), `weather` (**20 × 108/108**) a `netatmo` (**20 × 42/42**) zostávajú podľa existujúcich regresných inventárov vyplnené; neznamená to nezávislú korektúru všetkých viet rodenými hovoriacimi. Fyzický test na boxoch je stále otvorený.
- Všetko iba v pracovnej vetve `fix/skin-i18n-21-languages-20261117`. **Žiadne IPK, feed, release, zmena verzie, zlúčenie do `main` ani neschválené grafiky.**

## Tretia kompletná nápoveda 18. 11. 2026 – španielčina (+189)

- Doplnený celý nový španielsky katalóg `es/LC_MESSAGES/helpTxt.po`: **189/189 skutočných prekladov**, všetky identické referenčné `msgid` voči `sk/helpTxt.po`, žiadny prázdny `msgstr`, bez prepisu starých prekladov.
- Skompilované `es/LC_MESSAGES/helpTxt.mo` (**190 GNU gettext záznamov vrátane hlavičky**), platné UTF-8, `Language: es_ES`, korektná hlavička a pravidlá plurálu. Binárne kontrolované magic `0x950412de`, dĺžky/offsety a **190/190 presných prekladových dvojíc medzi `.po` a `.mo`**.
- Pridaný regresný test všetkých 189 položiek, konkrétnych prekladov, hlavičky `es_ES` a test načítania `gettext.GNUTranslations`. Existujúci celoplošný test kontroluje bezpečnosť printf placeholderov `%s/%d`. Konečný výsledok nového CI behu musí byť ešte potvrdený, nemá vopred status PASS.
- Spolu v tomto súvislom behu boli pridané **3 plné nové katalógy helpTxt: nemčina, francúzština a španielčina (3 × 189 = 567 skutočných prekladov)**, šesť nových `.po/.mo` súborov a regresné testy.
- **Aktuálne helpTxt: 9 z 20 lokalizovaných jazykov** (`cs, de, el, es, fr, lt, ru, sk, zh`); chýba **11 × 189 = 2 079**. **eWeather** bez zmeny v tejto dávke: **32 557** chýbajúcich referenčných položiek (15 úplne chýbajúcich katalógov × 2 117 + 802 v estónčine). **Celkové zostávajúce množstvo: 34 636 presne podľa katalógového inventára**, nie percentuálny odhad.
- Žiadna IPK, feed, release, zmena verzie, zlúčenie do `main` ani neschválená grafika. Zostáva jazyková korektúra a fyzické testy.

## Oprava identifikátorov jazykov hlavného skinu – 18. 11. 2026

- Preverené `Language:` hlavičky všetkých 20 `setupGlass17.po` katalógov. **Sedem historicky nesprávnych alebo neúplných hodnôt bolo opravených**: `de: sk_SK → de_DE`, `es: en_GB → es_ES`, `it: en_GB → it_IT`, `lt: lt → lt_LT`, `nl: nl → nl_NL`, `ru: ru → ru_RU`, `zh: zh → zh_CN`.
- **Zmenených 14 súborov (`setupGlass17.po` a príslušné `setupGlass17.mo` v týchto siedmich jazykoch)**, zachovaných všetkých **517/517 referenčných prekladov na jazyk**, bez prekladu technických názvov a bez zmeny kľúčov.
- Všetkých sedem binárnych katalógov má **518 GNU gettext správ vrátane hlavičky**, správny `Language:` a UTF-8. Priamou kontrolou celých binárnych tabuliek bolo potvrdených **7 × 518 = 3 626/3 626 presných zhodných dvojíc kľúč/hodnota `.mo` ↔ `.po`**; žiadne mimoriadne `.mo` kľúče neboli stratené.
- Nový regresný test `test_main_gettext_language_headers_match_locale` kontroluje všetkých **20 jazykových kódov** priamo v `.po` aj načítanom `.mo`; kontrola 20 skompilovaných hlavičiek bola aj samostatne vykonaná a všetky boli zhodné.
- **Množstvo chýbajúcich fráz sa nemení: 34 636** (`helpTxt` 2 079, `eWeather` 32 557). Korektnosť ostatných domén `Language:` nie je týmto konkrétnym testom uzavretá; nasledujúce dávky môžu preveriť aj tie.
- Čaká sa na finálny výsledok CI posledných commitov; bez IPK, feed, release, zmeny verzie alebo zásahu do `main`.
