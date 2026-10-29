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
