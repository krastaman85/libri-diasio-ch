#!/usr/bin/env python3
"""Pubblica su Instagram (API con Instagram Login) i post di social/calendar.json.

Solo libreria standard. Il token arriva dalla variabile d'ambiente IG_ACCESS_TOKEN
(mai nel repo). L'ID account Instagram si ricava dal token con /me.

Uso:
  publish.py                 pubblica al massimo 1 post scaduto e non ancora pubblicato
  publish.py --dry-run       controlla token, immagine e didascalia senza pubblicare
  publish.py --id 03-...     forza un post preciso (test), ignorando data e finestra
"""
import argparse, json, os, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
API = "https://graph.instagram.com/v23.0"
SITE = "https://libri.diasio.ch"
CAL, STATE = ROOT / "calendar.json", ROOT / "published.json"


def call(method, path, token, params=None):
    params = dict(params or {})
    params["access_token"] = token
    data = urllib.parse.urlencode(params).encode()
    url = f"{API}/{path}"
    req = urllib.request.Request(url + ("?" + data.decode() if method == "GET" else ""),
                                 data=None if method == "GET" else data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        raise SystemExit(f"Errore API {method} {path}: HTTP {e.code} {body}")


def image_ok(url):
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status == 200 and "image/jpeg" in r.headers.get("Content-Type", "")
    except Exception:
        return False


def due_post(cal, state, now, forced):
    if forced:
        return next((p for p in cal["post"] if p["id"] == forced), None)
    tz = ZoneInfo(cal.get("fuso", "Europe/Rome"))
    late = timedelta(hours=cal.get("max_ritardo_ore", 12))
    for p in cal["post"]:
        if p["id"] in state["pubblicati"]:
            continue
        when = datetime.fromisoformat(p["quando"]).replace(tzinfo=tz)
        if when > now:
            continue
        if now - when > late:
            state["pubblicati"][p["id"]] = {"stato": "saltato", "motivo": "oltre la finestra di ritardo"}
            print(f"Saltato {p['id']}: programmato {p['quando']}, troppo in ritardo.")
            continue
        return p
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--id")
    a = ap.parse_args()

    token = os.environ.get("IG_ACCESS_TOKEN", "").strip()
    if not token:
        sys.exit("IG_ACCESS_TOKEN mancante (Secret del repo, sezione Actions).")
    cal = json.loads(CAL.read_text(encoding="utf-8"))
    state = json.loads(STATE.read_text(encoding="utf-8"))
    if cal.get("pausa") and not a.id:
        print("Calendario in pausa (pausa: true). Nessuna pubblicazione.")
        return

    me = call("GET", "me", token, {"fields": "user_id,username"})
    uid = me.get("user_id") or me.get("id")
    print(f"Account collegato: @{me.get('username')}")

    now = datetime.now(timezone.utc)
    p = due_post(cal, state, now, a.id)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    if not p:
        print("Nessun post da pubblicare adesso.")
        return
    image_url = f"{SITE}/{p['immagine']}"
    print(f"Post: {p['id']} ({p['segmento']}) → {image_url}")
    if not image_ok(image_url):
        sys.exit(f"Immagine non raggiungibile o non JPEG: {image_url} (il sito è aggiornato?)")
    if a.dry_run:
        print("Dry run riuscito: token valido, immagine raggiungibile. Non pubblico.")
        return

    c = call("POST", f"{uid}/media", token, {"image_url": image_url, "caption": p["didascalia"],
                                            "alt_text": p.get("alt", "")})
    cid = c["id"]
    for _ in range(20):
        st = call("GET", cid, token, {"fields": "status_code"}).get("status_code")
        if st == "FINISHED":
            break
        if st in ("ERROR", "EXPIRED"):
            sys.exit(f"Container {cid} in stato {st}")
        time.sleep(3)
    else:
        sys.exit(f"Container {cid} non pronto in tempo")
    media = call("POST", f"{uid}/media_publish", token, {"creation_id": cid})["id"]
    link = call("GET", media, token, {"fields": "permalink"}).get("permalink", "")
    state["pubblicati"][p["id"]] = {"stato": "pubblicato", "media_id": media, "link": link,
                                    "ora_utc": now.isoformat(timespec="seconds")}
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Pubblicato: {link}")


if __name__ == "__main__":
    main()
