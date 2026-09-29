# Pubblicazione automatica su Instagram e Facebook

Account Instagram `@d.iasio.libri` e Pagina Facebook "D. Iasio". 24 post programmati dal 4 ottobre al 26 novembre 2026 (vedi `STRATEGIA.md`).

## Come funziona

- `calendar.json`: data/ora (ora di Roma), immagine, didascalia e testo alternativo di ogni post.
- `publish.py`: ogni 30 minuti (workflow `social-publish`) pubblica al massimo **un** post scaduto e non ancora pubblicato, tramite l'API Instagram con Instagram Login. L'immagine viene letta da `https://libri.diasio.ch/social/img/...`, quindi il sito deve essere già aggiornato.
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

## Rigenerare le grafiche

`cd social/tools && python generate.py` (serve Pillow e i font di Windows: Arial Narrow Bold, Georgia, Consolas). I testi sono in `tools/posts.py`; poi aggiorna `calendar.json`.

## Limiti

- Solo immagini singole. Storie con sticker o musica non sono automatizzabili in modo affidabile.
- Se il repo resta inattivo 60 giorni GitHub disattiva i cron: i commit di `published.json` contano come attività finché ci sono post da pubblicare.
- Su Facebook la didascalia è `didascalia_fb` (link diretto al posto di "link in bio", 3 hashtag). Se Facebook fallisce, Instagram non viene ripubblicato: lo stato è per piattaforma.
