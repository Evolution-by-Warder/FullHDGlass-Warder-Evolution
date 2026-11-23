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

**OVERENÉ A PUBLIKOVANÉ:** [Release v1.0.88](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/v1.0.88) z 23. 11. 2026 je verejný, nie draft ani prerelease. Oficiálny IPK má **18 394 974 B**, SHA-256 **`0da1f61a4e675ffc7b548d423430e9673230551d5bbc24e77598d5128d687c28`**. Oba aktualizačné kanály (`update-production.json`, `update-test.json`) ukazujú na 1.0.88 s identickým SHA-256 a desiatimi jazykovými textami. [Kanonický vydávací workflow #45252364033](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/45252364033) skončil **COMPLETED / SUCCESS** vrátane kontroly skutočne publikovaného stavu. PR #157 zlúčený, finálne 24/24 CI úspešných. Čaká sa už len na voliteľné následné snímky českého používateľa, nie na samotné vydanie.

**Po inštalácii reštartujte Enigma2.**
