#!/usr/bin/env python3
"""Offline regression for the Radio plugin artwork engine embedded in the skin."""
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKIN = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17"
sys.path.insert(0, str(SKIN))
import warderRadioCoverSearch as covers


class Response(io.BytesIO):
    def __init__(self, data, url):
        super().__init__(data)
        self.url = url
    def __enter__(self):
        return self
    def __exit__(self, *_):
        self.close()


class CoverSearchTests(unittest.TestCase):
    IMAGE = bytes((255, 216)) + b"x" * 2048

    def test_recording_rank_preserves_live_and_remix(self):
        row = {"kind":"song","artistName":"ABBA","trackName":"Dancing Queen"}
        self.assertGreater(covers.cover_rank(row, "ABBA", "Dancing Queen"), 0)
        self.assertEqual(covers.cover_rank(row, "ABBA", "Dancing Queen (Live)"), 0)
        self.assertEqual(covers.cover_rank(row, "ABBA", "Dancing Queen (Remix)"), 0)

    def test_album_cover_from_single_fast_catalogue_request(self):
        calls = []
        def opener(request, timeout):
            url = request.full_url
            calls.append(url)
            if "itunes.apple.com/search" in url:
                value = {"results":[{"kind":"song","artistName":"ABBA",
                          "trackName":"Dancing Queen",
                          "artworkUrl100":"https://is1-ssl.mzstatic.com/image/thumb/100x100bb.jpg"}]}
                return Response(json.dumps(value).encode(), url)
            if url.startswith("https://is1-ssl.mzstatic.com/"):
                return Response(self.IMAGE, url)
            raise AssertionError("unexpected URL " + url)
        with tempfile.TemporaryDirectory() as directory:
            path, provider = covers.lookup_cover("ABBA", "Dancing Queen", directory=directory, opener=opener)
            self.assertEqual(provider, "iTunes")
            self.assertEqual(Path(path).read_bytes(), self.IMAGE)
            self.assertEqual(len(calls), 2)
            self.assertIn("600x600bb", calls[-1])
            second, source = covers.lookup_cover("ABBA", "Dancing Queen", directory=directory, opener=opener)
            self.assertEqual((second, source), (path, provider))
            self.assertEqual(len(calls), 2)

    def test_artist_fallback_requires_exact_identity(self):
        def opener(request, timeout):
            url = request.full_url
            if "itunes.apple.com/search" in url:
                return Response(b'{"results":[]}', url)
            if "theaudiodb.com/api/" in url:
                return Response(json.dumps({"artists":[
                    {"strArtist":"Wrong Artist","strArtistThumb":"https://www.theaudiodb.com/artist.jpg"},
                    {"strArtist":"ABBA","strArtistThumb":"https://www.theaudiodb.com/artist.jpg"}
                ]}).encode(), url)
            if url == "https://www.theaudiodb.com/artist.jpg":
                return Response(self.IMAGE, url)
            raise AssertionError("unexpected URL " + url)
        with tempfile.TemporaryDirectory() as directory:
            path, provider = covers.lookup_cover("ABBA", "Unlisted Song", directory=directory, opener=opener)
            self.assertEqual(provider, "TheAudioDB")
            self.assertEqual(Path(path).read_bytes(), self.IMAGE)


if __name__ == "__main__":
    unittest.main()
