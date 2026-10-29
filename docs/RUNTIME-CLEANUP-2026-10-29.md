# FullHDGlass — kontrola prevádzkových zápisov, 29. 10. 2026

Prejdený celý inštalovaný zdrojový runtime: **108 Python modulov**, inštalačné skripty a pomocné procesy. Pre každý modul je uložený SHA256 v sprievodnom JSON zázname. Kontrola zahŕňa výstup do konzoly, súborové logy, atómové zápisy, pracovné priečinky a správanie pri chybe. Vývojové skripty bežiace na PC/CI nie sú diagnostika prijímača.

- Vypnutých sedem starých Writelog zapisovačov: konfigurácia, dve počasia, dva menu renderery, poster a Menu-new17.
- Odstránené automatické logy OpenWebif a časovanie tlačidla RADIO; funkčný príznak režimu pre OpenWebif zostáva.
- Diagnostika textov sa na prijímači nezapisuje. Vývojový test ju musí výslovne zapnúť parametrom diagnostics=True; výstup JSON pre proces GUI je zachovaný.
- InfoBar inštalátor nevytvára home/root/logs; rozpracovaný zápis sa odstraňuje aj pri chybe.
- Opravené upratovanie screenshotov, čiastočného IPK, JSON cache a celého dočasného rozbalenia piconov.
- Privátna RAM cache obalov má limit 128 obrázkov / 32 MiB. PROGRAM INFO má osobitne 128 metadát / 2 MiB a 128 obrázkov / 32 MiB. Aktuálny súbor, odkazy a neznáme mená sa nemažú.
- Zdieľaný PiconHub Stage uprace aj zlyhanie vytvorenia pracovných podpriečinkov; kanonický modul zostáva byte-identický v oboch projektoch.
- Schválený equalizér: 84 stĺpcov × 3 px, medzery 1 px, priehľadnosť, 360 odtieňov, 350 × 126 px. TEST2 používa hotové snímky ePixmap namiesto segmentového eCanvas; pri skrytí sa animácia zastaví aj pri následnej zmene zdroja. Podrobnosti: RADIO-SPECTRUM-PERFORMANCE-2026-10-29.md.

Inštalačné kroky odstránia iba presne pomenované vlastné staré logy, ak ide o bežné súbory a nie symbolické odkazy. Neodstraňujú cudzie logy ani všeobecné priečinky. Nastavenia, nainštalované picony a používateľské obrázky zostávajú zachované.

Kandidát je určený na overenie v prijímači. Statická kontrola a simulované Enigma2 rozhrania nepotvrdzujú fyzické správanie na všetkých boxoch. Produkčné aktualizačné feedy zostávajú nezmenené. Žiadne tvrdenie o čistení už bežiaceho prijímača: zmeny sa uplatnia po inštalácii nového balíka.
