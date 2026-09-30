#!/bin/bash
# Uso: ./render-all.sh r13-oblio-furto r14-...   (dalla cartella social/reels-src)
mkdir -p renders
for n in "$@"; do
  npx --yes hyperframes@0.8.96 render . --variables-file vars/$n.json -q high -o renders/$n.mp4 >/dev/null 2>&1 || { echo "ERRORE $n"; continue; }
  ffmpeg -loglevel error -y -i renders/$n.mp4 -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p -profile:v high -movflags +faststart -c:a aac -b:a 160k ../video/$n.mp4 && echo "ok $n"
done
