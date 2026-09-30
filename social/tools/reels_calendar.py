"""Aggiunge a ../calendar.json i Reel r07-r23 (senza duplicare). Uso, da social/tools: python reels_calendar.py
I video sono in ../video/ (render con reels-src/render-all.sh); le citazioni sono in reels-src/vars/<id>.json."""
import json, re
from pathlib import Path

SOCIAL = Path(__file__).resolve().parent.parent
CTA = "Puntata 1 gratis in PDF ed EPUB, senza iscrizione: link in bio."
# (id, quando, segmento, didascalia, hashtag)
REELS = [
 ("r07-bug-attivare", "2026-10-21T19:30", "Reel · Mondo del lavoro (chi «esegue e basta»)",
  "Il classico «io eseguo». Un portiere, un’email con le istruzioni e un aggiornamento da attivare entro le diciannove del quindici.",
  "#noir #thriller #mondodellavoro #narrativaitaliana #libriconsigliati"),
 ("r08-oblio-listino", "2026-10-24T12:30", "Reel · Satira del lavoro + distopia",
  "Un lutto pulito quattromila euro, una vergogna novecento. Il listino di uno studio di estrazioni, tra satira e distopia.\nNel romanzo il dolore è una materia prima: si estrae, si classifica, si vende.",
  "#thrillerpsicologico #distopia #satira #fantascienza #narrativaitaliana"),
 ("r09-bug-notifica", "2026-10-28T19:30", "Reel · Tech/privacy/app",
  "Nessuno legge le note di rilascio. Tutti approvano per acclamazione. Poi tutti i telefoni della sala vibrano insieme.\nÈ così che comincia Il Bug della Trasparenza.",
  "#privacy #tecnologia #thriller #noir #narrativaitaliana"),
 ("r10-oblio-innocente", "2026-10-31T12:30", "Reel · Atmosfera Halloween + lettori thriller",
  "Per un Halloween senza zucche: «Chi dimentica diventa innocente. Paga solo chi ricorda.»\nUn thriller psicologico in sei puntate.",
  "#thrillerpsicologico #halloween #distopia #narrativaitaliana #brividi"),
 ("r11-oblio-benissimo", "2026-11-04T19:30", "Reel · Psicologia/memoria (tono rispettoso)",
  "Il cliente esce più leggero e con la sensazione di aver perso qualcosa. «Ma sto benissimo, eh. Benissimo.»\nIl romanzo parla di questo: cosa resta di noi quando ci togliamo ciò che fa male.",
  "#thrillerpsicologico #memoria #psicologia #narrativaitaliana #bookstagram"),
 ("r12-bug-vicino", "2026-11-07T12:30", "Reel · Vita di condominio + lettori noir",
  "Nel tuo condominio c’è un’app per tutto: cancello, pacchi, assemblee. Ora immagina che una sera cominci a dire la verità.",
  "#noir #condominio #vicinidicasa #thrillersociale #narrativaitaliana"),
 ("r13-oblio-furto", "2026-11-11T19:30", "Reel · Community (commenti) + psicologia",
  "Atto d’amore o furto? Dora Calvi non l’ha ancora deciso, e forse dipende da chi lo racconta. Tu cosa diresti? Dimmelo nei commenti.",
  "#thrillerpsicologico #memoria #distopia #narrativaitaliana #bookstagram"),
 ("r14-bug-amministrazione", "2026-11-14T12:30", "Reel · Tech/privacy + giornalismo",
  "L’app non si spegne da sola: per disattivarla serve l’amministrazione. Cioè proprio l’uomo che l’app ha appena smascherato.",
  "#noir #thriller #privacy #giornalismo #narrativaitaliana"),
 ("r15-oblio-firma", "2026-11-18T19:30", "Reel · Fantascienza/distopia + lettori thriller",
  "Nel suo fascicolo Dora Calvi trova una firma che riconosce e un ricordo che non ha. Una delle due cose mente.",
  "#thrillerpsicologico #distopia #fantascienza #blackmirror #narrativaitaliana"),
 ("r16-bug-silenzio", "2026-11-21T12:30", "Reel · Lettori noir (core)",
  "Quaranta persone in una sala, un telefono che dice la verità, e nessuno che respira. La scena che apre il romanzo.",
  "#noir #thriller #narrativaitaliana #bookstagram #libriconsigliati"),
 ("r17-oblio-comitato", "2026-11-25T19:30", "Reel · Satira aziendale + distopia",
  "Dopo ogni estrazione: undici minuti nella Sala Prato. Un prato, un cane, e un cane scelto da un comitato. Satira aziendale, dal romanzo.",
  "#distopia #satira #mondodellavoro #thrillerpsicologico #narrativaitaliana"),
 ("r18-bug-note-rilascio", "2026-11-28T12:30", "Reel · Tech/privacy + condominio",
  "Nessuno legge le note di rilascio, nessuno legge il regolamento. È così che comincia.",
  "#privacy #tecnologia #condominio #noir #narrativaitaliana"),
 ("r19-oblio-brescia", "2026-12-02T19:30", "Reel · Psicologia/memoria (tono rispettoso)",
  "Un lutto, visto da dentro: i sei minuti che il cliente vuole dimenticare. Un romanzo sulla colpa e su ciò che resta di noi.",
  "#thrillerpsicologico #memoria #psicologia #narrativaitaliana #bookstagram"),
 ("r20-bug-acclamazione", "2026-12-05T12:30", "Reel · Vita di condominio + umorismo nero",
  "«Il punto quattro è una formalità.» Le ultime parole famose di un presidente d’assemblea.",
  "#noir #condominio #thrillersociale #narrativaitaliana #libriconsigliati"),
 ("r21-oblio-gratis", "2026-12-09T19:30", "Reel · Tech/IA + lavoro",
  "Il dolore è l’unica materia prima che la gente produce gratis. Bastava trovare chi la comprava.",
  "#thrillerpsicologico #intelligenzaartificiale #distopia #fantascienza #narrativaitaliana"),
 ("r22-bug-rettifica", "2026-12-12T12:30", "Reel · Giornalismo d’inchiesta + noir",
  "Nadia Colombo ha perso la carriera per un articolo. Ora vive nel palazzo dove tutto è cominciato, sotto copertura.",
  "#giornalismo #inchiesta #noir #thriller #narrativaitaliana"),
 ("r23-oblio-cara", "2026-12-16T19:30", "Reel · Mondo del lavoro + satira",
  "La Direttrice la chiama «cara», come si chiamano i cani appena adottati. E l’ha vista barare sul modulo prima ancora che finisse di sbadigliare.",
  "#thrillerpsicologico #mondodellavoro #satira #distopia #narrativaitaliana"),
]


def fb(cap, tags):
    return re.sub(r"link in bio\.?", "https://libri.diasio.ch/", cap, flags=re.I) + "\n\n" + " ".join(tags.split()[:3])


def main():
    p = SOCIAL / "calendar.json"
    cal = json.loads(p.read_text(encoding="utf-8"))
    have = {x["id"] for x in cal["post"]}
    for rid, when, seg, text, tags in REELS:
        if rid in have:
            continue
        cap = text + "\n" + CTA + "\n\n" + tags
        cal["post"].append({"id": rid, "tipo": "reel", "quando": when, "segmento": seg, "video": f"social/video/{rid}.mp4",
                            "miniatura_ms": 5500, "didascalia": cap, "didascalia_fb": fb(text + "\n" + CTA, tags)})
        print("+", rid, when)
    cal["post"].sort(key=lambda x: x["quando"])
    p.write_text(json.dumps(cal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
