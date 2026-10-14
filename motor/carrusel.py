# Corta un carrusel (una página con sus .dia de 1080×1350 una debajo de otra) en JPG.
#   python3 motor/carrusel.py carruseles/c1-asi-llevas.html instagram/lote-02/c1
#   → c1-1.jpg, c1-2.jpg… (calidad 92) y c1-hoja.jpg, todas en pequeño para revisarlas.
# Con un tercer argumento, otro alto: las portadas de los reels son de 1920.
#   python3 motor/carrusel.py portadas/portadas.html instagram/lote-02/portada 1920
import os, re, subprocess, sys, tempfile
from PIL import Image
CHROME = os.environ.get("CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
ANCHO, ALTO = 1080, 1350

pagina, prefijo = os.path.abspath(sys.argv[1]), sys.argv[2]
if len(sys.argv) > 3: ALTO = int(sys.argv[3])
n = len(re.findall(r'class="dia[ "]', open(pagina, encoding="utf-8").read()))
total = n * ALTO
os.makedirs(os.path.dirname(os.path.abspath(prefijo)), exist_ok=True)
with tempfile.TemporaryDirectory() as d:
    png = os.path.join(d, "todo.png")
    # Chrome sin ventana resta la barra de la ventana al alto: se pide de más y se recorta.
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--hide-scrollbars", "--allow-file-access-from-files",
                    "--force-color-profile=srgb", "--virtual-time-budget=4000", f"--window-size={ANCHO},{total + 200}",
                    f"--screenshot={png}", "file://" + pagina], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    todo = Image.open(png).convert("RGB")
    piezas = []
    for i in range(n):
        im = todo.crop((0, i * ALTO, ANCHO, (i + 1) * ALTO))
        ruta = f"{prefijo}-{i + 1}.jpg"
        im.save(ruta, quality=92, optimize=True)
        piezas.append(im)
    # la hoja para revisar, en filas de 4
    col = min(4 if ALTO <= 1350 else 5, n); fil = (n + col - 1) // col; w, h = 270, round(270 * ALTO / ANCHO)
    hoja = Image.new("RGB", (col * (w + 8) + 8, fil * (h + 8) + 8), (34, 34, 34))
    for i, im in enumerate(piezas):
        hoja.paste(im.resize((w, h)), (8 + (i % col) * (w + 8), 8 + (i // col) * (h + 8)))
    hoja.save(f"{prefijo}-hoja.jpg", quality=85)
print(f"{n} diapositivas: {prefijo}-1…{n}.jpg")
