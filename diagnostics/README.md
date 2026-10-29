# Radio source diagnostics

`check-radio-source-access.py` performs bounded anonymous checks of KaraokeTexty,
SuperMusic and Musixmatch. It reports response metadata and structured-field
sizes, never complete lyrics or credentials. A successful diagnostic run does
not by itself mean that a provider returned a usable song text.

These checks do not modify the Enigma2 plugin or production update feeds.
Historical findings are recorded in `docs/RADIO-ADDITIONAL-SOURCE-CHECKS.json`.

`compare-radio-lyrics-sources.py` compares SuperMusic.cz, KaraokeTexty.sk,
KaraokeTexty.cz and Akordy Kytary.cz against the same twelve recordings. It uses
the existing TEST12 identity/parser modules from `source/package-root` and
creates `/tmp/warder-radio-source-comparison.json`. Results of the local and
GitHub runs are in `docs/RADIO-FOUR-SOURCE-COMPARISON.md` and its JSON companion.
The two KaraokeTexty domains are tested separately without cross-domain fallback.

Genius was excluded from further development on 2026-10-29 at the owner's
request. Its standalone receiver tests and library-check workflow were removed;
the remaining source-access diagnostic no longer requests Genius. The runtime
provider was never integrated.
