/* ============================================================
   CONFIGURAZIONE — l'unico file da modificare dopo la pubblicazione
   Quando un libro è online in uno store, incolla qui il link.
   Lascia "" per mostrare "In arrivo negli store" (o "Prossimamente su StreetLib"
   se c'è già il link Amazon).
   amazon: pagina Kindle su Amazon.it (KDP)
   uscita: (facoltativo) data di uscita AAAA-MM-GG: prima di quel giorno il pulsante dice «Prenota su Amazon Kindle», da quel giorno «Disponibile»
   altriStore: pagina StreetLib, o di uno degli store che distribuisce (Kobo, Apple Books, Google Play Libri)
   ============================================================ */
window.SITE = {
  // Link alla pagina di iscrizione alla newsletter (MailerLite). "" = iscrizioni in apertura.
  newsletterUrl: "https://davide-fek7ym.subscribepage.io",
  // GoatCounter (statistiche senza cookie), attivo. "" = spente. Se cambi il codice aggiorna anche la CSP delle pagine (vedi social/kit/analytics.md).
  analytics: { goatcounter: "diasio" },
  books: {
    bug:   { amazon: "https://www.amazon.it/dp/B0HLN2VSJP", altriStore: "https://store.streetlib.com/fiction/il-bug-della-trasparenza-il-silenzio-e-finito-la-verita-e-pubblica-1008988/" },
    oblio: { amazon: "https://www.amazon.it/dp/B0HLMKWJZ5", altriStore: "https://store.streetlib.com/fiction/l-economia-dell-oblio-chi-dimentica-diventa-innocente-paga-solo-chi-ricorda-1008980/" },
    vuoto: { amazon: "https://www.amazon.it/dp/B0HM4HFK34", altriStore: "", uscita: "2026-10-23" }, // prenotazione online dal 6/10/2026
    aritmetica: { amazon: "https://www.amazon.it/dp/B0HM3Y19B6", altriStore: "https://store.streetlib.com/noir/l-aritmetica-del-consenso-romanzo-in-sei-puntate-1012194/" }
  }
};
