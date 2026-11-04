# Storie abbinate alle serie del piano D.IAsio (4/11/2026): «Inizia qui» (iq0), «Moduli ticinesi» (mt1-mt8),
# «La puntata» (pb1-pb8). Escono subito dopo il post (campo "poi" in calendar.json) e servono a riempire gli
# highlight omonimi, che l'utente crea a mano dall'app (l'API di Instagram non gestisce gli highlight).
# La Storia mostra la prima slide del post (stesso testo, nessuna frase nuova sui libri) su fondo sfocato.
# Uso: python social/tools/storie_serie.py   (scrive social/img/story/<id>.jpg)
import base64
import io
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOCIAL = HERE.parent
sys.path.insert(0, str(HERE))
import carousel as C  # noqa: E402

AMB = "#f0a24a"
NUOVI = SOCIAL / "img" / "nuovi"

# id del post -> (id della Storia, prima slide, occhiello, titolo, sottotitolo, riga finale)
SERIE = {"iq0-inizia-qui": ("iqs0-inizia-qui", "iq0-inizia-qui-01.jpg", "Inizia qui", "Da qui si comincia",
                            "Romanzi, una frase ogni sera alle 23:10, musica.", "Il post fissato in cima al profilo")}
MODULI = ["commemorazione", "listino-sordina", "domanda-lamentarsi", "verbale-assemblea", "certificato-grotto",
          "accettazione-nebbia", "listino-scuse", "ricevuta-ascensore"]
for n, slug in enumerate(MODULI, 1):
    pid = f"mt{n}-{'modulo-' if n == 1 else ''}{slug}"
    SERIE[pid] = (f"mts{n}-{slug}", f"{pid}.jpg", f"Moduli ticinesi · n. {n}", "Nuovo modulo nel feed",
                  "Compilalo. O mandalo a chi lo compilerebbe così.", "Tutti i moduli negli highlight")
for n in range(1, 9):
    pid = f"pb{n}-bug-puntata-{n}"
    SERIE[pid] = (f"pbs{n}-bug-puntata-{n}", f"{pid}-01.jpg", f"La puntata · {n}/8", "Il Bug della Trasparenza",
                  "Nuova puntata nel feed. L’inizio è gratis.", "Tutte le puntate negli highlight")

CSS = f"""body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#07090e;color:#f3ead8;font-family:'Source Serif 4',serif}}
.bg{{position:absolute;inset:-60px;background-size:cover;background-position:center;filter:blur(46px) brightness(.34) saturate(.85)}}
.vg{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(7,9,14,.75),rgba(7,9,14,.15) 30%,rgba(7,9,14,.2) 62%,rgba(7,9,14,.92))}}
.kick{{position:absolute;left:0;right:0;top:300px;text-align:center;font:500 34px 'Oswald';letter-spacing:.32em;text-transform:uppercase;color:{AMB}}}
.kick:after{{content:"";display:block;width:64px;height:3px;background:{AMB};margin:22px auto 0}}
.card{{position:absolute;left:118px;top:420px;width:844px;height:1055px;border-radius:22px;background-size:cover;
box-shadow:0 50px 110px -20px rgba(0,0,0,.9),0 0 0 2px rgba(255,255,255,.08)}}
.tit{{position:absolute;left:60px;right:60px;top:1530px;text-align:center;font:700 66px/1.05 'Oswald';text-transform:uppercase;letter-spacing:.02em}}
.sub{{position:absolute;left:90px;right:90px;top:1618px;text-align:center;font:italic 400 40px/1.3 'Source Serif 4';color:#e6dccb}}
.cta{{position:absolute;left:0;right:0;top:1740px;text-align:center;font:500 26px 'Oswald';letter-spacing:.26em;color:{AMB};text-transform:uppercase}}"""


def b64(path):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=92)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def main(solo=None):
    from playwright.sync_api import sync_playwright
    out = SOCIAL / "img" / "story"
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH") or None)
        pg = br.new_page(viewport={"width": 1080, "height": 1920})
        for pid, (sid, slide, kick, tit, sub, cta) in SERIE.items():
            if solo and sid not in solo:
                continue
            img = b64(NUOVI / slide)
            pg.set_content(f"<html><head><style>{C.fontface()}{CSS}</style></head><body>"
                           f"<div class=bg style=\"background-image:url({img})\"></div><div class=vg></div>"
                           f"<div class=kick>{kick}</div><div class=card style=\"background-image:url({img})\"></div>"
                           f"<div class=tit>{tit}</div><div class=sub>{sub}</div><div class=cta>{cta}</div></body></html>")
            pg.wait_for_timeout(250)
            pg.screenshot(path=str(out / f"{sid}.jpg"), type="jpeg", quality=90)
            print("→", f"img/story/{sid}.jpg")
        br.close()


if __name__ == "__main__":
    main(set(sys.argv[1:]) or None)
