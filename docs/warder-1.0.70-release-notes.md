# FullHDGlass – Warder Evolution 1.0.70

Stable Enigma2 skin update with Prime Time, Channel Selection EPG refinements and improved IPTV technical information.

## Changes

- Optional Prime Time display for **Channel Selection type 35**. Enable it in FullHDGlass Settings → Channel Selection → Show Prime Time for selected channel. Set the Prime Time clock (default 20:25). Disabled: six regular EPG entries; enabled: five regular entries plus a separated Prime Time entry.
- Improved clipping and presentation of long programme names and EPG information.
- Targeted PIG and Channel Selection layout repairs from the reviewed TEST76 candidate; the abandoned PR #54 geometry experiment is **not** included.
- IPTV InfoBar metadata recovery when streaming services supply resolution, aspect ratio or audio information late.
- Existing user settings and selected skin are retained during the upgrade.

## Install

Install the IPK directly over the current Warder Evolution package, then restart the Enigma2 GUI. Do not manually uninstall your existing skin.

Package ID: `enigma2-plugin-skins-fullhdglass-warder-evolution`
Version: `1.0.70-1`

The release contains the checked-in 1.0.70 source payload. Native OpenATV checks and focused Prime Time/EPG tests passed; a legacy graphics fingerprint check is not used as a release gate because its pinned digest predates intentional layout changes.
