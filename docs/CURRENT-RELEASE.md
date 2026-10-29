# FullHDGlass 1.0.38-test12 — ďalšie zdroje textov a oprava čakania na údaje

- Pripojené KaraokeTexty.sk aj KaraokeTexty.cz. Vyhľadáva sa podľa názvu, kandidáti aj cieľová stránka musia potvrdiť celého interpreta a skladbu. Čítajú sa iba odseky pôvodného textu; preklady a reklamy sa ignorujú.
- Pripojené Akordy Kytary.cz. Načítava sa celý text zo zobrazeného notového listu a vynechávajú sa akordové značky. Krátka ukážka v SEO metadátach sa nepoužíva namiesto celého textu.
- Opravený zápis `MIROSLAV ZBIRKA-Biely Kvet`. Keď majú obe časti viac slov, engine rozpozná aj pomlčku bez okolitých medzier. Vyhľadávanie sa tak spustí namiesto trvalého čakania na údaje. Mená Jay-Z, Jean-Michel Jarre a AC-DC sa tým nerozdeľujú.
- Hosťujúci interpreti s plnými menami sa rozpoznajú aj pri zápise s medzerami okolo lomky, napríklad Boban Markovic / Marko Markovic. Zápis AC/DC zostáva názvom kapely. Pri skladbe Vidiek — Hrajte trúbky sa overené kompletné kredity zjednotia aj pri skrátenom údaji hlavného interpreta.
- Presný výsledok vyhľadávania sa načíta hneď, pred skúšaním ďalšej zrkadlovej domény. Zbytočný druhý vyhľadávací krok tak neodďaľuje dostupný text.
- Staré negatívne výsledky TEST11 sa preveria znova; platné kladné výsledky zostávajú použiteľné.

## Živé overenie

Nový adaptér pri vypnutých ostatných zdrojoch získal text **Láska — Mraky** z KaraokeTexty (1 454 znakov) a **Lucie — Chci zas v tobě spát** z Akordy Kytary (1 616 znakov). Ide o overenie konkrétnych skladieb, nie odhad pokrytia celého katalógu. Záznamy a kontrolné súčty sú v `docs/RADIO-TEST12-SOURCE-CHECKS.json`; prevzaté celé texty ani HTML sa v Gite nepublikujú.

## Preverené, zatiaľ nepripojené zdroje

SuperMusic.sk presmeroval na SuperMusic.cz a priame načítanie vrátilo iba 552-bajtovú stránku vyžadujúcu JavaScript, bez textu piesne. Preto nebol pridaný nefunkčný adaptér.

LyricFind používateľovi zobrazil text skladby Kali & Tina — Aj keby. Náš engine tento zdroj zatiaľ nepoužíva. Overovanie jeho verejného webu v tomto prostredí narazilo na stránku Site Unavailable a pri skúšanej textovej stránke na HTTP 403. LyricFind ponúka aj oficiálne licencované produkty Lyric Search a Lyric Display; funkčný automatický prístup pre tento plugin ešte nebol overený. Neúspech našich súčasných adaptérov preto nie je tvrdenie, že text neexistuje.

Zachovaný je schválený vzhľad rádia aj všetky opravy TEST11. Ide o izolovanú skúšobnú verziu, produkčný kanál 1.0.37 sa nemení. Opravu ešte treba potvrdiť v prijímači.
