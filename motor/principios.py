# «Principios, demostrados en pantalla»: de un guion en JSON a la voz y a la página del reel.
#   python3 motor/principios.py reels/p1-cinco-principios.json
#     → salida/<nombre>-voz.wav (la voz montada) y reels/<nombre>.html (con window.REEL)
#   después: node motor/render.mjs reels/<nombre>.html salida/<nombre>.mp4
#
# Los tiempos salen de la voz: cada línea se dice, se mide y la siguiente empieza detrás. Cada
# bloque (portada, principios, cierre) marca cuándo empieza su «titulo», su «explica» y su
# «regla», y la página aparece al ritmo de lo que se va diciendo. En el HTML de las pantallas
# se pueden usar {a} (empieza el bloque), {e} y {e5} (empieza la explicación, y medio segundo
# después), {r} (la regla), {celdas21} y {celdas66}.
import html, json, os, sys, wave
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from voz import motor_tts, decir, recortar_silencio, pulir, SR

ENTRE_LINEAS, ENTRE_BLOQUES, ANTES = 0.28, 0.55, 0.4
C = '<svg viewBox="8 24 85 66"><path pathLength="1" d="M60.93,69.45 A23.5,23.5 0 1 1 41.00,33.50 L83.50,33.50"/></svg>'

def s(x): return f"{x:.2f}s"

def celdas(n, si, no=(), hoy=None):
    out = []
    for k in range(n):
        c = "si" if k < si and k not in no else ("no" if k in no else "")
        if hoy is not None and k == hoy: c += " hoy"
        out.append(f"<i class='{c.strip()}'></i>")
    return "".join(out)

def montar_voz(guion, tts, hablante, vel):
    bloques = [guion["intro"]] + guion["principios"] + [guion["cierre"]]
    t = ANTES; trozos = []
    for b in bloques:
        b["_a"] = t; b["_m"] = {}
        for l in b["voz"]:
            x = recortar_silencio(decir(tts, l["texto"], hablante, vel))
            b["_m"].setdefault(l["marca"], t)
            trozos.append((t, x)); t += len(x) / SR + ENTRE_LINEAS
            print(f"  {b['_m'][l['marca']]:6.2f}  {l['texto'][:70]}")
        b["_b"] = t - ENTRE_LINEAS + ENTRE_BLOQUES
        t = b["_b"]
    dur = t + 1.6
    pista = np.zeros(int(dur * SR))
    for t0, x in trozos:
        k = int(t0 * SR); pista[k:k + len(x)] += x[: len(pista) - k]
    return pulir(pista), dur

def ph(txt, b):
    m = b["_m"]; e = m.get("explica", b["_a"]); r = m.get("regla", e)
    return (txt.replace("{a}", f"{b['_a']:.2f}").replace("{e5}", f"{e + .5:.2f}").replace("{e}", f"{e:.2f}").replace("{r}", f"{r:.2f}")
               .replace("{celdas21}", celdas(21, 21))
               .replace("{celdas66}", celdas(66, 30, no=(9, 22), hoy=29)))

def escena_intro(b):
    a = b["_a"]; e = b["_m"].get("explica", a + 1)
    filas = "".join(f'<div class="fila entra" style="--d:{s(a + .5 + k * .14)}"><b>{n}</b>{html.escape(t)}<i>{y}</i></div>'
                    for k, (n, t, y) in enumerate(b["indice"]))
    return f'''<section class="escena" style="--a:0s;--b:{s(b['_b'])}">
    <h1 class="gran" style="top:400px;font-size:100px">{b["titular"]}</h1>
    <p class="funde" style="--d:{s(e)};position:absolute;left:70px;right:70px;top:760px;margin:0;font-family:var(--mono);font-size:32px;color:var(--gris)">{html.escape(b["sub"])}</p>
    <div class="indice" style="top:850px">{filas}</div>
  </section>'''

def escena_principio(b, k, total):
    a, bb = b["_a"], b["_b"]; m = b["_m"]; e = m.get("explica", a + 1.5); r = m.get("regla", e + 3)
    lado = lambda c, cl, d: f'''<div class="tarjeta-p {cl} entra" style="--d:{s(d)}"><span class="chip-p">{html.escape(c["chip"])}</span>
        <div class="pantalla-p">{ph(c["pantalla"], b)}</div><div class="cifra-p funde" style="--d:{s(e + .35)}">{ph(c["cifra"], b)}</div></div>'''
    p1, p2 = b["porque"]
    return f'''<section class="escena" style="--a:{s(a)};--b:{s(bb)}">
    <p class="etiqueta funde" style="--d:{s(a)}">PRINCIPIO {k + 1:02d} <b>—</b> {html.escape(b["etiqueta"].upper())}</p>
    <h2 class="titular-p entra" style="--d:{s(a + .05)}">{b["titular"]}</h2>
    <div class="pareja">{lado(b["mal"], "mal", a + .3)}{lado(b["bien"], "bien", a + .5)}<span class="vs funde" style="--d:{s(a + .6)}">vs</span></div>
    <p class="cita funde" style="--d:{s(e + .2)}">{html.escape(b["cita"])}</p>
    <div class="porque"><p class="r funde" style="--d:{s(e + 1.0)}">POR QUÉ FUNCIONA</p><p class="entra" style="--d:{s(e + 1.1)}">{html.escape(p1)}</p><p class="entra" style="--d:{s(e + 1.5)}">{html.escape(p2)}</p></div>
    <div class="regla entra" style="--d:{s(r)}"><div><small>REGLA</small>{html.escape(b["regla"])}</div></div>
  </section>'''

def escena_cierre(b):
    a = b["_a"]
    filas = "".join(f'<div class="fila entra" data-clase="hecha@{a + .9 + k * .5:.2f}" style="--d:{s(a + .3 + k * .12)}"><b>{n}</b>{html.escape(t)}<i>✓ {h}</i></div>'
                    for k, (n, t, h) in enumerate(b["indice"]))
    e = b["_m"].get("explica", a + 4)
    return f'''<section class="escena" style="--a:{s(a)};--b:999s">
    <h2 class="gran entra" style="--d:{s(a)};top:330px;font-size:90px">{b["titular"]}</h2>
    <div class="indice" style="top:560px">{filas}</div>
    <div class="entra" style="--d:{s(a + 3.4)};position:absolute;left:0;right:0;top:1150px;text-align:center"><span class="logo-p" style="--d:{s(a + 3.5)}">{C}<span class="txt">oachera</span></span></div>
    <div class="entra" style="--d:{s(a + 3.9)};position:absolute;left:0;right:0;top:1316px;text-align:center"><span class="boton-p">{html.escape(b["boton"])}</span></div>
    <p class="firma funde" style="--d:{s(e)};top:1452px">{html.escape(b["firma"])}</p>
  </section>'''

def pagina(g, dur, voz_wav):
    ps = g["principios"]; a0, b0 = ps[0]["_a"], ps[-1]["_b"]
    tramos = "".join(f'<i><b style="--ta:{s(p["_a"])};--tb:{s(p["_b"] - p["_a"])}"></b></i>' for p in ps)
    escenas = [escena_intro(g["intro"])] + [escena_principio(p, k, len(ps)) for k, p in enumerate(ps)] + [escena_cierre(g["cierre"])]
    sonidos = []
    for k, (n, t, y) in enumerate(g["intro"]["indice"]): sonidos.append({"t": round(g["intro"]["_a"] + .5 + k * .14, 2), "tipo": "toque", "vol": .25})
    for p in ps:
        a, m = p["_a"], p["_m"]
        sonidos += [{"t": round(a, 2), "tipo": "barrido", "vol": .35}, {"t": round(a + .3, 2), "tipo": "toque", "vol": .3}, {"t": round(a + .5, 2), "tipo": "toque", "vol": .3},
                    {"t": round(m.get("explica", a) + .5, 2), "tipo": "pop", "vol": .35}, {"t": round(m.get("regla", a) + .05, 2), "tipo": "ok", "vol": .45}]
    c = g["cierre"]
    sonidos += [{"t": round(c["_a"], 2), "tipo": "barrido", "vol": .45}] + [{"t": round(c["_a"] + .9 + k * .5, 2), "tipo": "toque", "vol": .3} for k in range(5)]
    sonidos += [{"t": round(c["_a"] + 3.5, 2), "tipo": "marca", "vol": .7}]
    reel = {"duracion": round(dur, 2), "musica": g.get("musica", {"estilo": "pulso", "vol": .3}), "sonidos": sonidos, "voz": voz_wav, "vol_voz": 1.7}
    return f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<title>{html.escape(g["titulo"])}</title>
<link rel="stylesheet" href="../motor/fuentes.css">
<link rel="stylesheet" href="../motor/reel.css">
<link rel="stylesheet" href="../motor/principios.css">
<!-- Generado por motor/principios.py desde {g["nombre"]}.json: no se edita a mano. -->
</head>
<body><div id="escena">
  <div class="fondo-p"></div>
  <div class="progreso" style="--a:{s(a0)};--b:{s(b0)}">{tramos}</div>
  {"".join(escenas)}
  <p class="firma" style="top:1600px;opacity:.0">coachera.fit</p>
</div>
<script src="../motor/reel.js"></script>
<script>
window.REEL = {json.dumps(reel, ensure_ascii=False)};
</script>
</body></html>
'''

if __name__ == "__main__":
    ruta = sys.argv[1]
    g = json.load(open(ruta, encoding="utf-8"))
    v = g["voz"]
    tts = motor_tts(v["modelo"])
    voz, dur = montar_voz(g, tts, int(v.get("hablante", 0)), float(v.get("velocidad", 1.0)))
    raiz = os.path.dirname(AQUI)
    wav = os.path.join(raiz, "salida", g["nombre"] + "-voz.wav")
    os.makedirs(os.path.dirname(wav), exist_ok=True)
    with wave.open(wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((voz * 32767).astype("<i2").tobytes())
    out = os.path.join(raiz, "reels", g["nombre"] + ".html")
    open(out, "w", encoding="utf-8").write(pagina(g, dur, wav))
    print(f"voz: {wav}\npágina: {out}\nduración: {dur:.1f} s")
