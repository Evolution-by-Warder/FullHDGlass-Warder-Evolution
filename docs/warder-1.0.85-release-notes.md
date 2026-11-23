# FullHDGlass – Warder Evolution 1.0.85

**Ostré opravné vydanie, 23. novembra 2026.** Nadväzuje na 1.0.84. Vlastník fyzicky overil na GigaBlue Quad 4K Pro s OpenATV 8.1 + GLES postup `14 → 9 → 14` zobrazovaných kanálov a správne rozloženie piconov, názvov staníc a EPG. Vo vydaní je schválený aj finálny riadok „Máš zvolené“, vrátane celej hodnoty `HDD/SSD: /dev/sda`, potvrdený na prijímači s TEST3. Toto nie je tvrdenie, že bol fyzicky otestovaný každý model Solo 4K, OpenPLi či každá iná obrazovka.

## Opravené zobrazenie staníc a EPG

- Pri zmene počtu riadkov natívneho výberu staníc sa znova synchronizujú rozmery piconov, výška položiek a hranice textových buniek. Predošlá chyba: po zmene `14 → 9` sa výška riadkov prepočítala, no picony a texty sa opravili až po zatvorení a opätovnom otvorení zoznamu.
- Vlastný renderer `WarderChannelEpgClip` rešpektuje aj rezervovanú šírku číselného stĺpca natívneho `ServiceListLegacy` pri číslovaných bouquetoch. Dlhé názvy relácií zostávajú v správnom priestore bez prekrytia názvu stanice.
- Rolovanie dlhých názvov EPG **ostáva dostupné a zapnuté podľa existujúceho nastavenia**; na obrazoch bez podporovaného GLES zostáva bezpečný natívny režim. Zachované sú farebné indikátory, Prime Time, veľkosti písma a picony.

## Nastavenia piconov a diagnostický riadok

- V spoločnom natívnom okne `Setup` je viac priestoru pre dlhšie vysvetlenie režimov vyhľadávania piconov: opis má 120 px namiesto 80 px. Výber ciest a farebné tlačidlá zostali na svojich miestach.
- Horný riadok **„Máš zvolené“** ponecháva pôvodné číslo Infobaru, typ ikon, sadu ikon menu, ikony počasia a HDD/SSD; pridáva **Menu: N** (vlastné poradové číslo typu menu, predvolené `1`), číslo typu výberu kanálov, stav rolovania EPG/GLES a parametre písma pre názvy/EPG/riadok.
- Riadok zostáva **jediný**, posunutý na `x=15`, široký `1890 px` s fontom `Regular;23`. Po fyzickom teste TEST3 sa celý údaj `/dev/sda` zobrazuje bez odrezania.
- Diagnostika je len na čítanie a nijako neprepisuje konfiguráciu prijímača.

## Kompatibilita a zachované údaje

- Predchádzajúce opravy 1.0.84 pre OpenATV 7.6, OpenPLi 9.2 a Warder Radio Live zostávajú zachované.
- Bez zmeny originálnych obrázkov, SAT piconov, rádiových log, dátových balíkov a používateľských nastavení; voľba grafiky, úložiska a služieb zostáva nedotknutá.
- OpenATV a OpenPLi matice kompatibility, testy EPG geometrie, natívneho režimu, konfiguračných väzieb a produkčné zostavenie sú podmienkou vydania. Fyzické overenie dlhšieho textu v natívnom Picon Setup na Solo 4K nebolo samostatne doložené.

## Vydanie, aktualizácia a bezpečný návrat

- Oficiálny balík: `enigma2-plugin-skins-fullhdglass_1.0.85_all.ipk`.
- Vydávací postup: schválený PR [#151](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/151), následná príprava verzie a kontrola `publish-warder-stable.yml`; SHA-256 finálneho vydaného balíka sa zaznamená až po produkčnom buil­de.
- Výsledný balík sa distribuuje cez oficiálny Release a `update-production.json`/`update-test.json`; starý migračný most `update.json` pre 1.0.18 musí zostať bezpečný.
- Po aktualizácii **reštartujte Enigma2**. Pri návrate na staršiu verziu skontrolujte kompatibilitu opkg a aktuálneho image.
