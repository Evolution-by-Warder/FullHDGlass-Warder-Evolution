# FullHDGlass Warder Evolution — TEST264

Oprava neviditeľného obsahu aktualizačného okna. Text otázky, nová verzia, popis zmien aj priebeh aktualizácie sa zobrazujú nad nepriehľadným pozadím. Zachované natívne potvrdenie Áno/Nie, časovač a bezpečné overenie balíka. Malé IPK a samostatné náhľady zostávajú zachované.

Príčina: ScrollLabel posúva zPosition na vnútorný text, jeho vonkajší kontajner zostával pod panelom. Oprava nastavuje vrstvu aj na kontajner. Fyzický test prijímača nie je deklarovaný.
