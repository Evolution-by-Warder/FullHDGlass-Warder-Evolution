# FullHDGlass 1.0.38-test7 — rádio a texty piesní

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
- Pri dočasnej chybe najviac tri pokusy na tú istú skladbu, bežné pauzy 20 a 60 sekúnd. Hlavička Retry-After má prednosť a zákaz požiadaviek na LRCLIB platí aj pre ďalší pracovný proces. Každý pokus má najviac šesť požiadaviek, každá časový limit 6 sekúnd; samostatný proces sa po 45 sekundách ukončí. GUI nečaká na sieť.
- Časový limit už nenechá visieť stav vyhľadávania a oneskorená odpoveď starého procesu neprepíše aktuálny obsah.

**Pokrytie SK/CZ nie je vyriešené pre všetky skladby.** LRCLIB pri kontrolnej skúške našiel „Biely kvet“, ale „Sme pre seba stvorení“ zo snímky v skúšaných verejných API chýba. SuperMusic túto skladbu eviduje, jeho stránka však pri priamom načítaní vracala JavaScriptovú overovaciu stránku. Táto verzia preto nepredstiera funkčný konektor SuperMusic a neobsahuje ručne vložené texty. Žiadna percentuálna úspešnosť sa nesľubuje.

- Niektoré stanice posielajú poradie skladba – interpret. Vyhľadanie v oboch poliach a prijatie obráteného poradia vyžaduje úplnú zhodu oboch údajov z databázového záznamu. Rovnaký princíp už používa vyhľadávanie obalov.

Oba zdroje dostávajú aj celý pár údajov v obrátenom poradí; žiadne meno interpreta ani slovo názvu sa pri tom neodstraňuje. Záložné API vracia iba text pre požadovaný pár a neposkytuje nezávislé polia interpreta a názvu na ďalšie miestne overenie.

## TEST5: pomalé odpovede zdroja

Presná skladba zo snímky používateľa „Janek Ledecký – Budu všechno co si budeš přát“ sa pri kontrolnom načítaní našla za 5,69 sekundy. Doterajší šesťsekundový limit bol pre takto pomalé odpovede tesný; zo snímky sa konkrétna HTTP chyba v prijímači spätne určiť nedá.

- Jedna požiadavka má teraz najviac 10 sekúnd podľa zostávajúceho spoločného rozpočtu 32 sekúnd. Vonkajšie ukončenie pracovného procesu po 45 sekundách zostáva.
- Po prvom pokuse LRCLIB nasleduje hneď záložný zdroj. Nečaká sa najprv na všetky štyri varianty v jednej databáze. Počet požiadaviek sa nezvyšuje, texty sa stále sťahujú mimo GUI.
- Retry-After sa ráta od prijatia chyby, zahŕňa aj HTTP dátum a zostáva rešpektovaný ďalšími pracovnými procesmi.
- Pridané kontroly pre pomalý primárny zdroj, okamžité poradie zálohy, spoločný časový rozpočet a obe podoby Retry-After.

**Dostupnosť externých služieb nie je zaručená.** Pri skutočnom výpadku oboch zdrojov alebo chýbajúcom texte zostáva príslušná hláška. Táto úprava znižuje zbytočné zlyhania pri pomalej odpovedi a čas čakania na zálohu; nesľubuje text pre každú skladbu.

## TEST6: optimalizácia podľa prijímača a úprava hlavičky

- Žiadne RÁDIO uprostred hornej lišty. Dátum obsahuje lokalizovaný názov dňa, napríklad `Streda 28.10.2026`. Menšie biele sekundy sú bez medzery za minútami ako `20:52.00`; polohy vychádzajú z metrík skutočného fontu Prive7. Obidva rádiové RDS panely používajú tú istú hlavičku. Názvy dní sú pripravené pre 11 jazykov a kontrolované na šírku riadka.
- Equalizér má interval 110 ms namiesto 140 ms, teda približne o 27 % častejšie prekreslenie.
- Záloha sa spustí po 750 ms pomalej odpovede primárneho servera alebo hneď po jeho dokončení bez textu. Prvá nájdená odpoveď vyhrá. Čakanie na iný server nepredlžuje zobrazenie výsledku. Na jeden server beží v pomocnom procese najviac jedna požiadavka naraz; nejde o ďalšie vlákna v Enigme. Zdroj lyrics.ovh môže sám používať LRCLIB, preto tieto servery nie sú zárukou nezávislého pokrytia.
- Najviac päť požiadaviek namiesto šiestich. Doplňujúce hľadanie iba podľa názvu stále vyžaduje úplnú zhodu názvu aj všetkých interpretov zo záznamu.
- Potvrdené nenájdenie v oboch zdrojoch neprekryje chyba neskoršieho doplnkového pokusu. Pri nedostupnom zdroji bez platnej negatívnej odpovede zostáva možnosť opakovania. Nové voliteľné požiadavky sa nespúšťajú s menej než dvoma sekundami rozpočtu.
- Úplné negatívne výsledky sa uchovávajú 30 minút, čiastočné 5 minút; nájdené texty 14 dní. Cache je naďalej obmedzená na 128 záznamov. Obrátený pár rovnakých metadát používa tú istú cache a nevymaže zobrazený text.
- Po bežnom výpadku sa opakuje po 5 a 20 sekundách, najviac trikrát na skladbu; Retry-After príslušného servera má prednosť. Rozbehnuté opakovanie sa odlišuje vlastnou preloženou hláškou. Obmedzenie pomalšie sa zotavujúceho servera neblokuje skorší pokus o iný dostupný server.
- Pri spojení dvoch celých osobných mien sa normalizuje aj slovenské/české „a“. Žiadny interpret sa nevynecháva, nepoužívajú sa odhady podľa prvého výsledku.
- `/tmp/warder-radio-lyrics/.last-result` obsahuje iba posledný stav, čas a najviac päť stručných záznamov požiadaviek. Neobsahuje text piesne ani odpovede serverov.

Kontrolné príklady zo snímok: Faraon – Šlapací kolo; Sima Martausová a Miťo Bodnár – Slovo chlapa; Belle de Z – Nie som tvoja hračka. Tieto prípady sú overovaním vyhľadávania a jeho stavov, nie prísľubom, že každá databáza ich text obsahuje. Pokrytie SK/CZ zostáva čiastočné. Reálnu ostrosť a polohu natívnych textov na HDMI treba overiť na prijímači.

## TEST7: kompaktné ľavé okno podľa obalu

- Odstránený pôvodný vysoký rám 440×720. Nový tenký rám tesne obopína skutočný obrázok a zachováva jeho pomer strán. Každá os obrázka má najviac 420 px.
- Štvorcový obal 420×420 má polohu 316,286; stred je (526,496). Zvislý stred ľavého panela je totožný so stredom pravého panela 766,136 / 860×720. Široké aj portrétové obaly sú vycentrované tým istým pravidlom. Neexistuje prázdny vysoký modrý panel nad/pod obalom.
- Samostatný kompaktný renderer používa existujúce vyhľadávanie a natívny asynchrónny dekóder. Zisťovanie rozmerov číta najviac 64 KiB hlavičky PNG/JPEG/GIF/BMP/WebP v pomocnom vlákne; písmo ani obraz sa neškálujú cez screenshot. Rozmery pribaleného neutrálneho obrázka sú známe bez dodatočného čítania. Staré výsledky po zmene obrázka alebo zatvorení obrazovky sa zahodia.
- Počas zisťovania rozmerov sa výsledok kontroluje každých 50 ms, potom sa obnoví pôvodná ľahká frekvencia. Formátovanie dní, menšie pripojené sekundy, rýchlejší equalizér a optimalizácie textov z TEST6 zostávajú súčasťou balíka.

Doplnené sú kontroly štvorcového/širokého/portrétového obalu, centra a pomeru strán, čítania hlavičiek bez voliteľných balíkov, tesného natívneho rámu a odmietnutia oneskoreného výsledku. Zobrazenie na fyzickej TV ostáva na potvrdenie používateľa.
