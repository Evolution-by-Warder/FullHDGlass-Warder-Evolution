# Warder Radio 0.1.0-test1 — verified handoff

Source commit: `7f739a0e5d0dde2b55cb38672872b8f2969cd64e`.

- First native receiver-test candidate published at `warder-radio-v0.1.0-test1`.
- GitHub Actions run `41612691569`: success, including 15 unit tests and six native replay tests on each of three pinned upstream revisions (33 executions total).
- Public IPK downloaded successfully and matched the local reproducible build: 2,774,848 bytes, SHA-256 `3846d67aaeeead87d6e347b80dd547ac52484c654319eb110d3fd9b11f41c6d5`.
- Approved final Warder-family icon is the installed `plugin.png`; master retained in artwork. English subtitle: World of Radio Stations.
- The imported Warder/PiconHub Git bouquet contains 5,444 unique station references in 203 groups.
- Stable FullHDGlass main remains `3f5c0f10dcd7d5368154e974cfcc895ab94088f5`; this new plugin lives on `warder-radio-development` in `projects/warder-radio`.

Receiver acceptance remains pending: OpenPLi/OpenATV audio playback and ICY updates, physical remote, native GPU/GLES rendering at the box's active resolution, station picons from installed PiconHub, favourite/history persistence, return to TV and optional streamripper recording. The native replay stubs the C++/OS boundary and does not establish hardware compatibility by itself.

Release: https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/tag/warder-radio-v0.1.0-test1
