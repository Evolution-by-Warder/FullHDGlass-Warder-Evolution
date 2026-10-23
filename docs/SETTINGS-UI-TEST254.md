# FullHDGlass Warder Evolution — nastavenia TEST254

Oprava čierneho obdĺžnika a modrého fragmentu v spodnom strede hlavnej ponuky, nahlásených zo snímky prijímača.

- Plocha na náhľad farby je štandardne skrytá; zobrazí sa len pri výbere konkrétnej farby v nastaveniach. Pri návrate na bežnú voľbu sa skryje.
- Stredový text aktuálnej hodnoty je v úvodnom menu skrytý a jeho pozadie je zosúladené s pozadím obrazovky. V nastaveniach zostáva dostupný.
- Natívne kreslenie vzorky farby, ukážky dátumu a hodnoty zostávajú zachované. Náhľad používa vlastný úzky renderer odvodený od natívneho Canvas, bez globálnej zmeny ostatných obrazoviek.
- Zachováva opravy TEST253: rozdelené úvodné menu, jeden panel pre nastavenia a položky Ponuky sťahovania nad pozadím.

```sh
opkg install /tmp/enigma2-skin-fullhdglass17-warder-evolution_1.0.16-test254_all.ipk
```

Po inštalácii reštartovať GUI. Overiť čistý stred medzi Zrušiť/Uložiť, vstup do nastavení farieb, viditeľnú vzorku konkrétnej farby, bežnú voľbu a návrat do hlavného menu. Skontrolovať aj ukážky dátumu. Zobrazenie TEST254 na prijímači zatiaľ nie je potvrdené.

Kontroly: 14 testov vrátane skrytia pri štarte, skutočného callbacku kreslenia farby, opakovaného prepínania a zachovania pôvodnej konfiguračnej logiky. Ďalej runtime-safety, rádiový/grafický základ, verzie a úplná zhoda obsahu IPK so zdrojom. Aktualizačné feedy zostávajú 1.0.15. Systémové dialógy sú mimo tejto opravy.
