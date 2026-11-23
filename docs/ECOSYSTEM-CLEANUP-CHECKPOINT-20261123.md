# WARDER EVOLUTION — spoločný checkpoint po konzervatívnom uprataní (23. 11. 2026)

**Rozsah schválenia:** vlastník 23. 11. 2026 požiadal o jednorazové odstránenie iba preukázateľne nepotrebných pomocných checkpointov/testovacích artefaktov v troch repozitároch, bez prepisovania histórie a bez zásahu do chránených grafík, záloh, produkčných artefaktov a aktuálne rozpracovaných úloh; schválené PR sa po úspešných relevantných kontrolách bezpečne zlučujú do `main`. Tento dokument je **jediný nový spoločný checkpoint**, nie automatická autorizácia ďalších mazaní.

## Východiskové overené HEAD (`main`, 23. 11. 2026)

| Repozitár | HEAD pred úpravami | Overená ostrá verzia |
|---|---|---|
| [FullHDGlass](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution) | `cc6e5e49c8881f5ac63df6096727a5b0181841b2` | `v1.0.84`, GitHub Release, runtime `1.0.84` |
| [PiconHub](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution) | `f185e4f8a7427a43379fcab6a767783e6cd44937` | `v0.1.44`, GitHub Release, runtime `0.1.44` |
| [Warder Radio](https://github.com/Evolution-by-Warder/Radio-Warder-Evolution) | `d865da4b54c12045bea84054cb94abcbfdcdc4a1` | `warder-radio-v0.2.2`, runtime `0.2.2`; samostatné `radio-country-20261122` |

**Dôležité:** stav sa musí pri ďalšej práci znovu overiť; údaje sú bodový checkpoint, nie trvalý HEAD. Produkčné ZIPy/IPK ani fyzické prijímače sa týmto upratovaním nepretestovali.

## Preukázané odstránenia – cez auditované pracovné vetvy a PR, bez priameho prepisu `main`

| Repozitár | Odstránená pomocná položka | Zdôvodnenie | Pracovný commit / PR |
|---|---|---|---|
| FullHDGlass | `.github/workflows/publish-warder-1.0.70.yml` | Version-pinned vydávací workflow v `main` vyžadoval zdrojovú verziu `1.0.70`, kým aktuálny runtime je `1.0.84`. Išlo o starý manuálne spustiteľný vydávací mechanizmus, nie aktuálny publisher. Neboli odstránené testy, kód ani historické dôkazy. | `29ff1e1fb6b31437b72be4187b901dfc89bcb5f9`; [PR #143](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/143) |
| PiconHub | `.github/workflows/piconhub-0.1.41-download-fix.yml` | Jednorazový workflow viazaný na starú vetvu `release/piconhub-0.1.41-download-fix`, ktorá nie je v aktuálnom zozname vetiev. Vytváral `v0.1.41` a aktuálna ostrá verzia je `v0.1.44`. | `1ce71df0d951d1a87cc911620e484921568f388e`; [PR #85](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/pull/85) |
| PiconHub | `.github/workflows/four-profiles-candidate.yml` | Neprítomná výhradne cieľová vetva `feature/four-profiles-20261101`, žiadny workflow_dispatch/schedule/PR trigger, nijaký iný workflow ho nevyvoláva. Zdrojové testy ostali. | [PR #85](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/pull/85), squash `e88d02e392e77dcd76f98f861e957c5ce9adb1e9` |
| PiconHub | `.github/workflows/gles-wqhd-candidate.yml` | Neprítomná vetva `fix/generated-list-rows-20261102`; žiadne iné aktívne triggery alebo workflow závislosti. | [PR #85](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/pull/85) |
| PiconHub | `.github/workflows/openpli-stdlib-candidate.yml` | Neprítomná vetva `fix/openpli-stdlib-20261102`; testovacie skripty a kompatibilitné workflowy zachované. | [PR #85](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/pull/85) |
| PiconHub | `.github/workflows/runtime-cleanup-candidate.yml` | Neprítomná vetva `fix/receiver-runtime-cleanup`; žiadne ručné/plánované spúšťanie ani workflow závislosti. | [PR #85](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/pull/85) |
| Warder Radio | `.github/workflows/radio-019-upgrade-check.yml` | Jednorazový test aktualizácie `0.1.9.1` viazaný na neprítomnú starú `release/radio-0.1.9.1-20261106` vetvu. Aktuálna verzia `0.2.2` má samostatné zachované moderné testy. | `311ea06620ffdb9b454971aec64b2584ada0ddc8`; [PR #58](https://github.com/Evolution-by-Warder/Radio-Warder-Evolution/pull/58) |

**Presný stav k poslednému overeniu 23.11.2026:**

- **Warder Radio [PR #58](https://github.com/Evolution-by-Warder/Radio-Warder-Evolution/pull/58): ZLÚČENÉ.** GitHub Actions `unit` SUCCESS na PR SHA `311ea06620ffdb9b454971aec64b2584ada0ddc8`; manuálne preskúmaný presný diff jedného workflowu. Squash merge `6651d52db631c331ff135afbbeef48727df7c51a`; potvrdený `main`, runtime/feed `0.2.2` zachované.
- **PiconHub [PR #85](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/pull/85): ZLÚČENÉ.** Päť odstránených zastaraných YAML a aktualizovaná read-only grafická CI ochrana; kontrola `whole-logo-regressions` SUCCESS na presnom SHA `f77fac302948bda64b52a9cb9b1e21a9450df75b`. Squash merge `e88d02e392e77dcd76f98f861e957c5ce9adb1e9`. Žiadny IPK/ZIP ani grafika sa nemenili.
- **FullHDGlass [PR #143](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/143): ZLÚČENÉ.** Jeden odstránený historický publisher `publish-warder-1.0.70.yml`, rozšírená existujúca read-only CI ochrana a pridaný jediný spoločný checkpoint. Finálny CI `verify` SUCCESS na presnom SHA `7bf4008bc3f44e212d15d7754f1cc47f66ba4783`, [GitHub Actions #45147095092](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/45147095092). Squash merge `0b1ff58280f14e43bf03d66d6c367eae4d145322`. Aktuálny stable publisher a verzia `1.0.84` zostali zachované.
- **Celkom sedem odstránených pracovných YAML súborov v troch repozitároch** (FullHDGlass 1 + PiconHub 5 + Radio 1). Všetky zmazania boli vykonané cez PR; nesmie sa zamieňať otvorený PR s dokončeným merge. Bez mazania Git vetiev, tagov, GitHub Releases alebo historických Actions dôkazov.
- Pri workflowoch `.github/workflows/` prebehla individuálna manuálna bezpečnostná kontrola a na dotknutých PR sú zapojené existujúce nepublikujúce read-only testy. Dokončovací krok nespustil nové zostavenie testovacieho IPK ani novú SAT automatizáciu. Rádiový PR používal už existujúcu CI validáciu, ktorej súčasťou je historický interný balíkovací test; žiadny nový IPK alebo ZIP nebol publikovaný.

## Finálne overenie po zlúčení všetkých troch PR (23.11.2026)

| Repozitár | Preverený produkčný merge SHA | PR | Existujúce ostré vydanie |
|---|---|---|---|
| FullHDGlass | `0b1ff58280f14e43bf03d66d6c367eae4d145322` | [#143](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/143) MERGED | `v1.0.84`, runtime `1.0.84` |
| PiconHub | `e88d02e392e77dcd76f98f861e957c5ce9adb1e9` | [#85](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/pull/85) MERGED | `v0.1.44`, runtime `0.1.44` |
| Warder Radio | `6651d52db631c331ff135afbbeef48727df7c51a` | [#58](https://github.com/Evolution-by-Warder/Radio-Warder-Evolution/pull/58) MERGED | `warder-radio-v0.2.2`, runtime `0.2.2` |

Bola vykonaná opätovná nezávislá kontrola troch GitHub `main` refs, stavu `merged=true`, merge commitov, runtime verzií a existencie pôvodných produkčných Releases.

**Overené GitHub CI doklady:** FullHDGlass [run #45147095092](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/45147095092) `verify` SUCCESS na PR #143; PiconHub [run #45146715000](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/actions/runs/45146715000) `whole-logo-regressions` SUCCESS na PR #85; Warder Radio [run #45144965219](https://github.com/Evolution-by-Warder/Radio-Warder-Evolution/actions/runs/45144965219) `unit` SUCCESS na PR #58. Všetky testy boli vyhodnotené na presných finálnych SHA svojich upratovacích PR. **Zmazaných presne 7 workflow YAML súborov:** FullHDGlass 1, PiconHub 5, Warder Radio 1. Navyše sa upravili 2 už existujúce read-only kontrolné workflowy na spustenie CI pri bezpečnostných zmenách a doplnil sa tento istý checkpoint; žiadna ďalšia checkpointová séria. Všetky 3 cieľové PR majú doložené úspešné CI. Tento dokumentačný dodatok môže posunúť HEAD FullHDGlass po samostatnom schválenom merge, ale nemení vyššie uvedený commit PR #143 ani produkciu.

**Výsledok:** konzervatívne jednorazové upratanie **DOKONČENÉ A OVERENÉ** v troch hlavných projektoch. Žiadna vetva, tag, Release, zdrojový test, schválená grafika, produkčný updater, SAT picon, rádiodáta ani používateľské nastavenie neboli zmazané alebo prepísané. Fyzické testy na prijímači neboli súčasťou tohto úzkeho cleanup rozsahu; nemožno ich vykazovať ako PASS.

## Zachované naschvál

- Všetky ostré vydania, release assety, update feedy, produkčné SAT manifesty a ZIP/`.partNN`, návratové balíky, SHA-256 dôkazy, schválené MASTER V9 a CANAL+ SK/CZ grafiky a zákaznícke nastavenia.
- **Všetky existujúce vetvy a všetka Git história** vrátane zdrojových experimentov, výsledkov a checkpointov; žiadna vetva nebola odstránená alebo prepísaná.
- FullHDGlass [PR #141](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/141): otvorený nezávislý read-only audit publikovaných SAT provider ZIPov.
- Radio [draft PR #52](https://github.com/Evolution-by-Warder/Radio-Warder-Evolution/pull/52): obsahuje **605 vlastných commitov navyše oproti `main` podľa porovnania**, preto nie je možné tvrdiť, že jeho všetka práca je prenesená do produkcie. Zostáva vývojovo chránený.
- FullHDGlass vetvy `diagnostics/dns-warder-20261118-2042` (2 jedinečné commity, 1 workflow), `warder-modernization-work` (21 jedinečných commitov a otvorené rozdiely), `test/personal-skin-1080-r2-20261118` a `r3` (vlastné experimentálne workflowy), `audit/menu-icons-ids-and-dedup-20261117` (mnoho zmien artwork/manifestu), `docs/record-verified-automerge-136-20261122` (vlastný dokumentačný commit) zostávajú zachované pre samostatné rozhodnutie.
- PiconHub `warder-master-production` (66 jedinečných commitov), `factory-warder-development` (3828 jedinečných commitov), ďalšie SAT monitorovacie vetvy vrátane `audit/sat-manager-sync-20261123` a všetky registre SAT manažéra.
- Radio `feature/now-playing-screensaver-20261111` (52 jedinečných commitov) aj existujúce vydávacie a dvojtýždňové country workflowy.
- Historické `docs/`, `reports/` a testovacie GitHub Releases: **nevykonané žiadne plošné mazanie**. `docs/RELEASE_RETENTION_POLICY.md` vyžaduje pre konkrétny release overenie referencií, update cesty a recovery kópie. To sa pre množstvo starých TEST vydaní nepreukázalo.

## Pokračovanie podľa aktuálnych registrov

1. **Jazyky:** FullHDGlass `docs/SKIN-I18N-AUDIT-20261117.md` deklaruje 61 380 / 61 380 prítomných prekladových položiek v 20 cieľových jazykoch a 5 katalógových doménach; chýba fyzická/terminologická kontrola. Samostatná zrkadlená lokalizácia jadra WarderPiconHub má len 10 jazykov; zdroj pravdy preveriť v PiconHube pred úpravou.
2. **FTP:** `weatherIcons/piconWeather.zip` stále `SOURCE_PRESERVED_TARGET_MISSING` / `NOT_EXPOSED` v `assets/warder/legacy-ftp-migration.tsv`; pôvodné 14 463 135 B, SHA-256 `39cc98af95ef07c1b22d701399be2e60a39f7c54080c5c10a2d193858b5b34ad`. Pôvodný obsah je zachovaný mimo verejného GitHubu; nenasadzovať náhradu bez fyzického originálu a SHA kontroly.
3. **DNS/web:** zachovaná diagnostická vetva s jedinečnými commitmi; verejný DNS ani produkčný web zatiaľ týmto kontrolným cyklom neboli úspešne potvrdené.
4. **Radio:** `v0.2.2`, `radio-country-20261122` (224 krajín, 48 219 staníc a 40 837 log podľa `RADIO_PROGRESS.md`), country feed/automatizácia zachované; fyzické testovanie prijímača a samostatné otvorené úlohy zostávajú.
5. **SAT:** jeden existujúci Warder SAT Picon Manager, termín používateľa 03.12.2026 o 08:00 Europe/Bratislava; nevytvorená žiadna ďalšia automatizácia.

## Politika ďalšieho upratovania

Zmazať len ďalšie jednotlivo dokázané nepotrebné položky **po** preverení runtime referencií, CI, aktívnych vetiev, release pravidiel a rollbacku. Sporné prípady ponechať. Zmeny `.github/workflows/` podliehajú manuálnej bezpečnostnej kontrole podľa `AGENTS.md`; neobchádzať ochrany vetvy, nevytvárať novú IPK ani meniť produkčné dáta. Po merge každého PR overiť jeho skutočný stav a aktualizovať len status tohto checkpointu (nevytvárať novú paralelnú sériu).

## 23. 11. 2026 — rozšírená schválená retencia ostrých inštalačných balíkov (päť projektov)

**Nové schválenie:** aktuálna ostrá verzia plus maximálne tri staršie ostré verzie; nikdy nemaž aktívnu aktualizačnú cestu, rollback ani zdrojové dáta. Schválenie v tomto chate sa týka FullHDGlass, PiconHub, Warder Radio, GSU a YouTube. Zmeny realizovať cez samostatné pracovné vetvy a PR; pri CI/overení uviesť skutočný stav.

**Východiskové main:** FullHDGlass `981071a363986afb70b8b919eb6fb24cbdd71acb`; PiconHub `e88d02e392e77dcd76f98f861e957c5ce9adb1e9`; Radio `6651d52db631c331ff135afbbeef48727df7c51a`; GSU `26b71c9d7c4707a379ba7d43c3864ab8371a21a3`; YouTube `8d1f10e9849b7754716f3fa9772f69b70b589855`. Tieto SHA reprezentujú stav pred novou retenčnou dávkou.

| Produkt | Ostré verzie na ponechanie | Stav kandidáta |
|---|---|---|
| FullHDGlass | `1.0.84`, `1.0.83`, `1.0.82`, `1.0.80` | `packages/` mal 61 záznamov (517 552 114 B); 24 zastaraných IPK + 24 SHA = **48 odstránených súborov z pracovnej vetvy** (412 670 304 B / 393,55 MiB). Nová vetva `maintenance/retain-four-stable-ipk-20261123` a CI majú potvrdiť bezpečnosť pred merge do main. |
| PiconHub | `0.1.44`, `0.1.43`, `0.1.42` (iba 3 existujúce ostré) | Aktuálny main nemá historické IPK v `packages/`, iba potrebné DAB dátové ZIPy. |
| Radio | `0.2.2`, `0.2.1`, `0.2.0`, `0.1.9.4` | Žiadne IPK v main; 224-krajinná dátová Release je neporušiteľný dátový produkt, **nepočíta sa** ako verzia prehrávača. TEST a staršie release assety riešiť iba po preverení odkazov/obnovy. |
| GSU | `13.41-r4`, `13.40-r95`, `13.40-r94`, `13.40-r93` | Nemá IPK v main; `13.40-r93` je aj prechodný balík pôvodnej opkg identity, nemazať. |
| YouTube | `1.0.2`, `1.0.1`, `1.0.0` (iba 3) | Žiadne IPK v main; všetky tri aktuálne ostré Releases zachovať. |

### Dve explicitné FullHDGlass migračné výnimky mimo štyroch ostrých verzií

1. **`1.0.18` pôvodnej opkg identity:** aktívny `main/update.json` je legacy bootstrap zo starej inštalácie. Priamy skok bez prípravného balíka `preinst` odmieta; táto verzia ostáva, hoci nepatrí medzi posledné štyri ostré.
2. **`1.0.72` pre historických TEST klientov:** aktuálny `warderAutoUpdate.TEST` z balíkov stále vyberá `warder-modernization-work/update-test.json`, ktorý ukazuje na `main/packages/1.0.72`. Jeho odstránenie by mohlo rozbiť TEST aktualizáciu. Zachovať, kým sa samostatná cesta nezmení a neotestuje.

`main/update-test.json` bol na pracovnej vetve zosúladený zo zastaranej 1.0.69 na overenú 1.0.84 a SHA `623be902288bf1bc872425729d5a85596228d06593f022ff60b8572b23227591`. `main/update.json` ostáva z dôvodu kompatibility na 1.0.18 a poskytuje informáciu o následnej 1.0.84. Produkčný publisher po ďalšom novom vydaní automaticky odstráni staršie súbory až po nemennom Release, správnych feedech a fail-closed regresiách; nespúšťa sa len pri zmene vlastného YAML.

**Nedotknuté:** SAT balíky, MASTER V9, CANAL+ SK/CZ, rádio katalóg, už vydané Releases/tagy, iné pracovné vetvy, prílohy PR #52, Trezor. Odstraňovanie historických GitHub Releases vyžaduje samostatne preukázaný audit aktívnych externých odkazov a bezpečnú návratovú kópiu; nerobiť neoverené mazanie a nepriznávať si z neho úsporu v main.


## 23. 11. 2026 — finálne overené výsledky päťprojektového upratovania (tento oddiel má prednosť pred predchádzajúcim pracovným plánom)

**Zdroj schválenia:** vlastník výslovne schválil najnovšiu ostrú verziu a najviac tri predchádzajúce ostré verzie v piatich repozitároch, bezpečné odstránenie nepotrebných historických IPK/SHA po overení odkazov, opravu FullHDGlass feedov, trvalé opatrenie v publisheri a aktualizáciu tohto jediného checkpointu. Staršie spomenuté „iba pracovná vetva“ znamenalo priebežný stav PRED nasledujúcimi potvrdenými merge.

| Projekt | Výsledný overený `main` po PR | Ponechané ostré vydania | Odstránené z main (nová dávka) | Zmenené/ušetrené bajty v aktuálnom strome |
|---|---|---|---|---|
| FullHDGlass | `f294be86720a6b3b754ccdd08ccd1e668be5ea56` ([PR #145](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/145) MERGED) | `1.0.84, 1.0.83, 1.0.82, 1.0.80` | **24 starých IPK + 24 SHA-256 = 48 súborov**; 24 verzií zo série `1.0.48–1.0.79` okrem chránených `1.0.72` a `1.0.80` | **412 670 304 B = 393,55 MiB** |
| PiconHub | `2018ec15efff0d51b41fcaa5a4d421fe18b5d76d` ([PR #86](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/pull/86) MERGED) | `0.1.44, 0.1.43, 0.1.42` (iba 3 existujúce) | 0 starých IPK, 0 SHA | **0 B** |
| Warder Radio | `b63e61f3531e083f641079e8df21f6725d006d0f` ([PR #59](https://github.com/Evolution-by-Warder/Radio-Warder-Evolution/pull/59) MERGED) | `0.2.2, 0.2.1, 0.2.0, 0.1.9.4` | 0 starých IPK, 0 SHA | **0 B** |
| GSU | `b173e1cdf7eb30d11821129ba3a0d14971813d76` ([PR #12](https://github.com/Evolution-by-Warder/GSU-Warder-Evolution/pull/12) MERGED) | `13.41-r4, 13.40-r95, 13.40-r94, 13.40-r93` | 0 starých IPK, 0 SHA | **0 B** |
| YouTube | `c6de0d43615a0961f7a2407597777f6820cbe5c2` ([PR #7](https://github.com/Evolution-by-Warder/YouTube-Warder-Evolution/pull/7) MERGED) | `1.0.2, 1.0.1, 1.0.0` (iba 3 existujúce) | 0 starých IPK, 0 SHA | **0 B** |

**Overené kroky:**
- FullHDGlass [PR #145](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/145) prešiel všetkými **9/9 GitHub CI kontrolami** (`verify-stable-package`, `verify`, `integration-tests`, tri OpenATV vetvy a tri OpenPLi/regresné joby). Workflow publish zachoval oficiálny vydávací mechanizmus, ale pri budúcich release po overení Release + update feedov prerezáva staré IPK dvojice fail-closed skriptom `tools/retain-fullhdglass-stable.py`. Už nezakladá nové IPK kvôli zmene samotného YAML.
- Aktualizátor: `main/update-production.json` aj `main/update-test.json` teraz zhodne uvádzajú `1.0.84`, `sha256 623be902288bf1bc872425729d5a85596228d06593f022ff60b8572b23227591` a reálne ponechanú raw-main IPK URL. Odstránený bol starý test-feed odkaz na `1.0.69` z `main`.
- Legacy `main/update.json` **úmyselne stále ponúka `1.0.18`** a jej vlastný fyzicky prítomný IPK/SHA, pretože pôvodná opkg identita potrebuje prípravu migrácie. Changelog/upstream informácia odkazuje po tomto kroku na najnovšiu produkčnú `1.0.84`. Tým sa zachová kompatibilita starého používateľa; zmena `update.json` priamo na nové meno IPK by sa nesmela vydávať za bezpečnú.
- Staršie `-test` runtime stále hardcodujú `warder-modernization-work/update-test.json` → `1.0.72`; IPK/SHA `1.0.72` zostali v main ako **samostatná doložená migračná výnimka**. Bez budúceho overeného presmerovania ju nemaž.
- Následná nezávislá kontrola cez GitHub API potvrdila `main` SHA, odstránené súbory v `main/packages/`, oba aktuálne feedy, SHA sidecars, existenciu štyroch ostrých FullHDGlass Releases a zachované GSU/radio/YouTube/PiconHub výstupné cesty.
- PiconHub, Radio, GSU a YouTube už pred týmto rozsahom nemali historické inštalačné IPK v `main`; ich vydávanie ostáva **GitHub Releases-only**. Aktualizovali sa existujúce retenčné dokumenty, v YouTube aj zastaraný `update/README.md`. YouTube PR #7 mal GitHub `test` SUCCESS; tri ostatné PR boli dokumentačné a porovnané priamo s platnými feedmi/release tagmi bez zmeny runtime.
- V tejto **novej** dávke nebol odstránený žiadny ďalší workflow; predchádzajúcich **7** už zmazaných nefunkčných YAML z PR #143/#85/#58 zostáva odstránených. Žiadny prípravný TEST IPK ani nový release sa touto retenciou nepublikoval.

**GitHub Releases / TEST artefakty — otvorená stop-podmienka, nie úspešné zmazanie:**
- Odstránených historických Releases: **0** v každom z piatich projektov. FullHDGlass má po tejto dávke stále **21 Releases** vrátane 15 starších `radio-live-test124–138` prerelease a dvoch starších ostrých `v1.0.78/79`; Radio má stále **9 Releases** vrátane mimo-štvoricových `0.1.9.2/0.1.9.3` a testovacej migrácie. Zvyšné počty: PiconHub **3**, GSU **4**, YouTube **3**.
- Niektoré staré testovacie tagy sú **funkčná migračná závislosť** (Radio `warder-radio-v0.1.0-test11` je citovaný živým `radio-test.yml` a `update/testing.json`; GSU r93 používa `plugin/update/candidate.json`); veľký `radio-country-20261122` je **samostatný produkčný dátový katalóg 224 krajín**, nie „piata verzia“ prehrávača. Bez úplného overenia odkazov, dlhodobej obnovy binárnych Release assetov a dostupnej bezpečnej mazacej operácie sa ostatné staré release assety **neodstránili**. GitHub connector nemá akciu na mazanie GitHub Releases; neobchádzať autorizáciu a nepredstierať zmazanie.
- Z toho dôvodu je splnené **vyčistenie súčasného zdrojového stromu FullHDGlass a ochrana ďalšieho rastu**, nie definitívna redukcia všetkých historických GitHub Releases. Toto je zámerne otvorená oblasť, nie druhý checkpoint.

**Rollback / aktualizácia:** existujúce adresy, version/sha metadáta, CI inštalačné/regresné testy a všetky potrebné GitHub Release assety boli overené; **fyzická zmena a návrat na konkrétnom Enigma2 prijímači** nebola vykonaná v tomto upratovacom rozsahu a nesmie sa prezentovať ako fyzický PASS. Git história a ochrany všetkých schválených dát sú nezmenené.

