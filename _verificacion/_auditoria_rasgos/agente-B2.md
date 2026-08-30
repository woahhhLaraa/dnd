# Auditoría de descripciones (Fase 13p) — lote B2

Agente: B2 · fecha: 2026-08-27
Páginas leídas: pdf 313, 314, 315, 316, 317
Conjuros revisados: 12 de 12

## Hallazgos

### Muro de espinas · pdf 313
- **Campo:** descripcion
- **Modo de fallo:** otro (sustituye un dato real por una afirmación que lo tapa — próximo al modo 7 del aviso, aplicado a un tipo de daño en vez de a una prohibición/permiso)
- **Dice la base:** «Moverse a través de la pared cuesta 4 pies de movimiento por cada pie recorrido y la primera vez que una criatura entra o termina su turno allí hace otra tirada de Destreza, **recibiendo el mismo daño**. [...] Con ranura de nivel superior, **el daño** aumenta 1d8 por nivel por encima de 6.»
- **Dice la página:** «Cuando aparezca el muro [...] sufrirán **7d8 de daño perforante** si la fallan [...]. [...] la primera vez que una criatura entre en un espacio del muro o termine su turno allí, realizará una tirada de salvación de Destreza; sufrirá **7d8 de daño cortante** si la falla [...]. Con un espacio de conjuro de nivel superior. **Los dos tipos de daño** aumentan en 1d8 por cada nivel...»
- La página distingue expresamente dos tipos de daño distintos (perforante al aparecer, cortante al cruzarlo) — lo confirma la propia frase de escalado, «los dos tipos de daño». La base dice «el mismo daño», es decir, presenta el segundo golpe como perforante cuando en realidad es cortante. Esto cambia qué resistencias/inmunidades aplican en mesa.
- **Gravedad:** alta (cambia el resultado en mesa: un objetivo con resistencia a cortante pero no a perforante, o viceversa, recibe distinto daño según cuál de los dos tramos sea).

### Muro de fuerza · pdf 314
- **Campo:** resumen
- **Modo de fallo:** otro (el resumen contradice una excepción que la propia página deja explícita)
- **Dice la base (resumen):** «Nada puede atravesarlo ni romperlo.»
- **Dice la página:** «Nada puede atravesar el muro físicamente. Es inmune a todo el daño y no se puede eliminar mediante disipar magia. **Sin embargo, un conjuro desintegrar destruye el muro al instante.**»
- El resumen afirma sin matices que nada puede «romperlo», pero la página da una excepción concreta y nombrada (desintegrar). Es un hallazgo menor porque el campo es un resumen de sabor, pero contradice literalmente el texto.
- **Gravedad:** baja (no afecta a la `descripcion` mecánica, que sí recoge bien la excepción; solo el resumen es impreciso).

## Revisados sin hallazgo
- Moldear la piedra (pdf 313)
- Muro de fuego (pdf 313)
- Muro de hielo (pdf 314)
- Muro de viento (pdf 314-315)
- Muro prismático (pdf 315) — auditado con especial cuidado por el aviso del encargo: coteja la tabla «Capas prismáticas» fila por fila (las 7 filas, textos de daño y efectos adicionales) y el cuerpo del conjuro contra la página; **todo coincide palabra por palabra**, sin discrepancias.
- Nube aniquiladora (pdf 315-316)
- Nube incendiaria (pdf 316)
- Ofuscación (pdf 316) — clases de la cabecera «(bardo, brujo, druida, mago)» cotejadas una a una contra `["Bardo","Brujo","Druida","Mago"]`: coinciden. Descripción íntegra coincide palabra por palabra con la página.
- Ojo arcano (pdf 316-317)
- Ola atronadora (pdf 317) — se comprobó también hoy el resto de su texto tras la corrección reciente de Nube de dagas en la página vecina; no hay relación entre ambos conjuros y Ola atronadora coincide con la página en su totalidad.

## Dudas / ilegible

- **`tirada` = "Directo" con descripción que exige salvación** (ya contado aparte según el briefing, no lo cuento como hallazgo): Muro de espinas (TdS Destreza), Muro de fuego (TdS Destreza), Muro de hielo (TdS Destreza y TdS Constitución), Muro prismático (TdS Destreza por capa y TdS Constitución al acercarse), Nube aniquiladora (TdS Constitución), Nube incendiaria (TdS Destreza).
- **Muro de viento:** el campo `tirada` de la base es literalmente `"TdS Fue,"` (con una coma final suelta). El contenido es correcto — la página exige salvación de Fuerza — pero el valor tiene un carácter sobrante que parece un resto de edición. Lo señalo por si interesa limpiarlo, no como error de contenido.
- **Ola atronadora, resumen:** «Una explosión de fuerza.» La página nunca usa la palabra «fuerza» para este conjuro — el daño es de trueno («daño de trueno»), no de fuerza (que en D&D es un tipo de daño distinto y nombrado, «daño de fuerza»). No es una contradicción categórica (podría leerse como "fuerza" en sentido de potencia/energía, no como el tipo de daño reglamentario), así que lo dejo en dudas y no en hallazgos, pero podría inducir a confundir el tipo de daño.
- Todas las páginas se leyeron con nitidez suficiente (170 dpi); no hubo texto ilegible.
