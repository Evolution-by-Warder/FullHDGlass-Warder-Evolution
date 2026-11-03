# Warder Radio 0.1.0-test4 — current handoff

Source: `b98d9031ff31d4d8a7f3f1f0725629540da6d050`.
CI run: https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/actions/runs/41618002419 — success.
Verified testing-feed publication: `8c18e11a312f92f1d0e64173bb0164bfce0a5452`.

- Left body heading is now Country, translated across all 21 locales.
- Current country beside it is a native Enigma2 Button. UP from the first station focuses it; OK opens the selector; DOWN returns. Native click signal opens the same dialog.
- First Settings entry is Choose country and opens that same selector. Current choice is preselected, selecting saves it without stopping playback, and cancel keeps the previous station/section.
- Now playing remains unchanged. A small section label preserves the active favourites/history/recordings/search heading.
- The selector reuses existing catalogue groups; the underlying source still contains country groups and themed/broadcaster groups. No station identity or country classification was rewritten in this UI change.
- All 21 languages, automatic verified updates, test/stable separation, catalogue of 5,444 stations/203 groups and persisted user data are retained.
- Validation: 25 unit cases and 11 native cases on each of three pinned revisions, 58 executions; package verification passed. Native Button fixtures were pinned from the same upstream commits.
- Public IPK: 2,795,814 bytes, SHA-256 `c09ba7c7ff42580162cec621e0b9ccb3edcb319aa9d95cd495757404b6865381`.
- Test2's updater can offer test4 on reopening/manual check. Stable channel remains empty. Older published test builds are preserved.

Receiver verification of the new header navigation/click action is pending; native tests stub the C++/OS boundary. The test2 receiver screenshot confirmed the previously fixed live interface displays successfully.

Release: https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/warder-radio-v0.1.0-test4
