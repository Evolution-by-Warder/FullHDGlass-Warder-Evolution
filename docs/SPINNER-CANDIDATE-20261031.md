# FullHDGlass 1.0.46-test1 — skúška pôvodného spinnera

Pôvodná 18-snímková holubica od Shamanna z používateľom dodaného balíka 9.50, prevedená na plnofarebné RGBA PNG s rozmerom 128 × 88 px. Všetky fázy majú rovnaký pomerný prevod a polohu, jemné alfa okraje a priehľadné pozadie. Náhľad v `design/spinner-repair/preview-128x88.gif` ukazuje skutočnú veľkosť a poradie snímok na kontrolnom pozadí.

## Čo sa opravuje

Pôvodný obrázok má 134 × 99 px a paletovú priehľadnosť. Hoci samotná paletová snímka je malá, stará PNG cesta v OpenATV vytvára 32-bitové pracovné obrazy na uloženie a skladanie pozadia. Ich 53 064 bajtov prekračuje štandardnú hranicu 48 000 bajtov, od ktorej sa môžu alokovať pre hardvérovú akceleráciu. Pri novom rozmere je snímka aj každý pracovný obraz veľký 45 056 bajtov; zostáva v CPU pamäti podľa overeného štandardného kódu. Tým odstraňujeme túto konkrétnu akcelerovanú cestu a paletový prevod, ktoré mohli súvisieť s poškodením obrazu.

Rozhodnutie alokátora bolo overené skompilovaním skutočnej funkcie z OpenATV, nie jej napodobeniny. Prešli aj kontroly snímok, kompresie, skladania/obnovy pozadia na CPU a bezpečného vypnutia kandidáta. Nie je to dôkaz odstránenia poruchy na fyzickom prijímači. Ten je potrebný pred riadnym zapnutím.

## Použitie

Nainštalovať krátky IPK `enigma2-plugin-skins-fullhdglass_1.0.46-test1_all.ipk` a reštartovať GUI pri aktívnom FullHDGlass. Súčasné OpenATV načíta snímky priamo z `/usr/share/enigma2/hd_glass17/spinner`. Nepoužíva sa stará voľba `par65`, presúvanie systémového spinnera ani odkazy `spinner-ori`.

Vyžaduje sa OpenATV s natívnym načítaním spinnera z aktívneho skinu (zmena `be4ff6f` z 25.10.2026). Ak existuje vlastný používateľský spinner v `/etc/enigma2/spinner`, má podľa OpenATV prednosť a kandidát ho nemení. V takom prípade sa pri skúške nemusí zobraziť holubica.

Pri bežnom zobrazení a zmiznutí spinnera overiť pohyb všetkých fáz a obraz pod ním aj po jeho zmiznutí. Skontrolovať prechod medzi TV a rádiom a ďalší štart GUI. Kandidát nepridáva zaťažovací test, časovače, diagnostické logy ani beh na pozadí.

## Vypnutie kandidáta

Spustiť iba pri potrebe návratu k spinneru image:

```sh
python /usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderSpinnerCandidate.py --disable
```

Potom reštartovať GUI. Nástroj odstráni iba 18 vlastných snímok po overení ich kontrolných súčtov a vlastný záznam. Zmenené súbory a symbolické odkazy odmietne, ostatné používateľské súbory ponechá. Nič nekopíruje do systémového spinnera.

## Zverejnenie

Samostatný testovací prerelease; bežný aktualizátor zostáva na overenej verzii 1.0.45. Pôvodný zdroj, pôvodná grafika 9.50 a výsledky kontroly sú zachované v tejto vývojovej vetve. Trezor sa nemení.
