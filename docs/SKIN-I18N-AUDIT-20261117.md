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
| Albánsky (al) | 169 |
| Nemecký (de) | 0 |
| Španielsky (es) | 0 |
| Estónsky (et) | 0 |
| Perzský (fa) | 174 |
| Francúzsky (fr) | 0 |
| Maďarský (hu) | 0 |
| Taliansky (it) | 0 |
| Holandský (nl) | 0 |
| Poľský (pl) | 0 |
| Portugalský (pt) | 0 |
| Rumunský (ro) | 0 |
| Turecký (tr) | 0 |
| Ukrajinský (uk) | 0 |

**V 2 hlavných katalógoch zostáva 343 prázdnych položiek.** Angličtina (en) je zdrojová verzia.

## Gréčtina

| Oblasť | Preložené |
|---|---:|
| Nastavenia setupGlass17 | 515/515 |
| Nápoveda helpTxt | 150/150 |
| Počasie weather | 108/108 |
| Netatmo | 42/42 |
| Historické eWeather | 345/2 117 |

**Grécke eWeather:** ďalších 200 meteorologických a používateľských fráz bolo preložených (spolu 345); zostáva 1 772 prázdnych položiek.

## Čo je zapísané

- Technický resolver pre 21 jazykov v štandardnom GNU gettext, bezpečný anglický fallback a zachovanie vypínača prekladov.
- Nové katalógy .po/.mo pre gréčtinu a doplnené preklady pre ostatné jazyky.
- Nové hlavné preklady v 14 ďalších jazykoch vrátane úplného dokončenia nemčiny, francúzštiny, holandčiny, španielčiny, taliančiny, estónčiny a poľštiny, portugalčiny, rumunčiny, ukrajinčiny, turečtiny a maďarčiny, nezmenené existujúce vyplnené hodnoty.
- Kontroly python3 syntaktiky, binárnych katalógov a regresné CI testy dokončených jazykov (DE/FR/NL/ES/IT/ET/PL/PT/RO/UK/TR/HU) v `tools/test-warder-catalog-integrity.py`. Opravený chybný test, ktorý považoval hlavičku gettext `msgid ""` za nepreloženú frázu. Stav CI musí ešte potvrdiť nasledujúci beh GitHub Actions.
- Zdrojové zmeny bez zostavenia alebo vydania IPK.

## Stále chýba

Preklad zostávajúcich 343 položiek v ďalších 2 hlavných katalógoch (al, fa) a textov, úplné pokrytie nápovied a rozšíreného počasia, kontrola kontextu i jazykovej kvality a fyzický test na OpenATV/OpenPLi.
