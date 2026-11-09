# Lote 6 de @coachera.app: viernes 20 de noviembre (4 imágenes de 1080 x 1350).
# Uso: python3 herramientas/lote-06.py [prefijo]   (sin prefijo, todas). Ver herramientas/README.md
import os, sys, subprocess, html
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.abspath(os.path.join(AQUI, "..", "recursos"))          # capturas de la app y el icono
SALIDA = os.environ.get("SALIDA", "/tmp/coachera-redes-salida")      # aquí quedan los PNG
HTML = os.path.join(SALIDA, "html"); PNG = os.path.join(SALIDA, "png")
os.makedirs(HTML, exist_ok=True); os.makedirs(PNG, exist_ok=True)
CHROME = os.environ.get("CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
LOGO = f"file://{CAP}/../marca/logo/icono-1024.png"   # la C que avanza, en turquesa (desde el 17/10)
def cap(n): return f"file://{CAP}/{n}"

CSS = """
:root{--bg:#06080B;--sf:#0E131A;--sf2:#131A23;--line:rgba(255,255,255,.08);--line2:rgba(255,255,255,.16);
--text:#E8EDF3;--strong:#FFFFFF;--muted:#9AA6B8;--brand:#14B8A6;--brandtext:#5EEAD4;--onbrand:#06231F}
*{box-sizing:border-box}
html,body{margin:0;background:var(--bg)}
.s{width:1080px;height:1350px;position:relative;overflow:hidden;background:var(--bg);color:var(--text);
 font-family:'IBM Plex Sans',sans-serif;padding:104px 88px 0;-webkit-font-smoothing:antialiased}
.s.t{background:var(--brand);color:var(--onbrand)}
.kicker{font-family:'IBM Plex Mono',monospace;font-weight:500;font-size:26px;letter-spacing:.1em;text-transform:uppercase;color:var(--brandtext);margin-bottom:34px}
.t .kicker{color:rgba(6,35,31,.72)}
h1{font-weight:600;font-size:96px;line-height:1.02;letter-spacing:-.03em;margin:0;color:var(--strong)}
h2{font-weight:600;font-size:68px;line-height:1.07;letter-spacing:-.025em;margin:0;color:var(--strong)}
.t h1,.t h2{color:var(--onbrand)}
.lead{font-size:38px;line-height:1.35;color:var(--muted);margin-top:30px;font-weight:400}
.t .lead{color:rgba(6,35,31,.82)}
.acento{color:var(--brandtext)}
.pie{position:absolute;left:88px;right:88px;bottom:70px;display:flex;align-items:center;justify-content:space-between}
.marca{display:flex;align-items:center;gap:16px;font-size:28px;color:var(--muted);font-weight:500}
.marca img{width:52px;height:52px;border-radius:12px;display:block}
.t .marca{color:rgba(6,35,31,.78)} .t .marca img{box-shadow:0 0 0 2px rgba(6,35,31,.55)}
.cont{font-family:'IBM Plex Mono',monospace;font-size:26px;color:var(--muted);display:flex;align-items:center;gap:14px}
.t .cont{color:rgba(6,35,31,.72)}
.desliza{font-size:44px;line-height:1}
.btn{display:inline-flex;align-items:center;gap:16px;background:var(--brand);color:var(--onbrand);font-weight:600;font-size:38px;
 padding:28px 44px;border-radius:999px;border:1.5px solid var(--brandtext)}
.t .btn{background:var(--onbrand);color:#fff;border-color:var(--onbrand)}
.chips{display:flex;flex-wrap:wrap;gap:16px;margin-top:56px}
.chip{border:1.5px solid var(--line2);border-radius:999px;padding:16px 30px;font-size:32px;font-weight:500;color:var(--text)}
.t .chip{border-color:rgba(6,35,31,.5);color:var(--onbrand)}
.nota{font-size:30px;color:var(--muted);margin-top:26px}
.t .nota{color:rgba(6,35,31,.78)}
.cifra{font-family:'IBM Plex Mono',monospace;font-weight:500;font-size:300px;line-height:.9;letter-spacing:-.05em;color:var(--strong)}
.tel{position:absolute;background:#000;border-radius:66px;padding:14px;border:1.5px solid var(--line2)}
.tel img{display:block;width:100%;border-radius:52px}
.win{background:var(--sf);border:1.5px solid var(--line2);border-radius:20px;overflow:hidden}
.win .barra{height:40px;display:flex;align-items:center;gap:10px;padding:0 18px;border-bottom:1px solid var(--line)}
.win .barra i{width:12px;height:12px;border-radius:50%;background:#2A3442;display:block}
.win img{display:block;width:100%}
.filas{margin-top:64px;display:flex;flex-direction:column;gap:0}
.fila{display:flex;align-items:center;gap:28px;padding:30px 0;border-top:1.5px solid var(--line);font-size:38px;color:var(--text)}
.fila:last-child{border-bottom:1.5px solid var(--line)}
.fila svg{width:46px;height:46px;flex:none;stroke:var(--brandtext);fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.card{background:var(--sf);border:1.5px solid var(--line2);border-radius:16px}
.mono{font-family:'IBM Plex Mono',monospace}
"""

ICON = {
 "fuga": '<svg viewBox="0 0 24 24"><circle cx="9" cy="8" r="4"/><path d="M2 21c0-3.9 3.1-7 7-7s7 3.1 7 7"/><path d="M17 8l5 5M22 8l-5 5"/></svg>',
 "memoria": '<svg viewBox="0 0 24 24"><path d="M7 7h13l-4-4M17 17H4l4 4"/></svg>',
 "pdf": '<svg viewBox="0 0 24 24"><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6"/></svg>',
 "cobro": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M15 9.5c-.5-1-1.6-1.5-3-1.5-1.7 0-3 .9-3 2s1.3 1.7 3 2 3 .9 3 2-1.3 2-3 2c-1.4 0-2.5-.5-3-1.5M12 6v2M12 16v2"/></svg>',
}

def pie(n=None, total=None, flecha=False):
    cont = ""
    if n:
        cont = f'<div class="cont">{n}/{total}' + ('<span class="desliza">→</span>' if flecha else '') + '</div>'
    return f'<div class="pie"><div class="marca"><img src="{LOGO}">coachera.fit</div>{cont}</div>'

def slide(body, turquesa=False, n=None, total=None, flecha=False):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="s{" t" if turquesa else ""}">{body}{pie(n,total,flecha)}</div></body></html>'

def tel(src, left, top, width):
    return f'<div class="tel" style="left:{left}px;top:{top}px;width:{width}px"><img src="{cap(src)}"></div>'

def win(src, extra=""):
    return f'<div class="win" style="{extra}"><div class="barra"><i></i><i></i><i></i></div><img src="{cap(src)}"></div>'

E = html.escape
S = {}
# ---------- P1 · Tu página para la bio de Instagram (viernes 20, carrusel de 4) ----------
S["p1-1"] = slide('<div class="kicker">Tu página</div>'
  '<h1 style="font-size:100px;margin-top:130px">El enlace de tu bio, con tus preguntas de filtro.</h1>'
  '<div class="lead" style="font-size:44px;margin-top:44px">Quien quiere entrenar contigo te contesta antes de que le escribas.</div>', True, 1, 4, True)
S["p1-2"] = slide('<div class="kicker">coachera.fit/con/tu-nombre</div><h2>Tu marca, para quién es y cómo trabajas.</h2>'
  + tel("pagina-arriba.png", 360, 430, 360), False, 2, 4)
S["p1-3"] = slide('<div class="kicker">Lo que rellena</div><h2>Tus preguntas. Sin precios: eso lo habláis después.</h2>'
  + tel("pagina-formulario.png", 360, 430, 360), False, 3, 4)
pasos = "".join(f'''<div style="display:flex;gap:36px;padding:36px 0;border-top:1.5px solid var(--line)">
 <div class="mono acento" style="font-size:60px;font-weight:500;line-height:1">{n}</div>
 <div style="font-size:40px;line-height:1.3;color:var(--text)">{t}</div></div>''' for n, t in [
  ("01", "Te llega a Clientes → Solicitudes, a tu lista de hoy y al móvil."),
  ("02", "Le escribes por WhatsApp con un toque, con el mensaje ya empezado."),
  ("03", "Si encajáis, «Aceptar e invitar» y ya es tu cliente.")])
S["p1-4"] = slide('<h2 style="margin-top:70px">De la bio a cliente, sin perder a nadie en un chat.</h2>'
  '<div style="margin-top:44px;border-bottom:1.5px solid var(--line)">' + pasos + '</div>'
  '<div style="margin-top:56px"><span class="btn">Empieza gratis en coachera.fit</span></div>'
  '<div class="nota">Gratis hasta 5 clientes · Sin tarjeta</div>', False, 4, 4)

def render(nombre, doc):
    h = os.path.join(HTML, nombre + ".html")
    open(h, "w", encoding="utf-8").write(doc)
    raw = os.path.join(HTML, nombre + "-raw.png")
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--allow-file-access-from-files", "--force-device-scale-factor=1",
                    "--window-size=1080,1500", f"--screenshot={raw}", "file://" + h],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
    Image.open(raw).convert("RGB").crop((0, 0, 1080, 1350)).save(os.path.join(PNG, nombre + ".png"))
    os.remove(raw)

pref = sys.argv[1] if len(sys.argv) > 1 else ""
for k in sorted(S):
    if k.startswith(pref):
        render(k, S[k]); print("ok", k)
