# coachera-redes

Imágenes de las publicaciones de Instagram de [@coachera.app](https://www.instagram.com/coachera.app/).

Están aquí para que Metricool pueda descargarlas al programar cada publicación. Todo lo que hay en
este repositorio es público y acaba publicado en Instagram: no subas nada que no sea una imagen ya
aprobada para publicar.

- `instagram/lote-01/`: las 9 primeras publicaciones (`NN-M.jpg` = publicación NN, imagen M del carrusel).
- `instagram/lote-02/`: las 9 del 16 al 30 de octubre de 2026, con la marca nueva: 5 reels (`rN-*.mp4`,
  con su portada `portada-N.jpg`) y 4 carruseles (`cN-M.jpg`). Fechas, horas y textos, en
  `publicaciones.json`. Sus fuentes están en `reels/`, `carruseles/` y `portadas/`.
- `instagram/virales/`: la serie «Cosas de entrenador», un reel de humor a la semana (los martes) con
  Coachera al final. Fuentes en `reels/vN-*.html`.
- `herramientas/`: los scripts que generan cada lote y cómo usarlos.
- `recursos/`: capturas de la app (con datos de ejemplo inventados) y el icono, que usan los scripts.
- `marca/`: el logotipo de octubre de 2026, «la C que avanza», en voltio (`#D6FF3F`) y negro. Los SVG y
  la foto de perfil de `marca/logo/` se generan con `python3 marca/construir.py`.
- `motor/`: con lo que se hacen los reels y los carruseles, sin red ni dependencias aparte de Chromium,
  ffmpeg y Python (numpy, scipy, Pillow):
  - `node motor/render.mjs <reel.html> <salida.mp4>`: una animación en HTML y CSS, fotograma a
    fotograma, a MP4 de 1080×1920 a 30 fps, con su sonido (`sonido.py`, sintetizado y a -14 LUFS).
  - `python3 motor/carrusel.py <carrusel.html> <prefijo> [alto]`: las diapositivas de 1080×1350 (o
    del alto que se diga: las portadas de los reels son de 1920) a JPG, y una hoja para revisarlas.
  - Las letras (IBM Plex, Archivo Black y Anton, licencia OFL; Permanent Marker, Apache 2.0) van en
    `motor/fuentes/`.
  - **Coachera TV** (`motor/tv.css`, `motor/tv.js`): la personalidad de los reels desde el 15-oct-2026,
    como una retransmisión (mosca, «en directo», marcador, rótulos, VAR, cinta de noticias, cortinilla
    con la C, «sin señal»). `motor/efectos.css`: alejar, atravesar, zoom a golpe, barras que crecen,
    muro de titulares, cristal, trazos que hierven y «romper el marco».
  - La música (`motor/musica.py`): phonk para los de humor, house para los de la app (y pop), todo
    sintetizado y mezclado para que se oiga en el altavoz de un móvil.
