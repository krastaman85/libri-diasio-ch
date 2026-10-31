"""Rubrica «Citazioni D. Iasio»: variabili dei Reel e voci del calendario.

Legge social/citazioni/citazioni.json e, nell'ordine del file, assegna una sera a ogni frase dal giorno «inizio»:
Reel alle 23:10 (Instagram e Facebook) e, nella stessa esecuzione, la Storia della stessa frase (campo "poi"
del Reel); l'orario 23:13 della Storia serve solo da ripiego se il Reel non esce.

Uso (dalla radice del repo):
  python3 social/tools/citazioni.py --vars        # scrive social/reels-src/vars/qNN-*.json
  python3 social/tools/citazioni.py --calendar    # aggiunge o aggiorna le voci qNN nel calendario (non tocca le pubblicate)
Render: social/reels-src/render-citazioni.sh (vedi README dei Reel).
"""
import json, sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATI = ROOT / "social" / "citazioni" / "citazioni.json"
CAL = ROOT / "social" / "calendar.json"
PUB = ROOT / "social" / "published.json"
VARS = ROOT / "social" / "reels-src" / "vars"

LIBRI = {
    "bug": ("Il Bug della Trasparenza", "bug", "B0HLN2VSJP", ["#NoirItaliano", "#LetteraturaNoir"]),
    "oblio": ("L’Economia dell’Oblio", "oblio", "B0HLMKWJZ5", ["#ThrillerPsicologico", "#ThrillerItaliano"]),
    "aritmetica": ("L’Aritmetica del Consenso", "aritmetica", "B0HM3Y19B6", ["#NoirItaliano", "#RomanzoNoir"]),
    "vuoto": ("Vuoto a rendere", "vuoto", "B0HM4HFK34", ["#RomanzoSatirico", "#CommediaNera"]),
}
COMMUNITY = ["#ScrittoriItaliani", "#BookstagramItalia", "#IoLeggo", "#ConsigliDiLettura", "#LibriDaLeggere", "#ScrittoriEmergenti"]
GEO = ["#Ticino", "#SvizzeraItaliana", "#ScrittoriSvizzeri", "#BookstagramSvizzera", "#LeggereInSvizzera", "#CulturaTicino"]
TONO_IRONICO = ["#UmorismoNero", "#Ironia", "#Satira"]
TONO_SERIO = ["#AltaTensione", "#LibriThriller", "#GialloItaliano"]


def carica():
    return json.loads(DATI.read_text(encoding="utf-8"))


def voci(d):
    """(numero, id, data, citazione) nell'ordine del file."""
    g0 = date.fromisoformat(d["inizio"])
    for i, c in enumerate(d["citazioni"]):
        n = i + 1
        yield n, f"q{n:02d}-{c['slug']}", g0 + timedelta(days=i), c


def tag(n, c, fb):
    titolo, _, _, genere = LIBRI[c["libro"]]
    tono = TONO_IRONICO if c["ironica"] else TONO_SERIO
    # Vuoto è satirico per genere: sulle sue frasi non ironiche niente tag di satira (regola dell'utente).
    if c["libro"] == "vuoto" and not c["ironica"]:
        genere = ["#NoirItaliano", "#LetteraturaNoir"]
    if not fb:
        return [genere[0], tono[n % len(tono)], COMMUNITY[n % len(COMMUNITY)], COMMUNITY[(n + 3) % len(COMMUNITY)], GEO[n % len(GEO)]]
    out = genere + [tono[n % len(tono)], tono[(n + 1) % len(tono)]] + COMMUNITY[:3] + [COMMUNITY[3 + n % 3]] + [GEO[n % len(GEO)], GEO[(n + 1) % len(GEO)]]
    seen, res = set(), []
    for t in out:
        if t.lower() not in seen:
            seen.add(t.lower()); res.append(t)
    return res


def didascalia(n, c, fb):
    # Dal 31/10/2026 (scelta dell'autore) le frasi delle 23:10 sono pensieri a sé, non pubblicità ai libri:
    # niente titolo, link o riga Kindle; solo la frase, la firma e l'appuntamento.
    righe = [f"«{c['testo']}»", "— D. Iasio", "", "Una frase ogni sera alle 23:10."]
    return "\n".join(righe) + "\n\n" + " ".join(tag(n, c, fb))


def scrivi_vars(d):
    for n, pid, _, c in voci(d):
        v = {"quote": c["testo"], "emphasis": c["enfasi"], "num": f"N. {n:02d}"}
        (VARS / f"{pid}.json").write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("variabili scritte")


def calendario(d):
    raw = CAL.read_bytes()
    crlf = b"\r\n" in raw
    cal = json.loads(raw.decode("utf-8"))
    pub = json.loads(PUB.read_text(encoding="utf-8"))["pubblicati"]
    nuove = []
    for n, pid, g, c in voci(d):
        sid = pid.replace("-", "s-", 1)
        reel = {"id": pid, "tipo": "reel", "quando": f"{g.isoformat()}T{d['ora_reel']}",
                "segmento": "Reel · Citazioni D. Iasio", "video": f"social/video/{pid}.mp4", "miniatura_ms": 12500,
                "didascalia": didascalia(n, c, False), "didascalia_fb": didascalia(n, c, True), "poi": sid}
        storia = {"id": sid, "tipo": "storia", "quando": f"{g.isoformat()}T{d['ora_storia']}",
                  "segmento": "Storia · Citazioni D. Iasio", "immagine": f"social/img/story/{pid}.jpg"}
        nuove += [reel, storia]
    ids = {p["id"] for p in nuove}
    tenute = [p for p in cal["post"] if p["id"] not in ids or p["id"] in pub]
    gia = {p["id"] for p in tenute}
    cal["post"] = sorted(tenute + [p for p in nuove if p["id"] not in gia], key=lambda x: x["quando"])
    txt = json.dumps(cal, indent=2, ensure_ascii=False) + "\n"
    CAL.write_bytes((txt.replace("\n", "\r\n") if crlf else txt).encode("utf-8"))
    print(f"calendario: {len(nuove)} voci della rubrica, {len(cal['post'])} in tutto")


if __name__ == "__main__":
    d = carica()
    if "--vars" in sys.argv:
        scrivi_vars(d)
    if "--calendar" in sys.argv:
        calendario(d)
