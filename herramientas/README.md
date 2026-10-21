# Cómo se hacen las imágenes

Cada lote es un script de Python que escribe una página HTML por imagen y la fotografía con
Chromium a 1080 × 1350 (4:5). `lote-01.py` es el primero y sirve de plantilla: para un lote nuevo,
cópialo como `lote-NN.py` y cambia solo el diccionario `S` (una entrada por imagen, `NN-M`).

## Antes de empezar (una vez por máquina)

1. **Las fuentes de la marca**, IBM Plex Sans y Mono, instaladas en el sistema (Chromium no carga
   Google Fonts sin red):
   ```
   npm i @ibm/plex-sans @ibm/plex-mono
   mkdir -p ~/.local/share/fonts
   cp node_modules/@ibm/plex-sans/fonts/complete/woff/IBMPlexSans-{Regular,Medium,SemiBold}.woff ~/.local/share/fonts/
   cp node_modules/@ibm/plex-mono/fonts/complete/woff/IBMPlexMono-{Regular,Medium,SemiBold}.woff ~/.local/share/fonts/
   fc-cache -f
   ```
2. **Pillow** (`pip install pillow`) y **Chromium** (variable `CHROME` con su ruta si no está en la de serie).

## Generar y publicar un lote

```
SALIDA=/tmp/lote python3 herramientas/lote-NN.py       # PNG en /tmp/lote/png
```

Revisa las imágenes, pásalas a JPG (calidad 92) en `instagram/lote-NN/` y súbelas. Metricool las
descarga desde `https://raw.githubusercontent.com/Txomolo/coachera-redes/main/instagram/lote-NN/NN-M.jpg`.

## Las reglas de diseño

- Fondo #06080B; superficies #0E131A y #131A23 con borde de 1 px rgba(255,255,255,.08–.16).
- Texto #FFFFFF (titulares), #E8EDF3 (cuerpo), #9AA6B8 (secundario).
- Turquesa #14B8A6 para rellenos con texto #06231F; #5EEAD4 cuando el turquesa es texto sobre oscuro.
- IBM Plex Sans 400/500/600 para el texto; IBM Plex Mono para las cifras. Nada más grueso que 600.
- Sin emojis, fotos de stock, degradados ni logos de otras marcas. Estados con símbolo: ✓ ✕ ! ◷ ▲.
- Margen de 80–88 px y lo importante en el centro: la cuadrícula del perfil recorta los lados (3:4).
- Portadas turquesa en diagonal en la cuadrícula; el resto, oscuras.
- Solo capturas reales de la app (en `recursos/`, sacadas con `npm run captura` del repositorio
  coachera-app, con datos de ejemplo inventados) y solo funciones que la app ya tiene.
- Los precios: solo «Gratis hasta 5 clientes · Sin tarjeta», como la web.

## Destacadas y carruseles «Cómo funciona» (desde el 21-oct-2026)

Las tres destacadas del perfil (Empieza, Tu panel y Su app: 15 historias y sus portadas) y tres
carruseles (Excel, Revisiones y Cobros), con las pantallas de la app publicada:

```
git -C ../coachera-app worktree add /tmp/app-main origin/main        # la app tal como está publicada
COACHERA_APP=/tmp/app-main node herramientas/pantallas-app.mjs herramientas/pantallas-destacadas.json salida/pantallas-dest
python3 herramientas/destacadas.py                                   # → carruseles/destacadas-*.html y k-*.html
python3 motor/carrusel.py carruseles/destacadas-empieza.html salida/destacadas/empieza 1920
python3 motor/carrusel.py carruseles/k-excel.html salida/carruseles-k/excel
```

Las pantallas «t-» son altas (375×2200 a 3×): se enseña su barra de arriba y, debajo, el
contenido desde `desde` px, que es lo que se ve con la pantalla bajada. Las «m-» son de 375×812.
En las historias, lo importante va por encima de 1700 px: ahí abajo Instagram pone «Enviar mensaje».
Las destacadas se publican como historias y se añaden a cada destacada a mano, desde la app.
