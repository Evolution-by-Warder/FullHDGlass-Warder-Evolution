# FullHDGlass – Warder Evolution 1.0.84 (aktuálna ostrá verzia)

**Oficiálne vydané 22. novembra 2026.** Aktuálny produkčný balík je `v1.0.84` pre kompatibilné OpenATV a OpenPLi. Pôvodné vydanie 1.0.73 uvedené v staršej verzii tohto dokumentu zostáva historickou poznámkou, **nie aktívnym odkazom na stiahnutie**.

## Opravy oproti 1.0.83

- Opravené načítanie konfigurácie na OpenATV 7.6 a OpenPLi 9.2 tam, kde staršie natívne `PluginDescriptor` nepodporuje `serviceFilter`.
- Zamedzené prekrytiu TV rádio vrstvou pri prepnutí služby na starších prijímačoch.
- Warder Radio Live pripraví samostatný bouquet aj bez nainštalovaného samostatného rádiového rozšírenia.
- Opravené kontextové menu výberu krajiny a ovládanie zoznamu po zmene krajiny na starších OpenATV/OpenPLi.
- Zachovaný aktuálny rádiový dátový katalóg **224 krajín, 48 219 staníc a 40 837 pôvodných rádiových log**; veľké country ZIPy zostávajú na zvolenom externom úložisku.

## Aktuálna inštalácia a bezpečný návrat

[Oficiálny GitHub Release 1.0.84](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/v1.0.84) · [Priame stiahnutie IPK 1.0.84](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/download/v1.0.84/enigma2-plugin-skins-fullhdglass_1.0.84_all.ipk) · [Úplné poznámky 1.0.84](warder-1.0.84-release-notes.md)

- **IPK:** `enigma2-plugin-skins-fullhdglass_1.0.84_all.ipk`
- **Veľkosť:** 18 389 618 B
- **SHA-256:** `623be902288bf1bc872425729d5a85596228d06593f022ff60b8572b23227591`
- **Produkčný feed:** `update-production.json` a hlavný `update-test.json` ponúkajú 1.0.84.
- **Návratové ostré verzie:** 1.0.83 / 1.0.82 / 1.0.80. Zhodné pôvodné Release assety zostávajú dostupné.
- **Chránené migračné výnimky:** 1.0.18 pre pôvodnú opkg identitu a 1.0.72 pre historický TEST updater, ktorý stále používa starú vetvu.

Existujúce nastavenia, picony, schválený layout a originálne grafiky zostávajú chránené. Pri prechode zo starého pôvodného balíka neobchádzajte bezpečný bootstrap 1.0.18; po aktualizácii reštartujte Enigma2. Fyzické overenie pôvodných opráv na OpenATV 7.6 a OpenPLi 9.2 je popísané v [oficiálnych poznámkach](warder-1.0.84-release-notes.md). Priame downgradovanie na ľubovoľnom prijímači nie je týmto dokumentom garantované; závisí od opkg a aktuálneho obrazu.

**Retencia vydaní:** najnovšie ostré + max. tri predošlé, prípadne overené nutné migračné výnimky. [Aktuálny spoločný checkpoint](ECOSYSTEM-CLEANUP-CHECKPOINT-20261123.md).
