# FullHDGlass Warder Evolution — ostrá prevádzka

Aktuálna produkčná verzia je **1.0.29**. Vlastník schválil doplnenie DAB a jednotné správanie vo Warder ekosystéme 27. októbra 2026. PiconHub a skin používajú rovnaké overené rádiové dáta a sťahovacie jadro; PiconHub nemusí byť samostatne nainštalovaný.

[Produkčné vydanie](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/v1.0.29) · [Presný produkčný záznam](PRODUCTION.json) · [Aktuálne zmeny](CURRENT-RELEASE.md)

Vo výbere zdrojov sú DAB a DVB-T na začiatku, s ikonou pred názvom. Rozlíšenie sa volí samostatne. Picony pozícií sa proporčne zmenšujú do existujúceho rámčeka, takže je viditeľný celý obrázok. Opätovné otvorenie spoločného výberu DAB a satelitov zachová ich označenie.

DAB používa existujúci cieľový priečinok a pozadia Transparent, Biele a Čierne pri 220×132. Sťahovanie beží na pozadí, archívy a PNG sa overujú a pri chybe sa zápis obnoví. Rovnaké presné rádiové referencie sú aj v celkových balíkoch 19,2°E a 23,5°E. Pôvodné súbory mimo spravovaného pokrytia sa zachovávajú.

Pôvodný obnovený DVB-T CZ/SK archív má 2 674 PNG v prevedení Transparent 220×132. Biele a čierne prevedenie je už dostupné z rovnakých transparentných log na schválených Warder podkladoch. Historický archív nie je zárukou úplného súčasného pokrytia vysielania.

## Aktualizácie a súbory

Aktuálny manifest je update-production.json. Staršie inštalácie najprv využijú nemenný prechod cez 1.0.18; podrobnosti sú v [PACKAGE-TRANSITION.md](PACKAGE-TRANSITION.md). Balík má štandardný identifikátor enigma2-plugin-skins-fullhdglass-warder-evolution. Kompatibilné vnútorné cesty a uložené nastavenia zostávajú zachované.

IPK zostáva pod limitom 16 MiB. Nápoveda používa pôvodný balík g17_setup_pict.zip a existujúce umiestnenie súborov skinu; archívy sa overujú podľa veľkosti a SHA256. Už uložené náhľady fungujú bez siete. Schválené obrázky, MASTER šablóny, autorské údaje Shamann a rádiové infobary zostávajú zachované.

## Overenie

Cielené testy kontrolujú sťahovanie, zmiešaný výber, zrušenie operácie, obnovu súborov, poradie a ikony aj vykreslenie celého piconu. Produkčný workflow overuje rozloženie, všetkých 252 pomocných obrázkov, pôvodné piconové balíky, preklady a každý súbor IPK. Aktualizačný manifest sa sprístupní až po kontrole verejných bajtov balíka.

Presný zdroj, workflow, veľkosť a SHA256 sú v PRODUCTION.json. Fyzické overenie novej verzie 1.0.29 v prijímači sa zatiaľ netvrdí. Používateľ potvrdil zobrazenie rádiových piconov v oboch infobaroch v predchádzajúcej verzii. Historické zdroje, výsledky a nemeniteľné vydania zostávajú dostupné v Gite.


Dátová aktualizácia 27.10.2026: [aktuálne piconové balíky a overenie](PICON-DATA-UPDATES.md). IPK 1.0.29 zostáva nezmenené.
