(function () {
  "use strict";
  // Trailer a richiesta: finché non si preme play non viene scaricato nulla se non l'immagine di copertina.
  // Senza JavaScript il collegamento apre direttamente il file video.
  document.querySelectorAll("[data-video]").forEach(function (box) {
    var link = box.querySelector("a.vid-play");
    var frame = box.querySelector(".vid-frame");
    if (!link || !frame) return;

    function start(e) {
      e.preventDefault();
      var v = document.createElement("video");
      v.controls = true;
      v.autoplay = true;
      v.playsInline = true;
      v.preload = "auto";
      v.poster = box.getAttribute("data-poster") || "";
      v.setAttribute("aria-label", box.getAttribute("data-label") || "Video");
      v.tabIndex = -1;
      v.addEventListener("error", function () {
        // Se il browser non riesce a riprodurlo, si torna al collegamento diretto al file.
        if (v.parentNode) v.parentNode.replaceChild(link, v);
        link.removeEventListener("click", start);
      }, { once: true });
      v.src = link.getAttribute("href");
      frame.replaceChild(v, link);
      v.focus({ preventScroll: true });
      var p = v.play();
      if (p && p.catch) p.catch(function () { /* l'utente può premere play nei controlli */ });
    }
    link.addEventListener("click", start);
  });
})();
