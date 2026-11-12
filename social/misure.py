#!/usr/bin/env python3
"""Misure dei post Instagram: copertura, tempo di visione, invii, salvataggi.

Legge published.json (media_id di ogni post uscito) e chiede a Instagram gli Insights di ciascuno.
Scrive social/misure.json (dati) e social/MISURE.md (tabelle leggibili). Non pubblica e non modifica nulla su Instagram.

Variabili d'ambiente:
  IG_ACCESS_TOKEN   lo stesso token di publish.py; serve il permesso instagram_business_manage_insights.

Uso:
  python3 social/misure.py            # aggiorna i post degli ultimi 35 giorni e quelli mai misurati
  python3 social/misure.py --tutti    # rilegge tutti i post

Perché: i segnali che Instagram dichiara di usare per i Reel sono tempo di visione, like e invii
(vedi social/STRATEGIA.md). Senza questi numeri ogni scelta di calendario resta un'ipotesi.
"""
import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import publish  # noqa: E402  (call, ApiError, IG_API, CAL, STATE)

ROOT = Path(__file__).resolve().parent
OUT_JSON, OUT_MD = ROOT / "misure.json", ROOT / "MISURE.md"
GIORNI = 35
COMUNI = ["reach", "likes", "comments", "shares", "saved", "total_interactions", "views"]
REEL = COMUNI + ["ig_reels_avg_watch_time", "ig_reels_video_view_total_time"]
SERIE = [("q", "Frase delle 23:10"), ("asmr", "ASMR"), ("mt", "Moduli ticinesi"), ("pb", "La puntata"), ("mu", "Musica"), ("vl", "Reel Vuoto"),
         ("r", "Reel dei libri"), ("c", "Caroselli"), ("x", "Aritmetica e Vuoto, dicembre"), ("n", "Grafiche Bug/Oblio"), ("d", "Grafiche di dicembre"),
         ("g", "Grafiche Vuoto"), ("a", "Aritmetica, lancio"), ("v", "Vuoto, lancio")]


class SenzaPermesso(Exception):
    pass


def serie(pid):
    for pref, nome in SERIE:
        if pid.startswith(pref) and (len(pid) == len(pref) or not pid[len(pref)].isalpha() or pref in ("asmr", "mt", "pb", "mu", "vl")):
            return nome
    return "Altro"


def libro(pid):
    for k in ("bug", "oblio", "vuoto", "aritmetica"):
        if k in pid:
            return k
    return ""


def leggi(media_id, tipo, token, call=None):
    """Insights di un contenuto. Ritorna un dizionario metrica -> valore; solleva SenzaPermesso se il token non può leggerli."""
    call = call or publish.call
    metriche = REEL if tipo == "reel" else COMUNI
    try:
        r = call(publish.IG_API, "GET", f"{media_id}/insights", token, {"metric": ",".join(metriche)})
    except publish.ApiError as e:
        t = str(e)
        c = t.replace(" ", "")
        if "(#10)" in t or '"code":10,' in c or '"code":10}' in c or '"code":200,' in c or '"code":200}' in c:
            raise SenzaPermesso(t)
        if '"code":100' in c:         # contenuto eliminato dall'app o non leggibile: si salta, non è un problema del token
            raise
        if tipo == "reel":            # alcune metriche non esistono per tutti i Reel: riprova con quelle comuni
            r = call(publish.IG_API, "GET", f"{media_id}/insights", token, {"metric": ",".join(COMUNI)})
        else:
            raise
    out = {}
    for m in r.get("data", []):
        v = (m.get("values") or [{}])[0].get("value", m.get("total_value", {}).get("value"))
        if v is not None:
            out[m["name"]] = v
    return out


def aggiorna(cal, stato, vecchie, token, adesso, tutti=False, call=None):
    tipi = {p["id"]: p.get("tipo", "immagine") for p in cal["post"]}
    post = dict(vecchie.get("post", {}))
    errori = []
    for pid, s in stato.items():
        ig = s.get("instagram") or {}
        mid, ora = ig.get("media_id"), ig.get("ora_utc")
        tipo = tipi.get(pid, post.get(pid, {}).get("tipo", "immagine"))
        if not mid or not ora or tipo in ("storia", "testo"):      # le Storie scadono dopo 24 ore: non si misurano qui
            continue
        eta = adesso - datetime.fromisoformat(ora)
        if not tutti and pid in post and eta > timedelta(days=GIORNI):
            continue
        try:
            m = leggi(mid, tipo, token, call)
        except SenzaPermesso:
            raise
        except publish.ApiError as e:
            errori.append(f"{pid}: {str(e)[:160]}")
            continue
        m.update(tipo=tipo, serie=serie(pid), libro=libro(pid), uscito=ora, link=ig.get("link", ""))
        post[pid] = m
    return post, errori


def pct(a, b):
    return f"{100 * a / b:.1f}%" if b else "–"


def tabella(righe, intest):
    out = ["| " + " | ".join(intest) + " |", "|" + "|".join("---" for _ in intest) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in righe]
    return "\n".join(out)


def rapporto(dati):
    post = dati["post"]
    L = [f"# Misure dei post Instagram\n\nAggiornato: {dati['aggiornato'][:16].replace('T', ' ')} UTC. Post misurati: {len(post)}. "
         "File scritto da `social/misure.py`: non modificarlo a mano.\n",
         "Come leggerlo: **copertura** = account raggiunti; **invii** = condivisioni in privato, il segnale che Instagram dice di pesare di più "
         "per arrivare a chi non segue; **visione media** = secondi guardati in media (solo Reel).\n"]
    if dati.get("profilo"):
        L.append("## Profilo\n\n" + tabella([(x["giorno"], x.get("follower", "–"), x.get("contenuti", "–")) for x in dati["profilo"][-12:]],
                                            ["Giorno", "Follower", "Contenuti"]) + "\n")
    gruppi = defaultdict(list)
    for pid, m in post.items():
        gruppi[m.get("serie", "Altro")].append(m)
    righe = []
    for nome, ms in sorted(gruppi.items(), key=lambda kv: -sum(x.get("reach", 0) for x in kv[1]) / len(kv[1])):
        n = len(ms); cop = sum(x.get("reach", 0) for x in ms); inv = sum(x.get("shares", 0) for x in ms); sal = sum(x.get("saved", 0) for x in ms)
        vm = [x["ig_reels_avg_watch_time"] / 1000 for x in ms if x.get("ig_reels_avg_watch_time")]
        righe.append((nome, n, round(cop / n), pct(inv, cop), pct(sal, cop), f"{sum(vm) / len(vm):.1f} s" if vm else "–"))
    L.append("## Per serie (media a post)\n\n" + tabella(righe, ["Serie", "Post", "Copertura media", "Invii / copertura", "Salvataggi / copertura", "Visione media"]) + "\n")
    lib = defaultdict(list)
    for m in post.values():
        if m.get("libro"):
            lib[m["libro"]].append(m)
    if lib:
        L.append("## Per libro\n\n" + tabella([(k, len(v), round(sum(x.get("reach", 0) for x in v) / len(v)), pct(sum(x.get("shares", 0) for x in v), sum(x.get("reach", 0) for x in v)))
                                               for k, v in sorted(lib.items())], ["Libro", "Post", "Copertura media", "Invii / copertura"]) + "\n")

    def riga(pid, m):
        vm = m.get("ig_reels_avg_watch_time")
        return (pid, m.get("tipo", ""), m["uscito"][:10], m.get("reach", 0), m.get("likes", 0), m.get("shares", 0), m.get("saved", 0), f"{vm / 1000:.1f} s" if vm else "–")
    intest = ["Post", "Tipo", "Uscito", "Copertura", "Like", "Invii", "Salvati", "Visione media"]
    per_cop = sorted(post.items(), key=lambda kv: -kv[1].get("reach", 0))
    limite = (datetime.fromisoformat(dati["aggiornato"]) - timedelta(days=3)).date().isoformat()
    L.append("## I 15 post con più copertura\n\n" + tabella([riga(*x) for x in per_cop[:15]], intest) + "\n")
    L.append("## I 10 post con meno copertura (usciti da almeno 3 giorni)\n\n" + tabella(
        [riga(*x) for x in [y for y in reversed(per_cop) if y[1]["uscito"][:10] <= limite][:10]], intest) + "\n")
    if dati.get("errori"):
        L.append("## Post non letti\n\n" + "\n".join(f"- {e}" for e in dati["errori"]) + "\n")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tutti", action="store_true", help="rilegge anche i post più vecchi di 35 giorni")
    a = ap.parse_args()
    token = os.environ.get("IG_ACCESS_TOKEN", "").strip()
    if not token:
        sys.exit("Manca IG_ACCESS_TOKEN.")
    cal = json.loads(publish.CAL.read_text(encoding="utf-8"))
    stato = json.loads(publish.STATE.read_text(encoding="utf-8"))["pubblicati"]
    vecchie = json.loads(OUT_JSON.read_text(encoding="utf-8")) if OUT_JSON.exists() else {}
    adesso = datetime.now(timezone.utc)
    try:
        post, errori = aggiorna(cal, stato, vecchie, token, adesso, a.tutti)
    except SenzaPermesso as e:
        print("::error::Il token Instagram non può leggere gli Insights: serve il permesso instagram_business_manage_insights "
              "(vedi social/README.md, sezione Misure). Nessun file modificato.")
        print(str(e)[:300])
        sys.exit(1)
    if errori and not post:      # nemmeno un post letto: non è un contenuto eliminato, è il token
        print("::error::Nessun post letto: probabilmente al token manca il permesso instagram_business_manage_insights "
              "(vedi social/README.md, sezione Misure). Nessun file modificato.")
        print(errori[0])
        sys.exit(1)
    profilo = list(vecchie.get("profilo", []))
    try:
        me = publish.call(publish.IG_API, "GET", "me", token, {"fields": "followers_count,media_count"})
        oggi = adesso.date().isoformat()
        profilo = [x for x in profilo if x["giorno"] != oggi] + [{"giorno": oggi, "follower": me.get("followers_count"), "contenuti": me.get("media_count")}]
    except publish.ApiError as e:
        errori.append(f"profilo: {str(e)[:160]}")
    dati = {"aggiornato": adesso.isoformat(), "profilo": profilo, "post": post, "errori": errori}
    OUT_JSON.write_text(json.dumps(dati, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    OUT_MD.write_text(rapporto(dati), encoding="utf-8")
    print(f"Misurati {len(post)} post, {len(errori)} non letti. Scritti {OUT_JSON.name} e {OUT_MD.name}.")


if __name__ == "__main__":
    main()
