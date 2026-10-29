# Radio source diagnostics

## One-command receiver test

Run `python3 /tmp/warder_genius_test.py` after downloading that standalone file.
It accepts `WARDER_GENIUS_TOKEN` from the process environment, or asks for the
token with terminal echo disabled when that variable is absent. It automatically writes
`/tmp/warder-genius-test.log`. It checks DNS, authenticated API search, an exact
matching song page and, if already installed, the real `lyricsgenius` library.
It installs nothing. Default per-request timeout is 20 seconds with three
retries for network failures; the entire diagnostic stops after 120 seconds.
HTTP errors and infrastructure placeholders are distinct from missing songs.
The test's normal exit means the diagnostic completed, not that Genius worked.

These standalone Python 3 checks do not install or modify the Enigma2 plugin.

`check-genius-auth.py` uses only the Python standard library. Enter the Genius
Client Access Token at its hidden prompt; never put it into source, a URL,
GitHub Actions inputs or result files.

```sh
python3 check-genius-auth.py --artist 'IMT Smile' --title 'Úsmev a čaj' | tee /tmp/warder-genius-auth.log
```

The check calls `https://api.genius.com/search` with a properly encoded query and
an Authorization header, then selects an exact artist/title match. A matched
song page is fetched without the token. Redirects are refused. Responses have a
12-second timeout and a 1 MiB size limit. HTML is processed with `HTMLParser`,
including entities and nested elements; excluded headers and script/style text
are ignored. Results contain metadata, text character counts and hashes, not
the token or full lyrics. Missing HTML containers do not establish that a song
has no lyrics, because embedded song-state parsing is outside this diagnostic.

Without artist/title arguments, the check runs three known examples. For the
recording discussed here, `Úsmev a čaj` is by IMT Smile. No authenticated success
has yet been verified: this workspace receives an infrastructure placeholder
instead of Genius API JSON. See `docs/RADIO-ADDITIONAL-SOURCE-CHECKS.json` for
the separate local, GitHub and library results.
