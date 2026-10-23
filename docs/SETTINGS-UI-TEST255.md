# FullHDGlass Warder Evolution — TEST255

Zobrazované názvy používajú FullHDGlass bez čísla 17. Aktualizované je označenie počasia v menu, titulok nastavení, reset nastavení (vrátane pôvodných prekladov), názov položky pluginu a text pre displej prijímača.

Názov inštalačného súboru je teraz bez 17:

```sh
opkg install /tmp/enigma2-skin-fullhdglass-warder-evolution_1.0.16-test255_all.ipk
```

Vnútorná identita balíka zostáva `enigma2-skin-fullhdglass17`, aby sa existujúca inštalácia aktualizovala na mieste. Technické priečinky, konfiguračné kľúče, gettext kľúče a pôvodné autorské záznamy zostávajú kompatibilné. Názov súboru IPK nemá vplyv na identitu balíka v opkg.

Spodné tlačidlá hlavnej ponuky majú rovnaké pozadie ako obrazovka, bez modrých obdĺžnikov. Farebné názvy a linky zostávajú.

Obsahuje aj všetky opravy TEST254: jeden panel pre nastavenia, rozdelené úvodné menu, viditeľné položky sťahovania a skrytý náhľad farby v hlavnej ponuke. Po inštalácii reštartovať GUI. Skontrolovať názvy v menu, resetovacom potvrdení a na displeji. Potvrdenie vzhľadu TEST255 na prijímači zatiaľ chýba. Aktualizačné feedy zostávajú na 1.0.15.
