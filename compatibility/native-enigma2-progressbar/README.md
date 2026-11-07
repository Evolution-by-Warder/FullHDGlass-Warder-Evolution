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

## GigaBlue Quad 4K Pro — current receiver identity (owner SSH, 2026-11-07)

| Key | Confirmed current value |
| --- | --- |
| Model / machine | `gbquad4kpro` |
| Distro | `openatv` |
| Image | `8.1.0~beta`, build `20261107`, compiled `20261107020925` |
| Enigma2 package | `8.1.0~beta+git36096+f9f72e10+f9f72e1115-r1` |
| Package architecture | `cortexa15hf-neon-vfpv4` |
| Kernel architecture | `armv7l` |
| OE base | `OE-Alliance 6.0` |
| Feed architecture | `gb7252` |

The receiver was **updated** from the previous 2026-11-06 image:
`8.1.0~beta+git36061+da455f50+da455f57dd-r1`.
That version is historic and must not be used for a new native binary.

Public `openatv/enigma2` GitHub lookup did **not** resolve the new
`f9f72e10` or `f9f72e1115` prefixes as commits during this audit.
Neither did public web search. Therefore **no exact source provenance** is
established for the installed Enigma2 binary, and source patch compatibility
with the running image is **unverified**.

The OE-Alliance 6.0 distro configuration `meta-oe/conf/distro/openatv.conf`
selects `openatv/enigma2` branch **`8.0`** when BitBake's
`DISTRO_TYPE` is `release`, and `master` otherwise. The receiver reports
`imagetype=release`, making branch `8.0` a particularly important source
candidate, although the actual resolved BitBake `DISTRO_TYPE` and `SRCREV`
are not yet proven from the installed image. The PR CI explicitly checks
the native patch against `8.0` as well as `master`. This does not
establish that either branch's current HEAD equals `f9f72e10`.

The OpenATV patch was independently applied by CI to public dated commit
`66df86bd9fa56f817e33099c09ee1811c9aa1aab` and current upstream
`master`. These are **source applicability checks**, not a native compile
nor ABI verification of the receiver's newer `f9f72e10` build.

The experimental `meta-warder-native` BitBake layer has a proper
`enigma2_%.bbappend` and a C++ patch in `SRC_URI:append:openatv`.
For a release, a trusted OE-Alliance 6.0 build environment must pin
`MACHINE=gbquad4kpro`, `DISTRO=openatv`, and the **exact `SRCREV`
used by the receiver package**. Only after this can `bitbake -c patch
enigma2`, a real ARM build, packaging QA, and recovery-capable receiver
tests establish a compatible result.

**Do not ship or install any native Enigma2 binary while the precise
`f9f72e10` source revision and build configuration are unavailable.**
Do not copy a C++ source patch to the receiver and attempt to run it; it
is not an installable package. The production image and skin remain untouched.
