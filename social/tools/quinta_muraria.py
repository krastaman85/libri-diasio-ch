# Campagna «Quinta Muraria» (richiesta di Davide del 14/11/2026): toglie i 4 Reel musicali del sabato
# (Spirale di vetro e L'Archivio della Sete, mu1-mu4 con le Storie mus1-mus4) e inserisce il lancio di
# «Venerdì Nero» (primo estratto, video ufficiale su YouTube il 27/11 alle 19:00, lyric video il 30/11)
# e l'annuncio dell'album «Quinta Muraria» (2027, senza data precisa). Testi da «Venerdì Nero - caption.md».
# Ogni Reel/carosello porta la sua Storia (campo "poi", id mus*: il promemoria serale ricorda l'highlight «Musica»).
# Uso: python social/tools/quinta_muraria.py   (idempotente)
import json
from pathlib import Path
SOCIAL = Path(__file__).resolve().parent.parent
CAL = SOCIAL / "calendar.json"
YT = "https://www.youtube.com/@D.IAsio_music"
SITO = "https://musica.diasio.ch/"
AMZ = "https://www.amazon.it/dp/B0HM4HFK34"
CRED = "Testi di D.IAsio. Musica e immagini create con l’ausilio di strumenti IA."   # formula di Davide (14/11/2026), ovunque
KIN_IG = "E se ti piacciono le storie nere, i romanzi di D.IAsio sono su Amazon Kindle (link in bio)."
KIN_FB = f"E se ti piacciono le storie nere, Vuoto a rendere è su Amazon Kindle: {AMZ}"
VN_IG = "#VenerdiNero #BlackFriday #MetalItaliano #RapItaliano #DIAsio"
VN_FB = "#VenerdiNero #BlackFriday #MetalItaliano #RapItaliano #DIAsio #QuintaMuraria #MusicaItaliana #NuovaMusica #SymphonicMetal #ArtistiEmergenti #Ticino #SvizzeraItaliana"
QM_IG = "#QuintaMuraria #MetalItaliano #RapItaliano #DIAsio #Ticino"
QM_FB = "#QuintaMuraria #MetalItaliano #RapItaliano #DIAsio #MusicaItaliana #NuovaMusica #SymphonicMetal #RapConscious #ArtistiEmergenti #Ticino #SvizzeraItaliana #CulturaTicino"


def cap(testo, cta_ig, cta_fb, tag_ig, tag_fb):
    ig = f"{testo}\n\n{cta_ig}\n{CRED}\n\n{KIN_IG}\n\n{tag_ig}"
    fb = f"{testo}\n\n{cta_fb}\n{CRED}\n\n{KIN_FB}\n\n{tag_fb}"
    return ig, fb


PRIMA_IG = "Video ufficiale venerdì 27 novembre alle 19:00 sul canale YouTube @D.IAsio_music: link in bio."
PRIMA_FB = f"Video ufficiale venerdì 27 novembre alle 19:00 su YouTube: {YT}"
DOPO_IG = "Il video ufficiale è sul canale YouTube @D.IAsio_music: link in bio."
DOPO_FB = f"Il video ufficiale è su YouTube: {YT}\nIl sito della musica: {SITO}"

# id, quando, tipo, file (video o elenco immagini), miniatura_ms, testo, prima/dopo, vn/qm, segmento, storia, alt
POST = [
    ("mu5-vn-annuncio", "2026-11-17T12:31", "carosello", [f"social/img/nuovi/mu5-vn-annuncio-0{i}.jpg" for i in range(1, 6)], None,
     "27.11. Venerdì Nero.\nIl giorno in cui tutto è in offerta, tranne il tempo.\nScorri: quattro versi dal brano.", "prima", "vn",
     "D.IAsio music · Venerdì Nero · annuncio", "mus5-vn-annuncio",
     "Carosello di cinque slide: la copertina di Venerdì Nero (un teatro con un'eclissi sopra un carrello vuoto) e quattro scene del video con un verso del brano."),
    ("mu6-vn-tre", "2026-11-19T19:12", "reel", "social/video/mu6-vn-tre.mp4", 9000,
     "TRE.\n«E nessuna di quelle mani ha un nome.»\nVenerdì Nero · 27.11", "prima", "vn", "D.IAsio music · Venerdì Nero · TRE", "mus6-vn-tre", None),
    ("mu7-vn-carrello", "2026-11-21T12:16", "reel", "social/video/mu7-vn-carrello.mp4", 2000,
     "Compra. Consuma. Dimentica.\nDietro un carrello che viaggia in digitale c’è sempre qualcuno che lo spinge.\nVenerdì Nero · 27.11", "prima", "vn",
     "D.IAsio music · Venerdì Nero · dietro il carrello", "mus7-vn-carrello", None),
    ("mu8-vn-due", "2026-11-22T12:14", "reel", "social/video/mu8-vn-due.mp4", 10000,
     "DUE.\nRiempiamo le stanze per svuotare il cuore.\nVenerdì Nero · 27.11", "prima", "vn", "D.IAsio music · Venerdì Nero · DUE", "mus8-vn-due", None),
    ("mu9-vn-uno", "2026-11-25T12:41", "reel", "social/video/mu9-vn-uno.mp4", 6000,
     "UNO.\nCosa cerchi davvero sul fondo del carrello?\nRispondi qui sotto. Venerdì Nero · 27.11", "prima", "vn", "D.IAsio music · Venerdì Nero · UNO", "mus9-vn-uno", None),
    ("mu10-vn-vigilia", "2026-11-26T19:22", "reel", "social/video/mu10-vn-vigilia.mp4", 9000,
     "Domani. Aperto.\nVenerdì Nero, video ufficiale: 27.11 alle 19:00.", "prima", "vn", "D.IAsio music · Venerdì Nero · vigilia", "mus10-vn-vigilia", None),
    ("mu11-vn-oggi", "2026-11-27T12:33", "reel", "social/video/mu11-vn-oggi.mp4", 3000,
     "Oggi è Black Friday. Stasera alle 19:00 esce Venerdì Nero.\nVenerdì nero, l’eclissi del valore: e chiamalo sconto, chiamalo affare.", "prima", "vn",
     "D.IAsio music · Venerdì Nero · giorno d'uscita", "mus11-vn-oggi", None),
    ("mu12-vn-aperto", "2026-11-28T12:27", "reel", "social/video/mu12-vn-aperto.mp4", 8000,
     "APERTO.\nVenerdì Nero è fuori: un uomo di vetro si riempie di pacchi fino a nascondere il cuore. Poi dice basta.\nCi hanno venduto la fretta e l’abbiamo chiamata libertà.", "dopo", "vn",
     "D.IAsio music · Venerdì Nero · fuori ora", "mus12-vn-aperto", None),
    ("mu13-vn-lyric", "2026-11-30T12:24", "reel", "social/video/mu13-vn-lyric.mp4", 3000,
     "Cyber Monday. L’offerta scade, la domanda resta.\nDa oggi su YouTube anche il lyric video di Venerdì Nero, con il testo intero.", "dopo", "vn",
     "D.IAsio music · Venerdì Nero · lyric video", "mus13-vn-lyric", None),
    ("mu14-vn-alba", "2026-12-02T12:18", "reel", "social/video/mu14-vn-alba.mp4", 6000,
     "Basta così. Io ho già abbastanza.\nIl finale di Venerdì Nero: l’uomo di vetro posa l’ultimo pacco e guarda l’alba.", "dopo", "vn",
     "D.IAsio music · Venerdì Nero · finale", "mus14-vn-alba", None),
    ("mu15-qm-album", "2026-12-05T12:38", "carosello", [f"social/img/nuovi/mu15-qm-album-{i:02d}.jpg" for i in range(1, 10)], None,
     "Quinta Muraria. Il nuovo album di D.IAsio, nel 2027.\nUn solo teatro: la quinta muraria è la parete di fondo del palco, quella che regge la scena. Qui crolla.\nScorri le copertine. Il primo estratto, Venerdì Nero, è già fuori: quale aspetti dopo?",
     "album", "qm", "D.IAsio music · Quinta Muraria · annuncio dell'album", "mus15-qm-album",
     "Carosello di nove slide: la copertina dell'album Quinta Muraria (un teatro all'italiana con il muro di quinta spaccato da una crepa di luce) e le copertine dei brani sullo stesso teatro."),
    ("mu16-qm-sipario", "2026-12-12T12:09", "reel", "social/video/mu16-qm-sipario.mp4", 22000,
     "Sipario.\nUna città in miniatura appesa ai fili, e qualcuno in regia che decide cosa va in onda.\nUn estratto dall’album Quinta Muraria, nel 2027.", "album", "qm",
     "D.IAsio music · Quinta Muraria · Sipario (estratto)", "mus16-qm-sipario", None),
]
ALBUM_IG = "Venerdì Nero, il primo estratto, è sul canale YouTube @D.IAsio_music: link in bio."
ALBUM_FB = f"Venerdì Nero, il primo estratto, è su YouTube: {YT}\nIl sito della musica: {SITO}"


# TikTok (14/11/2026): la musica va SOLO sul profilo personale @d.diasio, tramite Buffer (canale "musica").
# Stesso video del Reel, la sera alle 20:xx; niente "link in bio" e niente riga Kindle (profilo personale, solo musica).
TIKTOK = {  # id del Reel -> (orario, testo)
    "mu6-vn-tre": ("20:34", "TRE.\n«E nessuna di quelle mani ha un nome.»"),
    "mu7-vn-carrello": ("20:12", "Compra. Consuma. Dimentica.\nDietro un carrello che viaggia in digitale c’è sempre qualcuno che lo spinge."),
    "mu8-vn-due": ("20:41", "DUE.\nRiempiamo le stanze per svuotare il cuore."),
    "mu9-vn-uno": ("20:27", "UNO.\nCosa cerchi davvero sul fondo del carrello? Rispondi nei commenti."),
    "mu10-vn-vigilia": ("20:48", "Domani. Aperto."),
    "mu11-vn-oggi": ("20:06", "Il video ufficiale di Venerdì Nero è uscito alle 19:00. Buon Black Friday.\nE chiamalo sconto, chiamalo affare."),
    "mu12-vn-aperto": ("20:19", "APERTO.\nUn uomo di vetro si riempie di pacchi fino a nascondere il cuore. Poi dice basta."),
    "mu13-vn-lyric": ("20:38", "Cyber Monday. L’offerta scade, la domanda resta.\nVenerdì Nero, con il testo intero."),
    "mu14-vn-alba": ("20:23", "Basta così. Io ho già abbastanza."),
    "mu16-qm-sipario": ("20:31", "Sipario.\nUna città in miniatura appesa ai fili, e qualcuno in regia che decide cosa va in onda.\nDall’album Quinta Muraria, nel 2027."),
}
TT_PRIMA = "Venerdì Nero di D.IAsio: video ufficiale il 27.11 alle 19:00 su YouTube (cerca D.IAsio music)."
TT_DOPO = "Venerdì Nero di D.IAsio: video ufficiale su YouTube (cerca D.IAsio music)."
TT_ALBUM = "Il primo estratto, Venerdì Nero, è su YouTube (cerca D.IAsio music)."
TT_TAG = {"vn": "#VenerdiNero #BlackFriday #MetalItaliano #RapItaliano #DIAsio", "qm": "#QuintaMuraria #MetalItaliano #RapItaliano #DIAsio #MusicaItaliana"}


def main():
    cal = json.loads(CAL.read_text(encoding="utf-8"))
    via = {"mu1-spirale-di-vetro", "mus1-spirale-di-vetro", "mu2-archivio-della-sete", "mus2-archivio-della-sete",
           "mu3-spirale-di-vetro-2", "mus3-spirale-di-vetro-2", "mu4-archivio-della-sete-2", "mus4-archivio-della-sete-2"}
    nuovi_id = {p[0] for p in POST} | {p[9] for p in POST} | {p[0].replace("-", "t-", 1) for p in POST}
    cal["post"] = [p for p in cal["post"] if p["id"] not in via and p["id"] not in nuovi_id]
    for pid, quando, tipo, f, mini, testo, fase, serie, seg, sid, alt in POST:
        cta = {"prima": (PRIMA_IG, PRIMA_FB), "dopo": (DOPO_IG, DOPO_FB), "album": (ALBUM_IG, ALBUM_FB)}[fase]
        tags = (VN_IG, VN_FB) if serie == "vn" else (QM_IG, QM_FB)
        ig, fb = cap(testo, cta[0], cta[1], *tags)
        p = {"id": pid, "tipo": tipo, "quando": quando, "segmento": seg}
        if tipo == "reel":
            p["video"] = f; p["miniatura_ms"] = mini
        else:
            p["immagini"] = f; p["alt"] = alt
        p.update({"didascalia": ig, "didascalia_fb": fb, "poi": sid})
        cal["post"].append(p)
        sm = int(quando[-2:]) + 3
        if pid in TIKTOK:
            ora, tt = TIKTOK[pid]
            cta = {"prima": TT_PRIMA, "dopo": TT_DOPO, "album": TT_ALBUM}[fase]
            cal["post"].append({"id": pid.replace("-", "t-", 1), "tipo": "reel", "quando": f"{quando[:10]}T{ora}",
                                "segmento": "TikTok @d.diasio · " + seg, "video": f, "miniatura_ms": mini,
                                "piattaforme": ["tiktok"], "tiktok_canale": "musica", "ia": True,
                                "didascalia": f"{tt}\n\n{cta}\n{CRED}\n\n{TT_TAG[serie]}"})
        cal["post"].append({"id": sid, "tipo": "storia", "quando": f"{quando[:-2]}{sm:02d}",
                            "segmento": "Storia · D.IAsio music (highlight Musica)", "immagine": f"social/img/story/{sid}.jpg"})
    cal["post"].sort(key=lambda x: x["quando"])
    nl = "\r\n" if b"\r\n" in CAL.read_bytes()[:200] else "\n"
    CAL.write_bytes((json.dumps(cal, indent=2, ensure_ascii=False) + "\n").replace("\n", nl).encode("utf-8"))
    print("tolti", len(via), "· aggiunti", 2 * len(POST) + len(TIKTOK))


if __name__ == "__main__":
    main()
