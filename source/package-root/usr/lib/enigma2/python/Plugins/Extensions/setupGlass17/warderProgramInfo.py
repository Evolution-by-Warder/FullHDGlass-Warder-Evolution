# -*- coding: utf-8 -*-
# Warder PROGRAM INFO external metadata provider.
# EPG remains authoritative. External values are returned only for an exact normalized title match.
from __future__ import print_function
import json
import os
import re
import time
try:
    from urllib.parse import quote_plus
    from urllib.request import urlopen
except ImportError:
    from urllib import quote_plus
    from urllib2 import urlopen

TMDB_KEY = "3c3efcf47c3577558812bb9d64019d65"
CACHE_DIR = "/tmp/fullhdglass17-warder-programinfo"
GENRES = {
    12:"Adventure",14:"Fantasy",16:"Animation",18:"Drama",27:"Horror",28:"Action",35:"Comedy",
    36:"History",37:"Western",53:"Thriller",80:"Crime",99:"Documentary",878:"Science Fiction",
    9648:"Mystery",10402:"Music",10749:"Romance",10751:"Family",10752:"War",10759:"Action & Adventure",
    10762:"Kids",10763:"News",10764:"Reality",10765:"Sci-Fi & Fantasy",10766:"Soap",10767:"Talk",
    10768:"War & Politics"
}

def _norm(value):
    try:
        value = value.lower()
    except Exception:
        return ""
    value = re.sub(r'[^\w]+', ' ', value, flags=re.UNICODE)
    return re.sub(r'\s+', ' ', value).strip()

def _cachePath(title):
    key = re.sub(r'[^a-z0-9]+', '_', _norm(title)).strip('_')[:100] or "empty"
    return os.path.join(CACHE_DIR, key + ".json")

def _readCache(title):
    path = _cachePath(title)
    try:
        if os.path.isfile(path) and time.time() - os.path.getmtime(path) < 604800:
            with open(path, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return None

def _writeCache(title, data):
    try:
        if not os.path.isdir(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        with open(_cachePath(title), "w") as f:
            json.dump(data, f)
    except Exception:
        pass

def _fetch(url):
    raw = urlopen(url, timeout=4).read()
    if not isinstance(raw, str):
        raw = raw.decode("utf-8", "ignore")
    return json.loads(raw)

def lookup(title, context=""):
    """Return verified external metadata or {}. Never return a fuzzy/first-result guess."""
    if not title:
        return {}
    cached = _readCache(title)
    if cached is not None:
        return cached
    wanted = _norm(title)
    matches = []
    for media in ("movie", "tv"):
        try:
            data = _fetch("https://api.themoviedb.org/3/search/%s?api_key=%s&query=%s" % (media, TMDB_KEY, quote_plus(title)))
            for item in data.get("results", [])[:5]:
                candidate = item.get("title") or item.get("name") or item.get("original_title") or item.get("original_name") or ""
                if wanted and _norm(candidate) == wanted:
                    matches.append((media, item))
        except Exception:
            continue
    if not matches:
        _writeCache(title, {})
        return {}
    # Exact-name collisions may only be resolved by EPG description context; fuzzy titles stay forbidden.
    unique = {}
    for media, item in matches:
        unique[(media, item.get("id"))] = (media, item)
    candidates = list(unique.values())
    if len(candidates) == 1:
        media, item = candidates[0]
    else:
        words = set(x for x in _norm(context).split() if len(x) >= 5)
        ranked = []
        for cmedia, citem in candidates:
            hay = _norm(citem.get("overview") or "")
            score = sum(1 for word in words if word in hay)
            ranked.append((score, cmedia, citem))
        ranked.sort(key=lambda x: x[0], reverse=True)
        if not ranked or ranked[0][0] < 2 or (len(ranked) > 1 and ranked[0][0] == ranked[1][0]):
            return {}
        media, item = ranked[0][1], ranked[0][2]
    date = item.get("release_date") if media == "movie" else item.get("first_air_date")
    year = date[:4] if date and len(date) >= 4 else ""
    countries = item.get("origin_country") or []
    genres = [GENRES[x] for x in item.get("genre_ids", []) if x in GENRES]
    result = {
        "provider": "TMDB",
        "media_type": media,
        "year": year,
        "country": ", ".join(countries),
        "genre": ", ".join(genres),
        "rating": ("%.1f/10" % float(item.get("vote_average"))) if item.get("vote_average") and int(item.get("vote_count") or 0) > 0 else "",
        "overview": item.get("overview") or "",
        "poster_path": item.get("poster_path") or "",
        "backdrop_path": item.get("backdrop_path") or ""
    }
    _writeCache(title, result)
    return result
