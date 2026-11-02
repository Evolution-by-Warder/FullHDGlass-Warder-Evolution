# FullHDGlass 1.0.62-test5 — OpenPLi dialog crash repair TEST

Fix reported crashes when restoring settings, displaying restore results and requesting a factory reset. Native OpenPLi confirms via ok(), while OpenATV uses select(); the owned dialog now delegates to the appropriate native method. Optional OpenPLi timers are checked at close time, including native deletion before close. Yes/no selection, default=False, cancellation and disabled input are preserved.

Five regressions replay the actual native MessageBox controller and the owned dialog on OpenPLi release-9.2/develop and OpenATV. The previous test4 reproduces the reported missing-select failure. The third uploaded log is dated 30 August: its float-coordinate applet failure is historical; current MessageBox applet already uses integer division and is exercised with odd desktop dimensions.

Retains test4 plugin browser repair and all earlier fixes. Independent TEST release, production feeds unchanged. Physical receiver confirmation pending.
