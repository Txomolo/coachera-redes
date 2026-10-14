# Pasa a PNG un SVG (o una página .html) con Chromium (sin dependencias). python3 rasterizar.py entrada.svg salida.png ancho alto [fondo]
import sys, subprocess, os, tempfile
CHROME = os.environ.get("CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
def png(svg, salida, ancho, alto, fondo="transparent"):
    html = f'<!doctype html><style>html,body{{margin:0;background:{fondo}}}img{{display:block;width:{ancho}px;height:{alto}px}}</style><img src="file://{os.path.abspath(svg)}">'
    if svg.endswith(".html"):          # una página: se captura tal cual
        import shutil
        ruta = tempfile.mktemp(suffix=".html", dir=os.path.dirname(os.path.abspath(svg)))
        shutil.copy(svg, ruta)
    else:
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as t:
            t.write(html); ruta = t.name
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--hide-scrollbars", "--allow-file-access-from-files",
                    "--default-background-color=00000000", f"--window-size={max(ancho,500)},{alto+200}", f"--screenshot={os.path.abspath(salida)}",
                    "file://" + ruta], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    os.unlink(ruta)
    # Chrome sin ventana resta la barra de la ventana al alto y no baja de 500 de ancho: se pide de más y se recorta
    from PIL import Image
    Image.open(salida).crop((0, 0, ancho, alto)).save(salida)
if __name__ == "__main__":
    a = sys.argv[1:]
    png(a[0], a[1], int(a[2]), int(a[3]), a[4] if len(a) > 4 else "transparent")
