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
    bug:   { amazon: "https://www.amazon.it/dp/B0HLN2VSJP", altriStore: "" },
    oblio: { amazon: "https://www.amazon.it/dp/B0HLMKWJZ5", altriStore: "" },
    vuoto: { amazon: "https://www.amazon.it/dp/B0HM4HFK34", altriStore: "", uscita: "2026-10-23" },
    aritmetica: { amazon: "https://www.amazon.it/dp/B0HM3Y19B6", altriStore: "" }
  }
};
