"""Test di publish.py con API simulate (nessuna chiamata di rete). Uso: python3 -m unittest social/test_publish.py"""
import json, sys, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import publish  # noqa: E402


class Fake:
    def __init__(self):
        self.calls, self.n = [], 0

    def __call__(self, base, method, path, token, params=None):
        self.calls.append((method, path, dict(params or {})))
        if method == "GET" and path == "me":
            return {"user_id": "U1", "username": "d.iasio.libri"}
        if method == "GET" and "fields" in (params or {}) and params["fields"] == "status_code":
            return {"status_code": "FINISHED"}
        if method == "GET":
            return {"permalink": "https://example.test/p/" + path}
        self.n += 1
        return {"id": f"id{self.n}"}


CAR = {"id": "c", "tipo": "carosello", "didascalia": "cap", "didascalia_fb": "capfb",
       "immagini": [f"social/img/carousel/c/0{i}.jpg" for i in (1, 2, 3)]}


class PublishTests(unittest.TestCase):
    def test_carousel_instagram(self):
        f = Fake()
        with mock.patch.object(publish, "call", f), mock.patch.object(publish.time, "sleep"):
            r = publish.publish_instagram(CAR, publish.media_urls(CAR), "T")
        posts = [c for c in f.calls if c[0] == "POST"]
        self.assertEqual(len(posts), 3 + 1 + 1)                         # 3 slide + contenitore + publish
        self.assertTrue(all(c[2].get("is_carousel_item") == "true" for c in posts[:3]))
        self.assertEqual(posts[3][2]["media_type"], "CAROUSEL")
        self.assertEqual(posts[3][2]["children"], "id1,id2,id3")
        self.assertEqual(posts[4][1], "U1/media_publish")
        self.assertTrue(r["link"].startswith("https://example.test"))

    def test_carousel_facebook(self):
        f = Fake()
        with mock.patch.object(publish, "call", f):
            r = publish.publish_facebook(CAR, publish.media_urls(CAR), "T", "PG")
        posts = [c for c in f.calls if c[0] == "POST"]
        self.assertEqual([c[1] for c in posts], ["PG/photos"] * 3 + ["PG/feed"])
        self.assertTrue(all(c[2]["published"] == "false" for c in posts[:3]))
        self.assertEqual(json.loads(posts[3][2]["attached_media"]), [{"media_fbid": f"id{i}"} for i in (1, 2, 3)])
        self.assertEqual(posts[3][2]["message"], "capfb")
        self.assertIn("id4", r["link"])

    def test_single_image_and_reel_unchanged(self):
        img = {"id": "i", "immagine": "social/img/i.jpg", "didascalia": "d", "alt": "a"}
        reel = {"id": "r", "tipo": "reel", "video": "social/video/r.mp4", "didascalia": "d", "miniatura_ms": 5500}
        f = Fake()
        with mock.patch.object(publish, "call", f), mock.patch.object(publish.time, "sleep"):
            publish.publish_instagram(img, publish.media_urls(img)[0], "T")
            publish.publish_instagram(reel, publish.media_urls(reel)[0], "T")
            publish.publish_facebook(img, publish.media_urls(img)[0], "T", "PG")
            publish.publish_facebook(reel, publish.media_urls(reel)[0], "T", "PG")
        posts = [(c[1], c[2]) for c in f.calls if c[0] == "POST"]
        self.assertEqual(posts[0][1]["image_url"], "https://libri.diasio.ch/social/img/i.jpg")
        self.assertEqual(posts[2][1]["media_type"], "REELS")
        self.assertEqual(posts[2][1]["thumb_offset"], "5500")
        self.assertEqual(posts[4][0], "PG/photos")
        self.assertEqual(posts[5][0], "PG/videos")

    def test_story_and_text(self):
        st = {"id": "s", "tipo": "storia", "immagine": "social/img/story/s.jpg"}
        tx = {"id": "t", "tipo": "testo", "didascalia": "ciao", "link": "https://libri.diasio.ch/"}
        f = Fake()
        with mock.patch.object(publish, "call", f), mock.patch.object(publish.time, "sleep"):
            publish.publish_instagram(st, publish.media_urls(st)[0], "T")
            publish.publish_facebook(st, publish.media_urls(st)[0], "T", "PG")
            publish.publish_facebook(tx, None, "T", "PG")
        posts = [(c[1], c[2]) for c in f.calls if c[0] == "POST"]
        self.assertEqual(posts[0][1]["media_type"], "STORIES")
        self.assertNotIn("caption", posts[0][1])
        self.assertEqual([x[0] for x in posts[2:]], ["PG/photos", "PG/photo_stories", "PG/feed"])
        self.assertEqual(posts[3][1]["photo_id"], "id3")
        self.assertEqual(posts[4][1], {"message": "ciao", "link": "https://libri.diasio.ch/"})
        self.assertEqual(publish.media_urls(tx), [])

    def test_platform_restriction(self):
        tx = {"id": "t", "tipo": "testo", "didascalia": "x"}
        img = {"id": "i", "immagine": "a.jpg", "didascalia": "x"}
        only_ig = {"id": "g", "immagine": "a.jpg", "didascalia": "x", "piattaforme": ["instagram"]}
        state = {"pubblicati": {}}
        both = ["instagram", "facebook"]
        self.assertEqual(publish.pending(tx, state, both), ["facebook"])      # il testo va solo su Facebook
        self.assertEqual(publish.pending(img, state, both), both)
        self.assertEqual(publish.pending(only_ig, state, both), ["instagram"])

    def test_calendar_files_exist(self):
        root = Path(publish.ROOT).parent
        cal = json.loads(publish.CAL.read_text(encoding="utf-8"))
        ids = [p["id"] for p in cal["post"]]
        self.assertEqual(len(ids), len(set(ids)))
        for p in cal["post"]:
            for u in publish.media_urls(p):
                self.assertTrue((root / u.replace(publish.SITE + "/", "")).is_file(), u)
            if publish.is_carousel(p):
                self.assertTrue(2 <= len(p["immagini"]) <= 10, p["id"])
            if p.get("tipo") == "storia":            # le Storie non hanno didascalia
                continue
            self.assertTrue(p["didascalia"].strip())
            self.assertLessEqual(len(p["didascalia"]), 2200, p["id"])       # limite Instagram
            self.assertLessEqual(p["didascalia"].count("#"), 5, p["id"])


if __name__ == "__main__":
    unittest.main()
