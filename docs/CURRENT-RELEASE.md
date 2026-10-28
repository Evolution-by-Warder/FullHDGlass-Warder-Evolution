# FullHDGlass 1.0.38-test3 — rádio a texty piesní

Izolovaný skúšobný balík podľa odsúhlaseného modro-zlatého návrhu. Produkčná verzia 1.0.37 a všetky jej aktualizačné adresy zostávajú zachované.

- Vysoký panel obalu je užší iba po bokoch; obrázok si zachová pomer strán. Voľná plocha dekódera je priehľadná.
- Vedľa je natívny textový panel. Pri zmene skladby sa text vyhľadá automaticky v samostatnom procese. Prijíma sa iba úplná zhoda interpreta a názvu; živé/remixové verzie sa nezlievajú s originálom.
- Dlhší text sa plynulo posúva po krátkej pauze. Krátky zostáva stáť. Zmena stanice zruší staré vyhľadávanie; neskorá odpoveď sa nezobrazí. Nejde o karaoke.
- Dole zostáva picona, názov stanice, pôvodné riadky RadioText/RtpText, pôvodný animovaný equalizer a skutočný typ služby DAB/IPTV/DVB-S/DVB-T/DVB-C.
- Pozadie neobsahuje texty. Rámy a písmo sa kreslia samostatne; nevytvára sa škálovaný obrázok textu. Starý dodatočný rádio nadpis v InfoPanel vrstve je potlačený, aby sa nedvojil.
- Obaly, picony, DAB MOT/SLS, RASS vlastníctvo a RDS/ICY zdroje zostávajú v existujúcich komponentoch.

Zdroje textov: [LRCLIB](https://lrclib.net/docs) a záložné [lyrics.ovh](https://github.com/NTag/lyrics.ovh). Požiadavka obsahuje interpreta a názov skladby. Pokrytie našich rádií nie je zmerané; predchádzajúci odhad 50 % nebol meranie. Texty sa neukladajú do Gitu. Dočasná cache v prijímači má najviac 128 záznamov.

Zmeny XML sa obmedzujú na RdsInfoDisplay, RdsDisplay a RadioInfoBar; ostatné obrazovky zostávajú bajtovo rovnaké. Balík má kontrolu celého obsahu a limit 16 MiB.

**Na fyzickom prijímači ešte treba overiť ostrosť písma, správne orezanie posúvaného textu, oba infobary a návrat rádio/TV. Táto verzia sa automaticky neaktivuje v produkčnom feede.**

## Oprava reálneho TV pozadia

Používateľ potvrdil, že OpenWebif je správny, ale na fyzickej TV presvitá pôvodný stredový rám. Príčina: TEST1 zmenil JPG podklad, ale ponechal starý pasívny MPEG2 súbor `radio.mvi`. OpenWebif nahrádza video vrstvu aktuálnym JPG, preto sa chyba na jeho snímke neprejavila.

TEST2 obnovuje `radio.mvi` z aktuálneho čistého JPG bez rámov. Build aj kontrola IPK overujú obe SHA256 a porovnávajú dekódovaný TV obraz s JPG; samotná zhoda balíka so zdrojmi už nestačí. Pôvodná video konfigurácia a natívny výber rádiového podkladu zostávajú zachované. Nový podklad v reálnom HDMI výstupe ešte musí potvrdiť používateľ.

## Oprava infobaru po OK

TEST1 pri úprave vrstiev odfiltroval pôvodný grafický podklad InfoPanelu v rádio režime. Ostali iba jeho texty cez rádio obrazovku. TEST2 vracia vybraný grafický PNG podklad aj pre rádio s alfa prelínaním; priehľadná horná časť zachová rádio scénu a nepriehľadná plocha infobaru oddelí jeho údaje. Televízna vetva aj polohy a zdroje pôvodných údajov zostávajú zachované. Automatická kontrola prechádza všetky reálne celoplošné šablóny InfoPanelu.

## TEST3: dostupnosť textov

- Primárne vyhľadávanie číta databázu LRCLIB cez `/api/search`; pomalý `/api/get`, ktorý môže spúšťať ďalšie vyhľadávanie, už nepredchádza každej skladbe.
- Záložný zdroj lyrics.ovh dostáva celý názov interpreta aj skladby. Pri skúške našiel „Breaking Me“ s údajmi „Topic and A7S“ zo snímky používateľa.
- Pri LRCLIB sa normalizujú diakritika a oddeľovače spoluúčinkujúcich (`ft.`, `feat.`, `and`, `&`, čiarka). Všetci interpreti a celý názov vrátane verzie musia naďalej sedieť.
- Ak zhodný záznam obsahuje iba LRC, odstránia sa časové značky a zobrazí sa obyčajný text bez karaoke.
- Výpadok, HTTP 503/429 ani časový limit sa neukladajú ako nenájdený text na šesť hodín. HTTP 404 sa rozlišuje od nedostupného servera. Nová verzia cache zahodí staré negatívne výsledky.
- Pri dočasnej chybe najviac tri pokusy na tú istú skladbu, bežné pauzy 20 a 60 sekúnd. Hlavička Retry-After má prednosť a zákaz požiadaviek na LRCLIB platí aj pre ďalší pracovný proces. Každý pokus má najviac štyri požiadavky, každá časový limit 6 sekúnd; samostatný proces sa po 35 sekundách ukončí. GUI nečaká na sieť.
- Časový limit už nenechá visieť stav vyhľadávania a oneskorená odpoveď starého procesu neprepíše aktuálny obsah.

**Pokrytie SK/CZ nie je vyriešené pre všetky skladby.** LRCLIB pri kontrolnej skúške našiel „Biely kvet“, ale „Sme pre seba stvorení“ zo snímky v skúšaných verejných API chýba. SuperMusic túto skladbu eviduje, jeho stránka však pri priamom načítaní vracala JavaScriptovú overovaciu stránku. Táto verzia preto nepredstiera funkčný konektor SuperMusic a neobsahuje ručne vložené texty. Žiadna percentuálna úspešnosť sa nesľubuje.
