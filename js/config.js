/* ============================================================
   CONFIGURAZIONE — l'unico file da modificare dopo la pubblicazione
   Dall'11/10/2026 gli ebook sono in esclusiva su Amazon Kindle (KDP Select): niente altri store.
   amazon: pagina Kindle su Amazon.it (KDP). "" = «In arrivo negli store».
   uscita: (facoltativo) data di uscita AAAA-MM-GG: prima di quel giorno il pulsante dice «Prenota su Amazon Kindle», da quel giorno «Disponibile»
   altriStore: lasciare "" finché i libri sono in KDP Select (l'esclusiva vieta altri store digitali).
   kindleUnlimited: true quando l'iscrizione a KDP Select è attiva per tutti i libri:
   mostra «Incluso in Kindle Unlimited» sotto i pulsanti e le frasi [data-ku] delle pagine.
   ============================================================ */
window.SITE = {
  // Link alla pagina di iscrizione alla newsletter (MailerLite). "" = iscrizioni in apertura.
  newsletterUrl: "https://davide-fek7ym.subscribepage.io",
  // GoatCounter (statistiche senza cookie), attivo. "" = spente. Se cambi il codice aggiorna anche la CSP delle pagine (vedi social/kit/analytics.md).
  analytics: { goatcounter: "diasio" },
  // KDP Select / Kindle Unlimited: false finché l'iscrizione non è attiva su KDP (poi true)
  kindleUnlimited: false,
  books: {
    bug:   { amazon: "https://www.amazon.it/dp/B0HLN2VSJP", altriStore: "" },
    oblio: { amazon: "https://www.amazon.it/dp/B0HLMKWJZ5", altriStore: "" },
    vuoto: { amazon: "https://www.amazon.it/dp/B0HM4HFK34", altriStore: "", uscita: "2026-10-23" }, // prenotazione online dal 6/10/2026
    aritmetica: { amazon: "https://www.amazon.it/dp/B0HM3Y19B6", altriStore: "" }
  }
};
