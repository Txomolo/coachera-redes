# «Principios» en cortos de ~20 s: del guion y la voz ya partida a la página de cada Reel.
#   python3 motor/cortos.py reels/cortos-principios.json salida/voz-cortos/ [c1-cuando-y-donde …]
#     → reels/<nombre>.html (con window.REEL)
#   después: node motor/render.mjs reels/<nombre>.html salida/<nombre>.mp4
#
# La voz la parte antes motor/alinear.py (un WAV y un .tiempos.json por Reel). Los tiempos de
# cada escena salen de las marcas de las frases: gancho, contra, explica, no, regla, cierre y
# guarda. En el HTML del guion, {marca} o {marca+0.3} se cambia por ese segundo.
import html, json, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from principios import C

GUARDAR = '<svg viewBox="0 0 24 24"><path d="M6 3h12v18l-6-4.5L6 21z"/></svg>'

def s(x): return f"{x:.2f}s"

def resolver(txt, M, F=None):
    """{marca}, {marca+0.3} y {marca@unas palabras±n}: el segundo en que se dicen esas palabras
    dentro de la frase de esa marca (a velocidad media de la frase: basta para ir al compás)."""
    def f(m):
        nombre, frase, signo, n = m.group(1), m.group(2), m.group(3), m.group(4)
        if nombre not in M: raise KeyError(f"marca «{nombre}» sin frase en la voz")
        v = M[nombre]
        if frase:
            l = F[nombre]; k = l["texto"].lower().find(frase.lower())
            if k < 0: raise KeyError(f"«{frase}» no está en la frase «{l['texto']}»")
            v = l["t"] + (l["fin"] - l["t"]) * k / max(1, len(l["texto"]))
        v += (float(n) if signo == "+" else -float(n) if signo == "-" else 0)
        return f"{v:.2f}"
    return re.sub(r"\{([a-z]+)(?:@([^}+\-]+?))?(?:([+-])([\d.]+))?\}", f, txt)

def cuando_cifra(h, defecto):
    """Una cifra que cuenta no se enseña antes de empezar a contar (un «0 %» confunde)."""
    m = re.search(r"data-t='([\d.]+)'", h)
    return float(m.group(1)) - .1 if m else defecto

def pagina(serie, r, tiempos, wav):
    M, F = {}, {}
    for f in tiempos:
        if f.get("marca") and f["marca"] not in M: M[f["marca"]] = f["t"]; F[f["marca"]] = f
    fin = round(tiempos[-1]["fin"] + 0.9, 2); M["fin"] = fin
    E, C_, R = M["explica"], M["cierre"], M["regla"]
    no = M.get("no", R)
    ph = lambda t: resolver(t, M, F)
    lado = lambda c, cl, d, extra: f'''<div class="tarjeta-p {cl} entra" style="--d:{s(d)};{extra}" data-clase="{ 'acento-mal@' + f'{no:.2f}' if cl == 'mal' else 'acento-bien@' + f'{R:.2f}' }"><span class="chip-p">{html.escape(c["chip"])}</span>
        <div class="pantalla-p">{ph(c["pantalla"])}</div><div class="cifra-p funde" style="--d:{s(cuando_cifra(ph(c["cifra"]), d + .35))}">{ph(c["cifra"])}</div></div>'''
    tb = float(ph(r["bien"]["entra"])) if r["bien"].get("entra") else E + .25
    cab = f'PRINCIPIO {r["numero"]:02d} <b>/</b> 05 <b>—</b> {html.escape(r["etiqueta"].upper())}'
    g = r["cierre"]
    escenas = f'''
  <section class="escena primera" style="--a:0s;--b:{s(E)}">
    <p class="etiqueta">{cab}</p>
    {ph(r["gancho"])}
  </section>
  <section class="escena corto" style="--a:{s(E)};--b:{s(C_)}"><div class="golpe">
    <p class="etiqueta">{cab}</p>
    <h2 class="titular-p">{r["titular"]}</h2>
    <div class="pareja">{lado(r["mal"], "mal", E + .1, f"--tm:{s(no)}")}{lado(r["bien"], "bien", tb, f"--tb:{s(R)}")}<span class="vs funde" style="--d:{s(tb + .1)}">vs</span></div>
    <p class="cita funde" style="--d:{s(E + .5)}">{html.escape(r["cita"])}</p>
    <div class="regla entra" style="--d:{s(R)}"><div><small>REGLA</small>{html.escape(r["regla"])}</div></div>
  </div></section>
  <section class="escena" style="--a:{s(C_)};--b:999s"><div class="golpe">
    <p class="c-antes funde" style="--d:{s(C_ + .05)}">{html.escape(g["antes"])}</p>
    <h2 class="c-texto entra" style="--d:{s(C_ + .15)}">{g["texto"]}</h2>
    <div class="c-logo entra" style="--d:{s(C_ + .45)}"><span class="logo-p" style="--d:{s(C_ + .55)}">{C}<span class="txt">oachera</span></span></div>
    <div class="c-guarda entra" style="--d:{s(M.get('guarda', C_ + 1.2))}"><div class="late" style="--d2:{s(M.get('guarda', C_ + 1.2) + .5)}">{GUARDAR}Guárdalo</div></div>
  </div></section>
  <span class="corte" style="--d:{s(E - .2)}"></span><span class="corte" style="--d:{s(C_ - .2)}"></span>'''
    sonidos = [{"t": 0.02, "tipo": "golpe", "vol": .35},
               {"t": round(M["gancho"] + 1.15, 2), "tipo": "pop", "vol": .3}]
    if "contra" in M: sonidos.append({"t": round(M["contra"], 2), "tipo": "toque", "vol": .35})
    sonidos += [{"t": round(E - .2, 2), "tipo": "barrido", "vol": .4},
                {"t": round(E + .1, 2), "tipo": "toque", "vol": .28}, {"t": round(tb, 2), "tipo": "toque", "vol": .3},
                {"t": round(E + 1.5, 2), "tipo": "pop", "vol": .3},
                {"t": round(no, 2), "tipo": "toque", "vol": .3},
                {"t": round(R + .05, 2), "tipo": "ok", "vol": .45},
                {"t": round(C_ - .2, 2), "tipo": "barrido", "vol": .4},
                {"t": round(C_ + .55, 2), "tipo": "marca", "vol": .6}]
    if "guarda" in M: sonidos.append({"t": round(M["guarda"] + .05, 2), "tipo": "pop", "vol": .4})
    reel = {"duracion": fin, "musica": serie.get("musica", {"estilo": "pulso", "vol": .28}), "sonidos": sonidos, "voz": os.path.abspath(wav), "vol_voz": 1.7}
    return f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<title>{html.escape(r["etiqueta"])} · corto {r["numero"]}</title>
<link rel="stylesheet" href="../motor/fuentes.css">
<link rel="stylesheet" href="../motor/reel.css">
<link rel="stylesheet" href="../motor/principios.css">
<link rel="stylesheet" href="../motor/cortos.css">
<!-- Generado por motor/cortos.py desde {serie["serie"]}.json: no se edita a mano. -->
</head>
<body><div id="escena">
  <div class="fondo-p"></div>
  <div class="barra-c" style="--dur:{s(fin)}"><b></b></div>
  {escenas}
</div>
<script src="../motor/reel.js"></script>
<script>
window.REEL = {json.dumps(reel, ensure_ascii=False)};
</script>
</body></html>
'''

if __name__ == "__main__":
    ruta, carpeta = sys.argv[1], sys.argv[2]
    solo = set(sys.argv[3:])
    serie = json.load(open(ruta, encoding="utf-8"))
    raiz = os.path.dirname(AQUI)
    for r in serie["reels"]:
        if solo and r["nombre"] not in solo: continue
        if "gancho" not in r: print(f"{r['nombre']}: sin diseño todavía, se salta"); continue
        tiempos = json.load(open(os.path.join(carpeta, r["nombre"] + ".tiempos.json"), encoding="utf-8"))
        wav = os.path.join(carpeta, r["nombre"] + ".wav")
        out = os.path.join(raiz, "reels", r["nombre"] + ".html")
        open(out, "w", encoding="utf-8").write(pagina(serie, r, tiempos, wav))
        print(f"{r['nombre']}: {out} ({tiempos[-1]['fin'] + 0.9:.1f} s)")
