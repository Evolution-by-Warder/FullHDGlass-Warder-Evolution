# FullHDGlass – Warder Evolution 1.0.71

Stable maintenance release fixing direct upgrades from the original FullHDGlass 9.50 family, including 9.50, 9.50-r12 and 9.50-r12.2.

## Fixes
- Protect the original legacy post-removal script during a package-name upgrade so it cannot delete the newly installed Warder files.
- Keep an untouched backup of the original remover and preserve the original remove behaviour outside upgrade transactions.
- Preserve Enigma2 and FullHDGlass user settings and overlays.
- Retain all approved 1.0.70 Prime Time, EPG, PIG and IPTV improvements unchanged.

## Installation
Copy `enigma2-plugin-skins-fullhdglass_1.0.71_all.ipk` to `/tmp/` on the receiver, then run:

```sh
opkg install /tmp/enigma2-plugin-skins-fullhdglass_1.0.71_all.ipk
```

Do not manually remove the original FullHDGlass package and do not use force-overwrite. Restart Enigma2 GUI after successful installation.

Package: `enigma2-plugin-skins-fullhdglass-warder-evolution`
Version: `1.0.71-1`

The upgrade scripts were checked in isolated package-manager regression tests. A physical SF8008 run remains to be confirmed.
