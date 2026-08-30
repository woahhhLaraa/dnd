# Auditoría de descripciones (muestra 13o) — lote agente-S

Agente: agente-S · fecha: 2026-08-22
Páginas leídas: pdf 243, 244, 249, 262, 268, 269, 276, 294, 308, 316, 332, 335
Conjuros revisados: 10 de 10

## Hallazgos

### Aura sagrada · pdf 249
- **Campo:** descripcion
- **Dice la base:** «Con un toque, aplicas una ilusión a una criatura voluntaria o un objeto que no lleve ni vea nadie. Las criaturas obtienen el efecto de enmascarar y los objetos, el efecto de aura falsa, ambos descritos a continuación. El efecto durará hasta que termine el conjuro. Si lanzas el conjuro a diario sobre el mismo objetivo durante 30 días, la ilusión permanece hasta que sea disipada. Enmascarar (criaturas)... Aura falsa (objetos)...»
- **Dice la página:** «Hasta que termine el conjuro, emites un aura en una emanación de 9 m. Mientras permanezcan dentro, las criaturas de tu elección tienen ventaja en todas las tiradas de salvación y otras criaturas tienen desventaja en las tiradas de ataque contra ellas. Además, cuando un infernal o un muerto viviente acierte a una criatura afectada con una tirada de ataque cuerpo a cuerpo, el atacante deberá superar una tirada de salvación de Constitución o tendrá el estado de cegado hasta el final de su siguiente turno.»
- **Gravedad:** alta (cambia el resultado en mesa) — la `descripcion` almacenada no es la de *Aura sagrada*, sino la de *Aura mágica de Nystul* (pdf 249, mismo libro, columna izquierda). El texto real de *Aura sagrada* no aparece en la base. `nombre`, `resumen`, `clases` y `tirada` sí corresponden a *Aura sagrada*; solo la `descripcion` está intercambiada.

### Aura sagrada · pdf 249
- **Campo:** tirada
- **Dice la base:** «Directo»
- **Dice la página:** el conjuro real de *Aura sagrada* obliga a infernales/muertos vivientes que acierten a un objetivo protegido a superar una TdS de Constitución o quedar cegados.
- **Gravedad:** baja — anoto esto como duda relacionada, no como hallazgo aparte cerrado: no sé si el criterio del proyecto marca «Directo» cuando el efecto principal no exige salvación (aunque haya una salvación secundaria para terceros). Lo dejo también en «Dudas» para que se decida con el resto de la muestra.

### Crecimiento vegetal · pdf 268-269
- **Campo:** descripcion
- **Dice la base:** «...todas las plantas en un radio de 750 m / 0,46 yardas se fertilizan durante 365 días...»
- **Dice la página:** «Todas las plantas en un radio de 750 m centrado en un punto dentro del alcance estarán fertilizadas durante 365 días...» (la página no da ninguna conversión a yardas)
- **Gravedad:** baja — el valor en metros (750 m) es correcto y coincide con la página; el añadido «0,46 yardas» es una conversión de unidades errónea insertada por la base (750 m no son 0,46 yardas; si acaso, 750 m ≈ 0,46 millas). No contradice el dato de la página en sí, pero es una cifra falsa que la base agrega por su cuenta.

### Simulacro · pdf 335
- **Campo:** descripcion
- **Dice la base:** «Simulacro de hielo crea una copia de una bestia o humanoide que permanece a 3 m / 10 pies o menos de ti durante el lanzamiento...»
- **Dice la página:** «Creas un simulacro de una bestia o humanoide que permanezca a 3 m o menos de ti durante todo el tiempo de lanzamiento del conjuro...»
- **Gravedad:** baja — la base llama al efecto «Simulacro de hielo», una etiqueta que no aparece en la página (el conjuro se llama simplemente «Simulacro»; solo el material de creación es hielo o nieve). Puede ser un resto de redacción o una confusión con el nombre, no cambia la mecánica pero es un dato inventado que no está en la página.

### Simulacro · pdf 335
- **Campo:** descripcion
- **Dice la base:** «...obedece tus órdenes y actúa en su turno.»
- **Dice la página:** «...obedece tus órdenes y actúa en tu turno en combate.» (cita textual)
- **Gravedad:** media — la página dice que el simulacro actúa en el turno del lanzador («tu turno»), no que tenga turno propio («su turno»). Es un cambio de mecánica de iniciativa/turno que puede alterar el juego en mesa.

## Revisados sin hallazgo
- **Alzar a los muertos** (pdf 243-244): comprobé descripcion completa (incluye penalizador -4 y su reducción), clases (bardo, clérigo, paladín), tirada (Directo, sin salvación en la página) y resumen; todo coincide, incluyendo que el conjuro continúa en la pág. 244 y no le falta ningún párrafo (no tiene «nivel superior»).
- **Conjurar elementales menores** (pdf 262): descripcion, clases (druida, mago), tirada (Directo) y el párrafo «Con un espacio de conjuro de nivel superior» coinciden con la página.
- **Crecimiento vegetal** (pdf 268-269): descripcion (sobrecrecimiento y fertilización, ambos verificados incl. página 269 donde continúa el texto), clases (bardo, druida, explorador) y tirada (Directo) coinciden, salvo el detalle de unidades ya reportado arriba.
- **Dormir** (pdf 276): descripcion verificada íntegra frente a la mecánica 2024 (incapacitada → repetir TdS → inconsciente; termina con daño o zarandeo; exención para quienes no duermen), clases (bardo, hechicero, mago) y tirada (TdS Sab.) coinciden. Confirmado que NO usa el sistema de puntos de golpe de la edición 2014.
- **Ilusión menor** (pdf 294): descripcion completa (sonido e imagen, con los límites de 1,5 m y detección por Investigación) coincide; confirmado que la página NO trae párrafo de «Mejora de truco» y la base tampoco lo tiene; clases (bardo, brujo, hechicero, mago) y tirada (Directo) correctas.
- **Luces danzantes** (pdf 308): descripcion (hasta 4 luces, radio de luz tenue 3 m, movimiento de 18 m, distancia máxima entre luces 6 m) coincide con la página; confirmado que NO trae «Mejora de truco» en la página ni en la base; clases (bardo, hechicero, mago) y tirada (Directo) correctas.
- **Nube de oscurecimiento** (pdf 316): descripcion (esfera de niebla de 6 m, párrafo de nivel superior con +6 m por nivel) coincide con la página; clases (druida, explorador, hechicero, mago) y tirada (Directo) correctas.
- **Rociada de color** (pdf 332): descripcion verificada contra la mecánica 2024 (cono de 4,5 m, TdS Con., estado de cegadas hasta el final de tu siguiente turno; NO usa el total de PG de monstruos de la edición 2014); clases (bardo, hechicero, mago) y tirada (TdS Con.) coinciden.
- **Simulacro** (pdf 335): resto de la descripcion (creación, perfil con la mitad de PG, reparación a 100 po/PG durante descanso largo a 1,5 m, fin a 0 PG, destrucción del anterior al recastear) coincide; clases (mago) y tirada (Directo) correctas. (Ver hallazgos puntuales arriba sobre «Simulacro de hielo» y «actúa en su turno».)

## Dudas / ilegible
- **Aura sagrada — tirada:** dejo constancia de la duda sobre si «Directo» es la etiqueta correcta para un conjuro cuyo efecto principal no exige salvación del objetivo, pero que sí obliga a un tercero (el atacante infernal/muerto viviente) a hacer una TdS de Constitución. No decido si cuenta como hallazgo de campo `tirada`; lo dejo para que se evalúe junto con el hallazgo mayor de `descripcion` del mismo conjuro.
