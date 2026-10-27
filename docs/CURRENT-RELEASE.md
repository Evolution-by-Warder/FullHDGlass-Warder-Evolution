# FullHDGlass Warder Evolution 1.0.27

- Opravené chýbajúce picony satelitných rádií, vrátane AAC staníc s RDS, v spodnom paneli aj rádiovom infobare.
- Čítanie pôvodného picon/ aj existujúcich starších picon_220x132/ a picon_400x240/, s prednosťou picon/. Žiadne presúvanie súborov ani nové priečinky.
- Vlastná presná zhoda piconu má prednosť. Keď sa nenájde, použije sa systémové vyhľadanie piconu podľa referencie alebo názvu stanice.
- DAB používa pôvodné systémové hľadanie bez zmeny; rozloženie, obaly a grafika zostávajú zachované.

Jedenásť regresných testov overuje AAC/štandardné rádio, prednosť vlastnej cesty, DAB, TV, prechod staníc, vymazanie a staršie image. Potvrdenie opravy na prijímači ešte čaká.
