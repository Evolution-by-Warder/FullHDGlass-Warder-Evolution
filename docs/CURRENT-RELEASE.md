# FullHDGlass 1.0.38-test1 — rádio a texty piesní

Izolovaný skúšobný balík podľa odsúhlaseného modro-zlatého návrhu. Produkčná verzia 1.0.37 a všetky jej aktualizačné adresy zostávajú zachované.

- Vysoký panel obalu je užší iba po bokoch; obrázok si zachová pomer strán. Voľná plocha dekódera je priehľadná.
- Vedľa je natívny textový panel. Pri zmene skladby sa text vyhľadá automaticky v samostatnom procese. Prijíma sa iba úplná zhoda interpreta a názvu; živé/remixové verzie sa nezlievajú s originálom.
- Dlhší text sa plynulo posúva po krátkej pauze. Krátky zostáva stáť. Zmena stanice zruší staré vyhľadávanie; neskorá odpoveď sa nezobrazí. Nejde o karaoke.
- Dole zostáva picona, názov stanice, pôvodné riadky RadioText/RtpText, pôvodný animovaný equalizer a skutočný typ služby DAB/IPTV/DVB-S/DVB-T/DVB-C.
- Pozadie neobsahuje texty. Rámy a písmo sa kreslia samostatne; nevytvára sa škálovaný obrázok textu. Starý dodatočný rádio nadpis v InfoPanel vrstve je potlačený, aby sa nedvojil.
- Obaly, picony, DAB MOT/SLS, RASS vlastníctvo a RDS/ICY zdroje zostávajú v existujúcich komponentoch.

Zdroj slov piesní: [LRCLIB](https://lrclib.net/docs). Požiadavka obsahuje interpreta a názov skladby. Pokrytie našich rádií nie je zmerané; predchádzajúci odhad 50 % nebol meranie. Texty sa neukladajú do Gitu. Dočasná cache v prijímači má najviac 128 záznamov.

Zmeny XML sa obmedzujú na RdsInfoDisplay, RdsDisplay a RadioInfoBar; ostatné obrazovky zostávajú bajtovo rovnaké. Balík má kontrolu celého obsahu a limit 16 MiB.

**Na fyzickom prijímači ešte treba overiť ostrosť písma, správne orezanie posúvaného textu, oba infobary a návrat rádio/TV. Táto verzia sa automaticky neaktivuje v produkčnom feede.**
