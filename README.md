# coachera-redes

Imágenes de las publicaciones de Instagram de [@coachera.app](https://www.instagram.com/coachera.app/).

Están aquí para que Metricool pueda descargarlas al programar cada publicación. Todo lo que hay en
este repositorio es público y acaba publicado en Instagram: no subas nada que no sea una imagen ya
aprobada para publicar.

- `instagram/lote-01/`: las 9 primeras publicaciones (`NN-M.jpg` = publicación NN, imagen M del carrusel).
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
  - Las letras (IBM Plex y Archivo Black, licencia OFL) van en `motor/fuentes/`.
