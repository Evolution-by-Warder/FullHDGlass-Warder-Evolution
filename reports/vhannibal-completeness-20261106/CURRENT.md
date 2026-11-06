# Spoločný kandidát pre Vhannibal – 6. 11. 2026

Tento výsledok nahrádza samostatné návrhy #47 a #49. Pôvodné audity ostávajú dostupné na pripnutých commitoch [#47](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/tree/96a5d6c93f75af1c8100c7ed05b2b229a48ffefd/reports/vhannibal-completeness-20261106) a [#49](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/tree/9183905ee57c325fa297eaa9204bf2ea882ad11c/reports/vhannibal-completeness-20261106). Historické `summary.json`, `reference-ledger.*` a `approved-reuse-repairs.json` na tejto vetve sú dôkazom pôvodného stavu #47. Pre výslednú publikáciu rozhoduje [reconciliation.json](reconciliation.json), ktorý obsahuje presné rozdiely voči nim, všetky povolené zmeny členov ZIPov a hash manifestu.

| Rozhodnutie | Výsledok |
| --- | --- |
| Karavan TV | Deväť spoločných PNG má identické SHA256. Zachovaná je jediná sada z #47 v spoločných ZIPoch na 13°E. |
| Quest Red | Deväť spoločných referenčných pozícií má rozdielne SHA256. Zachovaných je všetkých deväť variantov z #47 s doloženou pixelovou zhodou pôvodného Vhannibalovho obrázka s donorom. Pôvodné existujúce donory zostávajú zachované. |
| Viasat Kino | Deväť variantov z #49 nahrádza zastarané TV1000 na rovnakej plnej referencii v balíkoch 1.9°E. |
| Telesur English a Daystar | Dva nové názvy na 11067.5 V, 19.2°E (SID 31307 a 31310), sú doložene neaktuálne po odchode 5. novembra. Kandidát používa pôvodné produkčné ZIPy 19.2°E. Obe opravy zostávajú v pripnutom audite #47. [KingOfSat](https://en.kingofsat.eu/news) |

Zjednotený inventár používa širší register #47 s 14 808 unikátnymi plnými referenciami. Obsahuje 10 433 aktuálnych satelitných TV referencií po oddelení dvoch uvedených odchodov, 2 704 položiek mimo rozsahu, 2 doložené odchody a 1 669 historických položiek alebo položiek bez presnej aktuálnej zhody.

**Opravených je 25 rôznych referencií** v 69 ZIPoch. Z toho 21 sú aktuálne TV referencie a štyri zachované staršie typové aliasy. Pribudlo 168 PNG a nahradených je 21 PNG. Pri 10 313 aktuálnych TV referenciách je prítomných deväť platných variantov. Pri **120 zostáva problém**. V 118 prípadoch chýba variant a dva chránené prípady TV5MONDE majú prázdny PNG. Viasat Kino je oprava identity pri už kompletnej sade deviatich PNG a nemení počet kompletne obsadených referencií.

Audit grafickej zhody V9 a súpis nejasných identít z #47 ostávajú k dispozícii. Pokrytie názvov a variantov neuzatvára revíziu log. Zmeny sú pripravené na pracovnej vetve.

Všetkých 556 pôvodne otvorených zdrojových referencií z #49 má záznam aj v širšom registri #47. Spoločný strojový report zachováva krížovú kontrolu ich rozsahu a hashový dôkaz deviatich variantov SIKA TV z #49.

## Overenie spoločného kandidáta

Prešiel validátor manifestu, kontrola SHA256 všetkých častí zmenených archívov, CRC, rozmery a skúška skutočnej inštalačnej funkcie pre všetkých 69 zmenených ZIPov. Porovnanie po bajtoch potvrdilo 127934 nezmenených položiek v dotknutých archívoch. Všetkých 18 schválených CANAL+ SK/CZ ZIPov používa identické časti z produkcie. [Strojový výsledok overenia](reconciliation-checks.json)
