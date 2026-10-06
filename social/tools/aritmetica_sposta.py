"""Sposta dopo il 2/11/2026 i 13 post Bug/Oblio che cedono lo slot ai post di lancio de L'Aritmetica del Consenso.
Uso, da social/tools: python aritmetica_sposta.py (una volta sola, dopo `python carousel.py --calendar`).
Ogni post spostato va nel primo giorno libero dopo il 2/11 nella stessa fascia (o, se piena, nell'altra fascia dello stesso giorno della settimana);
il minuto è scelto dentro la finestra del cron e diverso da quello dei vicini della stessa fascia (test_calendario.py)."""
import json, random, sys
from datetime import datetime, timedelta
from pathlib import Path

SOCIAL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SOCIAL))
import test_calendario as T                 # finestre e regole di test_calendario.py

CEDONO = {"a01-aritmetica-annuncio": "03-bug-cognato", "a02-aritmetica-quaderno": "04-oblio-domanda", "a03-aritmetica-direttori": "05-oblio-costo",
          "a04-aritmetica-silenzio": "n09-bug-alma", "a05-aritmetica-dopo": "n10-oblio-dora", "a06-aritmetica-posta": "n13-oblio-ricordo-non-suo",
          "a07-aritmetica-ci-penso": "07-bug-cta", "a08-aritmetica-storia": "s03-oblio-cugino", "a09-aritmetica-troverai": "08-oblio-levia",
          "a10-aritmetica-listino": "n19-oblio-modulo", "a11-aritmetica-da-oggi": "n20-bug-elio-bassi", "a12-aritmetica-lettera": "t02-oblio-ricordo",
          "a13-aritmetica-incipit": "10-bug-domanda"}
DAL = datetime(2026, 11, 3)


def main():
    p = SOCIAL / "calendar.json"
    cal = json.loads(p.read_text(encoding="utf-8"))
    post = {x["id"]: x for x in cal["post"]}
    occ = {(datetime.fromisoformat(x["quando"]).date(), datetime.fromisoformat(x["quando"]).hour) for x in cal["post"]}
    # i post che cedono liberano il loro slot: ma vanno rimessi dopo il 2/11, in ordine di data originale
    da_spostare = sorted((post[v] for v in CEDONO.values()), key=lambda x: x["quando"])
    for x in da_spostare:
        d0 = datetime.fromisoformat(x["quando"])
        occ.discard((d0.date(), d0.hour))
    rnd = random.Random(20261023)
    for x in da_spostare:
        d0 = datetime.fromisoformat(x["quando"])
        done = False
        day = DAL
        while not done:
            if day.weekday() == d0.weekday():
                ore = [d0.hour] + [f[0] for f in T.FINESTRE[day.weekday()] if f[0] != d0.hour]
                for ora in ore:
                    if (day.date(), ora) not in occ:
                        f = next(f for f in T.FINESTRE[day.weekday()] if f[0] == ora)
                        minuto = rnd.randint(max(0, f[1] - 4), f[2] - 2)
                        x["quando"] = day.replace(hour=ora, minute=minuto).strftime("%Y-%m-%dT%H:%M")
                        occ.add((day.date(), ora))
                        done = True
                        break
            day += timedelta(days=1)
        print("→", x["id"], "da", d0.strftime("%d/%m %H:%M"), "a", x["quando"])
    cal["post"].sort(key=lambda x: x["quando"])
    p.write_text(json.dumps(cal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
