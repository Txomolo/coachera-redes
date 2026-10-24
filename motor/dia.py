# «Un día de entrenador» en Reels de ~18 s: del guion y la voz ya partida a la página.
#   python3 motor/dia.py reels/dia-entrenador.json salida/voz-dia/ [d1-… …]
#     → reels/<nombre>.html (con window.REEL)
#   después: node motor/render.mjs reels/<nombre>.html salida/<nombre>.mp4
#   con --estimar, sin voz: los segundos de cada frase salen de su longitud (para ver el diseño)
#
# Marcas de la voz: gancho, lio, con, remate y cierre. Escenas: el lío (de 0 a «con»), la app
# (de «con» a «cierre»: el móvil entra, se acerca y en «remate» entra la segunda pantalla) y
# el cierre. En el HTML del diseño, {marca}, {marca+0.3} y {marca@unas palabras} como en cortos.
import html, json, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
from principios import C
from cortos import resolver, s
from PIL import Image

P = "../salida/pantallas-dest"
BARRA = 50

def movil(img, desde, ancho=760, clase="", d=0.0, zoom=None, foco=None):
    k = (ancho - 32) / 375
    url = f"{P}/{img}.png"
    ruta = os.path.join(RAIZ, "salida", "pantallas-dest", img + ".png")
    alto = Image.open(ruta).size[1] / 3
    fondo = Image.open(ruta).convert("RGB").getpixel((20, 20))
    color = "#0B0F14" if sum(fondo) / 3 > 140 else "#FFFFFF"
    estado = f'<div class="estado" style="background:rgb{fondo};color:{color}"><b>9:41</b><i></i></div>'
    if img.startswith("t-"):
        capas = (f'<div style="height:{BARRA * k:.1f}px;background-image:url({url})"></div>'
                 f'<div style="height:{alto * k:.0f}px;background-image:url({url});background-position:0 {-(BARRA + desde) * k:.1f}px"></div>')
    else:
        capas = f'<div style="height:{(alto - desde) * k:.0f}px;background-image:url({url});background-position:0 {-desde * k:.1f}px"></div>'
    z = ""
    if zoom:
        z = f' class="d-zoom" style="--z:{zoom["z"]};--ox:{zoom["x"]}%;--oy:{(zoom["y"] - desde) * k:.0f}px;--tz:{s(zoom["t"])}"'
    f = ""
    if foco:
        fx, fy, fw, fh, ft = foco
        f = f'<i class="d-foco" style="left:{fx * k:.0f}px;top:{(fy - desde) * k:.0f}px;width:{fw * k:.0f}px;height:{fh * k:.0f}px;--d:{s(ft)}"></i>'
    return (f'<div class="d-movil {clase}" style="--k:{k:.3f};--d:{s(d)}"><div class="d-pantalla">{estado}'
            f'<div{z}><div style="position:relative">{capas}{f}</div></div></div></div>')

def tiempos_estimados(r):
    t, out = 0.12, []
    for l in r["voz"]:
        dur = max(0.6, len(l["texto"]) / 15.5)
        out.append({"texto": l["texto"], "marca": l["marca"], "t": round(t, 2), "fin": round(t + dur, 2)})
        t += dur + 0.45
    return out

def pagina(serie, r, tiempos, wav=None):
    M, F = {}, {}
    for i, f in enumerate(tiempos):
        M[f"L{i}"] = f["t"]; F[f"L{i}"] = f
        if f.get("marca") and f["marca"] not in M: M[f["marca"]] = f["t"]; F[f["marca"]] = f
    fin = round(tiempos[-1]["fin"] + 1.0, 2); M["fin"] = fin
    CON, REM, CIE = M["con"], M["remate"], M["cierre"]
    ph = lambda t: resolver(t, M, F)
    num = lambda t: float(ph(t))
    cab = f'UN DÍA DE ENTRENADOR <b>—</b> {html.escape(r["cuando"])}'
    a = r["app"]
    p1 = movil(a["img"], a.get("desde", 0), d=CON + .15,
               zoom={**a["zoom"], "t": num(a["zoom"]["t"])} if a.get("zoom") else None,
               foco=(*a["foco"][:4], num(a["foco"][4])) if a.get("foco") else None)
    p2 = ""
    if a.get("img2"):
        p2 = movil(a["img2"], a.get("desde2", 0), clase="segundo", d=REM - .1,
                   foco=(*a["foco2"][:4], num(a["foco2"][4])) if a.get("foco2") else None)
    escenas = f'''
  <section class="escena primera" style="--a:0s;--b:{s(CON)}">
    <p class="etiqueta">{cab}</p>
    {ph(r["lio"])}
  </section>
  <section class="escena" style="--a:{s(CON)};--b:{s(CIE)}"><div class="golpe" style="--a:{s(CON)}">
    <p class="etiqueta">CON COACHERA</p>
    <h2 class="d-titular sale" style="--f:{s(REM - .1)}">{a["titulo"]}</h2>
    <h2 class="d-titular entra2" style="--d:{s(REM)}">{a["remate"]}</h2>
    {p1}{p2}
  </div></section>
  <section class="escena" style="--a:{s(CIE)};--b:999s"><div class="golpe" style="--a:{s(CIE)}">
    <div class="c-logo entra" style="--d:{s(CIE + .1)};top:820px"><span class="logo-p" style="--d:{s(CIE + .2)}">{C}<span class="txt">oachera</span></span></div>
    <div class="d-cta entra" style="--d:{s(num("{cierre@gratis}"))}"><div>{html.escape(serie.get("oferta", "14 días gratis"))}</div><span>coachera.fit · enlace en la bio</span></div>
  </div></section>
  <span class="corte" style="--d:{s(CON - .2)}"></span><span class="corte" style="--d:{s(CIE - .2)}"></span>'''
    sonidos = [{"t": 0.02, "tipo": "golpe", "vol": .35}]
    sonidos += [{"t": round(num(x), 2), "tipo": "pop", "vol": .28} for x in r.get("pops", [])]
    sonidos += [{"t": round(CON - .2, 2), "tipo": "barrido", "vol": .4}, {"t": round(CON + .2, 2), "tipo": "toque", "vol": .3},
                {"t": round(REM, 2), "tipo": "ok", "vol": .45}, {"t": round(CIE - .2, 2), "tipo": "barrido", "vol": .4},
                {"t": round(CIE + .3, 2), "tipo": "marca", "vol": .6}]
    reel = {"duracion": fin, "musica": serie.get("musica", {"estilo": "pulso", "vol": .28}), "sonidos": sonidos}
    if wav: reel.update(voz=os.path.abspath(wav), vol_voz=1.7)
    return f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<title>{html.escape(r["etiqueta"])} · un día de entrenador {r["numero"]}</title>
<link rel="stylesheet" href="../motor/fuentes.css">
<link rel="stylesheet" href="../motor/reel.css">
<link rel="stylesheet" href="../motor/principios.css">
<link rel="stylesheet" href="../motor/cortos.css">
<link rel="stylesheet" href="../motor/dia.css">
<!-- Generado por motor/dia.py desde {serie["serie"]}.json: no se edita a mano. -->
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
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    estimar = "--estimar" in sys.argv
    ruta, carpeta = args[0], args[1]
    solo = set(args[2:])
    serie = json.load(open(ruta, encoding="utf-8"))
    for r in serie["reels"]:
        if solo and r["nombre"] not in solo: continue
        if "lio" not in r: print(f"{r['nombre']}: sin diseño todavía, se salta"); continue
        if estimar: tiempos, wav = tiempos_estimados(r), None
        else:
            tiempos = json.load(open(os.path.join(carpeta, r["nombre"] + ".tiempos.json"), encoding="utf-8"))
            wav = os.path.join(carpeta, r["nombre"] + ".wav")
        out = os.path.join(RAIZ, "reels", r["nombre"] + ".html")
        open(out, "w", encoding="utf-8").write(pagina(serie, r, tiempos, wav))
        print(f"{r['nombre']}: {out} ({tiempos[-1]['fin'] + 1.0:.1f} s)")
