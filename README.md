# FullHDGlass - Warder Evolution

Modern continuation and evolution of the FullHDGlass Enigma2 skin, maintained by **Warder**.

## Production release — 30 October 2026

**FullHDGlass 1.0.48** displays the broadcast slideshow and current-song cover separately in DAB/DAB+ mode. Satellite and IPTV radio keep their original single cover window. Settings headers no longer show section names below the date. [Current release](docs/CURRENT-RELEASE.md) · [Production evidence](docs/PRODUCTION.json).

The improved spinner, compact History and localized radio-mode caption are preserved.

## Installation

[Download the installable IPK](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/download/v1.0.48/enigma2-plugin-skins-fullhdglass_1.0.48_all.ipk).

Radio behavior is based on receiver-confirmed test250: DVB/AAC, RDS, DAB and WDR, physical TV/OpenWebif parity, transparent equalizer, and opaque black radio channel selection with an image preview. Temporary diagnostics are retired on upgrade. The current native version is recorded in update-production.json and update-test.json; update.json retains the required legacy migration bridge.


## Project status

This repository is the official home of **FullHDGlass - Warder Evolution**.

The project preserves the character, approved graphics and visual identity of FullHDGlass while modernizing its internals for current Enigma2 environments.

### Current development work

- Python 3 compatibility and cleanup
- safer installation and removal scripts
- modernization of weather services
- repair of missing menu graphics
- cleanup of obsolete and legacy code
- compatibility work for current Enigma2 images

## Origins and credits

**FullHDGlass - Warder Evolution** is based on the original **FullHDGlass** Enigma2 skin created by **Shamann**.

Full credit and thanks belong to **Shamann** for creating the original FullHDGlass project, its design and the foundation on which this continuation is built.

Warder Evolution continues, maintains and modernizes that work for current Enigma2 environments. It does **not** claim authorship of Shamann's original work. Original authorship and credits are preserved and respected.

Shamann's Sat-Universe profile: https://www.sat-universe.com/index.php?members/shamann.48129/

## Versioning

The Warder Evolution branch starts a new release line at **1.0** rather than continuing the original FullHDGlass version numbering.

The historical receiver recovery baseline is **1.0.15**; the current offered settings release is recorded in update.json. The 1.0.4 extraction and GOLDEN archive are historical origins, not the current backup.

## Protected project rules

Approved graphics, GUI structure, layout, dimensions, positions and visual identity are **LOCKED**. They must not be redesigned, rearranged, regenerated, renamed or "optimized" without explicit approval.

New work must adapt to the approved FullHDGlass visual structure rather than changing that structure merely for convenience.

Legacy/runtime compatibility identifiers containing `17` are not cosmetic branding and must remain unchanged unless a deliberate future migration is explicitly designed and tested. The explicitly approved package-name migration is documented in docs/PACKAGE-TRANSITION.md; the package-manager identifier is now `enigma2-plugin-skins-fullhdglass-warder-evolution`. Preserved runtime identities include `hd_glass17`, `setupGlass17`, `g17_setup_pict`, `extraScreens17` and `/etc/enigma2/skin_user-hdg17.xml`.

Original authorship must not be erased or globally replaced with Warder branding. Warder branding applies to the continuation and new Warder Evolution work.

## Development

Maintained and evolved by **Warder** as **FullHDGlass - Warder Evolution**.

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

## ASA DE picons — corrected scope, 27 October 2026

ASA DE belongs **only to standalone DAB and the nine complete 23.5E archives** (three sizes × three backgrounds). Per the owner's correction it is excluded from Canal+ SK/CZ, legacy Skylink and complete 19.2E packages. Those 30 archives are restored byte-for-byte to their exact pre-ASA versions; their 51 public parts were verified by size and SHA256, and all 36 current receiver plans passed. Every other station picon is preserved. The complete 23.5E ASA archives and standalone DAB (52 labels / 82 references) remain unchanged. The publisher enforces the restricted selector list in the [source approval](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/blob/main/picons/DAB/asa/approval.json). [Current publication evidence](assets/warder/asa-radio-publication.json). No IPK update is required.


Internet-radio cover integration: [design and provenance](docs/RADIO-STREAM-METADATA.md) · [verification](docs/RADIO-STREAM-VERIFICATION.json). HDF Radio installation is not required. The 22 metadata tests and full release CI passed; live receiver confirmation remains pending.


## IPTV SK/CZ radio — 1.0.36

Shared with PiconHub 0.1.30: 247 programme picons, 263 exact reference PNGs per variant, three sizes × three styles. Refreshed bouquet: 321 entries (88 SK, 233 CZ), with audio samples confirmed for 286 selected URLs; 74 entries still lack suitable verified picons. [Bouquets and coverage](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/tree/main/picons/IPTV-SK-CZ). All nine shared modules are byte-identical in both published IPKs. [Verification](docs/IPTV-SK-CZ-1.0.36.json).


Dátové doplnenie 28.10.2026 (r2): 247 položiek s piconmi / 263 referencií v každom z deviatich variantov, 74 zatiaľ bez vhodného overeného piconu. Overené Radia.sk, Radia.cz a MyOnlineRadio.cz aj dodané originály. Všetkých deväť verejných archívov a obrázkov prešlo kontrolou; aktuálne dáta sa stiahnu opätovným výberom IPTV rádiá SK/CZ. Verzie IPK sa nemenia. [Zdroje a zhodovanie](https://github.com/Evolution-by-Warder/PiconHub-Warder-Evolution/blob/main/picons/IPTV-SK-CZ/catalog/followup-sources.json).

## Tiché obnovenie Warder Radio Streams (1.0.37)

Existujúci spravovaný rádio bouquet sa raz týždenne obnoví z nášho Gitu bez hlášok a reštartu. Na začiatku zostávajú naše SK/CZ stanice, ostatné krajiny obnovuje samostatný týždenný GitHub workflow. Sťahovanie beží mimo GUI; kontroluje sa SHA256 a pri chybe zostáva starý zoznam. [Rozsah a správanie](docs/CURRENT-RELEASE.md).

## Rádio s textami piesní — 1.0.39

Schválené rozloženie s kompaktným obalom a natívnym panelom textu je súčasťou produkčnej verzie. SuperMusic v TEST13 bol potvrdený na prijímači; výsledky a limity vyhľadávania sú uložené v [overení](docs/RADIO-SUPERMUSIC-TEST13.md).


Dátová aktualizácia piconov 29.10.2026: 27 schválených grafík, 63 živých balíkov v troch veľkostiach a prevedeniach. [Zmeny a overenie](docs/PICON-DATA-UPDATES.md). Aktualizácia dát nemení verziu skinu ani IPK.

Dátové doplnenie 30.10.2026: schválené D1 (Magenta Sport League 1–4) je aktívne v 18 spoločných balíkoch 9°E/13°E. Spolu A/B/C/D: 31 grafík, 93 originálov v 63 živých balíkoch. [Overenie a inštalácia](docs/PICON-DATA-UPDATES.md). Nový IPK netreba; príslušné dáta stiahnite znova v režime nahradenia.

Názov IPK od 30.10.2026: `enigma2-plugin-skins-fullhdglass_1.0.41_all.ipk`. Bajty, verzia aj vnútorná identita sú zachované. Správca pluginov: **Balíčky vzhľadu → fullhdglass-warder-evolution**. [Overenie všetkých troch kategórií](docs/PLUGIN-PACKAGE-GROUPS.json).
