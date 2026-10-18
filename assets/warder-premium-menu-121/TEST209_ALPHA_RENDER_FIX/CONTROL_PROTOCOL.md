WARDER EVOLUTION — TEST209 alpha/render correction

Branch: warder-modernization-work
Base commit: 879e4181c69719604085fa8d7ab9a9be19a64fd0

Findings from owner screenshots: the generic Enigma2 Menu screen used alphatest="on" for g17MenuEntry2, which can suppress partially transparent pixels. The 121 approved canonical PNGs use 810x810 RGBA and the dark edge-connected black canvas at alpha 128; their artwork RGB is preserved. Set the generic Menu preview to alphatest="off" so those pixels blend with the skin background.

The published menuIcons.zip and menuIconsBig.zip each contained 123 entries. Two runtime aliases (e.png and plugin_selection.png) still had edge background alpha 49; these were restored to alpha 128. The menu entry key timer_edit was missing from both archives, so the old icon remained/fell back. Added timer_edit.png as a runtime alias of approved timermenu.png. Canonical 121 artwork is unchanged. ZIP contains 126 entries: canonical assets and runtime aliases, with duplicate alias entries appended so extraction replaces stale alias files.

New archives validated: 810x810 RGBA for corrected aliases and timer_edit.png; ZIP CRC verified; archive SHA-256 recorded in assets/warder/downloads.json. TEST209 package is built only on warder-modernization-work.
