"""Verifica che gli orari dei post non ancora pubblicati cadano nelle finestre di avvio del cron esterno.
Uso: python3 -m unittest social/test_calendario.py
Le finestre sono quelle di social/AVVIO-ESTERNO.md (ora Europe/Zurich = fuso del calendario)."""
import json, re, unittest
from datetime import datetime
from pathlib import Path

DIR = Path(__file__).resolve().parent
# giorno (lunedi=0) -> (ora, primo avvio, ultimo avvio); l'orario del post va da primo-4 a ultimo-2 minuti
FINESTRE = {0: (18, 7, 52), 1: (19, 17, 57), 2: (19, 17, 57), 3: (12, 12, 52),
            4: (18, 2, 42), 5: (12, 2, 47), 6: (20, 2, 47)}
DAL = datetime(2026, 10, 5)


def da_controllare():
    cal = json.loads((DIR / "calendar.json").read_text(encoding="utf-8"))
    pub = json.loads((DIR / "published.json").read_text(encoding="utf-8"))["pubblicati"]
    for p in sorted(cal["post"], key=lambda x: x["quando"]):
        d = datetime.fromisoformat(p["quando"])
        if p["id"] not in pub and d >= DAL:
            yield p["id"], d


class FinestreCron(unittest.TestCase):
    def test_orari_dentro_le_finestre(self):
        for pid, d in da_controllare():
            ora, primo, ultimo = FINESTRE[d.weekday()]
            self.assertEqual(d.hour, ora, f"{pid} {d}: ora fuori finestra")
            self.assertTrue(max(0, primo - 4) <= d.minute <= ultimo - 2, f"{pid} {d}: minuto fuori finestra")

    def test_minuti_non_ripetuti_nello_stesso_giorno_della_settimana(self):
        ultimo = {}
        for pid, d in da_controllare():
            self.assertNotEqual(ultimo.get(d.weekday()), d.minute, f"{pid}: stesso minuto della settimana prima")
            ultimo[d.weekday()] = d.minute


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


if __name__ == "__main__":
    unittest.main()
