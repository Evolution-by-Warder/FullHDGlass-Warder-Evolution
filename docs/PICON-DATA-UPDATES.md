# Spoločné Warder piconové balíky — 27. október 2026

PiconHub a FullHDGlass používajú rovnaký živý katalóg. Táto aktualizácia mení iba sťahované dáta; nemení IPK ani jeho verziu.

Fun Rádio S/V má rovnakú schválenú piconu ako Fun Rádio Z. Melody S má rovnakú piconu ako Melody V/Z. ReginaBA, ReginaBB a ReginaKE používajú pôvodné priložené logá Západ, Stred a Východ. Všetkých 81 piconov pokrýva deväť presných referencií, tri pozadia a rozmery 50×30, 220×132 a 400×240. Farby a identita dodaných log zostali zachované.

Workflow 40572516519 preveril 30 súvisiacich satelitných a operátorských archívov. Zmenilo sa deväť celkových balíkov 23,5°E; operátorské archívy bez týchto referencií zostali nezmenené. Overených bolo všetkých 20 nových verejných častí podľa SHA256. Ostatné PNG a existujúce DAB picony zostali zachované. Zdroj: PiconHub commit 90d088e13f95ddc36df4369d0be4fdb0698a8ec2. Aktivačný commit: c5fc5ec6ef86e4de79305e892be3afbdf866f662. Presný výpis je v assets/warder/regional-radio-publication.json.

DVB-T CZ/SK 220×132 je dostupné v prevedeniach Transparent, Biele a Čierne. Biele a čierne používajú tie isté pôvodné transparentné logá na nezmenených Warder MASTER podkladoch. Obe odvodené inštalácie prešli skutočným Warder enginom a kontrolou každého PNG; cudzie súbory zostali zachované. Všetkých 44 verejných častí bolo overených podľa SHA256.

Každé pozadie DVB-T má 2 674 referenčných PNG súborov a 203 odlišných obrázkov. Počet súborov ani obrázkov sa nevydáva za presný počet staníc: v archíve nie je overený zoznam ich názvov. Pôvodné historické pokrytie zároveň nie je zárukou úplného dnešného vysielania.

Nové picony sa získajú opätovným stiahnutím príslušného dátového balíka v PiconHube alebo v Ponuke sťahovania skinu. Aktualizácia samotného pluginu na tieto zmeny nie je potrebná.


## Dopĺňanie rádií do Canal+ SK a CZ

Vlastník potvrdil, že uvedené rádia patria aj do operátorských sád. Ich neprítomnosť v pôvodných ZIPoch bola neúplnosť našich archívov, nie dôvod na vynechanie. Následná publikácia pridala všetkých deväť referencií (Fun Z/S/V, Melody Z/S/V, Regina BA/BB/KE) do každého z osemnástich balíkov Canal+ SK/CZ: 50×30, 220×132 a 400×240 v prevedeniach Transparent, Biele a Čierne. Ostatné PNG zostali zachované. Prešlo 10 testov, 18 inštalačných plánov a SHA256 kontrola všetkých 18 verejných častí. Workflow 40574914251; katalóg 17ac58f68dc2016b161790781d6532d859f30c98. Podrobný výsledok: assets/warder/canal-radio-publication.json. Zdrojové operátorské priečinky v PiconHube sú tiež doplnené identickými schválenými PNG. IPK ani runtime FastScan tabuľky sa nemenili.
