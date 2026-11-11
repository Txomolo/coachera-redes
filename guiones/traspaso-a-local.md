# Traspaso a una sesión local (11-nov-2026)

Este es el estado del trabajo que se hizo en una sesión en la nube, para seguir en Claude Code
en local con Claude in Chrome. Todo está en la rama `claude/quirky-babbage-zgco4v`.

## Antes de empezar

```bash
git fetch origin claude/quirky-babbage-zgco4v
git checkout claude/quirky-babbage-zgco4v
```

- Comprueba que Claude in Chrome está conectado y que la sesión de Google AI Studio está iniciada en Chrome.
- El motor necesita Chromium o Chrome, ffmpeg y Python con numpy, scipy y Pillow. En Windows,
  `render.mjs` encuentra Chrome solo. Si no, pon su ruta en la variable `CHROME`.
- Para partir la voz con `motor/alinear.py` hace falta Whisper de sherpa-onnx en local, en la variable
  `WHISPER` (lee la cabecera del script).

## Lo que ya está hecho (pendiente de que el usuario lo apruebe)

**«Cosas de entrenador», segunda tanda.** Son cinco reels de humor sin voz, con la identidad actual
(tinta, turquesa, IBM Plex y música pulso):

| Reel | Fecha | Vídeo |
|------|-------|-------|
| V4 · Audio de 4 minutos | mar 17/11 | `instagram/virales/v4-audio-de-4-minutos-final.mp4` |
| V5 · ¿Notas el cambio? | mar 24/11 | `instagram/virales/v5-notas-el-cambio-final.mp4` |
| BF · Black Friday | vie 27/11 | `instagram/virales/bf-black-friday-final.mp4` |
| V6 · Cena de empresa | mar 01/12 | `instagram/virales/v6-cena-de-empresa-final.mp4` |
| V7 · Se busca entrenador | mar 08/12 | `instagram/virales/v7-se-busca-entrenador-final.mp4` |

- Guiones: `guiones/cosas-de-entrenador-2.md`. Fuentes: `reels/v4-…`, `v5-…`, `bf-…`, `v6-…` y `v7-….html`.
- Textos y fechas: `instagram/virales/publicaciones.json`, con `"estado": "pendiente de aprobar"`.
- **Ojo con la estética:** la primera versión salió con la estética antigua (Coachera TV, Anton,
  voltio, phonk) y el usuario la rechazó. La de ahora es la de `motor/principios.css`, `dia.css` y
  `munecos.css`.
- **Faltan las portadas** de los cinco.

## Lo que hay que hacer ahora: m10 «Este es Dani, a fin de mes»

Es la continuación de m9 «Este es Dani, un lunes» (aprobado), con voz de Arlo. El guion completo
está en `guiones/m10-dani-fin-de-mes.md`.

**1. Generar la voz en Google AI Studio, abriendo una pestaña en Chrome** (lo pidió el usuario así):
   - aistudio.google.com → *Generate speech* (el TTS de Gemini).
   - Voz: **Arlo**. Instrucción de estilo: **«español de España, grave, cercano, un poco más rápido de lo
     normal»**. Es la misma configuración que en m9.
   - Texto, sin las marcas entre corchetes:
     > Este es Dani. Es día treinta. Doce clientes… y no sabe quién le ha pagado. Abre el banco: un Bizum de «Javi gym». ¿Qué Javi? Y a Andrés, que va con retraso… ¿cómo se lo dice sin quedar fatal? Con Coachera, abre Facturación. Lo cobrado, lo que falta y quién debe. Toca «Recordar»… y el mensaje ya está escrito. Tu fin de mes, sin abrir el banco.
   - Descarga el WAV a `salida/voz-m10/m10-dani.wav`. `salida/` no se versiona.

**2. Partir la voz y sacar los tiempos** con `motor/alinear.py`. Su guion JSON lleva
   `{"reels":[{"nombre":"m10-dani-fin-de-mes","voz":[{"texto":…,"marca":"gancho"},…]}]}`, con las
   frases y marcas de `guiones/m10-dani-fin-de-mes.md`. El resultado es un WAV y un `.tiempos.json`.

**3. Poner esos tiempos en el vídeo.** `reels/m10-dani-fin-de-mes.html` ya está hecho, con una versión sin voz
   para revisar el diseño: `instagram/munecos/m10-dani-fin-de-mes-sin-voz.mp4`, de 25,4 s con tiempos estimados.
   Todo se calcula desde el objeto `TIEMPOS` del principio del script: el segundo en que empieza cada frase,
   más `fin` para la duración total. Ahí van los tiempos del `.tiempos.json`. Si Arlo habla bastante más
   deprisa, cambia también `RITMO`, que reparte el karaoke dentro de cada frase.
   Para la voz, guarda el WAV (empezando en el segundo 0) en `instagram/munecos/voz/m10-dani-fin-de-mes.wav`
   y quita el `//` de `voz:` y `vol_voz: 1.7` en `window.REEL`. La música baja sola mientras habla.
   Los mismos pasos están en el comentario de la cabecera del HTML.

**4. Renderizar y revisar:**
   ```bash
   node motor/render.mjs reels/m10-dani-fin-de-mes.html instagram/munecos/m10-dani-fin-de-mes.mp4
   ```
   Al publicarlo hay que activar la etiqueta de «contenido creado con IA».

**5. Comparar con m9** (`instagram/munecos/m9-este-es-dani.mp4`). El código de m9 no está en el
   repositorio, así que el escritorio y Dani se han redibujado para que se parezcan. Si el código
   original de m9 está en tu ordenador, úsalo.

## Lo que el usuario quiere después

- **Vídeos en el estilo de dos reels de Instagram de referencia, pero de un entrenador.** Desde la
  nube no se pudieron abrir. Ábrelos en Chrome y míralos antes de escribir guiones:
  - https://www.instagram.com/reel/DeonnawBkxt/
  - https://www.instagram.com/reel/DfhVi6HFbGS/
- Dos ideas más para la serie de Dani, al final de `guiones/m10-dani-fin-de-mes.md`: «un domingo por
  la noche» y «con un cliente nuevo».

## Reglas que hay que seguir (README y `herramientas/README.md`)

- Este repositorio es público y lo que se sube acaba en Instagram. Solo se sube lo que está aprobado
  o va marcado como pendiente.
- Solo capturas reales de `recursos/` y solo funciones que la app ya tiene. Sin emojis ni marcas reales.
- Precio: «Gratis hasta 5 clientes» (algunas series usan «14 días gratis»).
- No se hacen pull requests salvo que el usuario los pida.
