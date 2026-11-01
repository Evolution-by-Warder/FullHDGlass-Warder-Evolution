# FullHDGlass 1.0.54-test3

Testovacia oprava zostávajúceho nulového video bitrate na ARM prijímačoch (GigaBlue, DM920).

Záznam z GigaBlue potvrdil stabilný správny video PID 5101, audio PID 5106 a demux 0. Nulu pre video vracia už pôvodný pomocný program, kým audio meria približne 443 kb/s. Samotné zobrazenie ani parsovanie nulu nevytvárajú.

Nový samostatný ARM pomocný program kontroluje otvorenie zariadenia a nastavenie filtrov. Ak video filter nedostáva PES dáta, po troch nulových vzorkách prepne iba svoj video filter na TS meranie. Počíta obsah paketov zvoleného PID-u bez TS hlavičiek a adaptačných polí. Meranie audia ostáva samostatné. Nevytvára odhad bitrate z rozlíšenia obrazu.

Pôvodné pomocné programy pre ARM, MIPS a SH4 ostávajú v balíku nezmenené. Voliteľný natívny eBitrateCalculator sa nemení. Nový pomocný program sa spúšťa priamo zo svojej cesty, aby nezávisel od neskoršieho kopírovania architektúrnych variantov pri štarte GUI.

Po inštalácii cez /tmp reštartujte GUI a nechajte FTA TV stanicu hrať približne 20–30 sekúnd. Overte nenulové video aj audio a potom prepnutie na inú stanicu. Ak video zostane nulové alebo meranie zlyhá, pošlite /tmp/fullhdglass-bitrate.json pred ďalším prepnutím.

## Validation
- Runtime and bounded receiver-diagnostic tests.
- Actual native C executable under a DVB syscall simulator: zero PES video recovers with TS, audio continues, working PES is retained, failed PES setup falls back, unsupported filters fail visibly, audio-only services and invalid arguments.
- TS payload unit tests: adaptation fields, TEI, wrong PID, all 565 read boundaries, resynchronisation and rate conversion.
- Static ARM build, ARM unit tests under QEMU, actual packaged ARM executable startup check.
- Existing OpenATV, radio, layout, safety and package checks.

Physical receiver verification of this replacement is pending. Public update feeds remain unchanged.

Primary API reference: https://www.kernel.org/doc/html/v4.8/media/uapi/dvb/dmx_types.html
