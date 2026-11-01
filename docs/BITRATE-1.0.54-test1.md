# FullHDGlass 1.0.54-test1

Testovacia oprava merania bitrate pre všetky typy infobaru.

- Opravené odovzdanie parametrov pomocnému programu btrGen17 na ARM, MIPS a SH4.
- Výstup sa spracuje aj po menších blokoch a s rôznymi medzerami.
- Chyba spustenia, ukončenie procesu alebo chýbajúce údaje už nenechajú visieť „Spúšťanie bitrate“.
- Zachované prepínanie aktuálnej, priemernej, minimálnej a maximálnej hodnoty a nastavený limit.
- Zachované grafické podklady, nastavenia, DAB, spinnerové opravy a aktualizačné kanály.

Po inštalácii cez lokálny inštalátor IPK reštartujte GUI. Overte meranie na satelitnej a pozemnej stanici a po prepnutí kanála; preveriť aj rádio. Fyzické overenie na GigaBlue/DM920 ešte neprebehlo.

## Engineering evidence
OpenATV's lib/python/python_console.i passes execute(argv[0], argv+1) to the C++ container. That overload calls execvp with the supplied argv array. The old caller omitted the executable's argv[0], so ARM lost its adapter argument and MIPS/SH4 lost demux. The ARM helper's embedded usage is: usage: %s <adapterid> <demuxid> <pid> [..<pidN>].

Primary source: https://github.com/openatv/enigma2/blob/master/lib/python/python_console.i

tools/test-bitrate-runtime.py exercises the actual AST-extracted infobar methods, including native argument order, arbitrary byte splits, text and multiple frames, statistics, process failures and cancellation. The optional eBitrateCalculator backend is unchanged. A 20-second deadline applies only to starting the external helper. New samples stop that timer.
