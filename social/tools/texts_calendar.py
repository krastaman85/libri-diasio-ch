"""Aggiunge a ../calendar.json i post di solo testo per la Pagina Facebook (senza duplicare).
Uso, da social/tools: python texts_calendar.py. Facebook mostra da solo l'anteprima del link."""
import json
from pathlib import Path

SOCIAL = Path(__file__).resolve().parent.parent
SITE = "https://libri.diasio.ch/"
# (id, quando, segmento, testo, link)
TESTI = [
 ("t01-bug-condominio", "2026-10-09T18:00", "Testo · Vita di condominio", "Se l’app del tuo condominio dicesse la verità, chi sarebbe il primo a finire nei guai? Nel romanzo è successo a un presidente d’assemblea.\nLa Puntata 1 de Il Bug della Trasparenza è gratis: PDF ed EPUB, senza iscrizione.", SITE + "bug/"),
 ("t02-oblio-ricordo", "2026-10-23T18:00", "Testo · Community", "Se potessi vendere un ricordo, quale sarebbe? In L’Economia dell’Oblio un lutto pulito vale quattromila euro. Dimmelo nei commenti.\nLa Puntata 1 è gratis, in PDF o EPUB.", SITE + "oblio/"),
 ("t03-bug-regolamento", "2026-11-06T18:00", "Testo · Condominio + privacy", "«Il regolamento di condominio la definiva strumento indispensabile alla vita comunitaria. Nessuno l’aveva letto fino in fondo. Nadia nemmeno.»\nE tu, li leggi i regolamenti? La Puntata 1 è gratis.", SITE + "bug/"),
 ("t04-oblio-listino", "2026-11-20T18:00", "Testo · Satira", "Quanto vale un dolore? Un lutto pulito quattromila euro, una vergogna novecento, una cotta non ricambiata sessanta. È il listino di uno studio di estrazioni, in L’Economia dell’Oblio.\nLa Puntata 1 è gratis.", SITE + "oblio/"),
 ("t05-newsletter", "2026-12-04T18:00", "Testo · Newsletter", "Una mail quando esce la prossima storia: solo un avviso e qualche estratto, niente rumore.\nIscriviti alla newsletter dal sito; la Puntata 1 di entrambi i romanzi è gratis.", SITE),
 ("t06-feste", "2026-12-18T18:00", "Testo · Feste", "Per le sere di festa: due romanzi a puntate, e la Puntata 1 di entrambi è gratis, in PDF o EPUB (va bene anche su Kindle). Nessuna iscrizione.", SITE),
]


def main():
    p = SOCIAL / "calendar.json"
    cal = json.loads(p.read_text(encoding="utf-8"))
    have = {x["id"] for x in cal["post"]}
    for pid, when, seg, text, link in TESTI:
        if pid in have:
            continue
        cal["post"].append({"id": pid, "tipo": "testo", "piattaforme": ["facebook"], "quando": when, "segmento": seg,
                            "didascalia": text, "link": link})
        print("+", pid, when)
    cal["post"].sort(key=lambda x: x["quando"])
    p.write_text(json.dumps(cal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
