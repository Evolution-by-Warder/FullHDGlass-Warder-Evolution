# FullHDGlass — jazykový audit 17. 11. 2026

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
| al | — | — | 42/42 | — |
| cs | 189/189 | 108/108 | 42/42 | 2117/2117 |
| de | — | 108/108 | 42/42 | — |
| el | 189/189 | 108/108 | 42/42 | 2117/2117 |
| es | — | 108/108 | 42/42 | — |
| et | — | 108/108 | 42/42 | 96/2117 |
| fa | — | — | 42/42 | — |
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
| tr | — | — | 42/42 | — |
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

Doplniť chýbajúce jazykové katalógy podľa tabuľky (weather zostáva pre al/fa/tr), 2 021 estónskych eWeather kľúčov; následne kontrola kontextu a jazykovej kvality, úspešné CI a fyzický test na OpenATV/OpenPLi.

## Voliteľné jazykové katalógy – 18. 11. 2026

**Implementácia v pracovnej vetve, bez vydania IPK:** ostrý zostavovací skript `tools/build-release-ipk.py` je upravený tak, aby do budúcej zostavy pridal iba anglické `.mo` (ak sú k dispozícii) a malý manifest SHA-256. Ostatné `.mo` zostávajú v zdrojovom repozitári, odkiaľ sa stiahnu iba pre jazyk zvolený v Enigma2. Zdrojové `.po` sa naďalej nebalí.

- Manifest je vytvorený počas zostavenia z aktuálnych `.mo` a pripnutý na konkrétny 40-znakový Git commit. Sťahovač overuje SHA-256, binárny gettext formát, veľkostný limit a cieľový URL pred atómovým nahradením súboru.
- `postinst` spustí iba neblokujúcu synchronizáciu aktuálneho jazyka; pri ďalšom otvorení obrazovky v novom jazyku môže gettext resolver spustiť doťahovanie na pozadí. Neúspech siete nezablokuje inštaláciu, pôvodné stiahnuté katalógy sa neodstraňujú a anglický zdrojový fallback zostáva.
- Doplnený `tools/test-warder-locale-on-demand.py` a kontroly v `.github/workflows/verify-skin-i18n.yml`. Fyzický test na Enigma2 boxe ani úspech najnovšieho CI zatiaľ nie je potvrdený.
- **Pokrytie prekladov sa týmto nemení:** setupGlass17 20 × 517/517, Netatmo 20 × 42/42; gréčtina eWeather 2117/2117, estónčina 96/2117 (zostáva 2021). Chýbajúce katalógy helpTxt, weather, eWeather ostatných jazykov sú stále rozpracované, nie „hotové“ vďaka anglickému fallbacku.
- **Žiadne vydanie, IPK, feed, zlúčenie do main ani zmena verzie.** Nová politika balenia sa prejaví až pri budúcom schválenom zostavení.
