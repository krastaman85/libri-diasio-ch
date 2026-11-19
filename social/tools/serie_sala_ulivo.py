"""Serie «Sala Ulivo» su TikTok @d.iasio (decisione di Davide del 19/11/2026): il capitolo 1 di Vuoto a rendere letto,
13 puntate in ordine, martedì e venerdì alle 21:05. Video montati sul PC in video-tools\\lavori\\Serie Sala Ulivo
(monta_serie.py + episodi.json). Frasi testuali dalla Puntata 1 (download/vuoto-a-rendere-puntata-1.epub).
Idempotente: aggiunge o aggiorna solo le puntate elencate qui (quelle con il video già pronto)."""
import json
from pathlib import Path

CAL = Path(__file__).resolve().parents[1] / "calendar.json"
TAG = "#RomanzoSatirico #UmorismoNero #BookTokItalia #LibriDaLeggere #Ticino"
LIBRO = "«Vuoto a rendere» di D. Iasio: ebook su Amazon Kindle (anche in Kindle Unlimited) e copertina flessibile. Cercalo su Amazon."

PUNTATE = [
    # id, quando, file video, miniatura (ms), prima riga della didascalia, commento da fissare
    ("tsu01-sala-ulivo-sedie", "2026-11-24T21:05", "sala-ulivo-01-sedie", 3000,
     "Sala Ulivo, parte 1 di 13. Quaranta sedie, nove persone, un morto in anticipo di venti minuti.",
     "Sei su nove, pagate a ore. Chi sono gli altri tre lo scopriamo strada facendo."),
]


def main():
    d = json.loads(CAL.read_text(encoding="utf-8"))
    per_id = {p["id"]: p for p in d["post"]}
    for pid, quando, nome, ms, riga, commento in PUNTATE:
        voce = {"id": pid, "tipo": "reel", "quando": quando, "segmento": "TikTok · Serie Sala Ulivo (Vuoto a rendere, capitolo 1)",
                "video": f"social/video/{nome}.mp4", "miniatura_ms": ms, "piattaforme": ["tiktok"], "ia": True,
                "didascalia": f"{riga}\nIl primo capitolo di Vuoto a rendere, letto ad alta voce, una parte alla volta. Meglio in cuffia.\n\n{LIBRO}\n\n{TAG}",
                "commento": commento}
        if pid in per_id:
            per_id[pid].update(voce)
        else:
            d["post"].append(voce)
    CAL.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
