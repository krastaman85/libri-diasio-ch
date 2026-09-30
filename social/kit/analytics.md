# Contatore visite rispettoso della privacy: GoatCounter

**Stato: attivo dal 2026-09-30** (codice del sito `diasio`, dashboard `https://diasio.goatcounter.com`). CSP e Privacy (punto 12) aggiornate. Le sezioni sotto descrivono la procedura, utile se cambi codice o dominio.

**Perché GoatCounter:** gratuito per uso non commerciale, open source, **nessun cookie**, nessun tracciamento tra siti, nessuna profilazione. Conta pagine viste, provenienza (referrer, campagne `?ref=`/`utm_`), paese, dispositivo e browser in forma aggregata. Non c'è il banner dei cookie.
Alternative (a pagamento): Plausible, Fathom. Cloudflare Web Analytics è gratuito ma richiede di passare per Cloudflare.

## Cosa fa il sito già oggi

`js/main.js` carica il contatore solo se `js/config.js` ha un codice in `analytics.goatcounter`. Con `""` non parte nulla e la Content-Security-Policy resta chiusa.

## Attivazione (10 minuti)

1. **Tu:** vai su https://www.goatcounter.com/signup e crea l'account (email `davide@diasio.ch`).
   - "Site code": scegli un nome breve, per esempio `diasio` → i dati stanno su `diasio.goatcounter.com`.
   - "Domain": `libri.diasio.ch`.
2. **Tu:** dimmi il codice scelto. Non serve nessuna password.
3. **Io:** in una PR imposto `analytics.goatcounter`, aggiungo alla CSP delle 6 pagine
   - `script-src 'self' https://gc.zgo.at`
   - `connect-src 'self' https://<codice>.goatcounter.com`
   - `img-src 'self' data: https://<codice>.goatcounter.com`
   e aggiorno la pagina Privacy con il testo qui sotto.
4. **Tu:** dopo il merge, apri il tuo dashboard GoatCounter e naviga su libri.diasio.ch: dopo qualche secondo vedi la visita.

## Testo per la pagina Privacy (sezione "Visite al sito")

> **Statistiche di visita.** Per capire quante persone leggono il sito uso GoatCounter, un servizio di statistiche che non usa cookie e non identifica le persone. Registra in forma aggregata la pagina visitata, il sito da cui arrivi, il paese, il tipo di dispositivo e di browser. Non salva il tuo indirizzo IP in modo riconoscibile e non condivide i dati con altri. Base giuridica: il mio interesse legittimo a conoscere l'uso del sito. Se non vuoi essere contato, attiva l'opzione "Do Not Track" del browser o un blocco dei tracciamenti.

(Da verificare con la privacy policy di GoatCounter al momento dell'attivazione; se hai un IP fisso o particolari esigenze, chiedi conferma.)

## Come leggere i numeri

- **Visite dalla bio Instagram:** metti il link `https://libri.diasio.ch/?ref=instagram` (e `?ref=facebook` sulla Pagina). GoatCounter mostra il canale in "Campagne".
- **Pagine più lette:** Il Bug, L'Oblio, `/grazie/` (chi ha confermato l'iscrizione).
- **Conversione:** iscritti nuovi in MailerLite ÷ visite alla home. Con poche visite è rumore: guarda i trend su 2-4 settimane.
- **Download:** i file PDF ed EPUB sono link diretti; per contarli in GoatCounter serve un evento sul clic (posso aggiungerlo dopo l'attivazione).
