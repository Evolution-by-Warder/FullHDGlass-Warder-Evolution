# TEST1 nepoužívať — hlásené zahltenie rádia

Majiteľ hlási vážne spomalenie alebo neovládateľnosť GUI po prepnutí na rádio.
TEST1 má príliš nákladné vykresľovanie equalizéra cez jednotlivé eCanvas segmenty.

Opravený pohyblivý renderer používa pripravené priehľadné snímky, jeden ePixmap
update za 100 ms, jednorazový timer a zdieľanú ohraničenú cache.

Použite [FullHDGlass 1.0.40-test2](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/radio-spectrum-1.0.40-test2)
na overenie opravy v prijímači. Stabilná produkčná verzia zostáva 1.0.39.

Historické súbory TEST1 sú ponechané iba pre dohľadateľnosť vydania a analýzu chyby.
