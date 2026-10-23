# FullHDGlass Warder Evolution — TEST258

Opravuje prijímačom nahlásené nedostatky TEST257.

- Spodný panel s opakovanou hodnotou je odstránený zo všetkých konfiguračných skupín. Nemá žiadny vykresľovaný widget; medzi tlačidlami nie je náhradná plocha. Interný dátový zdroj zostáva kvôli kompatibilite callbackov.
- Náhľad je väčší: 1029×350 namiesto 794×270, so zachovaným pomerom strán. Horná časť zobrazuje deväť riadkov a ostatné voľby sú dostupné posúvaním. Nápoveda má vlastný dostatočne veľký priestor a odstup od rámu.
- Žiadny pixel pôvodného pomocného obrázka sa neodstraňuje. Všetky obrysy a pôvodná priehľadnosť zostávajú zachované; spoločné čierne pozadie dostáva tmavomodrý tón. Vnútorné náhľady obrazoviek, texty a šípky zostávajú zachované.
- Nová verzia cache v2 nepoužíva staré obrázky so zmazaným pozadím. Nie je potrebné znovu sťahovať sadu pomocných obrázkov.
- Náhľad farby je vo vnútri nápovedy, bez plochy v spodnom strede obrazovky.

```sh
opkg install /tmp/enigma2-skin-fullhdglass-warder-evolution_1.0.16-test258_all.ipk
```

Potom reštartovať GUI. Overiť najmä ECM a výber kanálov podľa nahlásených snímok, prejsť ďalšie skupiny a skontrolovať voľný stred medzi tlačidlami. Prijímačové zobrazenie TEST258 zatiaľ nie je potvrdené.

Kontroly overujú absenciu widgetov v strede päty, väčšie rozmery, zachovanú riadiacu logiku, všetkých 252 pomocných obrázkov vrátane pôvodného alfa kanála a presného obsahu vnútorných náhľadov. Rádio, pôvodné grafické súbory a automatické aktualizačné feedy sa nemenia.
