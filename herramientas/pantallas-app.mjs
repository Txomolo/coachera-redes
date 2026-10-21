// Pantallas reales de la app (con los datos de ejemplo de sus escenas) en alta resolución,
// para las historias y los carruseles.
//   node herramientas/pantallas-app.mjs herramientas/pantallas.json salida/pantallas/
//
// Usa la herramienta de capturas de la propia app (coachera-app/scripts/capturas): la app se
// sirve en local, la escena cambia SB.db por datos inventados y nada sale a Supabase. Aquí solo
// se añade la escala: la página se maqueta al ancho del móvil (375) y se captura a 3×, como
// la pantalla de un teléfono de verdad.
// Cada entrada: { nombre, escena: "cliente" | "entrenador", datos: {…}, ancho, alto, escala,
//                 antes: "código JS que se ejecuta en la página antes de capturar" }
import { readFileSync, mkdirSync, writeFileSync } from "node:fs";
import { join, resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = dirname(fileURLToPath(import.meta.url));
const APP = resolve(process.env.COACHERA_APP || join(AQUI, "..", "..", "coachera-app"));
const { servidorLocal, abrirChrome, esperar } = await import(join(APP, "scripts", "capturas", "chrome.mjs"));

const [lista, carpeta] = process.argv.slice(2);
if (!lista || !carpeta) { console.error("Uso: node herramientas/pantallas-app.mjs <lista.json> <carpeta>"); process.exit(1); }
const tomas = JSON.parse(readFileSync(lista, "utf8"));
const solo = process.argv.slice(4);
mkdirSync(carpeta, { recursive: true });

const servidor = await servidorLocal();
const navegador = await abrirChrome();
let fallos = 0;
try {
  for (const t of tomas) {
    if (solo.length && !solo.includes(t.nombre)) continue;
    const ancho = t.ancho || 375, alto = t.alto || 812, movil = t.movil ?? ancho < 600, escala = t.escala || 3;
    const p = await navegador.nuevaPagina({ ancho, alto, movil, oscuro: !!t.oscuro, bloquear: url => /supabase\.co/i.test(url) });
    try {
      await p.ir(`${servidor.base}/app.html`);
      await p.cargarEscena(t.escena, t.datos || {});
      if (t.antes) { await p.evaluar(`(async () => { ${t.antes} })()`); }
      await p.evaluar("document.fonts ? document.fonts.ready.then(() => true) : true");
      await esperar(t.espera || 700);
      await p.cdp("Emulation.setDeviceMetricsOverride", { width: ancho, height: alto, deviceScaleFactor: escala, mobile: movil });
      await esperar(400);
      const salida = join(carpeta, `${t.nombre}.png`);
      writeFileSync(salida, await p.captura());
      console.log("✓", t.nombre);
      for (const e of p.errores) console.error("   aviso, error en la página:", e.slice(0, 300));
    } catch (err) {
      fallos++; console.error("✕", t.nombre, String(err.message || err).slice(0, 400));
    } finally {
      try { await p.cerrar?.(); } catch {}
    }
  }
} finally {
  await navegador.cerrar(); await servidor.cerrar();
}
process.exit(fallos ? 1 : 0);
