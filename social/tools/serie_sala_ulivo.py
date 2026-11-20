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
    ("tsu02-sala-ulivo-cane", "2026-11-27T21:05", "sala-ulivo-02-cane", 3000,
     "Sala Ulivo, parte 2 di 13. Nell’ultima foto il vecchio sorrideva a un cane. Il cane non era suo.",
     "Engagement anche al funerale. L'algoritmo non va mai in lutto."),
    ("tsu03-sala-ulivo-ventitre", "2026-12-01T21:05", "sala-ulivo-03-ventitre", 3000,
     "Sala Ulivo, parte 3 di 13. Aldo Soldati era morto da ventitré giorni. Se n'erano accorti per l'odore.",
     "A telefonare non è stato un figlio: è stato il gerente, dopo undici giorni di reclami. Ventitré giorni, zero visite."),
    ("tsu04-sala-ulivo-cose-semplici", "2026-12-04T21:05", "sala-ulivo-04-cose-semplici", 3000,
     "Sala Ulivo, parte 4 di 13. «Aldo amava le cose semplici.» Lo scrive il sistema quando il campo hobby è vuoto.",
     "Hobby: vuoto. Carattere: riservato, il valore predefinito. Nel vostro modulo, cosa ci finirebbe?"),
    ("tsu05-sala-ulivo-ottavio", "2026-12-08T21:05", "sala-ulivo-05-ottavio", 3000,
     "Sala Ulivo, parte 5 di 13. Ottavio piange a comando, con un occhio solo. Tariffa lacrime: otto franchi in più.",
     "Il sinistro, perché dalle file dietro si nota di più. Anche il dolore ha il suo lato buono per la telecamera."),
    ("tsu06-sala-ulivo-rotterdam", "2026-12-11T21:05", "sala-ulivo-06-rotterdam", 3000,
     "Sala Ulivo, parte 6 di 13. Spettatori connessi: uno. Località: Rotterdam. Davanti alla bara di suo padre, ma da dietro un vetro.",
     "Trentuno minuti di collegamento. In sala nove presenze pagate, a Rotterdam l'unico che c'era davvero."),
    ("tsu07-sala-ulivo-signora", "2026-12-15T21:05", "sala-ulivo-07-signora", 3000,
     "Sala Ulivo, parte 7 di 13. In ultima fila, fuori lista: una signora col cappotto di lana a ventisei gradi, che guarda lo schermo come una fattura.",
     "Non ha firmato il registro e non piange. In una sala dove piangere ha una tariffa, è lei quella fuori posto."),
    ("tsu08-sala-ulivo-fazzoletto", "2026-12-18T21:05", "sala-ulivo-08-fazzoletto", 3000,
     "Sala Ulivo, parte 8 di 13. La foto del cane, un no con la testa, una porta che si richiude senza rumore. Sulla sedia restò un fazzoletto.",
     "In Sala Ulivo ci si alza prima della fine una volta su duecento. Lei l'ha fatto, e ha lasciato qualcosa sulla sedia."),
    ("tsu09-sala-ulivo-fila", "2026-12-22T21:05", "sala-ulivo-09-fila", 3000,
     "Sala Ulivo, parte 9 di 13. In Ticino, all'uscita, si fa la fila e si stringono le mani. Quel giorno di parenti non ce n'erano.",
     "Sei comparse, uno stagista e un gerente spinto in testa alla fila. Alla terza mano gli tremò il labbro: non era commozione."),
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
