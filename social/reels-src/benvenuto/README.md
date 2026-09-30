# Reel di benvenuto (r00)

Composizione unica di 17 s (1080×1920): due domande (una per romanzo), «Due romanzi. A puntate. Una sera alla volta.», poi le due copertine e l'invito a leggere la Puntata 1.

```bash
npx hyperframes@0.8.96 check .
npx hyperframes@0.8.96 render . -q high -o renders/intro.mp4
ffmpeg -i renders/intro.mp4 -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p -profile:v high -movflags +faststart -c:a aac -b:a 160k ../../video/r00-benvenuto.mp4
```

Audio: `assets/audio/intro.filter` (grafo FFmpeg, stessa famiglia del Reel delle citazioni: pad sui medi, salita di rumore, colpo grave morbido a 12,6 s) più compressore dolce e guadagno fisso; livello medio ≈ -15 dB, nessun salto brusco. Le sorgenti e i livelli sono in `assets/audio/intro.filter`.
