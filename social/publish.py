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

Tipi di post in calendar.json: immagine (campo "immagine"), "tipo": "reel" (campo "video"),
"tipo": "carosello" (campo "immagini": da 2 a 10 file JPEG).
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


def media_ok(url, content_type):
    """True se l'URL risponde 200 con un Content-Type che contiene `content_type`
    (es. "image/jpeg" per le immagini, "video/" per i Reel)."""
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status == 200 and content_type in r.headers.get("Content-Type", "")
    except Exception:
        return False


def fb_token():
    """FB_PAGE_TOKEN può essere un token di Pagina o un token utente a lunga durata:
    nel secondo caso ricava il token della Pagina (che serve per pubblicare)."""
    tok, page = os.environ["FB_PAGE_TOKEN"], os.environ["FB_PAGE_ID"]
    try:
        r = call(FB_API, "GET", page, tok, {"fields": "access_token"})
        return r.get("access_token") or tok
    except ApiError:
        return tok


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
    for p in sorted(cal["post"], key=lambda x: x["quando"]):
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


def is_reel(p):
    return p.get("tipo") == "reel"


def is_carousel(p):
    return p.get("tipo") == "carosello"


def media_urls(p):
    """URL pubblici dei file del post (uno solo, tranne nei caroselli)."""
    if is_reel(p):
        return [f"{SITE}/{p['video']}"]
    if is_carousel(p):
        return [f"{SITE}/{x}" for x in p["immagini"]]
    return [f"{SITE}/{p['immagine']}"]


def wait_container(cid, token, tries, wait):
    for _ in range(tries):
        st = call(IG_API, "GET", cid, token, {"fields": "status_code"}).get("status_code")
        if st == "FINISHED":
            return
        if st in ("ERROR", "EXPIRED"):
            raise ApiError(f"container {cid} in stato {st}")
        time.sleep(wait)
    raise ApiError(f"container {cid} non pronto in tempo")


def publish_instagram(p, media_url, token):
    me = call(IG_API, "GET", "me", token, {"fields": "user_id,username"})
    uid = me.get("user_id") or me.get("id")
    if is_carousel(p):
        # un contenitore per slide, poi un contenitore CAROUSEL che le raccoglie (2-10 slide)
        kids = []
        for url in media_url:
            k = call(IG_API, "POST", f"{uid}/media", token, {"image_url": url, "is_carousel_item": "true"})["id"]
            wait_container(k, token, 20, 3)
            kids.append(k)
        params = {"media_type": "CAROUSEL", "children": ",".join(kids), "caption": p["didascalia"]}
        cid = call(IG_API, "POST", f"{uid}/media", token, params)["id"]
        wait_container(cid, token, 20, 3)
        media = call(IG_API, "POST", f"{uid}/media_publish", token, {"creation_id": cid})["id"]
        link = call(IG_API, "GET", media, token, {"fields": "permalink"}).get("permalink", "")
        return {"media_id": media, "link": link}
    if is_reel(p):
        params = {"media_type": "REELS", "video_url": media_url, "caption": p["didascalia"], "share_to_feed": "true"}
        if p.get("miniatura_ms") is not None:      # fotogramma usato come miniatura (millisecondi)
            params["thumb_offset"] = str(int(p["miniatura_ms"]))
        tries, wait = 60, 5          # i video richiedono più tempo di elaborazione
    else:
        params = {"image_url": media_url, "caption": p["didascalia"], "alt_text": p.get("alt", "")}
        tries, wait = 20, 3
    c = call(IG_API, "POST", f"{uid}/media", token, params)
    cid = c["id"]
    wait_container(cid, token, tries, wait)
    media = call(IG_API, "POST", f"{uid}/media_publish", token, {"creation_id": cid})["id"]
    link = call(IG_API, "GET", media, token, {"fields": "permalink"}).get("permalink", "")
    return {"media_id": media, "link": link}


def publish_facebook(p, media_url, token, page_id):
    text = p.get("didascalia_fb") or p["didascalia"]
    if is_carousel(p):
        # Facebook: le foto vengono caricate non pubblicate e poi allegate a un solo post di Pagina
        ids = [call(FB_API, "POST", f"{page_id}/photos", token, {"url": url, "published": "false"})["id"] for url in media_url]
        r = call(FB_API, "POST", f"{page_id}/feed", token,
                 {"message": text, "attached_media": json.dumps([{"media_fbid": i} for i in ids])})
        post_id = r.get("id")
        return {"post_id": post_id, "link": f"https://www.facebook.com/{post_id}"}
    media_url = media_url[0] if isinstance(media_url, list) else media_url
    if is_reel(p):
        # su Facebook ogni video pubblicato in Pagina è un Reel
        r = call(FB_API, "POST", f"{page_id}/videos", token,
                 {"file_url": media_url, "description": text, "published": "true"})
    else:
        r = call(FB_API, "POST", f"{page_id}/photos", token,
                 {"url": media_url, "caption": text, "alt_text_custom": p.get("alt", ""), "published": "true"})
    post_id = r.get("post_id") or r.get("id")
    return {"post_id": post_id, "link": f"https://www.facebook.com/{post_id}"}


def check_tokens(plats):
    if "instagram" in plats:
        me = call(IG_API, "GET", "me", os.environ["IG_ACCESS_TOKEN"], {"fields": "user_id,username"})
        print(f"Instagram: account @{me.get('username')}")
    if "facebook" in plats:
        pg = call(FB_API, "GET", os.environ["FB_PAGE_ID"], os.environ["FB_PAGE_TOKEN"], {"fields": "name"})
        print(f"Facebook: Pagina «{pg.get('name')}»")
        try:
            eff = fb_token()
            dbg = call(FB_API, "GET", "debug_token", eff, {"input_token": eff}).get("data", {})
            src = call(FB_API, "GET", "debug_token", os.environ["FB_PAGE_TOKEN"],
                       {"input_token": os.environ["FB_PAGE_TOKEN"]}).get("data", {})
            se = src.get("expires_at", 0)
            print(f"Facebook: token salvato di tipo {src.get('type', '?')}, "
                  + ("non scade" if not se else "scade il " + datetime.fromtimestamp(se, timezone.utc).strftime("%Y-%m-%d")))
            print(f"Facebook: permessi {', '.join(dbg.get('scopes', []))}")
            exp = dbg.get("expires_at", 0)
            when = "non scade" if not exp else "scade il " + datetime.fromtimestamp(exp, timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            print(f"Facebook: token {dbg.get('type', '?')}, valido={dbg.get('is_valid')}, {when}")
            if exp:
                print("::warning::Il token effettivo della Pagina ha una scadenza.")
        except ApiError as e:
            print(f"Facebook: scadenza non verificabile ({str(e)[:120]})")


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
    kind = "reel" if is_reel(p) else "carosello" if is_carousel(p) else "immagine"
    urls = media_urls(p)
    print(f"Post: {p['id']} ({kind}, {p['segmento']}) su {', '.join(todo)} → {', '.join(urls)}")
    if is_carousel(p) and not 2 <= len(urls) <= 10:
        sys.exit(f"Un carosello ha da 2 a 10 slide: {p['id']} ne ha {len(urls)}.")
    for u in urls:
        if not media_ok(u, "video/" if is_reel(p) else "image/jpeg"):
            sys.exit(f"File non raggiungibile o di tipo sbagliato: {u} (il sito è aggiornato?)")
    if a.dry_run:
        print("Dry run riuscito: token validi, file raggiungibile. Non pubblico.")
        return

    for plat in todo:
        try:
            if plat == "instagram":
                res = publish_instagram(p, urls if is_carousel(p) else urls[0], os.environ["IG_ACCESS_TOKEN"])
            else:
                res = publish_facebook(p, urls if is_carousel(p) else urls[0], fb_token(), os.environ["FB_PAGE_ID"])
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
