# Avvio puntuale di `social-publish` da un servizio esterno

Perché: il cron interno di GitHub (`schedule`) arriva con ore di ritardo (1/10: intervalli da 3h48 a 9h19 invece di 15 minuti). Un avvio esterno chiama l'API di GitHub all'ora esatta e il workflow parte subito (provato il 1/10: avvio manuale partito nello stesso secondo).
Il cron interno resta come ripiego. `publish.py` pubblica al massimo un post scaduto per piattaforma e salta quelli in ritardo di oltre 12 ore.

## Cosa serve (tutto gratuito)
1. Un token GitHub a grana fine, solo per questo repository, con il solo permesso `Actions: Read and write`.
2. Un job su cron-job.org che fa una richiesta POST all'ora giusta.

Nessun token va scritto in chat, nei file o nei commit: si incolla solo dentro cron-job.org.

## 1. Token GitHub (5 minuti)
Pagina: https://github.com/settings/personal-access-tokens/new (menu: foto profilo → Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token).
- Token name: `cron-job.org avvio social-publish`
- Expiration: 366 giorni (GitHub scrive una mail prima della scadenza; segna la data) oppure «No expiration» se preferisci non rinnovare
- Resource owner: `krastaman85`
- Repository access: **Only select repositories** → `libri-diasio-ch`
- Permissions → Repository permissions → **Actions: Read and write** (Metadata: Read-only si aggiunge da solo). Nient'altro.
- Generate token e **copia subito il valore** (si vede una volta sola).

## 2. Job su cron-job.org (10 minuti)
Registrazione: https://console.cron-job.org/signup (conferma la mail). Console: https://console.cron-job.org/jobs. Guida: https://docs.cron-job.org/.
Se le etichette sul sito differiscono, cerca la voce equivalente.
1. Imposta per il job il fuso orario **Europe/Zurich** (come nel job configurato); coincide con Europe/Rome anche nei passaggi tra ora legale e solare, usato dal calendario.
2. «Create cronjob» → scheda **Common**:
   - Title: `Social publish libri.diasio.ch`
   - URL: `https://api.github.com/repos/krastaman85/libri-diasio-ch/actions/workflows/social-publish.yml/dispatches`
   - Execution schedule: **User-defined**, un job per finestra come nella sezione «Finestre di avvio» qui sotto (stesso URL, stesse intestazioni e stesso body in tutti; per i job successivi al primo usa «Duplicate», così l'intestazione `Authorization` si copia senza reincollare il token).
    (Gli orari dei post nel calendario cadono dentro queste finestre. Se nel giorno non c'è nulla da pubblicare, il workflow termina senza fare niente.)
3. Scheda **Advanced**:
   - Request method: **POST**
   - Headers (nome → valore):
     - `Authorization` → `Bearer <incolla qui il token>`
     - `Accept` → `application/vnd.github+json`
     - `X-GitHub-Api-Version` → `2022-11-28`
     - `Content-Type` → `application/json`
   - Request body: `{"ref":"main","inputs":{"dry_run":"true"}}`  ← **solo per la prova**
4. Notifiche: attiva l'avviso mail se il job fallisce.
5. Salva e premi **Test run** (o «Run now»). Risposta attesa: **HTTP 204**.
6. Controlla https://github.com/krastaman85/libri-diasio-ch/actions/workflows/social-publish.yml: deve comparire in pochi secondi una nuova esecuzione con evento `workflow_dispatch`, che finisce in verde e **non pubblica** (è una prova).
7. Solo ora modifica il body in `{"ref":"main","inputs":{"dry_run":"false"}}` e salva. Da questo momento il job pubblica davvero.

Perché `dry_run` è nel body: nel workflow vale `true` di default; senza `"dry_run":"false"` ogni avvio sarebbe solo una prova.

## Finestre di avvio (dal 4 ottobre)
Fuso **Europe/Zurich**, ogni mese. Dentro ogni finestra il job parte ogni 5 minuti; il post esce al primo avvio utile, con 0-5 minuti di ritardo rispetto all'orario scritto nel calendario. Gli orari nel calendario sono irregolari di proposito: stesso giorno, minuti diversi di settimana in settimana, mai due settimane di fila lo stesso minuto.

| Job | Giorni | Ora | Minuti | Cosa esce |
|---|---|---|---|---|
| Lun | lunedì | 18 | 7,12,17,22,27,32,37,42,47,52 | Storie, fine giornata lavorativa |
| Mar+Mer | martedì, mercoledì | 19 | 17,22,27,32,37,42,47,52,57 | Grafiche e Reel serali |
| Gio | giovedì | 12 | 12,17,22,27,32,37,42,47,52 | Pausa pranzo |
| Ven | venerdì | 18 | 2,7,12,17,22,27,32,37,42 | Post di testo (solo Facebook) |
| Sab | sabato | 12 | 2,7,12,17,22,27,32,37,42,47 | Reel di tarda mattina |
| Dom | domenica | 20 | 2,7,12,17,22,27,32,37,42,47 | Domande e caroselli, sera di lettura |

Equivalente in formato crontab:
```
CRON_TZ=Europe/Zurich
7-52/5   18 * * 1
17-57/5  19 * * 2,3
12-52/5  12 * * 4
2-42/5   18 * * 5
2-47/5   12 * * 6
2-47/5   20 * * 0
```
Se cambi una finestra, cambia anche `social/test_calendario.py` (stesse finestre) e gli orari in `calendar.json`: l'orario di un post deve cadere prima dell'ultimo avvio della sua finestra. Il body è sempre `{"ref":"main","inputs":{"dry_run":"false"}}`.

## Controlli dopo l'attivazione
- Controlla l'esito su cron-job.org (History: HTTP 204) e su Actions: il run deve avere `dry_run` vuoto o `false` e deve riportare `Pubblicato su` per le piattaforme previste. HTTP 204 conferma solo l'avvio del workflow, non che abbia pubblicato.
- Il 2 ottobre il Reel r02 era ancora pianificato alle 12:30: i dispatch delle 12:01 e 12:31 risultano con `dry_run: true`, mentre il cron interno l'ha pubblicato alle 16:57. Il calendario ora è corretto; il primo controllo con gli orari allineati è il Reel r03 del 3 ottobre alle 12:31.
- Se un post esce due volte o troppo presto, disattiva il job su cron-job.org e scrivi a Claude.
- Se il token GitHub scade o viene revocato, cron-job.org riceve 401: rinnova il token e aggiornalo nell'header. Nel frattempo funziona ancora il cron interno (con i suoi ritardi).

## Sicurezza
- Il token può solo avviare workflow di questo repo. Se trapela: Settings → Developer settings → Fine-grained tokens → Revoke, poi creane uno nuovo.
- Non riusare questo token per altro e non dargli altri permessi (il rinnovo del token Instagram usa un altro Secret, `SECRETS_PAT`).
