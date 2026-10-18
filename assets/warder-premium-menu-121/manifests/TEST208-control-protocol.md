# TEST208 — opravený kontrolný protokol grafík

- Zdroj: `WARDER_121_ORIGINALY_JEDNOTNE_POZADIE_BEZ_DEGRADACIE.zip`; obsahuje presne 121 PNG s pôvodnými ID-názvami vrátane `manage_plugins.png`. Samostatná položka `plugin_browser` a obrázok ovládača zo šesťobrázkového archívu sa nepoužívajú.
- Parameter načítaný priamo z `source/package-root/usr/share/enigma2/hd_glass17/skin.xml` na pracovnej vetve `warder-modernization-work` (HEAD pri overení: `b7a33874b365428187cfad10449b53bec71942a2`): `<color name="background" value="#31000000" />`. Menu obrazovky používajú `backgroundColor="background"`.
- Skin farbu zapisuje AARRGGBB; jej PNG RGBA ekvivalent je `(0,0,0,49)` (0x31 = 49). Renderer berie priečinok ikon z `config.plugins.setupGlass17.par39.value + '/menuIconsBig/'`; `par39` je cesta, nie hodnota alfa kanála.
- V každej zo 121 grafík sa zmenili iba presné okrajovo spojené pixely pozadia `(0,0,0,128)` na `(0,0,0,49)`. Rozmery 810×810, RGBA aj všetky ostatné pixely zostali nezmenené.
- `menuIcons.zip`: 121 PNG, 63864790 B, SHA-256 `3a2b1f9c5d4537023bf7b935385a82191227b3c18113361bdc391f623cf79c2d`.
- `menuIconsBig.zip`: 121 PNG, 63865032 B, SHA-256 `232b982d06374c9cca7f481288c095a72260fbb5ed8dd077972383cafad0ade0`.
- Archívy používajú prenos po častiach: 700 000 B na časť, 92 častí na každý ZIP; `downloads.json` uvádza aktualizovanú veľkosť, SHA-256 a URL všetkých častí.
- TEST208 IPK kód nemením: jeho downloader číta `assets/warder/downloads.json` z pracovnej vetvy, takže stiahne opravené archívy bez zásahu do stabilnej verzie 1.0.4 alebo vetvy `main`.
- Lokálna kontrola: ZIP CRC OK; 121/121 PNG 810×810 RGBA; pozadie alpha 49; žiadna zmena mimo pozadia; manifest má presne 121 menu ID.
