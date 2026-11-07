# PR #51 — Native progressbar fix: build integration

## Verified root cause

In OpenATV `eListboxServiceContent::paint()`, the EPG text cell
(`celServiceInfo`) fetches the current `evt` only while that text cell
is enabled. Warder disables the native text cell to avoid drawing it twice;
native left/right progressbars subsequently test `evt` and disappear.
Percentage and remaining-minute cells independently request event data and
continue to work. This matches the GigaBlue TEST70 screenshots.

## Actual correction

`tools/apply-native-progressbar-event-fix.py` edits
`lib/service/listboxservice.cpp` in an **Enigma2 source checkout**.
It inserts an independent event lookup immediately before the native
progressbar painting branch. The existing bar condition, pixmap,
colors, geometry, and two-line behavior are unchanged.

The fast PR CI applies this script to current upstream OpenATV source,
runs `git diff --check`, and publishes the actual unified diff in the
`pr51-native-enigma2-progressbar-source-patch` GitHub Actions artifact.

### Integration into an Enigma2 image build

1. Select the Enigma2 source revision actually used to build the receiver
   image. This is an **image source change**, not a FullHDGlass plugin change.
2. Apply the generated unified patch to that source tree, or invoke the
   checked-in patcher on the same native C++ file. Abort if the anchor does
   not match exactly; never apply with `--reject` or `--3way` blindly.
3. Rebuild the image's normal Enigma2 recipe with the native patch included
   in its patch queue (e.g. the appropriate `SRC_URI` / `bbappend`
   mechanism, where the image's build system uses BitBake).
4. Confirm that the resulting Enigma2 binary comes from that patched build
   and matches the receiver image's architecture, ABI and dependencies.
5. On a recovery-capable test receiver, verify all seven indicator modes;
   verify the original EPG font is restored on leaving ChannelSelection
   and the right six-event panel remains unchanged.

Do **not** overwrite the live receiver's `enigma2` binary using an
unverified arbitrary build, and do **not** assume a skin IPK carries this fix.
Do not merge/release PR #51 until a native-image QA pass exists.

## Scope of current verification

- OpenATV upstream: native source edit applied successfully, `git diff --check` PASS.
- Warder targeted renderer tests: no masks and no synthetic bars.
- Receiver: TEST70 confirmed native left/right bars missing without native
  patch; patched Enigma2 has **not yet been compiled or installed**.
- OpenPLi: a separately verified patch is needed for its possibly different
  C++ rendering structure. Do not reuse the OpenATV patch untested.
