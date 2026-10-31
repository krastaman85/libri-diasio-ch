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

    def test_post_sospeso_non_esce(self):
        # «sospeso»: post in revisione, fermo finché il campo non viene tolto (31/10/2026)
        both = ["instagram", "facebook"]
        sosp = {"id": "s", "immagine": "a.jpg", "didascalia": "x", "sospeso": True}
        self.assertEqual(publish.pending(sosp, {"pubblicati": {}}, both), [])
        cal = {"fuso": "Europe/Rome", "post": [
            {"id": "s", "quando": "2026-11-01T12:00", "immagine": "a.jpg", "sospeso": True},
            {"id": "b", "quando": "2026-11-01T12:05", "immagine": "b.jpg"}]}
        now = publish.datetime(2026, 11, 1, 12, 10, tzinfo=publish.timezone.utc)
        p, _ = publish.pick(cal, {"pubblicati": {}}, both, now, None)
        self.assertEqual(p["id"], "b")

    def test_calendar_files_exist(self):
        root = Path(publish.ROOT).parent
        cal = json.loads(publish.CAL.read_text(encoding="utf-8"))
        ids = [p["id"] for p in cal["post"]]
        self.assertEqual(len(ids), len(set(ids)))
        state = json.loads(publish.STATE.read_text(encoding="utf-8"))
        for p in cal["post"]:
            # i media dei post già usciti si tolgono dal repo dopo ogni serie (social/tools/pulisci_media.py)
            piatt = ["tiktok"] if publish.is_tiktok(p) else ["instagram", "facebook"]
            if publish.pending(p, state, piatt):
                for u in publish.media_urls(p):
                    self.assertTrue((root / u.replace(publish.SITE + "/", "")).is_file(), u)
            if publish.is_carousel(p):
                self.assertTrue(2 <= len(p["immagini"]) <= 10, p["id"])
            if p.get("tipo") == "storia":            # le Storie non hanno didascalia
                continue
            self.assertTrue(p["didascalia"].strip())
            self.assertLessEqual(len(p["didascalia"]), 2200, p["id"])       # limite Instagram
            if p.get("piattaforme") != ["facebook"]:        # Instagram: max 5 hashtag (i post solo Facebook: test_calendario.py)
                self.assertLessEqual(p["didascalia"].count("#"), 5, p["id"])


class Abbinati(unittest.TestCase):
    """Campo "poi": il Reel delle 23:10 porta con sé la sua Storia nella stessa esecuzione."""

    CAL = {"fuso": "Europe/Rome", "max_ritardo_ore": 12, "post": [
        {"id": "q01-x", "tipo": "reel", "quando": "2026-10-23T23:10", "segmento": "s",
         "video": "social/video/q01-x.mp4", "didascalia": "d", "didascalia_fb": "d", "poi": "q01s-x"},
        {"id": "q01s-x", "tipo": "storia", "quando": "2026-10-23T23:13", "segmento": "s",
         "immagine": "social/img/story/q01-x.jpg"}]}

    def run_main(self, state, fail_on=None, dry=False, ora="2026-10-23T21:10:30+00:00"):
        """Esegue main() con API, file e orologio simulati; restituisce lo stato salvato e i POST fatti."""
        import tempfile
        from datetime import datetime as real_dt
        f = Fake()

        def call(base, method, path, token, params=None):
            if fail_on and method == "POST" and path.endswith(fail_on):
                raise publish.ApiError("simulato")
            return f(base, method, path, token, params)

        class Clock(real_dt):
            @classmethod
            def now(cls, tz=None):
                return real_dt.fromisoformat(ora)

        tmp = Path(tempfile.mkdtemp())
        (tmp / "calendar.json").write_text(json.dumps(self.CAL), encoding="utf-8")
        (tmp / "published.json").write_text(json.dumps(state), encoding="utf-8")
        env = {"IG_ACCESS_TOKEN": "T", "FB_PAGE_TOKEN": "F", "FB_PAGE_ID": "PG"}
        argv = ["publish.py"] + (["--dry-run"] if dry else [])
        with mock.patch.object(publish, "call", call), mock.patch.object(publish.time, "sleep"), \
                mock.patch.object(publish, "media_ok", lambda u, t: True), mock.patch.object(publish, "datetime", Clock), \
                mock.patch.object(publish, "CAL", tmp / "calendar.json"), mock.patch.object(publish, "STATE", tmp / "published.json"), \
                mock.patch.dict(publish.os.environ, env), mock.patch.object(sys, "argv", argv):
            code = None
            try:
                publish.main()
            except SystemExit as e:
                code = e.code
        out = json.loads((tmp / "published.json").read_text(encoding="utf-8"))
        return out, [c for c in f.calls if c[0] == "POST"], code

    def test_reel_e_poi_la_storia_nella_stessa_esecuzione(self):
        st, posts, code = self.run_main({"pubblicati": {}})
        self.assertIsNone(code)
        self.assertEqual(set(st["pubblicati"]["q01-x"]), {"instagram", "facebook"})
        self.assertEqual(set(st["pubblicati"]["q01s-x"]), {"instagram", "facebook"})
        tipi = [c[2].get("media_type") for c in posts if c[1] == "U1/media"]
        self.assertEqual(tipi, ["REELS", "STORIES"])        # prima il Reel, poi la Storia

    def test_se_il_reel_fallisce_la_storia_aspetta(self):
        st, posts, code = self.run_main({"pubblicati": {}}, fail_on="/videos")      # Reel su Facebook in errore
        self.assertEqual(code, 1)
        self.assertNotIn("q01s-x", st["pubblicati"])
        self.assertFalse(any(c[2].get("media_type") == "STORIES" for c in posts))

    def test_storia_gia_uscita_non_si_ripete(self):
        st0 = {"pubblicati": {"q01s-x": {"instagram": {"link": "x"}, "facebook": {"link": "y"}}}}
        st, posts, code = self.run_main(st0)
        self.assertIsNone(code)
        self.assertFalse(any(c[2].get("media_type") == "STORIES" for c in posts))

    def test_dry_run_non_pubblica_nessuno_dei_due(self):
        st, posts, code = self.run_main({"pubblicati": {}}, dry=True)
        self.assertEqual(posts, [])
        self.assertEqual(st["pubblicati"], {})

    def test_ripiego_la_storia_esce_da_sola_dopo_le_23_13(self):
        st0 = {"pubblicati": {"q01-x": {"instagram": {"link": "x"}, "facebook": {"link": "y"}}}}
        st, posts, code = self.run_main(st0, ora="2026-10-23T21:20:00+00:00")
        self.assertIsNone(code)
        self.assertIn("instagram", st["pubblicati"]["q01s-x"])


class TikTokBuffer(unittest.TestCase):
    """Invio a Buffer dei Reel solo TikTok (nessuna chiamata di rete)."""
    from datetime import datetime as _dt, timezone as _tz

    def setUp(self):
        self.cal = {"fuso": "Europe/Rome", "max_ritardo_ore": 12, "post": [
            {"id": "t1", "tipo": "reel", "quando": "2026-10-13T20:17", "video": "social/video/tiktok/a.mp4",
             "piattaforme": ["tiktok"], "didascalia": "d #BookTokItalia", "miniatura_ms": 1500},
            {"id": "t2", "tipo": "reel", "quando": "2026-10-20T21:14", "video": "social/video/tiktok/b.mp4",
             "piattaforme": ["tiktok"], "didascalia": "d2"},
            {"id": "ig", "tipo": "reel", "quando": "2026-10-13T12:30", "video": "social/video/r.mp4", "didascalia": "x"}]}
        self.env = mock.patch.dict(publish.os.environ, {"BUFFER_API_KEY": "K", "BUFFER_TIKTOK_CHANNEL": "CH"})
        self.env.start()
        self.state_file = mock.patch.object(publish, "STATE", mock.MagicMock())
        self.state_file.start()

    def tearDown(self):
        self.env.stop()
        self.state_file.stop()

    def run_pass(self, now, state, risposta=None):
        calls = []

        def fake(query, variables=None):
            calls.append(variables)
            return risposta or {"createPost": {"post": {"id": "B1", "dueAt": "2026-10-13T18:17:00.000Z"}}}
        with mock.patch.object(publish, "buffer_call", fake), mock.patch.object(publish, "media_ok", return_value=True):
            err = publish.tiktok_pass(self.cal, state, now)
        return calls, err

    def test_invio_con_orario_esatto_in_utc(self):
        state = {"pubblicati": {}}
        now = self._dt(2026, 10, 13, 10, 0, tzinfo=self._tz.utc)          # 12:00 a Zurigo, il post è alle 20:17
        calls, err = self.run_pass(now, state)
        self.assertEqual(err, [])
        self.assertEqual(len(calls), 1)                                   # t2 è oltre le 36 ore
        inp = calls[0]["input"]
        self.assertEqual(inp["mode"], "customScheduled")
        self.assertEqual(inp["dueAt"], "2026-10-13T18:17:00.000Z")
        self.assertEqual(inp["channelId"], "CH")
        self.assertTrue(inp["metadata"]["tiktok"]["isAiGenerated"])
        self.assertEqual(inp["assets"][0]["video"]["url"], "https://libri.diasio.ch/social/video/tiktok/a.mp4")
        self.assertEqual(state["pubblicati"]["t1"]["tiktok"]["buffer_post_id"], "B1")

    def test_non_reinvia_mai(self):
        state = {"pubblicati": {"t1": {"tiktok": {"buffer_post_id": "B1"}}}}
        calls, _ = self.run_pass(self._dt(2026, 10, 13, 17, 0, tzinfo=self._tz.utc), state)
        self.assertEqual(calls, [])

    def test_in_scadenza_esce_subito(self):
        state = {"pubblicati": {}}
        calls, _ = self.run_pass(self._dt(2026, 10, 13, 18, 30, tzinfo=self._tz.utc), state)
        self.assertEqual(calls[0]["input"]["mode"], "shareNow")
        self.assertNotIn("dueAt", calls[0]["input"])

    def test_troppo_in_ritardo_viene_saltato(self):
        state = {"pubblicati": {}}
        calls, _ = self.run_pass(self._dt(2026, 10, 14, 12, 0, tzinfo=self._tz.utc), state)
        self.assertEqual(calls, [])
        self.assertIn("saltato", state["pubblicati"]["t1"]["tiktok"])

    def test_errore_buffer_non_segna_il_post(self):
        state = {"pubblicati": {}}
        _, err = self.run_pass(self._dt(2026, 10, 13, 10, 0, tzinfo=self._tz.utc), state,
                               {"createPost": {"message": "video non valido"}})
        self.assertTrue(err)
        self.assertNotIn("t1", state["pubblicati"])

    def test_risposta_incerta_blocca_i_doppioni(self):
        state = {"pubblicati": {}}

        def boom(query, variables=None):
            raise publish.Incerto("timeout")
        with mock.patch.object(publish, "buffer_call", boom), mock.patch.object(publish, "media_ok", return_value=True):
            err = publish.tiktok_pass(self.cal, state, self._dt(2026, 10, 13, 10, 0, tzinfo=self._tz.utc))
        self.assertTrue(err)
        self.assertIn("incerto", state["pubblicati"]["t1"]["tiktok"])

    def test_instagram_e_facebook_ignorano_i_post_tiktok(self):
        state = {"pubblicati": {}}
        self.assertEqual(publish.pending(self.cal["post"][0], state, ["instagram", "facebook"]), [])
        self.assertEqual(publish.pending(self.cal["post"][2], state, ["instagram", "facebook"]), ["instagram", "facebook"])


if __name__ == "__main__":
    unittest.main()
