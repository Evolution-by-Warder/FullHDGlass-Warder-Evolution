# FullHDGlass Warder Evolution 1.0.30

- Internetové rádiá používajú náš existujúci obal albumu a riadok interpreta/skladby v rádiovej obrazovke.
- Údaje sa prednostne čítajú z prehrávača OpenATV; chýbajúce údaje môže doplniť samostatné čítanie ICY metadát na pozadí.
- Čítanie metadát má limity objemu, časový limit a jedného spoločného pracovníka. Ovládanie a prehrávanie na sieť nečakajú.
- Prepnutie stanice zahodí oneskorený výsledok starého obalu. Neúplné údaje alebo nenájdený obal použijú existujúci neutrálny obrázok.
- Rozloženie a grafika rádia sa nemenia. Natívny RDS text a prednosť DAB MOT obrázkov zostávajú zachované.
- Ide o samostatnú Warder implementáciu inšpirovanú funkciou HDF Radio. Jeho binárne moduly, YouTube ani databáza staníc sa nepribaľujú.

Overenie: 22 automatických testov metadát, priebežné kontroly existujúceho balíka a verejných bajtov cez CI. Spojenie na tri živé streamy z pracovného prostredia skončilo časovým limitom. Fyzické overenie nového internetového rádia na prijímači sa zatiaľ netvrdí.
