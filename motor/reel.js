// Lo común de los Reels: lo que el CSS no sabe hacer, en función del instante t (segundos).
//   data-cuenta="2310" data-t="3" [data-dur="1"] [data-dec="1"] [data-antes] [data-despues]
//        una cifra que cuenta hasta su valor (formato español: 2.310; 57,5)
//   data-escribe="texto" data-t="3" [data-cps="28"]   un texto que se escribe letra a letra
//   data-clase="hecha@7.2 fuera@9"                     pone cada clase a partir de ese segundo
//   window.alTiempoReel(t)                             lo propio de cada Reel, si lo necesita
(function () {
  const fmt = (v, dec) => v.toLocaleString("es-ES", { minimumFractionDigits: dec, maximumFractionDigits: dec, useGrouping: "always" });
  const suave = (x) => 1 - Math.pow(1 - Math.min(1, Math.max(0, x)), 3);
  window.alTiempo = function (t) {
    document.querySelectorAll("[data-cuenta]").forEach((el) => {
      const fin = +el.dataset.cuenta, ini = +(el.dataset.ini || 0), d = +el.dataset.t, dur = +(el.dataset.dur || 1), dec = +(el.dataset.dec || 0);
      el.textContent = (el.dataset.antes || "") + fmt(ini + (fin - ini) * suave((t - d) / dur), dec) + (el.dataset.despues || "");
    });
    document.querySelectorAll("[data-escribe]").forEach((el) => {
      const txt = el.dataset.escribe, d = +el.dataset.t, cps = +(el.dataset.cps || 28);
      const n = Math.max(0, Math.min(txt.length, Math.floor((t - d) * cps)));
      el.textContent = txt.slice(0, n);
      el.classList.toggle("escribiendo", n > 0 && n < txt.length);
    });
    document.querySelectorAll("[data-clase]").forEach((el) => {
      for (const par of el.dataset.clase.split(/\s+/)) {
        const [c, s] = par.split("@");
        if (c) el.classList.toggle(c, t >= +s);
      }
    });
    if (window.alTiempoReel) window.alTiempoReel(t);
  };
})();
