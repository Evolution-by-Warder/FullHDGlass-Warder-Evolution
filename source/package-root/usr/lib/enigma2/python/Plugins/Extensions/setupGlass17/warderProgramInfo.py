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
CACHE_SCHEMA = "v3"
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

def _baseTitle(title):
    value = (title or "").strip()
    # Common EPG episode suffixes: "Přátelé VI (10)" and "Series S06E10".
    value = re.sub(r'\s+[IVXLCDM]+\s*\(\d+\)\s*$', '', value, flags=re.I)
    value = re.sub(r'\s+S\d{1,2}E\d{1,3}\s*$', '', value, flags=re.I)
    return value.strip() or (title or "").strip()

def _cachePath(title):
    key = re.sub(r'[^a-z0-9]+', '_', _norm(title)).strip('_')[:100] or "empty"
    return os.path.join(CACHE_DIR, CACHE_SCHEMA + "_" + key + ".json")

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

def _artworkPath(data):
    provider_id = str(data.get("provider_id") or "")
    if not provider_id:
        return ""
    # Backdrop is preferred for the horizontal PROGRAM INFO window; poster is fallback.
    for kind, remote in (("backdrop", data.get("backdrop_path")), ("poster", data.get("poster_path"))):
        if not remote:
            continue
        try:
            if not os.path.isdir(CACHE_DIR):
                os.makedirs(CACHE_DIR)
            dest = os.path.join(CACHE_DIR, "tmdb_%s_%s.jpg" % (provider_id, kind))
            if os.path.isfile(dest) and os.path.getsize(dest) > 1000:
                return dest
            raw = urlopen("https://image.tmdb.org/t/p/w780%s" % remote, timeout=4).read()
            if raw and len(raw) > 1000 and raw[:2] == b"\xff\xd8":
                with open(dest, "wb") as f:
                    f.write(raw)
                return dest
        except Exception:
            continue
    return ""

def lookup(title, context=""):
    """Return verified external metadata or {}. Never return a fuzzy/first-result guess."""
    if not title:
        return {}
    cached = _readCache(title)
    if cached is not None:
        if cached and not cached.get("artwork_path"):
            cached["artwork_path"] = _artworkPath(cached)
        return cached

    query_title = _baseTitle(title)
    wanted = _norm(query_title)
    matches = []
    # Localized EPG titles must resolve by exact localized title; never accept fuzzy results.
    for media in ("movie", "tv"):
        for language in ("cs-CZ", "sk-SK", "en-US"):
            try:
                data = _fetch("https://api.themoviedb.org/3/search/%s?api_key=%s&language=%s&query=%s" % (media, TMDB_KEY, language, quote_plus(query_title)))
                for item in data.get("results", [])[:5]:
                    candidate = item.get("title") or item.get("name") or item.get("original_title") or item.get("original_name") or ""
                    if wanted and _norm(candidate) == wanted:
                        matches.append((media, item))
            except Exception:
                continue
    if not matches:
        _writeCache(title, {})
        return {}

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

    detail = {}
    try:
        detail = _fetch("https://api.themoviedb.org/3/%s/%s?api_key=%s&append_to_response=external_ids" % (media, item.get("id"), TMDB_KEY))
    except Exception:
        pass
    date = (detail.get("release_date") if media == "movie" else detail.get("first_air_date")) or (item.get("release_date") if media == "movie" else item.get("first_air_date"))
    year = date[:4] if date and len(date) >= 4 else ""
    if media == "movie":
        countries = [x.get("iso_3166_1") for x in detail.get("production_countries", []) if x.get("iso_3166_1")]
    else:
        countries = detail.get("origin_country") or item.get("origin_country") or []
    genres = [x.get("name") for x in detail.get("genres", []) if x.get("name")]
    if not genres:
        genres = [GENRES[x] for x in item.get("genre_ids", []) if x in GENRES]
    ext = detail.get("external_ids") or {}
    imdb_id = detail.get("imdb_id") or ext.get("imdb_id") or ""
    runtime = detail.get("runtime")
    if not runtime and media == "tv":
        runtimes = detail.get("episode_run_time") or []
        runtime = runtimes[0] if runtimes else None
    vote = detail.get("vote_average", item.get("vote_average"))
    votes = detail.get("vote_count", item.get("vote_count"))
    result = {
        "provider": "TMDB",
        "provider_id": str(item.get("id") or ""),
        "imdb_id": imdb_id,
        "media_type": media,
        "year": year,
        "country": ", ".join(countries),
        "genre": ", ".join(genres),
        "rating": ("%.1f/10" % float(vote)) if vote and int(votes or 0) > 0 else "",
        "runtime": str(runtime or ""),
        "overview": detail.get("overview") or item.get("overview") or "",
        "poster_path": detail.get("poster_path") or item.get("poster_path") or "",
        "backdrop_path": detail.get("backdrop_path") or item.get("backdrop_path") or ""
    }
    result["artwork_path"] = _artworkPath(result)
    _writeCache(title, result)
    return result
