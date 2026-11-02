# FullHDGlass 1.0.62-test3 — OpenPLi / OpenATV TEST

Samostatný testovací IPK pre OpenPLi 9.2 a vývojovú vetvu s Pythonom 3. Obsahuje aj doterajšie úpravy pre OpenATV 8.1 / GLES / WQHD z prijímačom overeného test2. Hlavný skin zostáva vo Full HD. OpenPLi 8.x/Python 2 nie je cieľom tejto zostavy.

- Opravených 29 väzieb natívnych tlačidiel a textov v OpenPLi, vrátane zoznamu kanálov, časovačov, ladenia a prehliadača pluginov.
- OpenPLi používa kompletnú virtuálnu klávesnicu so zadaním, jazykom a farebnými tlačidlami.
- Staré funkcie skinu neprepisujú systémové Menu.py, ChannelSelection.py, ServiceScan.py ani encoding.conf na OpenPLi.
- Úprava pracuje iba s vlastnými šablónami FullHDGlass v pamäti. OpenATV, ostatné skiny a používateľské prekrytia zostávajú zachované.

Pred zverejnením musia prejsť natívne kontroly OpenPLi release-9.2/develop, kontroly OpenATV 8.0/8.0-next/master, regresie ovládačov, kontrola každého súboru IPK a skutočná zabalená funkcia poinštalačného overovania. Súbory architektúrnych bitrate helperov a grafika ostávajú overené; produkčné aktualizácie sa nemenia.

Nahraj IPK do /tmp a nainštaluj presný súbor:

```sh
opkg install /tmp/enigma2-plugin-skins-fullhdglass_1.0.62-test3_all.ipk
```

Po úspešnej inštalácii reštartuj GUI. Na OpenPLi skontroluj prvé spustenie, zoznam kanálov a jeho farebné tlačidlá, virtuálnu klávesnicu, časovače, prehliadač pluginov a ladenie. Ide o TEST: fyzické overenie OpenPLi, displeja prijímača a GLES/WQHD výstupu ešte čaká.

PiconHub 0.1.39-test2 a GSU 13.41-r1 TEST pri tejto kontrole nepotrebovali zmenu runtime; používajú sa už pripravené balíky. Ďalšia ostrá verzia FullHDGlass bude najmenej 1.0.63 po prijímačovom potvrdení. Existujúce verejné IPK sa neprepisujú.
