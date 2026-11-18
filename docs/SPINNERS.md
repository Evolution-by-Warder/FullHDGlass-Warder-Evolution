# Spinner selection

Prepared in FullHDGlass source for the next authorized release. No new IPK or
production update feed has been published as part of this source change.

The skin configuration's Other settings section offers:

* **Holubica** in Slovak (Dove in English): the exact receiver-confirmed dove.
* **HDGlass - bakussa**: the existing 20-frame animation by **bakussa**.
* **Warder**: the 24-frame transparent 100 × 100 skull animation by **bakussa**.
  The static preview is its own `wait1.png`; activation plays all 24 frames.
  Bakussa remains the default and the Dove remains selectable.

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

## Warder provenance

Reconstructed from the original user-provided skull archive with 24 RGBA
100 x 100 frames; source ZIP SHA-256: `dfcf4c185be6f80c4ee9e890abc1b3f3a09bd7293ef6ff0caf24134ae5397dd2`.
This reproducibly pinned source differs byte-for-byte from the previously
recorded archive checksum in issue #112. Do not equate the two archives.
Physical receiver validation remains pending.
