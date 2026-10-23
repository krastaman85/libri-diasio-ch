/* ============================================================
   CONFIGURAZIONE — l'unico file da modificare dopo la pubblicazione
   Dall'11/10/2026 gli ebook sono in esclusiva su Amazon Kindle (KDP Select): niente altri store.
   amazon: pagina Kindle su Amazon.it (KDP). "" = «In arrivo negli store».
   uscita: (facoltativo) data di uscita AAAA-MM-GG: prima di quel giorno il pulsante dice «Prenota su Amazon Kindle», da quel giorno «Disponibile»
   altriStore: lasciare "" finché i libri sono in KDP Select (l'esclusiva vieta altri store digitali).
   cartaceo: (facoltativo) pagina Amazon della copertina flessibile (KDP Print): aggiunge il pulsante «Cartaceo su Amazon».
   kindleUnlimited: true quando l'iscrizione a KDP Select è attiva per tutti i libri:
   mostra «Incluso in Kindle Unlimited» sotto i pulsanti e le frasi [data-ku] delle pagine.
   ============================================================ */
window.SITE = {
  // Link alla pagina di iscrizione alla newsletter (MailerLite). "" = iscrizioni in apertura.
  newsletterUrl: "https://davide-fek7ym.subscribepage.io",
  // GoatCounter (statistiche senza cookie), attivo. "" = spente. Se cambi il codice aggiorna anche la CSP delle pagine (vedi social/kit/analytics.md).
  analytics: { goatcounter: "diasio" },
  // KDP Select / Kindle Unlimited: iscrizione attiva per i 4 ebook dall’11/10/2026
  kindleUnlimited: true,
  books: {
    bug:   { amazon: "https://www.amazon.it/dp/B0HLN2VSJP", altriStore: "" },
    oblio: { amazon: "https://www.amazon.it/dp/B0HLMKWJZ5", altriStore: "" },
    vuoto: { amazon: "https://www.amazon.it/dp/B0HM4HFK34", cartaceo: "https://www.amazon.it/dp/B0HMFNKKJ2", altriStore: "", uscita: "2026-10-23" }, // uscito il 23/10/2026; brossura 112 pp. in vendita dal 23/10
    aritmetica: { amazon: "https://www.amazon.it/dp/B0HM3Y19B6", altriStore: "" }
  }
};
