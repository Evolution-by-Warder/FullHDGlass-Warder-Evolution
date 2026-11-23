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
- **FullHDGlass [PR #143](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/143): pripravené na dokončenie, aktuálny merge status nezamieňať za hotový.** Odstránený jeden nefunkčný version-pinned publisher `1.0.70`; existujúci `verify-radio-release.yml` rozšírený o read-only kontrolu zmien workflowov a checkpointu. Relevantné CI `verify` už absolvovalo SUCCESS na pracovnom SHA `3782814274cb012d69b154e3bf3376885c0f7df5`; po posledných dokumentačných zmenách musí byť finálny HEAD znova úspešne overený pred merge.
- **Celkom sedem odstránených pracovných YAML súborov v troch repozitároch** (FullHDGlass 1 + PiconHub 5 + Radio 1). Všetky zmazania boli vykonané cez PR; nesmie sa zamieňať otvorený PR s dokončeným merge. Bez mazania Git vetiev, tagov, GitHub Releases alebo historických Actions dôkazov.
- Pri workflowoch `.github/workflows/` prebehla individuálna manuálna bezpečnostná kontrola a na dotknutých PR sú zapojené existujúce nepublikujúce read-only testy. Žiadne nové testovacie IPK ani SAT automatizácie sa v tejto dávke zámerne nevytvárali.

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
