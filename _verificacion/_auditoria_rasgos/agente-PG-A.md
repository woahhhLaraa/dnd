# Informe lector A — PG al subir de nivel

Fuente leída: `/tmp/render_pg/p-044.png` (pdf 44 = libro 42), leída con la
herramienta de lectura de imágenes. No ha hecho falta consultar p-043.png
(nada se corta al borde de la página). No se ha usado `pdftotext` ni
conocimiento previo de D&D; todo lo transcrito abajo está impreso en la
imagen.

## 1. Paso de «ajustar los puntos de golpe» en SUBIR DE NIVEL (transcripción literal completa)

La sección se titula **"Subir de nivel"** y empieza con: "Cuando subas de
nivel, sigue estos pasos:". El paso relevante es el número 2:

> "2: Ajustar los puntos de golpe y los dados de golpe. Cada vez que subas
> un nivel, obtendrás un dado de golpe adicional. Tira ese dado, suma tu
> modificador por Constitución al resultado y añade el total (mínimo de 1)
> a tus puntos de golpe máximos. En vez de tirar, puedes utilizar el valor
> establecido que se muestra en la tabla "Puntos de golpe establecidos por
> clase"."

(Transcripción literal, sin condensar.)

## 2. ¿Ofrece la página más de una forma de obtener los PG de un nivel nuevo?

**Sí, dos formas**, ambas descritas literalmente dentro del propio paso 2
citado arriba:

- **Tirar el dado**: "Tira ese dado, suma tu modificador por Constitución al
  resultado y añade el total (mínimo de 1) a tus puntos de golpe máximos."
- **Usar un valor fijo**: "En vez de tirar, puedes utilizar el valor
  establecido que se muestra en la tabla "Puntos de golpe establecidos por
  clase"."

No hay una tercera forma en la página.

## 3. Tabla cercana al texto: título y transcripción íntegra

**Título exacto de la tabla**: "Puntos de golpe establecidos por clase"

Columnas: **Clase** | **Puntos de golpe por nivel**

Filas (todas las que aparecen, tal cual, en el orden impreso):

| Clase | Puntos de golpe por nivel |
|---|---|
| Bárbaro | 7 + modificador por Con |
| Explorador, guerrero o paladín | 6 + modificador por Con |
| Bardo, brujo, clérigo, druida, monje o pícaro | 5 + modificador por Con |
| Hechicero o mago | 4 + modificador por Con |

No hay más filas visibles ni indicios de que falte alguna (la tabla termina
ahí, con espacio en blanco debajo en la columna izquierda).

## 4. ¿Qué dice sobre los PG máximos si sube el modificador por Constitución?

Sí, aparece en el paso **5 ("Ajustar los modificadores por característica")**
de la columna derecha. Transcripción literal completa del paso 5:

> "5: Ajustar los modificadores por característica. Si escoges una dote que
> aumente una o varias de tus puntuaciones de característica, tu
> modificador por característica también cambiará si la nueva puntuación es
> un número par. Cuando eso ocurra, ajusta todos los números de la hoja de
> personaje que utilicen ese modificador por característica. Cuando tu
> modificador por Constitución aumente en 1, tus puntos de golpe máximos
> también aumentarán en 1 por cada nivel que hayas alcanzado. Por ejemplo,
> si un personaje alcanza el nivel 8 y aumenta su puntuación de
> Constitución de 17 a 18, el modificador por Constitución pasará a ser de
> +4. Los puntos de golpe máximos del personaje aumentarán en 8, más los
> puntos de golpe obtenidos al alcanzar el nivel 8."

(La última línea "obtenidos al alcanzar el nivel 8" se lee con claridad en
el recorte ampliado; la frase completa continúa correctamente el sentido de
la anterior — no hay corte de página ni texto perdido.)

## 5. ¿Aparece «máximo» referido al dado de golpe, o la regla de PG del nivel 1?

- **"máximo" referido al dado de golpe**: **no aparece**. La palabra
  "máximos" solo aparece en esta página referida a "puntos de golpe
  máximos" (tres veces: en el paso 2 y dos veces en el paso 5), nunca
  pegada a "dado de golpe".
- **Regla de PG del nivel 1**: **no aparece** en esta página. Todo el texto
  de "Subir de nivel" habla de qué ocurre "cada vez que subas un nivel" /
  "subas de nivel"; no hay ninguna mención explícita al nivel 1 ni a cómo se
  calculan los PG iniciales de un personaje de nivel 1. La única mención a
  un nivel numérico concreto en la página es el nivel 8 del ejemplo del
  paso 5.

## Notas de fiabilidad

- Todo el texto anterior se ha verificado dos veces: una lectura de la
  página completa y una segunda pasada con recortes ampliados (herramienta
  `convert`/`magick` solo para recortar, no para OCR) de la tabla, el paso 2
  y el paso 5, para confirmar cada palabra y cada número.
- Nada de la página se leyó como "no se lee con claridad"; todo el texto
  citado es legible sin ambigüedad.
- Cita: pdf 44 = libro 42 (pie de página impreso: "42 | Capítulo 2 | Crear
  un personaje").
