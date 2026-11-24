# Warder Evolution – bezpečná retencia vydaní

**Nové pravidlo vlastníka: 23. 11. 2026 (nadradené staršej politike piatich vydaní).** V distribúcii a v aktuálnych zdrojových balíkoch ponechať **najnovšie ostré vydanie a najviac tri predchádzajúce ostré vydania** každého programu. TEST/RC nie sú ostré verzie. Nemaže sa Git história, tagy, zdrojové testy, schválené grafiky, manifesty dát, používateľské súbory ani Trezor.

V produkčnom priečinku FullHDGlass `main/packages/` sú po vydaní 1.0.91 štyri stabilné verzie **v1.0.91 / v1.0.90 / v1.0.89 / v1.0.88**. Historická chýbajúca 1.0.81 nie je ostrým vydaním v tejto štvorici.

## Povinné migrácie a výnimky

- **Legacy 1.0.18:** `update.json` je bootstrap zo starej `enigma2-skin-fullhdglass17` identity. `preinst` aktuálnej identity výslovne blokuje neoverený skok; preto musí pôvodná 1.0.18 zostať dostupná, kým všetky podporované staré inštalácie prejdú bezpečne do ostrého vydania. Číslo 1.0.18 sa nezapočítava do štyroch ostrých rollbackov.
- **Legacy TEST 1.0.72:** produkčný kód pre staršie `-test` inštalácie používa `warder-modernization-work/update-test.json`, ktorý na 1.0.72 naďalej odkazuje. Tento súbor zatiaľ zostáva v `main/packages/`, kým sa testovacím klientom bezpečne zmení cesta. Nie je to piate ostré vydanie.
- **História presmerovania main TEST feedu pri vydaní 1.0.86:** `main/update-test.json` prechádza zo zastaranej 1.0.69 na rovnaký overený package URL/SHA ako `update-production.json` (1.0.86). Starý `update.json` zachováva 1.0.18, ale už uvádza následnú produkčnú 1.0.86; jeho prepis na nové meno IPK by mohol poškodiť staré prijímače.

## Vydávanie a automatické prerezávanie

`publish-warder-stable.yml` overí zdroj, syntaktiku, existujúce regresie, celé IPK/SHA a nemenný GitHub Release. Až potom publikuje `update-production.json` a `update-test.json` s rovnakou overenou verziou a vykoná `tools/retain-fullhdglass-stable.py --apply`. Tento nástroj odmieta osirelé SHA, neočakávanú identitu, nepripravený legacy bootstrap, nesúlad test/stable feedu alebo chýbajúce štyri ostré dvojice. Zostávajú len štyri ostré verzie a doložené výnimky. Nevyvoláva sa vydanie pri samotnej zmene workflowu; novú ostrú verziu spúšťa zmena zdrojovej verzie/control alebo vedomý dispatch.

Staršie GitHub Releases / TEST artefakty môžu byť odstránené **iba po** nezávislej kontrole aktívnych URL, feedov, inštalačných závislostí a možnosti obnovy. GitHub Release, release asset a tag sú tri odlišné veci. Nikdy neodstráň fungujúci rollback bez náhrady; historické vydanie z Git histórie nie je náhradou za aktívnu aktualizačnú adresu. Pri nemožnosti overiť aktívne odkazy ponechaj označenú výnimku. Súkromné/originálne FTP zálohy sa nemenia.

**Bodový inventár 23.11.2026:** `main/packages/` pôvodne obsahoval 61 položiek, z toho 48 súborov (24 starých dvojíc IPK+SHA) bolo identifikovaných ako kandidáti na odstránenie po kontrole a presmerovaní aktívnych feedov. Presné počty odstránených položiek, zmenené HEAD a výsledky testov udržiava jediný `docs/ECOSYSTEM-CLEANUP-CHECKPOINT-20261123.md`, nie tento historický inventár.
