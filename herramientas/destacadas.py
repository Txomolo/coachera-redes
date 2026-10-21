# Las historias destacadas del perfil (1080×1920): «Empieza», «Tu panel» y «Su app», cinco
# historias cada una con las pantallas reales de la app, y sus tres portadas.
#   python3 herramientas/destacadas.py                → carruseles/destacadas-*.html
#   python3 motor/carrusel.py carruseles/destacadas-empieza.html salida/destacadas/empieza 1920
#
# Las pantallas salen de la app publicada (coachera-app, rama main) con sus escenas de datos
# inventados: node herramientas/pantallas-app.mjs <lista.json> salida/pantallas-dest/ con
# COACHERA_APP apuntando a una copia de main. Las «t-» son altas (375×2200 a 3×) y aquí se
# enseña su barra de arriba y, debajo, el contenido desde `desde` px: es lo que se ve en el
# móvil con la pantalla bajada, porque la barra de la app se queda fija. Las «m-» son de
# 375×812 (ventanas que flotan sobre la pantalla) y se enseñan tal cual.
#
# Zona segura de una historia: de 250 a 1700 (arriba va el nombre de la cuenta y abajo,
# «Enviar mensaje»). El móvil sale por abajo, cortado: lo que importa va en su mitad de arriba.
import html, os
from PIL import Image
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
P = "../salida/pantallas-dest"
VENTANAS = {"m-e-pegar-vista", "m-e-dieta", "m-ent-pegar", "m-ent-whatsapp-limpio", "m-c-equiv"}
BARRA = 50                     # alto de la barra de arriba de la app, en px de la app (375 de ancho)
C = '<svg viewBox="8 24 85 66"><path d="M60.93,69.45 A23.5,23.5 0 1 1 41.00,33.50 L83.50,33.50"/></svg>'
LOGO = f'<span class="logo-p">{C}<span class="txt">oachera</span></span>'

CSS = """
:root{--tinta:#06080B;--sf:#0E131A;--linea:rgba(255,255,255,.1);--texto:#FFFFFF;--cuerpo:#E8EDF3;--gris:#9AA6B8;--gris-2:#66727F;
 --turquesa:#14B8A6;--turquesa-t:#5EEAD4;--on-turquesa:#06231F;
 --sans:'IBM Plex Sans','Simbolos',system-ui,sans-serif;--mono:'IBM Plex Mono','Simbolos',ui-monospace,monospace}
*{box-sizing:border-box}html,body{margin:0;background:var(--tinta)}
body{width:1080px;font-family:var(--sans);color:var(--texto);-webkit-font-smoothing:antialiased}
.dia{position:relative;width:1080px;height:1920px;overflow:hidden;display:flex;flex-direction:column;padding:262px 84px 0;background:
 radial-gradient(1000px 760px at 50% 62%, rgba(20,184,166,.16), transparent 70%),
 radial-gradient(800px 500px at 50% 0%, rgba(20,184,166,.06), transparent 70%), var(--tinta)}
.alto-c{height:1350px;padding-top:96px}
.et{font-family:var(--mono);font-size:27px;font-weight:500;letter-spacing:.16em;color:var(--gris)}
.et b{color:var(--turquesa-t);font-weight:500}
h2{margin:22px 0 0;font-size:76px;line-height:1.05;font-weight:600;letter-spacing:-.025em;text-wrap:balance}
h2 em{font-style:normal;color:var(--turquesa-t)}
.sub{margin:22px 0 0;font-size:36px;line-height:1.34;color:var(--gris);text-wrap:pretty;max-width:880px}
.cta{display:flex;align-items:center;gap:26px;margin-top:34px}
.boton{flex-shrink:0;white-space:nowrap;display:inline-flex;align-items:center;height:88px;padding:0 40px;border-radius:999px;background:var(--turquesa);color:var(--on-turquesa);font-size:34px;font-weight:600;box-shadow:0 0 70px -12px rgba(20,184,166,.75)}
.web{white-space:nowrap;font-family:var(--mono);font-size:28px;color:var(--gris);letter-spacing:.03em;line-height:1.3}
.web b{display:block;color:var(--cuerpo);font-weight:500}
/* el escenario: el móvil (o los dos) debajo del texto, saliendo por abajo */
.escenario{position:relative;flex:1;margin:56px -84px 0}
.movil{position:absolute;padding:16px 16px 0;border-radius:74px 74px 0 0;background:#0B1016;border:2px solid rgba(255,255,255,.16);border-bottom:0;height:2200px;
 box-shadow:0 0 0 10px rgba(255,255,255,.035),0 40px 160px -20px rgba(20,184,166,.5)}
.movil::before{content:"";position:absolute;left:50%;top:calc(16px + 12px * var(--k));width:calc(110px * var(--k));height:calc(32px * var(--k));margin-left:calc(-55px * var(--k));border-radius:99px;background:#05080B;z-index:3}
/* la barra del sistema (la hora y la batería): la isla del móvil va ahí y no tapa la app */
.estado{display:flex;align-items:center;justify-content:space-between;height:calc(50px * var(--k));padding:calc(8px * var(--k)) calc(30px * var(--k)) 0;font-size:calc(15px * var(--k));font-weight:600;letter-spacing:.01em}
.estado i{display:flex;gap:calc(5px * var(--k));align-items:center}
.estado i::before{content:"";width:calc(17px * var(--k));height:calc(10px * var(--k));border-radius:calc(2px * var(--k));background:
 linear-gradient(90deg,currentColor 0 18%,transparent 18% 27%,currentColor 27% 45%,transparent 45% 54%,currentColor 54% 72%,transparent 72% 81%,currentColor 81%)}
.estado i::after{content:"";width:calc(22px * var(--k));height:calc(11px * var(--k));border-radius:calc(3px * var(--k));border:calc(1.5px * var(--k)) solid currentColor;box-sizing:border-box;background:linear-gradient(90deg,currentColor 0 70%,transparent 70%) content-box;padding:calc(1.5px * var(--k))}
.pantalla{position:relative;border-radius:58px 58px 0 0;overflow:hidden;background:#F5F7FA;height:100%}
.pantalla [style*="background-image"]{background-repeat:no-repeat;background-size:100% auto}
.foco{position:absolute;border-radius:18px;box-shadow:0 0 0 5px var(--turquesa-t),0 0 0 14px rgba(94,234,212,.22),0 0 60px rgba(20,184,166,.6);z-index:2}
.sin-isla::before{display:none}
.sin-isla{border-radius:56px 56px 0 0}.sin-isla .pantalla{border-radius:42px 42px 0 0}
.detras{filter:brightness(.62) saturate(.8)}
/* las portadas: Instagram enseña un círculo del centro */
.portada{padding:0;display:grid;place-items:center;background:var(--turquesa)}
.portada svg{width:400px;height:400px;fill:none;stroke:var(--on-turquesa);stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.logo-p{display:inline-flex;align-items:baseline;font-size:64px;color:#fff}
.logo-p svg{height:.56em;width:auto;margin-right:.07em;transform:translateY(.016em)}
.logo-p svg path{fill:none;stroke:var(--turquesa);stroke-width:19;stroke-linecap:round}
.logo-p .txt{font-family:'Archivo Black','IBM Plex Sans',sans-serif;letter-spacing:-.02em}
"""

def pagina(titulo, dias):
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{html.escape(titulo)}</title>
<link rel="stylesheet" href="../motor/fuentes.css"><style>{CSS}</style>
<!-- Generado por herramientas/destacadas.py: no se edita a mano. --></head><body>
{"".join(dias)}
</body></html>'''

def movil(img, x, y, ancho, desde=None, foco=None, clase="", isla=True):
    """Un móvil de `ancho` px en (x, y) del escenario. Con `desde` (pantallas «t-»): la barra de
    la app y, debajo, el contenido desde ese px. `foco` = (x, y, ancho, alto) en px de la app."""
    k = (ancho - 32) / 375
    url = f"{P}/{img}.png"
    if desde is None or img in VENTANAS:
        # una ventana que flota (pegar, invitar…): se baja entera, sin la barra de la app
        dy = desde or 0
        capas = f'<div style="height:{(812 - dy) * k:.0f}px;background-image:url({url});background-position:0 {-dy * k:.1f}px"></div>'
    else:
        capas = (f'<div style="height:{BARRA * k:.1f}px;background-image:url({url})"></div>'
                 f'<div style="height:{(812 if img.startswith("m-") else 2200) * k:.0f}px;background-image:url({url});background-position:0 {-(BARRA + desde) * k:.1f}px"></div>')
        dy = desde
    fondo = Image.open(os.path.join(RAIZ, "salida", "pantallas-dest", img + ".png")).convert("RGB").getpixel((20, 20))
    claro = sum(fondo) / 3 > 140
    estado = (f'<div class="estado" style="background:rgb{fondo};color:{"#0B0F14" if claro else "#FFFFFF"}">'
              '<b>9:41</b><i></i></div>') if isla else ""
    if not isla: clase += " sin-isla"
    f = ""
    if foco:
        fx, fy, fw, fh = foco
        f = f'<i class="foco" style="left:{fx * k:.0f}px;top:{(fy - dy) * k:.0f}px;width:{fw * k:.0f}px;height:{fh * k:.0f}px"></i>'
    return (f'<div class="movil {clase}" style="left:{x}px;top:{y}px;width:{ancho}px;--k:{k:.3f}">'
            f'<div class="pantalla">{estado}<div style="position:relative">{capas}{f}</div></div></div>')

def un_movil(img, desde=None, foco=None, ancho=800):
    return movil(img, (1080 - ancho) // 2, 0, ancho, desde, foco)

def historia(et, n, titulo, sub, escena, cta=False):
    c = ('<div class="cta"><span class="boton">Gratis hasta 5 clientes</span>'
         '<span class="web"><b>Sin tarjeta · coachera.fit</b>enlace en el perfil</span></div>') if cta else ""
    return f'''<section class="dia"><span class="et">{et} <b>·</b> {n}/5</span><h2>{titulo}</h2><p class="sub">{sub}</p>{c}
  <div class="escenario">{escena}</div></section>'''

DESTACADAS = {
 "empieza": [
  historia("EMPIEZA", 1, "Tus clientes, en una app <em>con tu marca</em>.",
           "Tú los llevas desde tu panel. Ellos entrenan, comen y te escriben desde su móvil.",
           movil("t-e-hoy", 40, 130, 600, desde=0, clase="detras") + movil("t-c-hoy", 440, 0, 600, desde=0)),
  historia("EMPIEZA", 2, "Crea tu cuenta <em>en un minuto</em>.",
           "Gratis hasta 5 clientes y sin tarjeta.", un_movil("m-entrada-signup")),
  historia("EMPIEZA", 3, "Pega tu rutina <em>desde Excel</em>.",
           "Copias las celdas de tu hoja: días, series, repes y descansos se colocan solos.", un_movil("m-ent-pegar")),
  historia("EMPIEZA", 4, "Invítale <em>por WhatsApp</em>.",
           "Le llega un mensaje con su enlace y entra desde el móvil, sin descargar nada.", un_movil("m-ent-whatsapp-limpio")),
  historia("EMPIEZA", 5, "Y ya está: <em>empieza contigo</em>.",
           "Su primer día, la app le guía paso a paso. Para él es gratis.", un_movil("t-c-nueva", desde=0, ancho=720), cta=True),
 ],
 "panel": [
  historia("TU PANEL", 1, "Cada mañana, <em>lo que te toca hoy</em>.",
           "Quién lleva días sin registrar, qué revisiones esperan y quién debe. Cada tarea, con su botón.",
           un_movil("t-e-hoy", desde=192)),
  historia("TU PANEL", 2, "Contesta las revisiones <em>con audio</em>.",
           "Cada una, frente a la anterior. Grabas y envías.",
           un_movil("t-e-rev3", desde=140, ancho=720)),
  historia("TU PANEL", 3, "Su ficha, <em>de un vistazo</em>.",
           "Peso, adherencia, racha y su próxima revisión. Y cómo va, semana a semana.",
           un_movil("t-e-ficha", desde=60)),
  historia("TU PANEL", 4, "Su dieta, <em>con opciones</em>.",
           "Menús para los días de entreno y los de descanso, con varias opciones en cada comida.",
           un_movil("t-e-nutri", desde=650)),
  historia("TU PANEL", 5, "Y quién <em>te ha pagado</em>.",
           "Lo cobrado, lo que falta y lo vencido, cliente a cliente.",
           un_movil("t-e-fact", desde=137, ancho=720), cta=True),
 ],
 "app": [
  historia("SU APP", 1, "Tu nombre <em>y tu color</em>.",
           "Tus clientes ven tu marca en su móvil, no la nuestra.",
           movil("t-c-hoy-b", 24, 90, 504, desde=0) + movil("t-c-hoy", 552, 0, 504, desde=0)),
  historia("SU APP", 2, "Entrena <em>serie a serie</em>.",
           "Kilos y repeticiones, con lo que hizo la vez anterior al lado.", un_movil("t-c-entreno", desde=0)),
  historia("SU APP", 3, "Y al terminar, <em>lo que ha conseguido</em>.",
           "Ejercicios, series, kilos movidos y sus marcas nuevas.", un_movil("m-cli-cerrado")),
  historia("SU APP", 4, "¿Sin arroz? <em>La app le dice cuánto</em>.",
           "Toca «Cambiar», elige otro alimento y le sale la cantidad.", un_movil("m-c-equiv")),
  historia("SU APP", 5, "Y sin cobertura, <em>sigue anotando</em>.",
           "Cada serie se queda en su móvil y se envía sola al volver la red.",
           un_movil("m-cli-sinred", ancho=720), cta=True),
 ],
}

ICONOS = {
  "empieza": '<svg viewBox="0 0 24 24"><path d="M6 21V4"/><path d="M6 4.5h10.5l-2.2 4 2.2 4H6"/></svg>',
  "panel": '<svg viewBox="0 0 24 24"><rect x="3.5" y="3.5" width="7" height="9" rx="1.6"/><rect x="13.5" y="3.5" width="7" height="5" rx="1.6"/><rect x="13.5" y="11.5" width="7" height="9" rx="1.6"/><rect x="3.5" y="15.5" width="7" height="5" rx="1.6"/></svg>',
  "app": '<svg viewBox="0 0 24 24"><rect x="6.5" y="2.5" width="11" height="19" rx="2.4"/><path d="M10.5 18.5h3"/></svg>',
}

# ---------- Los carruseles «Cómo funciona» (1080×1350), con el estilo del lote 4 ----------
CSS_K = """
.k{height:1350px;padding:100px 88px 0}
.k .et{color:var(--turquesa-t);letter-spacing:.1em}
.k h1{margin:34px 0 0;font-size:96px;line-height:1.02;font-weight:600;letter-spacing:-.03em;text-wrap:balance}
.k h2{margin:30px 0 0;font-size:64px;line-height:1.07}
.k .sub{font-size:34px;margin-top:22px}
.k .escenario{margin-top:44px;-webkit-mask-image:linear-gradient(#000 calc(100% - 210px),transparent calc(100% - 112px));mask-image:linear-gradient(#000 calc(100% - 210px),transparent calc(100% - 112px))}
.k.t{background:var(--turquesa);color:var(--on-turquesa)}
.k.t .et{color:rgba(6,35,31,.72)} .k.t h1,.k.t h2{color:var(--on-turquesa)} .k.t .sub{color:rgba(6,35,31,.82)}
.k.portada-k h1{margin-top:200px}
.pie{position:absolute;left:88px;right:88px;bottom:66px;display:flex;align-items:center;justify-content:space-between;z-index:5}
.marca{display:flex;align-items:center;gap:16px;font-size:28px;color:var(--gris);font-weight:500}
.marca img{width:52px;height:52px;border-radius:12px;display:block}
.k.t .marca{color:rgba(6,35,31,.78)} .k.t .marca img{box-shadow:0 0 0 2px rgba(6,35,31,.55)}
.cont{font-family:var(--mono);font-size:26px;color:var(--gris);display:flex;align-items:center;gap:14px}
.k.t .cont{color:rgba(6,35,31,.72)}
.desliza{font-size:44px;line-height:1}
.btn{display:inline-flex;align-items:center;background:var(--turquesa);color:var(--on-turquesa);font-weight:600;font-size:38px;padding:28px 44px;border-radius:999px;border:1.5px solid var(--turquesa-t);margin-top:64px;align-self:flex-start}
.nota{font-size:30px;color:var(--gris);margin-top:26px}
.k.final h2{margin-top:300px;font-size:80px}
"""

def pie(i, n, t=False):
    flecha = '<span class="desliza">→</span>' if i < n else ""
    return (f'<div class="pie"><span class="marca"><img src="../marca/logo/icono-1024.png" alt="">coachera.fit</span>'
            f'<span class="cont">{i}/{n} {flecha}</span></div>')

def k_portada(n, et, titulo, sub, turquesa=False):
    return f'''<section class="dia k portada-k{" t" if turquesa else ""}"><span class="et">{et}</span><h1>{titulo}</h1><p class="sub">{sub}</p>{pie(1, n)}</section>'''

def k_paso(i, n, et, titulo, sub, escena):
    return f'''<section class="dia k"><span class="et">{et}</span><h2>{titulo}</h2><p class="sub">{sub}</p><div class="escenario">{escena}</div>{pie(i, n)}</section>'''

def k_final(n, titulo, sub):
    return f'''<section class="dia k final"><h2>{titulo}</h2><p class="sub">{sub}</p><span class="btn">Empieza gratis en coachera.fit</span>
  <p class="nota">Gratis hasta 5 clientes · Sin tarjeta</p>{pie(n, n)}</section>'''

def k_movil(img, desde=None, foco=None, ancho=600):
    return movil(img, (1080 - ancho) // 2, 0, ancho, desde, foco, isla=False)

CARRUSELES = {
 "excel": [
  k_portada(6, "CÁMBIATE EN UNA TARDE", "Tu Excel, en el móvil de tu cliente.", "Copias tu rutina y tu dieta, las pegas y ya está. Sin volver a escribir nada.", turquesa=True),
  k_paso(2, 6, "1 · LA RUTINA", "Copia las celdas <em>y pégalas</em>.", "De Excel, Google Sheets, Numbers o LibreOffice.", k_movil("m-ent-pegar")),
  k_paso(3, 6, "2 · LO QUE ENTIENDE", "Días, series, repes y descansos, <em>en su sitio</em>.", "Y los ejercicios que no tienes en tu biblioteca, los añade de un toque.", k_movil("m-e-pegar-vista", desde=240)),
  k_paso(4, 6, "3 · LA DIETA", "Con la dieta, <em>igual</em>.", "Opciones en cada comida y menús de entreno y de descanso. Lo que no reconoce, se queda escrito.", k_movil("m-e-dieta", desde=180)),
  k_paso(5, 6, "4 · TU CLIENTE", "Y él la sigue <em>en su móvil</em>.", "Serie a serie en el gimnasio y comida a comida en casa.",
         movil("t-c-entreno", 70, 0, 460, desde=0, isla=False) + movil("t-c-comida", 550, 0, 460, desde=0, isla=False)),
  k_final(6, "Lo tienes escrito. <em>Pégalo</em>.", "Guárdalo para el día que te cambies."),
 ],
 "revisiones": [
  k_portada(5, "REVISIONES", "Las revisiones del domingo, en una bandeja.", "Cada una, comparada con la anterior y contestada con audio."),
  k_paso(2, 5, "1 · LA BANDEJA", "La que más lleva esperando, <em>primero</em>.", "Y en cada una, lo que destaca: un cambio grande o las fotos que faltan.", k_movil("t-e-bandeja", desde=0)),
  k_paso(3, 5, "2 · LA REVISIÓN", "Frente a la anterior, <em>y con audio</em>.", "Sus respuestas con el cambio al lado. Grabas, envías y pasas a la siguiente.", k_movil("t-e-rev3", desde=302)),
  k_paso(4, 5, "3 · TU CLIENTE", "Le llega <em>a su chat</em>.", "Tu audio y su informe, en la misma app donde os escribís.", k_movil("m-cli-respuesta", desde=250)),
  k_final(5, "En una bandeja, <em>no en diez chats</em>.", "Guárdalo para el domingo."),
 ],
 "cobros": [
  k_portada(6, "COBROS", "Sin hoja de cálculo para saber quién te debe.", "Las cuotas de tus clientes, en tu panel.", turquesa=True),
  k_paso(2, 6, "1 · SU CUOTA", "Cada cliente, <em>con su cuota</em>.", "Importe, cada cuánto y el próximo cobro. Cuando te paga, «Marcar como pagado».", k_movil("t-e-info", desde=1934)),
  k_paso(3, 6, "2 · HOY", "Los cobros que tocan, <em>en tu lista de hoy</em>.", "Junto a las revisiones y los mensajes.", k_movil("t-e-hoy-cobros", desde=470)),
  k_paso(4, 6, "3 · RECORDAR", "Recuérdaselo <em>sin pensar qué escribir</em>.", "«Recordar» abre su chat con el mensaje escrito. Lo lees y lo envías tú.", k_movil("m-e-recordar", desde=180)),
  k_paso(5, 6, "4 · EL MES", "Lo cobrado, lo que falta <em>y lo vencido</em>.", "Y lo previsto para el mes que viene.", k_movil("t-e-fact", desde=137)),
  k_final(6, "Tus cobros, <em>donde llevas a tus clientes</em>.", "Guárdalo para fin de mes."),
 ],
}

if __name__ == "__main__":
    d = os.path.join(RAIZ, "carruseles")
    for k, dias in DESTACADAS.items():
        open(os.path.join(d, f"destacadas-{k}.html"), "w", encoding="utf-8").write(pagina(f"Destacada · {k}", dias))
    portadas = [f'<section class="dia portada">{ICONOS[k]}</section>' for k in ICONOS]
    open(os.path.join(d, "destacadas-portadas.html"), "w", encoding="utf-8").write(pagina("Portadas de las destacadas", portadas))
    for k, dias in CARRUSELES.items():
        open(os.path.join(d, f"k-{k}.html"), "w", encoding="utf-8").write(pagina(f"Carrusel · {k}", dias).replace("</style>", CSS_K + "</style>"))
    print("ok")
