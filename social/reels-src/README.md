# Reel D. Iasio: progetto HyperFrames

Una sola composizione (`index.html`, 1080×1920, 13 s) che rivela una citazione parola per parola,
poi mostra copertina, titolo e invito a leggere la Puntata 1. Tutto il resto arriva da variabili.

## Rigenerare un Reel

Serve Node 20+ e FFmpeg. Dalla cartella `social/reels-src`:

```bash
npx hyperframes@0.8.96 check .
npx hyperframes@0.8.96 render . --variables-file vars/r01-bug-cognato.json -q high -o renders/r01-bug-cognato.mp4
```

Poi comprimi per il caricamento (circa 3-4 MB) e copia in `../video/`:

```bash
ffmpeg -i renders/r01-bug-cognato.mp4 -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p -profile:v high -movflags +faststart -c:a aac -b:a 160k ../video/r01-bug-cognato.mp4
```

## Un Reel nuovo

1. Copia un file in `vars/` e cambia `quote`, `emphasis` (parole in ambra, separate da virgola), `who`, `title`, `genre`, `cover`.
2. Render e compressione come sopra.
3. Aggiungi la voce in `../calendar.json` con `"tipo": "reel"` e `"video": "social/video/<id>.mp4"`.

## Note

- Font e copertine sono locali (`assets/`); GSAP è incluso (`assets/js/gsap.min.js`), nessuna dipendenza da CDN.
- L'audio (`assets/audio/bed.mp3`) è sintetizzato con FFmpeg (drone e un colpo grave all'arrivo della copertina): originale, senza diritti di terzi.
- Zone sicure per Instagram: il marchio parte da y=290 (la fascia alta, circa il 14%, è occupata da «Reels» e dal profilo) e il testo arriva fino a y=1650; il bordo inferiore resta libero per l'interfaccia dei Reel.

## Audio: come si rigenera

La traccia ssets/audio/bed.mp3 nasce da ssets/audio/bed.filter (grafo FFmpeg): pad di accordi sui medi (udibile da telefono), battito lieve che sfuma prima della rivelazione, salita di rumore rosa, un istante di vuoto e un colpo grave con attacco morbido a 7,75 s. Livello fisso (nessuna normalizzazione dinamica, che causava scatti) con compressore dolce. Obiettivo: totale ~ -15 dB, sopra 300 Hz ~ -23 dB, nessun salto di livello > 10 dB.
