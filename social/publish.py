#!/usr/bin/env python3
"""Pubblica su Instagram e sulla Pagina Facebook i post di social/calendar.json.

Solo libreria standard. I token arrivano da variabili d'ambiente (Secret di GitHub,
mai nel repo):
  IG_ACCESS_TOKEN   token Instagram (API con Instagram Login). L'ID account si ricava con /me.
  FB_PAGE_TOKEN     token della Pagina Facebook (facoltativo: senza, si pubblica solo su Instagram)
  FB_PAGE_ID        ID della Pagina Facebook (obbligatorio se c'è FB_PAGE_TOKEN)

Uso:
  publish.py                 pubblica al massimo 1 post scaduto per piattaforma
  publish.py --dry-run       controlla token, immagine e didascalia senza pubblicare
  publish.py --id 03-...     forza un post preciso (test), ignorando data e finestra
"""
import argparse, json, os, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
IG_API = "https://graph.instagram.com/v23.0"
FB_API = "https://graph.facebook.com/v23.0"
SITE = "https://libri.diasio.ch"
CAL, STATE = ROOT / "calendar.json", ROOT / "published.json"


class ApiError(Exception):
    pass


def call(base, method, path, token, params=None):
    params = dict(params or {})
    params["access_token"] = token
    data = urllib.parse.urlencode(params).encode()
    url = f"{base}/{path}"
    req = urllib.request.Request(url + ("?" + data.decode() if method == "GET" else ""),
                                 data=None if method == "GET" else data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise ApiError(f"{method} {path}: HTTP {e.code} {e.read().decode('utf-8', 'replace')}")


def image_ok(url):
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status == 200 and "image/jpeg" in r.headers.get("Content-Type", "")
    except Exception:
        return False


def platforms():
    out = []
    if os.environ.get("IG_ACCESS_TOKEN", "").strip():
        out.append("instagram")
    if os.environ.get("FB_PAGE_TOKEN", "").strip() and os.environ.get("FB_PAGE_ID", "").strip():
        out.append("facebook")
    return out


def entry(state, pid):
    return state["pubblicati"].setdefault(pid, {})


def pending(post, state, plats):
    done = state["pubblicati"].get(post["id"], {})
    if done.get("saltato"):
        return []
    return [p for p in plats if p not in done]


def pick(cal, state, plats, now, forced):
    """Primo post con almeno una piattaforma da fare. Segna come saltati quelli troppo in ritardo."""
    if forced:
        p = next((x for x in cal["post"] if x["id"] == forced), None)
        return p, plats
    tz = ZoneInfo(cal.get("fuso", "Europe/Rome"))
    late = timedelta(hours=cal.get("max_ritardo_ore", 12))
    for p in cal["post"]:
        todo = pending(p, state, plats)
        if not todo:
            continue
        when = datetime.fromisoformat(p["quando"]).replace(tzinfo=tz)
        if when > now:
            continue
        if now - when > late:
            entry(state, p["id"])["saltato"] = "oltre la finestra di ritardo"
            print(f"Saltato {p['id']}: programmato {p['quando']}, troppo in ritardo.")
            continue
        return p, todo
    return None, []


def publish_instagram(p, image_url, token):
    me = call(IG_API, "GET", "me", token, {"fields": "user_id,username"})
    uid = me.get("user_id") or me.get("id")
    c = call(IG_API, "POST", f"{uid}/media", token,
             {"image_url": image_url, "caption": p["didascalia"], "alt_text": p.get("alt", "")})
    cid = c["id"]
    for _ in range(20):
        st = call(IG_API, "GET", cid, token, {"fields": "status_code"}).get("status_code")
        if st == "FINISHED":
            break
        if st in ("ERROR", "EXPIRED"):
            raise ApiError(f"container {cid} in stato {st}")
        time.sleep(3)
    else:
        raise ApiError(f"container {cid} non pronto in tempo")
    media = call(IG_API, "POST", f"{uid}/media_publish", token, {"creation_id": cid})["id"]
    link = call(IG_API, "GET", media, token, {"fields": "permalink"}).get("permalink", "")
    return {"media_id": media, "link": link}


def publish_facebook(p, image_url, token, page_id):
    r = call(FB_API, "POST", f"{page_id}/photos", token,
             {"url": image_url, "caption": p.get("didascalia_fb") or p["didascalia"],
              "alt_text_custom": p.get("alt", ""), "published": "true"})
    post_id = r.get("post_id") or r.get("id")
    return {"post_id": post_id, "link": f"https://www.facebook.com/{post_id}"}


def check_tokens(plats):
    if "instagram" in plats:
        me = call(IG_API, "GET", "me", os.environ["IG_ACCESS_TOKEN"], {"fields": "user_id,username"})
        print(f"Instagram: account @{me.get('username')}")
    if "facebook" in plats:
        pg = call(FB_API, "GET", os.environ["FB_PAGE_ID"], os.environ["FB_PAGE_TOKEN"], {"fields": "name"})
        print(f"Facebook: Pagina «{pg.get('name')}»")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--id")
    a = ap.parse_args()

    plats = platforms()
    if not plats:
        sys.exit("Nessun token: servono IG_ACCESS_TOKEN e/o FB_PAGE_TOKEN + FB_PAGE_ID (Secret, sezione Actions).")
    cal = json.loads(CAL.read_text(encoding="utf-8"))
    state = json.loads(STATE.read_text(encoding="utf-8"))
    if cal.get("pausa") and not a.id:
        print("Calendario in pausa (pausa: true). Nessuna pubblicazione.")
        return

    print("Piattaforme attive:", ", ".join(plats))
    errors = []
    try:
        check_tokens(plats)
    except ApiError as e:
        sys.exit(f"Errore token: {e}")

    now = datetime.now(timezone.utc)
    p, todo = pick(cal, state, plats, now, a.id)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    if not p:
        print("Nessun post da pubblicare adesso.")
        return
    image_url = f"{SITE}/{p['immagine']}"
    print(f"Post: {p['id']} ({p['segmento']}) su {', '.join(todo)} → {image_url}")
    if not image_ok(image_url):
        sys.exit(f"Immagine non raggiungibile o non JPEG: {image_url} (il sito è aggiornato?)")
    if a.dry_run:
        print("Dry run riuscito: token validi, immagine raggiungibile. Non pubblico.")
        return

    for plat in todo:
        try:
            if plat == "instagram":
                res = publish_instagram(p, image_url, os.environ["IG_ACCESS_TOKEN"])
            else:
                res = publish_facebook(p, image_url, os.environ["FB_PAGE_TOKEN"], os.environ["FB_PAGE_ID"])
            res["ora_utc"] = now.isoformat(timespec="seconds")
            entry(state, p["id"])[plat] = res
            print(f"Pubblicato su {plat}: {res['link']}")
        except ApiError as e:
            errors.append(f"{plat}: {e}")
            print(f"::error::Errore su {plat}: {e}")
        STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
