# FullHDGlass Warder Evolution 1.0.31

- Opravené vyhľadávanie obalov slovenských a českých skladieb: namiesto implicitného amerického katalógu sa prehľadávajú katalógy SK, CZ a následne US.
- Meno interpreta a názov skladby sa porovnávajú aj bez diakritiky; celý názov a identita interpreta sa naďalej kontrolujú.
- Nesprávny výsledok „Protože to nevzdám“ pre „Život nás má rád“ sa odmietne. Zobrazenie obalu sa nepovažuje automaticky za dôkaz jeho správnosti.
- Vyhľadávanie zostáva na pozadí, úspešná zhoda zastaví ďalšie vyhľadávanie. Výpadok jedného katalógu neblokuje ďalší.
- RDS, prednosť DAB MOT, grafika a rozloženie rádia zostávajú zachované.

Overenie: 30 automatických testov metadát a obalov vrátane oboch nahlásených skladieb, nesprávnej skladby/umelca a výpadku katalógu. Živé sondy sú zapísané v RADIO-CATALOGUE-PROBES.json; nejde o fyzické overenie na prijímači. Úplné zostavenie a overenie balíka vykoná CI pred aktiváciou aktualizácie.
