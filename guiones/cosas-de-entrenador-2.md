# «Cosas de entrenador» · segunda tanda (V4-V7 y especial Black Friday)

Reels de humor de 15-20 s, uno a la semana, en el estilo de V1-V3 (Coachera TV, `motor/tv.css` y
`motor/tv.js`, música phonk). La regla de la serie es que **la broma va primero y Coachera aparece solo
en el cierre (los últimos 3-4 s)**: la C que se dibuja, el logotipo y la píldora «Gratis hasta 5
clientes». En el cierre solo salen funciones que la app ya tiene.

| Reel | Fecha | Título | Función de la app en el cierre |
|------|-------|--------|--------------------------------|
| V4 | mar 17/11 18:00 | Audio de 4 minutos | Equivalencias: «Cambiar» en su menú |
| V5 | mar 24/11 18:00 | ¿Notas el cambio? | Revisiones: fotos por fecha, una al lado de otra |
| BF | vie 27/11 18:00 | Ofertas que no deberías hacer | La oferta de verdad: gratis hasta 5 clientes |
| V6 | mar 01/12 18:00 | Cena de empresa: en directo | Lo que cuenta es volver: el entreno del lunes |
| V7 | mar 08/12 18:00 | Se busca entrenador | El panel «Hoy»: una sola app |

Los clientes tienen nombres inventados (Andrés, Lucía, Javier…). No salen marcas reales ni personas
reales.

---

## V4 · Audio de 4 minutos
**Formato:** un chat de WhatsApp genérico (con los colores del de V2: burbuja #202C33), sin el logo.
**Duración:** unos 17 s.

| t (s) | En pantalla | Sonido |
|-------|-------------|--------|
| 0,0 | GANCHO, que se ve desde el primer fotograma: «Tu cliente te ha mandado un audio» y, debajo, la burbuja de nota de voz con **4:37** en grande. | silbato |
| 1,6 | La onda del audio empieza a reproducirse. Sale el rótulo de TV «EN DIRECTO · MINUTO 0:12» y los subtítulos, frase a frase: «Hola, oye, una cosa…» | toque |
| 3,5 | «MINUTO 1:48»: «…que mi cuñado dice que el arroz por la noche…» | barrido |
| 5,5 | «MINUTO 3:02»: «…y luego está lo del ayuno, que lo vi en un vídeo…» | barrido |
| 7,5 | El entrenador (texto de narrador, `tv-narra`) «sigue esperando la pregunta». Un reloj que corre. | tecla |
| 9,0 | «MINUTO 4:31». Aparece la pregunta en grande: **«¿El pollo se pesa en crudo o en cocinado?»** | golpe + publico |
| 11,0 | Sello «4 MINUTOS · 1 PREGUNTA». | var |
| 12,5 | Cortinilla con la C, «FINAL». Cierre: «Lo que no hace falta preguntar, **ya lo tiene en su app**.» Al lado, la captura `recursos/cliente-equivalencia.png` dentro de un móvil. | barrido, marca |
| 14,5 | Logotipo y píldora «Gratis hasta 5 clientes». | |

**Texto:**
> Un audio de 4:37 para una pregunta de 6 segundos.
>
> Mándaselo a ese entrenador que escucha audios a 2x.
>
> Con Coachera tu cliente ve en su menú las cantidades y, si no tiene arroz, toca «Cambiar» y le sale la equivalencia. Gratis hasta 5 clientes. Enlace en la bio.
>
> #entrenadorpersonal #entrenadoronline #asesoriaonline #humorgym

---

## V5 · ¿Notas el cambio?
**Formato:** concurso de «encuentra las diferencias» en Coachera TV.
**Duración:** unos 17 s.

| t (s) | En pantalla | Sonido |
|-------|-------------|--------|
| 0,0 | GANCHO: «Encuentra las diferencias», con el subtítulo «REVISIÓN DE LA SEMANA 1 VS. LA SEMANA 6». | silbato |
| 1,5 | Dos «fotos» (siluetas de muñeco de palo de `motor/munecos.js`, iguales) en el mismo espejo, con la misma camiseta y la misma luz. Mensaje del cliente: «¿Notas el cambio?» | toque |
| 3,5 | Un cronómetro de concurso: 10, 9, 8… Una lupa recorre las dos fotos. | tecla |
| 6,0 | Rótulos de diferencias encontradas, uno a uno: «1. La toalla está doblada», «2. Hay otra planta», «3. ¿Se ha cortado el pelo?». | pop ×3 |
| 9,5 | El marcador «DIFERENCIAS EN EL CUERPO: 0», con un ! en amarillo. | golpe |
| 11,0 | Narrador: «Spoiler: **sí que había cambio.** Pero en lo que no sale en la foto.» | publico |
| 12,5 | Cortinilla, FINAL. La captura `recursos/panel-revision.png` con zoom en «Peso −0,7 kg · Hábitos 83 %» y las fotos por fecha. Texto: «Fotos, peso y respuestas, **comparadas con la revisión anterior**.» | barrido, marca |
| 14,8 | Logotipo y píldora. | |

**Texto:**
> «¿Notas el cambio?» Misma luz, mismo espejo, misma camiseta.
>
> Etiqueta al compañero que se ha pasado 10 minutos con el zoom.
>
> Con Coachera ves cada revisión al lado de la anterior: las fotos por fecha, el peso, los hábitos y sus respuestas, y le contestas con un audio. Gratis hasta 5 clientes. Enlace en la bio.
>
> #entrenadorpersonal #entrenadoronline #asesoriaonline #humorgym

---

## BF · Ofertas que no deberías hacer (especial Black Friday)
**Formato:** como el especial de Halloween (V3), con el estilo de un folleto de rebajas: etiquetas de
precio que se tachan, cinta de noticias de TV con «BLACK FRIDAY» y voltio sobre negro.
**Duración:** unos 18 s.

| t (s) | En pantalla | Sonido |
|-------|-------------|--------|
| 0,0 | GANCHO: «BLACK FRIDAY para entrenadores», con el subtítulo «OFERTAS QUE NO DEBERÍAS HACER». | silbato |
| 1,6 | Etiqueta 1: «**2×1 en burpees**» (el precio tachado: «20 burpees → 40 burpees»). Comentarista: «tu cliente no lo ve como una oferta». | pop, golpe |
| 4,2 | Etiqueta 2: «**−70 % en sentadillas**». Comentarista: «son 3 repeticiones. Las ha hecho de pie». | pop, golpe |
| 6,8 | Etiqueta 3: «**Revisión gratis… a las 23:58 del domingo**». | pop, golpe |
| 9,4 | Etiqueta 4: «**Rutina personalizada**», con la letra pequeña: «la misma para todos, en PDF». | pop, golpe |
| 12,0 | Sello «OFERTA RETIRADA» encima de las cuatro. | var |
| 13,0 | Cortinilla. Cierre: «La única oferta que **sí** vale la pena:» + el logotipo + la píldora grande «Gratis hasta 5 clientes · Sin tarjeta». | barrido, marca, publico |

**Texto:**
> Black Friday para entrenadores: 4 ofertas que no deberías hacer nunca.
>
> Mándaselo a ese compañero que ya ha anunciado el 2×1 en burpees.
>
> La que sí: Coachera es gratis hasta 5 clientes, sin tarjeta. Y no caduca el lunes. Enlace en la bio.
>
> #blackfriday #entrenadorpersonal #entrenadoronline #humorgym

---

## V6 · Cena de empresa: en directo
**Formato:** una retransmisión deportiva de Coachera TV, como si la cena fuera un partido (marcador,
minutos, cinta de noticias).
**Duración:** unos 18 s.

| t (s) | En pantalla | Sonido |
|-------|-------------|--------|
| 0,0 | GANCHO: «Tu cliente, en la cena de empresa», con «EN DIRECTO» y el marcador «PLAN 0 - 0 CENA». | silbato |
| 1,8 | Minuto 5: «Solo una cerveza.» Marcador 0-1. | golpe |
| 4,0 | Minuto 32: «Croquetas al centro. "Son caseras, no cuentan".» 0-2. | golpe, publico |
| 6,2 | Minuto 58: «El turrón llega por la banda.» 0-3. | golpe |
| 8,4 | Minuto 90+4: «Alguien ha dicho "la última y nos vamos".» 0-4. Cinta de noticias: «ÚLTIMA HORA: TU CLIENTE PIENSA EMPEZAR DE CERO EN ENERO». | noticia |
| 11,0 | Cortinilla con «LUNES». Narrador: «El partido no se pierde en una cena. **Se pierde si no vuelve el lunes.**» | barrido |
| 13,0 | La captura `recursos/cliente-hoy.png` en un móvil: el entreno del lunes. El marcador cambia: «VUELTA AL PLAN 1 - 0». | ok, publico |
| 15,0 | Logotipo y píldora. | marca |

**Texto:**
> Una cena no tira un mes de trabajo. Lo que lo tira es «ya empiezo en enero».
>
> Pásaselo a ese entrenador que ya está temiendo las revisiones de diciembre.
>
> Con Coachera tu cliente abre la app el lunes y tiene su entreno ahí, como si nada. Gratis hasta 5 clientes. Enlace en la bio.
>
> #entrenadorpersonal #entrenadoronline #asesoriaonline #navidad #humorgym

---

## V7 · Se busca entrenador
**Formato:** una oferta de empleo que se va alargando (un rollo de papel que no se acaba) con
requisitos absurdos que son, de verdad, lo que hace un entrenador online.
**Duración:** unos 18 s.

| t (s) | En pantalla | Sonido |
|-------|-------------|--------|
| 0,0 | GANCHO: «SE BUSCA: entrenador personal», con el subtítulo «REQUISITOS». | silbato |
| 1,5 | Los requisitos van saliendo con un ✓, cada vez más deprisa: «Programar rutinas» · «Hacer de nutricionista» · «Psicólogo los domingos por la noche» · «Cobrador a fin de mes» · «Community manager» · «Contestar audios de 4 minutos» · «Abogado (contratos)» · «Detective (¿ha entrenado o no?)». El papel baja y la lista sigue. | pop en cada ✓ |
| 9,0 | Al pie, en letra pequeña: «Horario: siempre. Herramientas: 6 apps y un Excel». Zoom a golpe. | golpe |
| 10,5 | Sello «PUESTO CUBIERTO… POR TI». | var, publico |
| 11,8 | Cortinilla, FINAL. Las 6 apps (iconos genéricos, sin logos reales) se juntan en una: `recursos/panel-hoy.png`. Texto: «Rutinas, revisiones, cobros y contratos. **En una sola app.**» | barrido |
| 14,8 | Logotipo y píldora. | marca |

**Texto:**
> Se busca entrenador: que programe, cobre, haga de psicólogo y conteste audios de 4 minutos. Horario: siempre.
>
> Etiqueta al compañero que cumple todos los requisitos.
>
> Con Coachera tienes en un panel lo de hoy: revisiones, avisos, cobros y contratos. Tus clientes, en su app. Gratis hasta 5 clientes. Enlace en la bio.
>
> #entrenadorpersonal #entrenadoronline #asesoriaonline #humorgym
