# FullHDGlass 1.0.38-test11 — obaly a ďalšie zápisy údajov z rádia

TEST11 nadväzuje na spoločnú opravu TEST10 a rieši konkrétne ďalšie chyby zo snímok prijímača:

- Skratky `Kroky F. Janecka` a `Kroky F.Janečka` sa rozpoznajú ako Kroky Františka Janečka. Zachová sa celý kredit spolu s Michalom Davidom; nesprávny sólový alebo živý výsledok sa neprijme.
- `Peter Bič Project — Stromy` sa rozpozná aj pod katalógovým názvom `Stromy (Original Version)`. Toto pravidlo je obmedzené na overenú skladbu; Radio Edit a naživo zostávajú odlišné.
- `Helena Vondráčková — Každá trampota má svou mez` sa priradí k overenej duetovej nahrávke s Jiřím Kornom. Pravidlo zachováva ďalších hostí a nevzťahuje sa na iné skladby.
- Hosť po `FT.`, `feat.` alebo `featuring` na konci názvu sa spracuje aj bez zátvoriek. `POLEMIC — SPOLU FT. A.M.O.` tak už nehľadá celý chybný reťazec ako samotný názov skladby. AMO a A.M.O. sú overené zápisy tej istej skupiny.
- Číslo súboru pred viacslovným interpretom, napríklad `24_Pavol Habera`, sa odstráni. Označenie remixu sa zachováva.
- Konkrétny preklep rádia `Darinka Rolincová — Az raz budem uvitelkou` sa pre vyhľadávanie textu aj obalu opraví na `Až raz budem učiteľkou`. Pravidlo je viazané na túto interpretku a celý presný chybný názov.
- Staré negatívne výsledky TEST10 sa preveria znova, aby neprekryli nové opravy. Platné kladné výsledky sa zachovajú.

Pri živých skúškach sa už podarilo stiahnuť skutočné obaly pre Michala Davida/Kroky, Stromy aj Helenu Vondráčkovú. Ďalšie výsledky sú v `docs/RADIO-TEST11-FIELD-CHECKS.json`; tento súbor nezverejňuje prevzaté texty ani celé obrázky. Pravidlá a primárne podklady sú v `docs/RADIO-IDENTITY-RULES.md`.

Pri Iskrí od Adama Ďuricu a Predsieni života od Paľa Naďa živé skúšky nenašli overený text; časť zdrojov bola nedostupná. Taký výsledok nie je dôkazom, že text neexistuje nikde. Rovnako sa automaticky nezamieňa remix Reklamy na ticho za pôvodnú verziu ani sa nevymýšľajú chýbajúce obaly.

Schválená grafika ostáva zachovaná. Ide o izolovanú skúšobnú verziu; produkčný kanál 1.0.37 sa nemení a overenie v prijímači s týmto balíkom ešte čaká.
