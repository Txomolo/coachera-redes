// ============================================================================
// Muñecos de palo para los Reels animados (desde el 25-oct-2026)
// ============================================================================
// Un muñeco blanco con brillo, de frente, que se mueve por poses. Cada pose dice dónde va la
// cadera, dónde las manos (respecto al cuello) y dónde los pies (absolutos): los codos y las
// rodillas los pone una cinemática inversa de dos huesos, que los dobla hacia fuera (o hacia
// donde diga el «polo» de la pose). Así una pose se escribe con cuatro puntos y queda natural.
//
//   const m = Muneco(svgGroup, { x: 540, suelo: 1438 })
//   m.linea([[0, POSE.neutro], [0.4, POSE.panico, "muelle"], …])   // tiempos en segundos
//   window.alTiempoReel = (t) => m.en(t)
//
// Una pose: { x, y (la cadera), inc (inclinación del tronco, grados), cab (cuánto asoma la
// cabeza: 1 normal, menos = se hunde), mI, mD ([dx, dy] de cada mano desde el cuello),
// pI, pD ([x, y] de cada pie), poloI, poloD (hacia dónde se doblan los codos, desde el
// hombro), tiembla (amplitud en px) }. Lo que no se dice, sale de la pose anterior.
// Todo es función del instante t: el motor pinta cada fotograma en su segundo exacto.
(function () {
  const L = { torso: 200, cuello: 16, cabeza: 58, brazo: 120, antebrazo: 114, muslo: 152, tibia: 150 };
  const NS = "http://www.w3.org/2000/svg";
  const lerp = (a, b, k) => a + (b - a) * k;
  const CURVAS = {
    lineal: (x) => x,
    suave: (x) => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
    sale: (x) => 1 - Math.pow(1 - x, 3),
    entra: (x) => x * x * x,
    muelle: (x) => { const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); },
  };

  // dos huesos de a a c; de las dos soluciones, la del codo más cerca del polo
  function ik(a, c, l1, l2, polo) {
    let dx = c[0] - a[0], dy = c[1] - a[1], d = Math.hypot(dx, dy) || 1e-6;
    const max = l1 + l2 - .5, min = Math.abs(l1 - l2) + .5;
    if (d > max) { c = [a[0] + dx / d * max, a[1] + dy / d * max]; d = max; }
    if (d < min) d = min;
    const ang = Math.atan2(c[1] - a[1], c[0] - a[0]);
    const A = Math.acos(Math.max(-1, Math.min(1, (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d))));
    const e1 = [a[0] + Math.cos(ang + A) * l1, a[1] + Math.sin(ang + A) * l1];
    const e2 = [a[0] + Math.cos(ang - A) * l1, a[1] + Math.sin(ang - A) * l1];
    const p = [a[0] + polo[0], a[1] + polo[1]];
    const e = Math.hypot(e1[0] - p[0], e1[1] - p[1]) < Math.hypot(e2[0] - p[0], e2[1] - p[1]) ? e1 : e2;
    return [e, c];
  }

  const CAMPOS = ["x", "y", "inc", "cab", "tiembla"];
  const PARES = ["mI", "mD", "pI", "pD", "poloI", "poloD"];
  const BASE = { inc: 0, cab: 1, tiembla: 0, poloI: [-700, 120], poloD: [700, 120] };

  function mezcla(p, q, k) {
    const r = {};
    for (const c of CAMPOS) r[c] = lerp(p[c], q[c], k);
    for (const c of PARES) r[c] = [lerp(p[c][0], q[c][0], k), lerp(p[c][1], q[c][1], k)];
    return r;
  }

  window.Muneco = function (g, op) {
    op = op || {};
    const color = op.color || "#F2F6F9";
    const grosor = op.grosor || 40;
    const el = (tag, at) => { const e = document.createElementNS(NS, tag); for (const k in at) e.setAttribute(k, at[k]); g.appendChild(e); return e; };
    const trazo = { fill: "none", stroke: color, "stroke-width": grosor, "stroke-linecap": "round", "stroke-linejoin": "round" };
    const piernaI = el("path", trazo), piernaD = el("path", trazo), tronco = el("path", trazo);
    const brazoI = el("path", trazo), brazoD = el("path", trazo);
    const cabeza = el("circle", { r: L.cabeza, fill: op.cabeza || "url(#esfera)" });
    let claves = [];

    const m = {
      L,
      // [[t, pose, curva], …]; cada pose hereda lo que no dice de la anterior
      linea(lista) {
        let prev = Object.assign({}, BASE);
        claves = lista.map(([t, pose, curva]) => {
          const p = Object.assign({}, prev, pose);
          prev = p;
          return { t, p, curva: CURVAS[curva || "suave"] };
        });
        return m;
      },
      pose(t) {
        if (t <= claves[0].t) return claves[0].p;
        for (let i = 1; i < claves.length; i++) {
          const b = claves[i];
          if (t < b.t) {
            const a = claves[i - 1];
            return mezcla(a.p, b.p, b.curva((t - a.t) / (b.t - a.t)));
          }
        }
        return claves[claves.length - 1].p;
      },
      en(t) {
        const p = m.pose(t);
        const j = p.tiembla ? [Math.sin(t * 71) * p.tiembla, Math.cos(t * 59) * p.tiembla * .6] : [0, 0];
        const cadera = [p.x + j[0], p.y + j[1]];
        const a = p.inc * Math.PI / 180;
        const cuello = [cadera[0] + Math.sin(a) * L.torso, cadera[1] - Math.cos(a) * L.torso];
        const hombro = [cuello[0] - Math.sin(a) * 14, cuello[1] + Math.cos(a) * 14];
        const cab = [cuello[0] + Math.sin(a) * (L.cuello + L.cabeza) * p.cab, cuello[1] - Math.cos(a) * (L.cuello + L.cabeza) * p.cab];
        const brazo = (mano, polo) => ik(hombro, [cuello[0] + mano[0] + j[0] * .5, cuello[1] + mano[1]], L.brazo, L.antebrazo, polo);
        const pierna = (pie, polo) => ik(cadera, pie, L.muslo, L.tibia, polo);
        const d = (o, [b, c]) => `M${o[0].toFixed(1)} ${o[1].toFixed(1)}L${b[0].toFixed(1)} ${b[1].toFixed(1)}L${c[0].toFixed(1)} ${c[1].toFixed(1)}`;
        piernaI.setAttribute("d", d(cadera, pierna(p.pI, [-700, -60])));
        piernaD.setAttribute("d", d(cadera, pierna(p.pD, [700, -60])));
        tronco.setAttribute("d", `M${cadera[0].toFixed(1)} ${cadera[1].toFixed(1)}L${cuello[0].toFixed(1)} ${cuello[1].toFixed(1)}`);
        brazoI.setAttribute("d", d(hombro, brazo(p.mI, p.poloI)));
        brazoD.setAttribute("d", d(hombro, brazo(p.mD, p.poloD)));
        cabeza.setAttribute("cx", cab[0].toFixed(1));
        cabeza.setAttribute("cy", cab[1].toFixed(1));
        return { cadera, cuello, cabeza: cab };
      },
    };
    return m;
  };
  window.Muneco.CURVAS = CURVAS;
})();
