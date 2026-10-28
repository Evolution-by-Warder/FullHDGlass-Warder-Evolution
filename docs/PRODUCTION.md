# FullHDGlass Warder Evolution — ostrá prevádzka

Aktuálna produkčná verzia je **1.0.36**. Doplnená je podpora samostatných textových správ internetového rádia v existujúcom riadku vedľa loga. Metadáta interpreta a skladby naďalej riadia presné vyhľadávanie obalov; slogan bez týchto údajov obal nevyhľadáva. Vlastník schválil pokračovanie úprav 28. októbra 2026.

PiconHub a skin používajú rovnaké overené piconové dáta a sťahovacie jadro; PiconHub nemusí byť samostatne nainštalovaný.

[Produkčné vydanie](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/v1.0.36) · [Presný produkčný záznam](PRODUCTION.json) · [Aktuálne zmeny](CURRENT-RELEASE.md)

Vo výbere zdrojov sú IPTV rádiá SK/CZ, DAB a DVB-T na začiatku, s ikonou pred názvom. Rozlíšenie sa volí samostatne. Picony pozícií sa proporčne zmenšujú do existujúceho rámčeka, takže je viditeľný celý obrázok. Opätovné otvorenie spoločného výberu DAB a satelitov zachová ich označenie.

DAB používa existujúci cieľový priečinok a pozadia Transparent, Biele a Čierne pri 220×132. Sťahovanie beží na pozadí, archívy a PNG sa overujú a pri chybe sa zápis obnoví. Rovnaké presné rádiové referencie sú aj v celkových balíkoch 19,2°E a 23,5°E. Pôvodné súbory mimo spravovaného pokrytia sa zachovávajú.

Pôvodný obnovený DVB-T CZ/SK archív má 2 674 PNG v prevedení Transparent 220×132. Biele a čierne prevedenie je už dostupné z rovnakých transparentných log na schválených Warder podkladoch. Historický archív nie je zárukou úplného súčasného pokrytia vysielania.

## Aktualizácie a súbory

Aktuálny manifest je update-production.json. Staršie inštalácie najprv využijú nemenný prechod cez 1.0.18; podrobnosti sú v [PACKAGE-TRANSITION.md](PACKAGE-TRANSITION.md). Balík má štandardný identifikátor enigma2-plugin-skins-fullhdglass-warder-evolution. Kompatibilné vnútorné cesty a uložené nastavenia zostávajú zachované.

IPK zostáva pod limitom 16 MiB. Nápoveda používa pôvodný balík g17_setup_pict.zip a existujúce umiestnenie súborov skinu; archívy sa overujú podľa veľkosti a SHA256. Už uložené náhľady fungujú bez siete. Schválené obrázky, MASTER šablóny, autorské údaje Shamann a rádiové infobary zostávajú zachované.

## Overenie

Vydanie 1.0.35 prešlo 65 testami metadát a obalov vrátane prechodov skladba → správa → skladba → prázdny text, prednosti aktuálnej natívnej správy a zachovania ICY pri neúplnom natívnom údaji. Cielené testy kontrolujú sťahovanie, zmiešaný výber, zrušenie operácie, obnovu súborov, poradie a ikony aj vykreslenie celého piconu. Produkčný workflow overuje rozloženie, všetkých 252 pomocných obrázkov, pôvodné piconové balíky, preklady a každý súbor IPK. Aktualizačný manifest sa sprístupní až po kontrole verejných bajtov balíka.

Presný zdroj, workflow, veľkosť a SHA256 sú v PRODUCTION.json. Fyzické overenie novej verzie 1.0.36 v prijímači sa zatiaľ netvrdí. Používateľ potvrdil zobrazenie rádiových piconov v oboch infobaroch v predchádzajúcej verzii. Historické zdroje, výsledky a nemeniteľné vydania zostávajú dostupné v Gite.


Dátová aktualizácia 27.10.2026: [aktuálne piconové balíky a overenie](PICON-DATA-UPDATES.md). Historické IPK 1.0.29 zostáva nezmenené; aktuálne vydanie je uvedené vyššie.


## IPTV SK/CZ — 1.0.36

Nová ponuka používa rovnaké overené dáta a kód ako PiconHub 0.1.30. Picony 247 položiek / 263 referencií v každom z deviatich variantov. Bouquet 321 položiek; 286 vybraných URL vrátilo zvukové dáta pri skúške. 74 položiek zatiaľ bez vhodného overeného piconu. [Dáta a bouquety](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/tree/main/picons/IPTV-SK-CZ).

Kompletné CI **40687770330** prešlo vrátane 252 pomocných ilustrácií, pôvodných piconových balíkov, prekladov a overenia všetkých súborov IPK. Verejný balík má **14 271 200 bajtov**, SHA256 `e2a7e43c6cb7fe129c12f7c3bb511bbbdfd2a075ac051ad708adaec29a7d811c`. Všetkých deväť spoločných modulov v zverejnených IPK bolo porovnaných bajt po bajte. Produkčný feed ponúka 1.0.36; legacy bridge 1.0.18 zostáva nezmenený. [Dôkaz overenia](IPTV-SK-CZ-1.0.36.json).


Dátové doplnenie 28.10.2026 (r2): 247 položiek s piconmi / 263 referencií v každom z deviatich variantov, 74 zatiaľ bez vhodného overeného piconu. Overené Radia.sk, Radia.cz a MyOnlineRadio.cz aj dodané originály. Všetkých deväť verejných archívov a obrázkov prešlo kontrolou; aktuálne dáta sa stiahnu opätovným výberom IPTV rádiá SK/CZ. Verzie IPK sa nemenia. [Zdroje a zhodovanie](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/blob/main/picons/IPTV-SK-CZ/catalog/followup-sources.json).
