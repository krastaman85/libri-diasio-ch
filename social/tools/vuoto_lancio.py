# Lancio di «Vuoto a rendere» (prenotazione su Amazon Kindle, uscita venerdì 23 ottobre 2026, ASIN B0HM4HFK34): 12 post, 2 Storie, 3 Reel.
# Citazioni testuali dalla Puntata 1 (download/vuoto-a-rendere-puntata-1.pdf). *parola* = parola in rosso. Tema grafico «vuoto» di carousel.py
# (grafite, rosso della sedia, IBM Plex Mono). Letto da carousel.py con exec: niente import relativi.
# `python carousel.py v` rende le immagini in social/img/nuovi/ (Storie in social/img/story/), `python carousel.py --calendar` aggiunge le voci a calendar.json.
# I Reel (v01-v03) si rigenerano con reels-src/index-vuoto.html (vedi README).
import hashlib
import random
import re
from pathlib import Path

SITO_V = "https://libri.diasio.ch/vuoto/"
AMAZON_V = "https://www.amazon.it/dp/B0HM4HFK34"      # scheda di prenotazione: va controllato che sia online prima del merge
# Fonte unica: se js/config.js ha il link di Vuoto, la scheda Amazon è online e le didascalie prima del 23/10 parlano di prenotazione e portano il link.
_cfg = (Path(__file__).resolve().parent.parent.parent / "js" / "config.js").read_text(encoding="utf-8")
LIVE = re.search(r'vuoto:\s*\{\s*amazon:\s*"https://', _cfg) is not None


def _rng(pid, kind):
    return random.Random(int(hashlib.sha256((pid + kind).encode()).hexdigest(), 16))


# Vocabolario dell'utente: satira (genere) + tono ironico solo sui post ironici + community + geografia.
GENERE = ["#RomanzoSatirico", "#Satira", "#LettureDivertenti"]
TONO = ["#Ironia", "#UmorismoNero", "#CommediaNera"]
COMMUNITY = ["#BookstagramItalia", "#ConsigliDiLettura", "#LibriDaLeggere"]
SPECIALI = ["#IoLeggo", "#ScrittoriItaliani", "#ScrittoriEmergenti", "#EditoriaItaliana"]
GEO = ["#Ticino", "#SvizzeraItaliana", "#ScrittoriSvizzeri", "#LeggereInSvizzera", "#CulturaTicino", "#BookstagramSvizzera"]


def tag_ig(pid, ironico=False):
    r = _rng(pid, "ig")
    primo = r.choice(["#RomanzoSatirico", "#Satira"])
    secondo = r.choice(TONO) if ironico else r.choice([g for g in GENERE if g != primo])
    return " ".join([primo, secondo, r.choice(COMMUNITY), r.choice(SPECIALI), r.choice(GEO)])


def tag_fb(pid, ironico=False):
    r = _rng(pid, "fb")
    n_gen, n_ton, n_com, n_geo = (2, 2, 2, 3) if ironico else (3, 0, 3, 3)
    t = r.sample(GENERE, n_gen) + (r.sample(TONO, n_ton) if n_ton else []) + r.sample(COMMUNITY, n_com) \
        + [r.choice(SPECIALI)] + r.sample(GEO, n_geo)
    return " ".join(t)


# Righe finali. Prima del 23/10 il libro si prenota; dal 23/10 è in vendita.
if LIVE:
    PRE_IG = "In prenotazione su Amazon Kindle: esce il 23 ottobre (link in bio). La Puntata 1 è gratis, in PDF o EPUB, senza iscrizione."
    PRE_FB = f"In prenotazione su Amazon Kindle, esce il 23 ottobre: {AMAZON_V}\nLa Puntata 1 è gratis, in PDF o EPUB, senza iscrizione: {SITO_V}"
else:
    PRE_IG = "Esce su Amazon Kindle il 23 ottobre. La Puntata 1 è gratis, in PDF o EPUB, senza iscrizione (link in bio)."
    PRE_FB = f"Esce su Amazon Kindle il 23 ottobre. La Puntata 1 è gratis, in PDF o EPUB, senza iscrizione: {SITO_V}"
POST_IG = "Il romanzo completo, in dieci capitoli, è su Amazon Kindle (link in bio). La Puntata 1 è gratis, in PDF o EPUB, senza iscrizione."
POST_FB = f"Il romanzo completo, in dieci capitoli, è su Amazon Kindle: {AMAZON_V}\nLa Puntata 1 è gratis, in PDF o EPUB, senza iscrizione: {SITO_V}"
KP = "Su Kindle dal 23 ottobre"          # fascia sull'immagine prima dell'uscita
KD = "Su Amazon Kindle"             # fascia sull'immagine dopo l'uscita
ES = "Esce il 23 ottobre"


def V(id, when, seg, slides, body, alt, ironico=False, post=False):
    riga_ig, riga_fb = (POST_IG, POST_FB) if post else (PRE_IG, PRE_FB)
    cap = body + "\n" + riga_ig + "\n\n" + tag_ig(id, ironico)
    cfb = body + "\n\n" + riga_fb + "\n\n" + tag_fb(id, ironico)
    return dict(id=id, when=when, book="vuoto", seg=seg, flat=True, theme="vuoto", slides=slides,
                caption=cap, caption_fb=cfb, alt=alt, ironico=ironico)


PUNT1 = "Vuoto a rendere · Puntata 1"

ITEMS = [

 V("v01-vuoto-prenotazione", "2026-10-10T17:21", "Annuncio · In prenotazione (locandina)",
   [dict(k="cta", books=["vuoto"], text="Esce il *23 ottobre*", button="Su Amazon Kindle dal 23 ottobre", line="Esce il 23 ottobre · <b>libri.diasio.ch</b>")],
   "Vuoto a rendere, romanzo satirico di D. Iasio, esce il 23 ottobre su Amazon Kindle.\nDario progetta funerali che sembrano pieni: sale con diffusore al cedro, comparse pagate e un indice che misura quanto un addio somigli a un addio.\nQuaranta sedie, nove presenti, sei pagate.",
   "Locandina su fondo grafite con la copertina di Vuoto a rendere (quaranta sedie, una rossa): «Esce il 23 ottobre», pulsante «Su Amazon Kindle dal 23 ottobre»."),

 V("v02-vuoto-listino", "2026-10-11T12:17", "Il listino (carosello)",
   [dict(k="hook", kick="Vuoto a rendere", text="Un funerale a *listino*", sub="Voce 01: Sala Ulivo, tre ore.", kindle=KP),
    dict(k="doc", kick="Vuoto a rendere", name="SORDINA · LISTINO · VOCE 01",
         lines=["Sala Ulivo, allestimento e tre ore di disponibilità: *CHF 1’200.00*", "Incluso: diffusione di essenze al cedro, playlist «Commiato Pianissimo», registro delle presenze."], kindle=KP),
    dict(k="rows", title="Dal manuale di Dario", sub="Il lutto in aula", rows=[("In aula, per ora", "CHF 25"), ("Festivi, in più", "+ CHF 5"), ("Tariffa lacrime", "+ CHF 8")],
         note="«Espressione raccolta, mai sofferente. Il sofferente mette a disagio.»", kindle=KP),
    dict(k="quote", text="«Sembra. Il prodotto era quello. Non il funerale: il sembra.»", who=PUNT1, kindle=KP),
    dict(k="cta", books=["vuoto"], text="Esce il *23 ottobre*", button="Su Amazon Kindle dal 23 ottobre", line="Puntata 1 gratis · <b>libri.diasio.ch</b>")],
   "Voce 01 del listino: Sala Ulivo, allestimento e tre ore di disponibilità, 1’200 franchi. In aula, per imparare l’espressione giusta, 25 franchi l’ora.\n«Sembra. Il prodotto era quello. Non il funerale: il sembra.»\nVuoto a rendere, romanzo satirico di D. Iasio, esce il 23 ottobre.",
   "Carosello di cinque slide su fondo grafite: «Un funerale a listino»; la voce 01 del listino della Sala Ulivo (1’200 franchi); le tariffe del manuale (25 franchi l’ora in aula, 5 in più nei festivi, 8 per le lacrime); la frase «Sembra. Il prodotto era quello. Non il funerale: il sembra.»; invito a prenotare, esce il 23 ottobre."),

 V("v04-vuoto-cane", "2026-10-13T12:41", "Citazione ironica · In prenotazione (grafica)",
   [dict(k="quote", text="«Nell’ultima il vecchio sorrideva a un cane. Il cane non era suo. Lo aveva scelto l’algoritmo: i cani fanno engagement.»", who=PUNT1, kindle=ES)],
   "«Nell’ultima il vecchio sorrideva a un cane. Il cane non era suo. Lo aveva scelto l’algoritmo: i cani fanno engagement.»\nVuoto a rendere esce il 23 ottobre.",
   "Frase su fondo grafite: «Nell’ultima il vecchio sorrideva a un cane. Il cane non era suo. Lo aveva scelto l’algoritmo: i cani fanno engagement.» Vuoto a rendere, Puntata 1. Fascia: «Esce il 23 ottobre».", ironico=True),

 V("v06-vuoto-presenti", "2026-10-15T12:27", "Chi c'è in sala (carosello)",
   [dict(k="hook", kick="Vuoto a rendere", text="Nove *presenti*", sub="Quaranta sedie. Sei pagate.", kindle=KP),
    dict(k="quote", text="«Chi piange davvero non sa dove mettere le mani»", who=PUNT1, kindle=KP),
    dict(k="quote", text="«Tariffa lacrime: otto franchi in più.»", who=PUNT1, sub="Ottavio, settantun anni, *piangeva* a comando.", kindle=KP),
    dict(k="quote", text="«Il terzo sedeva in ultima fila e non era in lista.»", who=PUNT1, kindle=KP),
    dict(k="cta", books=["vuoto"], text="Chi era la *terza*?", button="Leggi la Puntata 1 gratis", line="Esce il 23 ottobre · <b>libri.diasio.ch</b>")],
   "Nove presenti, sei pagate. Chi piange davvero non sa dove mettere le mani; le comparse sì, le hanno provate in aula.\nPoi c’è il terzo che non era in lista, in ultima fila.\nVuoto a rendere, romanzo satirico di D. Iasio, esce il 23 ottobre.",
   "Carosello di cinque slide su fondo grafite: «Nove presenti, quaranta sedie, sei pagate»; «Chi piange davvero non sa dove mettere le mani»; «Tariffa lacrime: otto franchi in più»; «Il terzo sedeva in ultima fila e non era in lista»; invito a leggere la Puntata 1 gratis, esce il 23 ottobre."),

 V("v08-vuoto-scheda", "2026-10-17T17:44", "La scheda del defunto (grafica in stile registro)",
   [dict(k="doc", kick="Vuoto a rendere", name="SORDINA · SOLDATI ALDO, N. 1947",
         lines=["Deceduto: 31 agosto.", "Ritrovamento: 14 settembre.", "Referente: Soldati Marco (figlio), Rotterdam (NL).", "Stato: *non presente*."], kindle=KP)],
   "Deceduto: 31 agosto. Ritrovamento: 14 settembre. Referente: il figlio, a Rotterdam. Stato: non presente.\nÈ la scheda che Dario apre dopo la cerimonia. Vuoto a rendere esce il 23 ottobre.",
   "Finta scheda su fondo grafite: «Soldati Aldo, n. 1947. Deceduto: 31 agosto. Ritrovamento: 14 settembre. Referente: Soldati Marco (figlio), Rotterdam. Stato: non presente.» Fascia: «Su Kindle dal 23 ottobre»."),

 V("v09-vuoto-domanda", "2026-10-18T12:09", "Domanda ai lettori · In prenotazione (grafica)",
   [dict(k="quote", text="«Chi siederebbe in prima fila al tuo funerale, e da quanto non gli dai un motivo per starci?»", who=PUNT1, kindle=ES)],
   "«Chi siederebbe in prima fila al tuo funerale, e da quanto non gli dai un motivo per starci?»\nLa domanda che chiude la Puntata 1 di Vuoto a rendere. Rispondi nei commenti.",
   "Frase su fondo grafite: «Chi siederebbe in prima fila al tuo funerale, e da quanto non gli dai un motivo per starci?» Vuoto a rendere, Puntata 1. Fascia: «Esce il 23 ottobre»."),

 V("v10-vuoto-incipit", "2026-10-20T12:22", "Prime righe (carosello)",
   [dict(k="quote", text="«Il morto arrivò alle 10:40, con venti minuti d’anticipo. Per un defunto è il massimo della puntualità. I vivi, invece, latitavano.»", who=PUNT1, foot="Puntata 1 gratis · libri.diasio.ch"),
    dict(k="quote", text="«Dario contò le sedie: quaranta. Contò le persone: nove. Sei erano sue.»", who=PUNT1, foot="Puntata 1 gratis · libri.diasio.ch"),
    dict(k="quote", text="«La Sala Ulivo era un capolavoro. Legno chiaro, luce calda, un diffusore al cedro che spargeva odore di spa svizzera.»", who=PUNT1, foot="Puntata 1 gratis · libri.diasio.ch"),
    dict(k="quote", text="«Poi, per la prima volta in sei anni, si chiese chi fosse il morto.»", who=PUNT1, foot="Puntata 1 gratis · libri.diasio.ch"),
    dict(k="cta", books=["vuoto"], text="Continua con la Puntata *1*", button="Leggi la Puntata 1 gratis", line="PDF ed EPUB · <b>libri.diasio.ch</b>")],
   "Le prime righe di Vuoto a rendere, una alla volta.\nUn funerale con quaranta sedie e nove presenti, e un uomo che per la prima volta in sei anni si chiede chi fosse il morto. Esce il 23 ottobre.",
   "Carosello di cinque slide su fondo grafite con le prime righe di Vuoto a rendere: il morto che arriva con venti minuti d’anticipo; le quaranta sedie e le nove persone; la Sala Ulivo; Dario che si chiede chi fosse il morto; invito a leggere la Puntata 1 gratis."),

 V("v13-vuoto-da-oggi", "2026-10-23T12:14", "Lancio · Da oggi (locandina)",
   [dict(k="cta", books=["vuoto"], text="Da *oggi*", button="Su Amazon Kindle", line="Puntata 1 gratis · <b>libri.diasio.ch</b>")],
   "Da oggi su Amazon Kindle: Vuoto a rendere, romanzo satirico di D. Iasio in dieci capitoli.\nDario progetta funerali che sembrano pieni. Poi si chiede chi fosse il morto.",
   "Locandina su fondo grafite con la copertina di Vuoto a rendere (quaranta sedie, una rossa): «Da oggi», pulsante «Su Amazon Kindle», Puntata 1 gratis su libri.diasio.ch.", post=True),

 V("v15-vuoto-fazzoletto", "2026-10-24T12:31", "Citazione · È uscito (grafica)",
   [dict(k="quote", text="«Sulla sedia restò un fazzoletto.»", who=PUNT1, sub="Una signora, ultima fila, non in lista.", kindle=KD)],
   "«Sulla sedia restò un fazzoletto.»\nVuoto a rendere, di D. Iasio, è uscito.",
   "Frase su fondo grafite: «Sulla sedia restò un fazzoletto.» Vuoto a rendere, Puntata 1. Fascia: «Su Amazon Kindle».", post=True),

 V("v16-vuoto-troverai", "2026-10-25T20:12", "Cosa troverai (carosello)",
   [dict(k="step", kick="Vuoto a rendere", n="1", title="Un mestiere che *sembra*", text="Dario progetta funerali che sembrano pieni: sale con diffusore al cedro, comparse pagate, un indice del *decoro*."),
    dict(k="step", kick="Vuoto a rendere", n="2", title="Un morto da *ventitré* giorni", text="Aldo Soldati se ne va senza che nessuno se ne accorga, finché qualcuno lo sente dall’*odore*."),
    dict(k="step", kick="Vuoto a rendere", n="3", title="Una signora in *ultima fila*", text="Non è in lista, non firma il registro, esce prima della fine e lascia un *fazzoletto*."),
    dict(k="hook", kick="È uscito", text="Su *Kindle*", sub="Puntata 1 gratis: link in bio.", kindle=KD)],
   "Un mestiere che sembra, un morto da ventitré giorni, una signora in ultima fila.\nVuoto a rendere, romanzo satirico di D. Iasio, è uscito.",
   "Carosello di quattro slide su fondo grafite: 1 «Un mestiere che sembra»; 2 «Un morto da ventitré giorni»; 3 «Una signora in ultima fila»; 4 «È uscito, su Kindle». Vuoto a rendere.", post=True),

 V("v17-vuoto-regia", "2026-10-27T12:46", "Dialogo · È uscito (grafica in stile registro)",
   [dict(k="doc", kick="Vuoto a rendere", name="REGIA · STREAMING",
         lines=["Spettatori connessi: *1*", "Località: Rotterdam", "Durata collegamento: *31 minuti*"], kindle=KD)],
   "«La regia non si conta.» «Lo so.» «E allora perché mi guardi?» «Per abitudine.»\nVuoto a rendere, romanzo satirico di D. Iasio, è uscito.",
   "Finta schermata su fondo grafite, «Regia · streaming»: spettatori connessi 1, località Rotterdam, durata del collegamento 31 minuti. Fascia: «Su Amazon Kindle».", post=True),

 # Storie (solo immagine, senza link)
 dict(id="vs01-vuoto-mani", when="2026-10-14T19:36", book="vuoto", seg="Storia · In prenotazione", story=True, theme="vuoto",
      slides=[dict(k="quote", text="«Chi piange davvero non sa dove mettere le mani.»", who=PUNT1, sub="Esce il *23 ottobre*")]),
 dict(id="vs02-vuoto-domani", when="2026-10-22T12:38", book="vuoto", seg="Storia · Domani", story=True, theme="vuoto",
      slides=[dict(k="hook", kick="Vuoto a rendere", text="Domani\n*esce*", sub="Su Amazon Kindle.")]),
]

if LIVE:
    RPRE_IG = "«Vuoto a rendere», romanzo satirico di D. Iasio, è in prenotazione su Amazon Kindle: esce il 23 ottobre (link in bio). La Puntata 1 è gratis, in PDF o EPUB, senza iscrizione."
    RPRE_FB = f"«Vuoto a rendere», romanzo satirico di D. Iasio, è in prenotazione su Amazon Kindle, esce il 23 ottobre: {AMAZON_V}\nLa Puntata 1 è gratis, in PDF o EPUB, senza iscrizione: {SITO_V}"
else:
    RPRE_IG = "«Vuoto a rendere», romanzo satirico di D. Iasio, esce su Amazon Kindle il 23 ottobre. La Puntata 1 è gratis, in PDF o EPUB, senza iscrizione (link in bio)."
    RPRE_FB = f"«Vuoto a rendere», romanzo satirico di D. Iasio, esce su Amazon Kindle il 23 ottobre. La Puntata 1 è gratis, in PDF o EPUB, senza iscrizione: {SITO_V}"
REELS = [
 dict(id="v01-listino", tipo="reel", quando="2026-10-12T12:33", segmento="Reel · Satira del lavoro (il listino)", video="social/video/v01-listino.mp4",
      didascalia="Voce 01 del listino: Sala Ulivo, tre ore di disponibilità, 1’200 franchi. Incluso: essenze al cedro e un registro delle presenze.\n«Il cliente ha avuto esattamente quello che ha pagato.»\n" + RPRE_IG + "\n\n#RomanzoSatirico #UmorismoNero #BookstagramItalia #IoLeggo #Ticino",
      didascalia_fb="Voce 01 del listino: Sala Ulivo, tre ore di disponibilità, 1’200 franchi. Incluso: essenze al cedro e un registro delle presenze.\n«Il cliente ha avuto esattamente quello che ha pagato.»\n\n" + RPRE_FB + "\n\n#RomanzoSatirico #Satira #Ironia #CommediaNera #BookstagramItalia #ConsigliDiLettura #IoLeggo #Ticino #SvizzeraItaliana #LeggereInSvizzera"),
 dict(id="v02-sedie", tipo="reel", quando="2026-10-16T18:19", segmento="Reel · Le quaranta sedie", video="social/video/v02-sedie.mp4",
      didascalia="Quaranta sedie, nove presenti, sei pagate. Chi siederebbe in prima fila al tuo funerale, e da quanto non gli dai un motivo per starci?\n" + RPRE_IG + "\n\n#RomanzoSatirico #LettureDivertenti #ConsigliDiLettura #ScrittoriItaliani #CulturaTicino",
      didascalia_fb="Quaranta sedie, nove presenti, sei pagate. Chi siederebbe in prima fila al tuo funerale, e da quanto non gli dai un motivo per starci?\n\n" + RPRE_FB + "\n\n#RomanzoSatirico #Satira #LettureDivertenti #BookstagramItalia #ConsigliDiLettura #LibriDaLeggere #ScrittoriItaliani #Ticino #ScrittoriSvizzeri #CulturaTicino"),
 dict(id="v03-regia", tipo="reel", quando="2026-10-21T19:41", segmento="Reel · La regia (Rotterdam)", video="social/video/v03-regia.mp4",
      didascalia="Spettatori connessi: 1. Località: Rotterdam. Durata del collegamento: 31 minuti.\n«La regia non si conta.» «Lo so.» «E allora perché mi guardi?» «Per abitudine.»\n" + RPRE_IG + "\n\n#Satira #CommediaNera #BookstagramItalia #EditoriaItaliana #SvizzeraItaliana",
      didascalia_fb="Spettatori connessi: 1. Località: Rotterdam. Durata del collegamento: 31 minuti.\n«La regia non si conta.» «Lo so.» «E allora perché mi guardi?» «Per abitudine.»\n\n" + RPRE_FB + "\n\n#RomanzoSatirico #Satira #UmorismoNero #CommediaNera #BookstagramItalia #ConsigliDiLettura #IoLeggo #Ticino #ScrittoriSvizzeri #LeggereInSvizzera"),
]

# Post di solo testo per la Pagina Facebook (letti da carousel.py --calendar). Venerdì 23 ottobre, sera.
TESTI = [
 ("v14-vuoto-lettera", "2026-10-23T18:27", "Testo · Lancio",
  "Vuoto a rendere è uscito.\nÈ un romanzo satirico in dieci capitoli, per adulti. Dario progetta funerali che sembrano pieni: sale con diffusore al cedro, comparse pagate, un indice che misura quanto un addio somigli a un addio. Poi, a una cerimonia con quaranta sedie e nove presenti, si chiede chi fosse il morto.\nLa Puntata 1 è gratis, in PDF o EPUB, senza iscrizione: " + SITO_V + "\nIl romanzo completo è su Amazon Kindle: " + AMAZON_V,
  SITO_V),
]
TESTI = [(i, w, g, t + "\n\n" + tag_fb(i), l) for i, w, g, t, l in TESTI]
