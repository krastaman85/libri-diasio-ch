/* ============================================================
   CONFIGURAZIONE — l'unico file da modificare dopo la pubblicazione
   Quando i libri sono online negli store, incolla qui i link.
   Lascia "" per mostrare "In arrivo negli store".
   ============================================================ */
window.SITE = {
  // Link alla pagina di iscrizione alla newsletter (MailerLite). "" = iscrizioni in apertura.
  newsletterUrl: "https://davide-fek7ym.subscribepage.io",
  // Statistiche visite senza cookie (GoatCounter). Codice del sito, es. "diasio" per diasio.goatcounter.com.
  // "" = spente. Quando lo imposti, aggiorna anche la CSP delle pagine e la pagina Privacy (vedi social/kit/analytics.md).
  analytics: { goatcounter: "" },
  books: {
    bug:   { amazon: "", altriStore: "" },   // altriStore: pagina StreetLib/Kobo/Apple
    oblio: { amazon: "", altriStore: "" }
  }
};
