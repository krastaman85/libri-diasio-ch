"""Verifica che gli orari dei post non ancora pubblicati cadano nelle finestre di avvio del cron esterno.
Uso: python3 -m unittest social/test_calendario.py
Le finestre sono quelle di social/AVVIO-ESTERNO.md (ora Europe/Zurich = fuso del calendario)."""
import json, unittest
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


if __name__ == "__main__":
    unittest.main()
