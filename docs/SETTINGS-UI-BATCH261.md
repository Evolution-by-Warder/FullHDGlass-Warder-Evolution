# Approved settings batch — 24 October 2026

Baseline TEST260: appearance and responsiveness confirmed by owner on receiver.
Work branch only; retain production feeds until validation.

- [x] Remove duplicate version under header on all settings pages.
- [x] Smaller download status/category graphics, transparent black backdrop, denser rows.
- [x] Uniform owned choice/input/confirmation/progress/result dialogs, including update/reset.
- [x] OLED choice available; correct 7zip detection at extraction, clear recovery path.
- [x] Current Warder changelog; centered Close below content frame.
- [x] Extra infobar Type: explain style samples and show meaningful type previews on opaque backing.
- [x] Extra infobar Icon type: lower/center left 1–10 list relative to right preview.
- [x] Move setup entry from Settings into Plugins exclusively; localized title and icon.
- [x] Preserve TEST259 asynchronous help previews, live TV/radio and all configuration semantics.

Owner explicitly authorized implementing the full batch after notes collection.

## Validation record

- TEST260 baseline appearance / TEST259 responsiveness: owner confirmed on receiver.
- TEST261 build-host checks: 22 layout/controller tests, 12 functional batch tests, 8 asynchronous-loader tests and full original-help pixel comparisons.
- Legacy picon catalogue test: passed, 370 pinned mappings and 29 fail-closed entries.
- An additional historical auxiliary test fails at its unchanged production-URL assertion: the current provider black catalogue entry uses the work/test ref and source id, while the old test hardcodes fullhd-production. All three inputs (test, sync module, catalogue) are byte-identical to TEST260; this batch does not change their trust policy. This is not an OLED/helper or settings regression.
- Actual receiver validation of TEST261 remains pending.
