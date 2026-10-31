# Spinner preview library

The owner requested separate named folders, one spinner per folder, for motion
review before any new installation package. This work creates preview assets
only. No IPK, updater feed or receiver settings are changed.

## Available source

SpinKit by Tobias Ahlin, MIT license, pinned revision
`742a71277c49b69053b5beb9fad80d720840a2ab`. The CSS and full license are preserved
in `assets/warder/downloads/ui/spinners/sources/spinkit/`.

All twelve designs are rendered from the actual upstream CSS in Chromium,
prepared as transparent 104×104 RGBA PNG sequences and separate GIF previews.
Each named directory has frames, its own preview, author, license and metadata.
The preview GIF uses a dark matte only for viewing; native PNGs stay transparent.
Chase and Swing container timing is synchronized to their existing two-second
child animation so complete loops fit the native 64-frame limit at 100 ms.
No browser, CSS rendering or conversion is required on a receiver.

The collection is outside the install payload. It is for review; later release
work must account for package size and include only approved/runtime-ready assets.

## Community archives supplied by the owner

Both forums initially returned HTTP 403. The owner then attached the actual
archives, so no further remote access or login is needed:

* `spinners with setup.zip`: actual contents contain **83** PNG sequences,
  rather than the 88 advertised in the source post. SHA-256
  `96c8b5131d0e10a45663cc24454afce946b39a47813575d9e1f9943bd6e0bbab`.
* `Spinner Pack_2_1.rar`: **58** PNG sequences. SHA-256
  `bb4159ff9bd7fde37bfcfb12df747d1aa7631bc605b5fdac5285443f4faaa110`.
* `spinner_football_soccer.zip`: one six-frame sequence. SHA-256
  `1cc8da9d04553bd51808e6cb22f3fb68a705b16829d500b6d48aae5e63e65e95`.

All 142 sequences were read and validated, producing 1,797 native RGBA frames.
No exact duplicates were found after normalization. Community artwork retains
its original colors and numeric frame order. Small originals are not enlarged;
large frames fit a 96-pixel inner area on the common transparent 104×104 canvas.
Existing opaque backgrounds are not guessed away; metadata records their presence.
The archive originals are preserved unchanged under `sources/community/`.
Thumbnail caches and the setup PDF are not included in the runtime-frame folders.
No installers are executed and no system spinner paths are replaced.

The collection's ekremtt credit is carried as an attributed collection credit.
Missing author or license details are stated as unknown, never invented. Each
folder retains its source archive/folder and frame checksums. SpinKit's MIT
license applies to SpinKit only and is not asserted for the community archives.

Together there are **154** spinner folders and **1,988** native frames. The root
`index.html` shows exactly one animation at a time. Every spinner also has its
own page, preview, native frames and attribution. The complete viewing archive is
`assets/warder/downloads/ui/spinners/preview-library/warder-spinnery-na-vyber.zip`.

The approved blue bakussa derivative remains on the base branch in
`design/spinner-choice/bakussa-blue-centered/`. Its original archive remains
unchanged. This task does not authorize further Trezor changes.
