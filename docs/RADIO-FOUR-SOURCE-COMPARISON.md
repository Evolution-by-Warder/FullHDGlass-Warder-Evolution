# Porovnanie štyroch zdrojov textov piesní

Dátum: 29. 10. 2026. Rovnakých 12 skladieb na každom zdroji. Spolu 48 živých porovnaní z GitHubu a 48 z pracovného prostredia. Produkčný skin sa nemenil, Genius je vyradený.

## Výsledok z GitHub Actions

| Zdroj | Získaný text | Ostatné výsledky |
|---|---:|---|
| SuperMusic.cz | 0/12 | 8× JS medzistránka; 4× neoverená stránka |
| KaraokeTexty.sk | 7/12 | 3× bez presnej zhody; 2× nerozpoznaná stránka |
| KaraokeTexty.cz | 7/12 | 3× bez presnej zhody; 2× nerozpoznaná stránka |
| Akordy Kytary.cz | 2/12 | 10× bez presnej zhody |

KaraokeTexty.sk a .cz získali rovnakých sedem textov s rovnakými kontrolnými súčtami. Kytary získali Lucie a ABBA; spolu sa v tejto vzorke získal text k ôsmim rôznym skladbám. Nejde o odhad celkového pokrytia katalógov.

| Interpret – skladba | SuperMusic.cz | KaraokeTexty.sk | KaraokeTexty.cz | Kytary |
|---|---|---|---|---|
| IMT Smile – Úsmev a čaj | JS medzistránka | text, 863 znakov | text, 863 znakov | bez presnej zhody |
| Instinct – Dozadu | JS medzistránka | text, 1039 znakov | text, 1039 znakov | bez presnej zhody |
| Kali & Tina – Aj keby | neoverená stránka | bez presnej zhody | bez presnej zhody | bez presnej zhody |
| Láska – Mraky | JS medzistránka | text, 1454 znakov | text, 1454 znakov | bez presnej zhody |
| Dara Rolins – Sľub | JS medzistránka | text, 1570 znakov | text, 1570 znakov | bez presnej zhody |
| Peter Bič Project – Stromy | neoverená stránka | text, 1102 znakov | text, 1102 znakov | bez presnej zhody |
| Wanastowi Vjecy – Kapky krve | JS medzistránka | text, 1352 znakov | text, 1352 znakov | bez presnej zhody |
| Lucie – Chci zas v tobě spát | JS medzistránka | text, 1656 znakov | text, 1656 znakov | text, 1616 znakov |
| Lucie Vondráčková – Hodiny duchů | neoverená stránka | bez presnej zhody | bez presnej zhody | bez presnej zhody |
| Hana Horecká – Den a noc | neoverená stránka | bez presnej zhody | bez presnej zhody | bez presnej zhody |
| ABBA – Dancing Queen | JS medzistránka | nerozpoznaná stránka | nerozpoznaná stránka | text, 1133 znakov |
| Queen – Bohemian Rhapsody | JS medzistránka | nerozpoznaná stránka | nerozpoznaná stránka | bez presnej zhody |

## Dôležité hranice výsledku

SuperMusic vrátil vyhľadávacie stránky, ale otvorené stránky piesní vrátili iba JavaScriptovú medzistránku. Zvyšné štyri prípady zostali neoverené. Z toho nemožno vyvodiť, že na webe chýba text.

Pri ABBA a Queen parser KaraokeTexty nerozpoznal prijatú stránku. Označenie neznamená chýbajúcu skladbu v katalógu. Pri chýbajúcej presnej zhode sa nevkladá text iného interpreta alebo inej verzie.

Miestny beh mal veľa chýb spojenia a získal iba tri texty. Je vedený oddelene; nepredstavuje výsledok prijímača. Aktuálny test na prijímači sa nevykonal.

Úspešné získania z GitHubu trvali približne 1,3–2,0 s pre KaraokeTexty a 1,0–1,1 s pre Kytary. Tieto časy nie sú zárukou odozvy na inej sieti.

## Reprodukcia

Diagnostika: `diagnostics/compare-radio-lyrics-sources.py`. Používa rovnaké moduly identifikácie skladby a parsery KaraokeTexty/Kytary ako TEST12. SuperMusic má iba konzervatívny diagnostický parser.

```sh
python3 diagnostics/compare-radio-lyrics-sources.py
```

Výstup: `/tmp/warder-radio-source-comparison.json`. Podrobnosti oboch behov: `docs/RADIO-FOUR-SOURCE-COMPARISON.json`. Texty piesní ani tokeny sa do reportov neukladajú.
