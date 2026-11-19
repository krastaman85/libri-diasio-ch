"""ASMR dei libri del 19/11/2026 (decisione di Davide: campagne concentrate su Vuoto a rendere e L'Aritmetica del Consenso).
Video montati sul PC con video-tools\\lavori\\ASMR Wan\\montaggio\\voce_reel.py (configurazioni in reel_voce.json);
clip Seedance 2.0 Mini da un primo fotogramma Firefly, voce dall'audiolibro (Persona «D. Iasio - Narratore»).
Frasi testuali dalla Puntata 1 (download/*.epub). Idempotente: aggiunge o aggiorna solo le voci elencate qui."""
import json
from pathlib import Path

CAL = Path(__file__).resolve().parents[1] / "calendar.json"

VUOTO_IG_FINE = ("Vuoto a rendere è su Amazon Kindle: link in bio. Anche in cartaceo.\n"
                 "Incluso in Kindle Unlimited. L’inizio è gratis su libri.diasio.ch.\n"
                 "Video, voce e suono creati con l’IA.\n\n"
                 "#RomanzoSatirico #UmorismoNero #BookstagramItalia #LibriDaLeggere #Ticino")
VUOTO_FB_FINE = ("Vuoto a rendere su Amazon Kindle: https://www.amazon.it/dp/B0HM4HFK34\n"
                 "Cartaceo: https://www.amazon.it/dp/B0HMFNKKJ2\n"
                 "Incluso in Kindle Unlimited.\n"
                 "L’inizio è gratis, in PDF o EPUB, senza iscrizione: https://libri.diasio.ch/vuoto/\n"
                 "Video, voce e suono creati con l’IA.\n\n"
                 "#RomanzoSatirico #Satira #UmorismoNero #CommediaNera #BookstagramItalia #ConsigliDiLettura "
                 "#LibriDaLeggere #ScrittoriItaliani #Ticino #LeggereInSvizzera")
VUOTO_TT_FINE = ("«Vuoto a rendere» di D. Iasio: ebook su Amazon Kindle (anche in Kindle Unlimited) e copertina flessibile. "
                 "Cercalo su Amazon.\n\n#RomanzoSatirico #UmorismoNero #BookTokItalia #LibriDaLeggere #Ticino")

PORTA = ("ASMR da un romanzo satirico, letto ad alta voce: una porta di faggio che si richiude senza un rumore, "
         "in una sala del commiato.\n«La porta si richiuse col suono ovattato che Dario aveva scelto dal catalogo dei fornitori.» "
         "È una riga di Vuoto a rendere. Meglio in cuffia.")

ARIT_IG_FINE = ("L’Aritmetica del Consenso è su Amazon Kindle: link in bio.\n"
                "Incluso in Kindle Unlimited. L’inizio è gratis su libri.diasio.ch.\n"
                "Video, voce e suono creati con l’IA.\n\n"
                "#NoirItaliano #LetteraturaNoir #BookstagramItalia #ScrittoriItaliani #Ticino")
ARIT_FB_FINE = ("L’Aritmetica del Consenso su Amazon Kindle: https://www.amazon.it/dp/B0HM3Y19B6\n"
                "Incluso in Kindle Unlimited.\n"
                "L’inizio è gratis, in PDF o EPUB, senza iscrizione: https://libri.diasio.ch/aritmetica/\n"
                "Video, voce e suono creati con l’IA.\n\n"
                "#NoirItaliano #RomanzoNoir #LetteraturaNoir #GialloItaliano #BookstagramItalia #ConsigliDiLettura "
                "#ScrittoriItaliani #Ticino #SvizzeraItaliana #CulturaTicino")
ARIT_TT_FINE = ("«L’Aritmetica del Consenso» di D. Iasio: ebook su Amazon Kindle, anche in Kindle Unlimited. "
                "Cercalo su Amazon.\n\n#NoirItaliano #LetteraturaNoir #BookTokItalia #LibriDaLeggere #Ticino")

BUSTE = ("ASMR da un romanzo noir, letto ad alta voce: buste di carta sul tavolo di una cucina, sotto una lampada verde.\n"
         "«Ogni primo del mese contava le buste con lei sul tavolo della cucina…» "
         "È una riga de L’Aritmetica del Consenso. Meglio in cuffia.")

VOCI = [
    {"id": "asmr7-vuoto-porta", "tipo": "reel", "segmento": "ASMR dei libri · Reel con voce narrante",
     "video": "social/video/asmr7-vuoto-porta.mp4", "miniatura_ms": 9500, "quando": "2027-01-13T19:41",
     "didascalia": PORTA + "\n\n" + VUOTO_IG_FINE, "didascalia_fb": PORTA + "\n\n" + VUOTO_FB_FINE,
     "commento": "Pagina quarantadue del catalogo: anche il silenzio ha il suo codice articolo."},
    {"id": "tasmr7-vuoto-porta", "tipo": "reel", "quando": "2026-12-16T21:05",
     "segmento": "TikTok · ASMR dei libri con voce narrante",
     "video": "social/video/asmr7-vuoto-porta.mp4", "miniatura_ms": 9500, "piattaforme": ["tiktok"], "ia": True,
     "didascalia": PORTA + "\n\n" + VUOTO_TT_FINE,
     "commento": "C'è chi sceglie le porte dal catalogo. E c'è chi le usa per uscire prima della fine."},
    {"id": "asmr8-aritmetica-buste", "tipo": "reel", "segmento": "ASMR dei libri · Reel con voce narrante",
     "video": "social/video/asmr8-aritmetica-buste.mp4", "miniatura_ms": 1500, "quando": "2027-01-20T19:33",
     "didascalia": BUSTE + "\n\n" + ARIT_IG_FINE, "didascalia_fb": BUSTE + "\n\n" + ARIT_FB_FINE,
     "commento": "Una lampada che non faceva ombre: in quella casa era l’unica cosa che non nascondeva niente."},
    {"id": "tasmr8-aritmetica-buste", "tipo": "reel", "quando": "2026-12-20T21:05",
     "segmento": "TikTok · ASMR dei libri con voce narrante",
     "video": "social/video/asmr8-aritmetica-buste.mp4", "miniatura_ms": 1500, "piattaforme": ["tiktok"], "ia": True,
     "didascalia": BUSTE + "\n\n" + ARIT_TT_FINE,
     "commento": "Il primo del mese, sul tavolo della cucina: in certe case il conto si fa ancora a mano."},
]


def main():
    d = json.loads(CAL.read_text(encoding="utf-8"))
    per_id = {p["id"]: p for p in d["post"]}
    for v in VOCI:
        if v["id"] in per_id:
            per_id[v["id"]].update(v)
        else:
            d["post"].append(dict(v))
    CAL.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
