# FullHDGlass Warder Evolution — TEST263

Menší základný inštalačný balík so zachovaným svižným menu.

- Veľké archívy náhľadov nápovedy a typov infobaru sa nepribaľujú do IPK.
- Pri otvorení konfigurácie sa chýbajúce archívy sťahujú v samostatnom vlákne do `.warder-previews` vo vybranom dátovom priečinku skinu.
- Stiahnuté súbory sa overia podľa veľkosti a SHA256, až potom atomicky nahradia cache. Rozpracované alebo chybné sťahovanie sa nepoužije.
- Existujúce originálne obrázky zostávajú podporované. CPU príprava náhľadov pokračuje v oddelenom procese, s posledným vybraným riadkom ako prioritou.
- Bez internetu zostáva nastavenie použiteľné; už uložené náhľady fungujú bez siete. Chýbajúce náhľady sa doplnia na pozadí a použijú pri ďalšom výbere alebo otvorení ponuky.
- Zachovaný názov Konfigurácia FullHDGlass Warder Evolution a menšia lebka v ikone z TEST262.

Balík sa kontroluje s pevným limitom pod 16 MiB; veľké ZIPy sú samostatné aktíva vydania. Kontroly nenahrádzajú fyzické overenie na prijímači. Používateľ výslovne schválil zaradenie TEST263 do aktualizácie priamo z konfigurácie skinu. Stav aktívnych kanálov určujú update.json a update-test.json.
