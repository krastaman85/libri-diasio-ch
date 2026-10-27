"""Verifica che gli orari dei post non ancora pubblicati cadano nelle finestre di avvio del cron esterno.
Uso: python3 -m unittest social/test_calendario.py
Le finestre sono quelle di social/AVVIO-ESTERNO.md (ora Europe/Zurich = fuso del calendario)."""
import json, re, unittest
from datetime import datetime
from pathlib import Path

DIR = Path(__file__).resolve().parent
# giorno (lunedi=0) -> finestre (ora, primo avvio, ultimo avvio); l'orario del post va da primo-4 a ultimo-2 minuti.
# Due uscite al giorno dal 6/10/2026: pranzo e sera (giovedi sera e sabato pomeriggio al posto del pranzo gia occupato).
FINESTRE = {0: [(18, 7, 52), (12, 2, 57)], 1: [(19, 17, 57), (12, 2, 57)], 2: [(19, 17, 57), (12, 2, 57)],
            3: [(12, 12, 52), (19, 7, 52)], 4: [(18, 2, 42), (12, 2, 57)], 5: [(12, 2, 47), (17, 2, 47)],
            6: [(20, 2, 47), (12, 2, 57)]}
DAL = datetime(2026, 10, 5)
# Rubrica «Citazioni D. Iasio» (decisione dell'utente del 12/10/2026): ogni sera alle 23:10 esatte il Reel,
# subito dopo la Storia (campo "poi" del Reel; 23:13 è l'orario di ripiego), con un job dedicato su cron-job.org (ogni giorno alle 23:10). Orario fisso: niente minuti variabili.
RUBRICA = re.compile(r"^q\d\d(s)?-")


def rubrica(pid):
    return RUBRICA.match(pid) is not None


def tiktok(p):
    """Post solo TikTok (dal 12/10/2026): li pubblica Buffer all'orario esatto, fuori dalle finestre di cron-job.org."""
    return p.get("piattaforme") == ["tiktok"]


def file_serve(p):
    """Vero se i file del post servono ancora: post non ancora uscito su tutte le sue piattaforme.
    I media dei post già usciti si tolgono dal repo dopo ogni serie (social/tools/pulisci_media.py, 27/10/2026)."""
    pub = json.loads((DIR / "published.json").read_text(encoding="utf-8"))["pubblicati"].get(p["id"], {})
    if pub.get("saltato"):
        return False
    piatt = p.get("piattaforme") or (["facebook"] if p.get("tipo") == "testo" else ["instagram", "facebook"])
    return any(x not in pub for x in piatt)


def da_controllare():
    cal = json.loads((DIR / "calendar.json").read_text(encoding="utf-8"))
    pub = json.loads((DIR / "published.json").read_text(encoding="utf-8"))["pubblicati"]
    for p in sorted(cal["post"], key=lambda x: x["quando"]):
        d = datetime.fromisoformat(p["quando"])
        if p["id"] not in pub and d >= DAL and not rubrica(p["id"]) and not tiktok(p):
            yield p["id"], d


def finestra(d):
    """Finestra del giorno che contiene l'ora del post, oppure None."""
    for f in FINESTRE[d.weekday()]:
        if f[0] == d.hour:
            return f
    return None


class FinestreCron(unittest.TestCase):
    def test_orari_dentro_le_finestre(self):
        for pid, d in da_controllare():
            f = finestra(d)
            self.assertIsNotNone(f, f"{pid} {d}: ora fuori finestra (ammesse {[x[0] for x in FINESTRE[d.weekday()]]})")
            ora, primo, ultimo = f
            self.assertTrue(max(0, primo - 4) <= d.minute <= ultimo - 2, f"{pid} {d}: minuto fuori finestra")

    def test_minuti_non_ripetuti_nella_stessa_fascia_della_settimana_dopo(self):
        ultimo = {}
        for pid, d in da_controllare():
            k = (d.weekday(), d.hour)
            self.assertNotEqual(ultimo.get(k), d.minute, f"{pid}: stesso minuto della settimana prima")
            ultimo[k] = d.minute

    def test_una_sola_uscita_per_fascia(self):
        visti = {}
        for pid, d in da_controllare():
            k = (d.date(), d.hour)
            self.assertNotIn(k, visti, f"{pid} e {visti.get(k)}: due uscite nella stessa fascia")
            visti[k] = pid


class RubricaCitazioni(unittest.TestCase):
    """Reel alle 23:10 e Storia alle 23:13, una coppia per sera, file presenti, firma e riga Kindle nelle didascalie."""

    def setUp(self):
        cal = json.loads((DIR / "calendar.json").read_text(encoding="utf-8"))
        self.q = [p for p in cal["post"] if rubrica(p["id"])]

    def test_orari_fissi(self):
        for p in self.q:
            d = datetime.fromisoformat(p["quando"])
            atteso = (23, 13) if p["tipo"] == "storia" else (23, 10)
            self.assertEqual((d.hour, d.minute), atteso, f"{p['id']}: {p['quando']}")

    def test_una_coppia_per_sera(self):
        per_giorno = {}
        for p in self.q:
            per_giorno.setdefault(p["quando"][:10], []).append(p["tipo"])
        for g, tipi in per_giorno.items():
            self.assertEqual(sorted(tipi), ["reel", "storia"], f"{g}: {tipi}")

    def test_i_file_esistono(self):
        for p in self.q:
            if not file_serve(p):
                continue
            f = p.get("video") or p.get("immagine")
            self.assertTrue((DIR.parent / f).exists(), f"{p['id']}: manca {f}")

    def test_ogni_reel_porta_la_sua_storia(self):
        ids = {p["id"]: p for p in self.q}
        for p in self.q:
            if p["tipo"] == "reel":
                s = ids.get(p.get("poi", ""))
                self.assertIsNotNone(s, f"{p['id']}: manca il campo poi con la Storia")
                self.assertEqual(s["tipo"], "storia", p["id"])
                self.assertEqual(s["quando"][:10], p["quando"][:10], f"{p['id']}: Storia di un'altra sera")

    def test_firma_nelle_didascalie(self):
        for p in self.q:
            if p["tipo"] == "reel":
                for k in ("didascalia", "didascalia_fb"):
                    self.assertIn("— D. Iasio", p[k], f"{p['id']} {k}: manca la firma")
                    self.assertIn("Amazon Kindle", p[k], f"{p['id']} {k}: manca la riga Kindle")


class TikTok(unittest.TestCase):
    """Reel solo TikTok inviati a Buffer: file nel repo, un post al giorno in fascia serale, IA dichiarata, riga Kindle."""

    def setUp(self):
        cal = json.loads((DIR / "calendar.json").read_text(encoding="utf-8"))
        self.t = [p for p in cal["post"] if tiktok(p)]

    def test_solo_reel_con_video_presente(self):
        for p in self.t:
            self.assertEqual(p.get("tipo"), "reel", p["id"])
            if file_serve(p):
                self.assertTrue((DIR.parent / p["video"]).exists(), f"{p['id']}: manca {p['video']}")

    def test_un_post_al_giorno_tra_le_7_e_le_23(self):
        giorni = {}
        for p in self.t:
            d = datetime.fromisoformat(p["quando"])
            self.assertTrue(7 <= d.hour <= 22, f"{p['id']}: {p['quando']}")
            self.assertNotIn(d.date(), giorni, f"{p['id']} e {giorni.get(d.date())}: due TikTok lo stesso giorno")
            giorni[d.date()] = p["id"]

    def test_ia_dichiarata_e_riga_kindle(self):
        for p in self.t:
            self.assertTrue(p.get("ia", True), f"{p['id']}: contenuto IA non dichiarato")
            self.assertIn("Amazon Kindle", p["didascalia"], f"{p['id']}: manca la riga Kindle")
            self.assertNotIn("link in bio", p["didascalia"], f"{p['id']}: su TikTok il link in bio non c'è")

    def test_vuoto_prima_dell_uscita(self):
        """I Reel di Vuoto dicono «Prenota su Kindle · 23 ottobre»: su TikTok devono uscire entro il 22/10."""
        for p in self.t:
            if "/v-" in p["video"]:
                self.assertLess(p["quando"][:10], "2026-10-23", f"{p['id']}: Reel di prenotazione dopo l'uscita")


# Vocabolario scelto dall'utente (4/10/2026): genere, satira, community, geolocalizzazione.
VOCABOLARIO = {t.lower() for t in """#ThrillerItaliano #NoirItaliano #RomanzoNoir #GialloItaliano #ThrillerPsicologico
#LibriThriller #AltaTensione #LetteraturaNoir #Satira #RomanzoSatirico #UmorismoNero #Ironia #LettureDivertenti
#CommediaNera #BookstagramItalia #BookTokItalia #ConsigliDiLettura #LibriDaLeggere #RecensioneLibro #IoLeggo
#ScrittoriEmergenti #ScrittoriItaliani #SvizzeraItaliana #Ticino #ScrittoriSvizzeri #EditoriaItaliana
#LeggereInSvizzera #CulturaTicino #BookstagramSvizzera""".split()}
MAX_IG = 5      # Instagram: dal dicembre 2025 massimo 5 hashtag per post e Reel
MAX_FB = 15     # Facebook: nessun tetto noto, 10-15 consigliati


def tag(testo):
    m = re.search(r"((?:#\w+[ \t]*)+)\s*$", testo)
    return re.findall(r"#\w+", m.group(1)) if m else []


def didascalie():
    """(id, piattaforma, testo) per i post non pubblicati e con didascalia."""
    cal = json.loads((DIR / "calendar.json").read_text(encoding="utf-8"))
    pub = json.loads((DIR / "published.json").read_text(encoding="utf-8"))["pubblicati"]
    for p in cal["post"]:
        if p["id"] in pub or not p.get("didascalia"):
            continue
        solo_fb = p.get("piattaforme") == ["facebook"]
        yield p["id"], "facebook" if solo_fb else "instagram", p["didascalia"]
        if not solo_fb and p.get("didascalia_fb"):
            yield p["id"], "facebook", p["didascalia_fb"]


class Hashtag(unittest.TestCase):
    def test_conteggio_per_piattaforma(self):
        for pid, piatt, testo in didascalie():
            n = len(tag(testo))
            if piatt == "instagram":
                self.assertTrue(1 <= n <= MAX_IG, f"{pid} Instagram: {n} hashtag (max {MAX_IG})")
            else:
                self.assertTrue(10 <= n <= MAX_FB, f"{pid} Facebook: {n} hashtag (10-{MAX_FB})")

    def test_solo_vocabolario_e_senza_doppioni(self):
        for pid, piatt, testo in didascalie():
            t = [x.lower() for x in tag(testo)]
            self.assertEqual(len(t), len(set(t)), f"{pid} {piatt}: hashtag ripetuti")
            fuori = [x for x in t if x not in VOCABOLARIO]
            self.assertFalse(fuori, f"{pid} {piatt}: fuori vocabolario {fuori}")


class RigaKindle(unittest.TestCase):
    def test_ogni_didascalia_nomina_amazon_kindle(self):
        """Dal 5/10/2026 ogni didascalia non pubblicata chiude con la riga sulla disponibilita su Amazon Kindle."""
        da_dal = {pid for pid, _ in da_controllare()}
        for pid, piatt, testo in didascalie():
            if pid not in da_dal:
                continue
            self.assertIn("Amazon Kindle", testo, f"{pid} {piatt}: manca la riga su Amazon Kindle")

    def test_su_facebook_il_link_amazon_c_e(self):
        """Su Facebook ogni post non ancora pubblicato porta il link alla scheda Amazon."""
        da_dal = {pid for pid, _ in da_controllare()}
        for pid, piatt, testo in didascalie():
            if piatt == "facebook" and pid in da_dal and not re.search(r"vuoto|^v0[123]-", pid):   # i post di Vuoto hanno la regola propria in LancioVuoto
                self.assertIn("amazon.it/dp/", testo, f"{pid} Facebook: manca il link Amazon")


def lancio_aritmetica(pid):
    return re.match(r"a\d\d-aritmetica", pid) is not None


class LancioAritmetica(unittest.TestCase):
    """Post «è uscito» de L'Aritmetica del Consenso (online su Amazon Kindle dal 6/10/2026, ASIN B0HM3Y19B6): niente conto alla rovescia."""

    def test_nominano_il_libro_e_la_data(self):
        for pid, piatt, testo in didascalie():
            if lancio_aritmetica(pid):
                self.assertIn("Aritmetica del Consenso", testo, f"{pid} {piatt}: manca il titolo")
                self.assertTrue(re.search(r"è uscito", testo, re.I), f"{pid} {piatt}: manca «è uscito»")
                self.assertFalse(re.search(r"Mancano|Manca |in arrivo|Esce il", testo, re.I), f"{pid} {piatt}: resta un conto alla rovescia o un «in arrivo»")

    def test_su_facebook_il_link_al_sito(self):
        for pid, piatt, testo in didascalie():
            if lancio_aritmetica(pid) and piatt == "facebook":
                self.assertIn("libri.diasio.ch/aritmetica/", testo, f"{pid} Facebook: manca il link alla pagina del libro")
                self.assertIn("amazon.it/dp/B0HM3Y19B6", testo, f"{pid} Facebook: manca il link Amazon dell'Aritmetica")

    def test_le_immagini_esistono(self):
        cal = json.loads((DIR / "calendar.json").read_text(encoding="utf-8"))
        for p in cal["post"]:
            if lancio_aritmetica(p["id"]) and file_serve(p):
                for f in ([p["immagine"]] if p.get("immagine") else p.get("immagini", [])):
                    self.assertTrue((DIR.parent / f).exists(), f"{p['id']}: manca {f}")


LANCIO_VUOTO_REEL = ("v01-listino", "v02-sedie", "v03-regia")
ASIN_VUOTO = "B0HM4HFK34"


def lancio_vuoto(pid):
    return "vuoto" in pid or pid in LANCIO_VUOTO_REEL


class LancioVuoto(unittest.TestCase):
    """Post di lancio di «Vuoto a rendere» (su Amazon Kindle dal 23/10/2026, ASIN B0HM4HFK34)."""

    def test_nominano_il_libro(self):
        for pid, piatt, testo in didascalie():
            if lancio_vuoto(pid):
                self.assertIn("Vuoto a rendere", testo, f"{pid} {piatt}: manca il titolo")

    def test_la_data_di_uscita_e_coerente(self):
        """Prima del 23/10 si prenota («Esce il 23 ottobre»), dal 23/10 si dice «è su Amazon Kindle»: niente «è uscito» in anticipo."""
        cal = json.loads((DIR / "calendar.json").read_text(encoding="utf-8"))
        per_id = {p["id"]: datetime.fromisoformat(p["quando"]) for p in cal["post"]}
        for pid, piatt, testo in didascalie():
            if not lancio_vuoto(pid):
                continue
            if per_id[pid] < datetime(2026, 10, 23):
                self.assertFalse(re.search(r"è uscito|è disponibile|da oggi", testo, re.I), f"{pid} {piatt}: dice che è già uscito prima del 23/10")
            else:
                self.assertFalse(re.search(r"Mancano|Manca |in prenotazione|Esce il", testo, re.I), f"{pid} {piatt}: resta un conto alla rovescia dopo l'uscita")

    def test_su_facebook_il_link_al_sito_e_ad_amazon(self):
        """Il link Amazon di Vuoto compare solo se la scheda è online (js/config.js ha `vuoto.amazon`): prima del 23/10 senza link in config non c'è nemmeno nelle didascalie; dal 23/10 deve esserci sempre."""
        cfg = (DIR.parent / "js" / "config.js").read_text(encoding="utf-8")
        online = re.search(r'vuoto:\s*\{\s*amazon:\s*"https://', cfg) is not None
        cal = json.loads((DIR / "calendar.json").read_text(encoding="utf-8"))
        per_id = {p["id"]: datetime.fromisoformat(p["quando"]) for p in cal["post"]}
        for pid, piatt, testo in didascalie():
            if lancio_vuoto(pid) and piatt == "facebook":
                self.assertIn("libri.diasio.ch/vuoto/", testo, f"{pid} Facebook: manca il link alla pagina del libro")
                self.assertNotIn("amazon.it/dp/B0HM3Y19B6", testo, f"{pid} Facebook: link Amazon dell'Aritmetica per sbaglio")
                if online or per_id[pid] >= datetime(2026, 10, 23):
                    self.assertIn(f"amazon.it/dp/{ASIN_VUOTO}", testo, f"{pid} Facebook: manca il link Amazon di Vuoto")
                else:
                    self.assertNotIn("amazon.it/dp/", testo, f"{pid} Facebook: link Amazon prima che la scheda sia online")

    def test_le_immagini_e_i_video_esistono(self):
        cal = json.loads((DIR / "calendar.json").read_text(encoding="utf-8"))
        for p in cal["post"]:
            if lancio_vuoto(p["id"]) and file_serve(p):
                files = ([p["immagine"]] if p.get("immagine") else p.get("immagini", [])) + ([p["video"]] if p.get("video") else [])
                for f in files:
                    self.assertTrue((DIR.parent / f).exists(), f"{p['id']}: manca {f}")


if __name__ == "__main__":
    unittest.main()
