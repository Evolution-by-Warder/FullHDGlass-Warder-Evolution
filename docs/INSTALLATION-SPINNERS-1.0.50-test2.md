# FullHDGlass 1.0.50-test2

Testovacie vydanie obsahuje opravu prvého prechodu z overenej pôvodnej r12.2,
overenie dokončenej inštalácie, výber spinnerov a presnejšie rozpoznávanie mien
interpretov pri vyhľadávaní obalov a textov piesní.

Spinnery: Holubica, upravený modrý HDGlass - bakussa a online ponuka ďalších
animácií. V zozname je statický náhľad, názov a autor. Do prijímača sa sťahuje
iba vybraný ZIP. Pohyb používa natívny prehrávač Enigmy. Náhľady sú dočasné,
sťahované po stránkach a po zatvorení výberu sa odstránia. Uložené zostanú
najviac dva zvolené balíčky: používaný a pripravovaný. Holubica aj bakussa
fungujú bez internetu. Pôvodný archív autora bakussa je zachovaný bez úprav.

## Prvý test prechodu

1. Pred odinštalovaním aktívneho skinu zvoliť MetrixHD a reštartovať GUI.
   Zálohovať nastavenia a zaznamenať presnú pôvodnú verziu.
2. Pri testovaní prvého prechodu nainštalovať IPK bežným spôsobom cez pôvodnú
   verziu, bez force-reinstall a bez predchádzajúceho odstránenia starého balíka.
   Ak sa objaví chyba, zachovať celý výpis; neopakovať zatiaľ reinštaláciu.
3. Po úspechu reštartovať GUI, overiť výber FullHDGlass a zachovanie nastavení.
4. V konfigurácii skinu otvoriť Ostatné → Spinner. Overiť statické náhľady,
   autora, zrušenie výberu a výber jednej stiahnutej animácie. Výber aktivovať
   uložením nastavení a reštartom GUI. Overiť aj návrat na Holubicu bez internetu.

Priamy prechod je povolený len pre overený odinštalačný skript dodanej
9.50-r12.2. Neznámy starý skript zostáva chránený pred neoverenou výmenou.
Toto vydanie nie je tvrdením, že boli otestované všetky staré balíky a image.

Ostré vydanie, existujúce IPK a aktualizačné kanály sa nemenia. Nejde o ostrú
verziu. Overenie na fyzickom prijímači je účelom tohto vydania.
