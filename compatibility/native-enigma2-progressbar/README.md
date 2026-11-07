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
- OpenPLi `develop`: source contract verified independently by CI. Its native
  `paint()` retrieves `evt` before the event-text and progressbar branches,
  so the OpenATV-specific event-fetch patch is not applicable to that source
  structure. Do not modify OpenPLi with the OpenATV patch.

## Compatibility gate for GigaBlue Quad 4K Pro

The box model and installed Warder test skin do not identify the exact running
Enigma2 build. Before attempting native image rebuild/deployment, obtain from
receiver **read-only** outputs:

```sh
cat /etc/image-version 2>/dev/null
cat /etc/issue 2>/dev/null
opkg list-installed | grep -E '^enigma2([ -]|$)' | head -20
uname -m
```

Compare these with the selected image's exact source revision and build
metadata. The CI-validated patch targets **upstream OpenATV master**; it must
not be assumed binary-compatible with a different or vendor-customized image.
No native binary was built or installed by this PR.

## GigaBlue Quad 4K Pro — actual receiver identity (owner SSH, 2026-11-07)

| Key | Confirmed value |
| --- | --- |
| Model / machine | `gbquad4kpro` |
| Distro | `openatv` |
| Image | `8.1.0~beta`, built `2026-11-06` |
| Enigma2 package | `8.1.0~beta+git36061+da455f50+da455f57dd-r1` |
| Package architecture | `cortexa15hf-neon-vfpv4` |
| Kernel architecture | `armv7l` |
| OE base | `OE-Alliance 6.0` |

The public OpenATV GitHub repository did not resolve the running package
prefix `da455f50` as a commit during the PR audit. This means
`openatv/enigma2:master` **is not proven to be the exact source of the
receiver's installed binary**. A public dated commit
`66df86bd9fa56f817e33099c09ee1811c9aa1aab` (Nov 6) and current master
both passed `git apply --check` and real patch application tests. This
demonstrates source-level portability, **not binary compatibility**.

The experimental `meta-warder-native` BitBake layer carries a proper
`enigma2_%.bbappend` and a C++ patch in `SRC_URI:append:openatv`.
To use it, a trusted OE-Alliance 6.0 build environment for **this exact
receiver** must add the layer to `BBLAYERS`, select
`MACHINE=gbquad4kpro` and `DISTRO=openatv`, confirm the appropriate
`ENIGMA2_URI` and `SRCREV` from the receiver's package build provenance,
then run `bitbake -c patch enigma2` followed by the supported native
package build and packaging QA. A `bitbake -c patch` pass alone does not
mean an ARM binary is available or tested.

Never install a binary from a different `SRCREV`/image feed or copy an
Enigma2 executable into a live box outside the supported image packaging
and recovery path.
