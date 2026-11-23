# FullHDGlass – Warder Evolution 1.0.87

**Ostrá opravná verzia – 23. november 2026.** Vychádza z prijímačovo overenej opravy sťahovania SAT piconov vo verzii 1.0.86.4 (kontrolný balík), zachováva schválený vzhľad a všetky existujúce používateľské dáta.

## SAT picony: oprava sťahovania a úložiska

- **Opravená zavádzajúca chyba pri sťahovaní:** výber satelitných pozícií, rozlíšenia, farby a spôsobu aktualizácie sa teraz posudzuje oddelene od kontroly cieľového adresára. Pri neplatnej ceste sa zobrazuje zodpovedajúca chyba, nie nesprávna výzva na opätovný výber piconov.
- **Podpora existujúcej cesty FullHDGlass:** bezpečne rozpoznáva presný alias `/usr/share/enigma2/hdg17_files/picon` → `/usr/share/enigma2/picon`, ktorý používa Octagon SF8008. Podporuje aj presne určené adresáre skinu a bezpečné aliasy na skutočne pripojené HDD/USB. Ostatné nebezpečné systémové cesty a symlinky sa naďalej odmietajú.
- **Bez zbytočného upozornenia na internú flash:** pokiaľ je na zvolenom internom úložisku aspoň 512 MiB pracovného priestoru **nad** systémovou rezervou 64 MiB, sťahovanie začne priamo. Pri nedostatku miesta zostáva upozornenie a voľba iného úložiska; pri kriticky nízkom priestore pokračovanie nie je možné.
- **Zachovaná ochrana pred zaplnením:** veľkosť každého sťahovaného balíka, priestor na jeho spracovanie a systémová rezerva sa nezávisle kontrolujú pred sťahovaním a zápisom. Zostávajú SHA-256 overenie, bezpečné spracovanie PNG a automatické odstránenie dočasných archívov.
- **Bez presúvania a mazania:** existujúce picony, symbolické odkazy, zvolené cesty, nastavenia a prevádzkované SAT/radio balíky zostávajú zachované.

## Overenie na prijímači

Na **Octagon SF8008** používateľ potvrdil úspešné sťahovanie pre **19,2°E a 23,5°E**, picony **220 × 132, čierne**, režim **Synchronizovať s TV zoznamami**. Výsledok: **145 aktualizovaných piconov pre 19,2°E bez chýb** a **184 piconov pre 23,5°E**; obrazovka skončila hlásením „Sťahovanie dokončené“.

Následná zmena správania upozornenia pri dostatku miesta bola overená používateľom na tom istom prijímači: **„teraz top je OK“**. Automatické regresné testy pokrývajú hranice voľného miesta, interné a externé úložiská, symbolické odkazy aj regresie OpenATV/OpenPLi.

## Aktualizácia

Balík: `enigma2-plugin-skins-fullhdglass_1.0.87_all.ipk`.

Oficiálny release a produkčný aktualizátor sa potvrdzujú až po úspešnom publikovaní a následnom koncovom overení. Táto poznámka nie je sama osebe dôkazom publikovania.

Po aktualizácii reštartujte Enigma2.
