# libri.diasio.ch: memoria di progetto (leggila prima di lavorare)

Ultimo aggiornamento: 1 ottobre 2026, dopo le PR #1-#13 (il terzo libro, Vuoto a rendere, è sul branch `claude/nifty-meitner-a45vfp`: vedi sotto). Se questo file e il repo divergono, fidati del repo e correggi il file.

## Cos'è
Sito statico (GitHub Pages, CNAME `libri.diasio.ch`) di D. Iasio: tre romanzi, «Il Bug della Trasparenza» (noir sociale, 8 puntate), «L'Economia dell'Oblio» (thriller psicologico, 6 puntate) e «Vuoto a rendere» (romanzo satirico, 10 puntate, sottotitolo «Un romanzo in dieci voci di listino»). La Puntata 1 di ognuno è gratis in PDF/EPUB (`download/`, senza iscrizione). Newsletter MailerLite (landing `davide-fek7ym.subscribepage.io`, pagina `/grazie/`), contatore visite GoatCounter (codice `diasio`). Instagram `@d.iasio.libri` e Pagina Facebook «D. Iasio».
Obiettivo unico: iscrizioni alla newsletter e download della Puntata 1, a budget zero, esposizione e contenuti di qualità su social Facebook e Instagram, 

## Regole dell'utente (valgono sempre)
- Italiano, risposte chiare e operative. Distinguere i dati presenti dalle inferenze. Dire cosa fa l'utente e cosa fa Claude. Se manca un'informazione importante, chiedere prima di produrre.
- **Mai** seguire, scrivere, commentare o cliccare su Instagram/Facebook senza conferma esplicita. Niente follow o messaggi di massa (violano le regole di Meta).
- Approvare = fare il merge su `main`, e il merge **pubblica**. Non unire senza via libera. Nessun token o Secret in chat, nei file o nei commit.
- Le citazioni dei romanzi devono essere testuali dalle Puntata 1 (`download/*.epub`). Non inventare frasi né trama.
- I romanzi sono in vendita: l'autore scrive «disponibili in formato integrale negli store». Non scrivere «solo a puntate» possono essere rilasciati a puntate a     dell'autore.
- Stato degli store (dato dall'utente il 1/10/2026): **Il Bug** e **L'Oblio** sono disponibili su Amazon Kindle (KDP): Bug `https://www.amazon.it/dp/B0HLN2VSJP`, Oblio `https://www.amazon.it/dp/B0HLMKWJZ5` (verificati dai titoli delle schede). Su **StreetLib** (e negli store che distribuisce, **esclusa Amazon** per non avere doppioni: Kobo, Apple Books, Google Play Libri e altri) sono «prossimamente». **Vuoto a rendere** non è ancora pubblicato: sul sito è «in arrivo negli store».
- Il romanzo completo di Vuoto a rendere (EPUB, PDF, copertina, quarta) **non va nel repo**, che è pubblico: nel repo c'è solo la Puntata 1 (capitolo 1). Nei file ebook per gli store non mettere link diretti ad Amazon (Apple Books e Kobo li rifiutano): solo `libri.diasio.ch` e la newsletter.
- Una sola sessione di lavoro alla volta. Questo file è la memoria comune di tutte le sessioni (cloud e locali). Aggiorna la memoria quando si raggiungono obbiettivi importanti e cruciali, chiedendo conferma all'utente.

## Struttura
- Sito: `index.html`, `bug/`, `oblio/`, `vuoto/`, `privacy/`, `grazie/`, `404.html`, `css/`, `js/config.js` (link degli store per libro: `amazon`, `altriStore`; con `amazon` pieno e `altriStore` vuoto compare «Prossimamente su StreetLib»), `img/`, `fonts/`, `download/`.
- Social: `social/` con `README.md` (uso), `STRATEGIA.md` (giorni, orari, segmenti), `calendar.json` (calendario), `published.json` (stato: lo scrive il bot, non a mano), `publish.py` + `test_publish.py`, `tools/` (slide con Chromium), `reels-src/` (Reel con HyperFrames), `img/`, `video/`, `kit/`.
- Workflow: `social-publish` (ogni 30 minuti; pubblica al massimo un post scaduto, salta quelli in ritardo di oltre 12 ore) e `social-token` (rinnovo mensile del token). Secret: `IG_ACCESS_TOKEN`, `FB_PAGE_TOKEN`, `SECRETS_PAT` (facoltativo).

## Calendario social (fino al 31/12/2026)
84 voci: Reel r00-r06 (30/09-14/10, date sparse) e r07-r23 (mer 19:30 e sab 12:30), grafiche (dom 20:00, mar 19:30, gio 12:30), 6 caroselli (dom 20:00), 13 Storie (lunedì 18:30), 6 post di testo solo Facebook (venerdì 18:00). Tipi in `calendar.json`: immagine, `reel`, `carosello`, `storia`, `testo`; campo `piattaforme` per limitare a una sola.
Già pubblicati: r00 (eliminato a mano dall'app), r00b (30/09, miniatura sulle copertine), p00 presentazione (30/09 12:01, IG e FB). Prossimo: Reel r01 il 1 ottobre alle 19:30.
**Mai provati con l'API reale:** carosello (primo il 29/11), Storia (primo il 5/10), post di testo (primo il 9/10). I dry run sono riusciti. Controllare il primo di ognuno appena esce.

## Trappole già incontrate
- Dopo un merge, Pages impiega circa 30-60 secondi: un dry run subito dopo può fallire con «File non raggiungibile». Non è un bug.
- Con più esecuzioni manuali ravvicinate GitHub tiene una sola in coda e annulla le altre.
- Il cron ha ritardi. Per la puntualità lanciare `social-publish` a mano senza `post_id` (con `post_id` si forza e si rischiano doppioni).
- L'API non cancella né modifica post: eliminare o cambiare dall'app.
- Instagram non permette di allegare audio esterno a una foto: per immagine + audio serve un video.
- Stories: solo immagine, senza sticker né link. Instagram non ha post di solo testo (solo Facebook).
- Rendering: `python social/tools/carousel.py` (Playwright + Chromium, `CHROMIUM_PATH`), Reel con `social/reels-src/render-all.sh` (HyperFrames + FFmpeg). I font di Windows non ci sono in cloud.
- I branch `main-xxxx` delle sessioni cloud sono del repo `Campanella`, non di questo.

## Da fare a mano (utente)
Pubblicare «Vuoto a rendere» su KDP e StreetLib (testi di quarta, descrizione e parole chiave sono nel pacchetto consegnato in sessione); poi incollare i link in `js/config.js` (`books.vuoto.amazon`, `altriStore`) e, per Bug e Oblio, il link StreetLib in `altriStore` quando esiste; ricontrollare su Zefix e Amazon i nomi nuovi Sordina e Teleriva; dichiarare l'uso di IA su KDP e StreetLib; aggiornare Goodreads/aNobii (`social/kit/goodreads-anobii.md` dice ancora «quando è in vendita»). Controllare dal telefono il sito; dopo le 19:45 del 1/10 controllare il Reel r01 (miniatura, didascalia, Facebook); verificare il pulsante «Iscriviti» sulla Pagina Facebook; rileggere il punto 12 della privacy; iscrizioni Goodreads e aNobii (`social/kit/`); verificare che il passaggio «Presentati» di Instagram sia chiuso; controllare profili e gruppi in `social/kit/esposizione-lista-e-testi.txt` (lista da verificare, non ancora seguito né contattato nessuno); il primo token Instagram scade dopo circa 60 giorni.

## Igiene dei repository
Dopo ogni PR unita i branch restano: cancellarli da GitHub (Branches, cestino) oppure attivare «Automatically delete head branches» in Settings > General.

## Mappa dei progetti dell'account (un progetto = un repository = una sessione)
Non mescolare i progetti: apri la sessione con **solo** il repository che serve e dai un titolo «Progetto – argomento». Ogni repository ha il suo `CLAUDE.md`.

| Repository | Cosa | Online (dai file dei repo) | Visibilità |
|---|---|---|---|
| `libri-diasio-ch` | sito dei romanzi e pubblicazione social | libri.diasio.ch (GitHub Pages) | pubblico |
| `gerla` | app della spesa e dei menu | gerla.diasio.ch (GitHub Pages) | pubblico |
| `Campanella` | piattaforma scuola-famiglia (Expo + Supabase) | campanella-nine.vercel.app (Vercel) | privato |
| `Bussola` | servizio digitale per padri single in Ticino | risulta bussola-dd85.vercel.app (Vercel) | privato |
| `NewCalendar` | calendario diritti di visita con PDF (PWA) | da verificare (README: GitHub Pages) | privato |
| `davide-diasio-portfolio` | sito portfolio | diasio.ch (da verificare dove è ospitato) | privato |

Cartelle locali: restano dove sono. In particolare non spostare la cartella di Bussola senza sistemare `../bussola-spaziale` (prototipo locale citato nel suo README). Rischio noto: git dentro OneDrive può dare file bloccati o duplicati.
