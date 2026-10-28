# FullHDGlass Warder Evolution 1.0.35

- Samostatné informačné správy internetového rádia, napríklad „Hudba na maximum“, sa zobrazujú v existujúcom spodnom riadku vedľa loga aj bez interpreta a skladby.
- Zachované sú natívne značky prehrávača aj správy ICY. Aktuálna natívna správa má prednosť pred skladbou uloženou z predchádzajúceho čítania ICY.
- Pri návrate k skladbe sa riadok aktualizuje; prázdne údaje odstránia starý text. Slogan bez údajov o skladbe nespustí vyhľadávanie obalu.
- Natívne DVB/RDS, DAB MOT, rozloženie a grafika zostávajú zachované.

Overenie: 64 automatických testov vrátane prechodov skladba → správa → skladba → prázdny text. Kompletné CI overí balík pred aktiváciou produkčnej aktualizácie. Fyzické overenie na prijímači sa zatiaľ netvrdí.
