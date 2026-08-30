# Informe verificador V4

Método: renderizado con `pdftoppm -r 170` de las páginas pdf 313, 314 y 318 (Manual del Jugador 2024, ES) y lectura visual directa de las imágenes PNG resultantes. No se ha usado `pdftotext` ni conocimiento previo, solo lo visible en cada imagen.

Confirmación de paginación: la página pdf 313 lleva el folio impreso "311" (CAPÍTULO 7 | CONJUROS), la pdf 314 lleva "312" y la pdf 318 lleva "316", coincidiendo con el offset indicado (página_pdf = página_libro + 2).

## Pregunta 1 — Muro de espinas, tipo de daño en los dos momentos (pdf 313 = libro 311)

- Momento 1 (al aparecer el muro): "Cuando aparezca el muro, todas las criaturas situadas en su área hacen una tirada de salvación de Destreza; sufrirán 7d8 de daño perforante si la fallan o la mitad de daño si la superan."
- Momento 2 (al entrar en un espacio del muro o terminar el turno en él): "Además, la primera vez que una criatura entre en un espacio del muro o termine su turno allí, realizará una tirada de salvación de Destreza; sufrirá 7d8 de daño cortante si la falla o la mitad del daño si la supera"

Respuesta: en el primer momento el daño es **perforante**; en el segundo momento el daño es **cortante**.

## Pregunta 2 — Muro de espinas, párrafo "Con un espacio de conjuro de nivel superior" (pdf 313 = libro 311)

Cita literal completa: "Con un espacio de conjuro de nivel superior. Los dos tipos de daño aumentan en 1d8 por cada nivel por encima de 6 que tenga el espacio."

## Pregunta 3 — Muro de fuerza, excepción nombrada que destruya/elimine el muro (pdf 314 = libro 312)

Cita literal: "Nada puede atravesar el muro físicamente. Es inmune a todo el daño y no se puede eliminar mediante *disipar magia*. Sin embargo, un conjuro *desintegrar* destruye el muro al instante."

Respuesta: sí, existe una excepción nombrada: el conjuro **desintegrar**, que "destruye el muro al instante".

## Pregunta 4 — Palabra de poder: aturdir, estado impuesto (pdf 318 = libro 316)

Cita literal: "Abrumas la mente de una criatura que puedas ver dentro del alcance. Si el objetivo tiene 150 puntos de golpe o menos, tendrá el estado de aturdido. De lo contrario, su velocidad será 0 hasta el principio de tu siguiente turno."

Respuesta: el estado exacto que impone es **aturdido** ("tendrá el estado de aturdido"). En toda la página (incluido el bloque completo de este conjuro) no aparece en ningún momento la palabra "paralizado" ni "parálisis"; el único estado nombrado en el conjuro es "aturdido" (y también se menciona el estado "derribado", pero en el conjuro Orden imperiosa, no en Palabra de poder: aturdir).

## Extras / ilegible

- No se ha detectado ningún problema de legibilidad en las tres páginas renderizadas a 170 dpi; el texto es nítido y completo en las tres imágenes.
- De paso, en la página pdf 318 (libro 316) se observa que el conjuro "Palabra de poder: aturdir" también especifica una tirada de salvación de recuperación: "El objetivo aturdido hace una tirada de salvación de Constitución al final de cada uno de sus turnos y, si tiene éxito, se librará del estado." (dato no solicitado explícitamente, pero relevante al estado impuesto).
- En la página pdf 314 (libro 312), el conjuro Muro de fuerza también indica expresamente: "Es inmune a todo el daño y no se puede eliminar mediante *disipar magia*", lo cual complementa (sin contradecir) la excepción de *desintegrar* citada en la pregunta 3.
