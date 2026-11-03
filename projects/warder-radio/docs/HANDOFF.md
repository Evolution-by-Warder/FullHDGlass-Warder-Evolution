# Warder Radio 0.1.0-test5 — current handoff

Source commit: `d1c851b4ecbe52a80105a678d12e7d9b3e73aa6b`.
CI: https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/41621151267 — success.
Testing-feed publication: `e808052a634bdc67633eaddd0380bacdd9929f3d`.

The left Country heading is now blank. The centre native button reads Select country – Slovakia ▾, translated for the receiver language and actual chosen group. Select country and the separator are white; the country and arrow stay cyan blue even when focused. A leading pointer marks remote focus. Native inline colour commands are supported by both inspected OpenPLi and OpenATV font renderers. Settings remains Choose country and Now playing is unchanged. Slovak/Czech display country names are localized without changing persisted catalogue identities.

Opening the plugin resumes the last played radio station from existing history, preferring fresh catalogue data for its identity and falling back to the remembered record. It selects the station in the corresponding list, makes one start attempt, does not rewrite history during resume, and restores the previous TV service on close. Fresh installations without history stay idle until selection. Installation/plugin discovery do not start playback.

Validation: 25 unit cases, 13 native cases on each of three pinned upstream revisions (64 executions), package verification, successful GitHub CI and verified public release download. The test4 updater offers test5. All 21 languages now contain all 65 UI strings. The underlying catalogue still contains 5,444 references/203 country and themed groups; no classification rewrite was included.

IPK: 2,797,010 bytes; SHA-256 `35856a0e73bb03f046e0f1ccdef6ba71cad1f50720e110d89248388205d0d209`.
Release: https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/warder-radio-v0.1.0-test5

Physical receiver confirmation of mixed header colours and startup resume is pending. Other production feeds remain unchanged; the independent stable channel remains empty.
