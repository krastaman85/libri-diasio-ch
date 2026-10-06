"""Sposta i post Bug/Oblio che occupano la stessa fascia dei post di lancio di Vuoto a rendere.
Uso, da social/tools: python vuoto_sposta.py (una volta sola, dopo `python carousel.py --calendar`).
Ogni post spostato va nel primo slot libero, dal 3/11/2026 in poi, nello stesso giorno della settimana (stessa fascia oraria, o l'altra dello stesso giorno);
il minuto cade nella finestra del cron ed e' diverso da quello dei vicini della stessa fascia (test_calendario.py)."""
import json, random, sys
from datetime import datetime, timedelta
from pathlib import Path

SOCIAL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SOCIAL))
import test_calendario as T

DAL = datetime(2026, 11, 3)
LANCIO = lambda i: "vuoto" in i or i in ("v01-listino", "v02-sedie", "v03-regia")


def main():
    p = SOCIAL / "calendar.json"
    cal = json.loads(p.read_text(encoding="utf-8"))
    slot = lambda x: (datetime.fromisoformat(x["quando"]).date(), datetime.fromisoformat(x["quando"]).hour)
    lancio = {slot(x) for x in cal["post"] if LANCIO(x["id"])}
    da_spostare = sorted((x for x in cal["post"] if not LANCIO(x["id"]) and slot(x) in lancio), key=lambda x: x["quando"])
    occ = {slot(x) for x in cal["post"] if x not in da_spostare}
    rnd = random.Random(20261006)
    for x in da_spostare:
        d0 = datetime.fromisoformat(x["quando"])
        day, done = DAL, False
        while not done:
            if day.weekday() == d0.weekday():
                for ora in [d0.hour] + [f[0] for f in T.FINESTRE[day.weekday()] if f[0] != d0.hour]:
                    if (day.date(), ora) not in occ:
                        f = next(f for f in T.FINESTRE[day.weekday()] if f[0] == ora)
                        x["quando"] = day.replace(hour=ora, minute=rnd.randint(max(0, f[1] - 4), f[2] - 2)).strftime("%Y-%m-%dT%H:%M")
                        occ.add((day.date(), ora))
                        done = True
                        break
            day += timedelta(days=1)
        print("→", x["id"], "da", d0.strftime("%d/%m %H:%M"), "a", x["quando"])
    # i minuti non devono ripetersi nella stessa fascia della settimana dopo: li ritocco finche' i vicini sono diversi
    cal["post"].sort(key=lambda x: x["quando"])
    ultimo = {}
    for x in cal["post"]:
        d = datetime.fromisoformat(x["quando"])
        if d < T.DAL or x["id"] in json.loads((SOCIAL / "published.json").read_text(encoding="utf-8"))["pubblicati"]:
            continue
        k = (d.weekday(), d.hour)
        if ultimo.get(k) == d.minute:
            f = next(f for f in T.FINESTRE[d.weekday()] if f[0] == d.hour)
            m = d.minute
            while m == ultimo[k]:
                m = rnd.randint(max(0, f[1] - 4), f[2] - 2)
            x["quando"] = d.replace(minute=m).strftime("%Y-%m-%dT%H:%M")
            print("minuto ritoccato:", x["id"], x["quando"])
            d = d.replace(minute=m)
        ultimo[k] = d.minute
    cal["post"].sort(key=lambda x: x["quando"])
    p.write_text(json.dumps(cal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
