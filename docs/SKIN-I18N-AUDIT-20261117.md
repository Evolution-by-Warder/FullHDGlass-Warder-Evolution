# 21-language source catalogue audit (17 November 2026)

The language resolver supports 21 Enigma2 OSD codes. It respects the skin's translation switch, normalizes sq→al and gr→el, and falls back to English when a translation is missing. This is not the same as complete human translation.

New Greek translation coverage (entry count, not UI coverage):

| Domain | Translated | Total | Coverage |
|---|---:|---:|---:|
| setupGlass17 | 397 | 515 | 77.1% |
| helpTxt | 29 | 150 | 19.3% |
| weather | 90 | 108 | 83.3% |
| netatmo | 26 | 42 | 61.9% |
| eWeather | 25 | 2117 | 1.2% |

There are still untranslated entries, particularly the large historic eWeather vocabulary; do not report point 9 as fully translated. Original translated entries of the other 19 non-English locale catalogues are left intact. No IPK was built or released.
