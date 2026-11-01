# FullHDGlass 1.0.54-test4

Testovací balík pre OpenATV: rýchlejší nábeh bitrate a samostatné ARM, MIPSel a AArch64 pomocné programy.

ARM meranie z TS bolo potvrdené na používateľovom GigaBlue v test3 (Das Erste HD, video 12015 kb/s, audio 514 kb/s). Tento balík začína video merať priamo z TS; pri ovládači bez podpory TS skúsi PES. Odstránené je pevné osemskundové čakanie aj čakanie na tri nulové video vzorky. Krátka kontrola čaká na platné PID-y a demux, najviac 20 pokusov po 250 ms. Úvodné nulové vzorky nenahrádzajú stav spúšťania. Prvá číselná hodnota musí pochádzať zo skutočného merania.

- ARM: nahradený pôvodný btrGen17-arm; jeho súbor a štartovacie kopírovanie boli odstránené.
- MIPSel: samostatná statická zostava pre MIPS32r2. Runtime kontroluje ISA, little endian, minimálny kernel podľa ABI poznámky binárky a potrebu FPU podľa emulačných testov 24Kc/24Kf. Staršie alebo nerozpoznané stroje používajú pôvodný MIPS program, ktorý je naďalej potrebný.
- AArch64: samostatná statická zostava a rozpoznávanie 64-bitového ARM pre ONE/TWO. Ak natívny kalkulátor nemožno spustiť, dostupný nový externý program môže prevziať meranie.
- SH4: pôvodná používaná vetva ostáva zachovaná.
- Voliteľný natívny kalkulátor má zachovanú prioritu.
- Každé zostavenie balíka vyžaduje správne pomocné programy a kontrolné súčty ich C zdroja; nemožno omylom vydať balík bez nových bináriek.

## Overenie
Runtime, čakanie na PMT, nulové úvodné vzorky, výber architektúry, kompatibilita MIPS, natívny fallback, skutočný C program v simulátore DVB, TS parser a jednotlivé ARM/MIPSel/AArch64 zostavy pod QEMU. Zostavenie a emulácia nenahrádzajú fyzickú skúšku MIPS alebo Dreamboxu. Rozsah tejto verzie je OpenATV.

Po inštalácii cez /tmp reštartujte GUI. Overte prvú hodnotu bitrate a prepnutie stanice. Pri probléme pošlite /tmp/fullhdglass-bitrate.json pred ďalším prepnutím.

Verejné aktualizačné kanály sa nemenia. Existujúce verejné IPK ostávajú nezmenené.
