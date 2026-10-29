# FullHDGlass Warder Evolution 1.0.40-test2

Oprava vážneho spomalenia po prepnutí na rádio v TEST1. **TEST1 nepoužívať.**

Schválený vzhľad zostáva: 84 stĺpcov 3 px, medzery 1 px, farebné segmenty a vrcholy, priehľadné pozadie, rozmer 350 × 126 px a pôvodné pozície.

Namiesto tisícov eCanvas operácií za sekundu sa zobrazujú hotové snímky cez ePixmap. Najviac jeden update za 100 ms; jednorazový timer sa obnovuje až po práci. Snímky sa postupne načítajú iba raz do zdieľanej RAM cache (48 snímok, 8.1 MiB RGBA pixelov). Pri skrytí animácia stojí; skrytý natívny rodič nespúšťa dekódovanie ani kreslenie. Prijímač nevypočítava farby či segmenty, nevytvára pomocné súbory a nepotrebuje Pillow. Animácia je krátka plynulo obojsmerná slučka, nie analýza zvuku.

Predchádzajúce opravy logov, cache a dočasných súborov ostávajú. Izolovaný testovací balík; produkčný aktualizátor zostáva na 1.0.39. Testy merajú počet natívnych operácií a simulujú životný cyklus; oprava ešte vyžaduje potvrdenie odozvy priamo v prijímači.
