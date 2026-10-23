# FullHDGlass Warder Evolution — nastavenia TEST252

Opravuje zvyšky delených rámov viditeľné v TEST251 na prijímači.

- Úvodná obrazovka zostáva rozdelená: TV náhľad a nápoveda vľavo, ponuka vpravo.
- Každá skupina nastavení používa jeden súvislý nepriehľadný panel. Oba úvodné panely aj ich rámiky sa pri vstupe skutočne skryjú, pri návrate obnovia.
- Ponuka sťahovania: zoznam je vykreslený nad nepriehľadným panelom, aby pozadie nezakrývalo dostupné položky.
- Nápoveda a náhľady zostávajú v spodnej časti spoločného panela. Existujúce nastavenia, klávesy, ukladanie a zrušenie zostávajú zachované.
- Bez zmien infobarov, rádia, EPG, kanálov, grafických súborov a aktualizačných feedov (stále 1.0.15).

## Inštalácia

```sh
opkg install /tmp/enigma2-skin-fullhdglass17-warder-evolution_1.0.16-test252_all.ipk
```

Potom reštartovať GUI. Overiť úvodné menu, vstup do EXTRA INFOBAR, INFOBAR/EXTRA INFOBAR, HDD/SSD a ďalších skupín, návrat a opakovaný vstup. V nastaveniach nesmie zostať stredová medzera, delené horné ani spodné rámiky. Vyskúšať uloženie aj zrušenie a náhľady.

## Kontroly a hranice

12 kontrol vrátane opakovaného prepnutia panelov, skutočného zapojenia prepínania a kontroly zmien ukladacej logiky. Pôvodný zmrazený AST základ z 1.0.15 sa nemení; odfiltrované sú iba presne definované príkazy prezentácie. Ďalej runtime-safety, schválený rádiový/grafický základ, verzie a úplné overenie obsahu IPK. Prijímačové zobrazenie TEST252 zatiaľ nie je potvrdené.

Systémové MessageBox/ChoiceBox/InputBox zostávajú mimo tejto opravy. Historická textová asercia v tools/test-r12-regressions.py zlyháva už na nezmenenej 1.0.15, ako je uvedené v poznámkach TEST251.
