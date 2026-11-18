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
| Historické eWeather | 1 014/2 117 |

**Grécke eWeather:** po ďalších 170 ručne pripravených meteorologických frázach obsahuje katalóg 1 014/2 117 prekladov; zostáva 1 103 prázdnych položiek.

## Inventár vedľajších katalógov
Údaje sú **prítomné preložené kľúče / referenčný počet**: nápoveda 189, počasie 108, Netatmo 42 a rozšírené počasie eWeather 2 117. Znak **—** znamená, že pre daný jazyk úplne chýba samostatný katalóg `.po`; nie je to dokončený preklad. Kontrola sa týka súborov pracovnej vetvy a nenahrádza jazykovú ani fyzickú validáciu.

| Jazyk | helpTxt | weather | netatmo | eWeather |
|---|---:|---:|---:|---:|
| al | — | — | — | — |
| cs | 189/189 | 108/108 | 42/42 | 2117/2117 |
| de | — | 108/108 | 42/42 | — |
| el | 189/189 | 108/108 | 42/42 | 1014/2117 |
| es | — | — | 42/42 | — |
| et | — | 108/108 | — | 96/2117 |
| fa | — | — | — | — |
| fr | — | 108/108 | 42/42 | — |
| hu | — | 108/108 | 42/42 | — |
| it | — | — | 42/42 | — |
| lt | 189/189 | 108/108 | — | 2117/2117 |
| nl | — | 108/108 | 42/42 | — |
| pl | — | 108/108 | 42/42 | — |
| pt | — | — | 42/42 | — |
| ro | — | 108/108 | 42/42 | — |
| ru | 189/189 | 108/108 | 42/42 | — |
| sk | 189/189 | 108/108 | 42/42 | 2117/2117 |
| tr | — | — | 42/42 | — |
| uk | — | 108/108 | 42/42 | — |
| zh | 189/189 | 108/108 | 42/42 | — |

Pri gréčtine zostáva **1 103 nepreložených fráz eWeather**; všetkých 189 kľúčov helpTxt je už preložených. Pri estónčine obsahuje eWeather iba 96 z 2 117 kľúčov, teda **2 021 chýba**. Väčšina ďalších jazykov potrebuje celé chýbajúce doplnkové katalógy.

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

## Stále chýba

Doplniť chýbajúce jazykové katalógy podľa tabuľky, 2 021 estónskych eWeather kľúčov a 1 103 gréckych eWeather prekladov; následne kontrola kontextu a jazykovej kvality, úspešné CI a fyzický test na OpenATV/OpenPLi.
