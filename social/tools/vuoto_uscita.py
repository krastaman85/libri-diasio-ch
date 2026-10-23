"""vuoto_uscita.py - campagna di uscita di «Vuoto a rendere» (24/10-13/11/2026): 8 Reel «Listino Sordina», 2 caroselli,
3 grafiche, 6 Storie e 9 TikTok. Ogni post nuovo prende l'orario di un post vecchio nella stessa fascia (quindi resta
nelle finestre di cron-job.org); i post spostati vanno, nell'ordine, nelle prime fasce libere dopo il 13/11.
Uso (dalla radice del repo): python social/tools/vuoto_uscita.py   (idempotente: se i post nuovi ci sono gia non fa nulla)
Decisioni dell'autore (23/10/2026): massimo 2 post al giorno su IG/FB (la rubrica delle 23:10 resta a parte),
musica = strumentali MusicAI licenziati il 13/10, campagna di 3 settimane, immagini esistenti + 15 nuove (Firefly)."""
import json, random
from datetime import datetime, date, timedelta
from pathlib import Path

R = Path(__file__).resolve().parents[2]; CAL = R / 'social' / 'calendar.json'; PUB = R / 'social' / 'published.json'
FINESTRE = {0: [(18, 7, 52), (12, 2, 57)], 1: [(19, 17, 57), (12, 2, 57)], 2: [(19, 17, 57), (12, 2, 57)],
            3: [(12, 12, 52), (19, 7, 52)], 4: [(18, 2, 42), (12, 2, 57)], 5: [(12, 2, 47), (17, 2, 47)],
            6: [(20, 2, 47), (12, 2, 57)]}
AMZ, AMZ_P, SITO = 'https://www.amazon.it/dp/B0HM4HFK34', 'https://www.amazon.it/dp/B0HMFNKKJ2', 'https://libri.diasio.ch/vuoto/'
IG = ['#RomanzoSatirico #UmorismoNero #BookstagramItalia #LibriDaLeggere #Ticino',
      '#Satira #CommediaNera #ConsigliDiLettura #IoLeggo #SvizzeraItaliana',
      '#RomanzoSatirico #LettureDivertenti #BookstagramItalia #ScrittoriItaliani #CulturaTicino',
      '#Satira #Ironia #LibriDaLeggere #ScrittoriEmergenti #LeggereInSvizzera']
FB = ['#RomanzoSatirico #Satira #UmorismoNero #CommediaNera #BookstagramItalia #ConsigliDiLettura #LibriDaLeggere #ScrittoriItaliani #Ticino #LeggereInSvizzera',
      '#RomanzoSatirico #LettureDivertenti #Ironia #Satira #IoLeggo #EditoriaItaliana #ScrittoriEmergenti #SvizzeraItaliana #CulturaTicino #BookstagramSvizzera']
TT = ['#RomanzoSatirico #UmorismoNero #BookTokItalia #LibriDaLeggere #Ticino', '#Satira #CommediaNera #BookTokItalia #ConsigliDiLettura #SvizzeraItaliana']


def ig(testo, k):
    return (testo + '\n\n«Vuoto a rendere», romanzo satirico di D. Iasio, è su Amazon Kindle e in copertina flessibile (link in bio).\n'
            'Incluso in Kindle Unlimited.\n\n' + IG[k % 4])


def fb(testo, k):
    return (testo + '\n\n«Vuoto a rendere», romanzo satirico di D. Iasio.\nEbook su Amazon Kindle: ' + AMZ + '\nCopertina flessibile: ' + AMZ_P +
            '\nIncluso in Kindle Unlimited.\nLa Puntata 1 è gratis, in PDF o EPUB, senza iscrizione: ' + SITO + '\n\n' + FB[k % 2])


def tt(testo, k):
    return (testo + '\n\n«Vuoto a rendere» di D. Iasio: ebook su Amazon Kindle (anche in Kindle Unlimited) e copertina flessibile. Cercalo su Amazon.\n\n' + TT[k % 2])


REEL = [  # id, file, testo, miniatura_ms, alt
 ('vl1-vuoto-sedie', 'Dario contò le sedie: quaranta. Contò le persone: nove. Sei erano sue.\n\nQuante persone, al tuo ultimo saluto, sarebbero lì gratis?', 9500),
 ('vl2-vuoto-lacrime', 'In prima fila Ottavio singhiozzò. Piangeva a comando, con un occhio solo: il sinistro, che dalle file dietro si nota di più.\nTariffa lacrime: otto franchi in più.\n\nQuanto vale una lacrima, se nessuno la vede?', 11000),
 ('vl3-vuoto-regia', 'Spettatori connessi: 1. Località: Rotterdam. Durata collegamento: 31 minuti.\nDavanti alla bara di suo padre, ma da dietro un vetro.\n\nA chi devi ancora una visita, non una videochiamata?', 7000),
 ('vl4-vuoto-algoritmo', 'Nell’ultima foto il vecchio sorrideva a un cane. Il cane non era suo: l’aveva scelto l’algoritmo. I cani fanno engagement.\n\nChe foto sceglierebbe un algoritmo per il tuo addio?', 7500),
 ('vl5-vuoto-modulo', 'Il modulo di commemorazione ha quattro campi: hobby, carattere, ricordo, ultimo saluto. Il campo hobby di Aldo Soldati era vuoto, e con il campo vuoto il sistema scrive «le cose semplici».\n\nCosa scriveresti nel campo hobby di qualcuno che ami?', 7500),
 ('vl6-vuoto-fazzoletto', 'Il terzo sedeva in ultima fila e non era in lista. Non piangeva. Sulla sedia restò un fazzoletto, con due iniziali in filo azzurro: R. C.\n\nChi è R. C.? Lo scopri leggendo.', 12000),
 ('vl7-vuoto-decoro', '«Indice di decoro percepito: novantaquattro.»\n«Il defunto non aveva nessuno.»\n«Il cliente ha avuto esattamente quello che ha pagato.»\n\nSe il decoro si misura, chi misura il vuoto?', 8000),
 ('vl8-vuoto-clic', 'Chiusura pratica: 1 clic. Dario l’aveva fatto più di mille volte in sei anni. Il pollice era già sopra lo schermo.\nNon cliccò.\n\nQual è il clic che non fai più da tempo?', 11500),
]
G = 'social/img/nuovi/'; ST = 'social/img/story/'
ALTRI = [  # id, tipo, file/i, testo, alt
 ('cc-vuoto-cartaceo', 'carosello', [G + 'cc-01-arrivato.jpg', G + 'cc-02-sottolineare.jpg', G + 'cc-03-una-sera.jpg', G + 'cc-04-cta.jpg'],
  'È arrivato il cartaceo. «Vuoto a rendere» in copertina flessibile, 112 pagine: da sottolineare, da prestare, da lasciare sul comodino di chi organizza sempre tutto.',
  'Carosello di quattro slide: il libro Vuoto a rendere su un tavolo di legno accanto a un caffè («È arrivato il cartaceo»); la frase «Sembra. Il prodotto era quello. Non il funerale: il sembra.»; il libro su una poltrona («Da leggere in una sera»); copertina e formati su Amazon.'),
 ('cl-vuoto-listino', 'carosello', [G + 'cl-01-domanda.jpg', G + 'cl-02-voce01.jpg', G + 'cl-03-comparse.jpg', G + 'cl-04-lacrime.jpg', G + 'cl-05-bonifica.jpg', G + 'cl-06-totale.jpg'],
  'Quanto costa un funerale che sembra pieno? Le voci del listino di Sala Ulivo, tutte dalla Puntata 1 di «Vuoto a rendere». Scorri fino al totale.',
  'Carosello di sei slide in stile scontrino: Sala Ulivo 1200 franchi, comparse 25 franchi l’ora, tariffa lacrime più 8, bonifica 3300; in chiusura «Il cliente ha avuto esattamente quello che ha pagato.» e la copertina.'),
 ('g-vuoto-fuori-sala', 'immagine', G + 'g-fuori-sala.jpg',
  'Ogni capitolo di «Vuoto a rendere» finisce con un riquadro «Fuori sala», rivolto a chi legge. Questo è il primo.\nRispondi nei commenti, o anche solo a te stesso.',
  'Su fondo grafite la domanda: «Chi siederebbe in prima fila al tuo funerale, e da quanto non gli dai un motivo per starci?»'),
 ('g-vuoto-pov', 'immagine', G + 'g-pov-modulo.jpg',
  'POV: il campo hobby del tuo modulo di commemorazione è vuoto. Il sistema scrive «le cose semplici». Funziona con la maggior parte dei ticinesi.',
  'Un registro delle presenze aperto su un leggio bianco, con la scritta «POV: il campo hobby del tuo modulo di commemorazione è vuoto.»'),
 ('g-vuoto-per-chi', 'immagine', G + 'g-per-chi.jpg',
  'Per chi ama vedere smascherata l’ipocrisia, con un sorriso storto. «Vuoto a rendere» è un romanzo satirico ambientato in Ticino, e si legge in una sera.',
  'Una celebrante al leggio in una sala del commiato chiara, con la scritta «Per chi ama vedere smascherata l’ipocrisia, con un sorriso storto.»'),
]
STORIE = ['st-cartaceo', 'st-fuori-sala', 'st-stasera', 'st-ku', 'st-listino', 'st-sembra']

# (data, fascia 'L'/'E', id nuovo, id vecchio da spostare)
PIANO = [
 ('2026-10-24', 'vl1-vuoto-sedie', 'n21-bug-non-rimovibile'), ('2026-10-25', 'st-vuoto-cartaceo', 'n22-oblio-undici-centimetri'),
 ('2026-10-26', 'cc-vuoto-cartaceo', 'n23-oblio-kindle'), ('2026-10-27', 'vl2-vuoto-lacrime', '11-oblio-bitcoin'),
 ('2026-10-28', 'g-vuoto-fuori-sala', 'n25-oblio-suora'), ('2026-10-29', 'vl3-vuoto-regia', 'n26-oblio-firma'),
 ('2026-10-30', 'vl4-vuoto-algoritmo', 'n28-oblio-strano'), ('2026-10-31', 'cl-vuoto-listino', 'n29-bug-presidente-parrocchia'),
 ('2026-11-01', 'vl5-vuoto-modulo', '13-oblio-cta'), ('2026-11-02', 'g-vuoto-pov', 'n31-oblio-regolamento'),
 ('2026-11-03', 'vl6-vuoto-fazzoletto', '14-bug-rimossa'), ('2026-11-04', 'st-vuoto-fuori-sala', 'n09-bug-alma'),
 ('2026-11-05', 'vl7-vuoto-decoro', '03-bug-cognato'), ('2026-11-06', 'g-vuoto-per-chi', 'n20-bug-elio-bassi'),
 ('2026-11-07', 'st-vuoto-stasera', 'n13-oblio-ricordo-non-suo'), ('2026-11-08', 'vl8-vuoto-clic', '16-bug-spot'),
 ('2026-11-09', 'st-vuoto-ku', 's03-oblio-cugino'), ('2026-11-10', 'st-vuoto-listino', '08-oblio-levia'),
 ('2026-11-12', 'st-vuoto-sembra', '18-bug-regolamento'),
]
TIKTOK = [('2026-10-24', 'vl1-vuoto-sedie', '20:16'), ('2026-10-25', 'trailer', '19:41'), ('2026-10-26', 'vl2-vuoto-lacrime', '20:52'),
          ('2026-10-28', 'vl3-vuoto-regia', '19:58'), ('2026-10-30', 'vl4-vuoto-algoritmo', '20:37'), ('2026-11-01', 'vl5-vuoto-modulo', '19:23'),
          ('2026-11-03', 'vl6-vuoto-fazzoletto', '21:04'), ('2026-11-05', 'vl7-vuoto-decoro', '20:11'), ('2026-11-07', 'vl8-vuoto-clic', '19:47')]
TRAILER_TT = ('Dario progetta funerali che sembrano pieni. Quaranta sedie, nove presenti, sei pagate. Poi si chiede chi fosse il morto.\n\n'
              'Il trailer di «Vuoto a rendere», uscito il 23 ottobre.')


def nuovo_post(nid, quando, k):
    reel = {r[0]: r for r in REEL}; alt = {a[0]: a for a in ALTRI}
    if nid in reel:
        _, testo, mini = reel[nid]
        return {'id': nid, 'tipo': 'reel', 'quando': quando, 'segmento': 'Reel · Listino Sordina · uscita di Vuoto a rendere',
                'video': 'social/video/%s.mp4' % nid, 'miniatura_ms': mini, 'didascalia': ig(testo, k), 'didascalia_fb': fb(testo, k)}
    if nid in alt:
        _, tipo, files, testo, a = alt[nid]
        p = {'id': nid, 'quando': quando, 'segmento': 'Uscita di Vuoto a rendere · ' + ('carosello' if tipo == 'carosello' else 'grafica'),
             'alt': a, 'didascalia': ig(testo, k), 'didascalia_fb': fb(testo, k)}
        if tipo == 'carosello': p['tipo'] = 'carosello'; p['immagini'] = files
        else: p['immagine'] = files
        return p
    if nid.startswith('st-vuoto-'):
        f = 'st-' + nid[len('st-vuoto-'):]
        return {'id': nid, 'tipo': 'storia', 'quando': quando, 'segmento': 'Storia · uscita di Vuoto a rendere', 'immagine': ST + f + '.jpg'}
    raise KeyError(nid)


def main():
    raw = CAL.read_bytes().decode('utf-8'); nl = '\r\n' if '\r\n' in raw else '\n'
    cal = json.loads(raw); posts = cal['post']; pub = json.loads(PUB.read_text(encoding='utf-8'))['pubblicati']
    ids = {p['id']: p for p in posts}
    if 'vl1-vuoto-sedie' in ids: print('gia presente: nulla da fare'); return
    norm = lambda p: not (p['id'][:1] == 'q' and p['id'][1:3].isdigit()) and p.get('piattaforme') != ['tiktok']
    spostati = []
    for k, (g, nid, vid) in enumerate(PIANO):
        v = ids[vid]; assert v['quando'][:10] == g and vid not in pub, (vid, v['quando'])
        posts.append(nuovo_post(nid, v['quando'], k)); spostati.append(v)
    # fasce libere dopo il 13/11
    occ = {(p['quando'][:10], int(p['quando'][11:13])) for p in posts if norm(p) and p not in spostati}
    liberi = []
    d = date(2026, 11, 14)
    while d <= date(2026, 12, 31):
        for (h, a, b) in sorted(FINESTRE[d.weekday()]):
            if (d.isoformat(), h) not in occ: liberi.append((d, h, a, b))
        d += timedelta(days=1)
    rnd = random.Random(2310)
    for v, (d, h, a, b) in zip(spostati, liberi):
        vicini = {int(p['quando'][14:16]) for p in posts if norm(p) and p is not v and p['quando'][11:13] == '%02d' % h
                  and datetime.fromisoformat(p['quando']).weekday() == d.weekday() and abs((datetime.fromisoformat(p['quando']).date() - d).days) <= 7}
        mm = [m for m in range(max(0, a - 4), b - 1) if m not in vicini and m % 5 not in (0,)]
        m = rnd.choice(mm)
        print('sposto %-32s %s -> %s %02d:%02d' % (v['id'], v['quando'], d.isoformat(), h, m))
        v['quando'] = '%s %02d:%02d'.replace(' ', 'T') % (d.isoformat(), h, m)
    # TikTok (Buffer)
    for k, (g, nid, ora) in enumerate(TIKTOK):
        if nid == 'trailer':
            posts.append({'id': 'tl0-vuoto-trailer', 'tipo': 'reel', 'quando': g + 'T' + ora, 'segmento': 'TikTok · trailer di Vuoto a rendere',
                          'video': 'social/video/tiktok/vuoto-trailer-9x16.mp4', 'miniatura_ms': 1500, 'piattaforme': ['tiktok'], 'ia': True,
                          'didascalia': tt(TRAILER_TT, k)})
        else:
            testo = {r[0]: r[1] for r in REEL}[nid]
            posts.append({'id': 't' + nid, 'tipo': 'reel', 'quando': g + 'T' + ora, 'segmento': 'TikTok · Listino Sordina · Vuoto a rendere',
                          'video': 'social/video/%s.mp4' % nid, 'miniatura_ms': {r[0]: r[2] for r in REEL}[nid], 'piattaforme': ['tiktok'], 'ia': True,
                          'didascalia': tt(testo, k)})
    posts.sort(key=lambda p: p['quando'])
    CAL.write_bytes((json.dumps(cal, indent=2, ensure_ascii=False) + '\n').replace('\n', nl).encode('utf-8'))
    print('post nel calendario:', len(posts))


if __name__ == '__main__':
    main()
