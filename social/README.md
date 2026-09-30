# Pubblicazione automatica su Instagram e Facebook

Account Instagram `@d.iasio.libri` e Pagina Facebook "D. Iasio". Calendario dal 30 settembre al 31 dicembre 2026: Reel, grafiche singole e caroselli (vedi `STRATEGIA.md`).

Contenuto della cartella: `calendar.json` (calendario), `img/` (grafiche), `video/` (Reel), `publish.py` (pubblicazione), `tools/` (generatori delle grafiche), `kit/` (Goodreads, aNobii, contatore visite), `reels-src/` (progetto HyperFrames dei Reel: una composizione con variabili, un file `vars/*.json` per Reel).

## Come funziona

- `calendar.json`: data/ora (ora di Roma), immagine, didascalia e testo alternativo di ogni post.
- `publish.py`: ogni 30 minuti (workflow `social-publish`) pubblica al massimo **un** post scaduto e non ancora pubblicato, tramite l'API Instagram con Instagram Login. L'immagine viene letta da `https://libri.diasio.ch/social/img/...`, quindi il sito deve essere già aggiornato.
- **Reel:** voci con `"tipo": "reel"` e `"video": "social/video/....mp4"`; facoltativo `"miniatura_ms"` sceglie il fotogramma della miniatura su Instagram (senza, prende il primo: quasi nero). Su Instagram escono come Reel (anche nel feed), su Facebook come video/Reel di Pagina. Sono MP4 H.264 1080×1920, max 90 secondi.
- **Caroselli:** voci con `"tipo": "carosello"` e `"immagini": [...]` (da 2 a 10 JPEG 1080×1350, nell'ordine di scorrimento). Su Instagram escono come carosello, su Facebook come un solo post con più foto.
- **Storie:** voci con `"tipo": "storia"` e `"immagine"` (JPEG 1080×1920, cartella `img/story/`). Niente didascalia, sticker, sondaggi o link: l'API non li supporta (restano manuali). Escono su Instagram e sulla Pagina Facebook.
- **Post di testo:** `"tipo": "testo"`, solo Facebook, con `"didascalia"` e `"link"` facoltativo (anteprima automatica). Instagram non ha post di solo testo.
- `"piattaforme": ["instagram"]` (o `["facebook"]`) limita qualsiasi voce a una sola piattaforma.
- `published.json`: stato (pubblicato, link, oppure saltato). Il workflow lo salva con un commit.
- Un post in ritardo di oltre 12 ore viene **saltato**, non pubblicato fuori orario.
- Il cron di GitHub può ritardare di qualche minuto: la pubblicazione avviene entro l'ora prevista + qualche minuto.

## Approvazione e controlli

- **Approvare** = fare il merge della PR su `main`. Prima del merge non parte niente.
- **Mettere in pausa**: in `calendar.json` imposta `"pausa": true` e fai commit su `main`.
- **Cambiare un post**: modifica data, didascalia o immagine in `calendar.json` prima che scada.
- **Test senza pubblicare**: Actions → "Pubblica su Instagram" → Run workflow con `dry_run` attivo. Controlla token, ID account e raggiungibilità dell'immagine.
- **Forzare un post**: stesso pulsante, `dry_run` disattivato e `post_id` con l'ID del post.

## Secret richiesti (Settings → Secrets and variables → **Actions**)

| Nome | Cosa | Note |
|---|---|---|
| `IG_ACCESS_TOKEN` | Token Instagram a lunga durata | Mai nel repo, mai in chat. Scade dopo circa 60 giorni. |
| `FB_PAGE_TOKEN` | Token della Pagina Facebook (permesso `pages_manage_posts`) | Facoltativo: senza, si pubblica solo su Instagram. Un token di Pagina ricavato da un token utente a lunga durata non scade. |
| `SECRETS_PAT` | Token GitHub a grana fine, solo questo repo, permesso "Secrets: Read and write" | Facoltativo. Serve al rinnovo mensile automatico del token. Senza, rinnova a mano prima della scadenza. |

L'ID dell'account Instagram non serve come Secret: lo script lo ricava dal token. L'ID della Pagina Facebook (`1377129402146055`) è nel workflow.

## Rinnovo del token a mano

Meta for Developers → app "Libri Diasio Social" → Casi d'uso → API con Instagram Login → Genera token, e aggiorna il Secret `IG_ACCESS_TOKEN`. Il rinnovo automatico (`social-token`, il 1° di ogni mese) usa `graph.instagram.com/refresh_access_token`.

## Caroselli e grafiche di novembre-dicembre

`social/tools/carousels.py` contiene testi e slide (le citazioni sono testuali dalle Puntate 1). Da `social/tools`: `python carousel.py` rende le slide con Chromium (stesso stile e font dei Reel; `pip install playwright`, poi `playwright install chromium` oppure `CHROMIUM_PATH=/percorso/chrome`), `python carousel.py --calendar` aggiunge le voci a `calendar.json`. Le Storie si rendono con lo stesso comando (`carousel.py`, voci con `story(...)`). I Reel r07-r23 si aggiungono con `python reels_calendar.py`, i post di testo con `python texts_calendar.py` (render con `reels-src/render-all.sh`). Test con API simulate: `python3 -m unittest social/test_publish.py`.

## Rigenerare le grafiche del 4 ottobre-26 novembre

`cd social/tools && python generate.py` (serve Pillow e i font di Windows: Arial Narrow Bold, Georgia, Consolas). I testi sono in `tools/posts.py`; poi aggiorna `calendar.json`.

## Limiti

- Storie con sticker, sondaggi, link o musica non sono automatizzabili: solo immagine fissa.
- Se il repo resta inattivo 60 giorni GitHub disattiva i cron: i commit di `published.json` contano come attività finché ci sono post da pubblicare.
- Su Facebook la didascalia è `didascalia_fb` (link diretto al posto di "link in bio", 3 hashtag). Se Facebook fallisce, Instagram non viene ripubblicato: lo stato è per piattaforma.
