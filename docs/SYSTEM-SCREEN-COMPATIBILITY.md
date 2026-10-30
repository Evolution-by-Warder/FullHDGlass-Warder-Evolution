# Kompatibilita systémových obrazoviek

Skin pri vlastnej definícii systémovej obrazovky preberá zodpovednosť za zobrazenie údajov, ktoré posiela Enigma2 alebo plugin. Názov okna nenahrádza popis vstupného poľa. Pri úpravách treba porovnať komponenty s aktuálnym ovládačom OpenATV.

## Virtuálna klávesnica

Od 1.0.43 sú povinné testy proti overenému aj aktuálnemu ovládaču OpenATV. Overujú komponenty prompt, text, list, mode, locale, štyri farebné klávesy a TEXT/INFO/HELP. Samostatné pole language je vedome vynechané: locale v ovládači zobrazuje názov jazyka aj krajiny.

Zmena množiny alebo typu zobrazovaných komponentov v aktuálnom OpenATV zastaví zostavenie a vyžaduje kontrolu kompatibility. Kontrola porovnáva aj alias výšky písma, rozmery dielov podkladov, umiestnenie prvkov a presnú pixelovú zhodu rozdelených klávesov.

Vstupné údaje, ich maskovanie a tlačidlové akcie obsluhuje systémová klávesnica. Skin ich nesmie duplikovať, zapisovať ani nahrádzať vlastným prihlasovacím ovládačom. Testy používajú len ukážkové názvy polí.

Kontrolný záznam: design/virtual-keyboard/compatibility.json. Test: tools/test-virtual-keyboard.py. Povinné spúšťanie: .github/workflows/build-settings-ui.yml. Kontroly sa spustia pri zmene definície obrazovky, klávesovej grafiky, testov a príprave každého nového vydania.

Táto automatická kontrola pokrýva spoločnú klávesnicu. Nové alebo meniace sa definície iných systémových obrazoviek majú dostať vlastnú kontrolu rozhrania; nemožno predpokladať, že starý skin zobrazí nové polia automaticky. Ostatné rozloženie a grafiku chráni pôvodný rádiový kontrolný súčet, pričom je presne vyčlenená iba táto oprava klávesnice.
