# Commento dell'autore sotto ai post (dal 19/11/2026)

Campo `commento` nel post di `social/calendar.json` (facoltativo `commento_fb` se su Facebook serve un testo diverso).

- **Instagram e Facebook**: lo scrive `publish.py` subito dopo l'uscita del post (`commenta()`). Se il permesso manca o l'API rifiuta, il post resta pubblicato e nel log compare un avviso; in `published.json` la piattaforma riporta `"commento": "scritto"` o `"errore"`. Fissarlo in cima è un gesto dall'app (le API non lo prevedono).
- **TikTok e YouTube Shorts**: Buffer non pubblica commenti su TikTok. Regia, nella pagina Oggi, mostra il commento dei video della giornata con il pulsante «Copia»: lo si incolla sotto il video e lo si fissa.
- **Storie**: niente commento (non esistono commenti alle Storie).
- **Rubrica 23:10**: niente commento: la frase basta.

## Come si scrive
- Nella voce di D. Iasio: frase breve, asciutta, ironica o noir; aggiunge un dettaglio o una domanda che il video non dice. Massimo 150 caratteri (limite dei commenti TikTok).
- Fedele ai libri: personaggi, luoghi e fatti solo se sono nella Puntata 1 (EPUB in `download/`) o nella didascalia del post. Le date (prossima puntata, uscite) si leggono dal calendario.
- Mai: hashtag, link, «link in bio», «che ne pensate», «fatemi sapere», «seguimi», emoji in serie, lo stesso inizio di un altro commento.
- I controlli automatici sono in `test_calendario.py`, classe `Commenti`.
