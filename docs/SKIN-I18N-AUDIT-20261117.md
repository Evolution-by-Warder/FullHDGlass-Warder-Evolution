# FullHDGlass Warder Evolution — 21-language audit (2026-11-17)

**Status: PARTIAL; not yet 100% translated.** 21 OSD language codes are recognized; English is the original msgid fallback. Correct existing translations must not be overwritten with the original English wording.

## Main skin settings (setupGlass17)

| Locale | Result |
|---|---|
| sk | Complete (515 original entries) |
| cs | Completed all 46 previously blank entries; GNU MO rebuilt |
| ru | Completed all 53 previously blank entries; GNU MO rebuilt |
| lt | Completed all 49 previously blank entries; GNU MO rebuilt |
| zh | Completed 54 blank entries, corrected five erroneous fuzzy translations; GNU MO rebuilt |
| el | New partial Greek translation, 397/515 entries |
| al | 213 source entries were untranslated |
| de | 211 source entries were untranslated |
| es | 211 source entries were untranslated |
| et | 134 source entries were untranslated |
| fa | 218 source entries were untranslated |
| fr | 167 source entries were untranslated |
| hu | 211 source entries were untranslated |
| it | 212 source entries were untranslated |
| nl | 107 source entries were untranslated |
| pl | 209 source entries were untranslated |
| pt | 208 source entries were untranslated |
| ro | 209 source entries were untranslated |
| tr | 211 source entries were untranslated |
| uk | 208 source entries were untranslated |
| en | Original English source (not a translation catalogue) |

The counts for al/de/es/et/fa/fr/hu/it/nl/pl/pt/ro/tr/uk are from the original main branch and have not yet been filled. Original translated strings are preserved.

## Greek optional catalogues

| Domain | Translated | Total |
|---|---:|---:|
| setupGlass17 | 397 | 515 |
| helpTxt | 29 | 150 |
| weather | 90 | 108 |
| netatmo | 26 | 42 |
| eWeather | 25 | 2117 |

## Runtime / build

- Standard Python 3 `gettext.translation` replaces unsupported legacy `gettext.Catalog` calls in setup, help, weather and Netatmo.
- The code normalizes Enigma2 language names, including `sq` -> `al`, `gr` -> `el` and `zh_CN` -> `zh`.
- The original skin translation-enabled setting is retained and absent translations fall back to the original English msgid.
- New Greek `.po` + compiled `.mo` catalogues exist in all five domains; updated CS/RU/LT/ZH main `.po` + `.mo` catalogues exist.
- `.github/workflows/verify-skin-i18n.yml` tests syntax, language-code normalization and compiled Greek and four completed main catalogs.
- A green workflow and test on an actual Enigma2 receiver have **not** been confirmed.
- **No IPK, feed update, release or version increment.**

## Remaining for real completion

Translate and review remaining original strings in all incomplete languages and domains, regenerate compiled gettext catalogs and test actual UI/text on OpenATV and OpenPLi. The source-only preparations do not count as fully localized releases.
