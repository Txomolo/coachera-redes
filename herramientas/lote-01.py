# Lote 1 de @coachera.app: las 9 primeras publicaciones (29 imágenes de 1080 x 1350).
# Uso: python3 herramientas/lote-01.py [prefijo]   (sin prefijo, todas). Ver herramientas/README.md
import os, sys, subprocess, html
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.abspath(os.path.join(AQUI, "..", "recursos"))          # capturas de la app y el icono
SALIDA = os.environ.get("SALIDA", "/tmp/coachera-redes-salida")      # aquí quedan los PNG
HTML = os.path.join(SALIDA, "html"); PNG = os.path.join(SALIDA, "png")
os.makedirs(HTML, exist_ok=True); os.makedirs(PNG, exist_ok=True)
CHROME = os.environ.get("CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
LOGO = f"file://{CAP}/icono-coachera.png"
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

# ---------- 1 · Qué es Coachera (5) ----------
S["01-1"] = slide('<div class="kicker">La app para entrenadores personales</div>'
  '<h1 style="font-size:132px;margin-top:150px">Más clientes.<br>Menos WhatsApp<br>y Excel.</h1>', True, 1, 5, True)
S["01-2"] = slide('<h2>Llevar una asesoría no debería ser perseguir a nadie.</h2><div class="filas">'
  + "".join(f'<div class="fila">{ICON[i]}{t}</div>' for i, t in [
    ("fuga", "Clientes que lo dejan sin que te enteres"),
    ("memoria", "Revisiones que comparas de memoria"),
    ("pdf", "Planes en PDF y mensajes sueltos"),
    ("cobro", "Cobros que se olvidan")]) + '</div>', False, 2, 5)
S["01-3"] = slide('<div class="kicker">Tu panel</div><h2>Abres el panel y sabes qué hacer primero.</h2>'
  + win("panel-hoy.png", "margin-top:64px;width:960px;margin-left:-28px"), False, 3, 5)
S["01-4"] = slide('<div class="kicker">La app de tus clientes</div><h2>Una app que tus clientes sí abren. Con tu marca.</h2>'
  + tel("cliente-hoy.png", 348, 430, 384), False, 4, 5)
S["01-5"] = slide('<h2 style="margin-top:80px">Lo que hoy llevas en cinco sitios, en uno.</h2><div class="chips">'
  + "".join(f'<span class="chip">{c}</span>' for c in ["Planes", "Revisiones", "Hábitos", "Cobros", "Chat"])
  + '</div><div style="margin-top:110px"><span class="btn">Empieza gratis en coachera.fit</span></div>'
  '<div class="nota">Gratis hasta 5 clientes · Sin tarjeta</div>', False, 5, 5)

# ---------- 2 · ¿Así llevas tu asesoría? (5) ----------
collage = '''
<div style="position:absolute;left:88px;top:470px;width:904px;height:620px">
 <div class="card" style="position:absolute;left:0;top:30px;width:420px;padding:34px;display:flex;flex-direction:column;gap:18px">
  <div style="display:flex;justify-content:space-between;align-items:center"><span class="mono" style="font-size:24px;color:var(--muted)">CHATS</span>
   <span class="mono" style="font-size:24px;background:var(--brand);color:var(--onbrand);border-radius:999px;padding:4px 16px">47</span></div>
  <div style="background:var(--sf2);border-radius:22px 22px 22px 6px;height:58px;width:78%"></div>
  <div style="background:var(--sf2);border-radius:22px 22px 22px 6px;height:58px;width:62%"></div>
  <div style="background:#1C2632;border-radius:22px 22px 6px 22px;height:58px;width:70%;align-self:flex-end"></div>
  <div style="background:var(--sf2);border-radius:22px 22px 22px 6px;height:58px;width:85%"></div>
 </div>
 <div class="card" style="position:absolute;right:0;top:0;width:450px;height:300px;overflow:hidden">
  <div style="display:grid;grid-template-columns:60px 1fr 1fr 1fr;grid-auto-rows:50px">
  ''' + "".join(f'<div style="border-right:1px solid var(--line);border-bottom:1px solid var(--line);{"background:var(--sf2)" if r==0 or c==0 else ""}"></div>' for r in range(6) for c in range(4)) + '''
  </div></div>
 <div class="card" style="position:absolute;right:60px;top:340px;width:250px;height:270px;padding:30px">
  <div class="mono" style="font-size:30px;color:var(--muted)">PDF</div>
  <div style="margin-top:26px;display:flex;flex-direction:column;gap:14px">
   <div style="height:12px;background:var(--sf2);width:100%"></div><div style="height:12px;background:var(--sf2);width:80%"></div>
   <div style="height:12px;background:var(--sf2);width:90%"></div><div style="height:12px;background:var(--sf2);width:60%"></div></div>
 </div>
 <div style="position:absolute;left:150px;top:470px;width:330px;padding:30px 32px;background:#E8EDF3;color:#0E131A;font-size:36px;font-weight:500;transform:rotate(-4deg);border-radius:6px">¿cobrar a Luis?</div>
</div>'''
S["02-1"] = slide('<h1>¿Así llevas tu asesoría?</h1>' + collage, False, 1, 5, True)
S["02-2"] = slide('<div class="cifra" style="margin-top:250px">47</div><h2 style="margin-top:60px;font-weight:500;color:var(--text)">chats sin leer, y uno es la revisión que esperabas.</h2>', False, 2, 5)
S["02-3"] = slide('<div class="cifra" style="margin-top:250px">23:40</div><h2 style="margin-top:60px;font-weight:500;color:var(--text)">Y tú, pasando a PDF la rutina de un cliente.</h2>', False, 3, 5)
S["02-4"] = slide('<h1 style="margin-top:250px">¿Quién te ha pagado este mes?</h1><div class="lead" style="font-size:44px">Si tienes que mirarlo en el banco, algo falla.</div>', False, 4, 5)
S["02-5"] = slide('<h1 style="margin-top:200px">Hay otra forma.</h1><div class="lead" style="font-size:44px">Planes, revisiones, hábitos, cobros y chat, en una sola app.</div>'
  '<div style="margin-top:90px"><span class="btn">coachera.fit</span></div>', False, 5, 5)

# ---------- 3 · Pega tu rutina desde Excel (4) ----------
S["03-1"] = slide('<h1 style="margin-top:230px">¿Tus rutinas están en Excel?</h1><h2 class="acento" style="margin-top:40px;color:var(--brandtext)">Pégalas.<br>No las vuelvas a escribir.</h2>', False, 1, 4, True)
S["03-2"] = slide('<div class="kicker">Pegar desde Excel</div><h2>Copias las celdas. Coachera entiende el resto.</h2>'
  + win("panel-pegar-excel.png", "margin-top:56px;width:960px;margin-left:-28px")
  + '<div class="nota" style="font-size:32px;line-height:1.4">Días, ejercicios, series y descansos. Sirve Excel, Google Sheets, Numbers o LibreOffice.</div>', False, 2, 4)
pasos = "".join(f'''<div style="display:flex;gap:36px;padding:44px 0;border-top:1.5px solid var(--line)">
 <div class="mono acento" style="font-size:64px;font-weight:500;line-height:1">{n}</div>
 <div style="font-size:42px;line-height:1.3;color:var(--text)">{t}</div></div>''' for n, t in [
  ("01", "Les mandas la invitación por WhatsApp o por correo."),
  ("02", "Instalan la app desde el navegador, sin tienda de apps. Para ellos es gratis.")])
S["03-3"] = slide('<h2 style="margin-top:120px">Y a tus clientes, los invitas por WhatsApp.</h2><div style="margin-top:80px;border-bottom:1.5px solid var(--line)">' + pasos + '</div>', False, 3, 4)
S["03-4"] = slide('<h1 style="margin-top:200px">Tu mudanza, en una tarde.</h1><div class="lead" style="font-size:44px">Y si empiezas de cero, tienes plantillas de entreno listas para usar.</div>'
  '<div style="margin-top:90px"><span class="btn">Empieza gratis en coachera.fit</span></div>', False, 4, 4)

# ---------- 4 · Serie a serie (1) ----------
# Teléfono: ancho 430 -> pantalla 402 de ancho (1125x2436); y de la pantalla = top+14
TW, TL, TT = 396, 88, 380
sw = TW - 28; sh = sw * 2436 / 1125
def pt(fx, fy): return (TL + 14 + fx * sw, TT + 14 + fy * sh)
ax1, ay1 = pt(0.47, 0.502)   # «La vez anterior: 57,5 × 7»
ax2, ay2 = pt(0.675, 0.754)  # ▲ de la primera serie
lx = 600
anot = f'''
<svg style="position:absolute;left:0;top:0" width="1080" height="1350">
 <g stroke="#5EEAD4" stroke-width="2.5" fill="none">
  <circle cx="{ax1}" cy="{ay1}" r="10" fill="#5EEAD4"/><path d="M{ax1} {ay1} H{lx-20}"/>
  <circle cx="{ax2}" cy="{ay2}" r="10" fill="#5EEAD4"/><path d="M{ax2} {ay2} H{lx-20}"/>
 </g></svg>
<div style="position:absolute;left:{lx}px;top:{ay1-50}px;width:400px;font-size:36px;line-height:1.25;color:#fff;font-weight:500">Lo de la última vez, a la vista</div>
<div style="position:absolute;left:{lx}px;top:{ay2-50}px;width:400px;font-size:36px;line-height:1.25;color:#fff;font-weight:500"><span class="acento">▲</span> Marca nueva, en la propia serie</div>'''
S["04-1"] = slide('<h1>Serie a serie.</h1><div class="lead" style="margin-top:22px;max-width:880px">Tu cliente ve lo que hizo la vez anterior y anota kilos y repeticiones en dos toques.</div>'
  + tel("cliente-entreno.png", TL, TT, TW) + anot)

# ---------- 5 · Revisiones comparadas (4) ----------
S["05-1"] = slide('<div class="kicker">Revisiones</div><h1 style="font-size:124px;margin-top:150px">Revisiones que no comparas de memoria.</h1>', True, 1, 4, True)
S["05-2"] = slide('<h2>Cada revisión llega junto a la anterior.</h2>'
  + win("panel-revision.png", "margin-top:56px;width:960px;margin-left:-28px")
  + '<div class="nota" style="font-size:32px;line-height:1.4">Peso medio de 7 días, medidas, fotos lado a lado y respuestas, frente a la revisión anterior.</div>', False, 2, 4)
tarjeta = '''<div class="card" style="margin-top:80px;padding:52px 56px;border-left:6px solid #fff">
 <div class="mono" style="font-size:24px;letter-spacing:.1em;color:var(--muted)">SU SEMANA</div>
 <div style="font-size:50px;font-weight:600;color:#fff;margin-top:20px">¿Cuánta hambre has pasado?</div>
 <div style="display:flex;justify-content:space-between;margin-top:48px">''' + "".join(f'''<div>
   <div class="mono" style="font-size:24px;letter-spacing:.1em;color:var(--muted)">{l}</div>
   <div class="mono" style="font-size:120px;font-weight:500;color:#fff;line-height:1;margin-top:10px">{v}</div></div>''' for l, v in [("ANTES", "4"), ("AHORA", "8"), ("CAMBIO", "+4")]) + '</div></div>'
S["05-3"] = slide('<h2>Lo que cambia salta a la vista.</h2>' + tarjeta
  + '<div class="lead" style="font-size:42px;margin-top:64px">La app marca lo que destaca. <span style="color:#fff">Tú decides qué significa.</span></div>', False, 3, 4)
onda = '<svg width="904" height="120" style="display:block;margin-top:56px">' + "".join(
  f'<rect x="{i*16}" y="{60-h/2}" width="7" height="{h}" rx="3.5" fill="#3A4656"/>' for i, h in enumerate(
  [12,24,40,30,60,84,50,36,70,96,64,40,28,52,80,58,34,22,44,72,90,62,38,26,48,66,42,30,20,36,58,76,50,32,24,16,28,46,64,40,26,18,30,22,14,20,12,10,16,12,8,10,8,6,10,8]
)) + '</svg>'
S["05-4"] = slide('<h2 style="margin-top:110px">Y contestas con un audio.</h2>'
  '<div style="margin-top:80px"><span class="btn" style="font-size:44px;padding:34px 52px"><span style="width:22px;height:22px;border-radius:50%;background:var(--onbrand);display:inline-block"></span>Grabar respuesta</span></div>'
  + onda + '<div class="lead" style="font-size:42px">Grabas, lo escuchas y lo envías. Le llega a su chat, con aviso al móvil.</div>', False, 4, 4)

# ---------- 6 · 5 señales (7) ----------
S["06-1"] = slide('<div class="kicker">Para guardar</div><h1 style="font-size:104px;margin-top:120px">5 señales de que tu asesoría online necesita un sistema</h1>'
  '<div class="lead" style="font-size:42px;margin-top:48px">Guárdalo y cuenta cuántas tienes.</div>', False, 1, 7, True)
senales = [
 ("01", "Buscas el plan de un cliente en tres sitios.", "El Excel, el PDF que le mandaste y el audio donde se lo cambiaste."),
 ("02", "Las revisiones llegan cuando el cliente se acuerda.", "Y si no llega, no te enteras hasta que lo deja."),
 ("03", "No sabes de memoria quién te debe la cuota.", "Y te da apuro preguntarlo."),
 ("04", "Contestas mensajes a las 23:00.", "Porque es el único rato que te queda."),
 ("05", "Te da miedo coger más clientes.", "No por falta de ganas: por falta de horas.")]
for i, (n, f, e) in enumerate(senales):
    S[f"06-{i+2}"] = slide(f'<div class="cifra acento" style="font-size:240px;margin-top:150px;color:var(--brandtext)">{n}</div>'
      f'<h2 style="margin-top:70px;font-size:76px">{f}</h2><div class="lead" style="font-size:42px;margin-top:36px">{e}</div>', False, i+2, 7)
S["06-7"] = slide('<h1 style="margin-top:200px">¿Tienes dos o más?</h1><div class="lead" style="font-size:44px">Coachera junta planes, revisiones, hábitos, cobros y chat en una app.</div>'
  '<div style="margin-top:90px"><span class="btn">Gratis hasta 5 clientes · coachera.fit</span></div>', False, 7, 7)

# ---------- 7 · Con tu marca (1) ----------
S["07-1"] = slide('<h1 style="font-size:88px">Tus clientes ven tu marca. No la nuestra.</h1>'
  + tel("cliente-marca-roja.png", 64, 420, 300) + tel("cliente-marca-azul.png", 716, 420, 300) + tel("cliente-hoy.png", 372, 380, 336)
  + '<div style="position:absolute;left:88px;right:88px;top:1120px;font-size:32px;line-height:1.35;color:var(--muted)">Tu nombre comercial y tu color en la app de tus clientes. Se instala desde el navegador y para ellos es gratis.</div>')

# ---------- 8 · Fundador (1) ----------
lineas = ["Llevo 2 años entrenando a clientes online.", "Con WhatsApp y Excel, todo era poco práctico e incómodo.", "Así que estoy construyendo la herramienta que me faltaba."]
S["08-1"] = slide('<div class="kicker">Quién está detrás</div><h1 style="font-size:110px">Soy entrenador. Por eso hago Coachera.</h1>'
  '<div style="margin-top:80px;border-bottom:1.5px solid var(--line)">' + "".join(f'<div style="padding:30px 0;border-top:1.5px solid var(--line);font-size:40px;line-height:1.3;color:var(--text)">{l}</div>' for l in lineas)
  + '</div><div style="margin-top:44px;font-size:32px;color:var(--muted)">Víctor · fundador de Coachera</div>')

# ---------- 9 · Empieza gratis (1) ----------
S["09-1"] = slide('<h1 style="font-size:112px;margin-top:110px">Tu próximo cliente merece algo mejor que un PDF.</h1>'
  '<div class="lead" style="font-size:42px;margin-top:44px">Crea tu cuenta gratis: en unos minutos tienes a tu primer cliente con su plan.</div>'
  '<div class="chips" style="margin-top:64px"><span class="chip" style="font-size:34px">Gratis hasta 5 clientes · Sin tarjeta</span></div>', True)

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
