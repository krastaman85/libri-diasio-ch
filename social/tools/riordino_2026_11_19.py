# Riordino del calendario del 19/11/2026 (regola di Davide: al massimo DUE post al giorno contando la rubrica
# delle 23:10, quindi un solo post di feed al giorno su Instagram e Facebook, anche i testi solo Facebook).
# - La puntata (pb4…pb8) slitta di una settimana: resta martedì/venerdì, così le immagini («esce martedì/venerdì») restano vere;
#   venerdì 27/11 è il giorno di Venerdì Nero.
# - I Moduli (mt4…mt8) cedono i giorni della campagna di Venerdì Nero; mt4 esce di martedì (1/12), mt8 a gennaio.
# - Natale: c06 al 19/12, t06 al 22/12; i post senza data (x04, d06, r21, r22, n15, t04, t05) vanno nei giorni liberi di gennaio;
#   mai due post dello stesso libro in giorni di fila, fuori dalle serie.
# - TikTok degli ASMR: la stessa sera del Reel su Instagram (21:05).
# Lanciato una volta. Gli orari stanno nelle finestre di cron-job.org (social/test_calendario.py).
# NB: non rilanciare piano_diasio_calendario.py (riporterebbe le date del 3/11).
import json
from datetime import datetime, timedelta
from pathlib import Path

SOCIAL = Path(__file__).resolve().parent.parent
NUOVE = {
    "mt4-verbale-assemblea": "2026-12-01T19:41",
    "pb4-bug-puntata-4": "2026-12-04T18:21",
    "mt5-certificato-grotto": "2026-12-07T18:38",
    "pb5-bug-puntata-5": "2026-12-08T19:46",
    "mt6-accettazione-nebbia": "2026-12-10T12:41",
    "pb6-bug-puntata-6": "2026-12-11T18:33",
    "mt7-listino-scuse": "2026-12-14T18:19",
    "pb7-bug-puntata-7": "2026-12-15T19:27",
    "pb8-bug-puntata-8": "2026-12-18T18:14",
    "c06-natale-albero": "2026-12-19T12:27",
    "t06-feste": "2026-12-22T12:33",
    "x04-aritmetica-due-mani": "2027-01-01T18:18",
    "d08-bug-nel-dubbio": "2026-12-29T12:09",
    "d06-oblio-regolatevi": "2027-01-02T12:12",
    "mt8-ricevuta-ascensore": "2027-01-04T18:22",
    "n15-oblio-otto-milioni": "2027-01-06T19:47",
    "r21-oblio-gratis": "2027-01-08T12:14",
    "t04-oblio-listino": "2027-01-11T12:16",
    "t05-newsletter": "2027-01-09T12:34",
    "r22-bug-rettifica": "2027-01-12T19:34",
    "tasmr6-aritmetica-registratore": "2026-11-29T21:05",
    "tasmr3-aritmetica-lago": "2027-01-05T21:05",
    "tasmr4-vuoto-diffusore": "2027-01-07T21:05",
}
TESTI = {"pb3-bug-puntata-3": ("La puntata 4 esce venerdì.", "La puntata 4 esce venerdì 4 dicembre.")}

p = SOCIAL / "calendar.json"
raw = p.read_text(encoding="utf-8")
cal = json.loads(raw)
pub = json.loads((SOCIAL / "published.json").read_text(encoding="utf-8"))["pubblicati"]
voci = {x["id"]: x for x in cal["post"]}
for pid, q in NUOVE.items():
    x = voci[pid]
    assert pid not in pub, pid
    x["quando"] = q
    if x.get("poi"):
        voci[x["poi"]]["quando"] = (datetime.fromisoformat(q) + timedelta(minutes=3)).strftime("%Y-%m-%dT%H:%M")
for pid, (a, b) in TESTI.items():
    for k in ("didascalia", "didascalia_fb"):
        if voci[pid].get(k) and a in voci[pid][k]:
            voci[pid][k] = voci[pid][k].replace(a, b)
cal["post"].sort(key=lambda x: x["quando"])
eol = "\r\n" if "\r\n" in raw else "\n"
p.write_text((json.dumps(cal, indent=2, ensure_ascii=False) + "\n").replace("\n", eol), encoding="utf-8", newline="")
print("spostati", len(NUOVE))
