# Kontrola inštalácie a aktualizácií — 31. 10. 2026

Pri FullHDGlass sa podarilo zopakovať konkrétnu chybu prvej inštalácie: skript preinst odmietol priamu výmenu pôvodnej 9.50-r12.2 za nový názov balíka, vyžadoval starší medzikrok 1.0.18 a opkg zanechal nový balík ako half-installed. Pôvodný balík už dotaz status nevrátil. Druhá reinštalácia potom prešla. Rovnaký výsledok nastal s force-reinstall aj bez neho.

Test používa skutočné opkg 0.10.0 a libsolv 0.7.40, rovnako ako v poskytnutej fotografii. Dáta sú malé izolované testovacie balíky; pôvodné skripty sú presmerované do dočasného koreňa a chránené kontrolou PKG_ROOT. Pôvodná r12.2 je používateľom dodaný archív. Nejde o plnú inštaláciu produktu ani o test na prijímači. Samostatné zmiznutie skin.xml z pôvodného hlásenia nemožno bez pôvodného výpisu transakcie pripísať tomuto testu ako definitívne vysvetlené.

## Pripravená oprava

Preinst dovolí priamy prechod iba z overenej 9.50-r12.2, pri argumente upgrade, s presným kontrolným súčtom pôvodného postrm a bez neznámeho prerm. Tento postrm pri upgrade nič nemaže. Pri neznámom odstraňovaní zostáva ochrana aktívna. V opravenom teste prvý pokus skončil install ok installed, obsah nových súborov sedel a nastavenia zostali zachované.

Postinst po novom overí prítomnosť potrebných súborov a platný skin.xml. Aktualizátor po skončení opkg overí aj presnú verziu a úplný stav balíka; samotný súbor version už nestačí. Existujúca cesta pre dpkg zostáva podporená. Kontrola nepridáva logy ani trvalý proces.

## PiconHub a GSU

PiconHub sa v izolovanom teste z pôvodnej 5.0.240904 nainštaloval na prvýkrát aj bez force-reinstall. Jeho hlásená chyba teda zostáva neobjasnená; nie je dôvod naslepo pridávať force-overwrite. V samostatnej vetve PiconHubu je pripravené overenie potrebných súborov a konečného stavu balíka. Tým sa zamedzí falošnému hláseniu úspechu pri neúplnej inštalácii.

Aktuálny GSU má vlastný overovaný prechod s návratom k predchádzajúcemu balíku pri chybe. Jeho zdroj nebol menený.

## Overenie a stav vydania

Prešlo 77 zameraných testov skinu a 45 testov PiconHubu. Starší test-r12-regressions.py má už v nezmenenom základe neaktuálne očakávanie adresy update.json; aktuálny aktualizátor používa update-production.json. Táto historická kontrola preto neprešla a nebola prepísaná. Súvisiace aktuálne testy aktualizátora, kontrola nemennosti ostatných riadiacich funkcií a kontrola bytecode prešli.

Presné vstupy, priebeh pred/po a obmedzenia sú v [reports/install-transition-20261031](../reports/install-transition-20261031). Žiadny nový produktový IPK nebol vytvorený ani vydaný, verejné balíky a aktualizačné kanály sú nezmenené. Trezor zostal nedotknutý.
