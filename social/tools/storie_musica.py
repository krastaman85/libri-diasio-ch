# Storie «D.IAsio music» (piano D.IAsio, 3/11/2026): una Storia 1080x1920 dopo ogni Reel musicale del sabato (campo "poi"),
# da mettere a mano nell'highlight «Musica» (l'API di Instagram non gestisce gli highlight).
# Fotogramma dal Reel (sopra la riga dei sottotitoli), lunetta da orologio dello stile degli highlight, firma una sola volta.
# Uso: python social/tools/storie_musica.py   (serve ffmpeg; scrive social/img/story/mus*.jpg)
import base64, math, subprocess, sys, tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
SOCIAL = HERE.parent
sys.path.insert(0, str(HERE))
import carousel as C  # noqa: E402

# id storia, video del Reel, secondo del fotogramma, titolo, riga
STORIE = [
    ("mus1-spirale-di-vetro", "mu1-spirale-di-vetro", 2, "Spirale di vetro", "Nuovo estratto"),
    ("mus2-archivio-della-sete", "mu2-archivio-della-sete", 9, "L’Archivio della Sete", "Nuovo brano"),
    ("mus3-spirale-di-vetro-2", "mu3-spirale-di-vetro-2", 9, "Spirale di vetro", "Seconda parte"),
    ("mus4-archivio-della-sete-2", "mu4-archivio-della-sete-2", 9, "L’Archivio della Sete", "Seconda parte"),
]
AMB = "#f0a24a"


def lunetta(r=402):
    t = []
    for i in range(60):
        a = math.radians(i * 6 - 90); r2 = r - (14 if i % 5 else 30)
        t.append(f'<line x1="{r*math.cos(a):.1f}" y1="{r*math.sin(a):.1f}" x2="{r2*math.cos(a):.1f}" y2="{r2*math.sin(a):.1f}" '
                 f'stroke="{AMB}" stroke-width="{2 if i % 5 else 5}" stroke-linecap="round" opacity="{.55 if i % 5 else .95}"/>')
    t.append(f'<circle r="{r+16}" fill="none" stroke="{AMB}" stroke-width="3"/><path d="M0,-{r+36} L-13,-{r+20} L13,-{r+20} Z" fill="{AMB}"/>')
    return "".join(t)


def fotogramma(video, sec):
    from PIL import Image, ImageFilter
    import io
    with tempfile.TemporaryDirectory() as d:
        png = Path(d) / "f.png"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(sec), "-i", str(SOCIAL / "video" / f"{video}.mp4"),
                        "-frames:v", "1", str(png)], check=True)
        im = Image.open(png).convert("RGB")
    w, h = im.size
    cerchio = im.crop((0, int(h * .05), w, int(h * .05) + w)).resize((720, 720), Image.LANCZOS)   # parte alta, senza sottotitoli
    fondo = im.resize((1080, 1920)).filter(ImageFilter.GaussianBlur(38))
    def b64(x):
        buf = io.BytesIO(); x.save(buf, "JPEG", quality=88); return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    return b64(cerchio), b64(fondo)


CSS = f"""body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#07090e;font-family:'Source Serif 4',serif;color:#f3ead8}}
.bg{{position:absolute;inset:0;background-size:cover;filter:brightness(.38) saturate(.8)}}
.vg{{position:absolute;inset:0;background:radial-gradient(circle at 50% 47%,rgba(7,9,14,0) 0,rgba(7,9,14,.55) 55%,rgba(7,9,14,.92) 100%)}}
.kick{{position:absolute;left:0;right:0;top:400px;text-align:center;font:500 34px 'Oswald';letter-spacing:.34em;color:{AMB}}}
.disc{{position:absolute;left:180px;top:540px;width:720px;height:720px;border-radius:50%;background-size:cover;box-shadow:0 0 120px rgba(240,162,74,.25)}}
svg{{position:absolute;left:0;top:0}}
.tit{{position:absolute;left:60px;right:60px;top:1380px;text-align:center;font:700 92px/1.05 'Oswald';text-transform:uppercase;letter-spacing:.02em}}
.sub{{position:absolute;left:60px;right:60px;top:1500px;text-align:center;font:italic 400 46px 'Source Serif 4';color:#e6dccb}}
.cta{{position:absolute;left:0;right:0;top:1590px;text-align:center;font:500 30px 'Oswald';letter-spacing:.24em;color:{AMB};text-transform:uppercase}}
.sig{{position:absolute;left:0;right:0;top:1650px;text-align:center;font:400 26px 'IBM Plex Mono';letter-spacing:.3em;color:#cfc6b6;opacity:.8}}"""


def main():
    from playwright.sync_api import sync_playwright
    out = SOCIAL / "img" / "story"
    out.mkdir(parents=True, exist_ok=True)
    import os
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH") or None)
        pg = br.new_page(viewport={"width": 1080, "height": 1920})
        for sid, video, sec, titolo, riga in STORIE:
            cer, fon = fotogramma(video, sec)
            svg = f'<svg width="1080" height="1920" viewBox="-540 -900 1080 1920">{lunetta()}</svg>'
            pg.set_content(f"<html><head><style>{C.fontface()}{CSS}</style></head><body>"
                           f"<div class=bg style=\"background-image:url({fon})\"></div><div class=vg></div>"
                           f"<div class=kick>D.IAsio music</div><div class=disc style=\"background-image:url({cer})\"></div>{svg}"
                           f"<div class=tit>{titolo}</div><div class=sub>{riga} · il brano intero su YouTube</div>"
                           f"<div class=cta>Link in bio</div><div class=sig>Musica e immagini create con l’IA</div></body></html>")
            pg.wait_for_timeout(250)
            pg.screenshot(path=str(out / f"{sid}.jpg"), type="jpeg", quality=90)
            print("→", f"img/story/{sid}.jpg")


if __name__ == "__main__":
    main()
