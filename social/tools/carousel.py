"""Genera le slide 1080x1350 dei caroselli e delle grafiche di dicembre da tools/carousels.py.

Stesso stile dei Reel: fondo blu notte, alone ambra, Oswald + Source Serif (font in reels-src/assets/fonts).
Serve Python 3, `pip install playwright` e Chromium (`playwright install chromium`, oppure CHROMIUM_PATH=/percorso/chrome).
Uso, dalla cartella social/tools:
  python carousel.py            # rende tutte le slide in ../img/carousel/<id>/NN.jpg e ../img/<id>.jpg
  python carousel.py c01-...    # solo quel carosello / grafica
  python carousel.py --calendar # aggiunge (senza duplicare) le voci a ../calendar.json
"""
import base64, html, json, os, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOCIAL = HERE.parent
FONTS = SOCIAL / "reels-src" / "assets" / "fonts"
COVERS = {"bug": SOCIAL / "reels-src/assets/img/cover-bug.jpg", "oblio": SOCIAL / "reels-src/assets/img/cover-oblio.jpg"}
TITLES = {"bug": "Il Bug della Trasparenza", "oblio": "L’Economia dell’Oblio"}
GENRES = {"bug": "Noir sociale · 8 puntate", "oblio": "Thriller psicologico · 6 puntate"}


def b64(p, mime):
    return f"data:{mime};base64," + base64.b64encode(Path(p).read_bytes()).decode()


def hero_src(book):
    """Copertina ad alta risoluzione (1200x1789) letta dall'EPUB della Puntata 1."""
    import zipfile
    name = {"bug": "il-bug-della-trasparenza-puntata-1.epub", "oblio": "leconomia-delloblio-puntata-1.epub"}[book]
    z = zipfile.ZipFile(SOCIAL.parent / "download" / name)
    return "data:image/jpeg;base64," + base64.b64encode(z.read("EPUB/images/cover.jpg")).decode()


def fontface():
    d = {"Oswald": [(500, "Oswald-500.woff2", "normal"), (700, "Oswald-700.woff2", "normal")],
         "Source Serif 4": [(400, "SourceSerif4-400.woff2", "normal"), (400, "SourceSerif4-400i.woff2", "italic"), (600, "SourceSerif4-600.woff2", "normal")]}
    out = []
    for fam, items in d.items():
        for w, f, st in items:
            out.append(f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{st};src:url({b64(FONTS / f, 'font/woff2')}) format('woff2')}}")
    return "\n".join(out)


CSS = """
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0a0f18;--ink:#eef1f5;--mut:#a7b2c2;--line:#22324a;--amb:#f0a24a;--dark:#1a1206}
body{width:1080px;height:1350px;background:var(--bg);color:var(--ink);font-family:'Source Serif 4',serif;position:relative;overflow:hidden}
.glow{position:absolute;left:380px;top:-260px;width:920px;height:880px;border-radius:50%;background:#2e2010;filter:blur(160px)}
.amber{background:var(--amb);color:var(--dark)}.amber .glow{left:-300px;top:700px;width:1000px;height:1000px;background:#e2923a;filter:blur(140px)}
.brand{position:absolute;left:70px;top:70px;font:700 40px 'Oswald';letter-spacing:.16em}
.brand i{font-style:normal;color:var(--amb)}.amber .brand i{color:var(--dark)}
.rule{position:absolute;left:70px;top:150px;width:80px;height:5px;background:var(--amb)}.amber .rule{background:var(--dark)}
.pg{position:absolute;right:70px;top:82px;font:500 26px 'Oswald';letter-spacing:.14em;color:var(--mut)}.amber .pg{color:#5a3a0c}
.swipe{position:absolute;right:70px;bottom:92px;font:500 28px 'Oswald';letter-spacing:.18em;color:var(--amb)}.amber .swipe{color:var(--dark)}
.main{position:absolute;left:70px;right:70px;top:230px;bottom:290px;display:flex;flex-direction:column;justify-content:center}
.kick{font:500 30px 'Oswald';letter-spacing:.22em;text-transform:uppercase;color:var(--amb);margin-bottom:34px}.amber .kick{color:var(--dark)}
.big{font:700 122px/1.02 'Oswald';text-transform:uppercase;letter-spacing:.005em}
.big b{color:var(--amb);font-weight:700}.amber .big b{color:var(--dark);opacity:.72}
.q{font:italic 400 80px/1.28 'Source Serif 4'}.q.m{font-size:68px}.q.s{font-size:58px}
.q b,.sub b{color:var(--amb);font-weight:400}.amber .q b{color:var(--dark);font-weight:600}
.who{margin-top:38px;font:500 28px 'Oswald';letter-spacing:.2em;text-transform:uppercase;color:var(--mut)}.amber .who{color:#5a3a0c}
.who:before{content:"";display:inline-block;width:46px;height:3px;background:var(--amb);vertical-align:middle;margin-right:18px}.amber .who:before{background:var(--dark)}
.sub{margin-top:40px;font:400 40px/1.4 'Source Serif 4';color:var(--mut)}.amber .sub{color:#4a2f08}
.num{font:700 190px/1 'Oswald';color:var(--amb)}
.stitle{font:700 84px/1.08 'Oswald';text-transform:uppercase;margin-top:6px}
.stext{font:400 46px/1.42 'Source Serif 4';color:var(--mut);margin-top:34px}.stext b{color:var(--ink);font-weight:600}
.rows{margin-top:44px}.row{display:flex;align-items:baseline;font:400 50px/1 'Source Serif 4';padding:30px 0;border-bottom:2px dashed var(--line)}
.row span:first-child{flex:1}.row span:last-child{font:700 54px 'Oswald';color:var(--amb)}
.rtitle{font:700 58px/1.1 'Oswald';letter-spacing:.06em}.rsub{font:500 30px 'Oswald';letter-spacing:.24em;color:var(--mut);margin-top:12px}
.main.tight{top:215px;bottom:250px;justify-content:flex-start}.tight .rows{margin-top:26px}.tight .row{padding:20px 0;font-size:46px}.tight .row span:last-child{font-size:48px}.tight .note{margin-top:30px;font-size:40px}
.note{margin-top:44px;font:italic 400 44px/1.35 'Source Serif 4';color:var(--mut)}
.foot{position:absolute;left:70px;bottom:70px;display:flex;align-items:center;gap:28px}
.foot img{width:96px;height:143px;border:2px solid var(--line);object-fit:cover}.amber .foot img{border-color:var(--dark)}
.foot .t{font:700 30px 'Oswald';letter-spacing:.04em;text-transform:uppercase}.foot .u{font:400 28px 'Source Serif 4';color:var(--amb);margin-top:12px}
.foot .h{font:400 24px 'Source Serif 4';color:var(--mut);margin-top:14px}.amber .foot .u,.amber .foot .h{color:var(--dark)}
.covers{display:flex;gap:56px;justify-content:center;margin-top:10px}.cv{width:420px;text-align:center}
.cv img{width:420px;height:626px;object-fit:cover;box-shadow:0 30px 60px rgba(0,0,0,.55);border:2px solid var(--line)}
.cv .t{font:700 34px 'Oswald';text-transform:uppercase;margin-top:30px}.cv .g{font:500 22px 'Oswald';white-space:nowrap;letter-spacing:.1em;text-transform:uppercase;color:var(--amb);margin-top:10px}
.cv .p{font:italic 400 34px/1.32 'Source Serif 4';color:var(--ink);margin-top:20px}.cv .p b{color:var(--amb);font-weight:400}
.one{display:flex;justify-content:center}.one img{width:460px;height:686px;object-fit:cover;box-shadow:0 30px 60px rgba(0,0,0,.55);border:2px solid var(--line)}
.btn{position:absolute;left:70px;right:70px;bottom:160px;text-align:center;background:var(--amb);color:var(--dark);font:700 50px 'Oswald';letter-spacing:.06em;text-transform:uppercase;padding:34px 0;box-shadow:0 0 60px rgba(240,162,74,.45)}
.btnsub{position:absolute;left:70px;right:70px;bottom:92px;text-align:center;font:400 30px 'Source Serif 4';color:var(--mut)}.btnsub b{color:var(--ink);font-weight:600}
.hero{position:absolute;left:0;top:0;width:1080px;height:640px;background-repeat:no-repeat;background-size:1080px auto}
.hero:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,15,24,.55) 0%,rgba(10,15,24,0) 24%,rgba(10,15,24,0) 52%,rgba(10,15,24,.78) 82%,var(--bg) 100%)}
.hq .brand,.hq .pg{z-index:3;text-shadow:0 2px 14px rgba(0,0,0,.85)}.hq .pg{background:rgba(10,15,24,.6);padding:6px 16px;border-radius:999px;top:76px;color:#d7dde6}.hq .rule{z-index:3}
.hq .main{top:610px;bottom:300px;justify-content:flex-start}
.hq .q{font-size:74px}.hq .q.l{font-size:96px;line-height:1.22}.hq .q.m{font-size:64px}.hq .q.s{font-size:56px}
.hq .big{font-size:96px}.hq .kick{margin-bottom:22px}.hq .sub{margin-top:26px;font-size:38px}
.hq .who{margin-top:30px}
body.story{height:1920px}
.story .brand{top:290px}.story .rule{top:370px}.story .pg,.story .swipe{display:none}
.story .main{top:470px;bottom:520px}.story .q{font-size:88px}.story .q.m{font-size:76px}.story .q.s{font-size:64px}
.story .big{font-size:132px}.story .sub{font-size:44px}.story .foot{bottom:250px}
.story .btn{bottom:400px}.story .btnsub{bottom:320px}.story .tagline{top:400px}
.story .cv{width:420px}.story .covers,.story .one{margin-top:0}
.tagline{position:absolute;left:70px;right:70px;top:190px;text-align:center;font:italic 400 44px/1.3 'Source Serif 4'}.tagline b{color:var(--amb);font-weight:400}

.photo{position:absolute;inset:0;background-size:cover;background-repeat:no-repeat}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,15,24,.62) 0%,rgba(10,15,24,0) 20%,rgba(10,15,24,0) 38%,rgba(10,15,24,.80) 66%,rgba(10,15,24,.97) 100%)}
.pq{position:absolute;left:70px;right:70px;bottom:290px;text-shadow:0 2px 24px rgba(0,0,0,.7)}
.pq .q{font-size:62px;line-height:1.26}.pq .q.s{font-size:54px}.pq .q.l{font-size:74px}
.pq .who{margin-top:30px;color:#c9d2de}
.pho .brand,.pho .pg,.pho .rule{z-index:3;text-shadow:0 2px 14px rgba(0,0,0,.85)}
.kb{position:absolute;left:70px;right:70px;bottom:70px;height:118px;background:var(--amb);color:var(--dark);display:flex;align-items:center;justify-content:space-between;padding:0 40px;box-shadow:0 0 60px rgba(240,162,74,.28)}
.kb span{font:700 46px 'Oswald';letter-spacing:.08em;text-transform:uppercase}.kb i{font:500 28px 'Oswald';font-style:normal;letter-spacing:.14em;color:#5a3a0c}
.kd .main{bottom:250px}.kd .pq{bottom:250px}
.notif{display:flex;gap:34px;align-items:flex-start;background:rgba(30,42,62,.97);border:2px solid var(--line);border-radius:48px;padding:48px;box-shadow:0 40px 90px rgba(0,0,0,.6);margin-top:8px}
.ni{flex:none;width:128px;height:128px;border-radius:32px;background:#bfd8ee;display:flex;align-items:center;justify-content:center}
.app{font:500 25px 'Oswald';letter-spacing:.2em;color:var(--mut);text-transform:uppercase}
.nh{font:700 46px/1.15 'Oswald';margin-top:12px}.nb{font:400 46px/1.36 'Source Serif 4';margin-top:14px;color:#dbe2ec}
.nsub{margin-top:36px;font:italic 400 38px/1.4 'Source Serif 4';color:var(--mut)}
.tab{font:500 28px 'DejaVu Sans Mono',monospace;color:var(--amb);letter-spacing:.04em;margin-bottom:22px}
.doc{background:#0d1522;border:2px solid var(--line);border-radius:18px;padding:44px 48px}
.doc p{font:400 33px/1.5 'DejaVu Sans Mono',monospace;color:#d6dde8;margin-bottom:26px}.doc p:last-child{margin-bottom:0}.doc b{color:var(--amb);font-weight:400}
"""


def em(s):
    """*parola* → parola in evidenza (ambra)."""
    return re.sub(r"\*(.+?)\*", r"<b>\1</b>", html.escape(s, quote=False)).replace("\n", "<br>")


def cover_img(book):
    return b64(COVERS[book], "image/jpeg")


def foot(book):
    return (f'<div class="foot"><img src="{cover_img(book)}"><div><div class="t">{TITLES[book]}</div>'
            f'<div class="u">Puntata 1 gratis · libri.diasio.ch</div><div class="h">@d.iasio.libri</div></div></div>')


def photo_src(rel, pos=30):
    """Foto 4:5 (1080x1350) ritagliata da una scena verticale in social/img/scene: pos = % dello scarto verticale."""
    import io
    from PIL import Image, ImageFilter
    im = Image.open(SOCIAL / "img" / "scene" / rel).convert("RGB")
    h = round(im.height * 1080 / im.width)
    im = im.resize((1080, h), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.4, percent=55, threshold=2))
    top = round(max(0, h - 1350) * pos / 100)
    im = im.crop((0, top, 1080, top + 1350))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def kband(text="Ora su Amazon Kindle"):
    return f'<div class="kb"><span>{html.escape(text)}</span><i>libri.diasio.ch</i></div>'


M_ICON = ('<svg width="84" height="84" viewBox="0 0 96 96"><polyline points="20,70 20,30 48,58 76,30 76,70" fill="none" '
          'stroke="#f3f8fc" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def slide_html(s, i, n, book, theme, story=False):
    k = s["k"]
    pg = f'<div class="pg">{i} / {n}</div>' if n > 1 else ""
    swipe = '<div class="swipe">SCORRI →</div>' if n > 1 and i < n else ""
    head = '<div class="brand">D<i>.</i> IASIO</div><div class="rule"></div>' + pg
    body, foo, pre = "", foot(book), ""
    if s.get("kindle"):
        foo = kband(s["kindle"] if isinstance(s["kindle"], str) else "Ora su Amazon Kindle")
    if s.get("hero") is not None:
        hy, hz, hx = (s["hero"] if isinstance(s["hero"], (tuple, list)) else (s["hero"], 1.0, 0))
        head += (f'<div class="hero" style="background-image:url({hero_src(book)});background-size:{int(1080 * hz)}px auto;'
                 f'background-position:-{int(hx)}px -{int(hy)}px"></div>')
    if k == "hook":
        kick = f'<div class="kick">{html.escape(s["kick"])}</div>' if s.get("kick") else ""
        sub = f'<div class="sub">{em(s["sub"])}</div>' if s.get("sub") else ""
        body = f'<div class="main">{kick}<div class="big">{em(s["text"])}</div>{sub}</div>'
    elif k == "quote":
        size = ("l" if s.get("hero") is not None else "") if len(s["text"]) < 60 else "" if len(s["text"]) < 70 else "m" if len(s["text"]) < 120 else "s"
        who = f'<div class="who">{html.escape(s.get("who") or TITLES[book] + " · Puntata 1")}</div>'
        txt = s["text"] if s["text"].startswith("«") else "“" + s["text"] + "”"
        body = f'<div class="main"><div class="q {size}">{em(txt)}</div>{who}</div>'
    elif k == "rows":
        rows = "".join(f'<div class="row"><span>{html.escape(a)}</span><span>{html.escape(b)}</span></div>' for a, b in s["rows"])
        note = f'<div class="note">{html.escape(s["note"])}</div>' if s.get("note") else ""
        tight = " tight" if len(s["rows"]) > 4 else ""
        body = f'<div class="main{tight}"><div class="rtitle">{html.escape(s["title"])}</div><div class="rsub">{html.escape(s["sub"])}</div><div class="rows">{rows}</div>{note}</div>'
    elif k == "step":
        kick = f'<div class="kick">{html.escape(s["kick"])}</div>' if s.get("kick") else ""
        body = f'<div class="main">{kick}<div class="num">{s["n"]}</div><div class="stitle">{em(s["title"])}</div><div class="stext">{em(s["text"])}</div></div>'
    elif k == "photo":
        pre = (f'<div class="photo" style="background-image:url({photo_src(s["photo"], s.get("pos", 30))});'
               f'background-position:center"></div><div class="shade"></div>')
        size = "l" if len(s["text"]) < 50 else "s" if len(s["text"]) > 150 else ""
        who = f'<div class="who">{html.escape(s["who"])}</div>' if s.get("who") else ""
        txt = s["text"] if s["text"].startswith("«") else "“" + s["text"] + "”"
        body = f'<div class="pq"><div class="q {size}">{em(txt)}</div>{who}</div>'
    elif k == "notif":
        kick = f'<div class="kick">{html.escape(s["kick"])}</div>' if s.get("kick") else ""
        sub = f'<div class="nsub">{em(s["sub"])}</div>' if s.get("sub") else ""
        body = (f'<div class="main">{kick}<div class="notif"><div class="ni">{M_ICON}</div><div>'
                f'<div class="app">{html.escape(s.get("app", "Meridiana Life"))} · {html.escape(s.get("when", "adesso"))}</div>'
                f'<div class="nh">{html.escape(s["title"])}</div><div class="nb">{em(s["text"])}</div></div></div>{sub}</div>')
    elif k == "doc":
        kick = f'<div class="kick">{html.escape(s["kick"])}</div>' if s.get("kick") else ""
        lines = "".join(f'<p>{em(x)}</p>' for x in s["lines"])
        body = f'<div class="main">{kick}<div class="tab">{html.escape(s["name"])}</div><div class="doc">{lines}</div></div>'
    elif k == "covers":
        cs = "".join(f'<div class="cv"><img src="{cover_img(b)}"><div class="t">{TITLES[b]}</div><div class="g">{GENRES[b]}</div><div class="p">{em(p)}</div></div>'
                     for b, p in s["items"])
        tag = f'<div class="tagline">{em(s["text"])}</div>' if s.get("text") else ""
        body = f'{tag}<div class="main" style="top:300px;bottom:150px;justify-content:flex-start"><div class="covers">{cs}</div></div>'
        foo = ""
    elif k == "cta":
        books = s.get("books") or [book]
        imgs = "".join(f'<img src="{cover_img(b)}">' for b in books)
        tag = f'<div class="tagline">{em(s["text"])}</div>' if s.get("text") else ""
        body = (f'{tag}<div class="main" style="top:280px;bottom:330px;justify-content:center"><div class="one" style="gap:40px">{imgs}</div></div>'
                f'<div class="btn">{html.escape(s.get("button", "Leggi la Puntata 1 gratis"))}</div>'
                f'<div class="btnsub">{s.get("line", "PDF ed EPUB · <b>libri.diasio.ch</b>")}</div>')
        foo = ""
        if len(books) == 2:
            body = body.replace('width:460px', 'width:400px')
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{fontface()}{CSS}</style></head>'
            f'<body class="{"amber" if theme == "amber" else ""}{" story" if story else ""}{" hq" if s.get("hero") is not None else ""}{" pho" if k == "photo" else ""}{" kd" if s.get("kindle") else ""}"><div class="glow"></div>{pre}{head}{body}{foo}{swipe}</body></html>')


def load():
    ns = {}
    exec((HERE / "carousels.py").read_text(encoding="utf-8"), ns)
    items = list(ns["ITEMS"])
    extra = HERE / "nuovi_ottobre.py"          # due uscite al giorno (ottobre 2026): file in img/nuovi/
    if extra.exists():
        ns2 = {"__file__": str(extra)}
        exec(extra.read_text(encoding="utf-8"), ns2)
        items += ns2["ITEMS"]
    return items


def out_path(it, i, n):
    """Cartella e nome del file di una slide. Gli item con flat=True stanno tutti in img/nuovi/."""
    if it.get("flat"):
        d = SOCIAL / "img" / "nuovi"
        return d, (f"{it['id']}-{i:02d}.jpg" if n > 1 else f"{it['id']}.jpg")
    story = bool(it.get("story"))
    d = SOCIAL / "img" / "story" if story else SOCIAL / "img" / "carousel" / it["id"] if n > 1 else SOCIAL / "img"
    return d, (f"{i:02d}.jpg" if n > 1 and not story else f"{it['id']}.jpg")


def render(items, only=None):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH") or None)
        for it in items:
            if only and it["id"] != only:
                continue
            story = bool(it.get("story"))
            pg = br.new_page(viewport={"width": 1080, "height": 1920 if story else 1350})
            slides = it["slides"]
            n = len(slides)
            for i, s in enumerate(slides, 1):
                outdir, fname = out_path(it, i, n)
                outdir.mkdir(parents=True, exist_ok=True)
                pg.set_content(slide_html(s, i, n, s.get("book", it["book"]), it.get("theme"), story))
                pg.wait_for_timeout(150)
                out = outdir / fname
                pg.screenshot(path=str(out), type="jpeg", quality=92)
                print("→", out.relative_to(SOCIAL))
            pg.close()
        br.close()


def fb_caption(cap, tags):
    cap = re.sub(r"link in bio\.?", "https://libri.diasio.ch/", cap, flags=re.I)
    return cap.replace("\n" + tags, "") + "\n\n" + " ".join(tags.split()[:3])


def add_calendar(items):
    p = SOCIAL / "calendar.json"
    cal = json.loads(p.read_text(encoding="utf-8"))
    have = {x["id"] for x in cal["post"]}
    for it in items:
        if it["id"] in have:
            continue
        n = len(it["slides"])
        if it.get("flat"):
            e = {"id": it["id"], "quando": it["when"], "segmento": it["seg"]}
            if n > 1:
                e["tipo"] = "carosello"
                e["immagini"] = [f"social/img/nuovi/{it['id']}-{i:02d}.jpg" for i in range(1, n + 1)]
            else:
                e["immagine"] = f"social/img/nuovi/{it['id']}.jpg"
            e.update({"alt": it["alt"], "didascalia": it["caption"], "didascalia_fb": it["caption_fb"]})
            cal["post"].append(e)
            print("+", it["id"], it["when"])
            continue
        if it.get("story"):
            cal["post"].append({"id": it["id"], "tipo": "storia", "quando": it["when"], "segmento": it["seg"],
                                "immagine": f"social/img/story/{it['id']}.jpg"})
            print("+", it["id"], it["when"])
            continue
        e = {"id": it["id"], "quando": it["when"], "segmento": it["seg"]}
        if n > 1:
            e["tipo"] = "carosello"
            e["immagini"] = [f"social/img/carousel/{it['id']}/{i:02d}.jpg" for i in range(1, n + 1)]
        else:
            e["immagine"] = f"social/img/{it['id']}.jpg"
        cap = it["caption"] + "\n" + it["tags"]
        e.update({"alt": it["alt"], "didascalia": cap, "didascalia_fb": it.get("caption_fb") or fb_caption(cap, it["tags"])})
        cal["post"].append(e)
        print("+", it["id"], it["when"])
    cal["post"].sort(key=lambda x: x["quando"])
    p.write_text(json.dumps(cal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    items = load()
    if "--calendar" in sys.argv:
        add_calendar(items)
    else:
        render(items, next((a for a in sys.argv[1:] if not a.startswith("-")), None))
