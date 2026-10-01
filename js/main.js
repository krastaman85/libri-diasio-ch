(function () {
  "use strict";
  var S = window.SITE || { books: {} };

  // Anno nel footer
  document.querySelectorAll("[data-year]").forEach(function (e) { e.textContent = new Date().getFullYear(); });

  // Statistiche visite: GoatCounter, senza cookie né dati personali. Attive solo se configurate.
  if (S.analytics && /^[a-z0-9-]+$/.test(S.analytics.goatcounter || "")) {
    var gc = document.createElement("script");
    gc.async = true;
    gc.src = "https://gc.zgo.at/count.js";
    gc.setAttribute("data-goatcounter", "https://" + S.analytics.goatcounter + ".goatcounter.com/count");
    document.head.appendChild(gc);
  }

  // Pulsante newsletter
  document.querySelectorAll("[data-news]").forEach(function (a) {
    if (S.newsletterUrl) { a.href = S.newsletterUrl; a.rel = "noopener"; a.removeAttribute("aria-disabled"); }
    else { a.setAttribute("aria-disabled", "true"); a.setAttribute("tabindex", "-1"); a.textContent = "Iscrizioni in apertura"; }
  });

  // Link negli store
  document.querySelectorAll("[data-stores]").forEach(function (box) {
    var b = (S.books || {})[box.getAttribute("data-stores")] || {};
    var out = [];
    if (b.amazon) out.push('<a class="btn primary" href="' + b.amazon + '" rel="noopener">Amazon Kindle</a>');
    if (b.altriStore) out.push('<a class="btn" href="' + b.altriStore + '" rel="noopener">Altri store</a>');
    else if (b.amazon) out.push('<span class="pill">Prossimamente su StreetLib</span>');
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
  // ---- Schede animate: frammenti de L'Economia dell'Oblio e fascicolo di Vuoto a rendere.
  // Tutti i testi sono testuali dalle Puntata 1 (download/*.epub). Senza JS, o con "riduci movimento", resta il primo elemento statico.
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function mk(tag, cls, txt) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; }
  function wait(ms, fn) { return setTimeout(function () { if (document.hidden) return wait(600, fn); fn(); }, ms); }

  var ob = document.querySelector('[data-feed="oblio"]');
  if (ob && !reduceMotion) {
    var FR = [
      ["Gianfranco Merli · cliente", "«Io lo dico sempre ai miei ragazzi: il dolore è un costo. E i costi si tagliano.»"],
      ["Dora Calvi · tecnica estrattiva", "«Signor Merli, mi porti a quel giorno. Non lo racconti, lo pensi.»"],
      ["Sul monitor · estrazione Merli", "Stanza 314. Tapparella abbassata a metà, quella luce gialla da corridoio che entra di sbieco."],
      ["Sul monitor · estrazione Merli", "«Scusa» dice Gianfranco al morto. «Era Brescia.»"],
      ["Studio Levia · Porta Romana", "«Nessuno è pulito» dice Nico. «Siamo tutti solo in ritardo con l’igiene.»"],
      ["Sala Prato · dopo l’estrazione", "Freddo sotto le ginocchia: piastrelle. Un bagno piccolo, una lampadina sola. Odore di shampoo alla pesca, quello economico, che si vende in flaconi da un litro."],
      ["Dora Calvi", "Ho un ricordo che non voglio e una firma che non ricordo."]
    ];
    var REC = [["Estrazioni a proprio carico:", "1"], ["Data:", "11 mesi e 3 giorni fa"], ["Contenuto:", "[OSCURATO — LIVELLO DIREZIONE]", "x"],
               ["Consenso informato:", "FIRMATO"], ["Compenso:", "nessuno"], ["Destinazione del lotto:", "NON REGISTRATA"]];
    var obBody = ob.querySelector(".feed-body"), dots = ob.querySelector(".dots"), n = 0;
    for (var d = 0; d <= FR.length; d++) dots.appendChild(mk("i"));
    function obShow(i) {
      var dd = dots.children; for (var k = 0; k < dd.length; k++) dd[k].className = k === i ? "on" : "";
      ob.classList.remove("on");
      if (i < FR.length) {
        obBody.innerHTML = "";
        obBody.appendChild(mk("p", "frag-who", FR[i][0]));
        var p = mk("p", "frag"), t = mk("span", "t", FR[i][1]); p.appendChild(t); p.appendChild(mk("span", "bar")); obBody.appendChild(p);
        wait(60, function () { ob.classList.add("on"); });
        wait(5600, function () { ob.classList.remove("on"); wait(1150, function () { obShow(i + 1); }); });
      } else {
        obBody.innerHTML = "";
        var rec = mk("div", "rec");
        REC.forEach(function (r) {
          var row = mk("div"); row.appendChild(mk("span", "k", r[0])); row.appendChild(mk("span", "v" + (r[2] ? " x" : ""), r[1])); rec.appendChild(row);
        });
        obBody.appendChild(rec);
        var rows = rec.children;
        for (var r = 0; r < rows.length; r++) (function (r) { wait(250 + r * 420, function () { rows[r].className = "in"; }); })(r);
        wait(250 + 3 * 420 + 900, function () { var x = rec.querySelector(".x"); if (x) x.classList.add("open"); });
        wait(8200, function () { obShow(0); });
      }
    }
    obShow(0);
  }

  var vu = document.querySelector('[data-feed="vuoto"]');
  if (vu && !reduceMotion) {
    var LG = [
      ["Fascicolo", "Soldati Aldo, n. 1947. Deceduto: 31 agosto. Ritrovamento: 14 settembre. Causa: indeterminata."],
      ["Fascicolo", "Referente: Soldati Marco (figlio), Rotterdam (NL). Stato: non presente."],
      ["Regia", "Spettatori connessi: 1. Località: Rotterdam. Durata collegamento: 31 minuti."],
      ["Direttrice", "«Bravo, Dario. Indice di decoro percepito: novantaquattro.»", "it"],
      ["Celebrante", "«Aldo amava le cose semplici»", "it"],
      ["Il modulo", "Il campo hobby di Aldo Soldati era vuoto, e con il campo vuoto il sistema scrive le cose semplici.", "it"],
      ["Dario", "Sembra. Il prodotto era quello. Non il funerale: il sembra.", "it"],
      ["Dario", "Il pollice era già sopra lo schermo.", "it", "hover"],
      ["Dario", "Non cliccò.", "it"]
    ];
    var body = vu.querySelector(".feed-body"), caretTimer = null;
    function typeInto(node, text, done) {
      var i = 0, c = mk("span", "caret"); node.textContent = ""; node.appendChild(document.createTextNode("")); node.appendChild(c);
      (function step() {
        if (i >= text.length) { if (c.parentNode) c.parentNode.removeChild(c); return done && done(); }
        node.firstChild.nodeValue = text.slice(0, ++i);
        caretTimer = setTimeout(step, 24 + (/[.,:;»]/.test(text.charAt(i - 1)) ? 140 : 0));
      })();
    }
    function vuAdd(i) {
      if (i >= LG.length) { return wait(4200, function () { vu.classList.remove("hover"); body.innerHTML = ""; wait(900, function () { vuAdd(0); }); }); }
      var it = LG[i], p = mk("p", "log rise" + (it[2] ? " " + it[2] : "")), k = mk("span", "k", it[0]), t = mk("span", "t");
      p.appendChild(k); p.appendChild(t); body.appendChild(p);
      while (body.children.length > 3) body.removeChild(body.firstChild);
      if (it[3] === "hover") vu.classList.add("hover");
      typeInto(t, it[1], function () { wait(i === LG.length - 2 ? 2300 : 2400, function () { vuAdd(i + 1); }); });
    }
    body.innerHTML = "";
    wait(500, function () { vuAdd(0); });
  }
})();
