# Convierte un texto en un trazado SVG con una fuente (para que el logotipo no dependa
# de tener la fuente instalada). tracking en milésimas de em, como en un programa de diseño.
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import os
AQUI = os.path.dirname(os.path.abspath(__file__))
_cache = {}
def fuente(nombre):
    if nombre not in _cache: _cache[nombre] = TTFont(nombre if os.path.isabs(nombre) else os.path.join(AQUI, nombre))
    return _cache[nombre]
def texto(nombre, cadena, tam=100, tracking=0, sustituir=None):
    """Devuelve (d, ancho, alto_mayus). Origen arriba a la izquierda, línea base en y=alto_mayus."""
    f = fuente(nombre)
    upem = f['head'].unitsPerEm
    cmap = f.getBestCmap(); gs = f.getGlyphSet(); hmtx = f['hmtx']
    esc = tam / upem
    cap = getattr(f['OS/2'], 'sCapHeight', 0) or upem*0.7
    pen = SVGPathPen(gs)
    x = 0
    for i, ch in enumerate(cadena):
        g = cmap.get(ord(ch))
        if sustituir and i in sustituir:
            sustituir[i](pen, x, esc, cap)   # glifo dibujado a mano
            x += sustituir[i].ancho * upem
        else:
            tp = TransformPen(pen, (esc, 0, 0, -esc, x*esc, cap*esc))
            gs[g].draw(tp)
            x += hmtx[g][0]
        x += tracking/1000*upem
    x -= tracking/1000*upem
    return pen.getCommands(), x*esc, cap*esc
