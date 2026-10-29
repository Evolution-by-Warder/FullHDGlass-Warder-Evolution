# Radio source diagnostics

These standalone Python 3 checks do not install or modify the Enigma2 plugin.

`check-genius-auth.py` uses only the Python standard library. Enter the Genius
Client Access Token at its hidden prompt; never put it into source, command-line
arguments, a URL, GitHub Actions inputs or result files.

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
