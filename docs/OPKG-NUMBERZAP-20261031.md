# FullHDGlass — installer layout and number-zap picon compatibility

Prepared on top of the verified TEST4 installation repair and generated-version-label fix. Existing releases and feeds remain unchanged.

The Opkg screen was centered at 1350x720 and reserved only 1230x315 for the log at y=300. Its updated layout uses 1800x960 with a 1680x720 log at y=120, compact status rows and separate progress/footer. Component bindings are preserved. A fixed ornament that overlapped the log is removed. The exact before/after XML is recorded in design/opkg-layout/layout.json.

Both supplied Octagon crash logs fail at native Picon.changed while opening NumberZapPicon: ServiceEvent has no text property. The matching OpenATV aaa789a source reproduces this exception. The repaired XML adds the existing ServiceName Reference converter, which supplies the expected text reference. The regression exercises the real upstream source, converter and renderer methods, including changed selection, clearing and missing-icon fallback. It is wired into the Python 3.14 compatibility job.

The protected skin baselines are not replaced: test guards reverse only the exact registered Opkg and NumberZap edits before comparing historical checksums.

Large menu icons remain a separate unresolved report. Current runtime/main catalogs agree and the archive directory contains 125 files under the expected menuIconsBig root. This does not prove a successful complete download on that receiver. Request its download result and graphics path before claiming a fix.

Receiver validation of the new layout and NumberZap fix is pending. Include these changes with the next reviewed package; do not overwrite published TEST4.
