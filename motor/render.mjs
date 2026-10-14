// ============================================================================
// Motor de vídeo de las redes de Coachera: una página HTML animada → MP4
// ============================================================================
//   node motor/render.mjs reels/r1-que-es.html salida/r1.mp4
//   node motor/render.mjs reels/r1-que-es.html salida/r1.jpg --foto 3.2      (un fotograma)
//   node motor/render.mjs reels/r1-que-es.html salida/hoja.jpg --hoja 12     (12 fotogramas en una hoja)
//
// Cada Reel es una página de 1080×1920 cuyas animaciones son CSS (@keyframes con su
// animation-delay contado desde el segundo 0) y, si hace falta, una función
// window.alTiempo(t) para lo que el CSS no sabe hacer (cifras que cuentan, texto que se
// escribe). La página declara window.REEL = { duracion, sonidos: [{ t, tipo, vol }], musica }.
//
// Para cada fotograma se pausan TODAS las animaciones y se ponen en el instante t
// (document.getAnimations()), se llama a alTiempo(t) y se hace la captura. Así el vídeo no
// depende de lo rápido que vaya la máquina: cada fotograma es exactamente su instante.
// Las capturas van por una tubería a ffmpeg (H.264, 30 fps, yuv420p) y el sonido lo
// sintetiza motor/sonido.py con los momentos de REEL.sonidos.
//
// Sin dependencias: Chrome por su protocolo de depuración (WebSocket de Node 22) y ffmpeg.

import { spawn } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = dirname(fileURLToPath(import.meta.url));
const CHROME = process.env.CHROME || "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";
const ANCHO = 1080, ALTO = 1920;

const args = process.argv.slice(2);
const pagina = resolve(args[0] || "");
const salida = resolve(args[1] || "");
const opcion = (n, d) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : d; };
const FPS = Number(opcion("--fps", 30));
const foto = opcion("--foto", null);
const hoja = opcion("--hoja", null);
const tam = (opcion("--tam", null) || "").split("x").map(Number);
const W = tam[0] || ANCHO, H = tam[1] || ALTO;
if (!existsSync(pagina) || !args[1]) {
  console.error("Uso: node motor/render.mjs <pagina.html> <salida.mp4|.jpg> [--foto t] [--hoja n] [--fps 30] [--tam 1080x1350]");
  process.exit(1);
}

// ---- Chrome por CDP -------------------------------------------------------------
async function abrirChrome() {
  const perfil = mkdtempSync(join(tmpdir(), "coachera-motor-"));
  const flags = ["--headless=new", "--remote-debugging-port=0", `--user-data-dir=${perfil}`, "--no-first-run",
    "--hide-scrollbars", "--mute-audio", "--allow-file-access-from-files", "--force-color-profile=srgb",
    "--disable-background-timer-throttling", "--disable-renderer-backgrounding", "--font-render-hinting=none", "about:blank"];
  if (process.getuid && process.getuid() === 0) flags.unshift("--no-sandbox");
  const proc = spawn(CHROME, flags, { stdio: ["ignore", "ignore", "pipe"] });
  const ws = await new Promise((ok, mal) => {
    let txt = "";
    const t = setTimeout(() => mal(new Error("Chrome no responde\n" + txt)), 20000);
    proc.stderr.on("data", (b) => { txt += b; const m = txt.match(/DevTools listening on (ws:\/\/\S+)/); if (m) { clearTimeout(t); ok(m[1]); } });
  });
  proc.stderr.resume();
  const sock = new WebSocket(ws);
  await new Promise((ok, mal) => { sock.onopen = ok; sock.onerror = mal; });
  let id = 0; const pend = new Map();
  sock.onmessage = (e) => { const m = JSON.parse(e.data); if (m.id && pend.has(m.id)) { const p = pend.get(m.id); pend.delete(m.id); m.error ? p.mal(new Error(m.error.message)) : p.ok(m.result); } };
  const enviar = (method, params = {}, sessionId) => new Promise((ok, mal) => { const i = ++id; pend.set(i, { ok, mal }); sock.send(JSON.stringify({ id: i, method, params, sessionId })); });
  const { targetId } = await enviar("Target.createTarget", { url: "about:blank" });
  const { sessionId } = await enviar("Target.attachToTarget", { targetId, flatten: true });
  const cdp = (m, p) => enviar(m, p, sessionId);
  return {
    cdp,
    async cerrar() { try { await enviar("Browser.close"); } catch {} try { sock.close(); } catch {} setTimeout(() => { try { proc.kill(); } catch {} try { rmSync(perfil, { recursive: true, force: true }); } catch {} }, 300); },
  };
}

async function evaluar(cdp, expr) {
  const r = await cdp("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true });
  if (r.exceptionDetails) throw new Error((r.exceptionDetails.exception && r.exceptionDetails.exception.description) || r.exceptionDetails.text);
  return r.result.value;
}

// Pone la página en el instante t (segundos) y espera a que esté pintada.
const IR = `async (t) => {
  for (const a of document.getAnimations()) { a.pause(); a.currentTime = t * 1000; }
  if (window.alTiempo) window.alTiempo(t);
  await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
}`;

async function capturar(cdp, t, formato = "jpeg") {
  await evaluar(cdp, `(${IR})(${t})`);
  const r = await cdp("Page.captureScreenshot", { format: formato, quality: formato === "jpeg" ? 95 : undefined, clip: { x: 0, y: 0, width: W, height: H, scale: 1 }, optimizeForSpeed: true });
  return Buffer.from(r.data, "base64");
}

const chrome = await abrirChrome();
const { cdp } = chrome;
try {
  await cdp("Page.enable");
  await cdp("Emulation.setDeviceMetricsOverride", { width: W, height: H, deviceScaleFactor: 1, mobile: false });
  await cdp("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: "no-preference" }] });
  await cdp("Page.navigate", { url: "file://" + pagina });
  await evaluar(cdp, `new Promise(r => { const ya = () => document.fonts.ready.then(() => Promise.all([...document.images].map(i => i.decode().catch(() => {})))).then(r); document.readyState === "complete" ? ya() : addEventListener("load", ya); })`);
  const REEL = await evaluar(cdp, `window.REEL || null`);
  if (!REEL || !REEL.duracion) throw new Error("La página no declara window.REEL = { duracion, ... }");

  if (foto !== null) {
    writeFileSync(salida, await capturar(cdp, Number(foto), salida.endsWith(".png") ? "png" : "jpeg"));
    console.log("foto:", salida);
  } else if (hoja !== null) {
    // n fotogramas repartidos en una hoja de 4 columnas, para revisar un Reel de un vistazo
    const n = Number(hoja), col = 4, fil = Math.ceil(n / col), w = 270, h = 480;
    const dir = mkdtempSync(join(tmpdir(), "hoja-"));
    const lista = [];
    for (let i = 0; i < n; i++) {
      const t = (REEL.duracion * (i + 0.5)) / n;
      const f = join(dir, `f${String(i).padStart(2, "0")}.jpg`);
      writeFileSync(f, await capturar(cdp, t)); lista.push(f);
    }
    await new Promise((ok, mal) => {
      const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-pattern_type", "glob", "-i", join(dir, "f*.jpg"), "-vf", `scale=${w}:${h},tile=${col}x${fil}:padding=6:color=0x222222`, "-frames:v", "1", salida]);
      ff.on("exit", c => c === 0 ? ok() : mal(new Error("ffmpeg " + c)));
    });
    rmSync(dir, { recursive: true, force: true });
    console.log("hoja:", salida);
  } else {
    const total = Math.round(REEL.duracion * FPS);
    const sinSonido = salida.replace(/\.mp4$/, ".video.mp4");
    const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(FPS), "-i", "-",
      "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-profile:v", "high", "-r", String(FPS), "-movflags", "+faststart", sinSonido],
      { stdio: ["pipe", "inherit", "inherit"] });
    const fin = new Promise((ok, mal) => ff.on("exit", c => c === 0 ? ok() : mal(new Error("ffmpeg salió con " + c))));
    const t0 = Date.now();
    for (let i = 0; i < total; i++) {
      const img = await capturar(cdp, i / FPS);
      if (!ff.stdin.write(img)) await new Promise(r => ff.stdin.once("drain", r));
      if (i % 60 === 0) process.stdout.write(`\r${i}/${total} fotogramas`);
    }
    ff.stdin.end(); await fin;
    process.stdout.write(`\r${total}/${total} fotogramas en ${((Date.now() - t0) / 1000).toFixed(0)} s\n`);
    // el sonido
    const pista = salida.replace(/\.mp4$/, ".wav");
    writeFileSync(pista + ".json", JSON.stringify(REEL));
    await new Promise((ok, mal) => { const p = spawn("python3", [join(AQUI, "sonido.py"), pista + ".json", pista], { stdio: "inherit" }); p.on("exit", c => c === 0 ? ok() : mal(new Error("sonido.py " + c))); });
    await new Promise((ok, mal) => {
      const m = spawn("ffmpeg", ["-y", "-loglevel", "error", "-i", sinSonido, "-i", pista, "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", salida], { stdio: "inherit" });
      m.on("exit", c => c === 0 ? ok() : mal(new Error("ffmpeg (mezcla) " + c)));
    });
    for (const f of [sinSonido, pista, pista + ".json"]) rmSync(f, { force: true });
    console.log("vídeo:", salida);
  }
} finally {
  await chrome.cerrar();
}
