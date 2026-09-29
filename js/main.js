(function () {
  "use strict";
  var S = window.SITE || { books: {} };

  // Anno nel footer
  document.querySelectorAll("[data-year]").forEach(function (e) { e.textContent = new Date().getFullYear(); });

  // Pulsante newsletter
  document.querySelectorAll("[data-news]").forEach(function (a) {
    if (S.newsletterUrl) { a.href = S.newsletterUrl; a.removeAttribute("aria-disabled"); }
    else { a.setAttribute("aria-disabled", "true"); a.setAttribute("tabindex", "-1"); a.textContent = "Iscrizioni in apertura"; }
  });

  // Link negli store
  document.querySelectorAll("[data-stores]").forEach(function (box) {
    var b = (S.books || {})[box.getAttribute("data-stores")] || {};
    var out = [];
    if (b.amazon) out.push('<a class="btn primary" href="' + b.amazon + '" rel="noopener">Amazon</a>');
    if (b.altriStore) out.push('<a class="btn" href="' + b.altriStore + '" rel="noopener">Altri store</a>');
    box.innerHTML = out.length ? out.join("") : '<span class="pill">In arrivo negli store</span>';
  });

  // Il Bug: messaggi della bacheca "Trasparenza attiva"
  var app = document.querySelector("[data-app]");
  if (app) {
    var msgs = [
      "Il preventivo B è di mio cognato. Se lo dico gli altri capiscono e mi tolgono la presidenza.",
      "Nessuno ha la mia password.",
      "Ho un segreto e in questo palazzo lo sanno già tutti.",
      "Mi sento osservato. Da quanto tempo non guardo più fuori dalla finestra?",
      "Chiedi chi lo ha creato. Chiedilo a voce alta.",
      "L'assemblea è fra dieci giorni e io non voglio andarci."
    ];
    var p = app.querySelector("p"), i = 0;
    p.textContent = msgs[0];
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!reduce) {
      setInterval(function () {
        p.style.opacity = 0;
        setTimeout(function () { i = (i + 1) % msgs.length; p.textContent = msgs[i]; p.style.opacity = 1; }, 350);
      }, 5200);
      p.style.transition = "opacity .35s";
    }
  }
})();
