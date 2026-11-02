# FullHDGlass 1.0.62-test4 — OpenPLi Plugin Browser

Oprava prázdneho prehliadača pluginov nahláseného na OpenPLi. Doterajšia šablóna obsahovala iba zdroje `pluginList` a `pluginGrid` z OpenATV; OpenPLi plní natívny komponent `list`, ktorý nemal v skine žiadny aktívny prvok. Oprava v OpenPLi pridá natívny zoznam s ikonami, názvami a popismi. Používa pôvodné obsluhy spustenia pluginu, zoradenia a farebných tlačidiel.

Výška obsahu aj zoznamu je v OpenPLi zosúladená na 90 pixelov, aby sa zmestil názov aj druhý riadok popisu. Rovnaká oprava výšky platí pri sťahovaní a odstraňovaní pluginov. Písmo a už väčšie používateľské riadky sa zachovajú. Zmena je obmedzená na aktívny FullHDGlass v OpenPLi; zdrojové šablóny OpenATV sa nemenia.

Nová regresia reprodukuje pôvodné nulové zobrazenie zoznamu, naplní skutočnú triedu PluginList cez natívny PluginBrowser.updateList, preverí ikony a oba textové riadky a cez pôvodnú metódu run spustí zvolený vzorový plugin. Testy používajú natívny procesor podmienok šablóny. Podmienka úspechu už nezahŕňa iba kontrolu existujúcich väzieb: vyžaduje aj zobrazenie naplneného hlavného zoznamu.

Určené pre OpenPLi 9.2 / develop s Pythonom 3 aj doterajšie testovanie OpenATV. Hlavný skin zostáva vo Full HD. Všetky opravy test3 zostávajú zahrnuté. Produkčné aktualizácie sa nemenia; starší IPK test3 zostáva nezmenený.

```sh
opkg install /tmp/enigma2-plugin-skins-fullhdglass_1.0.62-test4_all.ipk
```

Po úspešnej inštalácii reštartuj GUI a otvor prehliadač pluginov. Skontroluj názvy, popisy, ikony, posun zoznamu a spustenie pluginu. Toto je nová testovacia zostava; fyzické potvrdenie opravy na OpenPLi ešte čaká.
