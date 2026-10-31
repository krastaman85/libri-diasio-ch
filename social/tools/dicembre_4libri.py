# Post nuovi per «L'Aritmetica del Consenso» e «Vuoto a rendere» (dicembre 2026), aggiunti il 31/10/2026 per riequilibrare
# il calendario sui quattro libri. Citazioni testuali dalle Puntata 1 (verificate parola per parola sugli EPUB completi).
# Scene IA (Firefly Image 5) in social/img/scene/. Firma una sola volta: il nome dell'autore resta solo sulla copertina.
# Letto da carousel.py (load) con exec; le immagini vanno in social/img/nuovi/ (Storie in social/img/story/).
# Date e voci di calendario: social/tools/riequilibrio_quattro_libri.py (when=None qui).

ARI, VUO = "L’Aritmetica del Consenso", "Vuoto a rendere"
Q = lambda text, **kw: dict(k="quote", text=text, **kw)
FOTO = lambda photo, text, who, pos=40, alto=False: dict(k="photo", photo=photo, pos=pos, text=text, who=who, alto=alto)  # alto: frase in alto, soggetto della foto visibile sotto

AMZ = {"aritmetica": "https://www.amazon.it/dp/B0HM3Y19B6", "vuoto": "https://www.amazon.it/dp/B0HM4HFK34"}
SITO = {"aritmetica": "https://libri.diasio.ch/aritmetica/", "vuoto": "https://libri.diasio.ch/vuoto/"}
CARTA_V = "https://www.amazon.it/dp/B0HMFNKKJ2"
# Hashtag: solo il vocabolario dell'utente (IG 5, FB 10); satira e #RomanzoSatirico solo per Vuoto, #Ironia solo sui post ironici.
TAG = {"aritmetica": ("#NoirItaliano #LetteraturaNoir #BookstagramItalia #ScrittoriItaliani #Ticino",
                      "#NoirItaliano #RomanzoNoir #LetteraturaNoir #GialloItaliano #BookstagramItalia #ConsigliDiLettura #ScrittoriItaliani #Ticino #SvizzeraItaliana #CulturaTicino"),
       "aritmetica-2": ("#RomanzoNoir #GialloItaliano #ConsigliDiLettura #IoLeggo #CulturaTicino",
                        "#RomanzoNoir #NoirItaliano #ThrillerItaliano #AltaTensione #LibriDaLeggere #BookstagramItalia #EditoriaItaliana #ScrittoriSvizzeri #Ticino #LeggereInSvizzera"),
       "aritmetica-ironico": ("#RomanzoNoir #Ironia #LibriDaLeggere #ScrittoriEmergenti #SvizzeraItaliana",
                              "#RomanzoNoir #NoirItaliano #LetteraturaNoir #Ironia #UmorismoNero #LibriDaLeggere #ConsigliDiLettura #ScrittoriEmergenti #Ticino #LeggereInSvizzera"),
       "vuoto": ("#RomanzoSatirico #UmorismoNero #BookstagramItalia #LibriDaLeggere #Ticino",
                 "#RomanzoSatirico #Satira #UmorismoNero #CommediaNera #BookstagramItalia #ConsigliDiLettura #LibriDaLeggere #ScrittoriItaliani #Ticino #LeggereInSvizzera"),
       "vuoto-2": ("#Satira #CommediaNera #ConsigliDiLettura #IoLeggo #SvizzeraItaliana",
                   "#RomanzoSatirico #LettureDivertenti #Ironia #Satira #IoLeggo #EditoriaItaliana #ScrittoriEmergenti #SvizzeraItaliana #CulturaTicino #BookstagramSvizzera")}


def V(id, book, slides, alt, testo, seg, theme=None, tag=None):
    """testo = apertura della didascalia; poi riga Kindle (IG: link in bio; FB: link diretto), Kindle Unlimited, inizio gratis, hashtag."""
    ig_t, fb_t = TAG[tag or book]
    titolo = ARI if book == "aritmetica" else VUO
    carta = " Anche in cartaceo." if book == "vuoto" else ""
    ig = f"{testo}\n\n{titolo} è su Amazon Kindle: link in bio.{carta}\nIncluso in Kindle Unlimited. L’inizio è gratis su libri.diasio.ch.\n\n{ig_t}"
    fb = (f"{testo}\n\n{titolo} su Amazon Kindle: {AMZ[book]}" + (f"\nCartaceo: {CARTA_V}" if book == "vuoto" else "")
          + f"\nIncluso in Kindle Unlimited.\nL’inizio è gratis, in PDF o EPUB, senza iscrizione: {SITO[book]}\n\n{fb_t}")
    return dict(id=id, book=book, flat=True, slides=slides, alt=alt, theme=theme, caption=ig, caption_fb=fb, seg=seg, when=None)


ITEMS = [
 # ---------- L'Aritmetica del Consenso ----------
 V("x01-aritmetica-signora", "aritmetica",
   [FOTO("Aritmetica_signora-mano_9x16.jpg",
         "«Poi, tre mesi fa, la signora ha smesso di ricordare le cose in ordine. Ha cominciato a ricordarle *tutte*.»",
         ARI + " · Puntata 1", pos=100, alto=True)],
   "Immagine creata con l’IA: la mano di una signora anziana, con un anello, posata su un tavolo scuro accanto a un vassoio d’argento con un mandarino. "
   "Sopra, la frase del romanzo: «Poi, tre mesi fa, la signora ha smesso di ricordare le cose in ordine. Ha cominciato a ricordarle tutte.» L’Aritmetica del Consenso.",
   "Una famiglia ticinese, una matriarca che ricorda troppo, un ghostwriter pagato per mettere in ordine i ricordi giusti.",
   "Noir dinastico + lettori di saghe familiari", theme="green"),
 V("x02-aritmetica-ghostwriter", "aritmetica",
   [FOTO("Aritmetica_ghostwriter_9x16.jpg",
         "«Faccio il ghostwriter. Scrivo le vite degli altri e poi sparisco, come l’idraulico: nessuno ringrazia l’idraulico, si ringrazia il *rubinetto*.»",
         ARI + " · Puntata 1", pos=35)],
   "Immagine creata con l’IA: un uomo in giacca scrive su un quaderno; nel taschino, un piccolo registratore. "
   "Sopra, la frase del romanzo: «Faccio il ghostwriter. Scrivo le vite degli altri e poi sparisco, come l’idraulico: nessuno ringrazia l’idraulico, si ringrazia il rubinetto.»",
   "Il narratore de L’Aritmetica del Consenso fa un mestiere invisibile per definizione. In una famiglia ricca, è un vantaggio.",
   "Satira del lavoro + lettori noir", theme="green", tag="aritmetica-ironico"),
 V("x03-aritmetica-sala-lago", "aritmetica",
   [FOTO("Aritmetica_sala-lago_9x16.jpg",
         "«Quattro persone in una sala riunioni con vista sul lago, che è la vista di tutti i soldi ticinesi, solo guardata da più in *alto*.»",
         ARI + " · Puntata 1", pos=20, alto=True)],
   "Immagine creata con l’IA: una sala riunioni di vetro all’ultimo piano, sedie di pelle vuote, il lago e le montagne al tramonto. "
   "Sopra, la frase del romanzo sulla vista di tutti i soldi ticinesi. L’Aritmetica del Consenso.",
   "Quattro persone, un contratto, e un lago che non si guarda gratis.",
   "Lettori noir + Ticino", theme="green", tag="aritmetica-2"),
 V("x04-aritmetica-due-mani", "aritmetica",
   [dict(k="hook", kick=ARI, text="Il ghostwriter ha *due mani*.", sub="Una scrive per la famiglia. L’altra no. Scorri."),
    Q("La destra tiene la penna sopra un quaderno che serve da *alibi*, la sinistra stringe in tasca un registratore grande come un accendino.", who=ARI + " · Puntata 1"),
    Q("La penna scrive «tempo: sereno». Il *registratore* scrive tutto il resto.", who=ARI + " · Puntata 1"),
    Q("In una casa dove ogni cosa ha un prezzo, è l’unica persona che non so come *valutare*.", who="Il ghostwriter, sull’infermiera"),
    dict(k="cta", text="Noir dinastico · *sei puntate*", button="Disponibile su Amazon Kindle", line="L’inizio è gratis · <b>libri.diasio.ch</b>")],
   "Carosello di cinque slide su fondo verde scuro: il ghostwriter ha due mani, tre frasi dalla Puntata 1 de L’Aritmetica del Consenso e la copertina con il pulsante Amazon Kindle.",
   "Una penna per la versione ufficiale, un registratore per tutto il resto. Scorri: tre frasi dalla Puntata 1.",
   "Carosello · lettori noir", theme="green"),
 # ---------- Vuoto a rendere ----------
 V("x05-vuoto-cane", "vuoto",
   [FOTO("Vuoto_cane-monitor_9x16.jpg", "Il cane non era suo. Lo aveva scelto l’algoritmo: i cani fanno *engagement*.", VUO + " · Puntata 1", pos=20)],
   "Immagine creata con l’IA: in una sala del commiato vuota, un monitor mostra la foto sorridente di un cane. "
   "Sopra, la frase del romanzo: «Il cane non era suo. Lo aveva scelto l’algoritmo: i cani fanno engagement.» Vuoto a rendere.",
   "A Sordina il commiato si progetta come una campagna. Anche il cane sullo schermo.",
   "Satira + lettori di commedia nera", theme="vuoto"),
 V("x06-vuoto-wifi", "vuoto",
   [FOTO("Vuoto_wifi_9x16.jpg",
         "Il defunto non risultava iscritto a nessuna parrocchia, e in un Cantone dove per secoli l’ultimo saluto l’aveva organizzato la Chiesa, Sordina offriva la versione senza ostie e con il *wifi*.",
         VUO + " · Puntata 1", pos=100, alto=True)],
   "Immagine creata con l’IA: un router con le luci accese su un leggio di una sala del commiato, accanto ai fiori bianchi. "
   "Sopra, la frase del romanzo sul commiato laico «senza ostie e con il wifi». Vuoto a rendere.",
   "Il commiato laico, versione Sordina: niente ostie, connessione garantita.",
   "Satira + Ticino", theme="vuoto", tag="vuoto-2"),
 V("x07-vuoto-predefinito", "vuoto",
   [Q("Riservato è il valore *predefinito*: non offende nessuno e non si può smentire.", who=VUO + " · Puntata 1")],
   "Citazione su fondo scuro con l’impronta di Vuoto a rendere: «Riservato è il valore predefinito: non offende nessuno e non si può smentire.»",
   "Nel modulo di commemorazione c’è una casella per tutto. Anche per non dire niente.",
   "Satira del lavoro", theme="vuoto", tag="vuoto-2"),
 V("x08-vuoto-puntualita", "vuoto",
   [Q("Il morto arrivò alle 10:40, con venti minuti d’anticipo. Per un defunto è il massimo della *puntualità*.", who=VUO + " · La prima riga")],
   "Citazione su fondo scuro con l’impronta di Vuoto a rendere: «Il morto arrivò alle 10:40, con venti minuti d’anticipo. Per un defunto è il massimo della puntualità.»",
   "La prima riga di Vuoto a rendere. Il resto è all’altezza.",
   "Satira + lettori di commedia nera", theme="vuoto"),
]

STORIES = [
 dict(id="sx1-vuoto-regolamento", book="vuoto", story=True, theme="vuoto", seg="Storia · Vuoto a rendere", when=None,
      slides=[Q("Gli occhi asciutti come un *regolamento*.", who=VUO)]),
 dict(id="sx2-aritmetica-lago", book="aritmetica", story=True, theme="green", seg="Storia · L’Aritmetica del Consenso", when=None,
      slides=[Q("Fuori, il lago, che non si può guardare senza sentirne il *prezzo*.", who=ARI)]),
]
ITEMS += STORIES
