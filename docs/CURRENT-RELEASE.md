# FullHDGlass – Warder Evolution 1.0.85 (aktuálna ostrá verzia)

**Vydanie schválené vlastníkom 23. novembra 2026 po fyzickom teste TEST3 na GigaBlue Quad 4K Pro / OpenATV 8.1 + GLES.** Predchádzajúca stabilná verzia 1.0.84 zostáva zachovaná ako návratový bod.

## Hlavné opravy oproti 1.0.84

- **Výber kanálov / EPG:** odstránené prekrytie názvu stanice a názvu programu, rezerva pre natívny číselný stĺpec. Pri zmene počtu viditeľných staníc `14 ↔ 9` sa prepočítajú výšky riadkov a veľkosti piconov bez nutnosti zatvoriť zoznam; rolovanie EPG zostáva funkčné.
- **Nastavenia piconov:** väčší priestor na viacriadkovú nápovedu v natívnom okne `Setup`.
- **„Máš zvolené“:** v pôvodnom jednom riadku ostali Infobar, typ ikon, ikony menu, počasie a HDD/SSD; pribudlo číslovanie typu menu (`Menu: 1` = predvolené), typ výberu kanálov, EPG/GLES a informácie o fontoch.
- Diagnostický riadok začína na `x=15`, má šírku `1890 px` a font `Regular;23`. Celá cesta `HDD/SSD: /dev/sda` bola potvrdená na prijímači s TEST3.
- Zachované sú originálne grafiky, satelitné/radio picony, rádiové balíky, používateľská konfigurácia a kompatibilita z 1.0.84.

## Aktuálny produkčný balík a aktualizácie

[Oficiálny GitHub Release 1.0.85](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/v1.0.85) · [Stiahnuť IPK 1.0.85](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/download/v1.0.85/enigma2-plugin-skins-fullhdglass_1.0.85_all.ipk) · [Úplné poznámky](warder-1.0.85-release-notes.md)

- **Balík:** `enigma2-plugin-skins-fullhdglass_1.0.85_all.ipk`.
- **Veľkosť IPK:** 18 392 206 B.
- **SHA-256:** `f9f4af368cc2b7b6474dbde80f44a27c989de7c687b35e896bcf8af042c536d7`, overené vo verejnom Release assete, v `main/packages/*.sha256` aj v oboch produkčných manifestoch.
- **Oficiálny publisher:** [GitHub Actions #45179558117](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/45179558117) SUCCESS vrátane koncového `verify-production-release-state.py`. Aktuálny publikovaný main `313050910d2f4beefb2d6ceaaac303a869d3e83b`.
- **Aktuálne feedy:** `update-production.json` a `update-test.json` zobrazujú rovnakú overenú ostrú verziu po dokončení publikácie. `update.json` naďalej slúži ako migračný most 1.0.18.
- **Návratové ostré verzie:** v1.0.84 / v1.0.83 / v1.0.82; chránená 1.0.18 a starý TEST bridge 1.0.72 sa nezapočítavajú do štyroch stabilných dvojíc.

Po aktualizácii **reštartujte Enigma2**. Fyzické prijímačové potvrdenie tohto vydania je z GigaBlue/OpenATV 8.1; zábery samostatnej opravy textu Picon Setup na každom modeli Solo 4K neboli dodané.

**Kontrola skutočne publikovaného balíka/feedu:** `tools/verify-production-release-state.py` a oficiálny vydávací workflow. [Pracovný PR #151](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/151).
