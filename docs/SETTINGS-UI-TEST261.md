# FullHDGlass by Warder — TEST261

Spoločná dávka odsúhlasených úprav nastavení, nadväzujúca na používateľom overený TEST260.

- Konfigurácia je iba v Pluginoch ako **Konfigurácia FullHDGlass**; pôvodná položka v Nastaveniach zmizne.
- Verzia sa zobrazuje iba vpravo hore v spoločnom banneri.
- Ponuka sťahovania má menšie priehľadné obrázky a deväť viditeľných riadkov.
- Vlastné výbery, vstupy a hlásenia používajú jednotný nepriehľadný dizajn vrátane aktualizácie a resetu.
- História obsahuje aktuálne zmeny Warder; Zatvoriť je vycentrované pod rámom.
- Extra infobar: opravené označenie typov a podklad náhľadu; zoznam typov ikon je vycentrovaný.
- OLED výber sa otvorí bez kontroly 7zip. Pri sťahovaní sa potrebný pomocník pripraví pred archívmi; rozpoznáva sa aj systémový 7zz/7z/7za.
- Bezstratová kompresia PNG pri zostavení zachováva všetky pixely, rozmery a metadáta. Veľké pracovné obrázky sa nepribaľujú.
- Zachované svižné asynchrónne načítanie nápovedy z TEST259.

Inštalácia: skopírovať IPK do /tmp, nainštalovať cez opkg a reštartovať GUI. Následne otvoriť **Pluginy → Konfigurácia FullHDGlass**.

Kontroly na zostavovacom stroji nenahrádzajú skúšku na prijímači. Overiť výbery, zrušenie bez uloženia, aktualizačné a resetovacie okná, OLED výber a čitateľnosť náhľadov. Produkčný aj testovací automatický feed zostávajú na 1.0.15; táto verzia je samostatný kandidát na overenie celej dávky.
