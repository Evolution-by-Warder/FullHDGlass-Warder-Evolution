# FullHDGlass — prechod na nainštalované Balíčky vzhľadu

Vlastník 24. októbra 2026 výslovne schválil premenovanie inštalačného balíka. Vnútorné názvy súborov, adresárov a nastavení s číslom 17 sa v tejto úprave nemenia.

## Aktualizácia existujúcej inštalácie

1. V konfigurácii skinu potvrď migračnú aktualizáciu **1.0.18**. Tá ešte používa pôvodný identifikátor `enigma2-skin-fullhdglass17` a doplní ochranu používateľských súborov pri jeho výmene.
2. Po reštarte GUI otvor konfiguráciu a potvrď aktuálnu **ostré vydanie 1.0.84** z `update-production.json`. Nahradí pôvodnú opkg identitu za `enigma2-plugin-skins-fullhdglass-warder-evolution`. Historická prvá verzia nového balíka bola 1.0.19, ale už nie je potrebné ju inštalovať ako samostatný medzistupeň po pripravenom 1.0.18.
3. Po dokončení bude skin vo vlastnom zozname nainštalovaných balíkov OpenATV pod **Balíčky vzhľadu**. Odtiaľ ho možno štandardne spravovať a odstrániť.

Nejde o pridanie skinu do cudzieho online inštalačného feedu OpenATV. Zaradenie používa štandardný prefix skutočne nainštalovaného balíka, bez zásahu do systémového PluginBrowser.py a bez falošnej registračnej položky.

## Zachovanie stavu

Prechodná verzia 1.0.18 ešte pred odstránením pôvodného balíka uloží používateľské XML, príslušné pôvodné zálohy a migračný stav mimo balíkom vlastnených súborov. Nový balík overí SHA256 celého záznamu a obnoví súbory pred konfiguráciou skinu. Symbolické odkazy zostávajú odkazmi. Po úspechu sa dočasný záznam odstráni; pri chybe zostane na obnovu. Hlavný `/etc/enigma2/settings` sa tým neprepisuje.

`hd_glass17`, `setupGlass17`, generované XML a pôvodné kľúče nastavení zostávajú zachované. Pôvodný balík sa nahradí deklarovaným Replaces/Conflicts až po prípravnej verzii 1.0.18. Manuálne preskočenie priamo zo starej nepripravenej inštalácie na nový názov preinst odmietne.

## Aktualizačné kanály

**Aktuálna politika 23.11.2026:** starý `update.json` na `main` úmyselne naďalej ponúka migračnú 1.0.18 (zámerná výnimka, nie zastaraná omylom). `main/update-test.json` už ponúka overenú 1.0.84, rovnako ako `update-production.json`. Staršie nainštalované TEST verzie však majú samostatnú hardcoded URL `warder-modernization-work/update-test.json` (teraz 1.0.72); jej cieľový balík zostáva chránený, kým nebude migrácia TEST klientov overená. Po úspešnom prechode cez 1.0.18 sa ďalšie aktualizácie riadia produkčným manifestom. Tým existujúci používatelia nepreskočia krok potrebný na uchovanie svojich súborov.

Oba malé IPK sa zostavia a overia proti svojmu payloadu. Najprv sa zverejnia ich presné bajty, overí sa verejné stiahnutie a až potom sa naraz nastavia všetky tri manifesty. Kontroly pokrývajú kategóriu podľa názvu balíka, zachovanie XML/záloh/odkazov, odmietnutie chybných záznamov a poradie publikovania. Fyzický test tejto migrácie na prijímači zatiaľ netvrdíme.
