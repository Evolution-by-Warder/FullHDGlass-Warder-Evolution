# Warder Evolution

## Pokračovanie práce

- Na začiatku nového chatu alebo Worku otvor koreňový [WARDER_PROGRESS.md](WARDER_PROGRESS.md) vo FullHDGlass-Warder-Evolution. Kým sa jeho dokumentačný PR nezlúči, použi najnovšiu verziu z jeho pracovnej vetvy.
- Pred pokračovaním porovnaj zaznamenané SHA s aktuálnym `main` vo FullHDGlass-Warder-Evolution a PiconHub-Warder-Evolution. Over aj príslušnú pracovnú alebo produkčnú vetvu, stav otvorených PR a dôkazy o vydaní. Pri rozpore rozhoduje aktuálny GitHub a doložené schválenia. Nadviaž na posledný overený krok.
- Po každej významnej zmene aktualizuj register ešte pred ukončením práce alebo odovzdaním chatu. Zapíš dátum, oblasť, repo a vetvu, SHA a odkazy, výsledok testov, rozsah schválenia, stav publikácie, blokácie a najbližší vykonateľný krok. Ak zmena čaká na schválenie, zaznamenaj ju na pracovnej vetve a odkáž na príslušný PR. Staršie míľniky ponechaj v histórii registra alebo v odkazovaných checkpointoch.
- Oddeľuj satelitné picony vrátane Vhannibala od piconov Warder Radio. Chráň schválené šablóny MASTER V9, grafiky, existujúce servisné referencie a používateľské nastavenia. Novú alebo zmenenú grafiku predlož na schválenie. Merge, publikovanie balíkov, vydanie IPK a zápis do produkcie vyžadujú výslovný súhlas.
- Podrobnosti k skinu a rádiu sú v [PROJECT-CONTINUITY.md](PROJECT-CONTINUITY.md), [projektovom checkpointe](docs/PROJECT-CHECKPOINT.md) a [rádiovom checkpointe](docs/RADIO-WORK-CHECKPOINT.md).

## Samostatný Warder Radio

- Samostatný plugin Warder Radio a jeho rádiové picony patria výhradne rádiovému Worku. Stav a pravidlá odovzdania vedie v [RADIO_PROGRESS.md](https://github.com/Evolution-by-Warder/Radio-Warder-Evolution/blob/main/RADIO_PROGRESS.md) a [rádiových pokynoch](https://github.com/Evolution-by-Warder/Radio-Warder-Evolution/blob/main/AGENTS.md).
- V spoločnom Worku sa riaď existujúcimi pravidlami pre skin, PiconHub a satelitné picony. Samostatný plugin a jeho rádiové balíky odovzdaj rádiovému Worku.

## Bezpečnosť GitHub prístupu, autentifikácie a nahrávania

- Na všetky projektové repozitáre používaj iba už schválené a autorizované GitHub pripojenia a podporované operácie. Bez výslovného predchádzajúceho súhlasu vlastníka nemeň spôsob autentifikácie, neprechádzaj na nové webové prihlasovanie, nevytváraj tokeny a nežiadaj heslá, jednorazové 2FA kódy ani iné prihlasovacie tajomstvá.
- Ak narazíš na obmedzenie prenosu veľkých alebo binárnych súborov, zastav len dotknutý prenos, zaznamenaj presnú príčinu, chybu a možné bezpečné riešenia. Nový spôsob prihlasovania či prenosu vyžaduje predchádzajúce výslovné schválenie vlastníka. Bežné technické rozhodnutia v rámci už povoleného spojenia môžu pokračovať.
- Neopakuj bez konca zlyhávajúce Base64 uploady ani autentifikačné pokusy. Ak nie je dostupný bezpečný schválený prenos, zachovaj existujúce výsledky a jasne odlíš lokálne pripravené archívy od skutočne nahraných a overených súborov.
- Pracuj na oddelených vetvách a pred každým zásahom over cieľovú vetvu, SHA-256 a integritu už schválených súborov. Nečakaná zmena hashov je blokácia, nie dôvod na automatické prepísanie. Produkčné zlúčenie a publikovanie vyžadujú výslovný súhlas.
- Po každej bezpečne dokončenej dávke ulož overiteľný commit a aktualizuj príslušný projektový register s presným SHA, rozsahom testov, stavom uploadu a zostávajúcimi nespracovanými výstupmi. Bez overenia vzdialeného súboru a hashov netvrď, že upload bol úspešný.
