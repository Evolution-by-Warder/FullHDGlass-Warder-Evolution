# 0.1.0-test2

Fixes the receiver-reported blank interface: explicit z-order keeps background
artwork and panels below live text, lists, picons and the activity canvas.
Panels are opaque, so the TV video no longer shows through them. The regression
now reproduces test1 using its exact published skin and replays native creation
order with additional static widgets included.

Adds all 21 languages used across FullHDGlass, GSU and PiconHub, with complete UI
and update messages, receiver-language selection, Albanian aliases and Persian
right alignment. The approved English subtitle is preserved.

Adds automatic update checks when opening the plugin and a manual menu action.
Uses the existing reviewed Warder updater adapted for this independent package,
with TLS verification, exact release URL, bounded size, SHA-256, IPK identity,
installed-file/version and opkg-status checks. Installation and GUI restart are
offered to the user. Test and stable channels are kept separate, and the testing
feed is advanced only after the public IPK has been downloaded and verified.

Still a receiver-test prerelease; physical display/audio/GLES verification is
pending. Existing favourites, history and custom stations are preserved.

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
