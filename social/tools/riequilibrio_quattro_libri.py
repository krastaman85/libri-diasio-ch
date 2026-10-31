# Riequilibrio del calendario sui quattro romanzi (31/10/2026, decisioni dell'utente: rifacimento completo, firma una sola volta,
# post per L'Aritmetica e per Vuoto a dicembre). Da lanciare una volta sola, dopo aver reso le immagini:
#   python3 social/tools/riequilibrio_quattro_libri.py
# Cosa fa:
#  1. toglie dal calendario i 21 post di posts.py ancora da pubblicare (grafiche vecchie, contenuti già coperti da Reel e caroselli)
#     e n12 (il cane del comitato è già nel Reel r17);
#  2. riscrive le didascalie dei post «per tutti» (n30, c04, c05, c06, d07, d09) con i quattro romanzi;
#  3. aggiunge i post nuovi di dicembre (dicembre_4libri.py) e ridistribuisce dal 4/11 al 31/12 tutti i post rifatti,
#     al massimo due al giorno su IG/FB (una uscita per fascia), negli orari delle finestre di cron-job.org con minuti diversi;
#  4. toglie "sospeso" ai post rifatti. Le feste (c06 20/12, s12 21/12, d07 24/12, d09 31/12) restano nel loro giorno.
import hashlib, json, random, re, sys
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOCIAL = HERE.parent
sys.path.insert(0, str(HERE))
import carousel  # noqa: E402

# giorno (lunedì=0) -> fasce (ora, primo avvio, ultimo avvio), come in test_calendario.py
FINESTRE = {0: [(12, 2, 57), (18, 7, 52)], 1: [(12, 2, 57), (19, 17, 57)], 2: [(12, 2, 57), (19, 17, 57)],
            3: [(12, 12, 52), (19, 7, 52)], 4: [(12, 2, 57), (18, 2, 42)], 5: [(12, 2, 47), (17, 2, 47)],
            6: [(12, 2, 57), (20, 2, 47)]}
DAL, AL = date(2026, 11, 4), date(2026, 12, 31)
TOGLI = re.compile(r"^(0[3-9]|1\d|2[0-4])-|^n12-oblio-cane$")
FESTE = {"c06-natale-albero": date(2026, 12, 20), "s12-feste": date(2026, 12, 21), "d07-buone-feste": date(2026, 12, 24),
         "d09-buon-anno": date(2026, 12, 31)}
VICINO = {"n30-kindle-due-romanzi": date(2026, 11, 6), "c05-bug-o-oblio": date(2026, 12, 3), "c04-tre-passi": date(2026, 12, 27)}

AMZ = {"bug": "https://www.amazon.it/dp/B0HLN2VSJP", "oblio": "https://www.amazon.it/dp/B0HLMKWJZ5",
       "aritmetica": "https://www.amazon.it/dp/B0HM3Y19B6", "vuoto": "https://www.amazon.it/dp/B0HM4HFK34"}
QUATTRO_FB = ("I quattro romanzi su Amazon Kindle, inclusi in Kindle Unlimited:\n"
              f"Vuoto a rendere: {AMZ['vuoto']}\nL’Aritmetica del Consenso: {AMZ['aritmetica']}\n"
              f"Il Bug della Trasparenza: {AMZ['bug']}\nL’Economia dell’Oblio: {AMZ['oblio']}")
QUATTRO_IG = "I quattro romanzi sono su Amazon Kindle (link in bio), inclusi in Kindle Unlimited."
TESTI = {   # (apertura IG/FB, riga sul sito) — il resto della didascalia: riga Kindle + hashtag già presenti
 "n30-kindle-due-romanzi": ("Quattro romanzi, un posto dove trovarli interi: Amazon Kindle.\nUn romanzo satirico, un noir dinastico, un noir sociale, un thriller psicologico.",
                            "L’inizio di ognuno è gratis, in PDF o EPUB, senza iscrizione"),
 "c05-bug-o-oblio": ("Quattro romanzi, quattro porte: un listino del lutto, una famiglia che compra il silenzio, un condominio che dice la verità, un dolore che si vende. Quale apriresti per primo? Dimmelo nei commenti: leggo tutto.",
                     "L’inizio di ogni romanzo è gratis in PDF ed EPUB, senza iscrizione"),
 "c06-natale-albero": ("Se cerchi qualcosa da leggere nelle sere di festa: l’inizio di ognuno dei quattro romanzi è gratis, in PDF o EPUB (va bene anche su Kindle). Nessuna iscrizione.\nSe conosci qualcuno che ama noir, thriller o satira, basta girargli il link.",
                       "Tutti gli inizi gratis"),
 "d07-buone-feste": ("Buone feste a chi legge, a chi commenta e a chi è arrivato da poco. Se avete una sera libera, l’inizio dei quattro romanzi vi aspetta: gratis, in PDF o EPUB, senza iscrizione.",
                     "Gli inizi gratis"),
 "c04-tre-passi": ("Come leggere l’inizio gratis in tre passi, per chi arriva adesso: si scarica, si legge, e se piace si decide se continuare.\nVale per tutti e quattro i romanzi: PDF o EPUB, senza iscrizione.",
                   "Gli inizi gratis"),
 "d09-buon-anno": ("L’ultimo giorno dell’anno, un solo invito: se vuoi sapere quando esce la prossima storia, iscriviti alla newsletter. Una mail alla volta, niente rumore. E l’inizio dei quattro romanzi resta gratis.",
                   "Newsletter e inizi gratis"),
}


# Reel r06-r23 rifatti (motore «Libri reel» sul PC): copertina del Reel = frase intera, firma + 0,8 s
MINIATURA = {'r06-oblio-igiene': 8700, 'r07-bug-attivare': 9600, 'r08-oblio-listino': 9100, 'r11-oblio-benissimo': 9200, 'r12-bug-vicino': 8000, 'r13-oblio-furto': 8900, 'r14-bug-amministrazione': 9500, 'r15-oblio-firma': 9100, 'r16-bug-silenzio': 9600, 'r17-oblio-comitato': 8800, 'r18-bug-note-rilascio': 8000, 'r19-oblio-brescia': 9000, 'r20-bug-acclamazione': 9500, 'r21-oblio-gratis': 8800, 'r22-bug-rettifica': 9600, 'r23-oblio-cara': 9400}


def tags(t):
    return re.search(r"((?:#\w+[ \t]*)+)\s*$", t).group(1).strip()


def riscrivi(p):
    apre, sito = TESTI[p["id"]]
    p["didascalia"] = f"{apre}\n{sito}: link in bio.\n{QUATTRO_IG}\n\n{tags(p['didascalia'])}"
    p["didascalia_fb"] = f"{apre}\n{sito}: https://libri.diasio.ch/\n\n{QUATTRO_FB}\n\n{tags(p['didascalia_fb'])}"
    if p["id"] == "n30-kindle-due-romanzi":
        p["alt"] = ("Locandina su fondo scuro con le copertine dei quattro romanzi, Vuoto a rendere, L’Aritmetica del Consenso, Il Bug della Trasparenza e "
                    "L’Economia dell’Oblio: «Quattro romanzi. Amazon Kindle.» Pulsante «Disponibili su Amazon Kindle»; l’inizio di ognuno è gratis su libri.diasio.ch.")
    if p["id"] == "c05-bug-o-oblio":
        p["alt"] = ("Carosello di sette slide: la domanda «Quale comincerai per primo?», le copertine dei quattro romanzi con una domanda ciascuna, "
                    "una citazione da ognuno e l’invito a leggerne l’inizio gratis.")
        p["immagini"] = [f"social/img/carousel/c05-bug-o-oblio/{i:02d}.jpg" for i in range(1, 8)]
    if p["id"] == "c06-natale-albero":
        p["alt"] = p["alt"].replace("le copertine dei due romanzi", "le copertine dei quattro romanzi").replace("la Puntata 1 di entrambi", "l’inizio di ognuno")
    if p["id"] == "d07-buone-feste":
        p["alt"] = p["alt"].replace("La Puntata 1 è gratis", "L’inizio è gratis")


def fasce_libere(occupate):
    d = DAL
    while d <= AL:
        for ora, primo, ultimo in FINESTRE[d.weekday()]:
            if (d, ora) not in occupate:
                yield d, ora
        d += timedelta(days=1)


def minuto(pid, d, ora, usati):
    ora_, primo, ultimo = next(f for f in FINESTRE[d.weekday()] if f[0] == ora)
    r = random.Random(int(hashlib.sha256((pid + d.isoformat()).encode()).hexdigest(), 16))
    scelte = [m for m in range(max(0, primo - 4) + 1, ultimo - 2) if m not in usati.get((d.weekday(), ora), set())]
    return r.choice(scelte)


def main():
    p = SOCIAL / "calendar.json"
    cal = json.loads(p.read_text(encoding="utf-8"))
    pub = json.loads((SOCIAL / "published.json").read_text(encoding="utf-8"))["pubblicati"]
    tolti = [x["id"] for x in cal["post"] if x.get("sospeso") and TOGLI.match(x["id"]) and x["id"] not in pub]
    cal["post"] = [x for x in cal["post"] if x["id"] not in tolti]
    for x in cal["post"]:
        if x["id"] in TESTI:
            riscrivi(x)
        if x["id"] in MINIATURA:
            x["miniatura_ms"] = MINIATURA[x["id"]]
    # voci nuove
    nuovi = [it for it in carousel.load() if it["id"].startswith(("x0", "sx"))]
    have = {x["id"] for x in cal["post"]}
    for it in nuovi:
        if it["id"] in have:
            continue
        if it.get("story"):
            e = {"id": it["id"], "tipo": "storia", "quando": "", "segmento": it["seg"], "immagine": f"social/img/story/{it['id']}.jpg"}
        else:
            n = len(it["slides"])
            e = {"id": it["id"], "quando": "", "segmento": it["seg"]}
            if n > 1:
                e["tipo"] = "carosello"
                e["immagini"] = [f"social/img/nuovi/{it['id']}-{i:02d}.jpg" for i in range(1, n + 1)]
            else:
                e["immagine"] = f"social/img/nuovi/{it['id']}.jpg"
            e.update({"alt": it["alt"], "didascalia": it["caption"], "didascalia_fb": it["caption_fb"]})
        e["sospeso"] = True
        cal["post"].append(e)
    # da sistemare: tutti i sospesi non pubblicati
    mobili = [x for x in cal["post"] if x.get("sospeso") and x["id"] not in pub]
    fissi = [x for x in cal["post"] if x not in mobili and x["id"] not in pub and not re.match(r"^q\d\d", x["id"])
             and x.get("piattaforme") != ["tiktok"]]
    occupate = set()
    usati = {}
    for x in fissi:
        d = datetime.fromisoformat(x["quando"])
        occupate.add((d.date(), d.hour))
        usati.setdefault((d.weekday(), d.hour), set()).add(d.minute)
    # ordine: Bug e Oblio alternati (nell'ordine di prima), Aritmetica e Vuoto inseriti a dicembre, post «per tutti» vicino alla data scelta
    feste = {x["id"]: x for x in mobili if x["id"] in FESTE}
    vicini = {x["id"]: x for x in mobili if x["id"] in VICINO}
    nuove = [x for x in mobili if x["id"].startswith(("x0", "sx"))]
    bo = sorted([x for x in mobili if x["id"] not in feste and x["id"] not in vicini and x not in nuove], key=lambda x: x["quando"] or "9")
    bug = [x for x in bo if "bug" in x["id"]]
    obl = [x for x in bo if x not in bug]
    alt = []
    while bug or obl:
        for q in (bug, obl) if len(bug) >= len(obl) else (obl, bug):
            if q:
                alt.append(q.pop(0))
    # nuove: alternate Aritmetica / Vuoto
    ari = [x for x in nuove if "aritmetica" in x["id"]]
    vuo = [x for x in nuove if "vuoto" in x["id"]]
    nuove = [y for pair in zip(ari, vuo) for y in pair]
    # fasce
    for pid, d in FESTE.items():
        if pid in feste:
            ora = FINESTRE[d.weekday()][1][0] if pid != "d07-buone-feste" else FINESTRE[d.weekday()][0][0]
            if (d, ora) in occupate:
                ora = [f[0] for f in FINESTRE[d.weekday()] if f[0] != ora][0]
            feste[pid]["_slot"] = (d, ora)
            occupate.add((d, ora))
    libere = list(fasce_libere(occupate))
    # post «per tutti»: prima fascia libera dal giorno scelto
    for pid, d in VICINO.items():
        s = next(s for s in libere if s[0] >= d)
        vicini[pid]["_slot"] = s
        libere.remove(s)
    # Aritmetica e Vuoto: dicembre, ogni tre giorni circa, nella fascia serale quando c'è
    dic = [s for s in libere if s[0] >= date(2026, 12, 1)]
    passo = len(dic) / len(nuove)
    for i, x in enumerate(nuove):
        s = dic[int(i * passo + passo / 2)]
        x["_slot"] = s
        libere.remove(s)
    # Bug/Oblio: distribuiti in modo uniforme sulle fasce rimaste
    passo = len(libere) / len(alt)
    if passo < 1:
        raise SystemExit(f"fasce insufficienti: {len(libere)} per {len(alt)} post")
    scelte = [libere[int(i * passo)] for i in range(len(alt))]
    for x, s in zip(alt, scelte):
        x["_slot"] = s
    # minuti (in ordine di data, per non ripetere il minuto della settimana prima nella stessa fascia)
    for x in sorted(mobili, key=lambda x: x["_slot"]):
        d, ora = x.pop("_slot")
        m = minuto(x["id"], d, ora, usati)
        usati.setdefault((d.weekday(), ora), set()).add(m)
        x["quando"] = f"{d.isoformat()}T{ora:02d}:{m:02d}"
        x.pop("sospeso", None)
    cal["post"].sort(key=lambda x: x["quando"])
    p.write_text(json.dumps(cal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("tolti:", len(tolti), " ridistribuiti:", len(mobili))
    for x in sorted(mobili, key=lambda x: x["quando"]):
        print(x["quando"], x["id"])


if __name__ == "__main__":
    main()
