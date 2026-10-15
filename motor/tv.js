// Coachera TV: el reloj del partido y la estática. Se carga después de reel.js.
//   <span data-reloj="47:12"></span>   cuenta desde ese minuto al ritmo del vídeo
//   .tv-estatica feTurbulence          cambia de ruido en cada fotograma
(function () {
  const anterior = window.alTiempo;
  window.alTiempo = function (t) {
    if (anterior) anterior(t);
    document.querySelectorAll("[data-reloj]").forEach((el) => {
      const [m, s] = el.dataset.reloj.split(":").map(Number);
      const tot = m * 60 + s + Math.floor(t);
      el.textContent = String(Math.floor(tot / 60)).padStart(2, "0") + ":" + String(tot % 60).padStart(2, "0");
    });
    document.querySelectorAll(".tv-estatica feTurbulence, .hervor feTurbulence").forEach((f) => f.setAttribute("seed", String(1 + (Math.floor(t * 30) % 97))));
  };
})();
