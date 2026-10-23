# FullHDGlass Warder Evolution — nastavenia TEST251

Testovací balík **1.0.16-test251** zavádza spoločný štýl Warder Evolution do 11 vlastných nastavovacích obrazoviek. Vychádza zo stabilnej 1.0.15.

- Tmavomodré panely, tyrkysové línie, jednotné titulky a farebné tlačidlá.
- Hlavné menu s TV náhľadom, nápovedou, dátumom a živým časom so sekundami.
- Rovnaká vizuálna rodina pre menu sťahovania, družice, štýly, ikony, extra obrazovky, históriu/výsledky, mestá a priečinky.
- Všetky existujúce akcie, možnosti a ukladanie sú zachované. AST kontrola porovnáva riadiacu logiku s pôvodnou 1.0.15.
- Rádio, infobary, EPG, kanály, picony a schválené grafické súbory zostávajú nezmenené.
- Stabilný aj testovací automatický feed zostávajú na 1.0.15. Tento balík sa inštaluje ručne na overenie; nie je potvrdený prijímačom.

## Inštalácia na overenie

Stiahnuť konkrétny priložený IPK do /tmp a nainštalovať:

```sh
opkg install /tmp/enigma2-skin-fullhdglass17-warder-evolution_1.0.16-test251_all.ipk
```

Potom reštartovať GUI a otvoriť nastavenia FullHDGlass. Uloženie a zrušenie majú pôvodný význam a názvy. Počas prvého overenia stačí prejsť skupiny a skúsiť uloženie i zrušenie jednej bežnej voľby; nič sa automaticky neresetuje.

## Zatiaľ zostáva

Systémové MessageBox/ChoiceBox/InputBox, fyzické umiestňovacie obrazovky a OLED súhrny majú pôvodný vzhľad. Podrobnosti a ďalšie kroky sú v design/WARDER-UI-STANDARD.md.

## Kontroly

Deväť kontrol prezentácie/nezmenenej logiky, runtime-safety, zhodné grafické a XML súbory s potvrdeným rádiovým základom, verziovanie a úplné overenie každého bajtu IPK oproti zdroju. Starý tools/test-r12-regressions.py narazí na rovnakú textovú aserciu `fields[2].upper() in ("2", "A")` aj na nezmenenej 1.0.15; táto historická kontrola nie je vydávaná za úspešnú ani opravovaná ako súčasť úpravy vzhľadu.
