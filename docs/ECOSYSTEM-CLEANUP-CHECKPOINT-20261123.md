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
| FullHDGlass | `f294be86720a6b3b754ccdd08ccd1e668be5ea56` ([PR #145](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/145) MERGED) | `1.0.84, 1.0.83, 1.0.82, 1.0.80` | **24 starých IPK + 24 SHA-256 = 48 súborov**; 24 verzií zo série `1.0.48–1.0.79` okrem chránených `1.0.72` a `1.0.80` | **412 669 094 B netto = 393,55 MiB** |
| PiconHub | `2018ec15efff0d51b41fcaa5a4d421fe18b5d76d` ([PR #86](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/pull/86) MERGED) | `0.1.44, 0.1.43, 0.1.42` (iba 3 existujúce) | 0 starých IPK, 0 SHA | **0 B** |
| Warder Radio | `b63e61f3531e083f641079e8df21f6725d006d0f` ([PR #59](https://github.com/Evolution-by-Warder/Radio-Warder-Evolution/pull/59) MERGED) | `0.2.2, 0.2.1, 0.2.0, 0.1.9.4` | 0 starých IPK, 0 SHA | **0 B** |
| GSU | `b173e1cdf7eb30d11821129ba3a0d14971813d76` ([PR #12](https://github.com/Evolution-by-Warder/GSU-Warder-Evolution/pull/12) MERGED) | `13.41-r4, 13.40-r95, 13.40-r94, 13.40-r93` | 0 starých IPK, 0 SHA | **0 B** |
| YouTube | `c6de0d43615a0961f7a2407597777f6820cbe5c2` ([PR #7](https://github.com/Evolution-by-Warder/YouTube-Warder-Evolution/pull/7) MERGED) | `1.0.2, 1.0.1, 1.0.0` (iba 3 existujúce) | 0 starých IPK, 0 SHA | **0 B** |

**Presná bilancia:** pôvodný `main/packages/` mal 517 552 114 B a po merge má 104 883 020 B. Hrubá veľkosť 48 odstránených súborov je **412 670 304 B**; zmena `packages/README.md` ho zväčšila o 1 210 B, preto je **čistá úspora 412 669 094 B**. Git objekty v historických commitoch zostávajú zachované, nejde o fyzickú úsporu celej Git histórie.

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



## 23. 11. 2026 — konečný audit historických GitHub Releases (posledná fáza)

**Autorizácia:** vlastník 23.11.2026 schválil dokončiť retenciu najnovšie ostré + maximálne 3 predchádzajúce ostré verzie. Nezmenené pravidlá: najprv aktualizátor, rollback, dokumentácia a skutočné binárne zálohy. Zdroj: priamo živé GitHub Releases API + aktuálny `main` každého repozitára; pri nájdenom novom Release inventár znovu preveriť.

**Pripojenie a vykonateľnosť:** existujúce autorizované GitHub rozhranie podporuje čítanie Releases a PR, ale **neposkytuje mazanie GitHub Release, jeho assetov ani starých Actions artefaktov**. Žiadne z týchto objektov neboli týmto cyklom vymazané. Nepoužívať alternatívny token, 2FA, prístup ani neobchádzať obmedzenia. Manuálny postup nižšie je samostatná následná operácia používateľa, nie doklad o vykonanom mazaní.

### Aktuálne počty a povinné ochrany

| Repozitár | Súčasné Releases | Zachovať | Mimo retenčnej štvorice / status |
|---|---:|---|---|
| FullHDGlass | **21** | `v1.0.84`, `v1.0.83`, `v1.0.82`, `v1.0.80`; samostatné raw-main výnimky `1.0.18`, `1.0.72` | 15 rádiových `TEST124–138` a 2 historické ostré `v1.0.78/v1.0.79`; **17 kandidátov, 0 vymazaných** |
| PiconHub | **3** | `v0.1.44`, `v0.1.43`, `v0.1.42` | 0 |
| Radio | **9** | `warder-radio-v0.2.2`, `v0.2.1`, `v0.2.0`, `v0.1.9.4`; oddelené `radio-country-20261122` (224 krajín) a migračné `warder-radio-v0.1.0-test11` | `0.1.9.2`, `0.1.9.3`, `0.2.0-test22` = 3 kandidáti; **0 vymazaných** |
| GSU | **4** | `v13.41-r4`, `v13.40-r95`, `v13.40-r94`, `v13.40-r93` (r93 stále používa `plugin/update/candidate.json`) | 0 |
| YouTube | **3** | `youtube-warder-v1.0.2`, `v1.0.1`, `v1.0.0` | 0 |

### FullHDGlass — presných 15 TEST + 2 staré ostré (ručný zoznam)

| Release tag/odkaz | GitHub Release ID | Počet assetov | Veľkosť (B) | Bezpečnostný stav |
|---|---|---:|---:|---|
| [`radio-live-test124-20261119`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/radio-live-test124-20261119) | `450948394` | 3 | 18 325 205 | KANDIDÁT: najprv obnovovacia kópia a externé odkazy |
| [`radio-live-test125-20261119`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/radio-live-test125-20261119) | `450961338` | 3 | 18 330 843 | KANDIDÁT: najprv obnovovacia kópia a externé odkazy |
| [`radio-live-test126-20261119`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/radio-live-test126-20261119) | `450977851` | 3 | 18 331 345 | KANDIDÁT: najprv obnovovacia kópia a externé odkazy |
| [`radio-live-test127-20261119`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/radio-live-test127-20261119) | `451002406` | 3 | 18 332 523 | KANDIDÁT: najprv obnovovacia kópia a externé odkazy |
| [`radio-live-test128-20261119`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/radio-live-test128-20261119) | `451014439` | 3 | 18 336 895 | KANDIDÁT: najprv obnovovacia kópia a externé odkazy |
| [`radio-live-test129-20261119`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/radio-live-test129-20261119) | `451030981` | 3 | 18 339 557 | KANDIDÁT: najprv obnovovacia kópia a externé odkazy |
| [`radio-live-test130-20261119`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/radio-live-test130-20261119) | `451132817` | 3 | 18 340 387 | KANDIDÁT: najprv obnovovacia kópia a externé odkazy |
| [`radio-live-test131-20261119`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/radio-live-test131-20261119) | `451157691` | 3 | 18 342 831 | KANDIDÁT: najprv obnovovacia kópia a externé odkazy |
| [`radio-live-test132-20261119`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/radio-live-test132-20261119) | `451222303` | 3 | 18 343 219 | KANDIDÁT: najprv obnovovacia kópia a externé odkazy |
| [`radio-live-test133-20261119`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/radio-live-test133-20261119) | `451237908` | 3 | 18 343 853 | KANDIDÁT: najprv obnovovacia kópia a externé odkazy |
| [`radio-live-test134-20261119`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/radio-live-test134-20261119) | `451279436` | 3 | 18 344 641 | KANDIDÁT: najprv obnovovacia kópia a externé odkazy |
| [`radio-live-test135-20261119`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/radio-live-test135-20261119) | `451301242` | 3 | 18 344 641 | KANDIDÁT: najprv obnovovacia kópia a externé odkazy |
| [`radio-live-test136-20261119`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/radio-live-test136-20261119) | `451358455` | 3 | 18 345 141 | ZADRŽAŤ: priame odkazy v WARDER_PROGRESS |
| [`radio-live-test137-20261119`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/radio-live-test137-20261119) | `451394561` | 3 | 18 346 171 | ZADRŽAŤ: priame odkazy v WARDER_PROGRESS |
| [`radio-live-test138-20261119`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/radio-live-test138-20261119) | `451483754` | 3 | 18 346 797 | ZADRŽAŤ: aktívny ručný workflow + priame odkazy |
| [`v1.0.78`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/v1.0.78) | `440647553` | 2 | 18 111 158 | KANDIDÁT: mimo 4 ostrých; preveriť historické URL a backup |
| [`v1.0.79`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/v1.0.79) | `441872495` | 2 | 18 124 736 | KANDIDÁT: mimo 4 ostrých; preveriť historické URL a backup |

**Súčet:** 15 TEST = **275094049 B** (262.35 MiB), 2 prebytočné ostré = **36235894 B** (34.56 MiB). Dokopy 17 Releases, 49 assetov, **311329943 B**. Žiadna z týchto veľkostí nebola zatiaľ fyzicky uvoľnená. Release ID je jednoznačný cieľ pre prípadnú manuálnu operáciu; pred každou operáciou znovu potvrdiť tag, počet assetov, digest a hlavný feed.

**Zistené závislosti:** `WARDER_PROGRESS.md` priamo odkazuje na test136/137/138; `docs/RADIO-LIVE-BOUQUETS-20261119.md` opisuje TEST124/125; `.github/workflows/radio-live-test-package.yml` stále obsahuje `workflow_dispatch` a vydávací kód pre presný tag TEST138. Test136–138 **zadržať**, kým sa verejná dokumentácia a workflow neprevedú na historický záznam bez aktuálnych binárnych odkazov. Pri test124–135 nemožno z neexistencie aktívneho feedu vyvodiť neprítomnosť externých používateľských URL. Každá testovacia IPK bola jediným priamym odkazom svojho historického Release; bez overenej recovery kópie ju označiť ako KANDIDÁT, nie schválené bezpečné zmazanie.

### Warder Radio — tri kandidáti, ochrana starého migračného mosta

| Release tag/odkaz | GitHub Release ID | Počet assetov | Veľkosť (B) | Bezpečnostný stav |
|---|---|---:|---:|---|
| [`warder-radio-v0.1.9.2`](https://github.com/Evolution-by-Warder/Radio-Warder-Evolution/releases/tag/warder-radio-v0.1.9.2) | `436716653` | 3 | 3 179 797 | KANDIDÁT: overiť opkg/testovacie aktualizácie a zálohu |
| [`warder-radio-v0.1.9.3`](https://github.com/Evolution-by-Warder/Radio-Warder-Evolution/releases/tag/warder-radio-v0.1.9.3) | `440470107` | 3 | 3 182 993 | KANDIDÁT: overiť opkg/testovacie aktualizácie a zálohu |
| [`warder-radio-v0.2.0-test22`](https://github.com/Evolution-by-Warder/Radio-Warder-Evolution/releases/tag/warder-radio-v0.2.0-test22) | `446820666` | 3 | 2 931 612 | KANDIDÁT: overiť opkg/testovacie aktualizácie a zálohu |

**Súčet:** 3 kandidáti, 9 assetov, **9294402 B** (8.86 MiB). `warder-radio-v0.1.0-test11` **NIE JE** kandidát; na jeho IPK stále smeruje `update/testing.json` a odkazuje `.github/workflows/radio-test.yml`. Moderné `update/v2/stable.json` a `update/v2/testing.json` smerujú na `v0.2.2`. Nevymazať `radio-country-20261122` ani jediný zo 225 originálnych dátových assetov. Pred čistením `0.2.0-test22` preveriť existujúce tester-bridge scenáre; pred čistením `0.1.9.2/0.1.9.3` preveriť historické inštalačné/regresné odkazy.

### Aktívne aktualizačné cesty overené v zdrojoch

- FullHDGlass `main/update-production.json` a `main/update-test.json`: `1.0.84`, `sha256 623be902288bf1bc872425729d5a85596228d06593f022ff60b8572b23227591`; `main/update.json`: originálna migrácia `1.0.18`, `sha256 f785741d79a93d06e9d252e64e3d5b7a35a642db117aff1084dcfd20878f2383`; `warder-modernization-work/update-test.json` na historickú `1.0.72` (ochrana trvá).
- PiconHub `plugin/update/stable.json`: release `0.1.44`, verifikované Release assety. GSU `plugin/update/stable.json` `13.41-r4`, `plugin/update/candidate.json` `13.40-r93`. YouTube `update/stable.json`: `1.0.2`; testovací manifest má `release:null`.
- Radio moderné `update/v2/stable.json`, `update/v2/testing.json`: `0.2.2`; starý testovací `update/testing.json`: `0.1.0-test11`. Dátový `assets/radio-country/latest.json` je oddelený a nesmie byť menený v retencii programu.
- GitHub Release API potvrdzuje existenciu aktuálnych oficiálnych assetov, ich veľkosti a samostatný SHA-256 digest; ide o kontrolu zdrojov a distribučnej integrity, **nie fyzický downgrade test**.

### Presný bezpečný manuálny postup — vykoná iba autorizovaný vlastník

1. **Pred každým mazaním** stiahnuť IPK, `.sha256`/`SHA256SUMS`, `build.json` alebo testový manifest a celý text poznámok Release. Skontrolovať SHA-256 obsahu voči sidecaru alebo `assets[].digest` z GitHub API; následne uložiť overené identické bajty do samostatnej vlastníkovi schválenej návratovej zálohy. Nezapisovať/neorganizovať pôvodné Trezor originály; nová záloha má mať oddelenú evidenciu. Kým kópia s presným SHA reálne neexistuje, Release **nevymazať**.
2. Overiť všetky aktívne raw/Release adresy vo feedoch, updatéroch, inštalátoroch, `README.md`, dokumentoch a aktuálnych workflowoch. Nájsť aj externé používateľské odkazy a prípadné stále používané TEST inštalácie; nespoliehať sa na neúplný GitHub code search. Pri nájdenej závislosti najprv presmerovať klienta a otestovať; dovtedy ponechať výnimku.
3. Až pre jednoznačne uvoľnený tag otvoriť vyššie priloženú stránku `Releases → príslušné vydanie` na GitHube; zvoliť ikonu koša a **Delete this release**, potvrdiť. **Nezaškrtávať ani samostatne nemažte Git tag** a nepoužívať force-push. Pri immutable-release ochrane, neprístupnom ovládaní alebo nedostatočnej právomoci zastaviť dotknutý release; obmedzenia neobchádzať. Oficiálny postup: https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository.
4. Po **každom jednotlivom** mazaní overiť API `GET /repos/Evolution-by-Warder/<repo>/releases/tags/<tag>` → release už nie je prítomný, zostávajúce 4 ostré/releases/feed SHA a archívny backup existujú, cieľové IPK zostali inštalovateľné. Zaznamenať dátum, presný Release ID, asset IDs, SHA a výsledok do tohto istého checkpointu. Nikdy neoznačiť prácu ako dokončenú bez reálneho post-checku.

**Bodový výsledok 23.11.2026:** 5 repozitárov overených; **0 Releases a 0 Release assetov skutočne odstránených**, **20 potenciálnych kandidátov** (17 FullHDGlass, 3 Radio), celková teoretická veľkosť **320624345 B (305.77 MiB)**. Štvorkové pravidlo už platí pre novú distribúciu a aktuálny `main/packages/`, ale úplné fyzické zmazanie starých GitHub Releases je **otvorené** do bezpečného manuálneho vykonania a overenia. K tomuto stavu neexistujú doložené recovery kópie všetkých kandidátskych binárnych Releases; nedeklarovať pripravenosť na okamžité kliknutie „Delete“ bez nich.

### Samostatná dokončená korekcia verejných odkazov

Na pracovnej vetve tejto dávky je opravený `README.md`: hlavný download už nesmeruje na historickú `v1.0.69` a staré nápovedné linky `v1.0.66/67` smerujú na platnú `v1.0.84`, pričom historický text zostal. `docs/CURRENT-RELEASE.md` už správne označuje `v1.0.84` namiesto `v1.0.73` a uvádza presný SHA-256, byte size, zachované rollbacky a migračné výnimky. Tieto dokumentačné zmeny **nie sú odstránením Releases** a nesmú spustiť nový vydávací IPK.


## 23. 11. 2026 — oprava skutočného stavu DNS/webu a pôvodného FTP počasia

### DNS a verejný web: FUNKČNÉ — potvrdené vlastníkom
Vlastník 23. 11. 2026 predložil priamy snímok fungujúcej stránky `https://warder-evolution.eu/` v prehliadači Firefox: úspešne načítaná oficiálna titulná stránka Warder Evolution, HTTPS, menu Home / Privacy / Terms / GitHub a karty projektov. Vlastník výslovne potvrdil plnú funkčnosť domény. **Predchádzajúce hlásenia „DNS SERVFAIL/REFUSED“, „web čaká na aktiváciu“ či „neoverené“ už nesmú byť citované ako aktuálna otvorená úloha pre DNS a titulnú stránku.** Toto je reálne používateľské overenie konkrétnej verejnej adresy; nie je to automatický test každej podstránky alebo dostupnosti z každej siete. Nepresúvaj hotovú aktiváciu domény znovu do TODO.

### `weatherIcons/piconWeather.zip`: presný pôvodný zdroj identifikovaný; distribúcia ešte nie je hotová
- Súčasný verejný `main` stále **nemá** `assets/warder/downloads/weather/icons/piconWeather.zip`; `downloads.json` nemá službu `weatherIcons`. Stav `NOT_EXPOSED` sa zámerne nemení, kým archív nie je skutočne skopírovaný a overený.
- Pôvodný archív je evidovaný v súkromnom repo `Evolution-by-Warder/Trezor`, v `archives/hdglass-ftp/ORIGINAL-FTP-INVENTORY.md`. Presná pôvodná cesta: `weatherIcons/piconWeather.zip`, **14 463 135 B**, **SHA-256 `39cc98af95ef07c1b22d701399be2e60a39f7c54080c5c10a2d193858b5b34ad`**.
- Zálohový kontext: súkromný GitHub Release `Evolution-by-Warder/Trezor` / `hdglass-ftp-snapshot-2026-09-12`, archív `HDGlass_FTP_GOLDEN_MASTER_2026-09-12.zip` (535 201 061 B). Privátny inventár potvrdzuje identitu zaznamenaného súboru, no jeho binárne bajty neboli týmto kontrolným krokom vyextrahované a prepočítané.
- **Nasledujúci jediný realizačný krok:** z vlastníkovej chránenej zálohy extrahovať presne `weatherIcons/piconWeather.zip`, overiť veľkosť a SHA-256; pri zhode umiestniť do `assets/warder/downloads/weather/icons/`, doplniť `downloads.json`, opraviť presne túto položku v `legacy-ftp-migration.tsv` a jej sumári, otestovať bezpečné extrahovanie na externé `hdg17_files`, CI a následne publikovať cez riadny schválený PR. **Neimprovizovať iný ZIP ani nepoužiť farebné `picWeaInf.zip` ako náhradu.** Starý FTP snapshot/Trezor nikdy neprepisovať.
- **Aktuálny stav**: originál presne lokalizovaný v inventári súkromnej zálohy, ale samostatný archív zatiaľ nie je distribuovaný; neoznačovať `weatherIcons` za hotový bez byte-level overenia a produkčného merge.


## 23. 11. 2026 — finálne uzavretie historického `weatherIcons/piconWeather.zip`

Po dodatočnej kontrole **skutočného produkčného `plugin.py` / `downloadMenu.menuListAll`** (stav `main` 23.11.2026) je doložené, že `weatherIcons` klasický ZIP **nie je používaný ani ponúkaný súčasným sťahovacím menu**. Používané voľby sú `piconWeather` (aktuálne čierne/biele meteorologické picony), `weatherIconsN` a `animWeatherIcons`; voľná historická cesta `weatherIcons/` sa ešte tvorí v `chckPath` kvôli spätnej kompatibilite používateľských priečinkov, nejde o sieťový download ani o požiadavku na starý ZIP.

Rozhodnutie: historický `weatherIcons/piconWeather.zip` sa preklasifikuje z `SOURCE_PRESERVED_TARGET_MISSING / NOT_EXPOSED` na **`ARCHIVE_ONLY / ARCHIVE_ONLY`**. Súbor sa **nepublikuje** do produkcie, pretože by sa obnovovala funkcia, ktorú súčasný skin vôbec neponúka. Originálne dáta zostávajú bezpečne zachované v súkromnom FTP snapshote; žiadne binárne súbory, skin/runtime, testovacie alebo ostré IPK, nastavenia, zálohy ani existujúce Weather ZIPy sa nemenia. `assets/catalog.json` prestáva mylne označovať túto položku ako „čaká na obnovu“. Súhrn: **27 pôvodných súborov = 18 manifestom zásobovaných aktívnych rodín + 9 archívnych, 0 aktívnych chýbajúcich rodín, 0 starých FTP fallbackov**.

**Tento novší verdikt nahrádza predchádzajúce priebežné poznámky „chýba weatherIcons“** v tomto checkpointe a v starých dokumentoch. Vlastník žiada vyriešenie historicky otvorenej položky; nezadával však samostatné znovuzaradenie klasickej sady do aktuálneho sťahovacieho menu. Jej prípadné opätovné sprístupnenie by vyžadovalo jasne pomenovaný funkčný rozsah a overené originálne bajty. Táto uzávierka nemá meniť ani robiť tvrdenia o samostatnej funkčnosti ostatných aktuálnych meteo ikonových balíkov nad rámec ich produkčnej prítomnosti.
