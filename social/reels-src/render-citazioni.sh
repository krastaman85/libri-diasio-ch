#!/bin/bash
# Rubrica «Citazioni D. Iasio»: Reel (index-citazione.html) e Storia (fotogramma finale) per ogni qNN.
# Uso (dalla cartella social/reels-src): ./render-citazioni.sh q01-mutuo q02-cena ...   (senza argomenti: tutte le vars/q*.json)
set -u
cd "$(dirname "$0")"
W=$(mktemp -d)
cp -r assets hyperframes.json meta.json package.json "$W"/
cp index-citazione.html "$W"/index.html
mkdir -p "$W"/vars ../img/story
ids=("$@")
[ ${#ids[@]} -eq 0 ] && ids=($(ls vars/q*.json | xargs -n1 basename | sed 's/\.json$//'))
for n in "${ids[@]}"; do
  cp vars/$n.json "$W"/vars/
  ( cd "$W" && npx --yes hyperframes@0.8.96 render . --variables-file vars/$n.json -q high -o renders/$n.mp4 >/dev/null 2>&1 ) || { echo "ERRORE $n"; continue; }
  ffmpeg -loglevel error -y -i "$W"/renders/$n.mp4 -c:v libx264 -preset slow -crf 25 -pix_fmt yuv420p -profile:v high -movflags +faststart -c:a aac -b:a 128k ../video/$n.mp4 \
    && ffmpeg -loglevel error -y -ss 12.5 -i "$W"/renders/$n.mp4 -frames:v 1 -q:v 2 ../img/story/$n.jpg \
    && echo "ok $n"
done
rm -rf "$W"
