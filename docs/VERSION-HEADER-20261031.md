# FullHDGlass — version labels

The owner confirmed the first GUI transition from 9.50-r12.2 to TEST4 and a working skin after restart on GigaBlue Quad 4K Pro / OpenATV 8.0.1. The updater independently displays the runtime version 1.0.50-test4.

The menu and dialog banner values were stale generated labels (1.0.49 and 1.0.47), confirmed by inspecting the exact public TEST4 IPK. This is a presentation defect.

`tools/sync_header_version.py` synchronizes only the version eLabel at position 1680,70 in plugin.py and warderDialogSkins.py. TEST preparation invokes it after setting the runtime version. Both package builders check the result and reject stale values. For stable release preparation, run `python tools/sync_header_version.py` after the version bump, before packaging.

Include this fix with the next combined release. Do not rebuild or overwrite any already published TEST4 bytes, and do not change stable updater manifests for this cosmetic fix. Original 9.50 receiver migration and PiconHub remain separate verification items.
