# Auditoría de descripciones (Fase 13p) — lote M4

Agente: M4 · fecha: 2026-08-29
Páginas leídas: pdf 248, 254, 255, 266, 286, 287, 307, 322, 340
Conjuros revisados: 8 de 8

## Hallazgos

Ninguno. Los ocho conjuros del lote corresponden a su propia cabecera (nombre,
nivel, escuela y clases coinciden letra a letra con lo impreso), la
`descripcion` cubre el contenido de la página sin párrafos que falten, sin
cifras cambiadas y sin nombres de tabla inventados, `tirada` cuadra con lo que
pide la página, y `resumen` no contradice a la página en ningún caso.

## Revisados sin hallazgo

- **Asesino fantasmal** · pdf 248 — cabecera "Ilusionismo de nivel 4 (bardo,
  mago)" coincide con nivel/escuela/clases de la base. Descripción, párrafo de
  "Con un espacio de conjuro de nivel superior" y tirada (TdS Sab.) correctos.
- **Campo antimagia** · pdf 254-255 (descripción cortada al final de la 254,
  continúa en 255) — cabecera "Abjuración de nivel 8 (clérigo, mago)" correcta.
  Descripción completa cotejada con las dos páginas, sin párrafos que falten.
  Componente M "virutas de hierro" sin coste, consistente con `coste: null`.
  `tirada: "Directo"` correcto (la página no exige ninguna tirada de
  salvación).
- **Controlar el clima** · pdf 266 — cabecera "Transmutación de nivel 8
  (clérigo, druida, mago)" correcta. Los nombres de las tres tablas
  (Precipitaciones, Temperatura, Viento) coinciden exactamente con los
  impresos (este conjuro ya llevaba una `_nota_verificacion` de una pasada
  anterior, del 2026-08-22, y sigue correcto). `tirada: "Directo"` correcto.
- **Flecha de relámpago** · pdf 286 (descripción fluye del final de la columna
  izquierda al inicio de la derecha, es maquetación normal, no es
  contaminación) — cabecera "Transmutación de nivel 3 (explorador)" correcta.
  Descripción y párrafo de nivel superior coinciden con la página. Tirada
  "TdS Des." correcta (afecta a las criaturas cercanas al objetivo).
- **Forma gaseosa** · pdf 286-287 (descripción cortada al final de la 286,
  continúa en 287) — cabecera "Transmutación de nivel 3 (brujo, hechicero,
  mago)" correcta. Descripción completa cotejada, incluido el párrafo de
  nivel superior. `tirada: "Directo"` correcto (objetivo voluntario, sin
  tirada).
- **Llama permanente** · pdf 307 — cabecera "Evocación de nivel 2 (clérigo,
  druida, mago)" correcta. Componente M "polvo de rubí que valga al menos
  50 po, que se consume como parte del conjuro" coincide con `coste: "50 po*"`
  y `consume_material: true`. Descripción completa, sin diferencias de fondo.
  `tirada: "Directo"` correcto.
- **Polimorfar** · pdf 322 — cabecera "Transmutación de nivel 4 (bardo,
  druida, hechicero, mago)" correcta. Comprobado expresamente contra
  *Polimorfar verdadero*, impreso en la misma página (es uno de los pares de
  contaminación conocidos citados en el briefing): la `descripcion` de la
  base habla de transformar al objetivo en una **bestia** con VD igual o
  menor que el suyo, exactamente lo que dice el bloque de "Polimorfar" en la
  página, y no contiene nada de las secciones "Criatura en criatura",
  "Objeto en criatura" ni "Criatura en objeto" que sí aparecen bajo
  *Polimorfar verdadero*. No hay contaminación. Tirada "TdS Sab." correcta.
  (Ver duda sobre el `resumen` más abajo.)
- **Terror** · pdf 340 — cabecera "Ilusionismo de nivel 3 (bardo, brujo,
  hechicero, mago)" correcta. Descripción completa (incluida la segunda
  tirada de salvación al perder línea de visión) coincide con la página.
  Tirada "TdS Sab." correcta.

## Unidades

- pdf 248: solo métricas.
- pdf 254: solo métricas.
- pdf 255: solo métricas.
- pdf 266: solo métricas.
- pdf 286: solo métricas.
- pdf 287: solo métricas.
- pdf 307: solo métricas.
- pdf 322: solo métricas.
- pdf 340: solo métricas.

Ninguna de las nueve páginas leídas imprime una sola cifra en pies, pulgadas,
yardas o millas. Todas las distancias que aparecen en estas páginas están en
metros o kilómetros (p. ej. «3 m», «7,5 km», «9 m», «6 m», «18 m»). Las
equivalencias en pies que trae `hechizos.json` para estos conjuros (p. ej.
«3 m / 10 pies» en *Campo antimagia*, *Flecha de relámpago* y *Forma
gaseosa*; «6 m / 20 pies» en *Llama permanente*; «9 m / 30 pies» en *Terror*)
son, en todos los casos comprobados, un añadido nuestro y no algo impreso en
el manual — aritméticamente correctas, pero ausentes de la página. No se ha
encontrado ninguna excepción en este lote.

## Dudas / ilegible

- **Polimorfar · pdf 322 — campo `resumen`.** El valor actual es «Cambiar de
  forma.», que coincide letra por letra con el **nombre** de otro conjuro
  real del manual (*Cambiar de forma*, transmutación de nivel 9, impreso en
  la pdf 254 de este mismo lote). No contradice a la página — Polimorfar sí
  transforma al objetivo en otra forma — así que no lo cuento como hallazgo,
  pero la coincidencia exacta con el título de un conjuro distinto es
  llamativa y podría merecer revisión aparte. Comprobado que el `resumen`
  propio de *Cambiar de forma* es «La forma ya no es fija.» (no están
  intercambiados entre sí), así que no es una contaminación de resumen
  cruzada, solo una redacción que se solapa con un nombre ajeno.
