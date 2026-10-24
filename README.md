# FullHDGlass - Warder Evolution

Modern continuation and evolution of the FullHDGlass Enigma2 skin, maintained by **Warder**.

## Production baseline — 24 October 2026

**FullHDGlass 1.0.16** is the owner-approved production release, based on the accepted TEST270 with clean production numbering. [Production record](docs/PRODUCTION.md) · [Approval](docs/PRODUCTION-APPROVAL.json) · [Release](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/v1.0.16).

Production packages and displayed version labels use **1.0.16**, without the word test. Existing test releases remain historical. Both built-in update feeds offer the verified production IPK after public byte verification; 1.0.16 sorts newer than every 1.0.16-test candidate.

The small IPK excludes the large preview archives. Help and type previews remain verified background downloads. Approved graphics, layouts, radio behavior, runtime identifiers, settings and original author credits are preserved. Exact package identity, SHA256, source revision and validation are recorded in docs/PRODUCTION.json after publication. Owner acceptance does not claim a new exhaustive physical receiver test.

## Historical receiver recovery baseline: 1.0.15

[Download the installable IPK](packages/enigma2-skin-fullhdglass17-warder-evolution_1.0.15_all.ipk).

Radio behavior is based on receiver-confirmed test250: DVB/AAC, RDS, DAB and WDR, physical TV/OpenWebif parity, transparent equalizer, and opaque black radio channel selection with an image preview. Temporary diagnostics are retired on upgrade. The current offered version is recorded in update.json and update-test.json.


## Project status

This repository is the official home of **FullHDGlass17 - Warder Evolution**.

The project preserves the character, approved graphics and visual identity of FullHDGlass while modernizing its internals for current Enigma2 environments.

### Current development work

- Python 3 compatibility and cleanup
- safer installation and removal scripts
- modernization of weather services
- repair of missing menu graphics
- cleanup of obsolete and legacy code
- compatibility work for current Enigma2 images

## Origins and credits

**FullHDGlass17 - Warder Evolution** is based on the original **FullHDGlass** Enigma2 skin created by **Shamann**.

Full credit and thanks belong to **Shamann** for creating the original FullHDGlass project, its design and the foundation on which this continuation is built.

Warder Evolution continues, maintains and modernizes that work for current Enigma2 environments. It does **not** claim authorship of Shamann's original work. Original authorship and credits are preserved and respected.

Shamann's Sat-Universe profile: https://www.sat-universe.com/index.php?members/shamann.48129/

## Versioning

The Warder Evolution branch starts a new release line at **1.0** rather than continuing the original FullHDGlass version numbering.

The historical receiver recovery baseline is **1.0.15**; the current offered settings release is recorded in update.json. The 1.0.4 extraction and GOLDEN archive are historical origins, not the current backup.

## Protected project rules

Approved graphics, GUI structure, layout, dimensions, positions and visual identity are **LOCKED**. They must not be redesigned, rearranged, regenerated, renamed or "optimized" without explicit approval.

New work must adapt to the approved FullHDGlass visual structure rather than changing that structure merely for convenience.

Legacy/runtime compatibility identifiers containing `17` are not cosmetic branding and must remain unchanged unless a deliberate future migration is explicitly designed and tested. This includes `enigma2-skin-fullhdglass17`, `hd_glass17`, `setupGlass17`, `g17_setup_pict`, `extraScreens17` and `/etc/enigma2/skin_user-hdg17.xml`.

Original authorship must not be erased or globally replaced with Warder branding. Warder branding applies to the continuation and new Warder Evolution work.

## Development

Maintained and evolved by **Warder** as **FullHDGlass17 - Warder Evolution**.

Detailed recovery state and binding rules are maintained in `docs/PROJECT-CHECKPOINT.md`.

Release 1.0.7 also includes approved Seznam TV HD white and black picons in the complete 23.5E downloads and pins the downloader to their updated catalogue.

Release 1.0.9 fixes incomplete Canal+ downloads: SK contains 226 picons and CZ 231 in each of the transparent, white and black styles. All packages preserve the existing approved PNG bytes and have been tested with the actual skin installer.

Release 1.0.9 also includes approved Televizia Osem transparent, white and black picons in the complete 23.5E downloads and pins the downloader to their updated catalogue.

Release 1.0.10 fixes stale Python bytecode surviving upgrades, so the downloader uses the current pinned catalogue after GUI restart. Package failures now show their actual reason. The real 23.5E black downloader and selective PNG replacement have been exercised.

Release 1.0.11 uses the seven explicitly approved black PNGs from the full 23.5E package in both Canal+ packages. The black SK package contains 228 PNGs and CZ 231; the other colour packages are preserved.

Release 1.0.12 replaces the four approved Canal+ channel picons in all three styles in both Canal+ packages and adds them to the complete 23.5E packages (762 PNGs per style). The radio baseline and MASTER templates are preserved.

Release 1.0.13 follows the current approved main channel-picon catalogue at each download. Future channel-picon content changes need only archive/catalogue publication, without another IPK. Source, redirect, size and SHA-256 checks remain enabled. See [picon update policy](docs/PICON-CATALOG-UPDATES.md).

Release 1.0.14 connects the supplied original 50x30, 220x132 and 400x240 position sets through the live catalogue. Existing PNGs take precedence, especially at 16.0E and 23.5E.

Release 1.0.15 removes the six unsupported picon positions and their legacy download selectors. All 45 supported satellite positions, existing picons and receiver-confirmed radio graphics remain unchanged.

## Current recovery and offline backups

Use [PROJECT-CONTINUITY.md](PROJECT-CONTINUITY.md) for the current state and [backup/restore instructions](docs/BACKUP-RESTORE.md) for set `warder-backups-20261023`. Historical checkpoint entries do not override the current release or live publication catalog.
