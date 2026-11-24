# DTT ITALIA a talianske feedy – kontrolná dávka 23. novembra 2026

## 24. 11. 2026 – prílohy Azzurra v SAT manažéri

**Živé overenie zastavené na prihlasovacej stránke.** GitHub Actions na commite `4206c46` dostal z adresy `/cms/login/` odpoveď HTTP 403 ešte pred odoslaním formulára. Predchádzajúci test štandardným HTTP formulárom nepotvrdil členskú reláciu. Živý test GitHub Actions nepotvrdil prihlásenie ani stiahnutie kontrolného PNG s ID 151974. Produkčné balíky a posledný úspešný checkpoint zodpovedajú predchádzajúcemu vydaniu. Vlastník schválil zlúčenie po úspešnom živom teste. [GitHub Actions](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/actions/runs/45344778658) · [Implementácia v PiconHube](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/pull/88)

Implementácia a regresné testy sú v [pracovnom commite PiconHubu](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/commit/8e0ef1c4563b6acee1ebc16dec7d154f6e253af4). Prešlo 27 lokálnych testov skenerov a príloh. Prenos checkpointu prešiel pri prvom zápise, následnom prírastku aj opakovanom behu bez zmeny.

Integračný test pracovného commitu `c89abc0` úspešne načítal oba repozitáre a pripravil checkpoint. Pri otvorení prihlasovacej stránky skončil s `login_page_HTTP_403`. Beh nevytvoril žiadny artefakt ani dátovú vetvu. Samostatná regresia skenerov vykonala 27 testov. Všeobecná sada eviduje 249 testov, z nich jeden preskočený. Obrazový test prešiel v cielenej sade s knižnicou Pillow. Prešli aj kontroly OpenPLi a ochrany log. [Integračný beh](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/actions/runs/45346332798) · [Regresia skenerov](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/actions/runs/45346343488) · [Všeobecná sada](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/actions/runs/45346343448).

Východiskom je 483 príloh z registra FullHDGlass, SHA-256 `2ee27e9cab46eab8467a3de9ce790c17d6dd08f385a904a2378a7a68aabdd456`. Živý oficiálny archív Vhannibal Motor DTT Italia má SHA-256 `b44bc9affcc9f9263f8a77fd9391387fa6865f15645fcef12a08462b8dad20de`. Porovnanie bouquetov a lamedb potvrdilo 285 referencií DTT, 439 na 9°E a 260 na 5°W. Pravidelná úloha Warder SAT Picon Manager bola pri kontrole pozastavená. Po obnovení má ďalší termín 3. 12. 2026 o 08:00 Europe/Bratislava a dvojtýždňový interval.


## 23. 11. 2026 — DTT ITALIA a talianske feedy 9°E a 5°W sú overené a publikované

[FullHDGlass 1.0.89](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/v1.0.89) a [PiconHub 0.1.45](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/releases/tag/v0.1.45) sú dostupné cez produkčné aktualizátory. Pre každú aplikáciu boli skontrolované verejný IPK, jeho kontrolný súčet, verzia v metadátach opkg a obsah inštalovaného výberu. FullHDGlass má zhodný produkčný a testovací kanál. PiconHub má zhodné aktualizačné údaje na `main` a na kompatibilnej vetve `plugin/futuristic-rebuild`.

| Vydanie | Veľkosť IPK | SHA-256 verejného IPK | Oficiálne zostavenie |
| --- | ---: | --- | --- |
| [FullHDGlass 1.0.89](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/download/v1.0.89/enigma2-plugin-skins-fullhdglass_1.0.89_all.ipk) | 18 395 176 B | `50dd57e5e525688d7327c7915f6dfe1a9a5609f773ce017e87546b138cf53425` | [priebeh vydania](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/45271414450) |
| [PiconHub 0.1.45](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/releases/download/v0.1.45/enigma2-plugin-extensions-piconhub_0.1.45_all.ipk) | 3 038 080 B | `83758c52c4d5d6675183865239b0e38e9cc0e83340c378f5b2ed7e467adc9d45` | [priebeh vydania](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/actions/runs/45271765476) |

Opätovné stiahnutie z produkcie overilo 181 dielov a 27 archívov. V 891 väzbách servisná referencia / variant sa všetkých 405 schválených PNG zhodovalo s odtlačkami uloženými pri schválení. Katalóg v PiconHube má rovnaký SHA-256 ako živý katalóg FullHDGlass, `40db67977de066be65fa8f37f5a73041aa1b337b7a5c9cdf40233edaf537094a`.

**Grafika schválená vlastníkom 23. novembra 2026.** Vlastník po prezretí troch náhľadových hárkov prijal všetkých 45 výsledných sád, vrátane 80 označených kombinácií na bielom a čiernom podklade. [Záznam schválenia a odtlačky 405 výsledných PNG, troch náhľadov a 27 ZIP](owner-approval.json). Pôvodné hodnotenie MASTER V9 v matici zachytáva stav pred rozhodnutím vlastníka.

| Výber | Referencie v bouquetoch | Nové PNG naprieč 9 variantmi | Nahradené PNG | Zachované PNG zo starých balíkov |
| --- | ---: | ---: | ---: | ---: |
| DTT ITALIA | 285 | 2565 | 0 | 0 |
| 9°E | 439 | 9 | 399 | 18411 |
| 5°W | 260 | 0 | 102 | 13245 |

Rozmery sú 50×30, 220×132 a 400×240, pozadia Transparent, White a Black. Počty v stĺpcoch PNG zahŕňajú všetkých deväť variantov. Každý pôvodný člen mimo zmien má zhodný obsah. Katalóg obsahuje 507 balíkov a 2224 častí. SHA-256 spoločného manifestu je `40db67977de066be65fa8f37f5a73041aa1b337b7a5c9cdf40233edaf537094a`.

## Pôvod a porovnanie

- [Vlákno Azzurra](https://www.linuxsat-support.com/thread/157954-picons-dtt-italia-by-azzurra/) malo 10 strán a 183 príspevkov. Posledný bol zo 17. novembra. Vlákno ponúka jednotlivé aktualizácie. Z 483 príloh malo 480 názov končiaci na PNG. Pri dekódovaní boli tri z týchto súborov WebP. [Zoznam príloh s SHA-256](attachments.json).
- Nastavenia **Vhannibal Motor Dtt Italia 22 nov 2026** majú SHA-256 `b44bc9affcc9f9263f8a77fd9391387fa6865f15645fcef12a08462b8dad20de`. Z lamedb sa použili skutočné identifikátory služby, multiplexu, siete, typ služby a úplný namespace. Bouquety 01, 59/60 a 81/82 určujú taliansky rozsah. DTT používa 267 referencií s `EEEE0000` a 18 s `EEEE0272`. Na 9°E a 5°W sa zachovali aj pôvodné stanice mimo týchto bouquetov. SHA-256 porovnávacej sady Vhannibal Motor je `27e9ca4f15d62f00a1fa9365e69b702eb828dbee0d634f2495da3954f661bc8d`.
- Pre 885 z 984 väzieb sa použila existujúca deväťvariantová grafika Warder. Ďalších 99 väzieb používa 48 odlišných zdrojových grafík. [Matica referencií, dôkazov, zdrojov a kontrol MASTER V9](recipe.json). Pri Radio Classica TV sa použil originál od vysielateľa. [Radio Classica](https://www.radioclassica.fm/img/logo-radioclassica-mifi.png)
- [Výsledok zostavenia vrátane SHA-256 každého ZIP](build.json) a [skúšky oboch klientov](clients.json). FullHDGlass použil skutočný inštalátor pri 27 archívoch. PiconHub vykonal 54 inštalácií do dočasného adresára. Kontrola overila výber balíka, zhodu nainštalovaných PNG a ochranu cudzej pozemnej referencie. Aktualizovaný manifest prijali aj oba doterajšie validátory. Fyzický prijímač nebol súčasťou testu.

## Schválené náhľady

Každá skupina zobrazuje Transparent, White a Black na rozmere 220×132. Originál je v ZIP-e pod SHA zdroja v priečinku `artwork/`. Pole `variants_from` pri troch duplicitách odkazuje na spoločnú sadu všetkých rozmerov.

![Náhľad grafík 1 až 20](preview-1.jpg)

![Náhľad grafík 21 až 40](preview-2.jpg)

![Náhľad grafík 41 až 45](preview-3.jpg)

## Opätovné zostavenie

Vstupom je katalóg FullHDGlass v revízii `3597e077e7808997cc18542c6d57a8f1304f98d4` s časťami balíkov pre 9°E, 5°W a 13°E. Stavba pred použitím overí SHA-256 každého dielu a archívu. Príkazy sa spúšťajú z koreňa FullHDGlass, cesta `../PiconHub` odkazuje na sprievodnú zmenu PiconHubu.

```sh
python3 tools/build-dtt-italia.py --input ../povodny-katalog --output ../taliansky-kandidat --report ../zostavenie.json
python3 tools/test_dtt_italia_clients.py --hub ../PiconHub --channels ../taliansky-kandidat --report ../skusky-klientov.json
```

Odkazy v manifeste majú produkčný formát, ktorý kontrolujú oba klienty. Pred vydaním sa diely kontrolujú zo zhodnej revízie tejto vetvy. Hlásenia o nových príspevkoch Azzurra spracuje existujúci dvojtýždňový SAT skener PiconHubu.

## Nezávislé overenie uložených výsledkov

Z pracovnej revízie FullHDGlass `f903ec11c9ccbab0316894b5a152c1b9a1b77311` sa znova stiahlo všetkých 181 dielov. Pri každom sa overila dĺžka a SHA-256 a po ich spojení aj SHA-256 všetkých 27 archívov. Stiahnutý manifest bol bajtovo zhodný s lokálnym výstupom aj s kópiou v PiconHube `af01ddd3f10a87471f77b89ec100a845ccedbd26`. Druhé zostavenie z pôvodných vstupov dalo rovnaký manifest, index SHA256SUMS a report s 27 hashmi. Pri 220×132 majú talianske a existujúce SK/CZ sady vo všetkých troch pozadiach nula spoločných referencií.

Všetkých 241 testov PiconHubu prešlo. Prešli aj jeho GitHub kontroly balíka, OpenATV a OpenPLi. Katalógová regresia zachytáva zmenu akéhokoľvek z ostatných 480 balíkov a ich metadát. Dve kontroly FullHDGlass pôvodne očakávali presný odtlačok predchádzajúceho katalógu. Dostali odtlačky nezávisle overeného výsledku. Stav CI je pri [FullHDGlass #158](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/158) a [PiconHub #87](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/pull/87).

## 24. 11. 2026 – porovnanie verejného sťahovania a prihlasovania

Pri pôvodnom získaní sa podľa záznamu z 23. novembra otvorilo vlákno Azzurra z jednej relácie Cloud Browsera ako hosť. Historický register obsahuje 483 záznamov s ID, odkazom na príspevok a SHA-256. Jeden záznam má prázdne pole názvu. Záznamy nedokladajú úspešné prihlásenie na LinuxSat, presnú verziu vtedy použitého prehliadača ani presný príkaz, ktorým sa všetky kópie uložili na disk.

24. novembra Cloud Browser Chrome pri zadanom vlákne zobrazil tlačidlo Login a odkaz na obrázok v príspevku 790931. Odkaz pre hosťa smeroval na `/cms/file-download/151974/`. Po výbere odkazu použil Cloud Browser príkaz downloadMedia. Prvý testovací súbor PNG mal 21 689 B a SHA-256 `f2c1d4f903b5e29c39fd86d1c0006f239f5a5a5b0dd0a2237deb329a6d6ee70e`, ktorý sa presne zhodoval s registrovaným odtlačkom. Pred prihlásením ponúkalo fórum adresu `/cms/login/` s návratom do vlákna v parametri `url`.

Na GitHub Actions sa prvý test zastavil pri otváraní `/cms/login/` ešte pred odoslaním formulára. Pri druhej skúške sa pôvodný verejný vstup testoval z hostovaného runnera v samostatnom kroku bez poverení. Už prvé otvorenie vlákna vrátilo `public_thread_HTTP_403_challenge` a krok skončil ešte pred sťahovaním. Presnú podmienku, ktorú použil server pre prvú neúspešnú požiadavku, verejné výstupy neuvádzajú. [Prvý test](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/actions/runs/45346332798) · [Test verejného vstupu](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/actions/runs/45348061001).

Pravidelný SAT manažér má pre tento zdroj nastavené volanie GitHub Actions po schválení produkčnej integrácie. API úlohy uvádza pre prostredie hodnotu `inherited` a neuvádza, či má počas naplánovaného behu vlastný Cloud Browser. Včerajšie ani dnešné jednorazové stiahnutie nezaručuje splnenie podmienok produkčného kroku. V pracovnej vetve rozlišuje voľba `public-link` verejnú kartu a voľba `proof` členskú reláciu. Pri odmietnutí alebo výzve na overenie má produkčný krok jediný výsledok `SOURCE_ERROR_NO_ADVANCE`.
