/* ============================================================
   CONFIGURAZIONE — l'unico file da modificare dopo la pubblicazione
   Quando un libro è online in uno store, incolla qui il link.
   Lascia "" per mostrare "In arrivo negli store" (o "Prossimamente su StreetLib"
   se c'è già il link Amazon).
   amazon: pagina Kindle su Amazon.it (KDP)
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
    vuoto: { amazon: "", altriStore: "" }
  }
};
