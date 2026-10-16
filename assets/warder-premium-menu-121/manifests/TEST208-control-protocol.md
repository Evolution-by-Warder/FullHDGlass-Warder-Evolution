# TEST208 — kontrolný protokol grafík

- Vstup: 121 PNG z `WARDER_121_ORIGINALY_JEDNOTNE_POZADIE_BEZ_DEGRADACIE(1).zip`; schválený doplnkový obrázok `Prehliadac_pluginov.png` z `WARDER_6_SAMOSTATNYCH_810x810(1).zip`.
- Zdrojový skin XML definuje `background` ako `#31000000`, teda RGBA `(0,0,0,49)`.
- Z každej zo 121 PNG zmenené iba pixely jednotného okrajového pozadia `(0,0,0,128)` na `(0,0,0,49)`; RGB pixelov, rozmery 810 × 810, RGBA a obrazové detaily ostali zachované.
- V doplnkovom obrázku zmenené iba pixely jeho jednotného pozadia `(0,0,0,145)` na `(0,0,0,49)`.
- Výstup: 121 pôvodných ID-názvov + osobitný `PluginBrowser.png` (spolu 122 PNG) v každom archíve. `menuIcons.zip` používa koreň `menuIcons/1/`; `menuIconsBig.zip` používa `menuIconsBig/`.
- Manifest obsahuje 122 riadkov vrátane 121 unikátnych menu ID a samostatného schváleného `plugin_browser`. Zachované mapovania a ich pôvod sú uvedené v `mapping_provenance`; 6 vlastníkom schválených priradení ostáva označených `owner_approved_mapping`.
- menuIcons.zip: 71027419 B, SHA-256 `e7a75d03c7e38e2c3cc5eb3de0d58e0a5621a7cec71b1c495ee7e12bb855dae3`.
- menuIconsBig.zip: 71027663 B, SHA-256 `0d4873fb3a5b23f06c24e80d4b48428e2912dc530f8149a58b5b7b57e37660e7`.
- Každý archív sa prenáša ako 102 nadväzujúcich častí (každá najviac 700 000 B); po spojení majú presnú veľkosť a SHA-256 uvedenú vyššie.
- Pred pushom: všetky 122 PNG 810×810 RGBA, edge alpha 49, unikátne SHA-256; obe ZIP testované a obsahujú presne 122 PNG.
- GitHub Actions run `38941681552` prešiel: preflight, zostavenie IPK, kontrolu balíka a publikovanie TEST208. IPK SHA-256: `c437092ee2c312a8de9b8c3543d588905dba157e1a2d87be20c6671a413d7fb5`. Zmeny stabilnej vetvy `main` ani verzie 1.0.4 sa nerobili.
