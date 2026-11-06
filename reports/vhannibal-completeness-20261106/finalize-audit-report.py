from pathlib import Path
import json,gzip,hashlib,collections,csv,io,zipfile
O=Path('audit-output');B=O/'approved-repairs';R=O/'final';R.mkdir(exist_ok=True)
rows=json.loads(gzip.decompress((O/'joined-reference-ledger.json.gz').read_bytes()));proof=json.load(open(B/'approved-reuse-repairs.json'));fixed={x['reference']:x for x in proof['references']};frames=json.loads(gzip.decompress((O/'current-frame-deviations.json.gz').read_bytes()));counts=collections.Counter();tvbefore=collections.Counter();tvafter=collections.Counter()
for x in rows:
 x['scope_category']='CURRENT_TV'if x['current_satellite_nonradio']and int(x['reference'].split('_')[2],16)not in(0,3,12)else'CURRENT_DATA_OR_UNSPECIFIED_SERVICE'if x['current_satellite_nonradio']else x['scope'];x['status_after_candidate']=x['status'];x['repaired_on_working_branch']=x['reference']in fixed;x['v9_deviation_slots_before']=frames.get(x['reference'],[])
 if x['repaired_on_working_branch']and x['current_satellite_nonradio']:x['status_after_candidate']='COVERED_9_VALID'
 if x['scope_category']=='CURRENT_TV':tvbefore[x['status']]+=1;tvafter[x['status_after_candidate']]+=1
 counts[x['scope_category']]+=1
raw=gzip.compress(json.dumps(rows,separators=(',',':')).encode(),mtime=0);(R/'reference-ledger.json.gz').write_bytes(raw)
fields=['reference','name','provider','position','selector','scope_category','status','status_after_candidate','repaired_on_working_branch','present_slots','missing_slots','bad_slots','v9_deviation_slots_before','current_settings_source'];stream=io.StringIO();w=csv.DictWriter(stream,fieldnames=fields,extrasaction='ignore');w.writeheader()
for x in rows:w.writerow({k:json.dumps(x.get(k),ensure_ascii=False)if isinstance(x.get(k),list)else x.get(k)for k in fields})
(R/'reference-ledger.csv.gz').write_bytes(gzip.compress(stream.getvalue().encode('utf-8-sig'),mtime=0))
ps=json.load(open(O/'package-summary.json'));assert len(ps)==498;source=json.load(open(O/'sources.json'));v9=json.load(open(O/'v9-review-summary.json'))if(O/'v9-review-summary.json').exists()else json.loads(gzip.decompress((O/'v9-review-index.json.gz').read_bytes()))['summary'];checks=json.load(open(B/'receiver-checks.json'))
summary={'audit_date':'2026-11-06','conclusion':'VHANNIBAL_NOT_COMPLETE_NO_FULL_GRAPHIC_COMPLIANCE_CERTIFICATE','production_base_sha':'603218ea8fa51176f686f14f303509a4c64dc7e1','production_manifest_sha256':hashlib.sha256(Path('manifest.json').read_bytes()).hexdigest(),'candidate_manifest_sha256':hashlib.sha256((B/'manifest.json').read_bytes()).hexdigest(),'audited_reference_union':len(rows),'reference_scope_counts':dict(counts),'current_tv_references':sum(tvbefore.values()),'tv_coverage_before':dict(tvbefore),'tv_coverage_after_working_candidate':dict(tvafter),'justified_out_of_scope_references':counts['RADIO_OUT_OF_SCOPE']+counts['NON_SATELLITE']+counts['CURRENT_DATA_OR_UNSPECIFIED_SERVICE'],'historical_or_no_exact_current_match_references':counts['NO_CURRENT_SETTINGS_EVIDENCE']+counts['HISTORICAL_REPORT_ONLY'],'official_downloads_checked':27,'official_settings_sets_checked':26,'archive_files_physically_checked':len(source),'distinct_current_and_nov3_picon_reference_names':14104,'latest_picon_items':14088,'latest_valid_picon_reference_names':14084,'invalid_latest_png_filenames_quarantined':4,'production_packages_verified':len(ps),'production_parts_verified':1804,'production_pngs_decoded':sum(x['png_count']for x in ps),'empty_production_png_entries':sum(len(x['issues'])for x in ps),'repairs':proof['summary'],'current_tv_references_with_exact_outer_edge_deviation':sum(x['scope_category']=='CURRENT_TV'and bool(x['v9_deviation_slots_before'])for x in rows),'v9_review':v9,'receiver_validation':{k:v for k,v in checks.items()if k!='checks'},'source_checkpoint_sha256':'a81330ba86a56d108af334d40a05e1e3db6cb034e2337b15ef3c8f2448e2b408','canonical_canal_packages_preserved':18,'warder_radio_changes':0,'publication_status':'DRAFT_PR_47_ONLY_AWAITING_OWNER_APPROVAL'}
assert summary['audited_reference_union']==14808 and summary['current_tv_references']==10435 and summary['justified_out_of_scope_references']==2704
assert tvafter=={'COVERED_9_VALID':10315,'MISSING_VARIANTS':118,'EMPTY_OR_INVALID_PNG':2}
(R/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
# Human-readable exact archive list, keeping upstream settings themselves private.
lines=['# Skontrolované zdroje','', 'Kontrola k 6. 11. 2026: 27 oficiálnych downloadov (1 piconová sada a 26 sád nastavení), plus štyri pôvodné novembrové súbory vlastníka. Dvojice novembrových kópií majú zhodné SHA256. Žiadne pôvodné nastavenia sa v tomto PR nezverejňujú.','', '| Zdroj | Názov archívu / obsah | SHA256 |','| --- | --- | --- |']
for src in source:
 name=src['source'];label=src['lamedbs'][0]['member'].rsplit('/',1)[0]if src['lamedbs']else'PICON Vhannibal Motor 05 nov 2026'if name=='official-1.zip'else'PICON Vhannibal Motor 03 nov 2026'
 link=f"[id {name[9:-4]}](https://www.vhannibal.net/download_setting.php?action=download&id={name[9:-4]})"if name.startswith('official-')else name
 lines.append(f"| {link} | {label} | `{src['sha256']}` |")
lines+=['','Ďalej boli porovnané všetky riadky troch historických importných registrov v PiconHub: pôvodný import (13 903), Motor 13 (13 903) a Motor 18 October (14 041). Pôvodné septembrové a októbrové ZIPy sa nepodarilo získať; ich evidované referencie sú zahrnuté, ale ich obrazové pixely nemožno označiť za nanovo skontrolované. Dve presné vyhľadávania názvov týchto archívov nepriniesli dostupný download.','', 'Produkčné balíky: všetkých 498 ZIPov z pripnutého manifestu; kontrolované boli skutočné bajty všetkých 1 804 častí, SHA256, ZIP CRC a rozmery každého zo 400 476 PNG.']
(R/'SOURCES.md').write_text('\n'.join(lines)+'\n')
readme='''# Vhannibal – finálny audit úplnosti, 6. 11. 2026

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
'''
(R/'README.md').write_text(readme)
progress=Path('fullhd/WARDER_PROGRESS.md').read_text();progress+='''\n\n### 6. 11. 2026 – rozšírený finálny audit Vhannibala, PR #47 (bez produkčného merge)\n\n- Auditný základ FullHDGlass `603218ea8fa51176f686f14f303509a4c64dc7e1`; PiconHub main `e90a1fe3a2734b555f48f343284f9103530180fb`, produkčná vetva `a740b6da429b8d93eb0f3123158d81b8724f9d19`, Trezor `342e111a9b4adff06121c317d04ba2cfe4f82595`, GSU `c3978f69303de59391c1ff43b2563592526e97e2`. Stabilné vydania zostávajú 1.0.69 / 0.1.44 / 13.41-r4.\n- [Pracovná vetva a draft PR #47](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/47) obsahujú [úplný report](reports/vhannibal-completeness-20261106/README.md) a register 14 808 referencií. Skontrolovaných je 27 oficiálnych downloadov (jedna piconová sada + 26 sád nastavení), originály z 3. novembra a celé historické importné registre. Pôvodné septembrové a októbrové ZIPy neboli získané; ich pixely nie sú označené za skontrolované.\n- Fyzicky overených je všetkých 498 produkčných ZIPov, 1 804 častí a 400 476 PNG. Pre 10 435 aktuálnych TV referencií malo deväť platných neprázdnych variantov 10 293, pri 138 chýbal variant a pri štyroch bol PNG prázdny. Mimo TV rozsahu je oprávnene 2 704 referencií; 1 669 historických / bez presnej aktuálnej zhody sa neoznačuje automaticky za zaniknuté.\n- **Vhannibal nemožno označiť za kompletne spracovaný podľa MASTER V9.** Pripravená oprava 26 rôznych referencií v 69 ZIPoch obsahuje 186 doplnených a 12 opravených PNG záznamov (198 spolu). Po nej má 10 315 aktuálnych TV referencií deväť platných PNG, pri 118 stále chýba variant a dva TV5MONDE prípady majú prázdny kanonický Transparent. Všetkých 18 schválených CANAL+ balíkov je bitovo zachovaných.\n- Nové V9 návrhy majú [úspešné zostavenie](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/42206982364): 5 485 grafík, 49 365 PNG, 8 962 referencií. QC PASS má 125 referencií; 8 837 má REVIEW, ďalších 1 428 je pozastavených. Tieto počty nie sú schválením grafík. Osem konkrétnych konfliktov identity je evidovaných samostatne bez vymyslených log.\n- Kandidát prešiel produkčným validátorom a skutočnou inštalačnou metódou prijímača na 69 archívoch / 198 PNG; kontrolované boli SHA256, CRC, plné referencie, rozmery a zachovanie nesúvisiacich používateľských súborov. Nové grafiky, merge aj publikovanie stále čakajú na schválenie. Warder Radio a rádiové picony sa nemenili.\n- Ďalší krok: revízia uložených V9 hárkov, explicitných konfliktov a kanonického TV5MONDE; až potom vlastníkom schválený produkčný merge. Zdrojový checkpoint je zachovaný súkromne aj pre opakovanie po zmene upstreamu.\n''';(R/'WARDER_PROGRESS.md').write_text(progress)
print(json.dumps({k:v for k,v in summary.items()if k not in('v9_review','receiver_validation')},ensure_ascii=False))
