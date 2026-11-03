# Piano D.IAsio (approvato il 3/11/2026, in uscita dal 16/11 al 13/12/2026): un profilo unico _d.iasio_, un post al giorno + la frase delle 23:10.
# Rubriche: lunedì e giovedì «Moduli ticinesi» (finti documenti, satira su enti e abitudini, mai su gruppi di persone);
# martedì e venerdì «La puntata» (l'estratto gratuito del Bug in 8 caroselli, testo copiato dall'EPUB di download/ al momento del rendering).
# Firma una sola volta, nel piede. Letto da carousel.py (load) con exec; immagini in social/img/nuovi/. Date: social/tools/piano_diasio_calendario.py.
import html as _h
import re as _re
import zipfile as _zf
from pathlib import Path as _P

_ROOT = _P(__file__).resolve().parents[2]
BUG = "Il Bug della Trasparenza"
AMZ_BUG, AMZ_VUOTO = "https://www.amazon.it/dp/B0HLN2VSJP", "https://www.amazon.it/dp/B0HM4HFK34"


def _paragrafi_bug():
    t = _zf.ZipFile(_ROOT / "download" / "il-bug-della-trasparenza-puntata-1.epub").read("EPUB/text/ch01.xhtml").decode("utf-8")
    return [_h.unescape(_re.sub(r"<[^>]+>", "", m)).strip() for m in _re.findall(r"<p[^>]*>(.*?)</p>", t, _re.S)]


def _spezza(testo, maxc=330):
    """Divide un paragrafo in blocchi di frasi intere (testo invariato) di al massimo maxc caratteri."""
    frasi = _re.split(r"(?<=[.!?:])\s+(?=[A-ZÈÉ—“«])", testo)
    out, cur = [], ""
    for f in frasi:
        if cur and len(cur) + 1 + len(f) > maxc:
            out.append(cur)
            cur = f
        else:
            cur = (cur + " " + f).strip()
    if cur:
        out.append(cur)
    return out


_P_ = _paragrafi_bug()
# Prima e ultima riga dell'estratto: se l'EPUB cambia, il rendering si ferma invece di pubblicare un testo diverso.
assert _P_[1].startswith("Il garage di Residenza Meridiana") and _P_[31] == "(continua)", "EPUB del Bug cambiato: ricontrollare piano_diasio.py"

# (paragrafi dell'estratto, foto di copertina in social/img/scene, frase d'apertura testuale, giorno della puntata dopo)
PUNTATE = [
    ([1, 2], "Bug_B17_telefono-alba_9x16.jpg", "…il telefono si accendeva da solo.", "venerdì"),
    ([3, 4], "Bug_B12_nadia-loft_9x16.jpg", "Ventisette anni prima, in quel palazzo aveva vissuto un uomo di nome Elio Bassi.", "martedì"),
    ([5, 6, 7], "Bug_B09_portiere-porta-vetri_9x16.jpg", "Un uomo che apriva porte e non ne varcava mai nessuna che non gli fosse stata indicata.", "venerdì"),
    ([8, 9], "Bug_P4_sala-comune_9x16.jpg", "…osservare senza farsi notare.", "martedì"),
    ([10, 11, 12, 13], "Bug_B07_presidente-martelletto_9x16.jpg", "Lo approviamo per acclamazione e andiamo avanti, che alle venti ho una cena.", "venerdì"),
    ([14, 15, 16], "Bug_P6_telefoni_9x16.jpg", "…tutti i telefoni in sala vibrarono insieme.", "martedì"),
    ([17, 18, 19, 20, 21, 22], "Bug_P7_bacheca_9x16.jpg", "Il preventivo B è di mio cognato.", "venerdì"),
    ([23, 24, 25, 26, 27, 28, 29, 30, 31], "Bug_P8_mano-alzata_9x16.jpg", "Silenzio.", None),
]

TAG_BUG = [("#NoirItaliano #ThrillerItaliano #BookstagramItalia #ConsigliDiLettura #Ticino",
            "#NoirItaliano #RomanzoNoir #ThrillerItaliano #AltaTensione #GialloItaliano #BookstagramItalia #ConsigliDiLettura #ScrittoriItaliani #Ticino #SvizzeraItaliana"),
           ("#RomanzoNoir #GialloItaliano #LibriDaLeggere #IoLeggo #SvizzeraItaliana",
            "#RomanzoNoir #NoirItaliano #LetteraturaNoir #GialloItaliano #LibriDaLeggere #IoLeggo #ScrittoriEmergenti #ScrittoriSvizzeri #BookstagramSvizzera #SvizzeraItaliana")]


def _puntata(n, paras, foto, apertura, dopo):
    slides = [dict(k="photo", photo=foto, pos=40, alto=True, text="«" + apertura + "»", who=f"{BUG} · La puntata {n}/8")]
    for i in paras:
        p = _P_[i]
        if i == 15:   # notifica dell'aggiornamento
            slides.append(dict(k="notif", kick="Sala comune · assemblea", title="Meridiana Life si è aggiornata.", text="Benvenuti in Trasparenza Meridiana.",
                               when="adesso", testata=True))
            continue
        if i == 21:
            continue
        if i == 22:   # il post anonimo delle 19:41
            slides.append(dict(k="notif", kick="Bacheca condominiale", title="Trasparenza attiva", text=p, when="19:41"))
            continue
        if i == 31:
            slides[-1]["sub"] = "*(continua)*"
            continue
        for blocco in _spezza(p):
            slides.append(dict(k="quote", text=blocco, who=f"La puntata {n}/8"))
    # unisce le battute brevi consecutive nella stessa slide (resta testo invariato, separato da a capo)
    fuse = []
    for s in slides:
        if fuse and s["k"] == "quote" and fuse[-1]["k"] == "quote" and len(fuse[-1]["text"]) + len(s["text"]) < 300 and not fuse[-1].get("sub"):
            fuse[-1]["text"] += "\n" + s["text"]
        else:
            fuse.append(s)
    if dopo:
        cta = dict(k="cta", text=f"La puntata {n + 1}/8 esce *{dopo}*", button="Il romanzo intero è su Kindle",
                   line="Scrivi <b>PUNTATA</b> nei commenti se la aspetti")
    else:
        cta = dict(k="cta", text="Fine dell’estratto. *Il resto è nel romanzo.*", button="Su Amazon Kindle",
                   line="Incluso in Kindle Unlimited · <b>libri.diasio.ch</b>")
    fuse.append(cta)
    assert len(fuse) <= 10, f"puntata {n}: {len(fuse)} slide"
    # le citazioni sono il testo dell'estratto gratuito: niente evidenze inventate, solo la virgolettatura del modello
    ig_t, fb_t = TAG_BUG[n % 2]
    prossima = f"La puntata {n + 1} esce {dopo}. " if dopo else "Era l’ultima puntata dell’estratto gratuito: il resto è nel romanzo. "
    testo = (f"Il Bug della Trasparenza, la puntata {n}/8. Scorri.\n\n"
             f"{prossima}Scrivi PUNTATA nei commenti se vuoi sapere quando esce.\n"
             "Immagine creata con l’IA, il testo è dal romanzo.")
    ig = f"{testo}\n\nIl Bug della Trasparenza è su Amazon Kindle: link in bio.\nIncluso in Kindle Unlimited. L’inizio è gratis su libri.diasio.ch.\n\n{ig_t}"
    fb = (f"{testo}\n\nIl Bug della Trasparenza su Amazon Kindle: {AMZ_BUG}\nIncluso in Kindle Unlimited.\n"
          f"L’inizio è gratis, in PDF o EPUB, senza iscrizione: https://libri.diasio.ch/bug/\n\n{fb_t}")
    alt = (f"Carosello di {len(fuse)} slide: la puntata {n} di 8 de Il Bug della Trasparenza, testo dall’estratto gratuito del romanzo, "
           f"con un’immagine creata con l’IA in apertura e la copertina del libro in chiusura.")
    return dict(id=f"pb{n}-bug-puntata-{n}", book="bug", flat=True, slides=fuse, alt=alt, theme=None, caption=ig, caption_fb=fb,
                seg="La puntata · lettori noir", when=None)


# ---------- Moduli ticinesi ----------
TAG_MOD = ("#Satira #UmorismoNero #Ironia #Ticino #SvizzeraItaliana",
           "#Satira #UmorismoNero #Ironia #CommediaNera #Ticino #SvizzeraItaliana #CulturaTicino #LeggereInSvizzera #ScrittoriSvizzeri #BookstagramSvizzera")
TAG_MOD_VUOTO = ("#RomanzoSatirico #Satira #UmorismoNero #LettureDivertenti #Ticino",
                 "#RomanzoSatirico #Satira #UmorismoNero #CommediaNera #LettureDivertenti #BookstagramItalia #ConsigliDiLettura #Ticino #SvizzeraItaliana #LeggereInSvizzera")


def _modulo(id, titolo, ente, righe, nota, foto, apertura, alt, vuoto=False):
    slide = dict(k="modulo", photo=foto, pos=45, title=titolo, ente=ente, lines=righe, nota=nota, kick="Moduli ticinesi")
    ig_t, fb_t = TAG_MOD_VUOTO if vuoto else TAG_MOD
    if vuoto:
        riga_ig = "Dal romanzo Vuoto a rendere, su Amazon Kindle: link in bio. Anche in cartaceo.\nIncluso in Kindle Unlimited."
        riga_fb = f"Dal romanzo Vuoto a rendere, su Amazon Kindle: {AMZ_VUOTO}\nIncluso in Kindle Unlimited. L’inizio è gratis: https://libri.diasio.ch/vuoto/"
    else:
        riga_ig = "Noir e satira dal Ticino. I romanzi di D.IAsio sono su Amazon Kindle: link in bio."
        riga_fb = f"Noir e satira dal Ticino. Il più satirico dei romanzi di D.IAsio, Vuoto a rendere, è su Amazon Kindle: {AMZ_VUOTO}"
    testo = f"{apertura}\n\nMandalo a chi lo compilerebbe così."
    return dict(id=id, book="vuoto", flat=True, slides=[slide], alt=alt, theme="vuoto",
                caption=f"{testo}\n\n{riga_ig}\n\n{ig_t}", caption_fb=f"{testo}\n\n{riga_fb}\n\n{fb_t}",
                seg="Moduli ticinesi · satira, invii", when=None)


MODULI = [
    _modulo("mt1-modulo-commemorazione", "Modulo di commemorazione", "Sordina · commiato laico, pacchetto base",
            ["Hobby: ________", "  → «Aldo amava le cose *semplici*»", "Carattere: ________", "  → riservato (*valore predefinito*)",
             "Ricordo: ________", "Ultimo saluto: ________"],
            "«Funziona con la maggior parte dei *ticinesi*.»", "Vuoto_cane-monitor_9x16.jpg",
            "Quattro campi: hobby, carattere, ricordo, ultimo saluto. Se il campo è vuoto, il sistema scrive le cose semplici.",
            "Un finto modulo di commemorazione su una foto scura di una sala del commiato, creata con l’IA: hobby e carattere vuoti, "
            "il sistema scrive «le cose semplici» e «riservato». In fondo: «Funziona con la maggior parte dei ticinesi.» Da Vuoto a rendere.", vuoto=True),
    _modulo("mt2-listino-sordina", "Listino · voce 01", "Sordina · Sala Ulivo",
            ["Sala Ulivo, tre ore ...... CHF 1’200.00", "Essenze al cedro .......... incluse", "Playlist «Commiato Pianissimo» incl.",
             "Comparsa, all’ora ........... CHF 25", "  festivi ...................... +5", "Lacrime (Ottavio) ......... *+ CHF 8*"],
            "«La regia non si *conta*.»", "Vuoto_wifi_9x16.jpg",
            "A Sordina tutto ha una voce di listino. Anche le lacrime.",
            "Un finto listino su foto scura creata con l’IA: Sala Ulivo 1200 franchi, comparse a 25 franchi l’ora, lacrime più 8 franchi. "
            "In fondo: «La regia non si conta.» Da Vuoto a rendere.", vuoto=True),
    _modulo("mt3-domanda-lamentarsi", "Modulo L-1 · Domanda di autorizzazione a lamentarsi", "Ufficio del malumore · lamentele ordinarie",
            ["Oggetto: □ traffico □ parcheggio □ il tempo", "  □ «una volta era diverso»  ■ *tutto*",
             "Luogo: □ bar □ chat del condominio □ posta", "Durata: □ 5 min  □ un caffè  ■ *chiusura*",
             "Soluzione proposta: ________ (facoltativo)"],
            "Le lamentele senza soluzione vengono archiviate e ripresentate la *settimana dopo*.", "Mod_A_scrivania-ufficio_9x16.jpg",
            "Prima di lamentarti, compila il modulo. In triplice copia.",
            "Un finto modulo ufficiale su foto scura di una scrivania d’ufficio, creata con l’IA: domanda di autorizzazione a lamentarsi, "
            "con l’oggetto «tutto» e la durata «fino alla chiusura».")
    ,
    _modulo("mt4-verbale-assemblea", "Verbale dell’assemblea condominiale n. 47", "Ordine del giorno: 1. Bidone della carta. 2. Varie",
            ["Durata: 3 ore e 12 minuti", "Punto 1: discusso", "Punto 2: non raggiunto", "Deliberato: *rinvio*",
             "Contrari: il terzo piano, per principio"],
            "Allegati: nessuno ha letto gli *allegati*.", "Mod_B_sala-condominio_9x16.jpg",
            "Tre ore per un bidone. Poi la prossima assemblea.",
            "Un finto verbale di assemblea condominiale su foto scura di una sala riunioni, creata con l’IA: tre ore e dodici minuti, "
            "un solo punto discusso, deliberato il rinvio.")
    ,
    _modulo("mt5-certificato-grotto", "Certificato di frequenza al grotto", "Stagione estiva · valido fino a sera",
            ["Motivo: □ la polenta □ il fresco", "  ■ «*solo per un bicchiere*»", "Durata effettiva: 4 ore",
             "Rientro previsto: □ prima di cena", "  ■ *dopo cena*"],
            "Il certificato non vale come giustificazione a *casa*.", "Mod_C_grotto_9x16.jpg",
            "Era solo per un bicchiere. Il certificato dice altro.",
            "Un finto certificato su foto scura di un grotto ticinese con tavoli di pietra, creata con l’IA: «solo per un bicchiere», "
            "durata effettiva quattro ore, rientro dopo cena.")
    ,
    _modulo("mt6-accettazione-nebbia", "Modulo di accettazione della nebbia", "Piano di Magadino · da novembre a marzo",
            ["Il sottoscritto dichiara di:", "□ non vedere il lago", "□ non vedere le montagne", "□ non vedere la propria auto",
             "■ sostenere che «*più su c’è il sole*»"],
            "Firma: ________ (se trovate la penna)", "Mod_D_nebbia_9x16.jpg",
            "Da novembre a marzo, va rinnovato ogni mattina.",
            "Un finto modulo su foto scura di una strada di pianura nella nebbia, creata con l’IA: il firmatario non vede lago, montagne né auto, "
            "ma sostiene che più su c’è il sole.")
    ,
    _modulo("mt7-listino-scuse", "Listino ufficiale delle scuse per il ritardo", "Prezzi IVA inclusa",
            ["Colonna al Vedeggio ..... *accettata*", "Cantiere nuovo ........... accettata", "Treno ......... accettata con riserva",
             "«Ho trovato tutti verdi» .. sospetta", "«Sono uscito in orario» ... *respinta*"],
            "Le scuse non sono *rimborsabili*.", "Mod_E_coda-auto_9x16.jpg",
            "Arrivi tardi? Scegli la scusa dal listino.",
            "Un finto listino su foto scura di una coda di auto di sera, creata con l’IA: la colonna al Vedeggio è sempre accettata, "
            "«sono uscito in orario» è respinta.")
    ,
    _modulo("mt8-ricevuta-ascensore", "Ricevuta di conversazione in ascensore", "Corsa singola · 4 piani",
            ["Argomento: il tempo .......... 2 piani", "Argomento: il tempo domani .. 2 piani", "Contatto visivo .......... *0 secondi*",
             "Silenzio residuo ............. incluso"],
            "«Nessuno la salutava per prima nell’*ascensore*.» (Il Bug della Trasparenza)", "Mod_F_ascensore_9x16.jpg",
            "Conservare la ricevuta: alla prossima corsa si riparte da capo.",
            "Una finta ricevuta su foto scura dell’interno di un ascensore, creata con l’IA: quattro piani, due sul tempo e due sul tempo di domani, "
            "zero secondi di contatto visivo. In fondo una frase de Il Bug della Trasparenza."),
]

ITEMS = MODULI + [_puntata(i + 1, *p) for i, p in enumerate(PUNTATE)]

# ---------- «Inizia qui» (da fissare in cima al profilo) ----------
_INIZIA = [
    dict(k="hook", kick="D.IAsio", text="Noir e satira *dal Ticino*.", sub="12 anni di alta orologeria. Ora smonto colpevoli, pezzo per pezzo. Scorri.", testata=False, books=["bug", "oblio", "vuoto", "aritmetica"]),
    dict(k="step", n="23:10", kick="Ogni sera", title="Una frase *ogni sera*", text="Un pensiero nero e ironico, alle 23:10. Salvala per la sera dopo.", testata=False, books=["bug", "oblio", "vuoto", "aritmetica"]),
    dict(k="step", n="Lun · Gio", kick="Due volte a settimana", title="Moduli *ticinesi*", text="Finti documenti sul Ticino. Da mandare a chi li compilerebbe così.", testata=False, books=["bug", "oblio", "vuoto", "aritmetica"]),
    dict(k="step", n="Mar · Ven", kick="A puntate", title="La *puntata*", text="Il Bug della Trasparenza in otto caroselli. Scrivi PUNTATA nei commenti.", testata=False, books=["bug", "oblio", "vuoto", "aritmetica"]),
    dict(k="step", n="Sab", kick="D.IAsio music", title="Rap *conscious*", text="Un estratto dai videoclip. I brani interi sono su YouTube.", testata=False, books=["bug", "oblio", "vuoto", "aritmetica"]),
    dict(k="cta", text="Quattro romanzi, *un solo autore*", books=["bug", "oblio", "vuoto", "aritmetica"], button="Su Amazon Kindle",
         line="Scrivo io. L’IA illustra, e lo dichiaro."),
]
_TXT_INIZIA = ("Inizia qui. D.IAsio: noir e satira dal Ticino.\n"
               "Ogni sera alle 23:10 una frase. Lunedì e giovedì i Moduli ticinesi. Martedì e venerdì La puntata. Il sabato la musica.\n"
               "Il nome? D. Iasio, con dentro l’IA: le storie le scrivo io, le immagini le crea l’IA e lo dichiaro sempre.")
ITEMS.append(dict(id="iq0-inizia-qui", book="vuoto", flat=True, slides=_INIZIA, theme=None,
                  alt="Carosello di sei slide: chi è D.IAsio e cosa trovi sul profilo (frase delle 23:10, Moduli ticinesi, La puntata, musica), "
                      "in chiusura le copertine dei quattro romanzi e il pulsante Amazon Kindle.",
                  caption=_TXT_INIZIA + "\n\nI quattro romanzi sono su Amazon Kindle: link in bio. Inclusi in Kindle Unlimited.\n\n"
                          "#NoirItaliano #Satira #ScrittoriEmergenti #Ticino #SvizzeraItaliana",
                  caption_fb=_TXT_INIZIA + f"\n\nVuoto a rendere su Amazon Kindle: {AMZ_VUOTO}\nGli altri romanzi: https://libri.diasio.ch/\n\n"
                             "#NoirItaliano #Satira #UmorismoNero #ScrittoriEmergenti #ScrittoriSvizzeri #Ticino #SvizzeraItaliana #CulturaTicino #LeggereInSvizzera #BookstagramSvizzera",
                  seg="Inizia qui · post fissato", when=None))
