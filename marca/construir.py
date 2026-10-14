# El logotipo de Coachera: «la C que avanza». Genera los archivos maestros de marca/logo/.
#   python3 marca/construir.py      (después, render.sh pasa a PNG los que lo necesitan)
# La C es una sola línea de grueso constante (19 en una caja de 100) que da la vuelta y sigue
# hacia delante; extremos redondos. El nombre: la C hace de «c» y «oachera» va en Archivo Black.
import math, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import trazos
from fontTools.ttLib import TTFont

VOLTIO, NEGRO, BLANCO = "#D6FF3F", "#0B0F14", "#FFFFFF"
G, CX, CY, R, INI, LARGO = 19, 41, 57, 33, 32, 93
RM = R - G/2
x0, y0 = CX + RM*math.cos(math.radians(INI)), CY + RM*math.sin(math.radians(INI))
TRAZO = f"M{x0:.2f},{y0:.2f} A{RM},{RM} 0 1 1 {CX:.2f},{CY-RM:.2f} L{LARGO-G/2:.2f},{CY-RM:.2f}"
# caja visible de la C: de x 8 a 93 y de y 24 a 90
CAJA = (CX - R, CY - R, LARGO - (CX - R), 2*R)

def simbolo(color="currentColor"):
    return f'<path d="{TRAZO}" fill="none" stroke="{color}" stroke-width="{G}" stroke-linecap="round"/>'

def svg_simbolo(color="currentColor"):
    x, y, w, h = CAJA
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}">{simbolo(color)}</svg>\n'

FUENTE = os.path.join(AQUI, "..", "motor", "fuentes", "ArchivoBlack-Regular.woff2")
def svg_logo(c_simbolo="currentColor", c_texto="currentColor"):
    f = TTFont(FUENTE); upem = f['head'].unitsPerEm; xh = f['OS/2'].sxHeight
    tam = 100
    d, w, cap = trazos.texto(os.path.abspath(FUENTE), "oachera", tam, -20)
    xalto = xh / upem * tam                 # altura de la x en el mismo tamaño
    base = cap                               # trazos pone la línea base en y = cap
    # la C mide lo que la x (+3 % de compensación, como una letra redonda) y apoya en la línea base
    s = (xalto * 1.06) / CAJA[3]
    cx0 = -CAJA[0]*s; cy0 = base + xalto*0.03 - (CAJA[1] + CAJA[3])*s
    ancho_c = CAJA[2]*s
    hueco = tam * 0.065
    g_c = f'<g transform="translate({cx0:.2f} {cy0:.2f}) scale({s:.4f})">{simbolo(c_simbolo)}</g>'
    g_t = f'<path transform="translate({ancho_c + hueco:.2f} 0)" d="{d}" fill="{c_texto}"/>'
    arriba = base - cap          # mayúsculas ~ ascendentes de la h
    W = ancho_c + hueco + w
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {-2:.0f} {W:.1f} {cap + 6:.1f}">{g_c}{g_t}</svg>\n'

def svg_cuadrado(fondo, color, tam_simbolo=0.58, redondo=False, radio=0):
    x, y, w, h = CAJA
    s = tam_simbolo * 100 / w
    tx = 50 - (x + w/2)*s; ty = 50 - (y + h/2)*s + 1.5      # un pelo más abajo: la línea de arriba pesa
    fondo_el = (f'<circle cx="50" cy="50" r="50" fill="{fondo}"/>' if redondo else
                f'<rect width="100" height="100" rx="{radio}" fill="{fondo}"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">{fondo_el}<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.4f})">{simbolo(color)}</g></svg>\n'

L = os.path.join(AQUI, "logo")
os.makedirs(L, exist_ok=True)
archivos = {
  "coachera-simbolo.svg": svg_simbolo(),
  "coachera-simbolo-voltio.svg": svg_simbolo(VOLTIO),
  "coachera-simbolo-negro.svg": svg_simbolo(NEGRO),
  "coachera-logo.svg": svg_logo(),
  "coachera-logo-negro.svg": svg_logo(NEGRO, NEGRO),
  "coachera-logo-blanco.svg": svg_logo(BLANCO, BLANCO),
  "coachera-logo-voltio-blanco.svg": svg_logo(VOLTIO, BLANCO),
  "coachera-icono.svg": svg_cuadrado(VOLTIO, NEGRO, 0.60),
  "coachera-avatar.svg": svg_cuadrado(VOLTIO, NEGRO, 0.56, redondo=False),
}
for n, c in archivos.items():
    open(os.path.join(L, n), "w").write(c)
print("ok", list(archivos))
