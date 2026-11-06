# Warder Evolution – stav projektu

**Aktualizované 6. 11. 2026.** Spoločný register pre pokračovanie v novom Worku. Tento Work rieši skin, PiconHub a satelitné picony vrátane Vhannibala. Rádiové picony a Warder Radio má na starosti samostatný Work. SHA nižšie sú overené východiská tejto inventúry. Pri ďalšej práci over živé vetvy, PR a vydania podľa [projektových pokynov](AGENTS.md).

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

### 6. 11. 2026 – audit úplnosti Vhannibal

- [Pracovný audit](reports/vhannibal-completeness-20261106/README.md) porovnáva nový Picon Motor z 5. novembra, tri dostupné historické inventúry a starší importný výpis so stavom živého katalógu. Obsahuje počty, vylúčenia a samostatný zoznam otvorených referencií.
- V centrálnych adresároch 498 produkčných ZIPov je 400 476 PNG položiek, bez duplicity názvu v jednom balíku. Všetkých 12 508 doteraz prijatých referencií má v určenom satelitnom balíku deväť variantov. Rozdelenie podľa providerov má osobitné otvorené položky.
- Tri opravy pre Quest Red, Karavan TV a Viasat Kino sú otestované v 27 ZIPoch na pracovnej vetve. Zo 14 635 platných zdrojových referencií je 10 210 spracovaných, tri opravené v kandidátovi, 3 866 doložene vynechaných a 556 otvorených. Produkčné zlúčenie čaká na schválenie.

### 6. 11. 2026 – prevzatie satelitného auditu po Vhannibalovi

- Po schválení je [PR #43](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/43) zlúčený. `AGENTS.md` aj `WARDER_PROGRESS.md` na `main` boli overené voči schváleným verziám.
- Overený verejný [manifest](assets/warder/downloads/picons/channels/manifest.json) a jeho SHA256. Všetkých 1 804 deklarovaných častí má záznam v `SHA256SUMS` a súbor v Git strome. Katalóg obsahuje 498 ZIPov, 56 selektorov a 166 kombinácií selektora a rozmeru, každú s troma pozadiami. Táto kontrola overila úplnosť katalógu a evidencie častí. Fyzické testy ZIPov sú zaznamenané pri PR #42 nižšie.
- Z pripnutého vstupu bol znova zostavený `plans.json`. Overených 12 508 unikátnych plných referencií, všetkých 12 503 pôvodných referencií zachovaných, päť pridaných a jeden záznam CHC-HD aktualizovaný. Živý manifest eviduje 193 výnimiek.
- Otvorený [PiconHub #30](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/issues/30) obsahuje historické porovnanie 3 388 kandidátov podľa názvov súborov a vtedajších bouquetov. Na novú dávku použi živý katalóg po zlúčení #40–#42. Starý počet nevyjadruje aktuálne chýbajúce stanice. Najbližší krok je porovnať nové alebo zmenené služby s presnými referenciami a grafikami v živých ZIPoch a prehodnocovať výnimky len s novým dôkazom.

### 6. 11. 2026 – Vhannibal PR #42 v produkcii

- Po výslovnom súhlase vlastníka zlúčený do FullHDGlass `main` ako [`2079d56`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/commit/2079d56bb8f3337d2196d055ea3938952dc91077). Pribudlo päť servisných referencií a oprava CHC-HD pod pôvodnou referenciou. Zmenilo sa 39 ZIPov. Všetkých 18 CANAL+ SK/CZ ZIPov zostalo bitovo identických.
- [Commit `7f87346`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/commit/7f87346c96879080dbbb15af677110c6d8cfc419) pridal reprodukovateľné zosúladenie registra. Na čistom checkoute vytvor aktuálny výstup príkazom `python tools/materialize-vhannibal-plans.py /tmp/plans.json`. Zdrojové rozhodnutia a dôkazy sú v [reporte PR](reports/vhannibal-six-resolutions-20261105).
- Pred zlúčením prešli SHA256 a CRC všetkých 39 zmenených ZIPov, všetkých deväť variantov pre šesť dotknutých referencií a test inštalácie cez kód prijímača. [OpenATV](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/42193202113) a [OpenPLi](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/42193202090) prešli spolu v šiestich úlohách. Po zlúčení sa verejný manifest a `SHA256SUMS` zhodovali s otestovaným kandidátom a SHA256 novej časti sedel pre každý z 39 ZIPov. Najbližší krok pre satelity je audit nových zmien oproti tejto produkcii.
