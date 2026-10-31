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

## Sources still awaiting archives

* TechKings `spinners with setup.zip`: advertised 88 animations. The page and
  the exact attachment URL returned HTTP 403 when retrieval was attempted.
  Attachment: https://www.techkings.org/attachments/spinners-with-setup-zip.14106/
* OpenPLi `Spinner Pack_2_1.rar`: the source topic returned HTTP 403 and the web
  retrieval service could not open it. Contents have not been obtained or checked.
  Topic: https://forums.openpli.org/topic/57875-anderen-spinner-und-vil-anderes-bootlogo-gesucht/

These two are not counted as assimilated. Obtain the original archives from
the owner or a legitimately accessible source before importing, crediting and
checking them. Do not run old selector installers or replace system spinner paths.

The approved blue bakussa derivative remains on the base branch in
`design/spinner-choice/bakussa-blue-centered/`. Its original archive remains
unchanged. This task does not authorize further Trezor changes.
