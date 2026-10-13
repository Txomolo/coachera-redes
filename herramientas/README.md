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
