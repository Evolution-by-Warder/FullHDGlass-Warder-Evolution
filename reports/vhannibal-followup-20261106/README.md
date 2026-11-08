# Vhannibal – pokračovanie po PR #47

Produkčný základ je commit [`fd0a57d56d04e03d5e4560d718595fa5aa28e255`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/commit/fd0a57d56d04e03d5e4560d718595fa5aa28e255) po schválenom zlúčení PR #47. [Záznam opakovanej kontroly #47](pr47-recheck.json) obsahuje výsledky ZIPov a hashe všetkých 18 chránených balíkov CANAL+ SK/CZ.

## Mezzo SD

Presná referencia `1_0_1_37A0_44C_13E_820000_0_0_0` z registra zodpovedá 11411 H, SID 14240, TID 1100 a ONID 318 na Hot Bird 13°E. [Satindex](https://www.satindex.de/channel/40880/)

Vysielateľ vedie Mezzo a Mezzo Live ako dva odlišné programy. Pre Mezzo SD používame bitové kópie existujúcich deviatich PNG z referencie Mezzo TV `1_0_1_422B_2F44_13E_820000_0_0_0` na tej istej orbitálnej pozícii. [Mezzo](https://www.mezzo.tv/en/channels)

Deväť ZIPov prešlo SHA256 častí a výsledného archívu, CRC, kontrolou rozmerov a skúškou inštalačnej funkcie. Všetky pôvodné položky v týchto ZIPoch boli porovnané po bajtoch. Upravený manifest prešiel validátorom. [Hashové dôkazy](mezzo-proof.json)

## Zostávajúce prípady

V produkcii je technicky otvorených 120 referencií, z toho 118 s chýbajúcim variantom a dve chránené TV5MONDE s prázdnym PNG. Po prípadnom prijatí tohto kandidáta zostane 119 otvorených referencií, z toho 117 neúplných a dve chránené. [Evidencia všetkých 120 a krížová kontrola s existujúcim V9 indexom](remaining-review.json)

Z pôvodných 120 má 17 v existujúcom indexe V9 stav REVIEW a 103 je pozastavených. 2STV má doloženú zhodu služby na 11126 H so SID 1, ale jeho grafika je v REVIEW a nepatrí do tejto dávky. V9 návrhy a nejasné alebo chránené identity sa posudzujú samostatne. [KingOfSat](https://fr.kingofsat.tv/detail-2stv)


## 7. 11. 2026 — päť ďalších opráv na existujúcom PR #50

Overené main: FullHDGlass `3ba80ef8bb3b0ccd4148666372a9bf851ee85947`, PiconHub `8180aa0df6e185efad120338bc53ca04bc5e492a`. Pôvodný satelitný manifest produkcie sa oproti #47 nezmenil. PR #48 bol prečítaný ako starší rozpracovaný grafický checkpoint; jeho zdroje sa nestrácajú, jeho starý kandidát sa nepovažuje za produkciu.

- Nových päť opráv: Eurosport 2 HD (52E), Dom Kino Premium SD/HD (54.9E), SPORSMART (42E), Güneydoğu TV (42E). Presné referencie a donory sú v `batch-20261107.json`. Všetky PNG sú kópie existujúcich schválených grafík. Pri Güneydoğu ostáva pôvodná kompletná veľkosť 220×132 nezmenená; jej pixely sa zhodujú s donorom. V CANAL+ SK/CZ nie je vhodný Eurosport 2 donor; Eurosport 1 sa nesmie použiť.
- 27 nových zmenených ZIPov: `520E`, `549E`, `420E`, všetky tri rozmery × tri pozadia. Doplnených 42 PNG, 34 131 pôvodných členov bitovo identických. Spolu s Mezzo v PR #50: šesť referencií, 51 PNG, 36 ZIPov. `assets/warder/downloads/picons/channels/manifest.json` a `SHA256SUMS` sa aktualizujú len na pracovnej vetve.
- Mezzo znova prešiel SHA256 častí aj celých deviatich ZIPov, CRC, zachovaním všetkých 41 361 pôvodných členov, presnou zhodou PNG s donorom, rozmermi a skutočným aktuálnym inštalátorom. Nových 27 ZIPov prešlo rovnakou kontrolou a inštaláciou s neporušeným používateľským súborom. Všetkých 18 chránených archívov bolo znovu zostavených a overených SHA256/CRC; nezmenené.
- Pôvodných 120 otvorených: 6 opravených v kandidátovi, 3 doložené odchody presných referencií (Dijlah, Al Mawqef, 2STV), 111 zostáva aktuálne blokovaných. Nejde o nový plošný audit: pôvodný zdrojový súbor 14 808 referencií je zachovaný, upravuje sa len tento front. V aktuálnej snímke po zosúladení: 10 430 TV, 2 704 mimo rozsahu, 5 dátovaných odchodov vrátane pôvodných dvoch a 1 669 historických bez presnej aktuálnej zhody. Produkcia má stále 10 313 pokrytých; kandidát má 10 319. Publikovaných nových opráv v tomto behu: 0.
- Zo 17 REVIEW sú 4 opravené, 3 odišli a 10 zostáva: 2 BloombergHT (oficiálne SVG uložené v `sources/`, potrebuje V9 render a schválenie), 6 SIS/Betfred (aktuálne technické tuple potvrdené, chýba doloženie donorového aliasu), FUNBOX HD (nezamieňať s UHD/Fast&FunBox) a mesačný Kuukauden kanava. Zo 103 held sú Mezzo a Güneydoğu opravené; 101 držaných má dôvody v existujúcom `remaining-review.json`. Všetkých 28 held 23.5E má nulu presných zhôd v chránených balíkoch. TV5MONDE ani žiadne CANAL+ a Radio artworky sa nemenili.
- Ďalší krok: schválenie produkčného zlúčenia PR #50 samostatne; pracovné pokračovanie je oficiálny BloombergHT MASTER V9 návrh z uložených SVG a dôkaz priradenia šiestich SIS služieb. Nové grafiky sa nepovažujú za schválené. Žiadny merge, IPK ani publikácia neprebehli.
