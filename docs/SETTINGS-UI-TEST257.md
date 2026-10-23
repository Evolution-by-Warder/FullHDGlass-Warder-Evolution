# FullHDGlass Warder Evolution — TEST257

Celá spoločná sada 252 pomocných obrázkov sa zobrazuje s pozadím zladeným s nastavovacím panelom. Obrázky zostávajú: texty, ikony, fotografie, náhľady obrazoviek a šípky sa neprekresľujú ani nenahrádzajú textovým popisom.

Spoločné čierne ozdobné pozadie je pri načítaní priehľadné. Predpočítané masky sú viazané na SHA256 konkrétneho pôvodného PNG. Plochy skutočných náhľadov majú zachované vnútorné detaily. Pôvodné súbory v g17_setup_pict sa nemenia, nový archív sa nemusí sťahovať. Výsledok sa bezpečne a atomicky ukladá do /tmp/warder-help-art-v1. Pri neznámom alebo poškodenom obrázku/chybe zápisu zostáva pôvodné zobrazenie, bez pádu GUI. Nie je potrebný Pillow ani nový balík v prijímači.

Zachováva zmenšenie 882×300 → 794×270 s pomerom strán a odstupom od rámov vo všetkých konfiguračných skupinách, odstránenie duplicitnej hodnoty v päte, užitočné ukážky farby a dátumu, čistú pätu a názov IPK bez 17.

```sh
opkg install /tmp/enigma2-skin-fullhdglass-warder-evolution_1.0.16-test257_all.ipk
```

Potom reštartovať GUI. Overiť ECM, SIEŤ, MENU, počasie, picony a ďalšie skupiny s obrazovou nápovedou. Obsah ukážok musí zostať čitateľný, bez čiernej ozdobnej bubliny a bez presahu cez rám. Prijímačové potvrdenie TEST257 zatiaľ chýba.

Overenie zahŕňa rozloženie všetkých vlastných obrazoviek, spoločné načítanie vo všetkých konfiguračných skupinách, zmrazený AST základ nastavení, natívne PNG filtre a porovnanie všetkých 252 obrázkov s nezávislým dekóderom. Pôvodný balík pomocných obrázkov má SHA256 872d59dfccf090344a37ed46e277dd091cd9ec671db128fa421c748f4f6eb8ef. Rádio, ostatná grafika a aktualizačné feedy sa nemenia.
