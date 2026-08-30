# Auditoría de conjuros — lote 1

Agente: agente-I · fecha: 2026-08-21
Páginas leídas: pdf 244, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260
Conjuros revisados: 22 de 22

## Hallazgos

### Baile irresistible de Otto · pdf 249
- **Campo:** nombre (JSON)
- **Dice el JSON:** clave y campo `nombre`: «Baile irresistibile de Otto» (con doble "i": "irresistibile")
- **Dice la página:** cabecera «BAILE IRRESISTIBLE DE OTTO» (grafía española correcta, una sola "i" en el medio: "irresistible")
- **Gravedad:** baja (no afecta a las reglas, pero es una errata de nombre a corregir)

### Brazos de Hadar · pdf 251
- **Campo:** componentes (consume_material)
- **Dice el JSON:** `componentes.material: false` pero `componentes.consume_material: true` (inconsistencia interna: dice que no hay componente material pero que "se consume")
- **Dice la página:** «Componentes: V, S» — no hay componente material en absoluto
- **Gravedad:** baja (dato inconsistente, pero no material real que gastar en mesa)

### Brazos de Hadar · pdf 251
- **Campo:** descripción
- **Dice el JSON:** «…no puede tomar Reacciones hasta el comienzo de **tu** siguiente turno.» (turno del lanzador)
- **Dice la página:** «…no podrán llevar a cabo reacciones hasta el principio de **su** siguiente turno.» (turno de la propia criatura afectada)
- **Gravedad:** media (cambia a quién se refiere el temporizador del efecto; puede alterar cuánto dura la denegación de reacciones en mesa)

### Burla dañina · pdf 252
- **Campo:** descripción (texto corrupto)
- **Dice el JSON:** «...encantamientos **stuileshacia** una criatura...» (palabra corrupta, fusión de "sutiles" + "hacia")
- **Dice la página:** «...encantamientos **sutiles hacia** una criatura...»
- **Gravedad:** baja (no cambia la mecánica, pero es texto ilegible/corrupto que conviene arreglar; también `nombre_en` está mal escrito: JSON dice «Vicios Mockery», debería ser «Vicious Mockery»)

### Caldero burbujeante de Tasha · pdf 252
- **Campo:** componentes (consume_material)
- **Dice el JSON:** `componentes.consume_material: true`
- **Dice la página:** «Componentes: V, S, M (un cucharón bañado en oro que valga al menos 500 po)» — no dice «que se consume» ni nada equivalente
- **Gravedad:** media (afecta si el objeto de 500 po se pierde tras cada lanzamiento o es reutilizable)

### Cambiar de forma · pdf 254
- **Campo:** componentes (consume_material)
- **Dice el JSON:** `componentes.consume_material: true`
- **Dice la página:** «Componentes: V, S, M (una diadema de jade que valga al menos 1500 po)» — no dice «que se consume» ni nada equivalente
- **Gravedad:** media (afecta si la diadema de 1500 po se pierde tras cada lanzamiento; nota: el mismo patrón erróneo aparece ya en Brazos de Hadar y Caldero burbujeante de Tasha, revisar si es sistemático en toda la base)

### Carcaj veloz · pdf 255
- **Campo:** componentes (consume_material)
- **Dice el JSON:** `componentes.consume_material: true`
- **Dice la página:** «Componentes: V, S, M (una aljaba que valga al menos 1 po)» — no dice «que se consume» ni nada equivalente
- **Gravedad:** media (mismo patrón que Cambiar de forma y Caldero burbujeante de Tasha: parece que todo componente material con coste se marcó `consume_material: true` aunque la página no lo diga; convendría revisar sistemáticamente este campo en toda la base)

### Los seis «Castigo…» de paladín (Abrumador, Atronador, Cegador, Desterrador, Furioso) · pdf 256-257
- **Campo:** tiempo_lanzamiento
- **Dice el JSON:** en los cinco, `"tiempo_lanzamiento": "Acción adicional, inmediata tras acertar ataque"` (sin más precisión)
- **Dice la página:** en los cinco, «Acción adicional, que realizas de inmediato tras acertar a una criatura/objetivo **con un arma cuerpo a cuerpo o un ataque sin armas**» — la página siempre especifica que debe ser un ataque cuerpo a cuerpo o sin armas, nunca a distancia
- **Gravedad:** media (el JSON omite la restricción "cuerpo a cuerpo o sin armas"; un jugador podría creer que el castigo se activa también con un ataque a distancia, lo cual no está permitido según la página). No es un caso aislado: se repite igual en los cinco conjuros de la familia, así que probablemente conviene corregirlo de una vez para toda la familia (incluye también "Castigo divino", fuera de mi lote, con la misma redacción).

### Cautiverio · pdf 257-258
- **Campo:** descripción (nombres de las opciones de prisión)
- **Dice el JSON:** dos de las cinco opciones se llaman «prisión de cobertura» y «plomo»
- **Dice la página:** los nombres reales son «**Presidio cercado**» (semiplano protegido contra teletransportación/viaje interplanar — no «prisión de cobertura») y «**Sueño**» (el objetivo queda inconsciente y no puede despertarse — no «plomo»)
- **Gravedad:** media (el efecto descrito para cada opción es correcto, pero el nombre con el que se elige la opción en mesa no coincide con el de la página)

### Cautiverio · pdf 257
- **Campo:** componentes (consume_material)
- **Dice el JSON:** `componentes.consume_material: true`
- **Dice la página:** «Componentes: V, S, M (una estatuilla del objetivo que valga al menos 5000 po)» — no dice «que se consume»
- **Gravedad:** media (mismo patrón que Cambiar de forma, Caldero burbujeante de Tasha y Carcaj veloz — ver nota de patrón sistemático arriba)

### Cofre oculto de Leomund · pdf 259-260
- **Campo:** componentes (consume_material)
- **Dice el JSON:** `componentes.consume_material: true`
- **Dice la página:** «Componentes: V, S, M (un cofre... que valgan al menos 5000 po, así como una réplica Diminuta... que valga al menos 50 po)» — no dice «que se consume»; de hecho la propia descripción explica que el cofre y la réplica se siguen usando durante toda la duración del conjuro para recuperarlo y volver a enviarlo al Plano Etéreo, así que claramente no se consumen
- **Gravedad:** media (mismo patrón sistemático que Cambiar de forma, Caldero burbujeante de Tasha, Carcaj veloz y Cautiverio; el coste combinado "5050 po" del JSON sí es correcto, coincide con 5000+50 po de la página)

## Revisados sin hallazgo

- Amistad · pdf 244 — nivel, escuela, clases, tiempo, alcance, componentes, duración, concentración, ritual y descripción coinciden.
- Arma elemental · pdf 246 — todos los campos coinciden, incluida la escala de mejora por espacio superior (+2/2d4 en 5-6, +3/3d4 en 7+).
- Armadura de Agathys · pdf 247 — todos los campos coinciden (incl. "5 pg temp y 5 daño de frío, +5 por nivel superior a 1").
- Aura de pureza · pdf 249 — todos los campos coinciden.
- Aura de vitalidad · pdf 249 — todos los campos coinciden.
- Aura mágica de Nystul · pdf 249 — todos los campos coinciden, incluido el texto completo de "Enmascarar" y "Aura falsa".
- Baile irresistible de Otto · pdf 249 (+ continuación pdf 250) — todos los campos mecánicos coinciden (nivel, escuela, clases, tiempo, alcance, componentes V, duración/concentración, tirada de salvación Sabiduría, efectos de hechizado); solo hay errata de nombre (ver Hallazgos).

- Brazos de Hadar · pdf 251 — nivel, escuela, clases, tiempo, alcance, componentes V/S, duración/concentración/ritual y daño (2d6 nec., mitad si supera, +1d6 por nivel superior) coinciden (ver Hallazgos para componentes.consume_material y descripción).
- Burla dañina · pdf 252 — nivel, escuela, clases, tiempo, alcance, componentes, duración, tirada de salvación y escalado de daño coinciden (ver Hallazgos para texto corrupto).
- Caldero burbujeante de Tasha · pdf 252-253 — nivel, escuela, clases, tiempo, alcance, componentes (salvo consume_material), duración, coste (500 po) y mecánica de pociones coinciden (ver Hallazgos).
- Calentar metal · pdf 253 — todos los campos coinciden (2d8 fuego, salvación de Constitución, +1d8 por nivel superior a 2).

- Cambiar de forma · pdf 254 — nivel, escuela, clases, tiempo, alcance, componentes (salvo consume_material), duración/concentración y descripción mecánica (PG temp, perfil sustituido, rasgos conservados) coinciden.
- Carcaj veloz · pdf 255 — nivel, escuela, clases, tiempo, alcance, componentes (salvo consume_material), duración/concentración y descripción coinciden.
- Castigo abrumador · pdf 256 — nivel, escuela, clases, alcance, componentes, duración/concentración, daño 4d6 psíquico y escalado coinciden (tiempo_lanzamiento: ver Hallazgos).
- Castigo atronador · pdf 256 — nivel, escuela, clases, alcance, componentes, duración/concentración, daño 2d6 trueno, empujón/derribo y escalado coinciden (tiempo_lanzamiento: ver Hallazgos).
- Castigo cegador · pdf 257 — nivel, escuela, clases, alcance, componentes, duración (1 min, sin concentración — confirmado en la página), daño 3d8 radiante y escalado coinciden (tiempo_lanzamiento: ver Hallazgos).
- Castigo desterrador · pdf 257 — nivel, escuela, clases, alcance, componentes, duración/concentración, daño 5d10 fuerza, umbral de 50 pg y semiplano coinciden (tiempo_lanzamiento: ver Hallazgos).
- Castigo furioso · pdf 257 — nivel, escuela, clases, alcance, componentes, duración (1 min, sin concentración — confirmado en la página), daño 1d6 necrótico, asustado y escalado coinciden (tiempo_lanzamiento: ver Hallazgos).
- Cautiverio · pdf 257-258 — nivel, escuela, clases, tiempo, alcance, componentes (salvo consume_material), duración, salvación de Sabiduría e inmunidad 24h coinciden (ver Hallazgos para nombres de opciones y consume_material).
- Círculo de poder · pdf 258 — todos los campos coinciden.
- Círculo de teletransportación · pdf 258 — todos los campos coinciden, incluido `consume_material: true` (correcto: la página sí dice «que se consumen como parte del conjuro»).

- Cofre oculto de Leomund · pdf 259-260 — nivel, escuela, clases, tiempo, alcance, componentes (salvo consume_material), coste combinado (5050 po), duración y descripción coinciden (ver Hallazgos).

## Dudas / ilegible

Ninguna. Todas las páginas de la asignación (pdf 244, 246, 247, 249, 251, 252, 253, 254, 255, 256, 257, 258, 259) se han podido leer con claridad a 170 dpi; también se renderizaron pdf 248, 250 y 260 para completar descripciones que continuaban en la página siguiente.

## Resumen final

- Conjuros revisados: 22 de 22.
- Hallazgos: 10 (1 errata de nombre, 6 de `componentes.consume_material` con el mismo patrón sistemático, 1 de descripción con diferencia de "tu turno" vs "su turno" en Brazos de Hadar, 1 agrupado de `tiempo_lanzamiento` en los cinco "Castigo…" de mi lote, 1 de nombres de opciones en Cautiverio).
- El patrón `consume_material: true` sin que la página diga «que se consume» aparece en Brazos de Hadar, Cambiar de forma, Caldero burbujeante de Tasha, Carcaj veloz, Cautiverio y Cofre oculto de Leomund — 6 de los 22 conjuros de este lote. Merece revisión sistemática en el resto de `hechizos.json`, no solo en este lote.
