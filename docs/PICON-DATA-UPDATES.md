# Európske picony — 29. október 2026

Živé spoločné balíky FullHDGlass a PiconHub obsahujú 27 schválených grafík (listy A1/A2, B1/B2/B3, C1), 81 presných originálov 220×132. Dve ďalšie veľkosti 50×30 a 400×240 sa odvodili pomerne s prednásobenou alfou. Dnešný Vhannibal Motor 29 ott 2026 potvrdil 38 servisných priradení. Zmenilo sa 63 celopozičných balíkov na 4,8°E, 7°E, 9°E, 13°E, 23,5°E, 28,2°E a 42°E. Zo 111 relevantných celopozičných a operátorských archívov zostali ostatné bez zmeny.

Kontroly: 6 regresných testov, 63 plánov reálneho downloadera, 63 skúšok skutočného selektívneho inštalátora a SHA256/veľkosť všetkých 137 nových verejných častí. Ostatné PNG bajty a staršie archívy zostali zachované. Skin ani plugin nepotrebujú nový IPK; aktuálne picony sa získajú opätovným stiahnutím zvoleného balíka v režime nahradenia.

Zdroj grafík: `5ca5b5a08c0cf2cc7720334d05f00f09db899b8c` v PiconHube. Aktivácia katalógu: `6fe13bbcd00dc6ccd129f2727b081f8091013ac2`. Úspešný publikačný workflow: 40941891149; prvé úplné zostavenie a inštalačné kontroly: 40940899348 (jeho posledný zápis správy opravený v úspešnom pokračovaní). [Podrobný záznam](../reports/europe-picons-publication-20261029.json).

Samostatné Magenta Sport League 1–4 sú výslovne vylúčené: ďalší náhľad D1 čaká na schválenie; nesmú dostať obrázok bežných Sport 1–4. Grafické doplnenie nepredstiera dokončenie všetkých historických neistých aliasov z auditu.

---

# IPTV rádiá SK/CZ — 28. október 2026

PiconHub 0.1.30 a FullHDGlass 1.0.36 pridávajú rovnakú prvú položku IPTV rádiá SK/CZ. Picony pre 247 položiek, 229 presných referenčných PNG v každom z deviatich variantov; bouquet 321 položiek, 108 zatiaľ bez vhodného overeného piconu. Pri 286 vybraných URL skúška vrátila zvukové dáta.

[Bouquety, chýbajúce obrázky a pôvod](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/tree/main/picons/IPTV-SK-CZ). PNG sú samostatne sťahované, nezväčšujú IPK. Ostatné krajiny celého pôvodného bouquetu a nesúvisiace používateľské picony zostávajú zachované. Len oficiálne alebo schválené logá a zmrazené MASTER podklady.

---

# Spoločné Warder piconové balíky — 27. október 2026

PiconHub a FullHDGlass používajú rovnaký živý katalóg. Táto aktualizácia mení iba sťahované dáta; nemení IPK ani jeho verziu.

Fun Rádio S/V má rovnakú schválenú piconu ako Fun Rádio Z. Melody S má rovnakú piconu ako Melody V/Z. ReginaBA, ReginaBB a ReginaKE používajú pôvodné priložené logá Západ, Stred a Východ. Všetkých 81 piconov pokrýva deväť presných referencií, tri pozadia a rozmery 50×30, 220×132 a 400×240. Farby a identita dodaných log zostali zachované.

Workflow 40572516519 preveril 30 súvisiacich satelitných a operátorských archívov. Zmenilo sa deväť celkových balíkov 23,5°E; operátorské archívy bez týchto referencií zostali nezmenené. Overených bolo všetkých 20 nových verejných častí podľa SHA256. Ostatné PNG a existujúce DAB picony zostali zachované. Zdroj: PiconHub commit 90d088e13f95ddc36df4369d0be4fdb0698a8ec2. Aktivačný commit: c5fc5ec6ef86e4de79305e892be3afbdf866f662. Presný výpis je v assets/warder/regional-radio-publication.json.

DVB-T CZ/SK 220×132 je dostupné v prevedeniach Transparent, Biele a Čierne. Biele a čierne používajú tie isté pôvodné transparentné logá na nezmenených Warder MASTER podkladoch. Obe odvodené inštalácie prešli skutočným Warder enginom a kontrolou každého PNG; cudzie súbory zostali zachované. Všetkých 44 verejných častí bolo overených podľa SHA256.

Každé pozadie DVB-T má 2 674 referenčných PNG súborov a 203 odlišných obrázkov. Počet súborov ani obrázkov sa nevydáva za presný počet staníc: v archíve nie je overený zoznam ich názvov. Pôvodné historické pokrytie zároveň nie je zárukou úplného dnešného vysielania.

Nové picony sa získajú opätovným stiahnutím príslušného dátového balíka v PiconHube alebo v Ponuke sťahovania skinu. Aktualizácia samotného pluginu na tieto zmeny nie je potrebná.


## Dopĺňanie rádií do Canal+ SK a CZ

Vlastník potvrdil, že uvedené rádia patria aj do operátorských sád. Ich neprítomnosť v pôvodných ZIPoch bola neúplnosť našich archívov, nie dôvod na vynechanie. Následná publikácia pridala všetkých deväť referencií (Fun Z/S/V, Melody Z/S/V, Regina BA/BB/KE) do každého z osemnástich balíkov Canal+ SK/CZ: 50×30, 220×132 a 400×240 v prevedeniach Transparent, Biele a Čierne. Ostatné PNG zostali zachované. Prešlo 10 testov, 18 inštalačných plánov a SHA256 kontrola všetkých 18 verejných častí. Workflow 40574914251; katalóg 17ac58f68dc2016b161790781d6532d859f30c98. Podrobný výsledok: assets/warder/canal-radio-publication.json. Zdrojové operátorské priečinky v PiconHube sú tiež doplnené identickými schválenými PNG. IPK ani runtime FastScan tabuľky sa nemenili.


Dátové doplnenie 28.10.2026 (r2): 247 položiek s piconmi / 263 referencií v každom z deviatich variantov, 74 zatiaľ bez vhodného overeného piconu. Overené Radia.sk, Radia.cz a MyOnlineRadio.cz aj dodané originály. Všetkých deväť verejných archívov a obrázkov prešlo kontrolou; aktuálne dáta sa stiahnu opätovným výberom IPTV rádiá SK/CZ. Verzie IPK sa nemenia. [Zdroje a zhodovanie](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/blob/main/picons/IPTV-SK-CZ/catalog/followup-sources.json).

## 28. 10. 2026 — audit a vyčistenie DVB-T/T2 SK/CZ

Spoločný balík pre FullHDGlass a PiconHub obsahuje 2 531 referencií v každom pozadí 220×132. Pridaných je 54 názvov PNG, aktualizovaných 148 a odstránených 197 zastaraných alebo chybných súborov. Aktuálny zoznam má 227 riadkov vrátane regiónov a technických pozícií; nejde o počet unikátnych staníc. Nepotvrdené regionálne identity a chýbajúce aktuálne referencie sú výslovne označené.

[Zoznam a dôvody odstránení](../assets/warder/downloads/picons/dvb-t-skcz/README.md). Všetkých 47 verejných častí prešlo SHA-256 kontrolou. Skutočný Warder engine nainštaloval všetky tri pozadia a overil každý výsledný súbor aj zachovanie používateľského súboru. Inštalačné balíky a verzie pluginov sa nemenia.
