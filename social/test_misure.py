import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import misure  # noqa: E402
import publish  # noqa: E402

ADESSO = datetime(2026, 11, 12, 12, 0, tzinfo=timezone.utc)
CAL = {"post": [{"id": "r06-oblio-igiene", "tipo": "reel"}, {"id": "n07-bug-x"}, {"id": "st-vuoto-a", "tipo": "storia"}, {"id": "t01-x", "tipo": "testo"}]}
STATO = {
    "r06-oblio-igiene": {"instagram": {"media_id": "1", "link": "l1", "ora_utc": "2026-11-10T11:00:00+00:00"}},
    "n07-bug-x": {"instagram": {"media_id": "2", "link": "l2", "ora_utc": "2026-09-01T11:00:00+00:00"}},
    "st-vuoto-a": {"instagram": {"media_id": "3", "link": "l3", "ora_utc": "2026-11-11T11:00:00+00:00"}},
    "t01-x": {"facebook": {"post_id": "9"}},
}


def finta(risposte, chiamate):
    def call(base, method, path, token, params=None):
        chiamate.append((path, params["metric"]))
        r = risposte[path.split("/")[0]]
        if isinstance(r, Exception):
            raise r
        return {"data": [{"name": k, "values": [{"value": v}]} for k, v in r.items()]}
    return call


class Misure(unittest.TestCase):
    def test_reel_e_immagine(self):
        ch = []
        post, err = misure.aggiorna(CAL, STATO, {}, "tok", ADESSO, call=finta({"1": {"reach": 100, "shares": 4, "ig_reels_avg_watch_time": 5200}, "2": {"reach": 40, "saved": 2}}, ch))
        self.assertEqual(err, [])
        self.assertEqual(set(post), {"r06-oblio-igiene", "n07-bug-x"})          # Storie e testi non si misurano
        self.assertIn("ig_reels_avg_watch_time", ch[0][1]); self.assertNotIn("ig_reels_avg_watch_time", ch[1][1])
        self.assertEqual(post["r06-oblio-igiene"]["libro"], "oblio"); self.assertEqual(post["r06-oblio-igiene"]["serie"], "Reel dei libri")

    def test_post_vecchi_gia_misurati_non_si_rileggono(self):
        ch = []
        vecchie = {"post": {"n07-bug-x": {"reach": 40, "tipo": "immagine", "uscito": "2026-09-01T11:00:00+00:00"}}}
        post, _ = misure.aggiorna(CAL, STATO, vecchie, "tok", ADESSO, call=finta({"1": {"reach": 1}}, ch))
        self.assertEqual([c[0] for c in ch], ["1/insights"]); self.assertEqual(post["n07-bug-x"]["reach"], 40)

    def test_senza_permesso_si_ferma(self):
        e = publish.ApiError('GET 1/insights: HTTP 400 {"error":{"message":"(#10) Application does not have permission for this action","code":10}}')
        with self.assertRaises(misure.SenzaPermesso):
            misure.aggiorna(CAL, STATO, {}, "tok", ADESSO, call=finta({"1": e, "2": {}}, []))

    def test_errore_su_un_post_non_blocca_gli_altri(self):
        e = publish.ApiError("GET 2/insights: HTTP 400 media non trovato")
        post, err = misure.aggiorna(CAL, STATO, {}, "tok", ADESSO, call=finta({"1": {"reach": 9}, "2": e}, []))
        self.assertEqual(list(post), ["r06-oblio-igiene"]); self.assertEqual(len(err), 1)

    def test_post_eliminato_non_e_un_problema_di_permesso(self):
        e = publish.ApiError('GET 2/insights: HTTP 400 {"error":{"message":"Unsupported get request. Object with ID \'2\' does not exist, cannot be loaded '
                             'due to missing permissions, or does not support this operation","type":"IGApiException","code":100,"error_subcode":33}}')
        post, err = misure.aggiorna(CAL, STATO, {}, "tok", ADESSO, call=finta({"1": {"reach": 9}, "2": e}, []))
        self.assertEqual(list(post), ["r06-oblio-igiene"]); self.assertEqual(len(err), 1)

    def test_rapporto(self):
        post, _ = misure.aggiorna(CAL, STATO, {}, "tok", ADESSO, call=finta({"1": {"reach": 100, "shares": 4, "ig_reels_avg_watch_time": 5200}, "2": {"reach": 40}}, []))
        t = misure.rapporto({"aggiornato": ADESSO.isoformat(), "post": post, "profilo": [{"giorno": "2026-11-12", "follower": 120, "contenuti": 90}], "errori": []})
        self.assertIn("4.0%", t); self.assertIn("5.2 s", t); self.assertIn("| 2026-11-12 | 120 | 90 |", t)

    def test_serie(self):
        self.assertEqual(misure.serie("q12-tritacarne"), "Frase delle 23:10"); self.assertEqual(misure.serie("mt1-sala"), "Moduli ticinesi")
        self.assertEqual(misure.serie("asmr1-aritmetica-mandarino"), "ASMR"); self.assertEqual(misure.serie("vn1-vuoto-wifi"), "Voce narrante"); self.assertEqual(misure.serie("vl5-vuoto-modulo"), "Reel Vuoto")


if __name__ == "__main__":
    unittest.main()
