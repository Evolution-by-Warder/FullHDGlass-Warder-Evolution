# 23.5E / Canal+ SK / Canal+ CZ — zjednotenie piconov

Spoločné picony v plných balíkoch 23,5°E používajú presné pôvodné PNG bajty z navzájom zhodných Canal+ SK/CZ balíkov. Kontroluje sa technická referencia a orbitálna pozícia, nie iba názov stanice. Cudzie orbitálne aliasy sa nemenia.

| Rozlíšenie | Pozadie | Zjednotené PNG | Doplnené referencie | Ostatné pôvodné PNG zachované |
|---|---|---:|---:|---:|
| 220x132 | black | 142 | 0 | 2081 |
| 220x132 | transparent | 2 | 0 | 2221 |
| 220x132 | white | 157 | 0 | 2066 |
| 400x240 | black | 2 | 9 | 2072 |
| 400x240 | transparent | 2 | 9 | 2072 |
| 400x240 | white | 2 | 9 | 2072 |
| 50x30 | black | 2 | 9 | 2072 |
| 50x30 | transparent | 2 | 9 | 2072 |
| 50x30 | white | 2 | 9 | 2072 |

Celkovo: 313 zjednotených PNG a 54 doplnených referencií naprieč 9 variantmi. Počty obrázkov neznamenajú rovnaký počet staníc, pretože zahŕňajú rozlíšenia, pozadia a technické aliasy.

Ostatných 462 balíkov aj oba zdrojové Canal+ balíky zostávajú zachované. Staré publikované archívy zostávajú dostupné pod pôvodnými názvami.

## Overenie

- Skutočný sťahovací a inštalačný engine PiconHub 0.1.38 úspešne spracoval všetky tri selektory naraz vo všetkých deviatich variantoch.
- Druhý inkrementálny beh: 0 pridaných, 0 zmenených, 0 odstránených.
- Úplné nahradenie odstránilo skúšobnú neaktuálnu referenciu 23,5°E a zachovalo picon inej orbitálnej pozície.
- Synchronizácia podľa TV bouquetu aj dávka dvoch samostatných profilov prešli.
- Pri každom archíve sa overili SHA256 jeho častí, celého ZIPu a všetky pôvodné i nové PNG bajty.
- Výsledky sú hostiteľské testy s reálnym enginom; overenie na fyzickom prijímači zostáva na používateľovi.

## Použitie

Po zverejnení do produkčného katalógu stačí znovu spustiť sťahovanie piconov. Nové IPK ani zmena nastavení profilov nie sú potrebné. Táto dátová oprava nemení stabilný aktualizačný kanál pluginu.

Podrobné referencie a pôvodné/nové SHA256: [canal-unification-20261101.json](canal-unification-20261101.json).

## Stav zverejnenia

Oprava je zverejnená v produkčnom katalógu (commit `24a32b227f60dbc92b42579dd7f52dfd864ad220`). Po zverejnení bolo všetkých 27 verejných archívov znovu stiahnutých a overených podľa SHA256. Vo všetkých deviatich variantoch zostáva **0 nezhodných spoločných PNG a 0 chýbajúcich natívnych referencií Canal+**. Ostatných 462 záznamov balíkov sa nezmenilo. [Záznam verejného overenia](canal-live-verification-20261101.json).
