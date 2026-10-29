#!/usr/bin/env python3
"""Small live benchmark of the TEST8 lyrics adapters; never saves lyrics."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import importlib
import json
from pathlib import Path
import random
import statistics
import sys
import time
from urllib.error import HTTPError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

SONGS = [
    ('SK', 'Pavol Habera', 'Láska, necestuj tým vlakom'),
    ('SK', 'Majself', 'Posledný hráč'),
    ('SK', 'Júlia Hečková', 'Taliansky muzikál'),
    ('SK', 'Alan Murin', 'Prepáč'),
    ('SK', 'Richard Müller', 'Po schodoch'),
    ('SK', 'Kristína', 'Horehronie'),
    ('CZ', 'Damiens', 'Stýská se mi'),
    ('CZ', 'Faraon', 'Šlapací kolo'),
    ('CZ', 'Karel Gott', 'Trezor'),
    ('CZ', 'Lucie Bílá', 'Láska je láska'),
    ('CZ', 'Kabát', 'Pohoda'),
    ('CZ', 'Chinaski', '1970'),
]
PROVIDERS = ('lrclib', 'ovh', 'hudba', 'youradio')
UA = 'FullHDGlass-Warder-Evolution/lyrics-benchmark (https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution)'


def run_provider(name, rounds, helper, sites, out):
    results = []
    next_request = 0.0
    stop_at = time.monotonic() + 420
    for round_number in range(1, rounds + 1):
        order = list(SONGS)
        random.Random(2900 + round_number).shuffle(order)
        for country, artist, title in order:
            row = dict(provider=name, round=round_number, country=country,
                       artist=artist, title=title, requests=[])
            if max(next_request, time.monotonic()) >= stop_at:
                row.update(status='skipped-time-or-backoff', elapsed_ms=0)
                results.append(row)
                continue
            wait = next_request - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            began = time.monotonic()
            deadline = began + 32
            if name == 'lrclib':
                plans = [helper.SEARCH + '?' + urlencode(args) for args in (
                    {'artist_name': artist, 'track_name': title},
                    {'track_name': title}, {'track_name': artist})]
                limit = 3
            elif name == 'ovh':
                plans = [helper.FALLBACK + quote(a, safe='') + '/' + quote(t, safe='')
                         for a, t in ((artist, title), (title, artist))]
                limit = 2
            else:
                plans = sites.initial_urls(name, artist, title)
                limit = sites.LIMITS[name]
            found = ''
            for index, url in enumerate(plans):
                if index >= limit:
                    break
                if next_request > deadline - 2 or time.monotonic() > deadline - 2:
                    break
                wait = next_request - time.monotonic()
                if wait > 0:
                    time.sleep(wait)
                started = time.monotonic()
                next_request = started + 1.1
                trace = dict(variant=index+1)
                try:
                    req = Request(url, headers={'User-Agent': UA, 'Accept':
                                  'application/json' if name in ('lrclib','ovh') else 'text/html'})
                    fetch = urlopen if name in ('lrclib','ovh') else sites.opener(name)
                    with fetch(req, timeout=min(10, max(.1, deadline-started))) as response:
                        raw = response.read(helper.MAX_RESPONSE+1)
                        final = response.geturl()
                    if len(raw) > helper.MAX_RESPONSE:
                        raise ValueError('Oversized response')
                    if name == 'lrclib':
                        data = json.loads(raw.decode('utf-8'))
                        if not isinstance(data, list):
                            raise ValueError('Invalid API response')
                        found = helper.select(data, artist, title)
                        trace['status'] = 'found' if found else 'not-found'
                    elif name == 'ovh':
                        data = json.loads(raw.decode('utf-8'))
                        if not isinstance(data, dict):
                            raise ValueError('Invalid API response')
                        found = helper.clean_text(data.get('lyrics'))
                        trace['status'] = 'found' if found else 'not-found'
                    else:
                        page = sites.parse(name, final, raw, artist, title,
                                           helper.same_song, helper.clean_text)
                        found = page['text']
                        trace['status'] = 'found' if found else 'links' if page['links'] else 'not-found'
                        for link in page['links']:
                            if link not in plans and len(plans) < limit:
                                plans.append(link)
                except HTTPError as error:
                    trace.update(status='not-found' if error.code == 404 else 'http-error', http=error.code)
                    if error.code in (429,503):
                        delay = helper.retry_delay(error, time.time())
                        trace['retry_after'] = delay
                        next_request = max(next_request, time.monotonic()+delay)
                except Exception as error:
                    trace.update(status='request-error', error=type(error).__name__)
                trace['elapsed_ms'] = round((time.monotonic()-started)*1000)
                row['requests'].append(trace)
                if found or trace.get('http') in (429,503):
                    break
            row['elapsed_ms'] = round((time.monotonic()-began)*1000)
            if found:
                row.update(status='found', characters=len(found),
                           text_sha256=hashlib.sha256(found.encode()).hexdigest())
            elif any(r['status'] in ('http-error','request-error') for r in row['requests']):
                row['status'] = 'source-error'
            elif any(r['status'] == 'not-found' for r in row['requests']):
                row['status'] = 'not-found'
            else:
                row['status'] = 'incomplete'
            results.append(row)
            # An atomic checkpoint contains metadata only, never lyrics/HTML.
            temp = out / (name+'.json.tmp')
            temp.write_text(json.dumps(results, ensure_ascii=False, indent=2)+'\n')
            temp.replace(out / (name+'.json'))
            print(json.dumps({k:row[k] for k in ('provider','round','artist','title','status','elapsed_ms')}, ensure_ascii=False), flush=True)
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--helper-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--rounds', type=int, default=2, choices=(1,2))
    args = parser.parse_args()
    sys.path.insert(0, str(args.helper_dir.resolve()))
    helper = importlib.import_module('warderLyrics')
    sites = importlib.import_module('warderLyricsSites')
    args.output.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat()
    rows = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(run_provider, name, args.rounds, helper, sites, args.output) for name in PROVIDERS]
        for future in as_completed(futures):
            rows.extend(future.result())
    report = dict(schema=1, started_utc=started, finished_utc=datetime.now(timezone.utc).isoformat(),
                  helper_source_commit='eb430332895045f5722d92dc66d71e21019617a9',
                  helper_sha256={p:hashlib.sha256((args.helper_dir/p).read_bytes()).hexdigest()
                                 for p in ('warderLyrics.py','warderLyricsSites.py')},
                  rounds=args.rounds, songs=[dict(country=c,artist=a,title=t) for c,a,t in SONGS],
                  local_cache=False, lyrics_or_html_saved=False,
                  method='One sequential worker per provider; four providers measured concurrently. Same adapters, variants, identity matching and limits as TEST8. 1.1s minimum request-start spacing per host, Retry-After honored. Source errors separate from misses. One shared hosting network, not receiver latency or population coverage.',
                  results=rows, summary={})
    for name in PROVIDERS:
        subset = [r for r in rows if r['provider']==name]
        found = [r for r in subset if r['status']=='found']
        unique = {(r['artist'],r['title']) for r in found}
        sk = {(r['artist'],r['title']) for r in found if r['country']=='SK'}
        cz = unique-sk
        report['summary'][name] = dict(attempts=len(subset), found=len(found), unique_songs=len(unique),
          sk_unique=len(sk), cz_unique=len(cz),
          median_found_ms=round(statistics.median(r['elapsed_ms'] for r in found)) if found else None,
          median_completion_ms=round(statistics.median(r['elapsed_ms'] for r in subset)),
          errors=sum(r['status']=='source-error' for r in subset))
    (args.output/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('SUMMARY '+json.dumps(report['summary'],ensure_ascii=False),flush=True)


if __name__ == '__main__':
    main()
