> **Stav po zosúladení #47 a #49 je v [spoločnom výsledku](CURRENT.md).** Čísla nižšie opisujú historický kandidát #47 a slúžia ako pôvodný auditný dôkaz.

# Vhannibal – finálny audit úplnosti, 6. 11. 2026

**Výsledok: Vhannibal nie je úplne spracovaný.** Úplnosť názvov v starom registri nepreukazovala všetky pôvodné sady, všetky referencie ani grafickú zhodu s MASTER V9. Toto je negatívny výsledok auditu, nie certifikát správnosti všetkých log.

## Rozsah a presné počty

Skontrolovaný inventár má **14 808 unikátnych plných referencií**. Zahŕňa 14 104 platných názvov z originálov 3. a 5. novembra, ďalšie historicky evidované referencie a služby zo všetkých 26 aktuálne ponúkaných sád nastavení. Zachované sú celé namespace vrátane nízkych bitov. Autoritatívne počty a jeden riadok pre každú referenciu sú v `summary.json`, `reference-ledger.json.gz` a `reference-ledger.csv.gz`.

| Kategória | Počet |
| --- | ---: |
| Aktuálne satelitné TV referencie v zjednotení všetkých oficiálnych sád | 10 435 |
| Rádiové referencie mimo rozsahu | 2 237 |
| Nesatelitné referencie mimo rozsahu | 367 |
| Dátové alebo neurčené služby typu 0/3/0xC mimo TV rozsahu | 100 |
| Spolu oprávnene vynechané mimo TV rozsahu | **2 704** |
| Historické / bez presnej zhody v aktuálnych nastaveniach | 1 669 |

Posledná skupina sa **neoznačuje automaticky za zaniknutú**. Obsahuje aj staré typové aliasy; ich dôkazy a existujúce súbory sú zachované. Štyri chybne pomenované PNG v novom origináli sú karantenizované osobitne a nepočítajú sa ako platné referencie.

| Pokrytie 10 435 TV referencií | Produkčný základ | Kandidát v tomto PR |
| --- | ---: | ---: |
| Všetkých 9 PNG prítomných, dekódovateľných, správne rozmery a neprázdne alfa | 10 293 | **10 315** |
| Chýba aspoň jeden variant | 138 | **118** |
| Prítomný prázdny PNG | 4 | **2** |

Tieto počty nevyjadrujú potvrdenie identity loga, jeho aktuálnosti, kontrastu ani úplnú grafickú zhodu s V9. Zjednotenie metadát obsahuje 40 orbitálnych pozícií a 631 rôznych providerových označení vrátane prázdneho. Produkčný katalóg bol skontrolovaný celý: 49 orbitálnych selektorov, šesť satelitných providerových selektorov a pôvodný DTT selektor; DTT sa nemení. Rozpis je v `by-orbital-position.json` a `by-provider.json`.

## Opravy na pracovnej vetve

**26 rôznych referencií, 69 ZIPov a 198 PNG záznamov:** 19 skutočne chýbajúcich plných referencií doplnených v deviatich variantoch; jedna čiastočná referencia doplnená v šiestich chýbajúcich variantoch; šesť existujúcich referencií Sky Adventure vrátane štyroch starších typových aliasov má opravených 12 prázdnych derivátov. Ďalších deväť záznamov rozširuje existujúci Skylink roster o overenú novú RTL GOLD referenciu. Spolu pribudlo 186 PNG záznamov a 12 bolo nahradených. Aktuálnych TV identít sa zlepšilo 22; ďalšie štyri sú zachované staré aliasy.

Nové referencie: RTL GOLD., Telesur English, Daystar, dva CANAL+ EXTRA 2, Boyles, Eco TV, MILADY TV, Natali TV, Provence TV, KARAVAN TV, dva CANAL+ DOKUMENT HD, dva CANAL+ SERIALE HD, Quest Red, Food Network, AL AHAD VOICE a Alsharqiya TV HD. TELE CONGO HD dopĺňa iba chýbajúce veľkosti. Každé prevzatie má plnú referenciu, zdrojovú identitu, lamedb dôkaz, pôvodnú grafiku alebo pixelovú zhodu a deväť kontrolných súčtov. Posledné tri sú overené typové aliasy v regionálnych sadách, nie odhady odvodené iba z namespace.

Grafiky sa pre tieto opravy nekreslili. Opätovne sa používajú existujúce PNG. Nová RTL GOLD používa kanonické schválené CANAL+ bajty. Všetkých **18 CANAL+ SK/CZ balíkov zostáva bitovo identických**, aj pôvodný DTT a všetky rádiové referencie. Existujúce súbory mimo uvedených 12 prázdnych derivátov sú v zmenených archívoch zachované po bajtoch. Tieto opravy dopĺňajú pokrytie; prevzaté staršie grafiky tým automaticky nezískavajú potvrdenie V9.

Dva aktuálne TV5MONDE prípady zostávajú blokované: kanonický 220×132 Transparent je prázdny aj v chránených CANAL+ balíkoch. Ich náhrada by menila schválený podklad, preto sa bez novej grafickej revízie neprepisuje.

## MASTER V9 a identity

Presné SHA256 oboch MASTERov a zmrazeného renderera sú overené. Porovnanie vonkajšieho okraja našlo odchýlku pri 10 183 aktuálnych TV referenciách aspoň v jednom ich orbitálnom balíku. Ide o presný pixelový test okraja, nie o automatický rozsudok, že všetky tieto logá sú nesprávne. Vizuálna vzorka potvrdila aj staršie Chocholousek rámy medzi V9 grafikami.

Z presných pôvodných PNG bolo vytvorených **5 485 grafických návrhov, 49 365 PNG pre 8 962 referencií**. Kontrolou zmrazeného renderera prešlo 55 grafických skupín / 125 referencií. **5 430 skupín / 8 837 referencií má REVIEW**; neboli povýšené na PASS. Ďalších 1 428 referencií zostalo pozastavených z dôvodov uvedených v indexe. Ani PASS sa nepovažuje za súhlas vlastníka s novou grafikou.

[Úspešné zostavenie a kompletné kontrolné hárky](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/42206982364) obsahujú návrhy iba na revíziu. Index, súhrn a prvý hárok sú uložené priamo na vetve; celý artefakt má platnosť do 4. 2. 2027. Originály aktuálnych 27 downloadov sú navyše zachované v súkromnom checkpointe vlastníka `Vhannibal-originals-20261105-audit-checkpoint.zip` (SHA256 `a81330ba86a56d108af334d40a05e1e3db6cb034e2337b15ef3c8f2448e2b408`), takže sa návrhy dajú znovu zostaviť aj po zmene upstream downloadu.

Samostatne sú evidované **osem konkrétnych konfliktov**: Eurosport 2 s grafikou Eurosport 1; dve BLOOMBERGHT referencie s inou Bloomberg edíciou; SPORSMART s grafikou SPORSMART 2; dve Dom Kino Premium referencie bez PREMIUM v originálnej grafike; Dijlah a ALMAWQEF s technickým obrazcom. Ani pixelová zhoda s nesprávnym programom neoprávňuje kopírovať logo. Podrobnosti sú v `identity-conflicts.json`. Ich V9 náhľady sú odmietnuté z hľadiska identity bez ohľadu na kontrastnú klasifikáciu.

## Overenie a pokračovanie

- Vstup: všetkých 1 804 častí zodpovedá manifestu aj SHA256SUMS; všetkých 498 ZIPov má platné CRC. Dekódovaných je všetkých 400 476 PNG. Rozmery sú kontrolované po jednotlivých súboroch; nájdených je 21 prázdnych alfa záznamov v rôznych aliasoch a balíkoch.
- Opravy: SHA256 všetkých častí a ZIPov, CRC, duplicity, názvy, všetky varianty a zachovanie ostatných PNG overené. Po rozdelení na kanonické časti prešiel produkčný validátor manifestu.
- Skutočná inštalačná metóda prijímača z pripnutého zdroja prešla na všetkých 69 zmenených archívoch a 198 upravených PNG; nesúvisiaci používateľský súbor zostal pri každej skúške zachovaný. Nie je to RF ani hardvérový test prijímača.
- Nezískané historické originály zo septembra/októbra a nejasné identity sú výslovne oddelené od skontrolovaných obrazových bajtov. Neexistuje tvrdenie, že bola vizuálne potvrdená správnosť všetkých historických log.

**Produkcia sa nezlúčila a nevydal sa žiadny balík ani IPK.** [PR #47](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/47) je draft. Ďalší vykonateľný krok je posúdiť konkrétne V9 návrhy a identity, osobitne kanonický TV5MONDE. Produkčný merge vyžaduje výslovné schválenie vlastníka. Warder Radio ani jeho rádiové picony neboli upravené.

Všetky zdroje a dostupnostné obmedzenia: [SOURCES.md](SOURCES.md). Strojový register: [summary.json](summary.json), [reference-ledger.csv.gz](reference-ledger.csv.gz). Pôvodné míľniky zostávajú v koreňovom WARDER_PROGRESS.md.
