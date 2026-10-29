#!/usr/bin/env python3
"""Exercise the real library, without a token and without publishing lyric text."""
import hashlib
from importlib.metadata import version
import json
import logging
import re
import time

from lyricsgenius import Genius
from lyricsgenius.api import PublicAPI

logging.disable(logging.CRITICAL)


def run(label, action):
    started = time.monotonic()
    result = {'step': label, 'library_version': version('lyricsgenius'),
              'token_supplied': False, 'lyrics_logged': False}
    try:
        data = action()
        result['status'] = 'response-received'
        if isinstance(data, str):
            result.update(characters=len(data), text_sha256=hashlib.sha256(data.encode()).hexdigest())
        elif isinstance(data, dict):
            response = data.get('response', data)
            result['response_keys'] = list(response)[:15]
        elif data is None:
            result['status'] = 'no-result'
    except Exception as error:
        result.update(status='error', error=type(error).__name__)
        response = getattr(error, 'response', None)
        code = getattr(response, 'status_code', None)
        if code is None:
            match = re.search(r'(?:status(?: code)?|code)[\s:=]+(\d{3})', str(error), re.I)
            code = int(match.group(1)) if match else None
        result['http'] = code
    result['elapsed_ms'] = round(1000 * (time.monotonic() - started))
    print('LYRICSGENIUS_CHECK ' + json.dumps(result), flush=True)


if __name__ == '__main__':
    # No authenticated developer API can be exercised without the owner's token.
    # Use the library's public client and the same unmodified lyric-page method.
    # An explicit empty token avoids the library reading GENIUS_ACCESS_TOKEN;
    # PublicAPI does not send an Authorization header.
    class PublicLyricsClient(PublicAPI):
        lyrics = Genius.lyrics
        remove_section_headers = False
    print('LYRICSGENIUS_CHECK ' + json.dumps({
        'step': 'authenticated-api', 'status': 'not-tested-no-token',
        'library_version': version('lyricsgenius'), 'token_supplied': False,
        'lyrics_logged': False}), flush=True)
    client = PublicLyricsClient(access_token='', timeout=5, retries=0, sleep_time=0)
    run('public-search', lambda: client.search_all('Instinct Dozadu'))
    run('direct-song-page', lambda: client.lyrics(song_url='https://genius.com/Abba-dancing-queen-lyrics'))
