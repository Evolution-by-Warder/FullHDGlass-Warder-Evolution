# Warder Evolution — spoločný štýl, revízia 1

Schválený smer: jedna vizuálna rodina pre PiconHub, nastavenia FullHDGlass a následne ostatné pluginy Warder Evolution. PiconHub 0.1.13 je referencia ovládania a farebnosti. Tento test upravuje nastavovaciu časť FullHDGlass 1.0.15 na pracovnej vetve; stabilné kanály zostávajú na 1.0.15.

## Spoločné pravidlá

- Pozadie #071627, panely #102136, tyrkysové línie #3ee8ff, výber #2a70ad, text biely a sekundárny text #b5d4ec.
- Červená #ff526a, zelená #39ff59, žltá #f5d54e a modrá #45b9ff. Farebné názvy tlačidiel sú samotné popisy akcií, bez prefixov „Červené:“ a podobne.
- Opakujúca sa hlavička: názov projektu, Warder Evolution, dátum, živý čas a menšie biele sekundy. Názov a logo zostávajú vlastné danému projektu.
- Nepriehľadné pozadia informačných a výberových okien, jednotný tyrkysový rám, vlastný viditeľný titulok a vycentrované farebné akcie.
- Výbery majú viditeľný kontrastný riadok a posuvník podľa potreby. Textové informácie používajú šípky a posuvník, bez samostatného nápisu Posun.
- Všetky súčasné možnosti, konfiguračné kľúče, hodnoty, callbacks, uloženie, zrušenie, aktualizácie a sťahovanie zostávajú funkčne zachované.

## Prvý testovací rozsah

Jeden súbor obsahuje hlavné menu aj skupiny nastavení. Hlavná obrazovka má TV náhľad vľavo, existujúcu nápovedu pod ním, menu vpravo a živé údaje v hlavičke. Rovnaký vizuálny rámec dostali sťahovanie, družice, štýly, extra obrazovky, ikony, história/výsledok, výber miest, editor miest a prehliadač priečinkov — spolu 11 tried obrazoviek.

Čas a dátum používajú existujúce natívne zdroje/konvertory skinu. Existujúce fonty v dátových riadkoch konfigurácie zostávajú kvôli kompatibilite; nové titulky a tlačidlá používajú systémový Regular.

## Hranice tejto etapy

Živý infobar, rádio, EPG, výber kanálov, fyzické umiestňovacie obrazovky, OLED súhrny, dekódovanie, sieťové operácie a aktualizačné kanály sa nemenia. Systémové MessageBox, ChoiceBox a InputBox zatiaľ používajú natívny skin image. Ich samostatné zjednotenie príde po overení vlastných nastavení na prijímači; nedochádza ku globálnemu prepísaniu dialógov celého Enigma2.

Existujúci význam farebných akcií je v tejto etape zachovaný, vrátane staršieho žltého uloženia v satelitnom multivýbere. Prípadné zjednotenie väzieb tlačidiel je samostatný funkčný krok s testovaním; prvý balík mení prezentáciu.

## Overenie a ďalší postup

Zmrazená kontrola AST potvrdzuje nezmenenú riadiacu logiku celého plugin.py po odfiltrovaní XML rozložení a farieb výberu v uvedených triedach. Samostatne sa kontrolujú pôvodné widgety, callback-kontrakty, dynamicky dopĺňané ikony, stiahnutie v 150 px okne a presúvanie päty histórie.

Na prijímači treba potvrdiť čitateľnosť, TV náhľad, všetky skupiny nastavení, uloženie/zrušenie, dynamické náhľady a farebné akcie. Až potom sa pokračuje systémovými dialógmi a ďalšími projektmi. Produkčné vydanie vyžaduje potvrdenie funkčnosti na prijímači.

## Oprava TEST252 po overení prijímačom

Úvodné menu má dva skutočne prepínateľné panely; všetky konfiguračné skupiny jeden veľký panel. V konfiguračnom režime sú oba úvodné panely a ich rámy skryté. Návrat obnoví rozdelenie. Samostatne testovaný prezentačný prepínač nemení akcie ani konfiguračnú logiku. AST normalizácia povoľuje iba jeho presné príkazy, bez zmeny pôvodného základného odtlačku.

## Schválená grafická hlavička — TEST260

Majiteľ schválil banner FullHDGlass by Warder odvodený od PiconHubu, so zmenšeným emblémom. Hlavička má 164 px; hlavná ponuka je posunutá o 32 px a ostatný obsah zostáva dostupný posúvaním. Pomocný obrázok zostáva 1029×350. Všetkých 11 vlastných nastavovacích tried má rovnaké pozadie hlavičky; malé ponuky ponechávajú veľkosti ovládacích prvkov a pôvodné absolútne súradnice všade, kde nezasahujú do hlavičky. Deň/dátum, čas/biele sekundy a tyrkysová verzia sú vpravo v troch stĺpcoch. Ide o natívne widgety nad statickým obrázkom, nie o súčasť bitmapy.

Pôvodná radio/grafická sada je naďalej chránená pôvodným digestom; jediný nový nastavovací obrázok má samostatný SHA256 v settings-header-asset.json. Zdroj, schválenie a presné zadanie vstavaného imagegen sú v SETTINGS-HEADER-SOURCE.md. TEST259 má prijímačom potvrdené zrýchlenie; nová grafika TEST260 zatiaľ čaká na overenie prijímačom.
