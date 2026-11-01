FullHDGlass 1.0.60-test1 opravuje orezávanie posledného riadka dlhých ponúk.

Spoločné nastavenia kanálov, zvuku, titulkov a jazykov používali výšku zoznamu 615 bodov pri riadkoch po 45 bodoch. Posledný neúplný riadok sa preto vykreslil iba čiastočne. Zvislé zoznamy teraz využívajú iba celé riadky podľa ich skutočnej výšky po aplikovaní mierky obrazovky. Kontrola sa opakuje po dokončení rozloženia, keď plugin môže zmeniť výšku riadka.

Rovnaká úprava platí pre ďalšie ponuky a pluginy používajúce spoločné komponenty pod FullHDGlass. Kontrola všetkých zabalených XML a doslovných definícií obrazoviek našla 243 zvislých zoznamov s určenou výškou riadka, z toho 79 s neúplným posledným riadkom. Vodorovné zoznamy, mriežky a osobitné rozostupy sa nemenia.

Krátke hlavičky vrátane cesty v zozname kanálov zostávajú v jednom riadku, aby dlhý text nevytváral odrezaný druhý riadok. Úplný zdrojový text názvu sa zachováva; na konci úzkeho poľa môže byť horizontálne skrátený. Viacriadkové popisy zostávajú viacriadkové.

Hostiteľské testy používajú skutočné Python triedy GUIComponent a MenuList z overenej verzie OpenATV. Natívne vykresľovanie a navigačný backend nahrádza testovacia maketa. Zobrazenie na prijímači treba potvrdiť.

Toto je samostatná testovacia verzia nad 1.0.59. Aktualizačné profily sa týmto zostavením nemenia.
