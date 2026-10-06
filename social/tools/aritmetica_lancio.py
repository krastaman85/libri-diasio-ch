# ARCHIVIO (6/10/2026, sera): questi post con data 23 ottobre sono stati tolti dal calendario perché l'eBook esce prima; riscrivere date e conto alla rovescia prima di riusarli.
# 13 post di lancio de «L'Aritmetica del Consenso» (uscita prevista venerdì 23 ottobre 2026), approvati dall'utente il 6/10/2026.
# Le citazioni sono testuali dalla Puntata 1 (testo approvato, in Drive). *parola* = parola in ottone.
# Letto da carousel.py (load) con exec: niente import relativi. `python carousel.py` rende le immagini in social/img/nuovi/
# (le Storie in social/img/story/), `python carousel.py --calendar` aggiunge le voci a calendar.json.
import hashlib
import random

SITO_A = "https://libri.diasio.ch/aritmetica/"
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


# Righe finali. Prima dell'uscita non c'è ancora il link Amazon: si rimanda al sito (IG: link in bio).
PRE_IG = "Esce il 23 ottobre su Amazon Kindle e, tramite StreetLib, negli altri store digitali. Link in bio."
PRE_FB = f"Esce il 23 ottobre su Amazon Kindle e, tramite StreetLib, negli altri store digitali.\nLa Puntata 1 sarà gratuita dal giorno dell’uscita: {SITO_A}"
POST_IG = "Il romanzo è su Amazon Kindle e, tramite StreetLib, negli altri store digitali. La Puntata 1 è gratis, in PDF o EPUB, senza iscrizione: link in bio."
POST_FB = f"Il romanzo è su Amazon Kindle e, tramite StreetLib, negli altri store digitali: i link sono sul sito.\nLa Puntata 1 è gratis, in PDF o EPUB, senza iscrizione: {SITO_A}"


def A(id, when, seg, slides, body, alt, ironico=False, ig_extra=None, fb_extra=None, post=False):
    riga_ig, riga_fb = (POST_IG, POST_FB) if post else (PRE_IG, PRE_FB)
    cap = body + "\n" + (ig_extra or riga_ig) + "\n\n" + tag_ig(id, ironico)
    cfb = body + "\n\n" + (fb_extra or riga_fb) + "\n\n" + tag_fb(id, ironico)
    return dict(id=id, when=when, book="aritmetica", seg=seg, flat=True, theme="green", slides=slides,
                caption=cap, caption_fb=cfb, alt=alt, ironico=ironico)


def band(txt):
    return dict(kindle=txt)


ITEMS = [

 A("a01-aritmetica-annuncio", "2026-10-08T12:24", "Annuncio · Work in progress (grafica)",
   [dict(k="cta", books=["aritmetica"], text="«Somiglia a qualcuno che ho *pagato*.»", button="In uscita il 23 ottobre",
         line="Work in progress · <b>libri.diasio.ch</b>")],
   "Work in progress. Il prossimo romanzo esce il 23 ottobre.\nUn ghostwriter, una famiglia che sta per diventare legalmente eterna e una vecchia che ha cominciato a ricordare tutto.\n«Somiglia a qualcuno che ho pagato.»\nL’Aritmetica del Consenso, noir dinastico di D. Iasio. Segui il conto alla rovescia.",
   "Copertina de L’Aritmetica del Consenso (le mani di una vecchia sbucciano un mandarino su un piatto d’argento), con la frase «Somiglia a qualcuno che ho pagato.» e il pulsante «In uscita il 23 ottobre». Work in progress."),

 A("a02-aritmetica-quaderno", "2026-10-11T20:23", "Accenni · Il quaderno e il registratore (carosello)",
   [dict(k="hook", kick="L’Aritmetica del Consenso", text="Una *penna*.\nUn *registratore*.", sub="Due versioni dello stesso pomeriggio."),
    dict(k="quote", text="«La penna scrive «tempo: sereno». Il registratore scrive tutto il resto.»", who="L’Aritmetica del Consenso · Puntata 1"),
    dict(k="quote", text="«Per lei la vita è una partita doppia: da una parte quello che entra, dall'altra quello che si è dovuto dare perché entrasse.»", who="L’Aritmetica del Consenso · Puntata 1"),
    dict(k="hook", kick="Mancano 12 giorni", text="23 *ottobre*", sub="Avvisami all’uscita: link in bio.", kindle="Mancano 12 giorni")],
   "La penna scrive «tempo: sereno». Il registratore scrive tutto il resto.\nPer la signora la vita è una partita doppia: quello che entra e quello che si è dovuto dare perché entrasse.\nL’Aritmetica del Consenso, noir dinastico in uscita il 23 ottobre.",
   "Carosello di quattro slide su fondo verde bottiglia: «Una penna. Un registratore.»; la frase «La penna scrive «tempo: sereno». Il registratore scrive tutto il resto.»; la frase sulla vita come partita doppia; «23 ottobre, mancano 12 giorni». L’Aritmetica del Consenso."),

 A("a03-aritmetica-direttori", "2026-10-13T19:38", "Citazione ironica · Conto alla rovescia (grafica)",
   [dict(k="quote", text="«I direttori capiscono sempre, ragioniere, è per questo che li scelgono.»", who="L’Aritmetica del Consenso · Puntata 1", kindle="Mancano 10 giorni")],
   "«I direttori capiscono sempre, ragioniere, è per questo che li scelgono.»\nMancano 10 giorni a L’Aritmetica del Consenso, noir dinastico di D. Iasio.",
   "Frase su fondo verde bottiglia: «I direttori capiscono sempre, ragioniere, è per questo che li scelgono.» L’Aritmetica del Consenso, Puntata 1. Fascia: «Mancano 10 giorni».", ironico=True),

 A("a04-aritmetica-silenzio", "2026-10-14T12:31", "Domanda ai lettori · Conto alla rovescia (grafica)",
   [dict(k="quote", text="«Il compenso era indecente. Lo capisci da come nessuno lo nomina.»", who="L’Aritmetica del Consenso · Puntata 1",
         sub="E tu: quanto costa il tuo *silenzio*?", kindle="Mancano 9 giorni")],
   "«Il compenso era indecente. Lo capisci da come nessuno lo nomina.»\nE tu: quanto costa il tuo silenzio? Rispondi nei commenti.\nL’Aritmetica del Consenso esce il 23 ottobre.",
   "Frase su fondo verde bottiglia: «Il compenso era indecente. Lo capisci da come nessuno lo nomina.» Sotto, la domanda «E tu: quanto costa il tuo silenzio?». Fascia: «Mancano 9 giorni».",
   ig_extra="Esce il 23 ottobre su Amazon Kindle e, tramite StreetLib, negli altri store digitali. Link in bio."),

 A("a05-aritmetica-dopo", "2026-10-15T19:26", "Citazione · Conto alla rovescia (grafica)",
   [dict(k="quote", text="«Ma noi lavoriamo sempre dopo.»", who="L’Aritmetica del Consenso · Puntata 1", kindle="Mancano 8 giorni")],
   "«Ma noi lavoriamo sempre dopo.»\nMancano 8 giorni: L’Aritmetica del Consenso, di D. Iasio, esce il 23 ottobre.",
   "Frase su fondo verde bottiglia: «Ma noi lavoriamo sempre dopo.» L’Aritmetica del Consenso, Puntata 1. Fascia: «Mancano 8 giorni»."),

 A("a06-aritmetica-posta", "2026-10-17T12:38", "La «posta» · Conto alla rovescia (grafica in stile registro)",
   [dict(k="doc", kick="Mancano 6 giorni", name="REGISTRATORE · ACCESO",
         lines=["Dodici milioni di lire, in contanti, nel settantaquattro.", "Per il sottosegretario.",
                "Non per lui: per la sua segretaria, che era quella che decideva."], kindle="In uscita il 23 ottobre")],
   "Dodici milioni di lire, in contanti, nel settantaquattro. Per il sottosegretario. Non per lui: per la sua segretaria, che era quella che decideva.\nÈ la «posta» che la signora detta e il registratore conserva. Mancano 6 giorni a L’Aritmetica del Consenso.",
   "Finto registro su fondo verde bottiglia, «Registratore · acceso»: «Dodici milioni di lire, in contanti, nel settantaquattro. Per il sottosegretario. Non per lui: per la sua segretaria, che era quella che decideva.» Fascia: «Mancano 6 giorni»."),

 A("a07-aritmetica-ci-penso", "2026-10-18T20:36", "Domanda ai lettori (tono ironico) · Conto alla rovescia (grafica)",
   [dict(k="quote", text="«Brindare a un «ci penso» non è una cosa che si faccia, nelle famiglie normali.»", who="L’Aritmetica del Consenso · Puntata 1",
         sub="E tu, quando hai detto «ci penso» per non dire *no*?", kindle="Mancano 5 giorni")],
   "«Brindare a un «ci penso» non è una cosa che si faccia, nelle famiglie normali.»\nE tu, quando hai detto «ci penso» per non dire no? Rispondi nei commenti.\nMancano 5 giorni a L’Aritmetica del Consenso.",
   "Frase su fondo verde bottiglia: «Brindare a un «ci penso» non è una cosa che si faccia, nelle famiglie normali.» Sotto, la domanda «E tu, quando hai detto «ci penso» per non dire no?». Fascia: «Mancano 5 giorni».", ironico=True),

 A("a09-aritmetica-troverai", "2026-10-20T19:29", "Cosa troverai · Conto alla rovescia (carosello)",
   [dict(k="step", kick="L’Aritmetica del Consenso", n="1", title="Una vecchia che ricorda tutto", text="Da tre mesi ha smesso di ricordare le cose in ordine. Ha cominciato a ricordarle *tutte*."),
    dict(k="step", kick="L’Aritmetica del Consenso", n="2", title="Un mestiere da invisibile", text="Scrive le vite degli altri e poi sparisce, come l’idraulico. Il compenso è *indecente*."),
    dict(k="step", kick="L’Aritmetica del Consenso", n="3", title="Una famiglia gentile", text="Nessuno alza la voce e nessuno controlla le tasche di nessuno. Tutto si spiega con la buona *educazione*."),
    dict(k="hook", kick="Mancano 3 giorni", text="23 *ottobre*", sub="Avvisami all’uscita: iscriviti alla newsletter, link in bio.", kindle="Mancano 3 giorni")],
   "Una vecchia che ricorda tutto, un mestiere da invisibile, una famiglia gentile.\nMancano 3 giorni a L’Aritmetica del Consenso, noir dinastico di D. Iasio. Iscriviti alla newsletter per sapere quando esce e scaricare la Puntata 1.",
   "Carosello di quattro slide su fondo verde bottiglia: 1 «Una vecchia che ricorda tutto»; 2 «Un mestiere da invisibile»; 3 «Una famiglia gentile»; 4 «Mancano 3 giorni, 23 ottobre». L’Aritmetica del Consenso."),

 A("a10-aritmetica-listino", "2026-10-22T19:44", "Citazione · Ultimo giorno (grafica)",
   [dict(k="quote", text="«Era il suo listino.»", who="L’Aritmetica del Consenso · Puntata 1", kindle="Manca 1 giorno")],
   "«Era il suo listino.»\nManca 1 giorno a L’Aritmetica del Consenso.",
   "Frase su fondo verde bottiglia: «Era il suo listino.» L’Aritmetica del Consenso, Puntata 1. Fascia: «Manca 1 giorno»."),

 A("a11-aritmetica-da-oggi", "2026-10-23T12:29", "Lancio · Da oggi (locandina)",
   [dict(k="cta", books=["aritmetica"], text="Da *oggi*", button="Leggi la Puntata 1 gratis", line="PDF ed EPUB · <b>libri.diasio.ch</b>")],
   "Da oggi. L’Aritmetica del Consenso, noir dinastico di D. Iasio in sei puntate, tutte in un unico ebook.",
   "Locandina su fondo verde bottiglia con la copertina de L’Aritmetica del Consenso (mani di una vecchia che sbucciano un mandarino): «Da oggi», pulsante «Leggi la Puntata 1 gratis», PDF ed EPUB su libri.diasio.ch.", post=True),

 A("a13-aritmetica-incipit", "2026-10-25T20:19", "Prime righe (carosello)",
   [dict(k="quote", text="«La vecchia mi ha appena chiesto quanto costava un ministro, ai suoi tempi, e io le ho risposto la verità: meno di quanto costa oggi un buon avvocato.»", who="L’Aritmetica del Consenso · Puntata 1", foot="Puntata 1 gratis · libri.diasio.ch"),
    dict(k="quote", text="«Sono le dieci e quaranta di un mercoledì. Siamo in una sala da pranzo in cui potrebbe mangiare un reggimento e in cui non mangia mai nessuno.»", who="L’Aritmetica del Consenso · Puntata 1", foot="Puntata 1 gratis · libri.diasio.ch"),
    dict(k="quote", text="«Faccio il ghostwriter. Scrivo le vite degli altri e poi sparisco, come l'idraulico: nessuno ringrazia l'idraulico, si ringrazia il rubinetto.»", who="L’Aritmetica del Consenso · Puntata 1", foot="Puntata 1 gratis · libri.diasio.ch"),
    dict(k="quote", text="«Io ho il registratore acceso nella tasca della giacca. Non per coraggio, sia chiaro. Per mestiere.»", who="L’Aritmetica del Consenso · Puntata 1", foot="Puntata 1 gratis · libri.diasio.ch"),
    dict(k="cta", books=["aritmetica"], text="Continua con la Puntata *1*", button="Leggi la Puntata 1 gratis", line="PDF ed EPUB · <b>libri.diasio.ch</b>")],
   "L’Aritmetica del Consenso è uscito: ecco le prime righe, una alla volta.\nUn ghostwriter, una vecchia che ricorda tutto e un registratore in tasca.",
   "Carosello di cinque slide su fondo verde bottiglia con le prime righe de L’Aritmetica del Consenso: la domanda sul costo di un ministro; la sala da pranzo; il ghostwriter e l’idraulico; il registratore acceso in tasca; invito a leggere la Puntata 1 gratis.", post=True),

 # Storia (solo immagine, senza link): lunedì 19 ottobre
 dict(id="a08-aritmetica-storia", when="2026-10-19T18:44", book="aritmetica", seg="Storia · Conto alla rovescia", story=True, theme="green",
      slides=[dict(k="quote", text="«Nessuno, in questa famiglia, fa rumore quando si avvicina.»", who="L’Aritmetica del Consenso · Puntata 1", sub="Mancano 4 giorni · *23 ottobre*")]),
]

# Post di solo testo per la Pagina Facebook (letti da carousel.py --calendar). venerdì 23 ottobre
TESTI = [
 ("a12-aritmetica-lettera", "2026-10-23T18:26", "Testo · Lancio",
  "L’Aritmetica del Consenso è uscito.\nÈ un noir dinastico in sei puntate, per adulti, riunite in un unico ebook. Un ghostwriter scrive la biografia di una matriarca di novantun anni che ha cominciato a ricordare tutto; intanto la sua famiglia si prepara a votare la propria eternità.\nLa Puntata 1 è gratis, in PDF o EPUB, senza iscrizione: " + SITO_A + "\nIl romanzo completo è su Amazon Kindle e, tramite StreetLib, negli altri store digitali.",
  SITO_A),
]
TESTI = [(i, w, g, t + "\n\n" + tag_fb(i), l) for i, w, g, t, l in TESTI]   # con i 10 hashtag di Facebook
