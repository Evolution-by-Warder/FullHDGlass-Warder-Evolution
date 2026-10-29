# Rádio TEST2 — oprava záťaže GUI

Majiteľ po inštalácii TEST1 hlásil takmer neovládateľný prijímač po prepnutí na rádio. Výslovne schválil pohyblivú slučku pripravených snímok pri zachovaní jemných farebných stĺpcov a požiadal o minimálnu záťaž procesora. TEST1 nepoužívať; TEST2 čaká na overenie v boxe.

## Konkrétny problém

TEST1 zvýšil počet stĺpcov z 18 na 84 a frekvenciu z približne 9 na 20 snímok/s. Každý segment bol samostatný `eCanvas.fillRect`. V simulácii 30 sekúnd po zahriatí rendereru to znamenalo 895 742 volaní fillRect a 600 clear, približne 29 858 segmentov/s na jednu aktívnu inštanciu. OpenATV `lib/gui/ecanvas.cpp` vytvára pri každom fillRect samostatný gDC/gPainter a volá invalidate(rect). Toto je konkrétna výkonnostná regresia a pravdepodobná príčina hláseného zahltenia; meranie CPU na prijímači nemáme.

## Zvolená oprava

- Farby, geometria a priebeh pohybu sa vypočítajú na vývojovom PC skriptom `tools/build-radio-spectrum-frames.py`.
- Natívny `ePixmap` iba zobrazuje hotové priehľadné PNG. Najviac jeden setPixmap za 100 ms na aktívnu viditeľnú inštanciu; bez jednotlivých segmentov, trigonometrie alebo zvukovej analýzy v prijímači.
- 48 snímok sa prehráva dopredu a dozadu bez zdvojených koncov. Prechod slučky používa susedné snímky, takže pohyb nenaskočí na iný tvar.
- Snímky sa dekódujú postupne, najviac jedna za callback. Zdieľaná cache pre všetky tri natívne obrazovky má pevný limit 48 snímok, 8 467 200 bajtov RGBA pixelov plus malá réžia natívnych objektov. Samostatná globálna PNG cache je vypnutá. Po prvom cykle sa súbory znova nenačítavajú.
- Jednorazový timer sa znovu spustí až po práci; čas potrebný na pomalé dekódovanie sa nepridáva do fronty opakovaného časovača.
- onHide zastaví timer. Zmeny metadát nespúšťajú ďalšie kreslenie. Ak natívny rodič skryje obrazovku bez onHide, kontroluje sa viditeľnosť každých 500 ms bez načítavania a kreslenia, aby sa animácia mohla obnoviť aj na staršej RDS ceste.
- Chýbajúci alebo chybný voliteľný snímok zastaví animáciu bez opakovaných pokusov a súborových logov. Predchádzajúci dobrý obrázok ostáva.

## Zachovaný vzhľad a overenie

84 stĺpcov × 3 px, medzery 1 px, 2 px segmenty s rozstupom 3 px, pestré prechody a samostatné vrcholy; priehľadné pozadie; 350 × 126 px; pôvodné pozície v RadioInfoBar, RdsDisplay a RdsInfoDisplay. Prvý pripravený snímok bol pixel po pixeli porovnaný s TEST1 v tom istom bode simulácie a je zhodný.

Desať regresných testov overuje skutočné PNG, SHA256 a geometriu, jednu natívnu aktualizáciu za callback, zdieľanie cache, oba timer API, skrytého rodiča, záplavu metadát, pomalý loader, chybný snímok a spojitosť slučky. Po zahriatí v simulácii 30 sekúnd: 300 setPixmap, žiadne nové dekódovanie. Podrobné počty sú v `design/radio-spectrum/performance.json`; hostiteľské Python časy nemerajú natívny compositor ani CPU boxu.

Kontrola meria rozdiel vo vykresľovacom postupe, nie garantovanú percentuálnu záťaž prijímača. Pohyblivá grafika má nenulové náklady. Fyzicky treba overiť prepínanie TV ↔ rádio, odozvu ovládača, zoznam staníc a návrat animácie po menu. Produkčné feedy zostávajú nezmenené na 1.0.39.

Natívny postup overený v oficiálnom zdroji: https://github.com/openatv/enigma2/blob/master/lib/gui/ecanvas.cpp a https://github.com/openatv/enigma2/blob/master/lib/gui/epixmap.cpp.
