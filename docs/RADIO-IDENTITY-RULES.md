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
