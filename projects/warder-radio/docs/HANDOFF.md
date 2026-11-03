# Warder Radio 0.1.0-test2 — verified handoff

Source: `f66d0fdc57d41cab4875077c110d0d440f21e70e`.
CI run: https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/41615255493 — all steps passed.

- Fixed receiver-reported blank interface: background z=0, opaque panels z=1, live controls z=2. Regression reproduces test1 occlusion with real native creation order and confirms the corrected stacking.
- All 21 Warder languages, 60 complete UI/message keys each; regional/al/sq aliases and Persian alignment. Approved English subtitle and final logo retained.
- Automatic startup update check, manual menu check, confirmed install and restart, exact size/SHA-256/IPK identity/version/opkg-state verification. Testing and stable channels separated.
- 25 unit tests and nine native cases on each of three pinned OpenPLi/OpenATV revisions: 52 executions passed. Package verification passed.
- Public IPK was downloaded and verified: 2,794,972 bytes; SHA-256 `177ea65c08555aed349eea3f673f70c7551d6a65782f69bb0f839854acdd41c7`.
- Testing feed advanced only after that verification, commit `bf3b4eaecaa891e3c0578d589afab4e5e28a5a0f`; stable feed remains empty. Test1 needs a manual upgrade because it lacked the updater.
- Existing stations/favourites/history/custom data retained. Current catalogue: 5,444 references in 203 groups. Other plugin/skin production feeds are unchanged.

Physical receiver acceptance is still pending: corrected display and GLES painting, radio audio/metadata, remote control, picons and optional recording. Native tests stub the C++/OS boundary and are not hardware proof.

Release: https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/warder-radio-v0.1.0-test2
