# FullHDGlass – Warder Evolution 1.0.73

Spoločná stabilná verzia pre OpenATV a OpenPLi, vytvorená z testovanej vetvy **TEST12** (vrátane TEST11).

## Novinky a opravy

1. Dlhé názvy EPG v predvolenom ChannelSelection OpenATV sa skracujú podľa skutočnej šírky dostupného poľa.
2. Text nevstupuje do priestoru vyhradeného pre farebný progressbar, percentá alebo zostávajúci čas.
3. Dlhý názov práve vybranej udalosti sa plynulo posúva, aby bolo možné prečítať aj jeho koniec.
4. Rolovanie nezačína odznova po každej bežnej EPG aktualizácii.
5. Nová udalosť alebo skutočná zmena výberu resetuje animáciu na začiatok správneho textu.
6. Po úvodnej krátkej pauze sa rolovanie rozbehne bez predchádzajúceho zbytočného ďalšieho čakania.
7. Ostatné stanice zostávajú statické a ich dlhé názvy sú bezpečne skrátené.
8. Optimalizované prekresľovanie pri stojacom texte bez pridania ďalších grafických vrstiev.
9. Zachované pôvodné farebné bary, číselné indikátory, picony aj používateľská veľkosť písma.
10. OpenPLi 9.2: obnovený predvolený zoznam staníc, ktorý sa po TEST11 nezobrazoval.
11. OpenPLi používa natívny zoznam a natívne progressbary; experimentálny OpenATV renderer sa naň neaplikuje.
12. Zachované ostatné varianty ChannelSelection vrátane PIG 2/4/6, Prime Time, extra EPG a oprava rozloženia PluginBrowser.
13. Texty aktualizácie sú pripravené pre jazyk systému Enigma2 s angličtinou ako záložným jazykom.
14. Oprava je súčasťou obyčajného IPK. Žiadne úpravy binárnej Enigma2 ani C++ patch.

Tieto body rozpisujú jednotlivé aspekty potvrdených úprav; nepredstavujú štrnásť nezávislých chýb.

## Skúšky na prijímači (8. 11. 2026)

- **OpenATV 7.6 a 8.1, GigaBlue:** používateľ potvrdil plynulé listovanie, viditeľné progressbary a posúvanie vybraného dlhého EPG názvu.
- **OpenPLi 9.2, GigaBlue:** používateľ potvrdil návrat predvoleného zoznamu v TEST12. Natívne listovanie je subjektívne pomalšie než na OpenATV. Rolovanie dlhých názvov na OpenPLi nie je súčasťou tejto verzie.
- Režimy percent a zostávajúceho času boli kontrolované podľa diagnostických logov, nie všetky kombinácie sa overili snímkou.
- Súčasné správanie môže závisieť od verzie image, fontu, výšky riadkov a šablóny výberu staníc.

## Inštalácia a aktualizácia

Balík: `enigma2-plugin-skins-fullhdglass_1.0.73_all.ipk`  
Identita balíka: `enigma2-plugin-skins-fullhdglass-warder-evolution`  
Verzia: `1.0.73-1`

Po úspešnej inštalácii reštartujte GUI. Súčasné používateľské nastavenia a skiny zostávajú zachované.
