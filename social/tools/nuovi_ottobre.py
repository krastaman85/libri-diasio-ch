# 31 nuovi post per le due uscite al giorno (dal 6 ottobre al 2 novembre 2026), con la riga su Amazon Kindle.
# Le citazioni sono testuali dalle Puntata 1 (download/*.epub): *parola* = parola in ambra.
# Questo file viene letto da carousel.py (load) con exec: niente import relativi.
# `python carousel.py` rende le immagini in social/img/nuovi/, `python carousel.py --calendar` aggiunge le voci a calendar.json.
import hashlib
import random

BUG, OBL = "Il Bug della Trasparenza", "L’Economia dell’Oblio"
URL = {"bug": "https://www.amazon.it/dp/B0HLN2VSJP", "oblio": "https://www.amazon.it/dp/B0HLMKWJZ5"}
SITO = {"bug": "https://libri.diasio.ch/bug/", "oblio": "https://libri.diasio.ch/oblio/", "both": "https://libri.diasio.ch/"}
TITOLO = {"bug": BUG, "oblio": OBL}
Q = lambda text, **kw: dict(k="quote", text=text, **kw)


# ---------- hashtag: solo il vocabolario dell'utente; IG 5, FB 10; ironia solo sui post ironici ----------
def _rng(pid, kind):
    return random.Random(int(hashlib.sha256((pid + kind).encode()).hexdigest(), 16))


GENERE = {"bug": ["#NoirItaliano", "#RomanzoNoir", "#LetteraturaNoir", "#ThrillerItaliano", "#AltaTensione", "#GialloItaliano"],
          "oblio": ["#ThrillerPsicologico", "#LibriThriller", "#ThrillerItaliano", "#AltaTensione", "#LetteraturaNoir"]}
POPOLARI = {"bug": ["#NoirItaliano", "#RomanzoNoir"], "oblio": ["#ThrillerPsicologico", "#LibriThriller"]}
TONO = ["#Ironia", "#UmorismoNero", "#Satira", "#CommediaNera"]
COMMUNITY = ["#BookstagramItalia", "#ConsigliDiLettura", "#LibriDaLeggere"]
SPECIALI = ["#IoLeggo", "#ScrittoriItaliani", "#ScrittoriEmergenti", "#EditoriaItaliana"]
GEO = ["#Ticino", "#SvizzeraItaliana", "#ScrittoriSvizzeri", "#LeggereInSvizzera", "#CulturaTicino", "#BookstagramSvizzera"]


def tag_ig(pid, book, ironico=False):
    r = _rng(pid, "ig")
    primo = r.choice(POPOLARI[book])
    secondo = r.choice(TONO) if ironico else r.choice([g for g in GENERE[book] if g != primo])
    return " ".join([primo, secondo, r.choice(COMMUNITY), r.choice(SPECIALI), r.choice(GEO)])


def tag_fb(pid, book, ironico=False):
    r = _rng(pid, "fb")
    n_gen, n_ton, n_com, n_geo = (3, 2, 2, 2) if ironico else (4, 0, 2, 3)
    t = r.sample(GENERE[book], n_gen) + (r.sample(TONO, n_ton) if n_ton else []) + r.sample(COMMUNITY, n_com) \
        + [r.choice(SPECIALI)] + r.sample(GEO, n_geo)
    return " ".join(t)


# ---------- riga fissa su Amazon Kindle (solo disponibilità e link, niente prezzo) ----------
def riga_ig(pid, book):
    """Riga Kindle per Instagram (il link è in bio). book: bug | oblio | both."""
    v = int(hashlib.sha256((pid + "k").encode()).hexdigest(), 16) % 4
    if book == "both":
        return ["I due romanzi sono su Amazon Kindle: link in bio.",
                "Su Amazon Kindle trovi entrambi i romanzi (link in bio). La Puntata 1 resta gratis, in PDF o EPUB.",
                "Entrambi ora su Amazon Kindle. Link in bio.",
                "Disponibili su Amazon Kindle: link in bio, dove c’è anche la Puntata 1 gratis."][v]
    t = TITOLO[book]
    return [f"Il romanzo completo è su Amazon Kindle: link in bio.",
            f"Su Amazon Kindle trovi {t} completo (link in bio). La Puntata 1 resta gratis, in PDF o EPUB.",
            "Ora su Amazon Kindle. Link in bio.",
            "Disponibile su Amazon Kindle: link in bio, dove c’è anche la Puntata 1 gratis."][v]


def riga_fb(pid, book):
    v = int(hashlib.sha256((pid + "k").encode()).hexdigest(), 16) % 3
    if book == "both":
        return (f"Entrambi i romanzi sono su Amazon Kindle:\n{BUG}: {URL['bug']}\n{OBL}: {URL['oblio']}\n"
                f"La Puntata 1 di entrambi è gratis, in PDF o EPUB: {SITO['both']}")
    u, s = URL[book], SITO[book]
    return [f"Il romanzo completo è su Amazon Kindle: {u}\nLa Puntata 1 è gratis, in PDF o EPUB, senza iscrizione: {s}",
            f"Disponibile su Amazon Kindle: {u}\nPuntata 1 gratis, PDF o EPUB: {s}",
            f"Ora su Amazon Kindle: {u}\nPer cominciare dalla Puntata 1 gratis (PDF o EPUB): {s}"][v]


# ---------- riga Kindle breve per le didascalie già in calendario (hanno già la riga sulla Puntata 1 gratis) ----------
def riga_ig_breve(pid, book):
    v = int(hashlib.sha256((pid + "kb").encode()).hexdigest(), 16) % 3
    if book == "both":
        return ["I due romanzi sono su Amazon Kindle: link in bio.", "Entrambi ora su Amazon Kindle. Link in bio.",
                "Disponibili su Amazon Kindle (link in bio)."][v]
    return ["Il romanzo completo è su Amazon Kindle: link in bio.", "Ora su Amazon Kindle. Link in bio.",
            "Disponibile su Amazon Kindle (link in bio)."][v]


def riga_fb_breve(pid, book):
    v = int(hashlib.sha256((pid + "kb").encode()).hexdigest(), 16) % 3
    if book == "both":
        return (["I due romanzi completi sono su Amazon Kindle:", "Entrambi ora su Amazon Kindle:", "Disponibili su Amazon Kindle:"][v]
                + f"\n{BUG}: {URL['bug']}\n{OBL}: {URL['oblio']}")
    return ["Il romanzo completo è su Amazon Kindle: ", "Ora su Amazon Kindle: ", "Disponibile su Amazon Kindle: "][v] + URL[book]


def P(id, when, book, seg, slides, body, alt, ironico=False, ig=None, fb=None, tags_book=None):
    """Voce di calendario. body = testo comune; la riga Kindle si aggiunge da sola.
    ig/fb: testi completi (senza hashtag) per i post dedicati a Kindle."""
    tb = tags_book or book
    ti, tf = tag_ig(id, tb if tb != "both" else "bug", ironico), tag_fb(id, tb if tb != "both" else "bug", ironico)
    cap = ig if ig is not None else body + "\n" + riga_ig(id, book)
    cfb = fb if fb is not None else body + "\n\n" + riga_fb(id, book)
    return dict(id=id, when=when, book=book if book != "both" else "bug", seg=seg, flat=True, slides=slides,
                caption=cap + "\n\n" + ti, caption_fb=cfb + "\n\n" + tf, alt=alt, ironico=ironico)


KB = dict(button="Disponibile su Amazon Kindle")      # pulsante della slide finale
IA = "\nImmagine creata con l’IA, la frase è dal romanzo."

ITEMS = [

 # ================= martedì 6 ottobre =================
 P("n01-bug-7e14", "2026-10-06T12:19", "bug", "Lettori noir + tech/privacy (immagine IA)",
   [dict(k="photo", photo="Bug_B17_telefono-alba_9x16.jpg", pos=45,
         text="«E alle 7:14 di ogni mattina, un minuto prima della sveglia che lei non aveva ancora impostato, il telefono si accendeva da solo.»",
         who=BUG + " · Puntata 1")],
   "Alle 7:14, ogni mattina, il telefono di Nadia si accende da solo. Un minuto prima della sveglia che non ha ancora impostato.\nÈ l’inizio de Il Bug della Trasparenza: noir sociale in un condominio d’élite dove l’app sa più di quanto dovrebbe." + IA,
   "Immagine creata con l’IA: all’alba, sul comodino, uno smartphone acceso nel buio. Sopra, la frase del romanzo: «E alle 7:14 di ogni mattina, un minuto prima della sveglia che lei non aveva ancora impostato, il telefono si accendeva da solo.» Il Bug della Trasparenza."),

 # ================= mercoledì 7 ottobre =================
 P("n02-bug-aggiornata", "2026-10-07T12:36", "bug", "Tech/privacy + vita di condominio",
   [dict(k="notif", kick=BUG, app="Meridiana Life", when="adesso", title="Meridiana Life si è aggiornata.",
         text="Benvenuti in *Trasparenza Meridiana*.", sub="Nessuno ci fece caso più di tanto.")],
   "Tutti i telefoni della sala vibrano nello stesso istante, mentre il presidente fa approvare il punto quattro «per acclamazione».\nÈ la notifica che apre Il Bug della Trasparenza. Da lì in poi, nel palazzo, nessuno può più dire di non sapere.",
   "Finta notifica dell’app Meridiana Life: «Meridiana Life si è aggiornata. Benvenuti in Trasparenza Meridiana.» Sotto: «Nessuno ci fece caso più di tanto.» Il Bug della Trasparenza.", ironico=True),

 # ================= giovedì 8 ottobre =================
 P("n03-oblio-kindle", "2026-10-08T19:22", "oblio", "Thriller psicologico + lettori digitali (carosello Kindle)",
   [dict(k="hook", kick=OBL, text="Chi dimentica diventa *innocente*. Paga solo chi *ricorda*.", sub="Thriller psicologico in sei puntate. Scorri."),
    Q("«Perché curare un dolore quando puoi estrarlo, metterlo in una scatola e rivenderlo?»", book="oblio", who="Dora Calvi · L’Economia dell’Oblio"),
    Q("«Fuori, sul marciapiede, c’è il solito presidio del Comitato Anestesia: sei persone con i cartelli «Il dolore è tuo» e un megafono che non funziona mai.»", book="oblio", who="Dora Calvi · L’Economia dell’Oblio"),
    dict(k="cta", text="Il romanzo *completo*. Ora su *Kindle*.", **KB, line="Puntata 1 gratis, PDF ed EPUB · <b>libri.diasio.ch</b>")],
   "", "Carosello di quattro slide su fondo scuro: il motto de L’Economia dell’Oblio («Chi dimentica diventa innocente. Paga solo chi ricorda.»), due frasi dalla Puntata 1 sul dolore da estrarre e sul presidio del Comitato Anestesia, e l’invito a leggere il romanzo completo su Amazon Kindle.",
   ig="L’Economia dell’Oblio, thriller psicologico: Dora Calvi estrae i ricordi dei clienti e li mette in una scatola, finché trova nella propria testa i frammenti di un omicidio.\nScorri: due frasi dalla Puntata 1. Il romanzo completo, in sei puntate, è su Amazon Kindle (link in bio). La Puntata 1 resta gratis, in PDF o EPUB.",
   fb="L’Economia dell’Oblio, thriller psicologico: Dora Calvi estrae i ricordi dei clienti e li mette in una scatola, finché trova nella propria testa i frammenti di un omicidio.\nScorri: due frasi dalla Puntata 1.\n\nIl romanzo completo, in sei puntate, è su Amazon Kindle: " + URL["oblio"] + "\nLa Puntata 1 è gratis, in PDF o EPUB, senza iscrizione: " + SITO["oblio"]),

 # ================= venerdì 9 ottobre =================
 P("n04-oblio-caveau", "2026-10-09T12:28", "oblio", "Psicologia/memoria (tono rispettoso) + lettori thriller",
   [dict(k="rows", title="LE SPESE DI DORA CALVI · MENSILI", sub="CHI PAGA CHE COSA",
         rows=[("Retta della casa di cura, Pavia", "€ 2.900"), ("Caveau Personale", "€ 39"), ("Contenuto", "1 cartuccia"), ("Conservazione", "–80 °C")],
         note="Dentro c’è il giorno in cui mio padre è uscito di casa con la valigia e non è più tornato.")],
   "Il conto mensile di Dora Calvi: la retta di una casa di cura e un addebito da trentanove euro per una cartuccia tenuta in frigo.\nDentro c’è un ricordo di sua madre. Dora non ha mai capito se toglierglielo sia stato un atto d’amore o un furto.\nL’Economia dell’Oblio, Puntata 1.",
   "Finto estratto conto di Dora Calvi: retta della casa di cura a Pavia 2.900 euro, Caveau Personale 39 euro, contenuto una cartuccia, conservazione a meno 80 gradi. In fondo: «Dentro c’è il giorno in cui mio padre è uscito di casa con la valigia e non è più tornato.» L’Economia dell’Oblio."),

 # ================= sabato 10 ottobre =================
 P("n05-oblio-merli", "2026-10-10T17:18", "oblio", "Psicologia/memoria (tono rispettoso) + lettori thriller (carosello)",
   [dict(k="hook", kick=OBL, text="Gianfranco Merli vuole *dimenticare* suo padre.", sub="Entro l’ora di pranzo. Una scena della Puntata 1. Scorri."),
    Q("«Fa male?»\n«Dipende da cosa intende per male.»", book="oblio", who="Gianfranco Merli e Dora Calvi"),
    Q("«Scusa» dice Gianfranco al morto. «Era Brescia.»", book="oblio", who="Gianfranco Merli"),
    Q("«Il ventilatore col calzino si è fermato.»", book="oblio", who="Dora Calvi · la stanza 314"),
    Q("«Ha la mano calda e asciutta di chi non ha più niente da nascondere, e per un istante lo invidio da morire.»", book="oblio", who="Dora Calvi"),
    dict(k="cta", text="Il romanzo *completo*. Ora su *Kindle*.", **KB, line="Puntata 1 gratis, PDF ed EPUB · <b>libri.diasio.ch</b>")],
   "Gianfranco Merli ha cinquantadue anni e vuole togliersi dalla testa la morte di suo padre prima dell’assemblea dei soci. Dora Calvi vede che cosa c’è davvero dentro quel ricordo.\nUna scena della Puntata 1 de L’Economia dell’Oblio, in cinque frasi. Scorri.",
   "Carosello di sei slide su fondo scuro: Gianfranco Merli vuole dimenticare suo padre; il dialogo «Fa male?» «Dipende da cosa intende per male.»; «Scusa, era Brescia»; «Il ventilatore col calzino si è fermato»; la mano calda di chi non ha più niente da nascondere; invito a leggere il romanzo su Amazon Kindle. L’Economia dell’Oblio."),

 # ================= domenica 11 ottobre =================
 P("n06-bug-meridiana-note", "2026-10-11T12:34", "bug", "Giornalismo/inchieste + lettori noir (carosello)",
   [dict(k="hook", kick=BUG, text="Il file che *Nadia* apre alle undici di sera.", sub="Le sue note, riga per riga. Scorri."),
    dict(k="doc", kick="Prima assemblea", name="meridiana_note.txt",
         lines=["15 del mese.", "Aggiornamento attivato dal portiere su istruzione della gestione.", "Prima vittima: Cesare Rocchi Molteni, presidente, corruzione minore sul rifacimento tetto."]),
    dict(k="doc", kick="Prima assemblea", name="meridiana_note.txt",
         lines=["Reazione: minimizzare, promettere disattivazione, andarsene in fretta.", "Nessuno ha creduto davvero alla storia del bug — troppo specifico, troppo vero."]),
    dict(k="doc", kick="L’ultima riga", name="meridiana_note.txt",
         lines=["Domanda aperta: chi altro, nel palazzo, sa già cosa succederà quando toccherà a loro?"]),
    dict(k="cta", text="Il romanzo *completo*. Ora su *Kindle*.", **KB, line="Puntata 1 gratis, PDF ed EPUB · <b>libri.diasio.ch</b>")],
   "Alle undici di sera, dopo la prima assemblea, Nadia apre un file e scrive quello che ha visto. Lo chiama meridiana_note.txt «per pura mancanza di fantasia».\nQueste sono le sue note, parola per parola. Scorri.\nSalvalo, se anche tu tieni un file così.",
   "Carosello di cinque slide: il file meridiana_note.txt di Nadia Colombo, mostrato come nota di testo in tre schermate (l’aggiornamento attivato dal portiere, la prima vittima, la domanda aperta), e l’invito a leggere Il Bug della Trasparenza su Amazon Kindle."),

 # ================= lunedì 12 ottobre =================
 P("n07-bug-fa-parte-del-lavoro", "2026-10-12T12:23", "bug", "Lettori noir (core) + mondo del lavoro",
   [dict(k="quote", text="«L’aggiornamento l’ho installato io, sa?»\n«Me l’hanno mandato via mail, con le istruzioni. Non c’era scritto niente di strano.»", who="Yusuf Demir, il portiere", kindle=True)],
   "Il portiere ammette di aver installato lui l’aggiornamento: gli è arrivato per mail, con le istruzioni. Nadia sente che c’è dell’altro, ma non lo chiede. Non ancora.\nNella Puntata 1 del Bug della Trasparenza ogni frase innocua ha un secondo fondo.",
   "Citazione su fondo scuro con fascia ambra «Ora su Amazon Kindle»: «L’aggiornamento l’ho installato io, sa? Me l’hanno mandato via mail, con le istruzioni. Non c’era scritto niente di strano.» Yusuf Demir, il portiere. Il Bug della Trasparenza."),

 # ================= martedì 13 ottobre =================
 P("n08-bug-tre-passi-kindle", "2026-10-13T12:44", "bug", "Lettori digitali (ebook, Kindle) + nuovi arrivati (carosello)",
   [dict(k="hook", kick=BUG, text="Dalla Puntata 1 al *romanzo intero*.", sub="Tre passi. Scorri."),
    dict(k="step", n="1", title="Leggi la *Puntata 1*", text="Gratis, in PDF o EPUB, senza iscrizione. Dal link in bio, su libri.diasio.ch."),
    dict(k="step", n="2", title="Se ti prende, apri *Amazon Kindle*", text="Il romanzo completo, in otto puntate, è disponibile in formato integrale su Amazon Kindle."),
    dict(k="step", n="3", title="Leggi dove *vuoi*", text="Su un Kindle, oppure con l’app gratuita Kindle su telefono e tablet."),
    dict(k="cta", text="Noir sociale · *otto puntate*", **KB, line="Puntata 1 gratis · <b>libri.diasio.ch</b>")],
   "", "Carosello di cinque slide: dalla Puntata 1 gratuita al romanzo intero de Il Bug della Trasparenza in tre passi (leggere la Puntata 1, aprire Amazon Kindle, leggere su Kindle o con l’app).",
   ig="Come si passa dalla Puntata 1 gratis al romanzo intero, in tre passi. Scorri.\nIl Bug della Trasparenza è un noir sociale in otto puntate: il romanzo completo è su Amazon Kindle (link in bio), la Puntata 1 resta gratis in PDF o EPUB.",
   fb="Come si passa dalla Puntata 1 gratis al romanzo intero, in tre passi. Scorri.\n\nIl Bug della Trasparenza è un noir sociale in otto puntate. Il romanzo completo è su Amazon Kindle: " + URL["bug"] + "\nLa Puntata 1 è gratis, in PDF o EPUB, senza iscrizione: " + SITO["bug"]),

 # ================= mercoledì 14 ottobre =================
 P("n09-bug-alma", "2026-10-14T12:12", "bug", "Vita di condominio + lettori noir",
   [Q("«Scusate, ma è successo anche a me ieri sera. Il telefono che si accende da solo, tipo in ascolto. Pensavo fosse un virus.»", who="Alma Ferretti, all’assemblea")],
   "Il punto sei dell’ordine del giorno non arriva mai: una vicina alza la mano e dice una cosa che cambia l’assemblea.\nÈ la scena in cui il bug smette di essere un problema di Cesare e diventa di tutto il palazzo. Dal Bug della Trasparenza, Puntata 1.",
   "Citazione su fondo scuro: «Scusate, ma è successo anche a me ieri sera. Il telefono che si accende da solo, tipo in ascolto. Pensavo fosse un virus.» Alma Ferretti, all’assemblea. Il Bug della Trasparenza."),

 # ================= giovedì 15 ottobre =================
 P("n10-oblio-dora", "2026-10-15T19:41", "oblio", "Lettori thriller + voce narrante",
   [dict(k="quote", text="«Trent’anni fa, se stavi male, andavi da uno psicologo che ti faceva parlare per cinquanta minuti e ti mandava via sul più bello, e ci tornavi per anni, e alla fine forse stavi meglio, forse avevi solo imparato a raccontartela.»", who="Dora Calvi, voce narrante", kindle=True)],
   "Com’era curarsi, prima. Poi qualcuno ha fatto due conti: perché curare un dolore quando si può estrarre?\nDora Calvi, tecnica estrattiva, racconta il mondo de L’Economia dell’Oblio, thriller psicologico in sei puntate.",
   "Citazione su fondo scuro con fascia ambra «Ora su Amazon Kindle»: «Trent’anni fa, se stavi male, andavi da uno psicologo che ti faceva parlare per cinquanta minuti e ti mandava via sul più bello, e ci tornavi per anni, e alla fine forse stavi meglio, forse avevi solo imparato a raccontartela.» Dora Calvi. L’Economia dell’Oblio."),

 # ================= venerdì 16 ottobre (due uscite) =================
 P("n11-bug-presidente", "2026-10-16T12:03", "bug", "Vita di condominio + lettori noir (immagine IA)",
   [dict(k="photo", photo="Bug_B07_presidente-martelletto_9x16.jpg", pos=35,
         text="«Cesare Rocchi Molteni presiedeva in piedi, come sempre, perché diceva che seduto perdeva autorità.»",
         who=BUG + " · Puntata 1", kindle=True)],
   "Cesare Rocchi Molteni presiede in piedi, perché da seduto perderebbe autorità. Sessantotto anni, presidente da otto, e un telefono che agita come un martelletto.\nIl primo a finire nei guai, nel Bug della Trasparenza, è lui." + IA,
   "Immagine creata con l’IA: un uomo anziano in piedi in una sala d’assemblea, con il telefono in mano come un martelletto. Sopra, con fascia ambra «Ora su Amazon Kindle»: «Cesare Rocchi Molteni presiedeva in piedi, come sempre, perché diceva che seduto perdeva autorità.» Il Bug della Trasparenza."),
 P("n12-oblio-cane", "2026-10-16T18:31", "oblio", "Satira del lavoro + fantascienza/distopia",
   [Q("«Un prato e basta. Ogni tanto attraversa un cane. Il cane l’ha scelto un comitato.»", book="oblio", who="Dora Calvi · la Sala Prato")],
   "Dopo ogni estrazione, undici minuti nella Sala Prato: un prato su uno schermo e, ogni tanto, un cane che lo attraversa. Il cane l’ha scelto un comitato.\nL’Economia dell’Oblio ha un’idea molto precisa di cosa sia il benessere.",
   "Citazione su fondo scuro: «Un prato e basta. Ogni tanto attraversa un cane. Il cane l’ha scelto un comitato.» Dora Calvi, la Sala Prato. L’Economia dell’Oblio.", ironico=True),

 # ================= sabato 17 ottobre (due uscite) =================
 P("n13-oblio-ricordo-non-suo", "2026-10-17T12:21", "oblio", "Fantascienza/distopia + lettori thriller (carosello)",
   [dict(k="hook", kick=OBL, text="Il ricordo che *non è suo*.", sub="Dopo ogni estrazione c’è un risciacquo. Stavolta qualcosa resta. Scorri."),
    Q("«Odore di shampoo alla pesca, quello economico, che si vende in flaconi da un litro.»", book="oblio", who="Dora Calvi"),
    Q("«Ho in mano i capelli di qualcuno, bagnati, pesanti come una corda. Sotto di me c’è una persona.»", book="oblio", who="Dora Calvi"),
    Q("«Nell’altra stanza un telefono suona una suoneria da bambini, la stessa cantilena, ancora, ancora.»", book="oblio", who="Dora Calvi"),
    Q("«Mi sento come dopo il primo bagno dell’estate, quando ti asciughi al sole e non devi niente a nessuno. E rido. Sono io che rido.»", book="oblio", who="Dora Calvi"),
    dict(k="cta", text="Il romanzo *completo*. Ora su *Kindle*.", **KB, line="Puntata 1 gratis, PDF ed EPUB · <b>libri.diasio.ch</b>")],
   "Dopo un’estrazione, a Dora Calvi di solito resta addosso una briciola: un sapore, un jingle. Stavolta restano uno shampoo alla pesca, due mani sui polsi e una risata che è la sua.\nScorri: una scena della Puntata 1, senza spiegazioni.",
   "Carosello di sei slide su fondo scuro: un ricordo che Dora Calvi non riconosce come suo (shampoo alla pesca, capelli bagnati, una persona sotto di lei, una suoneria da bambini, una risata) e l’invito a leggere il romanzo su Amazon Kindle. L’Economia dell’Oblio."),
 P("n14-bug-kindle", "2026-10-17T17:36", "bug", "Lettori digitali + lettori noir (Kindle)",
   [dict(k="cta", text="Il condominio che *ti ascolta*. Ora su *Kindle*.", button="Disponibile su Amazon Kindle", line="Noir sociale · otto puntate · <b>libri.diasio.ch</b>")],
   "", "Locandina con la copertina de Il Bug della Trasparenza: «Il condominio che ti ascolta. Ora su Kindle.» Pulsante «Disponibile su Amazon Kindle», noir sociale in otto puntate, libri.diasio.ch.",
   ig="Il Bug della Trasparenza: un condominio d’élite, un’app che apre il cancello e a un certo punto comincia a dire la verità. Noir sociale in otto puntate.\nIl romanzo completo è su Amazon Kindle (link in bio). La Puntata 1 è gratis, in PDF o EPUB, senza iscrizione.",
   fb="Il Bug della Trasparenza: un condominio d’élite, un’app che apre il cancello e a un certo punto comincia a dire la verità. Noir sociale in otto puntate.\n\nIl romanzo completo è su Amazon Kindle: " + URL["bug"] + "\nLa Puntata 1 è gratis, in PDF o EPUB, senza iscrizione: " + SITO["bug"]),

 # ================= domenica 18 ottobre =================
 P("n15-oblio-otto-milioni", "2026-10-18T12:14", "oblio", "Satira del lavoro + fantascienza/distopia",
   [Q("«Ci hanno speso otto milioni. Io, per la cronaca, ho fatto il provino da comparsa e non mi hanno presa: troppo poco sollevata.»", book="oblio", who="Dora Calvi, sullo spot di Levia")],
   "Otto milioni per lo spot di un’azienda che toglie il dolore. E una comparsa scartata perché troppo poco sollevata.\nCosì Dora Calvi, tecnica estrattiva, ci presenta il mondo de L’Economia dell’Oblio. Puntata 1.",
   "Citazione su fondo scuro: «Ci hanno speso otto milioni. Io, per la cronaca, ho fatto il provino da comparsa e non mi hanno presa: troppo poco sollevata.» Dora Calvi, sullo spot di Levia. L’Economia dell’Oblio.", ironico=True),

 # ================= lunedì 19 ottobre =================
 P("n16-bug-bettarini", "2026-10-19T12:41", "bug", "Vita di condominio (relatable) + commenti",
   [Q("«I Bettarini, seduti in prima fila come sempre, annuirono insieme, come un solo corpo con due teste.»")],
   "Ogni assemblea ha la sua prima fila. Nel Bug della Trasparenza è questa: annuisce insieme, senza aver letto niente.\nSe riconosci i tuoi vicini, scrivilo nei commenti.",
   "Citazione su fondo scuro: «I Bettarini, seduti in prima fila come sempre, annuirono insieme, come un solo corpo con due teste.» Il Bug della Trasparenza, Puntata 1.", ironico=True),

 # ================= martedì 20 ottobre =================
 P("n17-bug-chiavi", "2026-10-20T12:07", "bug", "Lettori noir (core) + dialoghi (immagine IA)",
   [dict(k="photo", photo="Bug_B09_portiere-porta-vetri_9x16.jpg", pos=40,
         text="«Ho quelle che mi hanno dato. Non sempre sono le stesse cose.»", who="Yusuf Demir, il portiere")],
   "Il portiere di Residenza Meridiana non dice mai tutto. Questa è la sua risposta alla domanda sulle chiavi giuste, nell’atrio, dopo l’assemblea.\nDal Bug della Trasparenza, Puntata 1." + IA,
   "Immagine creata con l’IA: un portiere dietro la porta a vetri di un atrio, di notte. Sopra la frase: «Ho quelle che mi hanno dato. Non sempre sono le stesse cose.» Yusuf Demir, il portiere. Il Bug della Trasparenza."),

 # ================= mercoledì 21 ottobre =================
 P("n18-oblio-dove-leggi", "2026-10-21T12:49", "oblio", "Community (commenti) + lettori digitali",
   [dict(k="hook", kick="Domanda per chi legge", text="Dove leggi la *sera*?", sub="Sul divano, a letto, in treno, sul Kindle. Dimmelo nei *commenti*.", kindle=True)],
   "Domanda semplice: dove leggi la sera? Sul divano, a letto, in treno, sul Kindle?\nDimmelo nei commenti: leggo tutto e rispondo. Il Bug della Trasparenza e L’Economia dell’Oblio si leggono bene ovunque.",
   "Grafica scura con la scritta «Dove leggi la sera? Sul divano, a letto, in treno, sul Kindle. Dimmelo nei commenti.» e fascia ambra «Ora su Amazon Kindle»."),

 # ================= giovedì 22 ottobre =================
 P("n19-oblio-modulo", "2026-10-22T19:09", "oblio", "Fantascienza/distopia + mondo del lavoro",
   [dict(k="rows", title="CLASSIFICAZIONE · LUTTO", sub="MODULO DI STUDIO LEVIA · TECNICA ESTRATTIVA",
         rows=[("Tipo", "Lutto naturale"), ("Decorso", "Ospedaliero"), ("Elementi controversi", "Nessuno"), ("Presenza di colpa", "assente")],
         note="«Nessuno» dico, e spunto assente. A me arriva il quattro per cento sul venduto.")],
   "Il modulo di classificazione di un lutto ha una casella: presenza di colpa. Se la spunti, il lotto vale meno. Dora Calvi ci pensa un secondo, poi spunta «assente».\nUna scena della Puntata 1 de L’Economia dell’Oblio.",
   "Finto modulo di classificazione di uno studio Levia: lutto naturale, decorso ospedaliero, nessun elemento controverso, presenza di colpa assente. In fondo: «Nessuno» dico, e spunto assente. A me arriva il quattro per cento sul venduto. L’Economia dell’Oblio."),

 # ================= venerdì 23 ottobre =================
 P("n20-bug-elio-bassi", "2026-10-23T12:47", "bug", "Giornalismo d’inchiesta + lettori noir (carosello)",
   [dict(k="hook", kick=BUG, text="Perché Nadia è venuta a *vivere qui*.", sub="Un nome, un tetto, un articolo che le è costato la carriera. Scorri."),
    Q("«Ventisette anni prima, in quel palazzo aveva vissuto un uomo di nome Elio Bassi.»", who="Il Bug della Trasparenza · Puntata 1"),
    Q("«Programmatore, trentaquattro anni, morto in circostanze che il fascicolo della polizia chiamava “caduta accidentale dal tetto”.»"),
    Q("«Otto anni prima, Nadia aveva scritto l’unico articolo che qualcuno si fosse mai preso la briga di dedicare al caso, e le circostanze le aveva definite con più cautela.»"),
    Q("«L’articolo le era costato la carriera in redazione.»"),
    dict(k="cta", text="Noir sociale · *otto puntate*", **KB, line="Puntata 1 gratis, PDF ed EPUB · <b>libri.diasio.ch</b>")],
   "Ventisette anni prima, in quel palazzo, era morto un programmatore. Otto anni prima, Nadia aveva scritto l’articolo che le è costato la carriera. Per questo ha comprato un appartamento nel seminterrato.\nScorri: le frasi della Puntata 1 che mettono insieme i pezzi.",
   "Carosello di sei slide su fondo scuro: perché Nadia Colombo vive nel palazzo (Elio Bassi, programmatore, morto 27 anni prima; l’articolo di otto anni prima che le è costato la carriera) e l’invito a leggere Il Bug della Trasparenza su Amazon Kindle."),

 # ================= sabato 24 ottobre =================
 P("n21-bug-non-rimovibile", "2026-10-24T17:07", "bug", "Tech/privacy + lettori noir",
   [dict(k="notif", kick=BUG, app="Meridiana Life", when="Trasparenza attiva", title="Trasparenza Meridiana non può essere rimossa da un singolo utente.",
         text="Contattare l’amministrazione per la disattivazione collettiva.", sub="Amministrazione collettiva. Cioè *Cesare*.")],
   "Un messaggio che nessuno può cancellare: niente tasto elimina, solo l’avviso che serve una disattivazione collettiva, da chiedere all’amministrazione. Cioè a Cesare.\nL’app che ha appena smascherato il presidente adesso risponde al presidente. Dal Bug della Trasparenza, Puntata 1.",
   "Finto avviso dell’app Meridiana Life: «Trasparenza Meridiana non può essere rimossa da un singolo utente. Contattare l’amministrazione per la disattivazione collettiva.» Sotto: «Amministrazione collettiva. Cioè Cesare.» Il Bug della Trasparenza.", ironico=True),

 # ================= domenica 25 ottobre =================
 P("n22-oblio-undici-centimetri", "2026-10-25T12:52", "oblio", "Fantascienza/distopia + lettori thriller",
   [dict(k="quote", text="«Ho appena cucito undici centimetri di tempo nella testa di Gianfranco Merli. Lui non lo sa. Lui sente solo che è più leggero.»", who="Dora Calvi", kindle=True)],
   "Sul monitor la linea si spegne in un punto e riparte poco più giù, con un piccolo salto. Il cliente non se ne accorge: sente solo che è più leggero.\nIl lavoro di Dora Calvi, in tre frasi. L’Economia dell’Oblio, Puntata 1.",
   "Citazione su fondo scuro con fascia ambra «Ora su Amazon Kindle»: «Ho appena cucito undici centimetri di tempo nella testa di Gianfranco Merli. Lui non lo sa. Lui sente solo che è più leggero.» Dora Calvi. L’Economia dell’Oblio."),

 # ================= lunedì 26 ottobre =================
 P("n23-oblio-kindle", "2026-10-26T12:08", "oblio", "Lettori digitali + lettori thriller (Kindle)",
   [dict(k="cta", text="Chi dimentica diventa *innocente*. Ora su *Kindle*.", button="Disponibile su Amazon Kindle", line="Thriller psicologico · sei puntate · <b>libri.diasio.ch</b>")],
   "", "Locandina con la copertina de L’Economia dell’Oblio: «Chi dimentica diventa innocente. Ora su Kindle.» Pulsante «Disponibile su Amazon Kindle», thriller psicologico in sei puntate, libri.diasio.ch.",
   ig="L’Economia dell’Oblio è un thriller psicologico in sei puntate: Dora Calvi toglie il dolore ai clienti, finché trova nella propria testa i frammenti di un omicidio.\nIl romanzo completo è su Amazon Kindle (link in bio). La Puntata 1 è gratis, in PDF o EPUB.",
   fb="L’Economia dell’Oblio è un thriller psicologico in sei puntate: Dora Calvi toglie il dolore ai clienti, finché trova nella propria testa i frammenti di un omicidio.\n\nIl romanzo completo è su Amazon Kindle: " + URL["oblio"] + "\nLa Puntata 1 è gratis, in PDF o EPUB, senza iscrizione: " + SITO["oblio"]),

 # ================= martedì 27 ottobre =================
 P("n24-bug-garage", "2026-10-27T12:31", "bug", "Vita di condominio + lettori noir",
   [Q("«Il garage di Residenza Meridiana puzzava di cera per pavimenti anche al meno due, un dettaglio che nessun annuncio immobiliare avrebbe mai citato…»")],
   "Il garage di Residenza Meridiana, nel primo capoverso del romanzo: cera per pavimenti e un dettaglio che nessun annuncio immobiliare citerebbe.\nIl Bug della Trasparenza comincia così, undici giorni dopo il trasloco di Nadia.",
   "Citazione su fondo scuro: «Il garage di Residenza Meridiana puzzava di cera per pavimenti anche al meno due, un dettaglio che nessun annuncio immobiliare avrebbe mai citato…» Il Bug della Trasparenza, Puntata 1.", ironico=True),

 # ================= mercoledì 28 ottobre =================
 P("n25-oblio-suora", "2026-10-28T12:27", "oblio", "Satira del lavoro + dialoghi",
   [Q("«Pulito?»\n«Pulitissimo.»\n«Sì, come no.»\n«Hai la faccia da suora quando bari, Dora.»", book="oblio", who="Dora Calvi e Nico")],
   "Il collega di Dora Calvi sa quando bara. Il lutto «pulitissimo» di un cliente, per esempio.\nDialogo dalla Puntata 1 de L’Economia dell’Oblio: quattro battute e una diagnosi.",
   "Dialogo su fondo scuro: «Pulito?» «Pulitissimo.» «Sì, come no.» «Hai la faccia da suora quando bari, Dora.» Dora Calvi e Nico. L’Economia dell’Oblio.", ironico=True),

 # ================= giovedì 29 ottobre =================
 P("n26-oblio-firma", "2026-10-29T19:33", "oblio", "Fantascienza/distopia + lettori thriller",
   [Q("«Io ho la D più brutta d’Italia, una specie di gancio da macellaio. Questa è elegante. Sembra scritta da una che sapeva perfettamente cosa stava firmando.»", book="oblio", who="Dora Calvi, davanti a una firma")],
   "Una firma che sembra sua e non lo è: la D è troppo elegante. Dora Calvi lo nota prima di notare cos’altro non torna.\nPuntata 1 de L’Economia dell’Oblio. Tu ti fideresti dei tuoi ricordi?",
   "Citazione su fondo scuro: «Io ho la D più brutta d’Italia, una specie di gancio da macellaio. Questa è elegante. Sembra scritta da una che sapeva perfettamente cosa stava firmando.» Dora Calvi, davanti a una firma. L’Economia dell’Oblio.", ironico=True),

 # ================= venerdì 30 ottobre (due uscite) =================
 P("n27-bug-nadia", "2026-10-30T12:21", "bug", "Giornalismo d’inchiesta + lettori noir (immagine IA)",
   [dict(k="photo", photo="Bug_B12_nadia-loft_9x16.jpg", pos=35,
         text="«Da allora faceva la freelance, e da undici giorni faceva la vicina di casa sotto copertura di gente che, sospettava, sapeva più di quello che diceva.»",
         who="Nadia Colombo · " + BUG, kindle=True)],
   "Nadia Colombo vive nel seminterrato: ex giornalista, vicina di casa sotto copertura. Ha un motivo per essere lì e non l’ha detto a nessuno.\nQual è lo scopri nella Puntata 1 del Bug della Trasparenza." + IA,
   "Immagine creata con l’IA: una donna in un loft seminterrato con un portatile. Sopra, con fascia ambra «Ora su Amazon Kindle»: «Da allora faceva la freelance, e da undici giorni faceva la vicina di casa sotto copertura di gente che, sospettava, sapeva più di quello che diceva.» Il Bug della Trasparenza."),
 P("n28-oblio-strano", "2026-10-30T18:34", "oblio", "Psicologia/memoria (tono rispettoso) + lettori thriller",
   [dict(k="quote", text="«E mio padre?»\n«Cioè, so che è morto. So tutto. È come se me l’avessero detto.»\n«Le hanno detto bene»", who="Gianfranco Merli e Dora Calvi", kindle=True)],
   "Dopo l’estrazione, il cliente chiede di suo padre come si chiede l’orario di un treno. Sa che è morto. Gli hanno detto bene.\nDa L’Economia dell’Oblio, Puntata 1.",
   "Dialogo su fondo scuro con fascia ambra «Ora su Amazon Kindle»: «E mio padre?» «Cioè, so che è morto. So tutto. È come se me l’avessero detto.» «Le hanno detto bene.» Gianfranco Merli e Dora Calvi. L’Economia dell’Oblio."),

 # ================= sabato 31 ottobre =================
 P("n29-bug-presidente-parrocchia", "2026-10-31T17:29", "bug", "Vita di condominio + satira",
   [Q("«Presidente dell’assemblea da otto anni consecutivi, imprenditore immobiliare, il tipo che alla fine di ogni discorso pubblico ricordava a tutti quanto avesse donato alla parrocchia del quartiere.»")],
   "Il presidente dell’assemblea, in una frase: otto anni di mandato, un’impresa immobiliare e la donazione alla parrocchia che ricorda a ogni discorso.\nPoi arriva il punto cinque, il preventivo B, e il suo telefono vibra. Il Bug della Trasparenza, Puntata 1.",
   "Citazione su fondo scuro: «Presidente dell’assemblea da otto anni consecutivi, imprenditore immobiliare, il tipo che alla fine di ogni discorso pubblico ricordava a tutti quanto avesse donato alla parrocchia del quartiere.» Il Bug della Trasparenza, Puntata 1.", ironico=True),

 # ================= domenica 1 novembre =================
 P("n30-kindle-due-romanzi", "2026-11-01T12:26", "both", "Lettori digitali + tutti (Kindle)",
   [dict(k="cta", books=["bug", "oblio"], text="Due romanzi. *Amazon Kindle*.", button="Disponibili su Amazon Kindle", line="Puntata 1 di entrambi gratis · <b>libri.diasio.ch</b>")],
   "", "Locandina con le copertine dei due romanzi, Il Bug della Trasparenza e L’Economia dell’Oblio: «Due romanzi. Amazon Kindle.» Pulsante «Disponibili su Amazon Kindle», Puntata 1 di entrambi gratis su libri.diasio.ch.",
   ig="Due romanzi, un posto dove trovarli interi: Amazon Kindle.\nIl Bug della Trasparenza, noir sociale in otto puntate. L’Economia dell’Oblio, thriller psicologico in sei.\nLink in bio. La Puntata 1 di entrambi è gratis, in PDF o EPUB, senza iscrizione.",
   fb="Due romanzi, un posto dove trovarli interi: Amazon Kindle.\n\nIl Bug della Trasparenza, noir sociale in otto puntate: " + URL["bug"] + "\nL’Economia dell’Oblio, thriller psicologico in sei: " + URL["oblio"] + "\n\nLa Puntata 1 di entrambi è gratis, in PDF o EPUB, senza iscrizione: " + SITO["both"],
   tags_book="bug"),

 # ================= lunedì 2 novembre =================
 P("n31-oblio-regolamento", "2026-11-02T12:37", "oblio", "Satira del lavoro + lettori thriller",
   [Q("«Stamattina c’era una signora che voleva togliersi il proprio compleanno dei quarant’anni («ho preso troppa aria, capisce»), un ragazzo che voleva cancellare la prima comunione perché «dà una brutta impostazione al resto»…»", book="oblio", who="Dora Calvi, il mercoledì dei clienti strani")],
   "Il mercoledì, nello studio di Dora Calvi, è il giorno dei clienti strani: chi vuole togliersi il proprio compleanno, chi la prima comunione.\nSatira da sala d’attesa, poi il thriller. L’Economia dell’Oblio, Puntata 1.",
   "Citazione su fondo scuro: «Stamattina c’era una signora che voleva togliersi il proprio compleanno dei quarant’anni («ho preso troppa aria, capisce»), un ragazzo che voleva cancellare la prima comunione perché «dà una brutta impostazione al resto»…» Dora Calvi. L’Economia dell’Oblio.", ironico=True),
]
