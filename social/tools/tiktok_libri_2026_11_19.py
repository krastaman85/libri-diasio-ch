"""TikTok @d.iasio.libri: calendario a 4 video la settimana (decisione di Davide del 19/11/2026).
Mercoledì e domenica alle 21:05 i video già pronti (ASMR e voce narrante); martedì e venerdì la serie «Sala Ulivo»
(aggiunta a parte quando le puntate sono pronte). Idempotente: si può rilanciare."""
import json
from pathlib import Path

CAL = Path(__file__).resolve().parents[1] / "calendar.json"
TAG = "#RomanzoSatirico #UmorismoNero #BookTokItalia #LibriDaLeggere #Ticino"
TAG_A = "#NoirItaliano #BookTokItalia #LetteraturaNoir #LibriDaLeggere #Ticino"
VUOTO = "«Vuoto a rendere» di D. Iasio: ebook su Amazon Kindle (anche in Kindle Unlimited) e copertina flessibile. Cercalo su Amazon."
ARIT = "«L’Aritmetica del Consenso» di D. Iasio: ebook su Amazon Kindle, anche in Kindle Unlimited. Cercalo su Amazon."

SPOSTA = {  # ASMR già in calendario: anticipati su TikTok (su Instagram restano alle loro date)
    "tasmr4-vuoto-diffusore": "2026-11-20T21:05",
    "tasmr5-vuoto-timbro": "2026-11-25T21:05",
    "tasmr3-aritmetica-lago": "2026-12-02T21:05",
}
NUOVI = [
    ("tvn3-vuoto-puntualita", "2026-11-22T21:05", "social/video/vn3-vuoto-puntualita.mp4", 3500,
     "La prima riga di un romanzo satirico, letta ad alta voce: un morto in anticipo di venti minuti, quaranta sedie, nove persone.\nÈ l’inizio di Vuoto a rendere. Meglio in cuffia.\n\n" + VUOTO + "\n\n" + TAG),
    ("tvn1-vuoto-wifi", "2026-12-06T21:05", "social/video/vn1-vuoto-wifi.mp4", 3500,
     "Il commiato laico, pacchetto base: senza ostie e con il wifi. Letto ad alta voce, da Vuoto a rendere.\nMeglio in cuffia.\n\n" + VUOTO + "\n\n" + TAG),
    ("tvn4-aritmetica-ministro", "2026-12-13T21:05", "social/video/vn4-aritmetica-ministro.mp4", 3500,
     "«La vecchia mi ha appena chiesto quanto costava un ministro, ai suoi tempi…» La prima riga de L’Aritmetica del Consenso, letta ad alta voce.\nMeglio in cuffia.\n\n" + ARIT + "\n\n" + TAG_A),
]

def main():
    d = json.loads(CAL.read_text(encoding="utf-8"))
    per_id = {p["id"]: p for p in d["post"]}
    for k, quando in SPOSTA.items():
        per_id[k]["quando"] = quando
    for pid, quando, video, ms, testo in NUOVI:
        voce = {"id": pid, "tipo": "reel", "quando": quando, "segmento": "TikTok · Voce narrante", "video": video,
                "miniatura_ms": ms, "piattaforme": ["tiktok"], "ia": True, "didascalia": testo}
        if pid in per_id:
            per_id[pid].update(voce)
        else:
            d["post"].append(voce)
    CAL.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
