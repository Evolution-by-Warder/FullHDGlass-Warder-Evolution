# FullHDGlass Warder Evolution 1.0.32

- Zachovaná kontrola interpreta aj skladby. Iný duet sa nevyberá iba preto, že obsahuje rovnakého speváka; samotná prítomnosť obalu nie je dôkazom správnej zhody.
- Opravené opačné poradie metadát vysielateľa: „Uncovered Paradise – Ukitas“ sa rozpozná ako skladba „Uncovered Paradise“ od Ukitas, iba ak sa presne zhodujú oba celé údaje.
- Pre nahrávky nenájdené v obchode je doplnený MusicBrainz a Cover Art Archive: presná identita interpreta a skladby, obal patriaci priradenému vydaniu, iba schválená predná strana. Nežiadané live/remix/karaoke verzie sa odmietajú.
- Chybné stiahnutie obrázka neukončí celé hľadanie. Obrázky majú limit 4 MiB a časový limit; odpovede katalógov majú limit 1 MiB.
- Neúspešné hľadanie sa pre aktuálnu skladbu zopakuje najviac raz, po 15 sekundách. Prepnutie stanice stále zahadzuje staré výsledky.
- Vyhľadávanie zostáva na pozadí. Vzhľad rádia, RDS a prednosť DAB MOT zostávajú zachované.

Overenie: 45 automatických testov vrátane zamietnutia inej verzie s hosťujúcim interpretom, inej skladby/čiastočného mena, väzby archívneho obalu na vydanie a obmedzeného opakovania. Živý Cover Art Archive v pracovnom prostredí vrátil schválený predný obal pôvodného albumu. Živá požiadavka MusicBrainz bola z tohto prostredia nedostupná; funkčnosť celej cesty na prijímači sa zatiaľ netvrdí. Úplné zostavenie a overenie verejných bajtov vykoná CI pred aktiváciou aktualizácie.
