## 2026-11-10 — Batch 19 research checkpoint: independent audit PASS

Independent audit of `116e0aed` → `3edd726b` passed: exactly three documentation files; 47 unique open references annotated (16+6+23+1+1), no status changes or binary modifications. Counts remain **48 TV / 429 PNG / 99 ZIP / 86 open**. PASS confirms checkpoint integrity, not batch completion. Batch 19 remains **IN_PROGRESS_NO_SAFE_INTEGRATION**. Audit: `reports/vhannibal-followup-20261106/scope-batch-20261110-19-checkpoint-audit.json`. Continue only with new decisive evidence; preserve existing blockers and approved artwork.

### Dávka 19 – nový prieskum piatich skupín, bez integrácie – 10. 11. 2026

- Základ `116e0aed0590bbdd9d6747ee0a44fd78560be7fc`. **48 TV / 429 PNG / 99 ZIPov / 86 otvorených.** 0 integrácií, 0 technických uzavretí; dávka19 zostáva rozpracovaná.
- Päť skupín zahŕňa47otvorených referencií: Test23.5E16, MCK68.5E6, DSNS23, feed7E1 aRadioClassica1. Ide o skupinové dôkazy, nie47nových meraní. Podrobnosti a ďalší požadovaný dôkaz sú v `scope-batch-20261110-19-research.json` a dotknutých riadkoch `remaining-review.json`.
- Satindex potvrdil historickú zmenu ONID/TSID pre Test6303, ale neidentifikoval program. LyngSat potvrdzuje dva MCK transporty bez názvov cieľových služieb. Historická DSNS konfigurácia patrí inému TSID/ONID. Feed7E má iba frekvenčný údaj. Pri RadioClassica zdanlivá zhoda NID29 vo vyhľadávači patrí nasledujúcemu streamu35; nepoužitá.
- Žiadne domyslené aliasy ani nové logá. ALKAFEEL.TV ponechaná lokálne a blokovaná; bez renderu/uploadu. SES ASTRA nepoužitá. Dávky1–18 neauditované znova. Všetkých18CANAL+,PNG/ZIPy,manifest,rádio a produkcia bez zásahu. Inštalačné testy N/A.
- Pokračovať dávkou19 iba novým presným dôkazom podľa registra; neprezentovať tento prieskum ako dokončené referencie. PR50 nezlučovať.

### Dávka 18 – jedno technické uzavretie, nezávislý audit PASS – 10. 11. 2026

- Základ `077f909f0db3b95deb1c34017b6da022292b46dd`. **48 TV / 429 PNG / 99 ZIPov / 86 otvorených (80 pôvodných + 6 delta).** 0 nových grafických integrácií; 1 technické uzavretie.
- Test HD `1_0_1_1C2D_48_1_DC00000_0_0_0`: LyngSat explicitne uvádza testovací obrazec na8W12563H, SID7213/TSID72/ONID1; KingOfSat potvrdzuje rovnaký SID, VPID7244/APID7245 a symbol testovacieho obrazca. Nejde o zánik ani dátovú službu. Iraqia Sport má SID7207 a VPID7213; tento PID sa nesmie zameniť za SID cieľa.
- Report `reports/vhannibal-followup-20261106/scope-batch-20261110-18-completed.json`; aktualizované remaining-review, identity-evidence a register dávky18. Pôvodné porovnanie Ciefp ostáva historických87 cieľov; aktuálne86otvorených plus1uzavretý obrazec.
- Štyri Spare7W, Test SID7411 a HS1 zostávajú blokované; nové podklady a konkrétne chýbajúce dôkazy v reporte. Presun frekvencie Spare5677/5678 sa nepovažuje za zánik. Service11-13, ITA99A a1TV Iraq sa znova nekontrolovali.
- ALKAFEEL.TV originál, náhľad a9variantov ostávajú lokálne, mimo ZIPov; žiadny upload ani render. SES ASTRA nepoužité. Dávky01–17 neopakované.
- Iba dokumentácia; PNG/ZIPy/manifest,18CANAL+ archívov,rádio a produkcia bez zásahu. Inštalačné testy N/A. PR50 nezlučovať. Ďalej86otvorených podľa registra, iba nové rozhodujúce dôkazy.
- Nezávislý záverečný audit payloadu `a2231f0f13feb47d4777eb36a755189a8fcae4e8`: PASS. Presne5dokumentačných ciest; zmenený1riadok remaining-review,81→80pôvodných +6delta =86otvorených. Spätne načítaných5/5súborov presne zhodných. Katalógová klasifikácia, nie prijímačové meranie; audítor LyngSat403, pôvodné úspešné načítanie a KoS presná tabuľka zachované. Audit `scope-batch-20261110-18-remote-verification.json`.

### Dávka 18 – obnovenie prerušeného spracovania – 10. 11. 2026

- Obnovovací report: `reports/vhannibal-followup-20261106/scope-batch-20261110-18-recovery.json`, commit `a6de4ddf6e522c2866c34dc76bab7ab589931e47`; spätné načítanie celého textu presne zhodné.
- Zachovaných lokálne 17 súborov z prerušeného behu vrátane originálu, 9 ALKAFEEL.TV návrhov, náhľadu a metadát; 17/17 SHA256 sedí s pôvodným inventárom. Žiadny nový render ani binárny upload. **Návrhy NIE SÚ commitnuté v PR #50**: inventár zmien ich neobsahuje, priame načítanie review.json na pôvodnom HEAD vracia 404. Lokálne cesty a hashe sú v reporte; nejde o trvalú vzdialenú zálohu PNG.
- Hlásená chyba bola iba „Unknown error“; presná technická príčina nie je doložená. Prenos zostáva NEDOKONČENÝ, bez opakovania Base64 pokusov alebo novej autentifikácie/prenosovej metódy.
- Oficiálna projektová stránka potvrdzuje vzťah vlastníka k alkafeel.tv, nie presný satelitný tuple. ALKAFEEL.TV ostáva mimo ZIPov do potvrdenia identity aj vizuálneho schválenia. SES firemné podklady už v PR sú; SES ASTRA sa nepoužíva.
- Ďalší cielený prieskum: Service 11-13 má vo zverejnenom transporte z 10.11. nenulový AV tok (SID8); chýba programová identita, neuzatvárať ako zánik/dáta. ITA99A a 1TV Iraq indexované podklady patria iným frekvenciám; žiadne prenesenie loga ani uzavretie.
- **48 TV / 429 PNG / 99 ZIPov / 87 otvorených. Dávka18 rozpracovaná.** 0 nových integrácií, 0 technických uzavretí. Iba dokumentácia; inštalačné testy N/A. Dávky01–17 neopakované; ZIPy, manifest, všetkých18 CANAL+ archívov, rádio a produkcia bez zásahu. PR50 nezlučovať.
- Ďalej pracovať podľa 87 riadkov scope-batch-20261110-18-research.json iba s novým dôkazom; nevracať sa k už neúspešným dotazom. Zachované lokálne návrhy znovu nevytvárať.

### Dávka 18 – nový nezávislý zoznam, rozpracované – 10. 11. 2026

- Základ `dc5e7508af81d708720b4004ebad0ee84c7e8933`; dávky 01–17 sa neopakovali.
- Aktuálny Ciefp motorový lamedb: 13 463 služieb, 87 presných porovnaní SID/TSID/ONID/namespace, 14 zhôd a 73 nenájdených. Nenájdenie v kurátorovanom zozname nie je dôkaz zániku.
- Dve presné zhody dopĺňajú identitu SES DEMO HD 2025 test (45°E 12520 V a 66°E 11089 V); vhodná schválená HD grafika chýba. DSNS historické presuny nepreukazujú ukončenie služby.
- **48 TV / 429 PNG / 99 ZIPov / 87 otvorených.** Žiadna nová bezpečná integrácia ani technické uzavretie. Dávka18 NIE JE dokončená. Register priorít a presné zhody: `reports/vhannibal-followup-20261106/scope-batch-20261110-18-research.json`.
- 5 prípadov vyžaduje správnu schválenú grafiku, 80 presnú identitu/klasifikáciu, 2 sú chránené TV5MONDE. Všetky pôvodné blokácie platia. Bez zásahu do PNG/ZIPov, 18 CANAL+ archívov, rádia, produkcie či main. Inštalačné testy N/A: žiadny inštalovateľný obsah sa nemenil. PR #50 nezlučovať.

# Warder Evolution – stav projektu

### Dávka 17 – dve doložené technické uzavretia – 10. 11. 2026

- Prejdených všetkých **89 otvorených referencií** podľa existujúcich blokácií; nejde o 89 nových meraní. Uzavreté 2 presné staré transporty: Test 1 / Al Shabab TV na 7°W SID 459 / TSID 16 / ONID 110 (odchod 3. 11.) a Service-1 / Al Rabiaa Iraq na 3°E SID 1 / TSID 1 / ONID 65535 (odchod 2. 11.). Priame aktuálne histórie KoS archivované; staršie pozitívne indexy sa nepovažujú za návrat.
- **48 spracovaných TV referencií / 429 PNG / 99 jedinečných ZIPov; 87 otvorených (81 pôvodných + 6 delta).** Táto dávka pridala 0 PNG a nezmenila žiadny ZIP. Technické uzavretia sa nepripočítavajú k 48 graficky dokončeným referenciám.
- Existujúce PNG oboch historických referencií zachované. Všetkých 18 CANAL+ archívov, TV5MONDE, rádio, produkcia a stabilné balíky bez zásahu. Inštalačné testy sa neopakujú: nie je zmenený inštalovateľný obsah. PR #50 nezlučovať.
- Report `scope-batch-20261110-17.json`; úplný register 89 položiek `scope-batch-20261110-17-all89-review.json`. Zvyšných 87 ostáva blokovaných konkrétnymi uloženými dôkazmi/ochranou/grafikou. Pri pokračovaní preskočiť identické neúspešné dotazy; otvoriť iba nový dôkaz alebo schválenú správnu grafiku.
- Záverečný vzdialený audit PASS: 12 súborov / 1 155 435 bajtov presne zhodných s kandidátom. GitHub porovnanie potvrdilo 0 zmien PNG, ZIPov, manifestu alebo produkcie. Payload `d0043f949ed50bbb116e91decdb7488a6ef05774`; audit `scope-batch-20261110-17-remote-verification.json`. Dávka 17 dokončená dvoma technickými uzavretiami.

### Dávka 17 – ďalší prieskum, bez bezpečnej integrácie

- Pokračovanie: priame dátové katalógy nevyriešili BFBS SID8016 ani Thor SID65534. Meracie endpointy vrátili overovaciu stránku bez servisných dát; nevydávať za meranie. Dva konkrétne riadky registra majú uložený chýbajúci dôkaz a zákaz opakovania rovnakého slepého vyhľadávania. Počty sa nemenia; žiadne ZIPy ani PNG sa neupravovali a inštalačné testy sa preto neopakovali.

- Dávka16 dokončená a auditovaná: **48 TV / 429 PNG / 99 jedinečných ZIPov; 89 otvorených**. Nový prieskum17 nepridal PNG ani technické uzavretie a nie je vykázaný ako dokončená dávka.
- Nové priame podklady Sky2117/2118 patria iným SID než cieľovým51074/51078. SES Demo HD66°E má odlišný sieťový údaj a nemá potvrdenú schválenú HD sadu. Dôkazy a presné blokácie: `scope-batch-20261110-17-research.json`. Pokračovať iba novým rozhodujúcim dôkazom; neopakovať hotové dávky ani nepreberať podobné názvy.

### Dávka 16 – TEMP 1 potvrdené ako Sky News International – 10. 11. 2026

- **1 TV referencia / 9 PNG / 9 ZIPov. Kandidát 48 TV / 429 PNG / 99 jedinečných ZIPov; 89 otvorených (83 pôvodných + 6 delta).** Žiadne technické uzavretie iba podľa názvu.
- Nový priamy záznam viaže TEMP 1 na Sky News International: 15°W, 12666.50 H, SID 105 / TSID 10; pôvodný Vhannibal má ONID 1. Austrálska verzia je samostatný SID 113. Presná referencia `1_0_1_69_A_1_D7A0000_0_0_0` používa existujúcich 9 schválených Sky News Intl PNG, bez renderovania.
- Zachované pôvodné ZIP členy, celé byte prefixy, všetkých 18 CANAL+ archívov a všetky ostatné balíky. Report `reports/vhannibal-followup-20261106/scope-batch-20261110-16.json`. Payload `bd076557a2e74716f491646fc8a9f6f996851fa3`. Záverečný vzdialený audit PASS: 56 ciest, 36 častí, 17929251 bajtov; 9 ZIPov SHA256/CRC a presná zhoda 9 PNG. Všetkých 9 inštalačných testov cez kód prijímača PASS; zachovaných 441 pôvodných členov a používateľský PNG. Fyzický prijímač netestovaný. Report `scope-batch-20261110-16-remote-verification.json`.
- Skupiny Test 1–16 na 23,5°E a Service-900/906/907/908/911 na 52°E zostávajú otvorené: označenie neaktivity je v rozpore s nenulovými tokmi. Nevyradiť ako dáta alebo zaniknuté. Nové merania sú uložené v batch16-evidence.
- Produkcia, rádio a main bez zásahu; PR #50 nezlučovať. Predchádzajúci prieskum dávky 16 zostáva historickým podkladom.

### Historický podklad pred dokončením dávky 16 – rozpracovaný prieskum, bez ďalšieho zaradenia – 10. 11. 2026

- Dávka 15 dokončená a spätne overená. **47 TV / 420 PNG / 99 jedinečných ZIPov; 90 otvorených (84 pôvodných + 6 delta).**
- Nový priamy podklad EL JUMHURIA uložený: 12398.60 V, SID 7820, NID 1918 / TID 53600. Iné indexované verzie majú 2048 / 41; schválený správny artwork stále chýba. Nesprávny donor sa nepoužíva.
- Oficiálny Radio Classica web potvrdzuje vlastníctvo TV značky, nie aktívny satelitný TV stream ani sporný ONID. StarzPlay Movies oficiálny detail vracia 403; žiadny nový PNG nebol získaný. 1TV IRAQ sa nezamieňa s 1IraqTV ani s iným transportom.
- Report `reports/vhannibal-followup-20261106/scope-batch-20261110-16-research.json` zachováva nové podklady, výsledky a presné ďalšie kroky. **0 nových PNG, 0 uzavretých prípadov v dávke 16.** Bezpečné integrácie pokračujú až pri doloženom párovaní; nové grafiky sa zhromažďujú na spoločné schválenie. Dávky 01–15 neopakovať. PR #50 nezlučovať.

### Dávka15 – druhá presná UNKNOWN RUSSIA referencia na11012H –10.11.2026

- **1 TV referencia /9 PNG /9 ZIPov. Kandidát47 TV/420 PNG/99 jedinečných ZIPov;90 otvorených (84 pôvodných+6delta).**
- Čerstvé priameHTML Frocus7.11.2026 potvrdzujeSID17368/VPID1268/APID1368 na11012H/30000. Nové transportné podklady SatindexTSID32108 (bitrate31.10.) a SatFRQNID1070/TSID32108 dopĺňajú presnýVhannibal ONID1070/42E. Staršia augustová cache ani septembrové vypnutie neprepisujú návrat7.11. Žiadny rawSDT scan sa netvrdí.
- Presná `1_0_1_43D8_7D6C_42E_1A40000_0_0_0`; všetkých9schválenýchPNG z dávky10 skopírovaných bajtovo vrátaneWHITE, bez renderovania. Zachované pôvodné členy aj úplné ZIP prefixy;18CANAL+,39E Chefi/Antena a všetky ostatné balíky nezmenené.
- Report `reports/vhannibal-followup-20261106/scope-batch-20261110-15.json`; payload `32c0420e8769e4eadedc883974409c746e8a4dc0`. Záverečný vzdialený audit PASS: 133 ciest / 341322284 bajtov, 124 častí, 9 kompletných ZIPov; SHA256, CRC a presná zhoda 9 schválených PNG PASS. Všetkých 9 inštalačných testov cez aktuálny produkčný kód PASS, zachovaný používateľský PNG. Zachovaných 19470 pôvodných položiek. Fyzický prijímač netestovaný. Audit `scope-batch-20261110-15-remote-verification.json`. Produkcia,rádio,main bez zásahu; PR50 nezlúčený. Ďalej dávka16: získať správne oficiálne podklady ostatných otvorenýchTV, bez opakovania blokovaných DSNS/Quadrille/DMDU_T.

### Dávka14 – schválené Chefi.ro zaradené do9 pracovných ZIPov –10.11.2026

- **1 dokončená TV referencia /9 PNG /9 ZIPov. Kandidát46 TV/411 PNG/99 jedinečných ZIPov;91 otvorených (84 pôvodných +7 delta).**
- Všetkých9 variantov vrátaneWHITE výslovne schválených vlastníkom. Presné uložené PNG pre `1_0_16_5_A_16E_1860000_0_0_0`; bez renderovania,prebieľovania či zmeny efektov a alfy. ZU TV nepoužité.
- Zachovaných17484 pôvodných položiek aj celé ZIP prefixy;18 CANAL+ a ostatné balíky nezmenené. SHA256/CRC a zhoda schválenýchPNG PASS. Payload `b8507bb81b482657feb301ccd18f2283f97d837c`; jeden záverečný vzdialený audit PASS:69 ciest/225583785 bajtov,62častí a9úplných ZIPov presne zhodných; SHA256/CRC/9schválenýchPNG PASS. Inštalátor aktuálneho main prešiel na všetkých9ZIPoch so zachovaným používateľskýmPNG. Fyzický prijímač netestovaný. Report `scope-batch-20261110-14-integration-remote-verification.json`.
- Report `reports/vhannibal-followup-20261106/scope-batch-20261110-14-integration.json`. Produkcia,rádio a main bez zásahu; PR50 nezlučovať. Pokračovať dávkou15 s novými dôkazmi; hotové dávky neopakovať.

### Dávka14 – správny oficiálny Chefi.ro originál a9 návrhov – 10.11.2026

- **9 nových návrhov PNG /0 vložených PNG /0 ZIP zmien /0 uzavretých referencií. Kandidát45 TV/402 PNG/99 ZIPov;92 otvorených.**
- Oficiálny AntenaPLAY Live priamo označuje získaný1080×1080 RGBA originál ako logoChefi.ro; oficiálny webChefi.ro potvrdzuje rovnaký emblém. Nesprávny donorZU TV zostáva vyradený. PresnáSID5/TSID10/ONID366 väzba už doložená dávkou13.
- Všetky3 rozmery ×3 pozadia pripravené priamo z originálu, bez prefarbenia a prerábania; MASTER šablóny zachované. Rozmery/alfa/SHA256 PASS. Nový artwork čaká na vizuálne schválenie; zlatá žiara originálu zachovaná, drobný text pri50×30 posúdi vlastník.
- Payload `41010cf619db35cc3c13a5b84fcc46c43a9bb1f2`; spätný audit20 ciest/1851755 bajtov PASS, presná bajtová zhoda vrátane9 návrhov a originálu. Audit `scope-batch-20261110-14-remote-verification.json`.
- Náhľad `reports/vhannibal-followup-20261106/chefi-official-review/review/preview.png`; report `scope-batch-20261110-14.json`. Žiadne zmeny manifestu, balíkov,18CANAL+, rádia ani produkcie. PR50 nezlúčený.
- Dávka13 vzdialene overená: payload29a7fa0150ee944bae6cd377787d3aa9a21e3498; audit checkpoint1c0ebe67b3166980e463926bebb092526474f2f6. Spätné načítanie všetkých3 checkpoint dokumentov bajtovo zhodné.
- Ďalší krok: schválenie9Chefi.ro návrhov pred integráciou; ostatné prípady riešiť len s novým rozhodujúcim podkladom. DSNS/Quadrille/DMDU_T bez opakovaných neúspešných dotazov.

### Dávka13 – šesť Antena referencií po potvrdení TSID10 – 10.11.2026

- **6 TV referencií /54 PNG /9 ZIPov /0 technických uzavretí. Zostáva92 otvorených (84 pôvodných +8 delta). Kandidát45 TV/402 PNG/99 jedinečných ZIPov.**
- Antena1, AntenaStars, Antena3 CNN, Happy Channel, Antena International a Antena HD: nezávislý Satindex scan7.11.2026 doložil TSID0→10 na39°E12655H, NID366 a presnéSID1/2/3/4/6/7. Vhannibal12656H má rovnaký transport. Existujúce schválené PNG skopírované bez prerenderovania; SD/HD aj International odlíšené.
- Chefi.roSID5 má už potvrdenú identitu, ale existujúci donor má nesprávne logoZU TV. Ostáva otvorené iba pre správnu grafiku; žiadneZU TV vložené.
- SHA256/CRC/rozmery/alfa a bajtové zachovanie pôvodných členov aj úplných ZIP prefixov PASS.18 CANAL+ a ostatné balíky nezmenené. Payload `29a7fa0150ee944bae6cd377787d3aa9a21e3498`; vzdialený audit PASS:117 ciest/224760282 bajtov,53 častí a9 úplných ZIPov bajtovo zhodných;54 donorových PNG a CRC PASS. Inštalačné testy9 ZIPov na aktuálnom main PASS so zachovaním používateľského PNG. Fyzický prijímač netestovaný. Audit `scope-batch-20261110-13-remote-verification.json`.
- Dôkazy a donorové hashe: `scope-batch-20261110-13.json`;54 skutočnýchPNG v `antena-approved-reuse-batch13/`. Produkcia, rádio, aktívnaKuukaudenTSID72 aTV5MONDE nezmenené. PR50 nezlúčený.

### Dávka12 – doložený odchod starej Kuukauden referencie – 10.11.2026

- **0 nových TV referencií /0 PNG /0 ZIPov /1 uzavretá neaktívna referencia. Zostáva98 otvorených (84 pôvodných +14 delta). Kandidát39 TV/348 PNG/99 jedinečných ZIPov.** Nejde o dátovú službu ani zánik stanice.
- Uzavretá `1_0_16_42BC_A_46_E080000_0_0_0`: nový explicitný záznam8.11.2026 potvrdzuje odchod10934.6V/SID17084; starýTSID10/ONID70 doložený pôvodnými parametrami. Hotová referenciaTSID72 na10871.9H bez zmeny. Historické súbory zachované.
- Kompletné rozdelenie99 vstupných prípadov a požadované dôkazy pri každom sú v `identity-evidence-20261107.json` → `continuation_20261110_batch12.triage`. Žiadny pripravený bezpečný donor;2 TV5MONDE prípady vyžadujú ochranu kanonickej grafiky, ostatné otvorené prípady presnú identitu/klasifikáciu alebo použiteľný podklad. Bez nového dôkazu neopakovať rovnaké dotazy.
- Dôkazy: `scope-batch-20261110-12.json` a3 zachytené zdrojové stránky. Payload commit `59aa4f7b51b1bee79a355508ff0ec89b48927f7e`; jeden spätný audit7 uložených súborov PASS, bajtová zhoda aSHA256. GitHubdiff iba7 evidenčných/dokumentačných ciest; ZIPy, PNG a manifesty nedotknuté. Audit `scope-batch-20261110-12-remote-verification.json`.
- Balíky, manifesty,18 CANAL+, produkčnýmain a rádio nezmenené. PR50 sa nezlučuje. Ďalšia dávka13 musí vychádzať z nového dôkazu podľa konkrétneho riadka registra; dávky01–12 neopakovať.

### Dávka11 – štyri doložené technické testovacie obrazce – 10.11.2026

- Eutelsat1–4: SID7210/7220/7230/7240, TSID53600, Vhannibal ONID1918, 7°W 12399V. KingOfSat explicitne označuje všetky štyri ako Testcard (7.11.2026); zachytené HTML a presné riadky sú uložené. NID v externom zdroji sa nezamieňa za samostatný dôkaz ONID; väzbu poskytuje existujúci Vhannibal register.
- **0 nových TV referencií /0 PNG /0 ZIPov /4 technické uzavretia. Zostáva99 otvorených (85 pôvodných +14 delta). Kandidát39 TV/348 PNG/99 jedinečných ZIPov.** Ide o neprogramové testovacie obrazce s AV PID, nie dátové služby ani dôkaz zániku.
- Register pôvodných referencií remaining-review.json sa nemení: všetky štyri prípady patria do source_delta v identity-evidence-20261107.json. Historické grafiky a všetky balíky vrátane18 CANAL+ zachované bez zmeny; produkcia a rádio nedotknuté.
- Podklady a rozhodnutie: `reports/vhannibal-followup-20261106/scope-batch-20261110-11.json`. Payload commit `1b4f30ff3c34bf134c6a38ef5318945de9499570`; spätné načítanie všetkých4 zmenených súborov a SHA256 PASS. GitHub diff obsahuje iba tieto4 dokumentačné/evidenčné súbory; žiadny ZIP, PNG, manifest, rádio ani produkčný súbor zmenený. Audit: `scope-batch-20261110-11-remote-verification.json`.
- Cielené preverenie ďalších kandidátov: Sky2117/2118 má konflikt SID/TSID pri údajnom NickJr/MTV aliasovaní; StarzPlay Movies nemá získaný použiteľný oficiálny podklad konkrétnej edície; EL JUMHURIA nemá doloženú grafickú identitu. Žiadna z týchto položiek nebola uzavretá. AL-KAFEL a druhá NTV ostávajú blokované. Pokračovať od dávky12 iba s novým rozhodujúcim dôkazom alebo správnym oficiálnym podkladom; dávky01–11 neopakovať.

### Dávka10 – schválené NTV Неизвестная Россия v pracovných balíkoch – 10.11.2026

- **1 dokončená referencia /9 PNG /9 ZIPov /0 technických uzavretí. Zostáva103 otvorených (85 pôvodných +18 delta). Kandidát39 TV/348 PNG/99 jedinečných ZIPov.**
- Presný11727V tuple `1_0_1_43A6_EAC5_42E_1A40000_0_0_0`; všetkých9 PNG dávky09 explicitne schválených vrátaneWHITE, bez prerenderovania. Druhá11012H referencia sa nepridáva bez aktuálneho úplného tuple.
- Lokálne SHA256/CRC/rozmery/alfa a zhoda schválených PNG PASS. 19461 pôvodných ZIP členov a celé pôvodné archívy ako prefixy bajtovo zachované.18CANAL a ostatné balíky nezmenené.
- Report `reports/vhannibal-followup-20261106/scope-batch-20261110-10.json`; **Balíkový commit `3a30ac0f77f9c90de44b25fd3e8ce29afc7759c7`; jeden záverečný spätný audit PASS:121 ciest/338798286 bajtov,115 častí a9 úplných ZIPov bajtovo zhodných; SHA256/CRC/9 schválených PNG PASS.** Audit `reports/vhannibal-followup-20261106/scope-batch-20261110-10-remote-verification.json`. Validátor manifestu a skutočný inštalátor aktuálneho main prešli na9 archívoch so zachovaným používateľským PNG. Fyzický prijímač netestovaný.
- Súbežne AL-KAFEL: oficiálny nepriehľadný dekoratívny emblém nie je použiteľný ako čistý transparentný picon; Studio logo je nesprávna identita. TSID41/53600 zostáva sporné. Nevytvorených9 nesprávnych variantov.
- Nový produkčný main d4627ca18c966f03f05d11214b26025525ba2556 zachovaný; PiconHub main481e9b9154a510c64c743de72c1a73ed808307bf. Žiadny merge, produkcia ani rádio. Vlastník schválil samostatné pokračovanie bezpečných dávok bez jednotlivého schvaľovania.


### Dávka09 – nové NTV návrhy a oficiálne podklady – 9.11.2026

- **9 nových návrhov PNG** pre NTV Неизвестная Россия / UNKNOWN RUSSIA, všetky3 rozmery ×3 pozadia. Nové oficiálne oznámenie NTV a katalóg vlastníka potvrdzujú rebranding; transparentný originál pochádza z Cableman a je potvrdený oficiálnym vizuálom. `reports/vhannibal-followup-20261106/unknown-russia-official-review/review/`.
- Návrhy čakajú na schválenie. **WHITE má nízky kontrast pôvodného bieleho textu**; bez nepovoleného prefarbenia. Žiadny návrh vložený do balíkov. Prvý11727V tuple už doložený; druhý11012H stále potrebuje aktuálny úplný tuple.
- **0 dokončených TV referencií /0 vložených PNG /0 ZIP zmien /0 technických uzavretí;104 otvorených.** Kandidát zostáva38 TV/339 PNG/99 ZIPov.18 CANAL+ archívov, produkcia a rádio nezmenené.
- AL-KAFEL: uložený nový oficiálny emblém a dôkaz7W12399V; transparentné Studio logo je nesprávny donor. StarzPlay Movies: potvrdený cieľový transport a oficiálny Live katalóg, samostatný obrázok edície nezískaný. TEST_CB:11315V/TSID40060 nemožno zameniť za11277V/40040. SES: nový NID0 záznam vyžaduje rozlíšiť NID/ONID rawtabuľkami; nejde o automatický dôkaz zmeny ONID.
- Lokálna kontrola9 návrhov SHA256/rozmery/alfa PASS, grafická kvalita WHITE vyžaduje rozhodnutie. **Payload `8a2ad7ec0a0494fa74f5f00134e980fb279c0e38`; vzdialený audit PASS:25 súborov/1383125 bajtov načítaných z GitHubu a presne zhodných.** Report `reports/vhannibal-followup-20261106/unknown-russia-official-review/review/remote-audit-batch09.json`. Technický PASS nie je grafické schválenie. Ďalší vykonateľný krok: kontrola9 NTV návrhov vlastníkom, osobitne bieleho textu naWHITE; ostatné prípady len pri doplnení presného chýbajúceho dôkazu.


### Dávka08 – TV8 Turkey schválené a zapracované – 9.11.2026

- Vlastník schválil všetkých9 pripravených variantov. Presné schválené PNG bez prerenderovania vložené pod `1_0_16_390_20D_73_2080000_0_0_0` do9 pracovných520E balíkov. TV8 Turkey, nie International.
- **1 nová TV referencia /9 PNG /9 ZIPov /0 technických uzavretí. Zostáva104 otvorených. Kandidát spolu38 TV/339 PNG/99 jedinečných ZIPov.**
- Lokálne SHA256/CRC/rozmery/alfa a zhoda9 PNG so schváleným checkpointom PASS; 12471 pôvodných členov a celé pôvodné ZIP prefixy bajtovo zachované.18 CANAL+ balíkov a všetky nedotknuté balíky majú nezmenené záznamy a časti.
- Report `reports/vhannibal-followup-20261106/scope-batch-20261109-08.json`. **Balíkový commit `5997c267f3e90b9d5485f43eb07883401fedd5f9`; spätný audit PASS:81 ciest /233529918 bajtov, všetkých74 častí a9 úplných ZIPov bajtovo zhodných. SHA256/CRC/9 schválených PNG PASS. Validátor manifestu a inštalačná funkcia aktuálneho main a711c7940f8137eaa69331a1a4b511f617edad47 prešli na9 archívoch so zachovaným používateľským PNG; fyzický prijímač netestovaný.** Report `reports/vhannibal-followup-20261106/scope-batch-20261109-08-remote-verification.json`. AntenaTSID10/0 a RADIO CLASSICA TV ONID29/0 následne cielene preverené; bez rozhodujúceho nového dôkazu zostávajú blokované. Žiadny merge, produkčné feedy, skin ani rádio.


### Dávka07 – nové oficiálne podklady a TV8 návrhy – 9.11.2026

- TV8 Turkey: **9 nových návrhov PNG**, 3 rozmery × TRANSPARENT/WHITE/BLACK, z oficiálneho originálu ACUNMEDYA; čakajú na grafické schválenie. Náhľad a SHA256: `reports/vhannibal-followup-20261106/tv8-official-review/review/`.
- **0 schválených TV referencií / 0 vložených PNG / 0 upravených ZIPov / 0 technických uzavretí**. Zostáva **105 otvorených**. Kandidát zostáva37 TV/330 PNG/99 ZIPov. Návrhy nie sú súčasťou kandidátnych balíkov.
- Uložené nové oficiálne SES originály a NTV/PREMIER podklady s presnou provenienciou. SES corporate2025 vs HD demo branding a NTV legacy vs current marka zostávajú explicitne blokované; žiadne vymyslené aliasy.
- TV8 rozmery a alfy overené; farby originálu zachované, každý rozmer vytvorený priamo z originálu. Geometria návrhu 204×116 na220×132 je označená na kontrolu; nejde o tvrdenie zmrazeného V9 schválenia. Zdroj216×195 znamená zväčšenie pri400×240.
- Zmenené iba reportové/staging súbory a tento register. Produkcia, rádio, manifesty a všetkých18 CANAL+ archívov bez zmeny. **Payload commit `36706933abcbf849a661aa440ff2b0f04af95e6c`: spätný audit PASS. Všetkých28 zmenených súborov načítaných z GitHubu a bajtovo/Git blob SHA overených; SHA256 a rozmery9 návrhov uložené v `reports/vhannibal-followup-20261106/tv8-official-review/remote-audit.json`.**


### Dávka06 – technická služba ASSOCIATION MATERIEL – 9.11.2026

- **0 nových TV referencií / 0 PNG / 0 ZIPov / 1 technická výnimka / 0 dátových výnimiek**. Zostáva **105 otvorených = 86 pôvodných + 19 delta**; kandidát spolu37 TV/330 PNG/99 jedinečných ZIPov.
- Presný SID9124/TSID1098/ONID1 na19,2°E12363V, VPID2410/APID2421. Technický účel doložený priamym pozorovaním SatExpat a still-image záznamom Satindex; aktuálny Morpheus scan potvrdzuje identitu a AV PID. Nejde o tvrdenie zániku ani dátovej služby. Pôvodné referencie, chýbajúce varianty a všetky balíky zachované.
- Report `reports/vhannibal-followup-20261106/scope-batch-20261109-06.json`; payload commit `d03aadfd4bb4b93484e84639283f1ac2692a5781`; všetky4 zmenené dokumenty spätne načítané a bajtovo zhodné. GitHub compare potvrdil0 asset zmien, manifest aj18 CANAL+ archívov zachované. Menia sa iba registre, žiadne asset cesty.18 CANAL+ archívov zostáva identických.
- SES Demo66°E: fyzicky overený existujúci biely220×132 PNG má nápis UHD Demo Channel; nepoužiť ako dôkaz HD donora. Presný konflikt uložený v registri.
- Živý main FullHDGlass `a711c7940f8137eaa69331a1a4b511f617edad47` už obsahuje stabilnú1.0.76; PiconHub `481e9b9154a510c64c743de72c1a73ed808307bf`. Produkčný stav sa neprepisuje starším kandidátom. Rádio bez zásahu.


### Dávka05 – FUNBOX presná identita potvrdená – 8.11.2026

- **1 TV referencia / 9 PNG / 9 ZIPov / 0 technických výnimiek**. Zostáva **106 = 87 pôvodných + 19 delta**. PR spolu **37 TV referencií / 330 PNG / 99 jedinečných ZIPov**.
- Presný SID7/TSID8135/ONID702 na26°E/12380H je v pomenovanom multiplexe FunBox UHD vysielaný v HD; Fast&FunBox je samostatný SID3. Existujúci schválený donor FunBox UHD zo16°E/SID610/TSID50200/ONID366; značka vizuálne porovnaná s oficiálnym SPI logom. Pôvodný servisný názov FUNBOX HD a referencia zachované.
- Deväť PNG bajtovo skopírovaných, žiadne renderovanie. Lokálne SHA256/CRC/rozmery/alfa PASS, 17 934 pôvodných členov ZIPov a pôvodné ZIP prefixy zachované.18 CANAL+ balíkov nezmenených. Validátor manifestu a inštalačná funkcia1.0.74 PASS; fyzický prijímač netestovaný.
- Report `reports/vhannibal-followup-20261106/scope-batch-20261108-05.json`. Payload commit `4a779afb9528508629b5d64680585113b2250cf6`; vzdialený audit PASS: 113 častí / 307 603 286 bajtov, všetkých 9 ZIPov zhodných bajt po bajte; SHA256, CRC, 9 PNG, manifest, SHA256SUMS a 4 registre overené. Úplný report `scope-batch-20261108-05-remote-verification.json`. Produkcia a rádio bez zmien.

### Dávka 04 – preukázaný profesionálny feed EBU – 8. 11. 2026

- EBU 1 ENC, presný SID1/TSID17185/ONID235 na13°E/11039H, vyradený z fronty spotrebiteľských TV grafík ako profesionálny spravodajský prenos. Podklad: zhodný prijímačový scan, Satindex feed a oficiálny opis služby EBU. Nie je označený ako dátová služba.
- **0 nových TV piconov / 0 PNG / 0 ZIPov / 1 technická výnimka**. Pôvodná referencia, chýbajúce varianty a všetky archívy zachované.
- Zostáva **107 otvorených = 88 pôvodných + 19 delta**. Kandidát spolu **36 opravených referencií / 321 PNG / 99 jedinečných ZIPov**. Dávka03 spätne overená v `569c9c3e00b71bb3e84114e9c24af6f7e4c195e7`.
- Commit `c4afef5db19391f1fe273c7dab58d0d9f4a39ef4`; spätné načítanie všetkých štyroch zmenených dokumentov PASS, asset paths0. Dôkaz `reports/vhannibal-followup-20261106/scope-batch-20261108-04.json`. Žiadna zmena produkcie ani rádia.

### Dávka 03 – sedem presne identifikovaných AREF TV služieb – 8. 11. 2026

- **7 opravených TV referencií / 63 nových PNG / 9 ZIPov / 0 dátových výnimiek**. Zostáva **108 otvorených: 89 pôvodných + 19 delta**. PR spolu **36 opravených / 321 PNG / 99 jedinečných ZIPov**.
- SID913 Dream Türk, 914 Kanal D Turkey, 916 Show TV, 917 Show Max, 918 TRT1, 920 TRT Belgesel, 921 Kanal7 domestic. Všetky 52°E/10887H, TSID525/ONID115; pomenovaný servisný prehľad a nezávislý scan zhodných AV PID. Servisné názvy a referencie v pôvodnom registri zachované.
- Deväť variantov každej stanice je bajtovou kópiou existujúceho schváleného donora z42°E. Vizuálne skontrolované všetky tri pozadia. Kanal7 používa domáci donor CB20, nie AVRUPA/C579. TV8/SID912 ostáva pre rozdiel artworku otvorené.
- Lokálne PASS: SHA256/CRC, rozmery, alfa, presné PNG, 12 408 pôvodných členov a pôvodné ZIP prefixy zachované; všetkých18 CANAL+ archívov nezmenených. Validátor manifestu a test inštalačnej funkcie1.0.74 PASS. Bez testu fyzického prijímača.
- Základ `7923bfd4f8639d15b4705c9354da7b5ee2fcd14a`; Zor/NOW karanténa trvá. RADIO CLASSICA TV má pri čerstvom zdroji rozpor ONID/TSID, preto sa nevyraďuje podľa staršieho cache.
- Report `reports/vhannibal-followup-20261106/scope-batch-20261108-03.json`; payload commit `3c475292375b234d7db68055d344ebc38525486d`; spätné overenie PASS: 65 častí, 229 317 090 bajtov, 9 zostavených ZIPov zhodných bajt po bajte; manifest, SHA256SUMS a štyri registre tiež zhodné. Úplný dôkaz `scope-batch-20261108-03-remote-verification.json`. Bez produkčného merge, feedu, IPK a rádia.

### Dávka 02 – karanténa po zistení rozporu identity – 8. 11. 2026

- Pripravený Zor TV payload v `0ca6a3c1daa72f7a3edb278366f364eef5b597a4` **nie je dokončená dávka**. Dodatočný LyngSat záznam priraďuje presný SID900/TSID525/ONID115 stanici NOW od 16. 10. 2026 (PID2850/2950), kým Morpheus/KingOfSat uvádzajú Zor (PID208/308).
- Aktívny manifest, SHA256SUMS a registre obnovené presne na overený `d401bbb3ed78bc6b043c29568b26580402d2ac86`. Nové nemenné časti archívov ostávajú len historickým dôkazom, bez odkazu v aktívnom manifeste.
- **0 dokončených TV referencií / 0 aktívnych nových PNG / 0 aktívnych ZIPov; zostáva 115 (96 + 19).** PR spolu 29 referencií / 258 PNG / 99 ZIPov.
- Lokálny test integrity Zor balíkov prešiel, ale nepreukazuje identitu stanice. Pre tento prípad vyžadujeme aktuálny PMT/SDT alebo potvrdenie operátora; neprepisovať ho logom Zor ani NOW naslepo.
- Pokračovanie: jednotlivé služby 912–921, kde sa nezávisle zhodujú presné PID; osobitne doložené dátové služby. Bez zmien produkcie a rádia.

### Malá dávka 01 – BFBS dátové výnimky – 8. 11. 2026

- **115 otvorených: 96 pôvodných + 19 delta**, pred dávkou 117.
- BFBS 10°E: `1_0_16_1F53_1_10_640000_0_0_0` (16/SID8019) a `1_0_16_1F54_1_10_640000_0_0_0` (14/SID8020), TSID1/ONID16, doložené ako dátové služby mimo TV rozsahu. Zdroje a rozhodnutia: `reports/vhannibal-followup-20261106/scope-batch-20261108-01.json`.
- **2 dátové výnimky / 0 nových PNG / 0 ZIPov**. Celkový výsledok PR ostáva **29 opravených TV referencií / 258 PNG / 99 ZIPov**.
- Opravených aj šesť zastaraných boolean príznakov `remaining_current_technical` pri už dokončenej schválenej dávke. Ich artworky a rozhodnutia sa nemenia; nejde o nové opravy piconov.
- Zachovaných 120 riadkov, všetky pôvodné zoznamy chýbajúcich variantov a 19 delta holdov. DMDU_T, BFBS SID8016, Quadrille 75°E a ASSOCIATION MATERIEL zostávajú otvorené.
- Iba dokumentácia a register; produkcia, rádio a grafiky bez zmeny. Základ `6f5f7ebf8e51aa0faab7ae5ba9464f5b2f68c4f0`; **Spätné overenie PASS:** commit `6f2ddcd47862a2511f2b811f0a87ba11ba5306bc`, všetky 4 zmenené súbory načítané z GitHubu a obsahovo presne zhodné. Git blob SHA: register `78a02de2cb6457f44a08ad888ecc938071295569`, identity evidence `db1c3490a6a2ae3b3f2b55205aa47311132f03e5`, batch report `3645b8cdf3482dec7e92284cfec86f03280b1ffc`.

### Spätné overenie zachránenej dávky dokončené – 8. 11. 2026

- Balíkový commit: [`7d36ea4e7a8b92aabac5605a569224ae2769ec7c`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/commit/7d36ea4e7a8b92aabac5605a569224ae2769ec7c), rodič je pôvodný checkpoint `5dc376fcfd76a4f1255c93c5eac9e518ba79ae60`.
- **Vzdialený audit PASS:** 168 súborových ciest, 452 291 303 bajtov spätne načítaných z GitHubu; všetkých 18 ZIPov zostavených zo vzdialených častí, SHA256/CRC a 54 vložených PNG zhodné. Lokálne porovnanie pred/po potvrdilo 27 698 bitovo zachovaných pôvodných členov.
- Dôkaz uložený v commite `9b06440462cacdb833b53724fcae089d8672d524`: `reports/vhannibal-followup-20261106/remote-verification-20261108.json`, sekcia `recovery_approved_six_20261108`. Pôvodné overenia zostávajú zachované.
- PR #50: **29 opravených referencií / 258 pridaných PNG / 99 jedinečných zmenených ZIPov**; zostáva **117 technicky otvorených** (98 pôvodných + 19 nových). Schválené BloombergHT ×2, BETFRED TV1–3 a SIS Racing/SISSP už nečakajú na opakované schválenie. Bez ďalších SISSP aliasov.
- Inštalačná funkcia načítaná z produkčnej 1.0.74 je AST zhodná s otestovanou funkciou. Regresie publikácie PASS. GitHub nevrátil PR-triggered Actions beh pre balíkový commit; úspech CI sa netvrdí. Fyzický prijímač netestovaný.
- Zachránený dokončený prieskum 20 kandidátov / 11 584 existujúcich TV artworkov je v `recovered-donor-search-20261108.json`; žiadna podobnosť obrázka sa nepovýšila na identitu alebo schválenie. Čerstvé overenie Antena stále prinieslo konfliktné NID/TSID; tieto prípady zostávajú v karanténe.
- Ďalší krok: doložiť presný Antena tuple z nezávislého aktuálneho servisného zdroja, preveriť celé deviatky rovnakých edícií donorov, ponechať FUNBOX HD/UHD a chránené TV5MONDE oddelené. Pred prípadným merge preveriť aktuálny main a mesačný Kuukauden alias. Žiadny merge, produkčný feed, IPK, stabilný skin ani rádio neboli zmenené.


### Záchrana po páde Worku – 8. 11. 2026

Zachované lokálne výstupy approved-output boli nájdené a znova overené: 6 referencií / 54 PNG / 18 ZIPov; 27 698 pôvodných členov bitovo identických. Zdrojové PNG majú presné SHA256 a Git bloby checkpointu `5dc376fcfd76a4f1255c93c5eac9e518ba79ae60`. Schválenie vlastníka bolo dohľadané v rozhovore z 8.11.2026 10:14:51 UTC a týka sa presne BloombergHT HD ×2, BETFRED TV1–3 a SIS Racing/SISSP. Staršie označenie čakajúce na schválenie nižšie je historické. Bez ďalších SISSP aliasov.

Živý FullHDGlass main pri obnove: `63489718287327be969fa36e24dd384736776720`, produkcia 1.0.74. PiconHub main: `2b294878b14ca322fa277ba1e9781f83ec5649cf`. Staršie údaje 1.0.72 nižšie opisujú historické testy. Aktuálna záchrana mení iba existujúcu pracovnú vetvu PR #50. Spätný audit GitHubu bude zapísaný po uložení balíkov. Inštalačná funkcia produkcie 1.0.74 bola načítaná z aktuálneho main a jej AST sa zhoduje s otestovanou funkciou. Produkčné záznamy packages a parts manifestu sú zhodné s pôvodným základom; novší skin sa neprepisuje. Zachránený prieskum 20 kandidátov oproti 11 584 TV artworkom je v recovered-donor-search-20261108.json. Antena TSID má aj pri čerstvom vyhľadaní rozporné údaje, žiadny nový alias sa preto nevydáva za overený.

Opakované lokálne overenie SHA256, častí, CRC, 54 zdrojových PNG, 18 chránených CANAL+ archívov a historického inštalátora PASS; fyzický prijímač netestovaný.


**Aktualizované 8. 11. 2026.** Spoločný register pre pokračovanie v novom Worku. Tento Work rieši skin, PiconHub a satelitné picony vrátane Vhannibala. Rádiové picony a Warder Radio má na starosti samostatný Work. SHA nižšie sú overené východiská tejto inventúry. Pri ďalšej práci over živé vetvy, PR a vydania podľa [projektových pokynov](AGENTS.md).

### Schválených šesť grafík zapracovaných – 8. 11. 2026

Vlastník výslovne schválil pripravené BloombergHT HD (2 referencie), BETFRED TV1–3 a SIS Racing/SISSP. Do existujúcich 420E a 48E_A balíkov sa vložilo 54 PNG v 18 ZIPoch. Každý vstup má presný SHA256 z kontrolného prehľadu a Git blob zo schváleného checkpointu `5dc376f`; žiadne logo sa neprerobilo. Skratka SP sa nerozvíja a schválenie sa nevzťahuje na ďalšie aliasy.

27 698 pôvodných archívnych položiek zostalo bitovo identických. Časti/ZIPy SHA256, CRC, rozmery, alfa, referencie, zhoda schválených vstupov, manifest a skutočný inštalátor stabilného 1.0.72 s platným používateľským PNG prešli. Všetkých 18 CANAL+ SK/CZ archívov prešlo SHA256/CRC a zostalo nezmenených. Regresie publikácie PASS; fyzický prijímač netestovaný.

PR #50 má po tejto dávke 29 opravených referencií / 258 doplnených PNG / 99 jedinečných zmenených ZIPov. Zostáva 117 otvorených (98 pôvodných + 19 z nového zdrojového rozdielu). Produkčný main ostáva `12247acc20f699606f6d40f3783e4162b92674b9`; PiconHub main `8180aa0df6e185efad120338bc53ca04bc5e492a`. Žiadny merge, feed, skin, IPK ani rádio sa nemení. Pokračuje overovanie Antena TSID, FUNBOX a hľadanie donorov v celej existujúcej satelitnej a providerskej databáze.



### Overený koncový checkpoint satelitných piconov

Záverečné vzdialené overenie 8. 11. 2026: balíkový commit [`d5cbb323770fdbf9c67ed4b58c8a4290fade1740`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/commit/d5cbb323770fdbf9c67ed4b58c8a4290fade1740), strom `c16255a9b0d41b40f705935578e0a5643a866e96`. Overených **1 164 očakávaných ciest**; všetkých 20 nových súborov poslednej dávky (z toho 9 binárnych koncových častí ZIPov), spolu 4 685 517 bajtov, bolo z GitHubu stiahnutých a bitovo porovnaných. Predchádzajúca dávka `19809be` má overených 1 068 ciest a všetkých 103 nahraných súborov (15 188 989 bajtov). Súhrn je v `remote-verification-20261108.json → continuation_20261108`; staršie overenia zostávajú zachované.

**Finálny stav tohto behu: 17 nových opráv / 153 PNG / 63 jedinečných ZIPov. Celý PR #50: 23 opráv / 204 PNG / 99 ZIPov. Otvorených: 123 (104 pôvodných + 19 nových).** Šesť referencií čaká na konkrétne grafické schválenie v `ARTWORK_APPROVAL.md`; ostatné majú technické alebo identitné blokácie v existujúcich registroch. Štyri preukázané dátové služby nie sú vykázané ako opravené picony.

Kontrola živých vetiev po uložení: FullHDGlass main stále `12247acc20f699606f6d40f3783e4162b92674b9`, PiconHub main stále `8180aa0df6e185efad120338bc53ca04bc5e492a`. GitHub pre balíkový commit nevrátil žiadny PR-triggered Actions beh; úspech GitHub CI sa netvrdí. Lokálne regresie publikácie a izolované kontroly skutočného inštalátora prešli. Žiadny fyzický prijímač sa netestoval. Skin 1.0.72, aktualizátor, rádio a všetkých 18 CANAL+ SK/CZ balíkov zostali zachované. PR #50 zostáva nezlúčený.

**Presný ďalší krok:** schválenie uloženého prehľadu BloombergHT a SIS/Betfred; následne vložiť odsúhlasené deviatky do tej istej vetvy a overiť ich. Nezávisle doložiť Antena TSID 10 oproti 0 a zostávajúce nejasné identity. Pred produkčným merge znovu načítať main a preveriť mesačný Kuukauden alias. Zlúčenie, publikovanie a IPK vyžadujú samostatný súhlas. Tento pracovný beh je ukončený; po odovzdaní nepokračuje na pozadí.



## Najnovší overený výsledok – 8.11.2026, pokračovanie PR #50

- **Tento beh:17nových opravených referencií,153doplnených PNG,63jedinečných zmenených ZIPov. PR #50spolu:23referencií,204PNG,99ZIPov.** Žiadne zlúčenie ani publikácia.
- Pôvodný front120:9opravených,3doložené odchody,4dátové služby mimoTV,**104otvorených**. Rozdiel48nových zdrojových referencií:14opravenýchTV,1už úplne pokrytáTV,14rádiových mimo rozsahu bez úprav PNG,**19blokovanýchTV**. Spolu **123technicky otvorených**, nie pôvodných111: front sa rozšíril o nové dostupné zdroje.
- Známy zdrojový súbor14856:10460aktuálnychTV (10337má deväť platných variantov v kandidátovi,123otvorených),2722mimo rozsahu,5dátovaných odchodov,1669historických bez presnej aktuálnej zhody. Technické pokrytie nepotvrdzuje grafickú správnosť celého katalógu ani neuzatvára širší MASTER V9audit.
- Nový bezpečný donor z cieleného hľadania:SkySportsBoxOfficeHD, SID1035,TSID2024,ONID2,12168V. Už schválená rovnaká HDgrafika podTSID2003 má fyzicky všetkých9variantov. Doplnilo sa9bitových kópií do existujúcich282EZIPov, ktoré už boli v druhej dávke zmenené. Počet jedinečnýchZIPov sa preto nezvýšil. Všetky pôvodné členy aj predchádzajúce TNTdoplnenia sú zachované.
- Hotové balíkové commity: [`20aa8c6`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/commit/20aa8c68c8e9c4b55a6ce1a9a3d1b441d4d464c9) a [`19809be`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/commit/19809becb8fd8cde4abed18535994ed471b2318b). Oba sú vzdialene overené vrátane nahraných binárnych častí; ďalší checkpoint soSkyopravou je na tej istej vetvePR50. Presný finálnySHA je v PR a záverečnom overovacom zápise.
- Pri porovnaní63archívov pred týmto behom zostalo **126295pôvodných členov bitovo identických**. Dodatočný Skykrok zachoval aj17715členov priebežných282EZIPov; tento priebežný počet sa nepripočítava k jedinečným pôvodným členom. Všetkých18CANAL+SK/CZbalíkov je nezmenených.
- Kontroly:SHA256častí aarchívov,CRC,žiadne duplicitné členy,rozmery/alfa,zhoda sdonorom,zachovanie pôvodných členov,manifestový validátor PASS. Finálny inštalátor stabilného1.0.72 prešiel72inštalačnými prípadmi pre153novýchPNG,vrátane opakovaného282Eoverenia poSkyoprave; pri každom zachoval platný používateľskýPNG. Nie je to test fyzického prijímača. StavGitHubActions sa uvádza samostatne.
- [Grafiky na samostatné schválenie](ARTWORK_APPROVAL.md):45jedinečných kontrolnýchPNG pre6referencií –BloombergHT2,SISSP/SISRacing1,BetfredTV1–3. Sú mimoZIPov a stále medzi otvorenými. Bez schválenia sa nesmú vložiť.
- Blokácie nového rozdielu:7Antena sTSID10vs0;4technickéEutelsatnázvy;2číslované služby;2UNKNOWNRUSSIA;ELJUMHURIA aAL-KAFEL konfliktné artworky;STARZPLAYMovies a1TVIraq bez rovnakého schváleného donora. V pôvodnom fronte zostávajú nejasné/technické identity,pending grafiky,FUNBOXHD/UHD a2chránenéTV5MONDE; presný stav každej referencie je v existujúcich registroch.
- Ďalší krok:schváliť konkrétne grafiky zprehľadu,potom ich fyzicky vložiť do existujúcej vetvy aotestovať; nezávisle doložiť zostávajúce identity aAntenaTSID. Pred prípadným merge znovu overiť main amesačnýKuukaudenalias. Skin1.0.72,aktualizátor arádio sa nemenili. Produkčné zlúčenie,publikácia aIPK vyžadujú samostatný súhlas.



### Najnovší satelitný checkpoint –8.11.2026, PR50 bez produkčného merge

- Posledná skutočne uložená prvá dávka: [`20aa8c68c8e9c4b55a6ce1a9a3d1b441d4d464c9`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/commit/20aa8c68c8e9c4b55a6ce1a9a3d1b441d4d464c9). Jej556ciest a18nových binárnych častí boli vzdialene overené. Nová druhá dávka sa nachádza na tej istej vetve `work/vhannibal-mezzo-sd-20261106`; aktuálny presný HEAD over v [PR50](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/50).
- Tento beh:16nových fyzických opráv/144PNG/63ZIPov,126295pôvodných členov bitovo zachovaných. PR50celkom22referencií/195PNG/99ZIPov. Stabilný main `12247acc20f699606f6d40f3783e4162b92674b9` so skinom1.0.72 aaktualizátorom zachovaný. Žiadne zmeny18chránenýchCANAL+balíkov a žiadne úpravy rádia.
- Pôvodný front120:9opravených v kandidátovi,3odchody,4presne doložené dátové služby mimoTV,104otvorených. Nový8Nov rozdiel48:13TVopravených,1už pokrytáTV,14rádiových mimo práce,20ďalších blokovanýchTV. Spolu124technicky otvorených v známom zdrojovom súbore14856; nie je to schválenie všetkých grafík širšieho V9katalógu.
- AktuálnyMotor lamedb potvrdzuje101zo104otvorených pôvodných presných referencií;3neprítomné sa bez ďalších dôkazov nevyhlasujú za odchody. Nové7Antena tuple majú nevyriešený TSID10vs0. AL-KAFEL aEL JUMHURIA majú konfliktné podklady; nepreberajú sa podľa názvu. RTP TVInternacional je oficiálneRTP Mundo a dostalo existujúcu správnu schválenú grafiku. MesačnýKuukauden naTSID72 treba znovu preveriť pred merge.
- [Grafiky na samostatné schválenie](reports/vhannibal-followup-20261106/ARTWORK_APPROVAL.md):45jedinečných kontrolnýchPNG pre6referencií, všetky mimoZIPov. BloombergHT oficiálneSVG sú stále hashovo zhodné;36SIS/BetfredV9návrhov je obnovených bez zmeny pôvodných hashov. Žiadny REVIEW sa automaticky neschválil.
- Testy:63aktuálnych archívov/144PNG cez skutočnú inštalačnú funkciu1.0.72 s platným používateľskýmPNG sentinelom PASS; manifest,SHA256,CRC,rozmery a zachovanie starých členov PASS;18CANAL+SHA256/CRC PASS;regresie publikácie PASS. Hardvér netestovaný. Dôkazy a presné nové referencie sú v existujúcom `reports/vhannibal-followup-20261106`.
- Ďalší krok: schválenie konkrétnych návrhov v prehľade, potom ich zapracovanie na existujúcej vetve; nezávisle vyriešiť technické/identitné blokácie. Produkčné zlúčeniePR50,publikácia aIPK vyžadujú nový výslovný súhlas.



### 7. 11. 2026 – Channel Selection: dlhé EPG názvy a voliteľný Prime Time (pracovný kandidát, draft PR #51)

- [Draft PR #51](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/51), **nepripravený na merge**. Vetva: `work/channelselection-primetime-overlap-20261107`; základ `main fd0a57d56d04e03d5e4560d718595fa5aa28e255`. Bez produkčného merge a bez vydania IPK.
- Inventúra: 57 variantov `ChannelSelection-*` v `hdg17Screens.xml` + aktívny základný `ChannelSelection` v `skin.xml`. Všetkých 58 má `picServiceEventProgressbar`; len 23 variantov používa `g17ShowExtraEpg`. Samotný patch jedného EPG renderera teda nestačí.
- Prvý kandidát geometrie: vo všetkých 58 zoznamoch pridané `fieldMargins="26"`, bez úprav fontov, nastavení ich veľkosti, piconov, progressbarov alebo výšky riadkov. Automatický statický audit vrátil 58/58. **Nepovažovať za funkčne overené:** skutočné prekrývanie treba regresne overiť na Enigma2 pri dlhých názvoch, veľkom používateľskom fonte, stave označeného/neoznačeného riadku a v OpenATV/OpenPLi; ak medzera nestačí, opraviť natívne obmedzenie/prekreslenie textových buniek, nie zmenšovať font.
- Prime Time: doplnená **predvolene vypnutá** konfiguračná položka v menu výberu kanálov a samostatný používateľsky nastaviteľný čas s predvoleným 20:25. Doplnené izolované jadro `warderPrimeTime.py` a jednotkové testy pre EPG udalosť pokrývajúcu nasledujúci miestny čas (predvolený 20:25), nedostupné EPG a prechod na ďalší deň. **Zatiaľ nie je napojené na vizuálne zobrazenie Channel Selection**; zobrazenie podľa označenej stanice a kompatibilita všetkých relevantných variantov sú požiadavky na finálne overenie. Zistené typy EPG renderovania: 23× g17ShowExtraEpg, 21× g17ShowExtEpg, 9× g17EmptyEpg; 10 variantov nemá explicitný EPG renderer s týmto názvom. Nezapínať globálne.
- Regresné testy: `tools/test_warder_channelselection_layouts.py`, `tools/test_warder_epg_text_fit.py` a `tools/test_warder_primetime.py` sú uložené, avšak ešte nie sú spustené na Enigma2. `g17ShowExtraEpg.py` opravuje dlhé aj nezalomiteľné názvy meraním pixelov a nezasahuje do času; nový kandidátsky renderer `WarderPrimeTime.py` ešte nie je pripojený do obrazoviek. Statická kontrola: `tools/test_warder_channelselection_layouts.py` pokrýva všetkých 58 šablón. Statická kontrola dát z GitHubu prešla 58/58; jednotkové testy Prime Time a fyzický test zatiaľ nespustené.
- Regresná kontrola 7.11.: OpenATV CI odhalilo, že schválený `skin.xml` má byť bajtovo nedotknutý. Zdrojové XML obnovené na blob `a7ba9e5932fbb9c20e51cbdd0b45b75b97d1d9ed`; spoločná medzera je v 57 kandidátskych variantoch a pre aktívny základný skin sa pridáva až pri existujúcej generácii/runtime úprave `cChannelsel`. Pôvodný test nastavení vyžaduje poradie Type → Picon source → Date; Prime Time položky presunuté až za Date a chránené pri izolovaných testovacích mockoch. Oba problémy opravené na vetve; nové CI ešte treba potvrdiť.
- Konfigurácia Prime Time je teraz v `config.plugins.warderEvolutionPrimeTime` (mimo číslovaného starého registra `setupGlass17.par1..231`); `enabled=False`, `clock=[20,25]`. `saving()` explicitne ukladá a `exitNow()` ruší zmeny, aby sa nerozbila pôvodná záloha a nastavenia iných funkcií. Kandidátsky renderer číta túto sekciu. Kontroly OpenATV/OpenPLi a vlastný CI workflow pre syntaktické testy sú spustené; ich výsledky treba zaznamenať pred merge.
- Zobrazenie Prime Time je teraz pridané **iba v existujúcom EPG priestore** dvoch rendererov: `g17ShowExtraEpg` (24 vrátane základného variantu) a `g17ShowExtEpg` (21 variantov). Pri zapnutí používa jednu už existujúcu EPG riadkovú pozíciu a obmedzenie dĺžky podľa pixelov; pri vypnutí pôvodné zobrazovanie ostáva. **58 z 58 variantov má kandidátsku cestu na zobrazenie; posledných 13 používa vložený gate/renderer v pôvodnej EPG bunke.** Bez prijímačového testu to nie je potvrdená funkčnosť. Nie sú zmenené pozície piconov ani rozmery fontov.
- OpenATV po oprave schváleného `skin.xml` a poradia nastavení prešiel na vetvách 8.0 a master, ale 8.0-next stále hlásil nesúvisiaci historický test `test_original_positioner_buttons_reproduce_animation_failure`; odlíšiť od chyby Channel Selection. Testy aktuálneho posledného HEAD ešte prebiehajú.
- Systémový audit ďalších relevantných menu: [správa](reports/channelselection-primetime-audit-20261107.md). V zdrojových šablónach je 58 TV ChannelSelection, 10 EPGSelection, 4 MovieSelection, 3 EventView a 1 ChannelSelectionRadio; posledné štyri skupiny nemajú rovnaký natívny atribut `picServiceEventProgressbar` a vyžadujú samostatný regresný test, nie slepé pridanie `fieldMargins`.
- Pripravená kontrola `test_warder_primetime_settings.py` pre default OFF, zobrazenie nastaviteľného času, bezpečné uloženie/zrušenie a okamžité prekreslenie položky času pri zapnutí. Test zahrnutý v samostatnom GitHub Actions workflow. Zlyhanie posledného známeho OpenATV 8.0-next jobu bolo v historickom teste `test_original_positioner_buttons_reproduce_animation_failure`, nie v novom prekrývaní EPG; CI posledného HEAD stále nevyhodnotené.
- 7.11. doplnené všetkých 13 zostávajúcich variantov `ChannelSelection-1/2/3/4/6/8/9/10/11/12/13/14/18`: pôvodný widget s EPG textom dostal `WarderPrimeTimeGate`, ktorý pri zapnutom Prime Time potlačí starý text; nový `WarderPrimeTime` renderer používa tú istú plochu a je neviditeľný, keď je funkcia vypnutá. **Spolu 58/58 variantov má pracovnú integračnú cestu**, zatiaľ bez fyzického overenia vizuálneho výsledku. Variantu -12 bolo opravené počiatočné nesprávne umiestnenie; statický audit očakáva presné rozmery a pozície všetkých 13. Nový `tools/test_warder_primetime_placements.py` je pridaný do GitHub Actions. Pred produkciou treba otestovať aj opakovanie pri prepínaní staníc a nezávislé renderer zmeny.
- Úprava 7.11.: variant `ChannelSelection-14` používa pre nový Prime Time iba horný riadok `1395×45` v pôvodnom EPG poli, nie celých `1395×195`. Žiadny text neprekrýva ďalšie prvky mimo pôvodnej EPG oblasti. Presná pozícia je zachytená testom. Kandidátsky HEAD zodpovedá [draft PR #51](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/51); overovanie najnovších GitHub Actions a prijímačové UI testy zostávajú povinné.
- Následná kontrola: `g17EmptyEpg` pri prázdnom texte automaticky vykreslí fallback EPG hlásenie, preto pri Prime Time v `ChannelSelection-1/-2/-9` dostal presne označené `warderPrimeTimeGate="1"`. Len na týchto troch miestach vypne fallback aj prípadný textový animačný timer; bez aktívneho Prime Time sa pôvodné vykreslenie nemení. Statická kontrola v GitHube: 13/13 vložených PrimeTime polí zodpovedá pozícii presne jedného pôvodného gated EPG widgetu; 3/3 fallback widgety sú správne označené. Doplnila som automatické regresné kontroly a kompiláciu `g17EmptyEpg.py`; CI a fyzický prijímač zatiaľ nedokončili overenie.
- Ďalší krok: overiť aktuálnu kandidátsku integráciu Prime Time v 58 variantoch na skutočnom prijímači, opraviť prípadné chyby nájdené v CI a vyskúšať dlhé EPG názvy pri zväčšenom používateľskom fonte; samostatne overiť EPGSelection, MovieSelection, EventView a rádiový výber. Draft PR #51 nechaj bez produkčného merge, kým budú testy neúplné.


### 7. 11. 2026 – satelitné pokračovanie PR #50, uložený kandidát bez merge

- Overený živý FullHDGlass main `3ba80ef8bb3b0ccd4148666372a9bf851ee85947`, PiconHub main `8180aa0df6e185efad120338bc53ca04bc5e492a`. Existujúce novšie zmeny skinu sú zachované; rádio sa nemení. PR #47 zostáva publikovaný ako `fd0a57d`; PR #50 je nezlúčený a nepublikovaný.
- [PR #50](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/50) rozšírený na existujúcej vetve `work/vhannibal-mezzo-sd-20261106`: päť ďalších presne doložených opráv existujúcimi PNG (Eurosport 2, dva Dom Kino Premium, SPORSMART, Güneydoğu). 42 PNG v 27 ZIPoch, 34 131 nedotknutých členov bitovo zachovaných. Spolu s pôvodným Mezzo: 6 referencií / 51 PNG / 36 ZIPov. Predchádzajúci overený kandidát je `d1523e7`; presný nový HEAD je v PR a jeho commitoch, nie v sebeodkazujúcom texte commitu.
- Znova overených deväť Mezzo ZIPov a 18 chránených CANAL+ SK/CZ (SHA256, CRC); nové balíky prešli porovnaním pôvodných položiek, rozmermi, platnosťou manifestu a aktuálnou inštalačnou funkciou prijímača s neporušeným používateľským súborom. Žiadna nová/renderovaná grafika sa nepridáva.
- Front pôvodných 120: 6 opravených v kandidátovi, 3 doložené odchody presných referencií bez mazania historických PNG, 111 aktuálne blokovaných (10 z pôvodných REVIEW a 101 held). Fyzická neúplnosť pôvodného frontu je stále 114, z toho 3 odchody; odchody sa nepočítajú medzi opravy. Produkcia sa nemenila a tieto kandidátske počty nie sú publikované pokrytie.
- [Dôkazy a presné počty](reports/vhannibal-followup-20261106/identity-evidence-20261107.json), [balíkové testy](reports/vhannibal-followup-20261106/batch-20261107.json), [Mezzo a CANAL kontrola](reports/vhannibal-followup-20261106/mezzo-recheck-20261107.json), [existujúci register dôvodov](reports/vhannibal-followup-20261106/remaining-review.json). Dôkazy PR #48 prečítané a zachované; jeho stará vetva sa nepoužila na prepísanie novšej produkcie.
- Balíková dávka skutočne uložená ako [`5e3143a5581a1d5d952b6ca719069d72b7fdf172`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/commit/5e3143a5581a1d5d952b6ca719069d72b7fdf172). Overených 371/371 vzdialených ciest a 27/27 nových binárnych častí stiahnutých a bitovo zhodných; aktualizované dôkazy sú v `remote-verification-20261108.json`. Regresný test `tools/test-picon-publication-integrity.py` PASS.
- 8.11. pripravený [nový BloombergHT návrh](reports/vhannibal-followup-20261106/bloomberght-review/review.json): 9 PNG z oficiálnych čiernych/bielych SVG pre dve referencie, chránené farebné pixely a alfa, nemenné MASTER V9. **Čaká na schválenie grafiky, nie je v ZIPoch a neznižuje 111 otvorených.**
- Najbližšie: schválenie BloombergHT grafiky a následné vloženie do existujúcich 42E balíkov; nezávisle dôkaz mapovania SIS/Betfred, mesačnej identity Kuukauden a správneho FUNBOX HD. Produkčný merge PR #50 vyžaduje nový výslovný súhlas vlastníka.


### 8.11.2026 – pokračovanie po checkpoint a4e720d, SIS a mesačný alias

- Aktuálne main FullHDGlass `12247acc20f699606f6d40f3783e4162b92674b9`, PiconHub `8180aa0df6e185efad120338bc53ca04bc5e492a`. Stabilný skin1.0.72, aktualizátor a všetky novšie produkčné súbory zachované. PR50 stále bez produkčného merge.
- Pripravené tri ďalšie opravy existujúcimi schválenými PNG: SIS One, SIS Two, Kuukauden TSID72→presný stream Viasat Explore (prednostný CANAL+SK artwork). 27PNG/18ZIPov48E_A+08W;36338nedotknutých členov bitovo zachovaných;27variantov,CRC,SHA256,manifest,aktuálny inštalátor a publikácia-regresie PASS. Kuukauden je mesačný alias, pred merge znovu over aktuálny stream.
- PR50 spolu9opravených referencií/78PNG/54ZIPov; pôvodných120=9kandidátskych opráv+3odchody+4preukázané dátové služby+104otvorených. Produkcia nemá tieto kandidátske opravy. Chránených18CANAL+balíkov a rádio sa nemení. Presné dôvody v existujúcom `reports/vhannibal-followup-20261106/remaining-review.json`.
- SISSP/BF1–3 nie sú automatické aliasy starších schválených grafík: pripraviť samostatné schválenie už existujúcich V9návrhov. BloombergHT9PNG čaká na schválenie mimo ZIPov. FUNBOX HD originál je nesprávne UHD; dve TV5MONDE referencie zostávajú chránené.
- Nový pôvodný piconový zdroj8Nov má48referencií mimo registra14808. Tento deltafront je ďalšia samostatná kontrola; neuvádzať104ako úplný počet otvorených všetkých dostupných nových zdrojov. Pôvodný veľký reviewartifact2.2GB odmietnutý limitom512MB; prevzatá existujúca menšia časť319579614B rovnakým autorizovaným nástrojom.

## Overené vetvy

| Repozitár a vetva | Posledný overený commit | Stav |
| --- | --- | --- |
| FullHDGlass-Warder-Evolution · `main` | [`5966de55871c1fd3ab912885ab102a0a100b853e`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/commit/5966de55871c1fd3ab912885ab102a0a100b853e) | [PR #43](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/43) zaviedol spoločný register a pokyny pre nový Work. Posledný doložený stabilný IPK je [1.0.69](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/v1.0.69). |
| PiconHub-Warder-Evolution · `main` | [`e90a1fe3a2734b555f48f343284f9103530180fb`](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/commit/e90a1fe3a2734b555f48f343284f9103530180fb) | Verejné overenie selektorov cez [PR #63](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/pull/63). Posledný doložený stabilný IPK je [0.1.44](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/releases/tag/v0.1.44). |
| PiconHub-Warder-Evolution · `warder-master-production` | [`a740b6da429b8d93eb0f3123158d81b8724f9d19`](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/commit/a740b6da429b8d93eb0f3123158d81b8724f9d19) | Overený HEAD samostatnej produkčnej vetvy. |
| Warder Radio a GSU | Posledné doložené verzie v odovzdávke sú 0.1.8 a 13.41-r4. | Pred samostatnou úlohou over aktuálne vydanie a SHA príslušného repozitára. |

## Stav podľa oblastí

| Oblasť | Dokončené, rozpracované a najbližší krok |
| --- | --- |
| Satelitné picony a Vhannibal | **Publikované v živom katalógu.** [PR #40](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/40), [#41](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/41) a [#42](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/42) sú zlúčené. Celkom 12 508 prijatých servisných referencií, 193 evidovaných výnimiek. RADIO CLASSICA TV zostáva výnimkou. [Živý manifest](assets/warder/downloads/picons/channels/manifest.json) mal pri overení 498 ZIPov a 1 804 častí. Ďalší audit rob podľa aktuálneho manifestu cez všetky pokryté pozície a porovnávaj nové stanice, presuny, aliasy a zmeny grafík so skutočnými balíkmi. |
| MASTER V9 a CANAL+ | **Schválené podklady sú chránené.** Zachovaj [MASTER V9 šablóny](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/tree/main/plugin/artwork/templates/picons), kanonické CANAL+ SK/CZ grafiky a plné referencie. Pred tvorbou hľadaj existujúcu schválenú grafiku a alias. Požadované varianty sú Transparent, White a Black pri 50×30, 220×132 a 400×240. |
| Rádiové picony | **Publikované SK/CZ r6** podľa odovzdávky pokrýva 320 staníc a 358 referencií. [Svetový checkpoint](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/blob/4dd8220efc5180db9e0fca56335b4a01b9193558/migration/radio-reconciled-checkpoint-20261105/summary.json) eviduje 19 756 pripravených a 21 197 nepokrytých referencií. Je rozpracovaný. Pokračuj z [auditu krajín](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/blob/main/reports/radio-country-quality-20261105.json), [redakčného registra #41](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/issues/41) a [otvorených PR](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/pulls) #42, #44, #49, #50, #51, #53, #54 a #59. Blokované identity v odovzdávke zahŕňajú Kossuth, Radio 88 Retro / REPLAY a regionálne ESKA 2. Najprv porovnaj kandidátov s aktuálnou produkciou a over ich identitu a zdroje. |
| FullHDGlass a Radio Mode | **Otvorené.** Pokračuj v audite dynamických obrazoviek a rozložení, natívnych rozhraní OpenATV/OpenPLi a v overovaní na fyzických prijímačoch vrátane GLES/WQHD. Historický [PR #1](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/1) bol pri inventúre otvorený. Zosúladenie vyhľadávania obalov v Radio Mode so samostatným Warder Radio je v [NEXT-RELEASE.md](NEXT-RELEASE.md). |
| PiconHub plugin | **Otvorené.** Over návrhy univerzálneho rádia pre TV a rádio, stiahnutia jedného piconu a prvého prechodu z Chocholousek. Východiská sú [#10](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/issues/10), [#19](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/issues/19) a [plán vydania](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/blob/main/NEXT-RELEASE.md). |
| GSU a Trezor | GSU je súčasťou [spoločného stabilného vydania](docs/COMMON-STABLE-20261102.md). [Trezor](https://github.com/Evolution-by-Warder/Trezor) uchováva zdrojové archívy a checkpointy. Pri práci s jeho podkladmi vychádzaj z presného SHA uvedeného v príslušnom produkčnom manifeste alebo reporte. |

## Denník významných zmien

### 6. 11. 2026 – produkčné zlúčenie Vhannibal #47 a prvá ďalšia oprava

- [PR #47](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/47) po schválení zlúčený do `main` ako [`fd0a57d`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/commit/fd0a57d56d04e03d5e4560d718595fa5aa28e255). Znovu overených 69 ZIPov, 127 934 nesúvisiacich položiek a bitová zhoda všetkých 18 CANAL+ SK/CZ balíkov. Produkčný strom, manifest a `SHA256SUMS` sa zhodujú s overeným kandidátom. Produkcia má 10 313 z 10 433 aktuálnych TV referencií s deviatimi platnými variantmi.
- [Samostatná dávka Mezzo SD](reports/vhannibal-followup-20261106/README.md) pridáva jednu presnú referenciu do deviatich balíkov 13°E bez zmeny existujúcich PNG. Po prípadnom schválení dávky bude technicky otvorených 119 referencií. Rádiové picony a chránené CANAL+ SK/CZ zostávajú mimo dávky.
- Z pôvodných 120 otvorených referencií malo v už vytvorenej revízii MASTER V9 stav REVIEW 17 a pozastavených bolo 103. Ďalší krok je nezávisle overiť konkrétne identity a platné existujúce grafiky. Bez schválenia sa nenasadzuje nová grafika ani ďalšia dávka.

### 6. 11. 2026 – spoločný kandidát Vhannibal #47 a #49

- [Spoločný výsledok](reports/vhannibal-completeness-20261106/CURRENT.md) používa overené balíky z oboch vetiev. Karavan TV je bitovo totožný, Quest Red preberá pixelovo doloženú sadu #47 a Viasat Kino dopĺňa #49. Telesur English a Daystar na 11067.5 V zostávajú zdokumentované ako dva odchody.
- Opravených je 25 rôznych referencií v 69 ZIPoch. Po kandidátovi má 10 313 z 10 433 aktuálnych satelitných TV referencií všetkých deväť platných variantov. Zostáva 118 neúplných a dva chránené prázdne TV5MONDE. Grafický audit V9 zostáva samostatný.
- Stav častí, SHA256, prípady prekryvu a testy sú v spoločnom reporte. Zlúčenie a produkčná publikácia čakajú na schválenie.

### 6. 11. 2026 – prevzatie satelitného auditu po Vhannibalovi

- Po schválení je [PR #43](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/43) zlúčený. `AGENTS.md` aj `WARDER_PROGRESS.md` na `main` boli overené voči schváleným verziám.
- Overený verejný [manifest](assets/warder/downloads/picons/channels/manifest.json) a jeho SHA256. Všetkých 1 804 deklarovaných častí má záznam v `SHA256SUMS` a súbor v Git strome. Katalóg obsahuje 498 ZIPov, 56 selektorov a 166 kombinácií selektora a rozmeru, každú s troma pozadiami. Táto kontrola overila úplnosť katalógu a evidencie častí. Fyzické testy ZIPov sú zaznamenané pri PR #42 nižšie.
- Z pripnutého vstupu bol znova zostavený `plans.json`. Overených 12 508 unikátnych plných referencií, všetkých 12 503 pôvodných referencií zachovaných, päť pridaných a jeden záznam CHC-HD aktualizovaný. Živý manifest eviduje 193 výnimiek.
- Otvorený [PiconHub #30](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/issues/30) obsahuje historické porovnanie 3 388 kandidátov podľa názvov súborov a vtedajších bouquetov. Na novú dávku použi živý katalóg po zlúčení #40–#42. Starý počet nevyjadruje aktuálne chýbajúce stanice. Najbližší krok je porovnať nové alebo zmenené služby s presnými referenciami a grafikami v živých ZIPoch a prehodnocovať výnimky len s novým dôkazom.

### 6. 11. 2026 – Vhannibal PR #42 v produkcii

- Po výslovnom súhlase vlastníka zlúčený do FullHDGlass `main` ako [`2079d56`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/commit/2079d56bb8f3337d2196d055ea3938952dc91077). Pribudlo päť servisných referencií a oprava CHC-HD pod pôvodnou referenciou. Zmenilo sa 39 ZIPov. Všetkých 18 CANAL+ SK/CZ ZIPov zostalo bitovo identických.
- [Commit `7f87346`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/commit/7f87346c96879080dbbb15af677110c6d8cfc419) pridal reprodukovateľné zosúladenie registra. Na čistom checkoute vytvor aktuálny výstup príkazom `python tools/materialize-vhannibal-plans.py /tmp/plans.json`. Zdrojové rozhodnutia a dôkazy sú v [reporte PR](reports/vhannibal-six-resolutions-20261105).
- Pred zlúčením prešli SHA256 a CRC všetkých 39 zmenených ZIPov, všetkých deväť variantov pre šesť dotknutých referencií a test inštalácie cez kód prijímača. [OpenATV](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/42193202113) a [OpenPLi](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/42193202090) prešli spolu v šiestich úlohách. Po zlúčení sa verejný manifest a `SHA256SUMS` zhodovali s otestovaným kandidátom a SHA256 novej časti sedel pre každý z 39 ZIPov. Najbližší krok pre satelity je audit nových zmien oproti tejto produkcii.


### 6. 11. 2026 – rozšírený finálny audit Vhannibala, PR #47 (bez produkčného merge)

- Auditný základ FullHDGlass `603218ea8fa51176f686f14f303509a4c64dc7e1`; PiconHub main `e90a1fe3a2734b555f48f343284f9103530180fb`, produkčná vetva `a740b6da429b8d93eb0f3123158d81b8724f9d19`, Trezor `342e111a9b4adff06121c317d04ba2cfe4f82595`, GSU `c3978f69303de59391c1ff43b2563592526e97e2`. Stabilné vydania zostávajú 1.0.69 / 0.1.44 / 13.41-r4.
- [Pracovná vetva a draft PR #47](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/47) obsahujú [úplný report](reports/vhannibal-completeness-20261106/README.md) a register 14 808 referencií. Skontrolovaných je 27 oficiálnych downloadov (jedna piconová sada + 26 sád nastavení), originály z 3. novembra a celé historické importné registre. Pôvodné septembrové a októbrové ZIPy neboli získané; ich pixely nie sú označené za skontrolované.
- Fyzicky overených je všetkých 498 produkčných ZIPov, 1 804 častí a 400 476 PNG. Pre 10 435 aktuálnych TV referencií malo deväť platných neprázdnych variantov 10 293, pri 138 chýbal variant a pri štyroch bol PNG prázdny. Mimo TV rozsahu je oprávnene 2 704 referencií; 1 669 historických / bez presnej aktuálnej zhody sa neoznačuje automaticky za zaniknuté.
- **Vhannibal nemožno označiť za kompletne spracovaný podľa MASTER V9.** Pripravená oprava 26 rôznych referencií v 69 ZIPoch obsahuje 186 doplnených a 12 opravených PNG záznamov (198 spolu). Po nej má 10 315 aktuálnych TV referencií deväť platných PNG, pri 118 stále chýba variant a dva TV5MONDE prípady majú prázdny kanonický Transparent. Všetkých 18 schválených CANAL+ balíkov je bitovo zachovaných.
- Nové V9 návrhy majú [úspešné zostavenie](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/42206982364): 5 485 grafík, 49 365 PNG, 8 962 referencií. QC PASS má 125 referencií; 8 837 má REVIEW, ďalších 1 428 je pozastavených. Tieto počty nie sú schválením grafík. Osem konkrétnych konfliktov identity je evidovaných samostatne bez vymyslených log.
- Kandidát prešiel produkčným validátorom a skutočnou inštalačnou metódou prijímača na 69 archívoch / 198 PNG; kontrolované boli SHA256, CRC, plné referencie, rozmery a zachovanie nesúvisiacich používateľských súborov. Nové grafiky, merge aj publikovanie stále čakajú na schválenie. Warder Radio a rádiové picony sa nemenili.
- Ďalší krok: revízia uložených V9 hárkov, explicitných konfliktov a kanonického TV5MONDE; až potom vlastníkom schválený produkčný merge. Zdrojový checkpoint je zachovaný súkromne aj pre opakovanie po zmene upstreamu.

### Historický ďalší krok po dávke04

- 107 zostávajúcich prípadov ostáva blokovaných dôkazom identity, schváleným donorom alebo presnou klasifikáciou. Nové zistenia uložené v `identity-evidence-20261107.json` → `continuation_20261108.followup_after_batch03` a v príslušných riadkoch `remaining-review.json`.
- Priorita: schválený domáci TV8 Turkey donor; overenie konfliktu SID900 Zor/NOW; aktuálna transportná tabuľka Antena TSID10/0. Neopakovať dávky03/04 ani uzavretú záchranu šiestich schválených referencií. TV5MONDE a18 CANAL+ balíkov chránené. Nové artworky vyžadujú schválenie.


### Pokračovanie po dávke05 – uložený prieskum, nie ďalšie opravy

- Zostáva **106 otvorených (87 pôvodných + 19 delta)**. Nové dôkazy pre 40 referencií sú v `identity-evidence-20261107.json` → `continuation_20261108.followup_after_batch05`; príslušné riadky registrov aktualizované. Žiadna ďalšia referencia sa tým neuzatvára.
- TV8: oficiálny pôvodný PNG 91×80 uložený v reporte ako **neschválený výskumný podklad**, mimo inštalačných balíkov. Cielené porovnanie nového cieľa s 11 584 už uloženými grafikami nenašlo prijateľného donora medzi vizuálne overenými 24 výsledkami; nejde o dôkaz neexistencie donora. Súbor `tv8-focused-donor-search-20261108.json` uchováva referencie a SHA256.
- SES Demo na66°E má už presnejší identifikačný podklad; potrebuje schváleného donora rovnakej edície. Dve45°E referencie majú ONID1/0 konflikt. DSNS historické testy nepreukazujú aktuálnu dátovú klasifikáciu. BFBS oficiálny zoznam čísel kanálov nie je tabuľka SID; Quadrille57°E nemožno preniesť na75°E.
- UNKNOWN RUSSIA sa podľa čerstvých záznamov7.11. vrátila; staršie oznámenie o odchode nepoužiť na vyradenie. AntenaTSID10/0, Zor/NOW, TV5MONDE a ďalšie blokácie ostávajú chránené.
- Ďalší konkrétny krok: získať schválený domáci TV8 alebo SES Demo HD donor; presnú aktuálnu transportnú tabuľku Antena a BFBS75°E. Nové grafiky pripraviť oddelene na schválenie, žiadne domyslené aliasy. Produkčný merge nie je povolený.

- Následná kontrola RADIO CLASSICA TV9°E: čerstvý KingOfSat má ONID0/TSID516, Morpheus ONID29/TSID516. Sporný ONID pretrváva; neuzavreté. SHA256 oboch čerstvých stránok uložené v registri. Zostáva105.

