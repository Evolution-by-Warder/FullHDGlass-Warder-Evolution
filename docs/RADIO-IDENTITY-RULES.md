# Overené varianty identity rádiových skladieb

`warderSongIdentity.py` používajú metadáta, texty aj obaly. Zachováva celý názov, verziu a úplnú zostavu spoluúčinkujúcich. Nedopĺňa ľubovoľné krstné mená podľa iniciály a nevyberá prvý výsledok iba podľa podobnosti. Nasledujúce výnimky sú konkrétne a overiteľné.

| Zápis z vysielania | Overená katalógová identita | Obmedzenie |
| --- | --- | --- |
| M. Zbirka, Limit | Miroslav Žbirka / Miro Žbirka | Spojenie s Limitom iba pri Bielom kvete; ďalší hosť sa nevynechá. |
| Necar Vaclav / Neckar Vaclav | Václav Neckář | Úplný známy zápis mena; rozšírené pomenovania Svatovítského chrámu platia iba pre tohto interpreta. |
| Júlia Hečková / Hečkovci | Júlia a Peter Heckovci | Zjednotenie kreditov iba pri Talianskom muzikáli. |
| Ivan Tásler & IMT Smile | IMT Smile | Zjednotenie kreditov iba pri skladbe Viac. |
| Sima Martausová / Sima Magušinová (Martausová) | Rovnaká interpretka | For You či iný hosť zostáva samostatne povinný; sólová verzia sa tým nevyrovná duetu. |
| 08 - Krasnejsi nez ruze (Maliconia) - Pavel Roth | Pavel Roth — Krásnější než růže (Malinconia) | Opravený číselný prefix a konkrétny názov podľa oficiálneho interpreta; Live/Remix sa nezahadzuje. |

Odstránenie prefixu sa uplatní iba pri čisto číselnom poli do troch číslic a dvojitom oddeľovači. Názvy ako `070 Shake`, rok `1970` alebo číslo bez ďalšej dvojice polí sa tým neprepisujú. Skratky, zmenené priezviská a známe názvy sú explicitný zoznam, nie všeobecná voľná podobnosť.

## Podklady

- [Miroslav Žbirka — Biely kvet, vydanie OPUS](https://music.apple.com/sk/song/1533351204) a [rozhovor s interpretom o skupine Limit](https://radiozurnal.rozhlas.cz/dulezite-nejsou-ceny-ale-kvalitni-hudba-rika-miro-zbirka-ve-zlatem-slavikovi-7183115).
- [Václav Neckář — Svatovítský chrám, katalóg Supraphonu](https://www.supraphonline.cz/album/2208-40-hitu-jsem-tady-ja/flac?trackId=34822) a [Apple Music](https://music.apple.com/sk/song/1384668475).
- [Júlia a Peter Heckovci — Taliansky muzikál](https://music.apple.com/us/artist/j%C3%BAlia-a-peter-heckovci/1615992759), skladba 1615992544; pôvodný alternatívny kredit z vysielania je zaznamenaný v prípadoch prijímača.
- [Rozhovor s Ivanom Táslerom o IMT Smile a skladbe Viac](https://www.teraz.sk/kultura/ivan-taslerimt-smile-hudba-otm/216987-clanok.html).
- [STVR — Sima Magušinová a zmena priezviska](https://slovensko.stvr.sk/rubriky/starsie-znovu-si-vypocujte/nasa-hudba/289813/sima-magusinova) a [oficiálny klip Sima Martausová & For You](https://www.youtube.com/watch?v=Fb1fIST9OIk).
- [Pavel Roth — oficiálny text a názov](https://www.pavelroth.cz/texty.htm?skladba=36), [oficiálna diskografia](https://www.pavelroth.cz/discografie.htm) a [Supraphon](https://www.supraphonline.cz/album/582179-singly-1982-1988?highlighted=1&trackId=5692206).

## Zdroje a správanie

Nové HTML adaptéry čítajú iba pôvodný text zo známeho kontajnera, overujú nadpisy a zostávajú na presne povolenom HTTPS hostiteľovi. Oznamy o chýbajúcom texte, prihlasovacie stránky či nerozpoznané HTML sa nepovažujú za úspech. SuperMusic v skúške poskytol iba stránku vyžadujúcu JavaScript; taký zdroj nie je predstieraný ako funkčný adaptér.

Oficiálny web Pavla Rotha sa kontaktuje iba pre overenú skladbu a presnú cestu s identifikátorom 36. Pri ostatných interpretoch nevytvára ďalšie požiadavky. Súbory v Gite neobsahujú prevzaté celé texty ani HTML stránok.

Tekstowo sa číta výhradne z `inner-text` vo vnútri `#songText`. Rovnako pomenovaný kontajner v poľskom preklade `#songTranslation` sa ignoruje. Nadpis musí zodpovedať celému interpretovi a názvu. Overený príklad: [Dara Rolins — Sľub](https://www.tekstowo.pl/dara-rolins/slub).

## Doplnené po ďalších snímkach prijímača — TEST11

| Údaj z rádia | Overený zápis | Obmedzenie |
| --- | --- | --- |
| Kroky F. Janecka / Kroky F.Janečka | Kroky Františka Janečka | Rozpis celého známeho názvu skupiny; Michal David aj ostatní účinkujúci sa zachovávajú. |
| Peter Bič Project — Stromy | Stromy (Original Version) | Iba tento interpret a názov; Radio Edit, naživo a Remix zostávajú odlišné. |
| Helena Vondráčková — Každá trampota má svou mez | Helena Vondráčková & Jiří Korn | Konkrétna overená duetová nahrávka; iné skladby a ďalší hostia sa tým nezlučujú. Anglický pôvodný názov je Rest Your Love On Me. |
| A.M.O. / AMO | Rovnaká kapela | Neznamená vynechanie Polemicu či iného hosťa. |

Podklady: [Supraphon — Michal David, Každý mi tě, lásko, závidí](https://www.supraphonline.cz/album/107-deti-raje-bonusy?trackId=2091), [oficiálne videá Peter Bič Project](https://peterbicproject.sk/videa/), [Apple Music — Stromy, pôvodná verzia](https://music.apple.com/sk/song/1811180301), [Supraphon — duet Vondráčkovej a Korna](https://www.supraphonline.cz/album/2139-tech-par-dnu?trackId=33160), [oficiálny web AMO o spolupráci s Polemicom](https://www.amo24hodin.sk/novinky/vypo%C4%8Duj-si-%C5%A1t%C3%BAdiov%C3%BA-nahr%C3%A1vku-singlu-amo-polemic-spolu/) a [Apple Music — Spolu (feat. Polemic)](https://music.apple.com/us/song/1781096045).

Všeobecné spracovanie metadát teraz rozpoznáva hosťa na konci názvu po `ft.`, `feat.` alebo `featuring` aj bez zátvoriek. Číslo `1–3 číslice_` sa odstráni iba pred viacslovným menom interpreta. Príklad `24_Pavol Habera` sa opraví, no názov `Reklama na ticho (remix)` zostane celý. `24kGoldn`, `070 Shake`, `1975` a jednoslovný `24_Band` sa neprepisujú.

Preklep `DARINKA ROLINCOVA — Az raz budem uvitelkou` zo snímky prijímača sa opravuje na `Až raz budem učiteľkou` iba pri tomto úplnom mene a presnom chybnom názve. Správny názov a interpretku potvrdzuje aj [TV Markíza](https://www.markiza.sk/relacie/tvoja-tvar-znie-povedome/clanok/600099-zoznam-pesniciek-na-specialne-kolo-tvojej-tvare-co-zaspievaju-male-talenty). Iní interpreti a označenia Live/Remix sa tým nemenia.

## TEST12 — nové zdroje a zápisy z vysielania

KaraokeTexty.sk a KaraokeTexty.cz tvoria jednu explicitne povolenú rodinu HTTPS hostiteľov. Vyhľadávanie vyberie najviac dve presne pomenované skladby a cieľová stránka znovu overí meno z navigácie a celý názov. Známe odseky pôvodného textu sa čítajú samostatne, prekladový stĺpec sa ignoruje. Akordy Kytary číta iba celý kontajner `smartchordsheet`, overuje H1/H2 a ignoruje `scs-chord`; krátky JSON-LD úryvok nie je celý text.

Časť `Boban Markovic / Marko Markovic` sa rozdelí na dvoch hostí iba pri medzerách okolo lomky a viacslovných menách na oboch stranách. AC/DC sa nemení. Pôvodná nahrávka [Vidiek — Hrajte trúbky](https://music.apple.com/sk/song/1510333267) uvádza oboch hostí; výnimka pre hlavný kredit Vidiek je viazaná iba na tento názov. Ďalší explicitný hosť sa nevynechá.

Pri pomlčke bez medzier sa vyžaduje viacslovný interpret aj viacslovný názov; bežné formáty s medzerami majú prednosť. Táto oprava odstraňuje potvrdené čakanie pred samotným spustením hľadania pri `MIROSLAV ZBIRKA-Biely Kvet`.

SuperMusic v opakovanej skúške .sk presmeroval na .cz a vrátil JavaScriptový prístupový medzikrok. LyricFind sa v tomto prostredí nepodarilo spoľahlivo načítať. Tieto stránky sa nepredstierajú ako pripojené zdroje; [Lyric Display](https://www.lyricfind.com/products/lyric-display) a [Lyric Search](https://www.lyricfind.com/products/lyric-search) sú oficiálne možnosti ďalšej integrácie.
