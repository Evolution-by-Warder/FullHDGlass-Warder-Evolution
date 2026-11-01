# FullHDGlass 1.0.54-test2

Diagnostický testovací balík pre zostávajúcu chybu nulového video bitrate.

Prvá oprava spúšťania merania ostáva zachovaná. Na GigaBlue sa meranie spustí, zvuk ukazuje hodnotu, video však zostáva na 0 kb/s aj na FTA stanici. Táto zostávajúca chyba zatiaľ nie je vyriešená.

Balík zaznamená skutočné argumenty pomocného programu, jeho SHA256, PID-y a demux pri spustení aj pri prijatých vzorkách a surové číselné výsledky. Záznam má najviac 24 udalostí a zapisuje sa do /tmp/fullhdglass-bitrate.json. Nepíše prihlasovacie údaje, streamovacie URL ani obraz alebo zvuk.

Po inštalácii reštartujte GUI. Prepnite na TV stanicu, nechajte ju približne 30 sekúnd hrať a skopírujte uvedený súbor. Pre vyhodnotenie ho pošlite ešte pred ďalším prepnutím stanice (nové meranie záznam prepíše).

Verzia je určená na diagnostiku; verejné aktualizačné kanály sa nemenia. Pôvodné IPK ostávajú nezmenené.
