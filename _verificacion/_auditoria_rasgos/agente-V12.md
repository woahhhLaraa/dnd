# Agente V12 — Verificación de parejas de conjuros con alto solapamiento textual

Fuente consultada: renders PNG a 170 dpi del `Manual_del_Jugador_2024.pdf` (páginas de libro 294, 298 y 316, leídas como imagen), contrastados con `hechizos.json`. Ningún fichero de la base ha sido editado.

## Pareja 1 — Inmovilizar persona / Inmovilizar monstruo (pdf 296, libro 294)

### Transcripción de la página (libro 294)

**INMOVILIZAR PERSONA**
*Encantamiento de nivel 2 (bardo, brujo, clérigo, druida, hechicero, mago)*
- Tiempo de lanzamiento: Acción
- Alcance: 18 m
- Componentes: V, S, M (un trozo de hierro recto)
- Duración: Concentración, hasta 1 minuto

Elige a un humanoide que puedas ver dentro del alcance. El objetivo deberá superar una tirada de salvación de Sabiduría o tendrá el estado de paralizado hasta que termine el conjuro. Al final de cada uno de sus turnos, el objetivo repite la tirada de salvación y, si tiene éxito, se librará del conjuro.
Con un espacio de conjuro de nivel superior. Puedes hacer objetivo a un humanoide adicional por cada nivel por encima de 2 que tenga el espacio.

**INMOVILIZAR MONSTRUO**
*Encantamiento de nivel 5 (bardo, brujo, hechicero, mago)*
- Tiempo de lanzamiento: Acción
- Alcance: 27 m
- Componentes: V, S, M (un trozo de hierro recto)
- Duración: Concentración, hasta 1 minuto

Elige a una criatura que puedas ver dentro del alcance. El objetivo deberá superar una tirada de salvación de Sabiduría o tendrá el estado de paralizado hasta que termine el conjuro. Al final de cada uno de sus turnos, el objetivo repite la tirada de salvación y, si tiene éxito, se librará del conjuro.
Con un espacio de conjuro de nivel superior. Puedes hacer objetivo a una criatura adicional por cada nivel por encima de 5 que tenga el espacio.

### Veredicto: **LEGÍTIMA**

El manual imprime ambos conjuros con un cuerpo de texto casi idéntico a propósito (son la versión de nivel 2 y la de nivel 5 del mismo efecto de parálisis). No hay indicio de copia contaminante.

### Diferencias reales y su conservación en la base

| Diferencia | Manual | ¿Conservada en `hechizos.json`? |
|---|---|---|
| Nivel | 2 vs 5 | Sí (`nivel: 2` / `nivel: 5`) |
| Clases | persona: bardo, brujo, clérigo, druida, hechicero, mago · monstruo: bardo, brujo, hechicero, mago (sin clérigo ni druida) | Sí, listas de `clases` coinciden exactamente |
| Alcance | 18 m vs 27 m | Sí (`alcance.metros: "18"` / `"27"`) |
| Tipo de objetivo | "un humanoide" vs "una criatura" | Sí, la `descripcion` de cada uno usa la palabra correcta |
| Umbral de mejora con espacio superior | "por encima de 2" vs "por encima de 5" | Sí, cada `descripcion` cita su propio umbral |

No se detectó ninguna diferencia perdida ni texto cruzado entre ambos registros.

## Pareja 2 — Invocar bestia / Invocar celestial (pdf 300, libro 298)

### Transcripción de la página (libro 298)

**INVOCAR BESTIA**
*Conjuración de nivel 2 (druida, explorador)*
- Tiempo de lanzamiento: Acción
- Alcance: 27 m
- Componentes: V, S, M (una pluma, un poco de pelaje y cola de pez dentro de una bellota bañada en oro que valga al menos 200 po)
- Duración: Concentración, hasta 1 hora

Invocas un espíritu bestial que se manifiesta en un espacio sin ocupar que puedas ver dentro del alcance y usa el perfil del **espíritu bestial**. Cuando lances el conjuro, elige un hábitat: tierra, mar o aire. La criatura se parecerá a un animal de tu elección de ese hábitat, lo que determinará ciertos detalles de su perfil. La criatura desaparecerá si sus puntos de golpe se reducen a 0 o si el conjuro termina.
La criatura se considera un aliado para tus aliados y para ti. En combate, la criatura comparte tu orden de iniciativa, pero su turno va justo después del tuyo, obedece tus órdenes verbales (no requiere acción) y, si no le das ninguna, realiza la acción de esquivar y usa su movimiento para evitar el peligro.
Con un espacio de conjuro de nivel superior. Usa el nivel del espacio de conjuro para determinar el nivel del conjuro en el perfil.

**INVOCAR CELESTIAL**
*Conjuración de nivel 5 (clérigo, paladín)*
- Tiempo de lanzamiento: Acción
- Alcance: 27 m
- Componentes: V, S, M (un relicario que valga al menos 500 po)
- Duración: Concentración, hasta 1 hora

Invocas un espíritu celestial que se manifiesta con una forma angelical en un espacio sin ocupar que puedas ver dentro del alcance y usa el perfil del **espíritu celestial**. Cuando lances el conjuro, elige defensor o vengador. Tu elección determinará ciertos detalles de su perfil. La criatura desaparecerá si sus puntos de golpe se reducen a 0 o si el conjuro termina.
La criatura se considera un aliado para tus aliados y para ti. En combate, la criatura comparte tu orden de iniciativa, pero su turno va justo después del tuyo, obedece tus órdenes verbales (no requiere acción) y, si no le das ninguna, realiza la acción de esquivar y usa su movimiento para evitar el peligro.
Con un espacio de conjuro de nivel superior. Usa el nivel del espacio de conjuro para determinar el nivel del conjuro en el perfil.

### Veredicto: **LEGÍTIMA**

Ambos "Invocar X" comparten literalmente la misma plantilla de texto de invocación (párrafo del aliado en combate idéntico palabra por palabra) por diseño del manual. El alcance (27 m) y la duración (1 hora, concentración) también son iguales en ambos — no es un error, el propio libro los imprime así.

### Diferencias reales y su conservación en la base

| Diferencia | Manual | ¿Conservada? |
|---|---|---|
| Nivel | 2 vs 5 | Sí |
| Clases | druida, explorador vs clérigo, paladín | Sí |
| Coste del componente material | 200 po (bellota bañada en oro) vs 500 po (relicario) | Sí (`componentes.coste`) |
| Elección al lanzar | hábitat (tierra/mar/aire) vs defensor/vengador | Sí, cada `descripcion` recoge la elección correcta |
| Criatura invocada | espíritu bestial vs espíritu celestial | Sí |

No se detectó pérdida de diferencias ni contaminación cruzada.

## Pareja 3 — Palabra de curación / Palabra de curación en masa (pdf 318, libro 316)

### Transcripción de la página (libro 316)

**PALABRA DE CURACIÓN**
*Abjuración de nivel 1 (bardo, clérigo, druida)*
- Tiempo de lanzamiento: Acción adicional
- Alcance: 18 m
- Componentes: V
- Duración: Instantáneo

Una criatura de tu elección que puedas ver dentro del alcance recupera una cantidad de puntos de golpe igual a 2d4 más tu modificador por aptitud mágica.
Con un espacio de conjuro de nivel superior. La curación aumenta en 2d4 por cada nivel por encima de 1 que tenga el espacio.

**PALABRA DE CURACIÓN EN MASA**
*Abjuración de nivel 3 (bardo, clérigo)*
- Tiempo de lanzamiento: Acción adicional
- Alcance: 18 m
- Componentes: V
- Duración: Instantáneo

Hasta seis criaturas de tu elección que puedas ver dentro del alcance recuperan una cantidad de puntos de golpe igual a 2d4 más tu modificador por aptitud mágica.
Con un espacio de conjuro de nivel superior. La curación aumenta en 1d4 por cada nivel por encima de 3 que tenga el espacio.

(Nota: el manual clasifica ambos conjuros como escuela "Abjuración" — no Evocación —, y así consta también en `hechizos.json`; coincide con el texto impreso, no es un error de la base.)

### Veredicto: **LEGÍTIMA**

Es el par con menor solapamiento (41 %) de los tres, y con razón: el manual solo repite literalmente la fórmula de curación base (2d4 + modificador) y la estructura de cabecera; el resto del texto (número de objetivos, escalado) ya difiere en el propio libro.

### Diferencias reales y su conservación en la base

| Diferencia | Manual | ¿Conservada? |
|---|---|---|
| Nivel | 1 vs 3 | Sí |
| Clases | bardo, clérigo, druida vs bardo, clérigo (sin druida) | Sí |
| Número de objetivos | "Una criatura de tu elección" vs "Hasta seis criaturas de tu elección" (con verbo en plural "recuperan") | Sí, cada `descripcion` lo recoge textualmente |
| Escalado con espacio superior | +2d4 por nivel por encima de 1 vs +1d4 por nivel por encima de 3 | Sí, cada `descripcion` cita su propia cantidad y umbral |

No se detectó pérdida de diferencias ni contaminación cruzada.

## Resumen

Las tres parejas son **LEGÍTIMAS**: el Manual del Jugador 2024 imprime realmente estos conjuros con plantillas de texto casi idénticas (son variantes de nivel superior del mismo efecto), y en los tres casos `hechizos.json` conserva correctamente todas las diferencias reales que el manual sí establece (nivel, clases, alcance u objetivo, coste de componente, número de criaturas afectadas y cifras/umbrales de escalado). No se ha encontrado ningún caso de texto copiado de un conjuro vecino ni ninguna diferencia real "comida" por la base.
