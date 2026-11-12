# Piano D.IAsio (approvato il 3/11/2026): dal 16/11 un post al giorno + la frase delle 23:10, in giorni fissi.
#   Lun e Gio: Moduli ticinesi (mt*) · Mar e Ven: La puntata del Bug (pb*) · Mer e Dom: Il libro (post già pronti, uno per libro a settimana)
#   Sab: D.IAsio music (mu*, Reel dai videoclip del canale YouTube @D.IAsio_music)
# Dal 12/11/2026 il mercoledì de «Il libro» è l'ASMR del libro quando esiste (asmr*: oggetti dei romanzi, Blender/Firefly + Seedance, suono generato);
# i post che sostituisce (x05, x01) restano in calendario come sospesi.
# Dal 12/11/2026 (sera) c'è la voce narrante (Persona «D. Iasio - Narratore» su MusicAI, testi letti testuali dalla Puntata 1):
#   - sugli ASMR del mercoledì (asmr1…asmr4), che si alternano tra Vuoto a rendere e L'Aritmetica del Consenso;
#   - sui Reel «Voce narrante» della domenica (vn*: immagine di scena ferma con movimento lento + voce), al posto di x06, n21, n05 e x08.
#   Niente voce su rubrica 23:10, musica, Moduli, Puntate del Bug, Storie e caroselli. Bug e Oblio tornano dopo (decisione del 12/11).
# I post già in calendario che non rientrano nello schema restano, con "sospeso": true (riutilizzabili). Dal 14/12 al 31/12 resta un solo post al giorno.
# Idempotente: si può rilanciare. Uso: python social/tools/piano_diasio_calendario.py
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOCIAL = HERE.parent
sys.path.insert(0, str(HERE))
import carousel  # noqa: E402

AMZ_VUOTO = "https://www.amazon.it/dp/B0HM4HFK34"
NOTA = "piano D.IAsio 3/11/2026: fuori schema, da ricollocare"

# id -> orario (ora svizzera, dentro le finestre di cron-job.org; minuti diversi di settimana in settimana)
SCHEMA = {
    # settimana 1 (Vuoto a rendere)
    "iq0-inizia-qui": "2026-11-15T12:21",
    "mt1-modulo-commemorazione": "2026-11-16T18:14", "pb1-bug-puntata-1": "2026-11-17T19:22", "asmr1-vuoto-fazzoletto": "2026-11-18T19:31",
    "mt2-listino-sordina": "2026-11-19T12:17", "pb2-bug-puntata-2": "2026-11-20T18:09", "mu1-spirale-di-vetro": "2026-11-21T12:16",
    "vn1-vuoto-wifi": "2026-11-22T20:13",
    # settimana 2 (Il Bug della Trasparenza)
    "mt3-domanda-lamentarsi": "2026-11-23T18:26", "pb3-bug-puntata-3": "2026-11-24T19:34", "asmr3-aritmetica-lago": "2026-11-25T19:43",
    "mt4-verbale-assemblea": "2026-11-26T12:29", "pb4-bug-puntata-4": "2026-11-27T18:21", "mu2-archivio-della-sete": "2026-11-28T12:27",
    "vn2-aritmetica-ghostwriter": "2026-11-29T20:24",
    # settimana 3 (L'Economia dell'Oblio)
    "mt5-certificato-grotto": "2026-11-30T18:38", "pb5-bug-puntata-5": "2026-12-01T19:46", "asmr4-vuoto-diffusore": "2026-12-02T19:24",
    "mt6-accettazione-nebbia": "2026-12-03T12:41", "pb6-bug-puntata-6": "2026-12-04T18:33", "mu3-spirale-di-vetro-2": "2026-12-05T12:38",
    "vn3-vuoto-puntualita": "2026-12-06T20:36",
    # settimana 4 (L'Aritmetica del Consenso)
    "mt7-listino-scuse": "2026-12-07T18:19", "pb7-bug-puntata-7": "2026-12-08T19:27", "asmr2-aritmetica-mandarino": "2026-12-09T19:36",
    "mt8-ricevuta-ascensore": "2026-12-10T12:22", "pb8-bug-puntata-8": "2026-12-11T18:14", "mu4-archivio-della-sete-2": "2026-12-12T12:09",
    "x04-aritmetica-due-mani": "2026-12-13T20:18",
    # dicembre: la prima riga de L'Aritmetica letta, al posto della grafica x08 (stessa frase di vn3)
    "vn4-aritmetica-ministro": "2026-12-23T19:36",
}
# post di solo testo su Facebook nella stessa fascia di una puntata: spostati a pranzo dello stesso venerdì
SPOSTA = {"t04-oblio-listino": "2026-11-20T12:34", "t05-newsletter": "2026-12-04T12:16"}
# fine dicembre: un post al giorno; si tengono questi (feste comprese), gli altri non ancora usciti vanno in sospeso
TIENI_DICEMBRE = {"r22-bug-rettifica", "n15-oblio-otto-milioni", "x07-vuoto-predefinito", "d05-bug-istruttiva", "t06-feste",
                  "d08-bug-nel-dubbio", "c06-natale-albero", "r21-oblio-gratis", "d07-buone-feste",
                  "c03-oblio-pettine", "c04-tre-passi", "r23-oblio-cara", "d06-oblio-regolatevi",
                  "sx1-vuoto-regolamento", "d09-buon-anno"}

TAG_MU = ("#Ticino #SvizzeraItaliana #CulturaTicino #ScrittoriEmergenti #ScrittoriSvizzeri",
          "#Ticino #SvizzeraItaliana #CulturaTicino #ScrittoriEmergenti #ScrittoriSvizzeri #LeggereInSvizzera #BookstagramSvizzera #ScrittoriItaliani #EditoriaItaliana #Ironia")


def musica(id, titolo, apertura, su_youtube=True):
    canale = "Il brano intero è" if su_youtube else "Gli altri brani sono"
    testo = (f"D.IAsio music · {titolo}.\n{apertura}\n\n"
             f"{canale} sul canale YouTube @D.IAsio_music: link in bio.\n"
             "Testi di D.IAsio. Musica e immagini create con l’IA.")
    ig = f"{testo}\n\nE se ti piacciono le storie nere, i romanzi di D.IAsio sono su Amazon Kindle (link in bio).\n\n{TAG_MU[0]}"
    fb = (f"{testo.replace('link in bio', 'https://www.youtube.com/@D.IAsio_music')}\n\n"
          f"E se ti piacciono le storie nere, Vuoto a rendere è su Amazon Kindle: {AMZ_VUOTO}\n\n{TAG_MU[1]}")
    return {"id": id, "tipo": "reel", "segmento": "D.IAsio music · Reel dal videoclip", "video": f"social/video/{id}.mp4",
            "miniatura_ms": 1500, "didascalia": ig, "didascalia_fb": fb}


MUSICA = [
    musica("mu1-spirale-di-vetro", "Spirale di vetro", "Rap conscious dal Ticino: lavoro, merito e quello che resta quando la corsa si ferma."),
    musica("mu2-archivio-della-sete", "L’Archivio della Sete", "Un estratto del brano nuovo: dimmi quale verso ti resta in testa."),
    musica("mu3-spirale-di-vetro-2", "Spirale di vetro", "Un altro passaggio dello stesso brano. Quale parte preferisci?"),
    musica("mu4-archivio-della-sete-2", "L’Archivio della Sete", "Seconda parte del brano, meglio in cuffia."),
]


# miniatura_ms = fotogramma di copertina del Reel: la frase più forte del passo, scritta per intero sullo schermo.
# ASMR dei libri (12/11/2026): un oggetto del romanzo da vicinissimo, una voce che legge il passo (testuale, Puntata 1), cartello finale con la copertina.
# Prima riga della didascalia con le parole che un lettore cercherebbe (Instagram usa la didascalia per capire l'argomento).
IA_VOCE = "Video, voce e suono creati con l’IA."
KINDLE = {
    "vuoto": ("Vuoto a rendere è su Amazon Kindle: link in bio. Anche in cartaceo.\nIncluso in Kindle Unlimited. L’inizio è gratis su libri.diasio.ch.",
              "Vuoto a rendere su Amazon Kindle: https://www.amazon.it/dp/B0HM4HFK34\nCartaceo: https://www.amazon.it/dp/B0HMFNKKJ2\nIncluso in Kindle Unlimited.\n"
              "L’inizio è gratis, in PDF o EPUB, senza iscrizione: https://libri.diasio.ch/vuoto/",
              "#RomanzoSatirico #UmorismoNero #BookstagramItalia #LibriDaLeggere #Ticino",
              "#RomanzoSatirico #Satira #UmorismoNero #CommediaNera #BookstagramItalia #ConsigliDiLettura #LibriDaLeggere #ScrittoriItaliani #Ticino #LeggereInSvizzera",
              "«Vuoto a rendere» di D. Iasio: ebook su Amazon Kindle (anche in Kindle Unlimited) e copertina flessibile. Cercalo su Amazon.",
              "#RomanzoSatirico #UmorismoNero #BookTokItalia #LibriDaLeggere #Ticino"),
    "aritmetica": ("L’Aritmetica del Consenso è su Amazon Kindle: link in bio.\nIncluso in Kindle Unlimited. L’inizio è gratis su libri.diasio.ch.",
                   "L’Aritmetica del Consenso su Amazon Kindle: https://www.amazon.it/dp/B0HM3Y19B6\nIncluso in Kindle Unlimited.\n"
                   "L’inizio è gratis, in PDF o EPUB, senza iscrizione: https://libri.diasio.ch/aritmetica/",
                   "#NoirItaliano #LetteraturaNoir #BookstagramItalia #ScrittoriItaliani #Ticino",
                   "#NoirItaliano #RomanzoNoir #LetteraturaNoir #GialloItaliano #BookstagramItalia #ConsigliDiLettura #ScrittoriItaliani #Ticino #SvizzeraItaliana #CulturaTicino",
                   "«L’Aritmetica del Consenso» di D. Iasio: ebook su Amazon Kindle, anche in Kindle Unlimited. Cercalo su Amazon.",
                   "#NoirItaliano #LetteraturaNoir #BookTokItalia #LibriDaLeggere #Ticino"),
}


def asmr(id, apertura, miniatura_ms, segmento="ASMR dei libri · Reel con voce narrante", video=None):
    ig, fb, tag_ig, tag_fb = KINDLE["vuoto" if "vuoto" in id else "aritmetica"][:4]
    return {"id": id, "tipo": "reel", "segmento": segmento, "video": video or f"social/video/{id}.mp4", "miniatura_ms": miniatura_ms,
            "didascalia": f"{apertura}\n\n{ig}\n{IA_VOCE}\n\n{tag_ig}", "didascalia_fb": f"{apertura}\n\n{fb}\n{IA_VOCE}\n\n{tag_fb}"}


ASMR = [
    asmr("asmr1-vuoto-fazzoletto",
         "ASMR da un romanzo satirico, letto ad alta voce: una sala del commiato vuota, una porta che si chiude piano, un fazzoletto rimasto sulla sedia.\n"
         "«Sulla sedia restò un fazzoletto.» È una riga di Vuoto a rendere. Meglio in cuffia.", 18000),
    asmr("asmr3-aritmetica-lago",
         "ASMR da un romanzo noir, letto ad alta voce: una sala riunioni sopra il lago di Lugano, quattro tazzine ancora calde, le sedie vuote.\n"
         "«…che è la vista di tutti i soldi ticinesi, solo guardata da più in alto.» È L’Aritmetica del Consenso. Meglio in cuffia.", 16000),
    asmr("asmr4-vuoto-diffusore",
         "ASMR da un romanzo satirico, letto ad alta voce: legno chiaro, luce calda, un diffusore al cedro in una sala del commiato.\n"
         "«…un diffusore al cedro che spargeva odore di spa svizzera.» È Vuoto a rendere. Meglio in cuffia.", 7000),
    asmr("asmr2-aritmetica-mandarino",
         "ASMR da un romanzo noir, letto ad alta voce: un mandarino solo su un piattino d’argento, la buccia che si apre, uno spicchio che si stacca.\n"
         "«Somiglia a qualcuno che ho pagato.» È una battuta de L’Aritmetica del Consenso. Meglio in cuffia.", 12500),
]

# Voce narrante della domenica (12/11/2026): la scena Firefly del post x* che sostituiscono, movimento lento, la voce che legge il passo.
VOCE = [
    asmr("vn1-vuoto-wifi", "Il commiato laico, versione Sordina: niente ostie, connessione garantita.\n"
         "Una voce legge Vuoto a rendere, il romanzo satirico sulle pompe funebri che vendono il «sembra».", 13500, "Voce narrante · Reel"),
    asmr("vn2-aritmetica-ghostwriter", "Il narratore de L’Aritmetica del Consenso fa un mestiere invisibile per definizione.\n"
         "«…nessuno ringrazia l’idraulico, si ringrazia il rubinetto.» Una voce legge l’inizio del romanzo.", 8000, "Voce narrante · Reel"),
    asmr("vn3-vuoto-puntualita", "La prima riga di Vuoto a rendere, letta ad alta voce. Il resto è all’altezza.", 3500, "Voce narrante · Reel"),
    asmr("vn4-aritmetica-ministro", "La prima riga de L’Aritmetica del Consenso, letta ad alta voce: quanto costava un ministro.", 14500, "Voce narrante · Reel"),
]

# Gli ASMR con voce anche su TikTok (Buffer), la sera dello stesso giorno.
TIKTOK_ASMR = {"asmr1-vuoto-fazzoletto": "2026-11-18T21:05", "asmr3-aritmetica-lago": "2026-11-25T21:05",
               "asmr4-vuoto-diffusore": "2026-12-02T21:05", "asmr2-aritmetica-mandarino": "2026-12-09T21:05"}


def tiktok(m):
    libro = "vuoto" if "vuoto" in m["id"] else "aritmetica"
    riga, tag = KINDLE[libro][4:]
    apertura = m["didascalia"].split("\n\n")[0]
    return {"id": "t" + m["id"], "tipo": "reel", "quando": TIKTOK_ASMR[m["id"]], "segmento": "TikTok · ASMR dei libri con voce narrante",
            "video": m["video"], "miniatura_ms": m["miniatura_ms"], "piattaforme": ["tiktok"], "ia": True,
            "didascalia": f"{apertura}\n\n{riga}\n\n{tag}"}


# Storie musicali (3/11/2026): escono subito dopo il Reel del sabato (campo "poi"), da mettere a mano nell'highlight «Musica».
# Immagini da social/tools/storie_musica.py. L'orario della Storia (Reel + 3 minuti) vale solo come ripiego.
STORIE_MUSICA = {"mu1-spirale-di-vetro": "mus1-spirale-di-vetro", "mu2-archivio-della-sete": "mus2-archivio-della-sete",
                 "mu3-spirale-di-vetro-2": "mus3-spirale-di-vetro-2", "mu4-archivio-della-sete-2": "mus4-archivio-della-sete-2"}


# Storie delle serie (4/11/2026): dopo «Inizia qui», ogni Modulo e ogni Puntata esce una Storia (social/tools/storie_serie.py),
# da mettere a mano negli highlight «Inizia qui», «Moduli» e «La puntata».
from storie_serie import SERIE  # noqa: E402
STORIE_SERIE = {pid: v[0] for pid, v in SERIE.items()}
HIGHLIGHT = {"iq": "Inizia qui", "mt": "Moduli", "pb": "La puntata"}
STORIE_ABBINATE = {**STORIE_MUSICA, **STORIE_SERIE}


def storie_musica(cal):
    from datetime import datetime, timedelta
    have = {x["id"] for x in cal["post"]}
    for x in list(cal["post"]):
        sid = STORIE_ABBINATE.get(x["id"])
        if not sid:
            continue
        x["poi"] = sid
        quando = (datetime.fromisoformat(x["quando"]) + timedelta(minutes=3)).strftime("%Y-%m-%dT%H:%M")
        seg = ("Storia · D.IAsio music (highlight Musica)" if x["id"] in STORIE_MUSICA
               else f"Storia · {HIGHLIGHT[x['id'][:2]]} (highlight {HIGHLIGHT[x['id'][:2]]})")
        if sid not in have:
            cal["post"].append({"id": sid, "tipo": "storia", "quando": quando, "segmento": seg,
                                "immagine": f"social/img/story/{sid}.jpg"})
        else:
            next(y for y in cal["post"] if y["id"] == sid)["quando"] = quando


def main():
    p = SOCIAL / "calendar.json"
    testo = p.read_text(encoding="utf-8")
    cal = json.loads(testo)
    pub = json.loads((SOCIAL / "published.json").read_text(encoding="utf-8"))["pubblicati"]
    have = {x["id"] for x in cal["post"]}
    nuovi = [it for it in carousel.load() if it["id"] in SCHEMA and it["id"] not in have]
    for it in nuovi:
        it["when"] = SCHEMA[it["id"]]
    carousel.add_calendar(nuovi)   # scrive il file: lo rileggiamo
    cal = json.loads(p.read_text(encoding="utf-8"))
    have = {x["id"] for x in cal["post"]}
    voci = {x["id"]: x for x in cal["post"]}
    for m in MUSICA + ASMR + VOCE + [tiktok(a) for a in ASMR]:
        if m["id"] in pub:
            continue
        if m["id"] not in voci:
            cal["post"].append(dict(m, quando=m.get("quando") or SCHEMA[m["id"]]))
        else:                       # testi e file aggiornati (per esempio la voce aggiunta agli ASMR)
            voci[m["id"]].update(m)
    for x in cal["post"]:
        if x["id"] in pub or x.get("piattaforme") == ["tiktok"] or (x["id"][0] == "q" and x["id"][1].isdigit()):
            continue
        if x["id"] in STORIE_ABBINATE.values():   # Storie abbinate (musica e serie): le gestisce storie_musica()
            x.pop("sospeso", None)
            x.pop("nota", None)
        elif x["id"] in SCHEMA:
            x["quando"] = SCHEMA[x["id"]]
            x.pop("sospeso", None)
            x.pop("nota", None)
        elif x["id"] in SPOSTA:
            x["quando"] = SPOSTA[x["id"]]
        elif "2026-11-16" <= x["quando"][:10] <= "2026-12-13":
            x["sospeso"], x["nota"] = True, NOTA
        elif "2026-12-14" <= x["quando"][:10] <= "2026-12-31" and x["id"] not in TIENI_DICEMBRE:
            x["sospeso"], x["nota"] = True, NOTA
    storie_musica(cal)
    cal["post"].sort(key=lambda x: x["quando"])
    eol = "\r\n" if "\r\n" in testo else "\n"
    p.write_text((json.dumps(cal, indent=2, ensure_ascii=False) + "\n").replace("\n", eol), encoding="utf-8", newline="")
    print("calendario aggiornato:", len(cal["post"]), "voci")


if __name__ == "__main__":
    main()
