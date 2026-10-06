# 10 post «è uscito» de «L'Aritmetica del Consenso» (online su Amazon Kindle dal 6/10/2026, ASIN B0HM3Y19B6), rielaborati il 6/10/2026 sera
# senza conto alla rovescia: date nuove, riga finale con il link Amazon. Le citazioni sono testuali dalla Puntata 1 (testo approvato, in Drive). *parola* = parola in ottone.
# Letto da carousel.py (load) con exec: niente import relativi. `python carousel.py` rende le immagini in social/img/nuovi/
# (le Storie in social/img/story/), `python carousel.py --calendar` aggiunge le voci a calendar.json.
import hashlib
import random

SITO_A = "https://libri.diasio.ch/aritmetica/"
AMAZON = "https://www.amazon.it/dp/B0HM3Y19B6"
NEWS = "https://libri.diasio.ch/#iscrizione"


def _rng(pid, kind):
    return random.Random(int(hashlib.sha256((pid + kind).encode()).hexdigest(), 16))


# Vocabolario dell'utente: noir (genere) + community + geografia; ironia solo sui post ironici.
GENERE = ["#NoirItaliano", "#RomanzoNoir", "#LetteraturaNoir", "#ThrillerItaliano", "#AltaTensione", "#GialloItaliano"]
POPOLARI = ["#NoirItaliano", "#RomanzoNoir"]
TONO = ["#Ironia", "#UmorismoNero", "#Satira", "#CommediaNera"]
COMMUNITY = ["#BookstagramItalia", "#ConsigliDiLettura", "#LibriDaLeggere"]
SPECIALI = ["#IoLeggo", "#ScrittoriItaliani", "#ScrittoriEmergenti", "#EditoriaItaliana"]
GEO = ["#Ticino", "#SvizzeraItaliana", "#ScrittoriSvizzeri", "#LeggereInSvizzera", "#CulturaTicino", "#BookstagramSvizzera"]


def tag_ig(pid, ironico=False):
    r = _rng(pid, "ig")
    primo = r.choice(POPOLARI)
    secondo = r.choice(TONO) if ironico else r.choice([g for g in GENERE if g != primo])
    return " ".join([primo, secondo, r.choice(COMMUNITY), r.choice(SPECIALI), r.choice(GEO)])


def tag_fb(pid, ironico=False):
    r = _rng(pid, "fb")
    n_gen, n_ton, n_com, n_geo = (3, 2, 2, 2) if ironico else (4, 0, 2, 3)
    t = r.sample(GENERE, n_gen) + (r.sample(TONO, n_ton) if n_ton else []) + r.sample(COMMUNITY, n_com) \
        + [r.choice(SPECIALI)] + r.sample(GEO, n_geo)
    return " ".join(t)


# Righe finali: il libro è online (link Amazon su Facebook; su Instagram «link in bio»).
POST_IG = "Il romanzo completo, in sei puntate, è su Amazon Kindle (link in bio). La Puntata 1 è gratis, in PDF o EPUB, senza iscrizione."
POST_FB = f"Il romanzo completo, in sei puntate, è su Amazon Kindle: {AMAZON}\nLa Puntata 1 è gratis, in PDF o EPUB, senza iscrizione: {SITO_A}"
KB = "Su Amazon Kindle"


def A(id, when, seg, slides, body, alt, ironico=False):
    cap = body + "\n" + POST_IG + "\n\n" + tag_ig(id, ironico)
    cfb = body + "\n\n" + POST_FB + "\n\n" + tag_fb(id, ironico)
    return dict(id=id, when=when, book="aritmetica", seg=seg, flat=True, theme="green", slides=slides,
                caption=cap, caption_fb=cfb, alt=alt, ironico=ironico)


ITEMS = [

 A("a11-aritmetica-da-oggi", "2026-10-08T12:24", "Lancio · È uscito (locandina)",
   [dict(k="cta", books=["aritmetica"], text="Appena *uscito*", button="Su Amazon Kindle", line="Puntata 1 gratis · <b>libri.diasio.ch</b>")],
   "È uscito L’Aritmetica del Consenso, noir dinastico di D. Iasio in sei puntate, tutte in un unico ebook.\nUn ghostwriter, una famiglia che sta per diventare legalmente eterna e una vecchia che ha cominciato a ricordare tutto.",
   "Locandina su fondo verde bottiglia con la copertina de L’Aritmetica del Consenso (mani di una vecchia che sbucciano un mandarino): «Appena uscito», pulsante «Su Amazon Kindle», Puntata 1 gratis su libri.diasio.ch."),

 A("a13-aritmetica-incipit", "2026-10-11T20:23", "Prime righe (carosello)",
   [dict(k="quote", text="«La vecchia mi ha appena chiesto quanto costava un ministro, ai suoi tempi, e io le ho risposto la verità: meno di quanto costa oggi un buon avvocato.»", who="L’Aritmetica del Consenso · Puntata 1", foot="Puntata 1 gratis · libri.diasio.ch"),
    dict(k="quote", text="«Sono le dieci e quaranta di un mercoledì. Siamo in una sala da pranzo in cui potrebbe mangiare un reggimento e in cui non mangia mai nessuno.»", who="L’Aritmetica del Consenso · Puntata 1", foot="Puntata 1 gratis · libri.diasio.ch"),
    dict(k="quote", text="«Faccio il ghostwriter. Scrivo le vite degli altri e poi sparisco, come l'idraulico: nessuno ringrazia l'idraulico, si ringrazia il rubinetto.»", who="L’Aritmetica del Consenso · Puntata 1", foot="Puntata 1 gratis · libri.diasio.ch"),
    dict(k="quote", text="«Io ho il registratore acceso nella tasca della giacca. Non per coraggio, sia chiaro. Per mestiere.»", who="L’Aritmetica del Consenso · Puntata 1", foot="Puntata 1 gratis · libri.diasio.ch"),
    dict(k="cta", books=["aritmetica"], text="Continua con la Puntata *1*", button="Leggi la Puntata 1 gratis", line="PDF ed EPUB · <b>libri.diasio.ch</b>")],
   "L’Aritmetica del Consenso è uscito: ecco le prime righe, una alla volta.\nUn ghostwriter, una vecchia che ricorda tutto e un registratore in tasca.",
   "Carosello di cinque slide su fondo verde bottiglia con le prime righe de L’Aritmetica del Consenso: la domanda sul costo di un ministro; la sala da pranzo; il ghostwriter e l’idraulico; il registratore acceso in tasca; invito a leggere la Puntata 1 gratis."),

 A("a03-aritmetica-direttori", "2026-10-13T19:38", "Citazione ironica · È uscito (grafica)",
   [dict(k="quote", text="«I direttori capiscono sempre, ragioniere, è per questo che li scelgono.»", who="L’Aritmetica del Consenso · Puntata 1", kindle=KB)],
   "«I direttori capiscono sempre, ragioniere, è per questo che li scelgono.»\nL’Aritmetica del Consenso, noir dinastico di D. Iasio, è uscito.",
   "Frase su fondo verde bottiglia: «I direttori capiscono sempre, ragioniere, è per questo che li scelgono.» L’Aritmetica del Consenso, Puntata 1. Fascia: «Su Amazon Kindle».", ironico=True),

 A("a04-aritmetica-silenzio", "2026-10-14T12:31", "Domanda ai lettori · È uscito (grafica)",
   [dict(k="quote", text="«Il compenso era indecente. Lo capisci da come nessuno lo nomina.»", who="L’Aritmetica del Consenso · Puntata 1",
         sub="E tu: quanto costa il tuo *silenzio*?", kindle=KB)],
   "«Il compenso era indecente. Lo capisci da come nessuno lo nomina.»\nE tu: quanto costa il tuo silenzio? Rispondi nei commenti.\nL’Aritmetica del Consenso è uscito.",
   "Frase su fondo verde bottiglia: «Il compenso era indecente. Lo capisci da come nessuno lo nomina.» Sotto, la domanda «E tu: quanto costa il tuo silenzio?». Fascia: «Su Amazon Kindle»."),

 A("a05-aritmetica-dopo", "2026-10-15T19:26", "Citazione · È uscito (grafica)",
   [dict(k="quote", text="«Ma noi lavoriamo sempre dopo.»", who="L’Aritmetica del Consenso · Puntata 1", kindle=KB)],
   "«Ma noi lavoriamo sempre dopo.»\nL’Aritmetica del Consenso, di D. Iasio, è uscito.",
   "Frase su fondo verde bottiglia: «Ma noi lavoriamo sempre dopo.» L’Aritmetica del Consenso, Puntata 1. Fascia: «Su Amazon Kindle»."),

 A("a06-aritmetica-posta", "2026-10-17T12:38", "La «posta» · È uscito (grafica in stile registro)",
   [dict(k="doc", kick="L’Aritmetica del Consenso", name="REGISTRATORE · ACCESO",
         lines=["Dodici milioni di lire, in contanti, nel settantaquattro.", "Per il sottosegretario.",
                "Non per lui: per la sua segretaria, che era quella che decideva."], kindle=KB)],
   "Dodici milioni di lire, in contanti, nel settantaquattro. Per il sottosegretario. Non per lui: per la sua segretaria, che era quella che decideva.\nÈ la «posta» che la signora detta e il registratore conserva. L’Aritmetica del Consenso è uscito.",
   "Finto registro su fondo verde bottiglia, «Registratore · acceso»: «Dodici milioni di lire, in contanti, nel settantaquattro. Per il sottosegretario. Non per lui: per la sua segretaria, che era quella che decideva.» Fascia: «Su Amazon Kindle»."),

 A("a07-aritmetica-ci-penso", "2026-10-18T20:36", "Domanda ai lettori (tono ironico) · È uscito (grafica)",
   [dict(k="quote", text="«Brindare a un «ci penso» non è una cosa che si faccia, nelle famiglie normali.»", who="L’Aritmetica del Consenso · Puntata 1",
         sub="E tu, quando hai detto «ci penso» per non dire *no*?", kindle=KB)],
   "«Brindare a un «ci penso» non è una cosa che si faccia, nelle famiglie normali.»\nE tu, quando hai detto «ci penso» per non dire no? Rispondi nei commenti.\nL’Aritmetica del Consenso è uscito.",
   "Frase su fondo verde bottiglia: «Brindare a un «ci penso» non è una cosa che si faccia, nelle famiglie normali.» Sotto, la domanda «E tu, quando hai detto «ci penso» per non dire no?». Fascia: «Su Amazon Kindle».", ironico=True),

 A("a09-aritmetica-troverai", "2026-10-20T19:29", "Cosa troverai · È uscito (carosello)",
   [dict(k="step", kick="L’Aritmetica del Consenso", n="1", title="Una vecchia che ricorda tutto", text="Da tre mesi ha smesso di ricordare le cose in ordine. Ha cominciato a ricordarle *tutte*."),
    dict(k="step", kick="L’Aritmetica del Consenso", n="2", title="Un mestiere da invisibile", text="Scrive le vite degli altri e poi sparisce, come l’idraulico. Il compenso è *indecente*."),
    dict(k="step", kick="L’Aritmetica del Consenso", n="3", title="Una famiglia gentile", text="Nessuno alza la voce e nessuno controlla le tasche di nessuno. Tutto si spiega con la buona *educazione*."),
    dict(k="hook", kick="È uscito", text="Su *Kindle*", sub="Puntata 1 gratis: link in bio.", kindle=KB)],
   "Una vecchia che ricorda tutto, un mestiere da invisibile, una famiglia gentile.\nL’Aritmetica del Consenso, noir dinastico di D. Iasio, è uscito.",
   "Carosello di quattro slide su fondo verde bottiglia: 1 «Una vecchia che ricorda tutto»; 2 «Un mestiere da invisibile»; 3 «Una famiglia gentile»; 4 «È uscito, su Kindle». L’Aritmetica del Consenso."),

 A("a10-aritmetica-listino", "2026-10-22T19:44", "Citazione · È uscito (grafica)",
   [dict(k="quote", text="«Era il suo listino.»", who="L’Aritmetica del Consenso · Puntata 1", kindle=KB)],
   "«Era il suo listino.»\nL’Aritmetica del Consenso è uscito.",
   "Frase su fondo verde bottiglia: «Era il suo listino.» L’Aritmetica del Consenso, Puntata 1. Fascia: «Su Amazon Kindle»."),
]

# Post di solo testo per la Pagina Facebook (letti da carousel.py --calendar).
TESTI = [
 ("a12-aritmetica-lettera", "2026-10-19T18:26", "Testo · È uscito",
  "L’Aritmetica del Consenso è uscito.\nÈ un noir dinastico in sei puntate, per adulti, riunite in un unico ebook. Un ghostwriter scrive la biografia di una matriarca di novantun anni che ha cominciato a ricordare tutto; intanto la sua famiglia si prepara a votare la propria eternità.\nLa Puntata 1 è gratis, in PDF o EPUB, senza iscrizione: " + SITO_A + "\nIl romanzo completo è su Amazon Kindle: " + AMAZON,
  SITO_A),
]
TESTI = [(i, w, g, t + "\n\n" + tag_fb(i), l) for i, w, g, t, l in TESTI]   # con i 10 hashtag di Facebook
