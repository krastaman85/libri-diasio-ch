"""pulisci_media.py: elenca (o toglie dal repo) i media social che non servono più.

Da lanciare dopo ogni serie di post, dalla radice del repo:
    python3 social/tools/pulisci_media.py              # solo elenco e totali
    python3 social/tools/pulisci_media.py --rimuovi    # git rm dei file elencati

Un file si può togliere se, guardando social/video, social/img e social/audio-nuovi:
  - è usato solo da post già usciti su tutte le loro piattaforme (stato in social/published.json,
    stessa regola di pending() in publish.py, TikTok compreso) e il sito non lo usa, oppure
  - non è usato da nessun post e il suo nome non compare in nessun file di testo del repo
    (se uno script lo nomina può essere materiale di partenza: si tiene).
Non si toglie mai un file usato da un post ancora da pubblicare.
I file tolti restano nella cronologia di git; prima di toglierli, copiarli in Drive
(«Archivio media social pubblicati»): la cartella di destinazione la sceglie chi lancia lo script.
"""
import json
import os
import subprocess
import sys

R = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, os.path.join(R, "social"))
os.chdir(R)
import publish  # noqa: E402  (stessa logica di pending())

CARTELLE = ("social/video/", "social/img/", "social/audio-nuovi/")
TESTO = (".html", ".js", ".css", ".py", ".sh", ".md", ".json", ".txt", ".yml", ".yaml", ".xml")
SITO = (".html", ".js", ".css", ".xml", ".txt", ".webmanifest")


def file_del_post(p):
    out = [p[k] for k in ("video", "immagine") if p.get(k)]
    out += list(p.get("immagini") or [])
    return out


def main():
    rimuovi = "--rimuovi" in sys.argv
    cal = json.load(open("social/calendar.json", encoding="utf-8"))
    state = json.load(open("social/published.json", encoding="utf-8"))
    serve, usato = set(), set()
    for p in cal["post"]:
        fs = file_del_post(p)
        usato.update(fs)
        # come in produzione: IG e FB per i post normali (testo solo FB), TikTok per quelli marcati tiktok
        plats = ["tiktok"] if publish.is_tiktok(p) else ["instagram", "facebook"]
        if publish.pending(p, state, plats):
            serve.update(fs)
    tracciati = subprocess.run(["git", "ls-files", "-z"], capture_output=True, text=True, check=True).stdout.split("\0")
    media = [f for f in tracciati if f.startswith(CARTELLE)]
    # dove cercare i nomi: il sito (che li servirebbe davvero) e tutto il testo del repo
    # (calendario e stato esclusi: li valuta già la logica dei post)
    def leggi(fs):
        t = ""
        for f in fs:
            if os.path.isfile(f):
                try:
                    t += open(f, encoding="utf-8", errors="ignore").read() + "\n"
                except OSError:
                    pass
        return t
    sito = leggi(f for f in tracciati if f.endswith(SITO) and not f.startswith("social/"))
    testi = leggi(f for f in tracciati if f.endswith(TESTO) and f not in ("social/calendar.json", "social/published.json"))
    via, tot = [], 0
    for f in sorted(media):
        if f in serve:
            continue
        nome = os.path.splitext(os.path.basename(f))[0]
        if f in usato:
            # uscito ovunque: si tiene solo se il sito lo usa (gli script lo hanno solo generato)
            if nome in sito:
                continue
            motivo = "post già pubblicato"
        else:
            # mai usato: si tiene se un file del repo lo nomina (può essere materiale di partenza di uno script)
            if nome in testi:
                continue
            motivo = "non usato da nessun post"
        s = os.path.getsize(f)
        via.append(f)
        tot += s
        print(f"{s / 1048576:6.2f} MB  {f}  ({motivo})")
    print(f"\n{len(via)} file, {tot / 1048576:.1f} MB da togliere su {len(media)} media tracciati")
    if rimuovi and via:
        for i in range(0, len(via), 100):
            subprocess.run(["git", "rm", "-q", "--"] + via[i:i + 100], check=True)
        print("Tolti con git rm: ora test, commit e PR.")


if __name__ == "__main__":
    main()
