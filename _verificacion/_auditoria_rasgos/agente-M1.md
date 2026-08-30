# Auditoría de descripciones (Fase 13p) — lote M1

Agente: M1 · fecha: 2026-08-29
Páginas leídas: pdf 243, 249, 261, 276, 289, 313, 326, 327, 344
Conjuros revisados: 10 de 10

## Hallazgos

### Golpe de viento acerado · pdf 289
- **Campo:** material
- **Modo de fallo:** otro (dato de coste omitido)
- **Dice la base:** `componentes.coste: null`
- **Dice la página:** «Componentes: S, M (un arma cuerpo a cuerpo que valga al menos 1 pp)» — cita textual confirmada con recorte a 300 dpi
- **Gravedad:** media (el manual exige que el arma valga al menos 1 pieza de platino; la base no registra ese requisito, a diferencia de otros conjuros con coste de material como *Impacto certero* que sí lo llevan en `coste`)

## Revisados sin hallazgo
- Alterar los recuerdos
- Aura mágica de Nystul
- Conjurar elemental
- Don de lenguas
- Moldear la piedra
- Rayo abrasador
- Puerta dimensional
- Ver invisibilidad
- Vigor arcano

(Golpe de viento acerado tiene hallazgo arriba; sus campos `nombre`, `descripcion`, `clases`, `tirada` y `resumen` no presentan problema.)

Para cada uno de los 10 se comprobó, contra la imagen de la página:
- **nombre**: las diez cabeceras transcriben letra a letra el nombre de la base. Sin erratas.
- **descripcion**: en todos los casos el texto de la página se corresponde en contenido, cifras (dados, número de objetivos, días de recuerdo, etc.) y nombres de tabla/opciones con la `descripcion` de la base. No se encontró ningún párrafo de reglas completo que falte (los apartados «Con un espacio de conjuro de nivel superior» presentes en la página están presentes en la base, y los ausentes en la página también están ausentes en la base). No se encontró contaminación con el conjuro vecino ni regla de la edición 2014 ni regla inventada.
  - Nota menor sin gravedad de hallazgo: en *Alterar los recuerdos* la base omite la frase «Su mente llenará cualquier hueco que falte en los detalles de tu descripción», presente en la página; es densidad de resumen, no un cambio de regla, así que no se lista como hallazgo.
- **clases**: las diez listas coinciden una a una con el paréntesis de la cabecera (incluidos los casos de listas largas: *Don de lenguas* con 5 clases y *Puerta dimensional* con 4, ambas completas en la base).
- **tirada**: coincide con lo que pide la página en 9 de 10 casos. El caso restante (*Conjurar elemental*) se documenta en Dudas, no en Hallazgos, según la instrucción del briefing.
- **resumen**: ninguno de los diez contradice la `descripcion` ni la página.
- **material** (paréntesis tras la M): el registro no guarda el texto libre del material (solo `coste`), así que solo se audita `coste`. De los cinco conjuros del lote con componente M (*Aura mágica de Nystul*, *Don de lenguas*, *Golpe de viento acerado*, *Moldear la piedra*, *Ver invisibilidad*), cuatro no llevan coste en po/pp impreso en la página y la base los guarda correctamente como `null`. El quinto, *Golpe de viento acerado*, sí lleva coste («al menos 1 pp») y la base lo tiene en `null` — ver Hallazgos.

## Unidades
- pdf 243 (Alterar los recuerdos): solo métricas.
- pdf 249 (Aura mágica de Nystul): solo métricas.
- pdf 261 (Conjurar elemental): solo métricas.
- pdf 276 (Don de lenguas): solo métricas.
- pdf 289 (Golpe de viento acerado): solo métricas. (Aparece «1 pp» en el material, pero es una pieza de platino, no una unidad de distancia; no cuenta como «pies».)
- pdf 313 (Moldear la piedra): solo métricas.
- pdf 326 (Puerta dimensional / Rayo abrasador, cabecera): solo métricas.
- pdf 327 (Rayo abrasador, cuerpo): solo métricas.
- pdf 344 (Ver invisibilidad / Vigor arcano): solo métricas.

Ninguna de las nueve páginas leídas en este lote imprime «pies», «pulgadas», «yardas», «millas» ni «pies cuadrados» en ningún punto del cuerpo de texto. Todas las distancias, radios, alturas y volúmenes aparecen solo en metros, centímetros o metros cuadrados/cúbicos. Las equivalencias «X m / Y pies» que trae `descripcion` en la base (p. ej. «1,5 m / 5 pies» en *Conjurar elemental*, *Moldear la piedra*, *Puerta dimensional* y *Golpe de viento acerado*) son, en las nueve páginas de este lote, añadido nuestro: el manual castellano no las imprime.

## Dudas / ilegible

### Conjurar elemental · pdf 261
- `tirada` dice «Directo», pero la descripción exige una tirada de salvación de Destreza tanto al entrar/empezar turno junto al espíritu como, repetida, al principio de cada turno de la criatura apresada. Cita de la página: «puedes obligarla a hacer una tirada de salvación de Destreza si el espíritu no tiene ninguna criatura apresada. Si la falla, el objetivo sufrirá 8d8 de daño... Al principio de cada uno de sus turnos, el objetivo apresado repite la tirada de salvación.» Se marca en Dudas, no en Hallazgos, según la instrucción del briefing sobre el valor «Directo».

No hubo texto ilegible en ninguna de las páginas del lote (renderizadas a 170 dpi, con un recorte adicional a 300 dpi para confirmar el coste de material de *Golpe de viento acerado*).
