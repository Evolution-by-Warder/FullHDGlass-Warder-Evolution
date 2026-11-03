# 0.1.0-test1

First independent Warder Radio receiver-test candidate. Implements the approved
three-column design, functions on the left and version after the clock, with the
approved transparent Warder-family plugin-browser icon.

Includes the complete current Warder/PiconHub bouquet (5,444 unique references in
203 groups), native radio playback, metadata, picons, favourites, history, local
search, custom stations, explicit catalogue refresh, recordings browser and
optional streamripper recording. English subtitle: **World of Radio Stations**.

No HDF Radio executable/bytecode is included. No existing stable plugin, skin,
feed or global action mapping is changed. Runtime is pure Python 3.9+.

Validation: 15 unit tests plus 6 native replay cases on each of three pinned
OpenPLi/OpenATV source revisions; integral rows verified at HD/FHD/WQHD/UHD;
IPK payload and offline scripts verified. Hardware playback/GLES/remote test is
pending and this version is deliberately a prerelease.
