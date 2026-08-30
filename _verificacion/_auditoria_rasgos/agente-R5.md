# Auditoría de descripciones (Fase 13p) — lote R5 (remuestreo de control)

Agente: R5 · fecha: 2026-08-29
Páginas leídas: pdf 325, 326, 327, 328, 329 (libro 323-327)
Conjuros revisados: 14 de 14

Nota de método: este es un remuestreo de control sobre un lote que otro agente
(B5) auditó con «0 hallazgos». No se ha abierto `agente-B5.md` ni ningún otro
informe. Auditoría hecha de cero, leyendo las imágenes renderizadas de las
páginas 325-329 del pdf con `pdftoppm -r 170` (y recortes a `-r 220` para
confirmar espacios en blanco al final de columna).

## Hallazgos

### Rayo nauseabundo · pdf 328 (libro 326)
- **Campo:** descripcion
- **Modo de fallo:** 7 (regla/texto de más que la página no trae) — aquí en
  sentido inverso a los ejemplos del briefing: no tapa una regla real, añade
  una que la página no da.
- **Dice la base:** «...Si acierta, el objetivo sufrirá 2d8 de daño de veneno
  y tendrá el estado de envenenado hasta el final de tu siguiente turno.
  Con un espacio de conjuro de nivel superior. El daño aumenta en 1d8 por
  cada nivel por encima de 1 que tenga el espacio.»
- **Dice la página:** el párrafo termina en «...y tendrá el estado de
  envenenado hasta el final de tu siguiente turno.» — **no hay ningún párrafo
  de «Con un espacio de conjuro de nivel superior»**. Tras esa frase queda
  espacio en blanco en la columna y luego el pie de página «326 · CAPÍTULO 7
  | CONJUROS». Comprobado dos veces con recortes a 220 dpi para descartar que
  el texto quedara cortado por el render; también se renderizó la página
  siguiente (pdf 329, libro 327) y esta empieza directamente en «Reencarnar»,
  sin ningún resto de Rayo nauseabundo.
- **Gravedad:** media (cambia el resultado en mesa si alguien lanza el
  conjuro con espacio de nivel superior: la base promete daño extra que la
  página no concede).

## Revisados sin hallazgo
Proyectar imagen, Proyectil mágico, Puerta dimensional, Purificar comida y
bebida, Ralentizar, Rayo abrasador, Ráfaga de viento, Rayo de escarcha, Rayo
de luna, Rayo debilitador, Rayo solar, Recado, Recluir.

(Rayo nauseabundo aparece arriba, en Hallazgos — el resto de sus campos,
nombre/clases/tirada/resumen/material, están correctos.)

Para los 14 conjuros se comprobó letra a letra la cabecera (nombre, escuela y
lista de clases entre paréntesis) y se cotejaron los conjuros de nombre
parecido impresos en la misma página unos contra otros para descartar
contaminación cruzada:
- Puerta arcana / Puerta dimensional (pdf 326): descripciones distintas y
  correctamente asignadas.
- Rayo de escarcha / Rayo de hechicería (pdf 327): descripciones distintas y
  correctamente asignadas (Rayo de hechicería no es de mi lote).
- Rayo de luna / Rayo debilitador / Rayo nauseabundo / Rayo solar (pdf 328):
  las cuatro entradas «Rayo X» tienen mecánicas y daños distintos y ninguna
  está cruzada con otra.

`clases` coteja correctamente contra el paréntesis de cabecera en los 14
casos (incluidas las listas largas: Puerta dimensional con 4 clases, Ráfaga
de viento con 4 clases, Rayo solar con 4 clases, Recado con 3 clases).

`material` (texto tras la M): el esquema de la base no guarda el texto
completo del paréntesis, solo `coste` y `consume_material`. En los 14 casos
esos dos campos son coherentes con lo impreso (p. ej. Recluir: página dice
«polvo de piedras preciosas que valga al menos 5000 po, que se consume como
parte del conjuro» → base `coste: "5000 po*"`, `consume_material: true`;
Ralentizar/Ráfaga de viento/Rayo de luna/Rayo solar/Recado tienen material
sin coste en oro y la base lleva `coste: null`, correcto).

## Unidades
- pdf 325 (libro 323): solo métricas. Proyectar imagen y Proyectil mágico no
  imprimen ninguna cifra en pies/pulgadas/yardas/millas.
- pdf 326 (libro 324): solo métricas. Puerta arcana, Puerta dimensional,
  Purificar comida y bebida, Ralentizar, Rayo abrasador y Ráfaga de viento no
  traen ninguna unidad imperial impresa.
- pdf 327 (libro 325): solo métricas. Cierre de Rayo abrasador, Rayo de
  escarcha y Rayo de hechicería, sin unidades imperiales.
- pdf 328 (libro 326): solo métricas. Rayo de luna, Rayo debilitador, Rayo
  nauseabundo, Rayo solar, Recado y el inicio de Recluir, sin unidades
  imperiales.
- pdf 329 (libro 327): solo métricas. Cierre de Recluir («1,5 km») y el resto
  de la página (Reencarnar, Regenerar, Relámpago, Relámpago en cadena,
  Reparar), sin unidades imperiales.

Ni una sola cifra en pies, pulgadas, yardas o millas aparece impresa en
ninguna de las cinco páginas leídas. Todas las conversiones «N m / M pies»
que lleva la base en este lote (Puerta dimensional, Ráfaga de viento, Rayo
de escarcha, Rayo de luna, Rayo solar, Recluir) son añadido nuestro; se
comprobó aritméticamente que son correctas (conversión estándar 1,5 m = 5
pies), pero no están en la página.

## Dudas / ilegible
- **Rayo de luna** (pdf 328) lleva `tirada: "Directo"`, pero su descripción
  exige explícitamente «todas las criaturas... realizan una tirada de
  salvación de Constitución». Según el briefing, si el único problema de un
  conjuro es que dice «Directo» con una descripción que pide salvación, va a
  Dudas y no a Hallazgos porque ya está contado aparte en la decisión de
  diseño pendiente sobre ese valor.
- **Rayo nauseabundo**: el campo `resumen` de la base es «Asco hecho rayo,»
  — termina en coma en vez de punto. No es hallazgo (no contradice la
  página, es un campo nuestro), pero lo anoto por si es una errata de
  redacción a limpiar aparte.
