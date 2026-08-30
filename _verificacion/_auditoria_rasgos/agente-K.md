# Auditoría de conjuros — lote 3

Agente: agente-K · fecha: 2026-08-21
Páginas leídas: pdf 290, 291, 292-293, 297, 298, 299, 300, 302, 303, 304, 305, 306, 309-310, 311, 312, 313, 316, 317
Conjuros revisados: 23 de 23

## Hallazgos

**Nota sobre el patrón de `consume_material` en los ocho conjuros «Invocar…»:** en pdf 306 (Jaula de fuerza, fuera de mi lote) la página SÍ usa expresamente la fórmula «que se consume como parte del conjuro» para un material con coste. Eso confirma que el manual marca explícitamente cuándo un material se consume, y que su ausencia en los ocho «Invocar…» de mi lote no es un descuido de redacción: la base los da todos por consumidos y la página no lo dice en ninguno.

### Insecto gigante · pdf 297
- **Campo:** descripción
- **Dice el JSON:** «Acciones: Ataca = nivel conjuro (redondeado hacia abajo).»
- **Dice la página:** «Ataque múltiple. El insecto realiza una cantidad de ataques igual a la mitad del nivel de este conjuro (redondeado hacia abajo).»
- **Gravedad:** alta (cambia el resultado en mesa: el JSON omite «la mitad de», duplicando el número de ataques que hace la criatura invocada)

### Invocar aberración · pdf 298
- **Campo:** componentes.consume_material
- **Dice el JSON:** «consume_material: true» (coste "400 po")
- **Dice la página:** «M (un tentáculo en salmuera y un globo ocular en un vial con incrustaciones de platino que valga al menos 400 po)» — no aparece la frase «que se consume» ni equivalente en el paréntesis material.
- **Gravedad:** media (afecta si el material se gasta tras lanzar el conjuro; a confirmar si se repite en el resto de conjuros «Invocar…», ver más abajo)

### Invocar autómata · pdf 299
- **Campo:** componentes.consume_material
- **Dice el JSON:** «consume_material: true» (coste "400 po")
- **Dice la página:** «M (una caja de seguridad que valga al menos 400 po)» — no aparece «que se consume» ni equivalente.
- **Gravedad:** media (mismo patrón que Invocar aberración)

### Invocar bestia · pdf 300
- **Campo:** componentes.consume_material
- **Dice el JSON:** «consume_material: true» (coste "200 po")
- **Dice la página:** «M (una pluma, un poco de pelaje y cola de pez dentro de una bellota bañada en oro que valga al menos 200 po)» — no aparece «que se consume».
- **Gravedad:** media (mismo patrón)

### Orbe cromático · pdf 317
- **Campo:** componentes.consume_material
- **Dice el JSON:** «consume_material: true» (coste "50 po")
- **Dice la página:** «M (un diamante que valga al menos 50 po)» — no aparece «que se consume».
- **Gravedad:** media (mismo patrón que los ocho «Invocar…» y Mansión magnífica de Mordenkainen)

### Mansión magnífica de Mordenkainen · pdf 311
- **Campo:** componentes.consume_material
- **Dice el JSON:** «consume_material: true» (coste "15 po")
- **Dice la página:** «M (una puerta en miniatura que valga al menos 15 po)» — no aparece «que se consume».
- **Gravedad:** media (mismo patrón detectado en los ocho «Invocar…»; ver nota de control arriba)

### Mano de Bigby · pdf 309-310
- **Campo:** descripción
- **Dice el JSON:** «...Mano apresadora.\tMano contundente. Mano interpuesta. \nPuño cerrado. (Revisar efectos en el MdJ)...»
- **Dice la página:** el texto completo de los cuatro efectos está desarrollado, p. ej. «Puño cerrado. La mano golpea a un objetivo a 1,5 m o menos de ella. Haz un ataque de conjuro cuerpo a cuerpo. Si acierta, el objetivo recibe 5d8 de daño de fuerza.» y «Mano interpuesta. La mano te proporciona cobertura media contra ataques y otros efectos que se originen en su espacio o intenten atravesarla. Además, ese espacio se considera terreno difícil para tus enemigos.» (más «Mano apresadora» y «Mano contundente», ya presentes en el JSON antes del corte).
- **Gravedad:** alta (faltan por completo las reglas de dos de los cuatro efectos del conjuro; el JSON incluso deja una nota literal «Revisar efectos en el MdJ» en vez de la transcripción)
- Nota de control: Alcance «36 m» y Duración «Concentración, hasta 1 minuto» sí coinciden con el JSON, como se esperaba.

### Invocar muerto viviente · pdf 305
- **Campo:** componentes.consume_material
- **Dice el JSON:** «consume_material: true» (coste "300 po")
- **Dice la página:** «M (una calavera bañada en oro que valga al menos 300 po)» — no aparece «que se consume».
- **Gravedad:** media (mismo patrón)

### Invocar infernal · pdf 304
- **Campo:** componentes.consume_material
- **Dice el JSON:** «consume_material: true» (coste "600 po")
- **Dice la página:** «M (un vial con sangre que valga al menos 600 po)» — no aparece «que se consume».
- **Gravedad:** media (mismo patrón)

### Invocar feérico · pdf 303
- **Campo:** componentes.consume_material
- **Dice el JSON:** «consume_material: true» (coste "300 po")
- **Dice la página:** «M (una flor bañada en oro que valga al menos 300 po)» — no aparece «que se consume».
- **Gravedad:** media (mismo patrón)

### Invocar elemental · pdf 302
- **Campo:** componentes.consume_material
- **Dice el JSON:** «consume_material: true» (coste "400 po")
- **Dice la página:** «M (aire, un guijarro, ceniza y agua dentro de un vial con incrustaciones de oro que valga al menos 400 po)» — no aparece «que se consume».
- **Gravedad:** media (mismo patrón)

### Invocar celestial · pdf 300
- **Campo:** componentes.consume_material
- **Dice el JSON:** «consume_material: true» (coste "500 po")
- **Dice la página:** «M (un relicario que valga al menos 500 po)» — no aparece «que se consume».
- **Gravedad:** media (mismo patrón)

## Revisados sin hallazgo
- Guardia de cuchillas · pdf 290
- Hablar con las plantas · pdf 291
- Hambre de Hadar · pdf 292-293
- Invocación instantánea de Drawmij · pdf 298
- Látigo de espinas · pdf 306
- Manto del cruzado · pdf 311
- Mastín fiel de Mordenkainen · pdf 312
- Mover la tierra · pdf 313
- Nube apestosa · pdf 316
- Nube de dagas · pdf 316
- Ola destructora · pdf 317

## Dudas / ilegible

Ninguna. Todas las páginas de mi asignación se leyeron con claridad a 170 dpi (más un par de recortes a mayor zoom para confirmar el texto exacto del paréntesis de componentes material). No hubo texto ilegible ni ambigüedad de lectura en ningún conjuro del lote.
