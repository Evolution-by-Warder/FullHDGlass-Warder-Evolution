# FullHDGlass 1.0.38-test13 — SuperMusic.cz

SuperMusic now supplies original lyrics through its normal public visitor-session flow. The adapter verifies the complete artist/title identity, ignores chord markup and keeps a session within the background worker so a verified visitor does not repeat the check on each song candidate.

The visitor computation is capped at 0.4 seconds / 100000 candidates and all requests stay inside the existing helper time budget. Cross-source destinations, oversized pages and repeated verification pages are not accepted. No browser, new third-party dependency or shared API key is required.

Existing successful text caches remain valid; older negative results are checked again. The radio layout and production update feeds are unchanged.

Validation: exact matching, chord removal, source/destination guards, bounded visitor checks, cache compatibility and the complete radio suite. Live SuperMusic and package-byte verification are required by CI.
