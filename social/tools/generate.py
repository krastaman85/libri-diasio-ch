# Genera le grafiche 1080x1350 per Instagram/Facebook da posts.py
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, ".")
from posts import POSTS

W, H = 1080, 1350
BG, PANEL, INK, MUTED, LINE, AMBER = (10,15,24), (17,26,40), (238,241,245), (167,178,194), (34,50,74), (240,162,74)
DARK, DMUT = (26,18,6), (86,56,14)
FD = "C:/Windows/Fonts/"
head = lambda s: ImageFont.truetype(FD+"arialnb.ttf", s)
serif = lambda s: ImageFont.truetype(FD+"georgiai.ttf", s)
serifr = lambda s: ImageFont.truetype(FD+"georgia.ttf", s)
mono = lambda s: ImageFont.truetype(FD+"consola.ttf", s)
monob = lambda s: ImageFont.truetype(FD+"consolab.ttf", s)
COVERS = {"bug": "../../img/cover-bug.jpg", "oblio": "../../img/cover-oblio.jpg"}
TITLES = {"bug": "IL BUG DELLA TRASPARENZA", "oblio": "L’ECONOMIA DELL’OBLIO"}


def wrap(d, text, font, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def canvas(theme):
    if theme == "amber":
        g = Image.new("RGB", (W, H), AMBER)
        ImageDraw.Draw(g).ellipse((-300, 700, 700, 1700), fill=(226, 146, 58))
        return g.filter(ImageFilter.GaussianBlur(140))
    g = Image.new("RGB", (W, H), BG)
    ImageDraw.Draw(g).ellipse((380, -260, 1300, 620), fill=(46, 32, 16))
    return g.filter(ImageFilter.GaussianBlur(160))


def header(d, theme):
    ink = DARK if theme == "amber" else INK
    acc = DARK if theme == "amber" else AMBER
    d.text((70, 78), "D", font=head(40), fill=ink)
    d.text((70 + d.textlength("D", font=head(40)), 78), ".", font=head(40), fill=acc)
    d.text((70 + d.textlength("D.", font=head(40)) + 14, 78), "IASIO", font=head(40), fill=ink)
    d.rectangle((70, 150, 150, 155), fill=acc)


def footer(im, d, book, theme):
    amber = theme == "amber"
    ink, sub, mut = (DARK, DARK, DMUT) if amber else (INK, AMBER, MUTED)
    cw, ch = 96, 143
    c = Image.open(COVERS[book]).convert("RGB").resize((cw, ch), Image.LANCZOS)
    y = H - 70 - ch
    d.rectangle((68, y - 2, 70 + cw + 1, y + ch + 1), outline=DARK if amber else LINE, width=2)
    im.paste(c, (70, y))
    d.text((70 + cw + 28, y + 16), TITLES[book], font=head(30), fill=ink)
    d.text((70 + cw + 28, y + 62), "Puntata 1 gratis · libri.diasio.ch", font=serifr(28), fill=sub)
    d.text((70 + cw + 28, y + 104), "@d.iasio.libri", font=serifr(24), fill=mut)


def text_block(d, lines, font, x, y, lh, fill):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def k_quote(im, d, p, theme):
    ink, mut = (DARK, DMUT) if theme == "amber" else (INK, MUTED)
    size = 80 if len(p["text"]) < 90 else 66
    f = serif(size)
    lines = wrap(d, "“" + p["text"] + "”", f, W - 140)
    lh = int(size * 1.32)
    y = 250 + (700 - len(lines) * lh) // 2
    y = text_block(d, lines, f, 70, y, lh, ink)
    d.text((70, y + 30), "— " + p["who"], font=serifr(30), fill=mut)


def k_hook(im, d, p, theme):
    ink, mut, acc = (DARK, DMUT, DARK) if theme == "amber" else (INK, MUTED, AMBER)
    f = head(84)
    lines = wrap(d, p["text"], f, W - 140)
    y = 250 + (620 - len(lines) * 108) // 2
    y = text_block(d, lines, f, 70, y, 108, ink)
    d.rectangle((70, y + 20, 150, y + 25), fill=acc)
    sf = serifr(38)
    y += 30
    for ln in wrap(d, p["sub"], sf, W - 140):
        y += 56
        d.text((70, y), ln, font=sf, fill=mut)


def k_brand(im, d, p, theme):
    d.text((70, 330), p["text"], font=head(250), fill=DARK)
    d.rectangle((70, 640, 150, 646), fill=DARK)
    d.text((70, 690), p["tag"], font=head(88), fill=DARK)
    sf = serifr(38)
    y = 850
    for ln in wrap(d, p["sub"], sf, W - 140):
        d.text((70, y), ln, font=sf, fill=DMUT)
        y += 56


def k_notif(im, d, p, theme):
    d.text((70, 260), p["kicker"], font=head(32), fill=AMBER)
    d.rounded_rectangle((70, 340, 1010, 760), 40, fill=PANEL, outline=LINE, width=2)
    d.ellipse((110, 380, 190, 460), fill=(150, 196, 232))
    d.text((132, 392), "M", font=head(52), fill=(20, 40, 70))
    d.text((214, 396), "MERIDIANA LIFE", font=head(34), fill=MUTED)
    d.text((880, 400), "adesso", font=serifr(30), fill=MUTED)
    f = serifr(56)
    text_block(d, wrap(d, p["text"], f, 860), f, 110, 500, 76, INK)
    sf = serif(44)
    y = 830
    for ln in wrap(d, p["sub"], sf, W - 140):
        d.text((70, y), ln, font=sf, fill=MUTED)
        y += 62


def k_terminal(im, d, p, theme):
    d.rounded_rectangle((70, 240, 1010, 1010), 22, fill=(13, 20, 32), outline=LINE, width=2)
    for i, c in enumerate([(200, 80, 70), (226, 170, 70), (90, 170, 100)]):
        d.ellipse((104 + i * 34, 274, 124 + i * 34, 294), fill=c)
    d.text((240, 268), p["file"], font=mono(30), fill=MUTED)
    d.line((70, 326, 1010, 326), fill=LINE, width=2)
    f = mono(38)
    y = 366
    for para in p["lines"]:
        col = AMBER if para.get("hot") else INK
        for ln in wrap(d, para["t"], f, 860):
            d.text((110, y), ln, font=f, fill=col)
            y += 54
        y += 22


def k_panel(im, d, p, theme):
    d.text((70, 250), p["title"], font=head(62), fill=AMBER)
    d.rectangle((70, 340, 150, 345), fill=AMBER)
    f = serifr(46)
    y = 400
    for i, ln in enumerate(p["lines"]):
        for w in wrap(d, ln, f, W - 140):
            d.text((70, y), w, font=f, fill=INK if i < len(p["lines"]) - 1 else AMBER)
            y += 64
        y += 34
        d.line((70, y - 18, 1010, y - 18), fill=LINE, width=2)


def k_receipt(im, d, p, theme):
    x0, x1, y0, y1 = 130, 950, 230, 960
    pts = [(x0, y0), (x1, y0), (x1, y1)]
    for i in range(0, x1 - x0, 30):
        pts += [(x1 - i - 15, y1 + 22), (x1 - i - 30, y1)]
    d.polygon(pts, fill=INK)
    f, fb = mono(38), monob(38)
    d.text((x0 + 50, y0 + 50), p["title"], font=monob(34), fill=DARK)
    d.text((x0 + 50, y0 + 100), p["subtitle"], font=mono(30), fill=DMUT)
    d.line((x0 + 50, y0 + 150, x1 - 50, y0 + 150), fill=DARK, width=3)
    y = y0 + 190
    for label, price in p["rows"]:
        pw = d.textlength(price, font=fb)
        lw = d.textlength(label, font=f)
        dots = "." * max(3, int((x1 - x0 - 100 - pw - lw - 20) / d.textlength(".", font=f)))
        d.text((x0 + 50, y), label, font=f, fill=DARK)
        d.text((x0 + 50 + lw + 8, y), dots, font=f, fill=DMUT)
        d.text((x1 - 50 - pw, y), price, font=fb, fill=DARK)
        y += 74
    d.line((x0 + 50, y + 10, x1 - 50, y + 10), fill=DARK, width=3)
    nf = mono(30)
    y += 44
    for ln in wrap(d, p["note"], nf, x1 - x0 - 100):
        d.text((x0 + 50, y), ln, font=nf, fill=DMUT)
        y += 42


def k_spot(im, d, p, theme):
    ch = 830
    cw = round(ch * 900 / 1342)
    x, y = (W - cw) // 2, 210
    c = Image.open(COVERS[p["book"]]).convert("RGB").resize((cw, ch), Image.LANCZOS)
    d.rectangle((x - 3, y - 3, x + cw + 2, y + ch + 2), outline=LINE, width=3)
    im.paste(c, (x, y))
    tf = serif(40)
    yy = y + ch + 34
    for ln in wrap(d, p["tag"], tf, W - 160):
        d.text(((W - d.textlength(ln, font=tf)) / 2, yy), ln, font=tf, fill=INK)
        yy += 54
    cta = "Puntata 1 gratis · link in bio"
    d.text(((W - d.textlength(cta, font=head(34))) / 2, yy + 14), cta, font=head(34), fill=AMBER)


def k_both(im, d, p, theme):
    ch = 620
    cw = round(ch * 900 / 1342)
    gap = 34
    x0, y = (W - (2 * cw + gap)) // 2, 230
    for i, b in enumerate(["bug", "oblio"]):
        c = Image.open(COVERS[b]).convert("RGB").resize((cw, ch), Image.LANCZOS)
        x = x0 + i * (cw + gap)
        d.rectangle((x - 3, y - 3, x + cw + 2, y + ch + 2), outline=LINE, width=3)
        im.paste(c, (x, y))
    f = head(70)
    yy = text_block(d, wrap(d, p["text"], f, W - 140), f, 70, y + ch + 44, 88, INK)
    sf = serifr(36)
    for ln in wrap(d, p["sub"], sf, W - 140):
        d.text((70, yy + 8), ln, font=sf, fill=MUTED)
        yy += 50
    d.text((70, H - 90), "@d.iasio.libri · libri.diasio.ch", font=serifr(28), fill=AMBER)


KINDS = dict(quote=k_quote, hook=k_hook, brand=k_brand, notif=k_notif, terminal=k_terminal,
             panel=k_panel, receipt=k_receipt, spot=k_spot, both=k_both)
NOFOOT = {"spot", "both"}


def card(p, out):
    theme = p.get("theme", "dark")
    im = canvas(theme)
    d = ImageDraw.Draw(im)
    header(d, theme)
    KINDS[p["kind"]](im, d, p, theme)
    if p["kind"] not in NOFOOT:
        footer(im, d, p["book"], theme)
    im.save(out, quality=92, optimize=True)


if __name__ == "__main__":
    os.makedirs("../img", exist_ok=True)
    for p in POSTS:
        card(p, f"../img/{p['id']}.jpg")
        print(p["id"])
