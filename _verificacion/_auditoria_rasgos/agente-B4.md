# Auditoría de descripciones (Fase 13p) — lote B4

Agente: B4 · fecha: 2026-08-29
Páginas leídas: pdf 321, 322, 323, 324 (más pdf 325 para comprobar el final de *Proyección astral*, cortado al final de pdf 324)
Conjuros revisados: 15 de 15

## Hallazgos

### Poliformar verdadero · pdf 322
- **Campo:** descripcion
- **Modo de fallo:** otro (mecánica alterada; parece mezclar reglas del conjuro *Polimorfar*, que sí termina al agotar los puntos de golpe temporales y sí "asume" el perfil físico completo de la forma)
- **Dice la base:** «Transformas una criatura u objeto que veas en otra criatura o en un objeto mientras dure tu concentración, hasta 0 puntos de golpe o muerte. […] Criatura a criatura: nueva forma con VD igual o menor, conserva alineamiento y personalidad, asume puntos de golpe de la forma, limitada por su anatomía, no puede hablar, lanzar conjuros ni usar equipo.»
- **Dice la página:** «Criatura en criatura. […] El perfil del objetivo se reemplaza por el perfil de la nueva forma, pero mantiene sus puntos de golpe, dados de puntos de golpe, alineamiento y personalidad. El objetivo obtiene una cantidad de puntos de golpe temporales igual a los puntos de golpe de la nueva forma. Estos puntos de golpe temporales se desvanecerán si conservas alguno cuando el conjuro termine.» — la página **no** dice en ningún momento que el conjuro termine si el objetivo llega a 0 puntos de golpe o si se le agotan los temporales (esa cláusula sí existe para *Polimorfar*, pdf 322, pero no aparece en el texto de *Poliformar verdadero*).
- **Gravedad:** alta (cambia el resultado en mesa: la base da a entender que el objetivo pierde sus propios puntos de golpe y los sustituye por los de la nueva forma, cuando en realidad los conserva y solo gana un colchón de puntos de golpe temporales)

### Poliformar verdadero · pdf 322
- **Campo:** descripcion
- **Modo de fallo:** 4 (detalle de regla cambiado)
- **Dice la base:** «Objeto a criatura: tamaño ≤ objeto y VD ≤ 9, amistosa contigo, actúa en tus turnos según tu decisión; permanente pierde control.»
- **Dice la página:** «Objeto en criatura. […] La criatura es amistosa contigo y tus aliados. En combate, sus turnos van inmediatamente después de los tuyos y obedece tus órdenes.»
- **Gravedad:** media (la página dice que la criatura actúa en su propio turno, inmediatamente después del tuyo, no «en tus turnos»; afecta al orden de iniciativa en mesa)

### Prohibición · pdf 324
- **Campo:** descripcion
- **Modo de fallo:** 6 (conversión de unidad falsa)
- **Dice la base:** «Prohibición crea una barrera que cubre 4000 m² / 13000 pies² hasta 9 m / 30 pies de altura […]»
- **Dice la página:** «Creas una protección contra los viajes mágicos que cubre una zona del suelo de 4000 m² hasta una altura de 9 m.» — la página no da la cifra en pies². Comprobación aritmética: 4000 m² equivalen a ≈ 43 000 pies² (factor de área 10,76 pies²/m²), no a 13 000. El SRD en inglés confirma «40,000 square feet» para este conjuro. 13 000 parece resultar de aplicar por error el factor lineal (3,28) en vez del factor de área.
- **Gravedad:** media (la cifra en metros, que es la que se usa en mesa, es correcta; el error está solo en la conversión auxiliar a pies², pero es una cifra objetivamente falsa)

### Presciencia · pdf 323
- **Campo:** resumen
- **Modo de fallo:** otro (el resumen no corresponde al efecto del conjuro; posible confusión con el conjuro vecino en la misma página, *Presencia regia de Yolande*)
- **Dice la base:** «Imponer presencia.»
- **Dice la página:** «Tocas a una criatura voluntaria y la dotas de una capacidad limitada de ver el futuro inmediato. Hasta que el conjuro termine, el objetivo tendrá ventaja en las pruebas con d20 y las demás criaturas tendrán desventaja en las tiradas de ataque contra él.» — no hay nada sobre «imponer presencia»; ese resumen encaja mejor con *Presencia regia de Yolande* (emanación que asusta/derriba), impresa justo al lado en la misma página.
- **Gravedad:** baja (campo `resumen`, no afecta a la mecánica jugada, pero es objetivamente incorrecto y con pinta de contaminación cruzada entre conjuros vecinos)

### Potenciar característica · pdf 323 — aviso del encargo, verificado sin hallazgo
- **Campo:** clases
- **Modo de fallo:** — (se pidió verificar expresamente una discrepancia detectada por script)
- **Cabecera transcrita literalmente:** «POTENCIAR CARACTERÍSTICA — Transmutación de nivel 2 (bardo, clérigo, druida, explorador, hechicero, mago)»
- **Dice la base:** `clases: ["Bardo", "Clérigo", "Druida", "Explorador", "Hechicero", "Mago"]`
- **Dice la página:** las mismas seis clases, mismo orden.
- **Conclusión:** no encuentro discrepancia entre la base y la página del manual. Las seis clases coinciden exactamente (y también coinciden con el SRD 5.2 en inglés: Bard, Cleric, Druid, Ranger, Sorcerer, Wizard). Si el script marcó una discrepancia, no la reproduce esta página; podría ser un falso positivo o estar comparando contra otra fuente. Lo dejo constatado tal y como se pidió, sin marcarlo como hallazgo porque la base sí coincide con el manual.

## Revisados sin hallazgo

- Perdición (pdf 321)
- Piedad con los moribundos (pdf 321)
- Piel robliza (pdf 321)
- Plegaria de curación (pdf 321-322)
- Poliformar (pdf 322)
- Portal (pdf 322)
- Prestidigitación (pdf 323-324)
- Prohibición — resto del conjuro aparte de la conversión en pies² (pdf 324)
- Protección contra el bien y el mal (pdf 324)
- Protección contra energía (pdf 324)
- Protección contra veneno (pdf 324)
- Proyección astral (pdf 324-325)

(Potenciar característica y Presciencia y Poliformar verdadero aparecen arriba, con hallazgo o con la verificación solicitada.)

## Dudas / ilegible

- **Poliformar verdadero** — campo `tirada`: la base dice `"Directo"`, pero la página dice «Una criatura no voluntaria puede hacer una tirada de salvación de Sabiduría y, si la supera, el conjuro no le afectará.» Según el criterio del encargo, esto se deja en dudas y no cuenta como hallazgo (decisión de diseño pendiente sobre el valor `Directo`).
- Nada ilegible en las páginas 321-325 a 170-300 ppp; todas las imágenes se leyeron con claridad suficiente para los campos auditados.
