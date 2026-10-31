# Spinner selection

Prepared for the next FullHDGlass release. This feature has not been published
in an IPK yet; the public updater remains on 1.0.49.

The skin configuration's Other settings section offers:

* **Holubica** in Slovak (Dove in English): the exact receiver-confirmed dove.
* **HDGlass - bakussa**: the animation contributed by **bakussa**. Thank you!

Press OK on Spinner to open the choice list, or change it with left/right.
Save the selected animation and restart the GUI. Canceling the configuration
does not change the animation. Playback uses Enigma2's native spinner loader;
there is no additional rendering timer, worker or runtime PNG conversion.
The animation choice survives normal package updates.
Removal returns known selected frames to the package-owned default set first,
so additional frames from a longer animation do not remain after uninstall.

Enigma2 gives a user's custom system spinner precedence over a skin spinner.
This selector preserves that precedence and never replaces the system spinner.

## Artwork

The dove retains all eighteen approved PNG files byte for byte, at 128 × 88.
The submitted bakussa archive is preserved unmodified in
`assets/warder/downloads/ui/spinners/bakussa-original.zip`.
Its twenty RGBA frames are resized proportionally from 130 × 130 to 104 × 104
with premultiplied alpha at build time. Each decoded 32-bit frame and native
working surface stays below the previously reviewed 48,000-byte allocation
threshold. Bakussa's animation and menu selection still require a receiver test;
desktop tests cannot establish framebuffer correctness on every receiver.

## Adding another animation

1. Put its original archive in `assets/warder/downloads/ui/spinners/`.
2. Add one definition to `design/spinner-choice/sources.json`: a stable unique
   ID, display name, author, sequential frame count, target size, source archive,
   original dimensions, SHA-256 and the archive directory containing `wait1.png`,
   `wait2.png`, etc. Maximum 64 frames; reviewed decoded surface size below
   48,000 bytes. Keep both target dimensions at most 128 pixels.
3. Run `python3 tools/build-spinner-themes.py` and
   `PYTHONDONTWRITEBYTECODE=1 python3 tools/test-spinner-choice.py -v`.
4. Review the artwork, attribution, dimensions and receiver behavior before
   publication. Localize a new descriptive display name where appropriate;
   author nicknames remain unchanged.

The menu, persistence and application helper read the generated catalog; adding
a new approved definition requires no edits to those controllers. The regression
suite explicitly exercises a third theme introduced through the catalog alone.
