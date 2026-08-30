# Auditoría de conjuros — lote 2

Agente: agente-J · fecha: 2026-08-21
Páginas leídas: pdf 261, 262, 263, 264, 267, 268, 269, 271, 272, 273, 274, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 289
Conjuros revisados: 22 de 22

## Hallazgos

### Conjurar lluvia de flechas · pdf 263
- **Campo:** componentes (coste / consume_material)
- **Dice el JSON:** `componentes.coste: "1 pc"`, `componentes.consume_material: true`
- **Dice la página:** «Componentes: V, S, M (un arma cuerpo a cuerpo o a distancia que valga al menos 1 pc)» — no dice «se consume». El mismo patrón de texto en «Conjurar descarga de proyectiles» (pdf 261, misma página) sí está codificado correctamente en el JSON como `coste: null, consume_material: false`. La frase «que valga al menos 1 pc» es un umbral de valor del arma usada (que no se pierde), no un coste que se gasta al lanzar el conjuro.
- **Gravedad:** media (afecta a la gestión de inventario/material, no al resultado directo del conjuro en combate)

### Desintegrar · pdf 271
- **Campo:** descripción
- **Dice el JSON:** «...recibirá 10d6 + 40 de daño de fuerza. Si este daño reduce sus puntos de golpe a 0. La criatura solo puede ser devuelta a la vida mediante un conjuro deseo o resurrección verdadera.»
- **Dice la página:** «...recibirá 10d6 + 40 de daño de fuerza. Si este daño reduce sus puntos de golpe a 0, **la criatura y todos los objetos no mágicos que vista o lleve quedarán reducidos a un polvo gris.** La criatura solo puede ser devuelta a la vida mediante un conjuro deseo o resurrección verdadera.»
- **Gravedad:** alta (falta una cláusula mecánica completa: qué pasa con la criatura y su equipo no mágico al llegar a 0 PG)

### Espada de Mordenkainen · pdf 283
- **Campo:** componentes (consume_material)
- **Dice el JSON:** `componentes.coste: "250 po"`, `componentes.consume_material: true`
- **Dice la página:** «Componentes: V, S, M (una espada en miniatura que valga al menos 250 po)» — no dice «que se consume como parte del conjuro» (a diferencia de otros conjuros de esta misma página y libro, como *Consagrar* o *Festín de héroes*, que sí llevan esa frase explícita). El coste de 250 po es correcto, pero el componente NO se consume: es un foco reutilizable.
- **Gravedad:** media

### Flecha ácida de Melf · pdf 286
- **Campo:** nombre (tilde)
- **Dice el JSON:** `"nombre": "Flecha acida de Melf"` (sin tilde en «acida»)
- **Dice la página:** «FLECHA ÁCIDA DE MELF» (con tilde)
- **Gravedad:** baja (solo tilde, pero se señala explícitamente porque el encargo pidió comprobar este caso en particular)

### Fuente de la luz lunar · pdf 287
- **Campo:** nombre
- **Dice el JSON:** `"nombre": "Fuente de la luz lunar"`
- **Dice la página:** «FUENTE DE LUZ LUNAR» (sin el artículo «la»)
- **Gravedad:** baja (nombre propio, pero es un error de transcripción, no solo de tilde/mayúscula — sobra una palabra)

## Revisados sin hallazgo
- Conjurar descarga de proyectiles (pdf 261)
- Cordón de flechas (pdf 267)
- Corona de la locura (pdf 267)
- Curar heridas (pdf 269)
- Disco flotante de Tenser (pdf 273)
- Duelo forzado (pdf 276)
- Enlace telepático de Rary (pdf 279)
- Enredadera (pdf 279-280)
- Entender idiomas (pdf 280) — confirmado `ritual: true` correcto, «Tiempo de lanzamiento: Acción o ritual»
- Esfera congelante de Otiluke (pdf 281-282)
- Esfera elástica de Otiluke (pdf 282)
- Estática sináptica (pdf 284)
- Festín de héroes (pdf 285) — confirmado `consume_material: true` correcto («se consume como parte del conjuro»)
- Fingir muerte (pdf 285) — confirmado `ritual: true` correcto, «Tiempo de lanzamiento: Acción o ritual»
- Flecha de relámpago (pdf 286) — mecánica y campos correctos (el `tiempo_lanzamiento` del JSON es una versión abreviada de la frase completa de la página, pero conserva el requisito mecánico clave)
- Fragmento mental (pdf 287)
- Golpe de viento acerado (pdf 289)

## Dudas / ilegible
- Festín de héroes (pdf 285): el campo `coste` del JSON es `"1000 po*"` (con asterisco). La página solo dice «1000 po», sin ningún símbolo. No lo marco como hallazgo porque no cambia el valor ni el sentido, pero podría ser un artefacto de la conversión del CSV que convenga revisar.

## Resumen
22 de 22 conjuros revisados. 5 hallazgos: 2 de mecánica/componentes (Conjurar lluvia de flechas, Espada de Mordenkainen), 1 de descripción incompleta (Desintegrar — gravedad alta), 2 de nombre propio mal transcrito (Flecha acida de Melf sin tilde, Fuente de la luz lunar con «la» de más). Los dos casos marcados como ritual en este lote (Entender idiomas, Fingir muerte) están correctamente codificados.
