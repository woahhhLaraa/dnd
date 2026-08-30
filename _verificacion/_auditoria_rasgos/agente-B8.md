# Auditoría de descripciones (Fase 13p) — lote B8

Agente: B8 · fecha: 2026-08-29
Páginas leídas: pdf 337, 338, 339, 340, 341 (y 342 para comprobar que ningún conjuro del lote se cortaba)
Conjuros revisados: 14 de 14

## Hallazgos

### Teletransporte · pdf 338
- **Campo:** descripcion
- **Modo de fallo:** 2 (regla de 2014 filtrada) / 7 (regla inventada que tapa a la real)
- **Dice la base:** «Si eliges un objeto como objetivo, debe caber completamente dentro de un cubo de 3 metros, y no puede ser sostenido ni transportado por una criatura involuntaria.»
- **Dice la página:** «Si el objetivo es un objeto, debe ser Grande o más pequeño y no puede llevarlo o vestirlo una criatura no voluntaria.»
- **Gravedad:** alta (cambia el criterio de qué objetos son válidos: la edición de 2024 usa la categoría de tamaño «Grande o más pequeño», no un cubo de 3 m — que es, además, la conversión casi exacta del «cubo de 10 pies» de la regla de 2014).

### Teletransporte · pdf 338
- **Campo:** descripcion
- **Modo de fallo:** 5 (nombre de tabla inventado)
- **Dice la base:** «El DM tira 1d100 y consulta la tabla de accidentes.»
- **Dice la página:** «Tu DM tira 1d100 y consulta la tabla "Resultado del teletransporte" y las explicaciones que la siguen.» (así se titula la tabla impresa en la misma página)
- **Gravedad:** media (el nombre de tabla no existe en el manual; dificulta encontrarla, aunque no cambia el resultado mecánico).

### Terremoto · pdf 339
- **Campo:** descripcion
- **Modo de fallo:** otro (terminología: «salvamento» en vez de «tirada de salvación» — patrón ya detectado en otros lotes)
- **Dice la base:** «cada criatura en el suelo del área hace un salvamento de Destreza»
- **Dice la página:** «todas las criaturas que haya en el suelo en la zona deberán hacer una tirada de salvación de Destreza»
- **Gravedad:** baja (terminología, no cambia la mecánica, pero es el patrón de error ya señalado como hallazgo en el encargo).

### Terremoto · pdf 339
- **Campo:** descripcion
- **Modo de fallo:** 4 (cifra/mecánica cambiada) / 7 (regla inventada)
- **Dice la base:** «Grietas. Se abren 1d6 fisuras **por turno**, de 3 m / 10 pies de ancho…»
- **Dice la página:** «Grietas. Se abre un total de 1d6 fisuras en la zona del conjuro **al final del turno en que lo lances**. Tú eliges la ubicación de las grietas…»
- **Gravedad:** alta (la página dice que las grietas se abren UNA SOLA VEZ, al final del turno de lanzamiento; la base da a entender que se abren cada turno, lo que multiplica muchísimo el daño y la duración del efecto).

### Terremoto · pdf 339
- **Campo:** descripcion
- **Modo de fallo:** 5 (nombre de apartado inventado)
- **Dice la base:** «**Temblor.** Inflige 50 de daño contundente a estructuras en contacto con el suelo…»
- **Dice la página:** «**Estructuras.** El temblor causa 50 de daño contundente a cualquier estructura que esté en contacto con el suelo de la zona…» (el efecto se llama «Estructuras»; «temblor» es una palabra dentro del texto, no el nombre del apartado)
- **Gravedad:** media (nombre de epígrafe incorrecto; el conjuro solo tiene dos efectos con nombre — Grietas y Estructuras — y la base rebautiza el segundo).

### Tormenta de la venganza · pdf 341
- **Campo:** descripcion
- **Modo de fallo:** otro (terminología: «salvamento» en vez de «tirada de salvación»)
- **Dice la base:** «cada criatura bajo la nube hace un salvamento de Constitución»
- **Dice la página:** «Todas las criaturas que estén debajo de ella cuando aparezca deberán superar una tirada de salvación de Constitución»
- **Gravedad:** baja (mismo patrón terminológico que en Terremoto).

### Tormenta de la venganza · pdf 341
- **Campo:** descripcion
- **Modo de fallo:** 3 (detalle de regla que falta, dentro de un párrafo por lo demás correcto)
- **Dice la base:** «Ráfagas y lluvia helada, cada criatura recibe 1d6 daño de frío, el área se vuelve terreno difícil y ataques con armas a distancia son imposibles, el fuerte viento sopla por el área.»
- **Dice la página:** «Turnos 5 a 10. […] Todas las criaturas que estén allí sufren 1d6 de daño de frío. Hasta que el conjuro termine, la zona es terreno difícil **y está muy oscura**. Además, es imposible hacer ataques con armas a distancia…»
- **Gravedad:** media (omite que la zona queda muy oscura durante los turnos 5-10, un efecto de visibilidad con consecuencias reales en mesa: oscuridad, sigilo, conjuros con requisito de visión).

## Revisados sin hallazgo
- Taumaturgia (pdf 337) — descripción, clases y efectos (Jugar con fuego, Mano invisible, Ojos alterados, Sonido fantasmal, Temblores, Voz atronadora) cuadran con la página.
- Telaraña (pdf 337) — descripción cuadra con la página en todo su contenido; ver `## Unidades` sobre las conversiones a pies. `tirada: "Directo"` con salvación de Destreza en la descripción → ver Dudas.
- Telequinesis (pdf 337-338) — descripción cuadra con la página (Criatura / Objeto). `tirada: "Directo"` con salvación de Fuerza en la descripción → ver Dudas.
- Terreno alucinatorio (pdf 339-340) — descripción cuadra con la página.
- Terror (pdf 340) — descripción prácticamente verbatim a la página.
- Terror abyecto (pdf 340) — descripción prácticamente verbatim a la página.
- Toque helado (pdf 340) — descripción y mejora de truco verbatim a la página.
- Toque vampírico (pdf 340) — descripción y «con espacio de nivel superior» verbatim a la página.
- Tormenta de aguanieve (pdf 341) — descripción cuadra con la página. `tirada: "Directo"` con salvación de Destreza → ver Dudas.
- Tormenta de fuego (pdf 341) — descripción cuadra con la página.
- Tormenta de hielo (pdf 341) — descripción cuadra con la página. `tirada: "Directo"` con salvación de Destreza → ver Dudas.

Nombres (`nombre`): las 14 cabeceras impresas coinciden letra a letra con el campo `nombre` de la base. Ninguna errata de nombre en este lote.

`clases`: en los 14 conjuros la lista de la base coincide, una a una, con el paréntesis de la cabecera de la página.

`resumen`: en los 14 conjuros el resumen no contradice la página (son descriptivos genéricos que no chocan con el texto).

## Unidades
- pdf 337: solo métricas. No aparece «pies», «pulgadas», «yardas» ni «millas» en ningún punto de la página (Taumaturgia, Telaraña, Telepatía, inicio de Telequinesis). Todas las cifras impresas son en metros o "cas" no aparece tampoco — solo metros.
- pdf 338: solo métricas. Fin de Telequinesis y toda la Teletransporte (incluida la tabla «Resultado del teletransporte»); ninguna cifra en pies/pulgadas/yardas/millas.
- pdf 339: solo métricas. Fin de Teletransporte (incluye «2d12 × 1,5 km»), Tentáculos negros de Evard, Terremoto completo, inicio de Terreno alucinatorio. Ninguna cifra imperial impresa.
- pdf 340: solo métricas. Fin de Terreno alucinatorio, Texto ilusorio, Terror, Terror abyecto, Toque helado, Toque vampírico. Ninguna cifra imperial impresa (el «10 po» de Texto ilusorio son piezas de oro, no unidad de distancia).
- pdf 341: solo métricas. Tormenta de aguanieve, Tormenta de espinas, Tormenta de fuego, Tormenta de hielo, Tormenta de la venganza. Ninguna cifra imperial impresa.

**Veredicto del lote: cero apariciones de pies/pulgadas/yardas/millas en las cinco páginas (337-341).** El manual en castellano es íntegramente métrico en este tramo; las equivalencias en pies que trae `hechizos.json` (p. ej. Telaraña «6 m / 20 pies» y «1,5 m / 5 pies» ×2, Terremoto «30 m / 100 pies», etc.) son aritméticamente correctas pero **no están impresas en la página**: son un añadido de la base, no del manual. No las cuento como hallazgo porque son conversiones bien hechas (así lo pide el briefing), pero confirman el patrón de las «~550 equivalencias» que la Fase 13p quiere zanjar.

## Dudas / ilegible
- **Telaraña, Telequinesis, Tormenta de aguanieve, Tormenta de hielo:** `tirada: "Directo"` pero la descripción exige una tirada de salvación explícita (Destreza en Telaraña/Aguanieve/Hielo, Fuerza en Telequinesis). Según el briefing esto va contado aparte y no como hallazgo.
- **Tormenta de la venganza — campo `alcance`:** el texto guardado es `"1'5 km / 0.9 mi / 5000 cas"`, con apostrofe en vez de coma decimal («1'5» en lugar de «1,5»). El campo `alcance` no es parte de mi lote, pero lo señalo porque es una inconsistencia de formato frente al resto del fichero (que usa coma). La página imprime «1,5 km» con coma.
- Ninguna imagen resultó ilegible; todas las páginas se leyeron a 170-300 dpi sin problema.
