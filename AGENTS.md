# Warder Evolution

## Trvalé pravidlo dokončovania schválenej práce (22. 11. 2026)

Toto pravidlo výslovne požadoval vlastník pre **všetky projekty Evolution-by-Warder**. Je nadradené starším všeobecným formuláciám o opakovanom schvaľovaní každého merge, IPK a produkčného zápisu.

1. **Jedno schválenie na konkrétny rozsah.** Ak vlastník schválil pomenovanú úpravu, celú dávku, vydanie alebo vopred definovanú automatickú aktualizáciu, súhlas zahŕňa aj obvyklé dokončovacie kroky v tomto rozsahu: vytvorenie PR, absolvovanie povinných testov, zlúčenie do `main`, zostavenie/vydanie príslušného finálneho balíka (ak projekt balíky vydáva) a aktualizáciu produkčného kanála. **Nepýtaj sa znovu na ten istý súhlas pri každom kroku ani v novom chate/Worku.** Rozsah a zdroj schválenia zapíš do PR a projektového denníka.
2. **Dokončenie po úspešnej verifikácii.** Pokiaľ rozsah zahŕňa produkčné vydanie a všetky povinné relevantné CI/regresné testy prejdú, bezpečne dokonči merge → release → verifikáciu skutočne publikovaného artefaktu/SHA-256 → aktualizáciu produkcie. Ak je nastavená schválená automatizácia, nech postup vykoná ona. Nevydávaj zbytočné medziverzie a nenechávaj hotové, schválené PR otvorené iba kvôli opakovanému žiadaniu.
3. **Žiadne neautorizované rozšírenie.** Test-only/draft, nová neschválená funkcia, zmena schválenej grafiky, neoverená licencia, zásah do súkromných dát, mazaní/zálohovaní či zmena autentifikácie nesmú byť ticho považované za schválené na produkciu. V týchto prípadoch si vyžiadaj jedno nové konkrétne schválenie.
4. **Povinné stop-podmienky.** Zlyhané alebo neúplné CI, zmena očakávaného SHA, nejasná identita artefaktu, konflikt vetvy, nedostatočné oprávnenia, bezpečnostná chyba alebo neoverená publikácia blokujú merge/vydanie. Skutočný stav a blokáciu zapíš; nikdy netvrď, že automatický merge či release prebehol, ak nie je doložený na GitHube.
5. **Trvalé odovzdanie.** Každý nový chat/Work načíta tieto pravidlá, aktuálny `main`, otvorené PR, CI, posledné vydanie a projektový register. Pokračuj od posledného overeného kroku a dokonči už schválenú prácu bez návratu na staré opakované schvaľovanie. Zachovaj používateľské súbory, existujúce schválené picony a históriu.

Toto je záväzné pravidlo práce vo všetkých repozitároch; **samo vloženie tohto textu nespúšťa GitHub automatizáciu**. Ak chýba mechanizmus automatického vykonania, odlíš pripravenú politiku od reálne aktivovaného workflowu.


## Pokračovanie práce

- Na začiatku nového chatu alebo Worku otvor koreňový [WARDER_PROGRESS.md](WARDER_PROGRESS.md) vo FullHDGlass-Warder-Evolution. Kým sa jeho dokumentačný PR nezlúči, použi najnovšiu verziu z jeho pracovnej vetvy.
- Pred pokračovaním porovnaj zaznamenané SHA s aktuálnym `main` vo FullHDGlass-Warder-Evolution a PiconHub-Warder-Evolution. Over aj príslušnú pracovnú alebo produkčnú vetvu, stav otvorených PR a dôkazy o vydaní. Pri rozpore rozhoduje aktuálny GitHub a doložené schválenia. Nadviaž na posledný overený krok.
- Po každej významnej zmene aktualizuj register ešte pred ukončením práce alebo odovzdaním chatu. Zapíš dátum, oblasť, repo a vetvu, SHA a odkazy, výsledok testov, rozsah schválenia, stav publikácie, blokácie a najbližší vykonateľný krok. Ak zmena čaká na schválenie, zaznamenaj ju na pracovnej vetve a odkáž na príslušný PR. Staršie míľniky ponechaj v histórii registra alebo v odkazovaných checkpointoch.
- Oddeľuj satelitné picony vrátane Vhannibala od piconov Warder Radio. Chráň schválené šablóny MASTER V9, grafiky, existujúce servisné referencie a používateľské nastavenia. Novú alebo zmenenú grafiku predlož na schválenie. Merge, publikovanie balíkov, vydanie IPK a zápis do produkcie patria do už schváleného rozsahu podľa trvalého pravidla; opakované schvaľovanie toho istého nie je potrebné.
- Podrobnosti k skinu a rádiu sú v [PROJECT-CONTINUITY.md](PROJECT-CONTINUITY.md), [projektovom checkpointe](docs/PROJECT-CHECKPOINT.md) a [rádiovom checkpointe](docs/RADIO-WORK-CHECKPOINT.md).

## Samostatný Warder Radio

- Samostatný plugin Warder Radio a jeho rádiové picony patria výhradne rádiovému Worku. Stav a pravidlá odovzdania vedie v [RADIO_PROGRESS.md](https://github.com/Evolution-by-Warder/Radio-Warder-Evolution/blob/main/RADIO_PROGRESS.md) a [rádiových pokynoch](https://github.com/Evolution-by-Warder/Radio-Warder-Evolution/blob/main/AGENTS.md).
- V spoločnom Worku sa riaď existujúcimi pravidlami pre skin, PiconHub a satelitné picony. Samostatný plugin a jeho rádiové balíky odovzdaj rádiovému Worku.

## Bezpečnosť GitHub prístupu, autentifikácie a nahrávania

- Na všetky projektové repozitáre používaj iba už schválené a autorizované GitHub pripojenia a podporované operácie. Bez výslovného predchádzajúceho súhlasu vlastníka nemeň spôsob autentifikácie, neprechádzaj na nové webové prihlasovanie, nevytváraj tokeny a nežiadaj heslá, jednorazové 2FA kódy ani iné prihlasovacie tajomstvá.
- Ak narazíš na obmedzenie prenosu veľkých alebo binárnych súborov, zastav len dotknutý prenos, zaznamenaj presnú príčinu, chybu a možné bezpečné riešenia. Nový spôsob prihlasovania či prenosu vyžaduje predchádzajúce výslovné schválenie vlastníka. Bežné technické rozhodnutia v rámci už povoleného spojenia môžu pokračovať.
- Neopakuj bez konca zlyhávajúce Base64 uploady ani autentifikačné pokusy. Ak nie je dostupný bezpečný schválený prenos, zachovaj existujúce výsledky a jasne odlíš lokálne pripravené archívy od skutočne nahraných a overených súborov.
- Pracuj na oddelených vetvách a pred každým zásahom over cieľovú vetvu, SHA-256 a integritu už schválených súborov. Nečakaná zmena hashov je blokácia, nie dôvod na automatické prepísanie. Produkčné zlúčenie a publikovanie vyžadujú preukázateľný súhlas s daným rozsahom; už udelený súhlas sa pri technickom dokončovaní neopakuje (pozri trvalé pravidlo vyššie).
- Po každej bezpečne dokončenej dávke ulož overiteľný commit a aktualizuj príslušný projektový register s presným SHA, rozsahom testov, stavom uploadu a zostávajúcimi nespracovanými výstupmi. Bez overenia vzdialeného súboru a hashov netvrď, že upload bol úspešný.
