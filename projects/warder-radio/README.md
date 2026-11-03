# Warder Radio — World of Radio Stations

Independent native Enigma2 internet radio plugin. First receiver-test candidate:
**0.1.0-test1**. It is not a production release and is not added to existing stable feeds.

The approved layout uses the Warder graphic family, functions on the left,
stations in the centre and the player on the right. The header places the actual
package version after the clock. The approved transparent WARDER RADIO icon is
registered in the plugin browser.

## Included

- Bundled PiconHub/Warder catalogue: 5,444 stations in 203 groups, with original
  stream URLs and service references. Updates are explicit, from the same Git
  bouquet; the bundled/cached list remains usable without the catalogue server.
- Native Enigma2/GStreamer playback, station and available ICY artist/title data.
- Persistent favourites, last 100 played stations, accent-insensitive search
  across the catalogue and custom HTTP/HTTPS stations.
- Native/PiconHub picon lookup, with a neutral Warder Radio fallback logo.
- Mounted-disk recordings folder `/media/hdd/WarderRadio`; playback of recordings.
  Optional recording uses the separately installed `streamripper` executable.
  Its stream/codec/TLS support depends on the receiver's streamripper build.
- Slovak, Czech and English UI. Other receiver languages use English.
- Native layouts at 1280×720, 1920×1080, 2560×1440 and 3840×2160; list heights
  always contain an exact number of complete rows.

The animated bars indicate playback activity. They are decorative and are not a
measured audio spectrum. This first candidate does not include cover-art lookup,
lyrics, a sleep timer or recording schedules.

## Install and use

Copy the IPK to `/tmp`, then run:

```sh
opkg install /tmp/enigma2-plugin-extensions-warderradio_0.1.0-test1_all.ipk
```

Restart the GUI manually, then open **Warder Radio** from Plugins or Extensions.
No stream starts during installation or plugin discovery. Select a station and
press OK or green. Left/right switch between the function and station panels;
up/down move within a panel; CH+/CH− change pages. Yellow toggles a favourite;
blue searches all stations. MENU selects a group, updates the catalogue, adds a
station, controls recording and opens About. STOP stops radio playback and
returns to the previous service. EXIT/red closes the plugin and restores the
previous service, unless another application has already changed navigation.

The REC key starts/stops an optional streamripper recording of the playing
station. Closing the plugin stops its recorder. At least 100 MB free on a mounted
`/media/hdd` is required. Recordings are not deleted by the plugin.

Settings are stored atomically in `/etc/enigma2/warder-radio/state.json` and are
preserved by upgrades/uninstall. Installation writes only Warder Radio's own
plugin and documentation directories; it does not patch the skin, firmware,
other plugins, global keymaps or stable update feeds.

## Compatibility and verification

Runtime is architecture-independent Python 3.9+ and uses native Enigma2
components. It contains no HDF Radio binaries or bytecode. Tests replay real
OpenPLi release-9.2 and OpenATV Python classes with the C++ GUI/OS boundary stubbed.
See `tools/native-fixtures.json` for exact source commits and file hashes,
including the previously reviewed OpenATV 8.1 base and 8.0-next.

These tests check screen binding/lifecycle, full rows at four resolutions,
metadata, favourites, history, private remote mappings, timer cleanup and return
to TV. Unit tests cover catalogue parsing, persistence, update failure,
thread dispatch, navigation ownership and recording process handling.
**Receiver audio, GPU/GLES painting and physical remote behaviour still need a
real receiver test.** The catalogue does not assert every stream is online.

Build locally with `python3 tools/build_ipk.py`. Run unit tests with
`PYTHONPATH=src python3 -m unittest discover -s tests -v`. For the native replay,
run `python3 tools/test_native.py --upstream /path/to/enigma2/lib/python -v`.

## Provenance

Catalogue: `Evolution-by-Warder/PiconHub-Warder-Evolution`, source and commit in
`src/WarderRadio/catalogue-source.json`. Original Warder Radio background and
logo were generated for this project using the owner's supplied brand references.
The full logo master is retained in `artwork/warder-radio-logo.png`; the plugin
uses `plugin.png`. No existing unrelated logos were changed.

License: GPL-2.0-or-later. Copyright 2026 Warder.
