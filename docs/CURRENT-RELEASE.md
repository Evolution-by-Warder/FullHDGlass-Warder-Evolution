# FullHDGlass 1.0.38-test8 — nové zdroje textov piesní

Skúšobná verzia dopĺňa slovenské a české zdroje textov. Zachováva používateľom schválenú kompaktnú rádiovú obrazovku z TEST7. Produkčná verzia 1.0.37 a produkčný aktualizačný kanál sa týmto vydaním nemenia.

## Získavanie textov

- Najprv lokálna cache a LRCLIB. Ak LRCLIB neodpovie do 750 ms alebo sa jeho vyhľadávanie skončí bez výsledku skôr, súbežne začnú lyrics.ovh, Hudba.sk a textypisni.youradio.cz. Prvý nájdený text sa zobrazí bez čakania na ostatné servery.
- HTML zdroje musia potvrdiť celého interpreta aj názov skladby podľa nadpisov a navigácie stránky. Neberie sa prvý všeobecný výsledok. Zachovajú sa všetci spoluúčinkujúci aj označenie živej/remixovej verzie; tolerujú sa diakritika, bežné oddeľovače spoluúčinkujúcich a vynechaná čiarka v názve.
- Hudba.sk používa priamu cestu k skladbe a podľa potreby vlastné vyhľadávanie. Youradio používa vlastné vyhľadávanie a presne zodpovedajúcu stránku. Číta sa iba pôvodný text; preklady, reklamy, navigácia a skripty sa ignorujú.
- Všetky HTTP požiadavky, parsovanie aj cache textov zostávajú v samostatnom pomocnom procese. Najviac jedna požiadavka na jeden server naraz, 12 požiadaviek celkovo, 1 MiB na odpoveď, 20 000 znakov textu. Rozpočet spúšťania požiadaviek 32 sekúnd a vonkajšie ukončenie procesu po 45 sekundách zostávajú. Rešpektuje sa Retry-After.
- Odkazy a presmerovania HTML zdrojov zostávajú iba na presnom HTTPS hostiteľovi príslušného zdroja. Blokovacia či prihlasovacia stránka sa neukladá ako skutočné nenájdenie.
- Nájdené texty sa uchovávajú 14 dní, úplné negatívne výsledky 30 minút a čiastočné 5 minút; najviac 128 záznamov. Upgrade zachová platné nájdené texty z TEST7 a zneplatní staré negatívne výsledky, aby sa využili nové zdroje.
- Bežné opakovanie zostáva po 5 a 20 sekundách, najviac tri pokusy na skladbu; dlhší interval servera má prednosť. Nevytvára sa karaoke ani synchronizované zvýrazňovanie slov.

## Overenie

Pavol Habera – Láska, necestuj tým vlakom: pri reálnej skúške so zámerne nedostupnými oboma JSON API získaný text z Hudba.sk za približne 5–7 sekúnd. Faraon – Šlapací kolo: pri kontrolnom živom vyhľadávaní získaný text z Youradio za približne 10 sekúnd. Samostatné parsovanie overilo aj pôvodný text Youradio a jeho oddelenie od prekladu. Žiadny celý text piesne ani HTML stránka sa neukladá do Gitu; záznamy overenia obsahujú iba stav, veľkosť a SHA256.

CI okrem existujúcich kontrol spúšťa aj reálny regionálny test s vypnutými JSON API. Testy obsahujú vlastné ilustračné reťazce, nie skopírované texty piesní. Pokrytie všetkých SK/CZ skladieb nie je zmerané a nie je garantované.

## Zachovaný vzhľad

Kompaktný rám tesne okolo obalu, zachovaný pomer strán a zvislé vycentrovanie oproti pravému panelu. Bez nápisu RÁDIO uprostred hlavičky; lokalizovaný deň a dátum, menšie pripojené biele sekundy a interval equalizéra 110 ms. Grafické podklady, XML geometria, prehrávanie, obaly, picony, DAB MOT/SLS a RDS zostávajú rovnaké ako v TEST7. Nepotrebujú sa nové voliteľné balíky na prijímači.

## Zdroje

- [LRCLIB](https://lrclib.net/docs)
- [lyrics.ovh](https://github.com/NTag/lyrics.ovh)
- [Hudba.sk](https://hudba.zoznam.sk/)
- [Youradio – texty piesní](https://textypisni.youradio.cz/)

Ide o texty poskytované príslušnými stránkami; nemeníme ich na vlastnú tvorbu. Poskytovatelia dostanú interpreta a názov požadovanej skladby. Posledná diagnostika v `/tmp/warder-radio-lyrics/.last-result` obsahuje najviac 12 stručných stavov požiadaviek a neobsahuje samotný text piesne.
