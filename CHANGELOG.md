## 1.0.91 — 24. november 2026

Plynulé rolovanie dlhých EPG popisov v druhom infobare a všetkých piatich režimoch informácií o programe. Obe polia sa posúvajú nezávisle po malých pixelových krokoch. Pridané ochrany pri skrytí a zatvorení okna a opravené voliteľné zdroje tlačidiel QuickMenu a InformationNetwork. Po inštalácii reštartujte Enigma2.

[Poznámky k vydaniu](docs/warder-1.0.91-release-notes.md).

## 1.0.90 — 24. november 2026

Obnovený výpis chýbajúcich ikon menu v /tmp/missing_menu_icons.txt bez duplicít. Opravená grafika FullHDGlass v menu Zoznam a ikony3. Dlhé popisy EPG sa automaticky rolujú vo všetkých piatich režimoch informácií o programe, pri aktuálnej a nasledujúcej udalosti nezávisle. Po inštalácii reštartujte Enigma2.

Podrobnosti: [poznámky k vydaniu](docs/warder-1.0.90-release-notes.md).

**OVERENÉ A PUBLIKOVANÉ:** PR #161, 18/18 CI, [publisher #45365758190](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/45365758190) SUCCESS. [Ostrý IPK](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/download/v1.0.90/enigma2-plugin-skins-fullhdglass_1.0.90_all.ipk), 18 811 074 B, SHA-256 `4c898a89e8d49f386bb62f75bc259e0a859d80e4fcb7c6d44c66766f4e7f0102`. Oba aktualizačné kanály 1.0.90.

## 1.0.89 – 23. november 2026

Vo výbere piconov pribudla samostatná položka DTT ITALIA s 285 stanicovými referenciami. Aktualizované sú aj talianske feedy na 9°E a 5°W. Vybrať si môžete zo všetkých troch rozmerov a pozadí. Po inštalácii reštartujte Enigma2.

## 1.0.88 — 2026-11-23 — oprava prekrytia natívnych nastavovacích posuvníkov

- Oprava nahlásená českým používateľom: v „Nastavení korekce obrazu“ a „Nastavení displeje“ prekrýval posuvník dlhý názov nastavenia. Príčinou bol krátky predvolený oddeľovací stĺpec v natívnom Enigma2 ConfigList pri veľkom písme FullHDGlass.
- Rozostup vo veľkých natívnych konfiguračných zoznamoch sa upravuje na 55 % ich šírky, so zachovaním najmenej 450 px pre hodnotu/posuvník; úzke pluginové okná, náhľady, systémový Enigma2 kód a vlastné nastavenia skinu sa nemenia.
- Vstupný kontrolný IPK 1.0.88-test1: 6/6 úzko zameraných testov, overený kontrolný súčet; PR #157 absolvoval kontroly OpenATV a OpenPLi pred prípravou stabilnej verzie.
- Vlastník výslovne nariadil zaradiť opravu do ostrej verzie. Opakované prijímačové vizuálne potvrdenie českým používateľom zatiaľ nemáme. Ostatné funkcie, grafika, picony, bezpečnostné opravy 1.0.87 aj nastavenia zostávajú zachované.
- **OVERENÉ A PUBLIKOVANÉ:** PR #157 zlúčený do `main`, 24/24 CI úspešných. Oficiálny [Release v1.0.88](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/v1.0.88) a [publikačný workflow #45252364033](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/45252364033) **SUCCESS**. IPK 18 394 974 B, SHA-256 `0da1f61a4e675ffc7b548d423430e9673230551d5bbc24e77598d5128d687c28`; oba feedy `update-production.json` a `update-test.json` ukazujú na 1.0.88. Podrobnosti: [poznámky 1.0.88](docs/warder-1.0.88-release-notes.md).

## 1.0.87 — 2026-11-23 — overené a publikované vydanie opravy SAT piconov

- Oddelená kontrola používateľských možností od bezpečnostnej validácie cieľovej cesty. SF8008 už bezpečne používa zachovaný picon alias `/usr/share/enigma2/hdg17_files/picon -> /usr/share/enigma2/picon`.
- Pri dostatku miesta na internej flash (512 MiB pracovná rezerva navyše k 64 MiB systémovej rezerve) je zbytočný potvrdzovací dialóg vypnutý. Pri nedostatku miesta alebo priveľkom archíve zostávajú všetky bezpečnostné kontroly aktívne.
- Prijímačové testy SF8008: 19,2°E 145 aktualizovaných PNG, 0 chýb; 23,5°E 184 PNG, výsledok „Stahování dokončeno“. Test upozornenia potvrdený vlastníkom.
- Schválený a zlúčený PR #156; 18/18 relevantných CI úspešných. Oficiálny publikovací workflow #45245269154 úspešne vytvoril IPK 1.0.87 a aktualizoval produkčný aj testovací feed s rovnakým SHA-256.
- Oficiálny Release: [v1.0.87](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/v1.0.87). Úplné poznámky: [docs/warder-1.0.87-release-notes.md](docs/warder-1.0.87-release-notes.md). Existujúce grafiky, picony, konfigurácia a migrácia zostávajú nezmenené.

## 1.0.72 — 2026-11-08 — receiver-approved IPTV/CAID release

- Fix missing IPTV video resolution with decoder fallback; preserve DVB behavior and dynamic dimensions.
- Prevent CAID text overlap with colored indicators in InfoBar 76; scroll full CAID/SID/VPID details seamlessly at 220 ms.
- Localize update release notes according to the Enigma2 system language (English fallback).
- Preserve existing settings, migration protections from 9.50 and previous Prime Time/EPG changes. Receiver validation: GigaBlue Quad 4K Pro, IPTV and DVB-S2 and movie player.
- Release notes: docs/warder-1.0.72-release-notes.md.

## 1.0.62-test1 — 2026-11-01 — isolated OpenATV 8.1 candidate

- Fix PicturePlayer caption sources and optional blue-caption binding, PiP dish Boolean/pixmap rendering, PositionerSetupLog native buttons and legacy Swap Label captions.
- Preserve all existing geometry, fonts, images, helpers and 1.0.61 behavior. Normal production remains 1.0.61; receiver confirmation of this candidate is pending.
- Add stable/beta/master native checks, typed skin binding inspection and native replay. Preserve the frozen original controller fingerprint through exact reviewed bitrate/adapter records.
- Public byte verification: reports/openatv81-candidate-public-20261101.json.

## 1.0.61 — 2026-11-01

- Promote owner-approved 1.0.60-test3 repairs: whole native list rows, safe single-line headers and complete graphical EPG timeline.
- Fix CoolTVGuide/CoolTinyGuide window framing and shorten wrapped event captions with an ellipsis without changing event data or detail descriptions.
- Provide correctly typed and live setup summary sources for receiver displays; preserve native SetupSummary behavior.
- Preserve the bound layout callback startup correction and all approved 1.0.59 runtime/artwork. Native package upgrade from test versions is supported.
- See docs/FULLHDGLASS-1.0.61.md and reports/stable61-public-20261101.json for the final package and update-channel evidence.

## 1.0.55 — 2026-11-01

- Repair shared DVB video/audio bitrate measurement and fast startup; retain starting status until a real nonzero sample.
- Include the exact receiver-approved ARM/MIPS32r2/AArch64 test5 helpers; remove the obsolete ARM helper and disable routine diagnostic logging.
- Preserve settings, package identity, DAB layouts and artwork. Version 1.0.55 upgrades normally from 1.0.53 and 1.0.54-test5.
- GigaBlue receiver confirmation covers FTA and encrypted services. MIPS and Dreambox hardware validation remains pending.

# 1.0.43 — 30.10.2026

Opravená moderná systémová virtuálna klávesnica: prompt, režim zadávania, jazyk, popisy tlačidiel a zhodná geometria 67 px. Povinná kontrola kompatibility voči overenému aj aktuálnemu OpenATV. Staršia klávesnica a ostatná grafika zachované.

# 1.0.42 — 30.10.2026

Zjednotené pomocné balíky v `assets/warder/downloads/`: nápoveda v `ui/help`, náhľady informačných panelov pri sadách ikon v `ui/icon-set-previews`. Odstránené paralelné umiestnenie v `design/preview-assets`; sťahovač aj zostavovanie používajú spoločnú štruktúru. Pomocné ZIP archívy sa neprikladajú k vydaniam IPK. Existujúce kontrolné súčty a cache ostávajú platné.

# 1.0.41 — 29.10.2026

Jemný farebný equalizér: 84 stĺpcov 3 px, medzery 1 px, priehľadnosť a pôvodné farby TEST2. Hotové snímky znižujú náklady na vykresľovanie rádia. Tichá prevádzka bez zbytočných automatických logov, upratovanie dočasných súborov a ohraničené RAM cache. Zachované nastavenia, texty, obaly, RDS/DAB a rádio zoznamy.

Produkčné povýšenie na výslovný pokyn vlastníka. Verzia 1.0.41 sa v správcovi balíkov radí nad 1.0.40-test2 bez vynucovania downgrade. Jasnejšie farebné návrhy neboli prijaté a nie sú súčasťou vydania.

# 1.0.40-test2 — 29. 10. 2026

- Oprava zahltenia GUI po prepnutí na rádio hláseného v TEST1.
- Jemný 3 px equalizér používa hotové priehľadné snímky cez ePixmap: jeden obrazový update za 100 ms, bez vykresľovania jednotlivých segmentov v boxe.
- Jednorazový timer sa obnoví až po práci; kontroluje aj viditeľnosť rodiča. Skrytie zastaví animáciu a zmeny metadát nepridávajú kreslenie.
- 48 snímok sa načítava postupne a zdieľa medzi obrazovkami, najviac 8.1 MiB RGBA pixelov. Žiadne pracovné zápisy, dekódovanie zvuku ani nová závislosť v prijímači.
- TEST1 nepoužívať; TEST2 čaká na overenie odozvy prijímača. Produkčný aktualizátor zostáva na 1.0.39.

# 1.0.40-test1 — 29. 10. 2026

Jemný farebný equalizér: 84 stĺpcov 3 px, medzery 1 px, priehľadné pozadie, plynulé farby. Vypnuté automatické diagnostické logy, opravené upratovanie dočasných súborov a ohraničené RAM cache.

# 1.0.39 — 29. 10. 2026

- Produkčné vydanie prijímačom potvrdeného TEST13: natívne texty a obaly rádiových skladieb.
- Funkčný SuperMusic bez tokenu, kanonické adresy skladieb a opätovné použitie verejnej relácie.
- Rozšírené SK/CZ zdroje, presné párovanie interpreta/nahrávky, opravy metadát a cache.
- Zachované schválené rozloženie, používateľské nastavenia, RDS/DAB a týždenný rádio zoznam.
- Verzia 1.0.39 umožňuje riadnu aktualizáciu aj z 1.0.38-test13.

# 1.0.28

- Zjednotené hľadanie piconov satelitného rádia v oboch ďalších variantoch infobaru, zachované ich časovače a animácie.

# 1.0.27

- Záložné systémové vyhľadávanie piconov satelitného rádia v g17PicRef pred použitím náhradného loga.
- Zachované vlastné picony, DAB a rádiové rozloženie; dvanásť regresných testov.

# 1.0.26

- Odstránené automatické zakladanie starých priečinkov piconProv_220x132, piconSat_220x132 a picon_220x132. Existujúce súbory sa touto zmenou nemažú.
- Čítanie kanálových piconov uprednostňuje pôvodný adresár picon aj pri starších rozmerových nastaveniach.
- Automatická kontrola aktualizácií pri každom otvorení konfigurácie beží mimo hlavného vlákna; ponuka a potvrdenie inštalácie zachované.

# 1.0.25

- Po úspešnej výmene balíkov sa obnoví aj zapamätaná cesta k logám zo starého adresára; nie je potrebný ručný reštart GUI kvôli tejto ceste.
- Opakované publikovanie bezpečne preskočí archívy, ktoré už boli odstránené.
- Obsah šiestich aktuálnych balíkov zostáva rovnaký ako pri zjednotení v1.0.24.

# 1.0.24

- Kompletné aktuálne picony providerov a satelitov vo všetkých troch pozadiach nahrádzajú pôvodné ZIP-y pod názvami piconProv.zip a piconSat.zip.
- Inštalácia používa pôvodné piconProv/ a piconSat/; existujúce zhodné kópie v adresároch s rozmerom sa odstraňujú až po úspešnom stiahnutí a porovnaní obsahu.
- Kanálové picony 220×132 sa sťahujú do picon/; zjednotené aj staršie mapovanie a načítavanie.
- Zachované aktuálne logá a opravy Canal+ SK/CZ; zostávajúce staré rozmery obrázkov normalizované pri zostavení balíkov.

# 1.0.23

- Jediný aktualizovaný balík Nápoveda `g17_setup_pict.zip` pre ručné stiahnutie aj automatické náhľady; pôvodné názvy obrázkov zachované.

- Natívne asynchrónne prepínanie pomocných náhľadov a vyčistenie starej nápovedy pri zmene výberu alebo chybe.
- Plne priehľadné okolie bublín; zachované texty a názorné ukážky.

# 1.0.22

- Jemná priehľadnosť pozadia všetkých pomocných bublinových obrázkov; text a názorné detaily bez zmeny.
- Alpha blending a nová revízia overovaného voliteľného balíka bez zväčšenia IPK.

# FullHDGlass Warder Evolution — zmeny

## 1.0.21 — 26. 10. 2026

Doplnená ochrana návratu z výberového dialógu: vlastný Pig renderer nedovolí zobraziť malé TV v nastaveniach ani pri natívnom onShow. Hlavná ponuka s LiveTV sa obnovuje normálne.

## 1.0.20 — 26. 10. 2026

Jemná priehľadnosť nastavovacích/výberových obrazoviek bez LiveTV podľa GSU; banner zostáva hore, zachované náhľady a geometria. Hlavné menu s malou TV sa nemení. Pri vstupe do nastavení sa Pig skryje a pri návrate obnoví. Výber a posuvníky majú nepriehľadné farby. Natívne zobrazenie čaká na potvrdenie používateľom.

## Staršie záznamy

# Changelog

## FullHDGlass Warder Evolution 1.0

- Established the Warder Evolution release line.
- Python 3 compatibility cleanup and syntax fixes.
- Safer installation and removal scripts.
- Repaired missing menu graphics.
- Removed obsolete duplicate legacy files and unsafe global HTTPS bypass.
- Reworked Enhanced Weather to use Open-Meteo JSON services.
- Removed the obsolete MSN weather fallback and modernized weather HTTPS access.
- Replaced the original FTP skin updater with the Warder GitHub update service.
- Added HTTPS package download, version comparison and SHA256 package verification.
- Migrated downloadable FullHDGlass runtime assets to the Warder GitHub asset catalog.
- Added SHA-256 verification for every downloaded Warder asset before extraction.
- Removed embedded legacy FTP credentials from the plugin.
- Removed the legacy rotating PayPal donation banner from the setup header.
- Preserved original FullHDGlass author credits; Warder identifies only the Evolution continuation and new maintenance work.
- Preserved the existing external satellite/channel picon download path for categories not supplied by the Warder asset catalog.
- Kept the package identity `enigma2-skin-fullhdglass17`, so an existing FullHDGlass installation is upgraded in place and remains registered in the system package manager.
- Kept `/usr/share/enigma2/hd_glass17/skin.xml` as the standard Enigma2 skin entry, so FullHDGlass remains available in Skin Setup / appearance selection.
- Preserved `/etc/enigma2/settings`, `/etc/enigma2/skin_user.xml`, and the generated FullHDGlass user overlay during upgrades.
- Marked `/etc/enigma2/skin_user-hdg17.xml` as a package configuration file and prevented removal cleanup from running during upgrade transitions.
