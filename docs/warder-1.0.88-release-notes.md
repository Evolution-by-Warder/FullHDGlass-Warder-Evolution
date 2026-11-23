# FullHDGlass – Warder Evolution 1.0.88

**Ostré opravné vydanie – 23. november 2026.** Rozsah výslovne schválil vlastník po hlásení českého používateľa. Zahŕňa výhradne korekciu prekrytia názvov nastavení a posuvníkov v natívnych nastavovacích oknách Enigma2. Zachováva všetky funkcie a balíky z 1.0.87.

## Oprava natívnych nastavovacích okien

- V oknách **Nastavení korekce obrazu** (natívne `VideoEnhancementSetup`) a **Nastavení displeje** (natívne `Setup`) sa dlhé české názvy nastavení prekrývali s posuvníkmi jasu, ostrosti a ďalších parametrov.
- Pôvodný natívny `Components.ConfigList` používal pri širokých obrazovkách príliš krátky, zvyčajne 200 px, odstup medzi názvom a hodnotou. FullHDGlass používa väčšie písmo a preklady rôznej dĺžky.
- Pomocník `warderNativeConfigSpacing.py` po natívnom `applySkin` upraví odstup **len v zoznamoch širokých najmenej 1200 px**: 55 % skutočnej šírky pre názov a najmenej 450 px pre hodnotu/posuvník.
- Úzke obrazovky a náhľady (vrátane 825 px `VideoEnhancementPreview`) majú pôvodné správanie. Režim je idempotentný, bezpečne ignoruje nepodporované API a aktivuje sa len pri používaní `hd_glass17/skin.xml`.
- Nemenia sa systémové súbory image, nastavenia používateľa, preklady, picony, menu, grafika ani fungovanie ovládacích tlačidiel.

## Overenie a rozsah vydania

- Podklad: dve snímky českého používateľa; model prijímača a verzia image neboli potvrdené. **Opakované vizuálne overenie u daného používateľa ešte neprebehlo**; neoznačovať za test prijímača.
- Kontrolný **1.0.88-test1**: [GitHub Actions #45249486600](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/45249486600), 6/6 cielených regresných testov a overený obsah IPK/SHA-256.
- Zmeny pripravené v [PR #157](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/pull/157). Automatické kontroly OpenATV/OpenPLi, bezpečnosti a integračného balíka sú povinné na presnom finálnom HEAD pred zlúčením.
- Predchádzajúca **1.0.87** ostáva schválenou východiskovou verziou: úspešne overené sťahovanie SAT piconov a bezpečná kontrola voľného miesta na SF8008.

## Aktualizácia

Balík: `enigma2-plugin-skins-fullhdglass_1.0.88_all.ipk`.

Oficiálny GitHub Release, kontrolný súčet publikovaného IPK a produkčný/testovací aktualizačný kanál musia byť potvrdené až po úspešnom kanonickom publikačnom workflow. Tento dokument nie je dôkazom hotového publikovania.

**Po inštalácii reštartujte Enigma2.**
