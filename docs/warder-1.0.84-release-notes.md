# FullHDGlass – Warder Evolution 1.0.84

Ostré opravné vydanie schválené po fyzickom odskúšaní na **OpenATV 7.6** a **OpenPLi 9.2**. Zachováva funkčný režim OpenATV 8.1 a obsah verzie 1.0.83 vrátane originálnych rádiových balíkov.

## Opravy kompatibility starších Enigma2

- Opravené načítanie konfigurácie FullHDGlass a prehliadača pluginov na starších obrazoch, ktorých `PluginDescriptor` nepodporuje argument `serviceFilter`. Voliteľný kontextový záznam už nesmie zablokovať celý plugin.
- Zabezpečené skrytie natívnej rádio vrstvy pri prechode na televíznu službu na starších systémoch. Fungujúce správanie OpenATV 8.1 zostalo zachované.
- **Warder Radio Live** sa inicializuje a pripravuje vlastný bouquet aj bez nainštalovaného samostatného rozšírenia Warder Radio.
- Opravený prístup ku kontextovému menu výberu krajiny na OpenPLi 9.2 a OpenATV 7.6. Rozdielne natívne API zoznamu položiek sa spracúva bezpečne.
- Po výbere krajiny sa na starších obrazoch natívny rádio zoznam zavrie až po dokončení okna výberu; nedochádza k narušeniu ovládania farebnými tlačidlami. Preberanie a prepnutie krajiny prebieha ďalej na pozadí.

## Rádiové balíky a zachovanie dát

- Zostáva oficiálny podpísaný katalóg **224 krajín, 48 219 staníc a 40 837 originálnych rádiových log** z verzie 1.0.83.
- Zo servera sa sťahuje iba zvolená krajina a jej logá na nastavené externé úložisko `hdg17_files`; veľké dáta sa neukladajú do internej flash.
- Existujúce používateľské bouquets, picony, televízne a satelitné balíky, nastavenia skinu, grafika a režim 14-dňových aktualizácií zostávajú zachované.

## Overenie a inštalácia

Opravy na OpenATV 7.6 a OpenPLi 9.2 fyzicky odskúšal vlastník 22. novembra 2026. Automatické regresné testy pre staršie rozhrania a distribúciu sú povinnou podmienkou vydania. Fyzický test na konkrétnom zariadení nepredstavuje garanciu všetkých modelov a variantov obrazov.

Použite oficiálny IPK balík **1.0.84** alebo overený produkčný aktualizačný kanál. Po aktualizácii reštartujte Enigma2.
