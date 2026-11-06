# Vhannibal – pokračovanie po PR #47

Produkčný základ je commit [`fd0a57d56d04e03d5e4560d718595fa5aa28e255`](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/commit/fd0a57d56d04e03d5e4560d718595fa5aa28e255) po schválenom zlúčení PR #47. [Záznam opakovanej kontroly #47](pr47-recheck.json) obsahuje výsledky ZIPov a hashe všetkých 18 chránených balíkov CANAL+ SK/CZ.

## Mezzo SD

Presná referencia `1_0_1_37A0_44C_13E_820000_0_0_0` z registra zodpovedá 11411 H, SID 14240, TID 1100 a ONID 318 na Hot Bird 13°E. [Satindex](https://www.satindex.de/channel/40880/)

Vysielateľ vedie Mezzo a Mezzo Live ako dva odlišné programy. Pre Mezzo SD používame bitové kópie existujúcich deviatich PNG z referencie Mezzo TV `1_0_1_422B_2F44_13E_820000_0_0_0` na tej istej orbitálnej pozícii. [Mezzo](https://www.mezzo.tv/en/channels)

Deväť ZIPov prešlo SHA256 častí a výsledného archívu, CRC, kontrolou rozmerov a skúškou inštalačnej funkcie. Všetky pôvodné položky v týchto ZIPoch boli porovnané po bajtoch. Upravený manifest prešiel validátorom. [Hashové dôkazy](mezzo-proof.json)

## Zostávajúce prípady

V produkcii je technicky otvorených 120 referencií, z toho 118 s chýbajúcim variantom a dve chránené TV5MONDE s prázdnym PNG. Po prípadnom prijatí tohto kandidáta zostane 119 otvorených referencií, z toho 117 neúplných a dve chránené. [Evidencia všetkých 120 a krížová kontrola s existujúcim V9 indexom](remaining-review.json)

Z pôvodných 120 má 17 v existujúcom indexe V9 stav REVIEW a 103 je pozastavených. 2STV má doloženú zhodu služby na 11126 H so SID 1, ale jeho grafika je v REVIEW a nepatrí do tejto dávky. V9 návrhy a nejasné alebo chránené identity sa posudzujú samostatne. [KingOfSat](https://fr.kingofsat.tv/detail-2stv)
