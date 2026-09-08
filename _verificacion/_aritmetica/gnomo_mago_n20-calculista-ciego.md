# Derivación a mano — `gnomo_mago_n20` (Fippen Cascabelroble)

**Agente E · «el calculista» — `PLAN_ESTRES.md`**
Fecha: 2026-09-08

---

## Cabecera

### Ficha

| Campo | Valor (de los datos crudos) |
|---|---|
| Nombre | Fippen Cascabelroble |
| Especie | Gnomo (`especies/especies.yaml#Gnomo`), linaje **Gnomo de los bosques**, aptitud mágica de linaje: Inteligencia |
| Clase | Mago nivel 20, subclase **Evocador** (desde nivel 3) |
| Nivel total | 20 |
| Trasfondo | Erudito (`trasfondos/trasfondos.yaml#Erudito`) |
| Dote | Iniciado en la magia (de origen, por trasfondo) |
| Mejoras de característica | n4: Int +2 · n8: Int +1 y Des +1 · n12: Con +2 · n16: Des +2 |
| Características finales | Fue 8 · Des 17 · Con 16 · Int 20 · Sab 12 · Car 10 |
| PG por nivel | n1 máximo del dado (6); n2–n20 valor establecido (4) |
| Armadura / escudo | **ninguno** (competencias de armadura vacías) |

### Método

Transcripción independiente. Cada número se ha derivado leyendo **el texto de la
regla** en los ficheros de la base y haciendo la aritmética a mano, sin ejecutar
nada y sin ver ningún valor calculado por el motor. La entrada ha sido
exclusivamente la copia **cruda** de la ficha (sin bloque `calculado`):

    /tmp/claude-0/-home-user-dnd/ccce6f54-5659-5d7c-89a3-15e0f610e8cf/scratchpad/crudos/gnomo_mago_n20.yaml

### Ficheros consultados

| Fichero | Para qué |
|---|---|
| `clases/mago.yaml` | dado de golpe, `lanzador`, `aptitud_magica`, competencias de armadura (vacías), tabla de progresión (PB por nivel, rasgos de cada nivel) |
| `clases/rasgos/mago.yaml` | texto de los 8 rasgos de mago, uno por uno, buscando cuál toca `pg_max`, `ca` o `velocidad` |
| `clases/subclases/mago.yaml` | `niveles_de_subclase` y los 5 rasgos del Evocador (niveles 3, 3, 6, 10, 14) |
| `clases/_ESQUEMA_atributos_basicos.md` — *no consultado* | ver nota en «Desviaciones» |
| `especies/especies.yaml` | velocidad base y los 3 rasgos del Gnomo, más sus 2 linajes; y contraste con Enano y Goliat, los únicos con `efectos:` |
| `trasfondos/trasfondos.yaml` | Erudito: características ajustables, dote, `reparto_caracteristicas` |
| `dotes/origen.yaml` | texto de «Iniciado en la magia»; y contraste con «Duro», que sí toca `pg_max` |
| `dotes/generales.yaml` | registro «Mejora de característica» (las 4 subidas de la ficha) y las 4 dotes de ese fichero que llevan `efectos:` |
| `dotes/don_epico.yaml` | las 12 dotes de don épico, por el rasgo «Don épico» de nivel 19 — ver el hallazgo del final |
| `dotes/estilo_de_combate.yaml` | comprobar que su único `efectos:` no es de un estilo que el Mago pueda tomar |
| `reglas/generacion_personaje.yaml` | tabla de modificadores; PG de nivel 1; PG de niveles siguientes + tabla de valores establecidos; **`aumento_de_constitucion`** (la regla retroactiva); fórmulas de conjuros; `px_por_nivel` |
| `reglas/caracteristicas.yaml` | emparejamiento nombre ↔ abreviatura (`Inteligencia` ↔ `int`) |
| `reglas/fuentes_de_efectos.yaml` | qué ficheros de la base **pueden** conceder efectos, para no dejarme ninguno |
| `reglas/subida_de_nivel.yaml` | qué concede y qué hace elegir la base al subir de nivel (aquí sale el hallazgo) |
| `equipo/armaduras.yaml` | catálogo completo de armaduras y escudos; reglas de entrenamiento, Fuerza mínima y sigilo |
| `equipo/armas.yaml` | comprobar que Daga y Bastón son armas, no armadura |
| `equipo/aventureros.yaml` | contenido de «Paquete de erudito», y qué es «Túnica», «Canalizador arcano», «Libro», «Pergamino» |
| `equipo/herramientas.yaml` | «Suministros de calígrafo»: herramienta, no armadura |
| `hechizos.json` | **solo** la entrada «Armadura de mago», por su interacción con la CA — ver «Desviaciones» y el apartado de CA |

### Desviaciones cometidas — declaración honesta

**No he abierto ningún fichero prohibido.** Ni `calculo.py`, ni `efectos.py`, ni
`reglas/efectos.yaml`, ni ningún `validar*.py` / `verificar*.py`, ni
`personajes/` (ni la ficha original ni ninguna otra), ni nada bajo
`_verificacion/` salvo (a) escribir este informe y (b) leer el informe modelo
`_verificacion/_aritmetica/orco_barbaro-calculista-ciego.md`, que **el propio
encargo manda leer** como listón de formato. Ese informe es de un **Bárbaro de
nivel 1** y no comparte con esta ficha ni especie, ni clase, ni nivel, ni un
solo número: sus valores (14 / 13 / 9 m / no procede) no me dan ninguna pista
sobre los míos, y el único apartado del que he tomado algo es la *estructura*.

Cinco matices que declaro por transparencia:

1. **Bloques `efectos:` dentro de ficheros permitidos.** `especies/especies.yaml`,
   `dotes/*.yaml` y algunas subclases traen, junto al texto en prosa, la fórmula
   ya formalizada. He derivado **siempre desde el `desc`/`descripcion` en prosa**
   y solo después he mirado el `efectos:` como confirmación; lo digo en cada
   apartado donde ocurre. En esta ficha, además, el asunto es casi vacío: **ningún
   rasgo, dote o linaje que Fippen tenga lleva bloque `efectos:`**. Los que hay en
   esos ficheros son de rasgos y dotes que **no** tiene (Enano, Goliat, Duro,
   Atacante a la carga, Duelista defensivo, Maestro en armaduras pesadas, dos
   dones épicos, un estilo de combate), y los he leído justamente para poder
   afirmar que no le tocan.

2. **`reglas/fuentes_de_efectos.yaml`.** Está en `reglas/` y no es `efectos.yaml`,
   así que es lectura permitida. Lo he usado para una cosa concreta: cerrar la
   lista de ficheros que pueden conceder efectos (Paso 1). Sus comentarios hablan
   del motor y de fallos históricos del proyecto, pero no traen ningún número de
   esta ficha.

3. **`hechizos.json`.** No está en la lista de directorios que el encargo enumera
   como lectura («`reglas/`, `especies/`, `clases/`, `equipo/`, `dotes/`,
   `trasfondos/`»), pero tampoco en la de prohibidos, y es base de datos del
   juego, no motor. He leído **una** entrada, «Armadura de mago», porque el
   personaje la lleva preparada y su texto habla de la CA: necesitaba su
   **duración** para decidir si entra o no en el valor de la ficha (no entra;
   ver el apartado de CA). No he leído ninguna otra entrada.

4. **Comentarios de cabecera de `reglas/generacion_personaje.yaml`.** El bloque
   `conjuros` y el bloque `puntos_golpe` van precedidos de comentarios que
   cuentan la historia del proyecto y mencionan a calculistas anteriores y a
   `calculo.py` por su nombre. Vienen pegados a las reglas que necesitaba y los
   he leído; no contienen ninguna fórmula distinta de la del propio registro ni
   ningún valor de esta ficha.

5. **Listado de la raíz del proyecto** (`ls /home/user/dnd/`): he visto los
   *nombres* de los ficheros de código y de los planes, no su contenido.

**Hallazgo previo ya conocido, no lo cuento como nuevo:** la CA por defecto sin
armadura (`10 + mod. Destreza`) vive en `reglas/efectos.yaml`, fichero que este
encargo me prohíbe. La doy por buena tal como el encargo indica y no la anoto
como hueco de la base. Es exactamente la misma situación que declaró el
calculista del Orco.

**Una lectura que decidí NO hacer:** `clases/_ESQUEMA_atributos_basicos.md` (el
informe modelo lo usó para confirmar que `d12` significa «1d12 por nivel»). Aquí
no hacía falta: el Mago usa `d6` y la regla de PG del manual habla del «máximo
del dado de golpe», que para `d6` es 6 sin ambigüedad posible. Lo digo para que
la tabla de ficheros consultados no mienta por omisión.

---

## Paso 0 — Modificadores de característica

Los cinco valores cuelgan de los modificadores, así que los derivo primero.

**Regla.** `reglas/generacion_personaje.yaml → metodos_generacion_caracteristicas.modificadores_por_puntuacion`
(bloque con `fuente: {pagina_pdf: 40, libro: 38}`, cap. 2, «Paso 3: determinar
las puntuaciones de característica»):

> `formula: "(puntuación - 10) / 2, redondeando hacia abajo"`

El mismo bloque trae una `tabla:` explícita que uso como segunda comprobación.

**Qué puntuaciones uso: las finales**, es decir, el bloque
`caracteristicas.final` de la ficha — que en un personaje de nivel 20 no es solo
«base + trasfondo», sino «base + trasfondo + las cuatro mejoras de nivel». Lo
reconstruyo entero antes de fiarme de él:

| | Fue | Des | Con | Int | Sab | Car |
|---|---|---|---|---|---|---|
| `base` (conjunto estándar) | 8 | 14 | 13 | 15 | 12 | 10 |
| `ajuste_trasfondo` (Erudito) | — | — | +1 | +2 | — | — |
| tras la creación | 8 | 14 | 14 | **17** | 12 | 10 |
| mejora nivel 4 (Int +2) | | | | +2 → **19** | | |
| mejora nivel 8 (Int +1, Des +1) | | +1 → **15** | | +1 → **20** | | |
| mejora nivel 12 (Con +2) | | | +2 → **16** | | | |
| mejora nivel 16 (Des +2) | | +2 → **17** | | | | |
| **final** | **8** | **17** | **16** | **20** | **12** | **10** |

Coincide exactamente con el bloque `caracteristicas.final` de la ficha. ✔

Comprobaciones de legalidad de cada paso (no son mis cinco valores, pero
sostienen los que sí lo son):

- **Conjunto estándar.** El `base` de la ficha usa el multiconjunto
  {15, 14, 13, 12, 10, 8}, que es el conjunto estándar declarado en
  `reglas/generacion_personaje.yaml`. **No** coincide, eso sí, con la fila
  recomendada para el Mago en `conjunto_estandar_por_clase.filas`
  (`{clase: Mago, fue: 8, des: 12, con: 13, int: 15, sab: 14, car: 10}`): la
  ficha ha intercambiado Des y Sab (Des 14 / Sab 12 en vez de Des 12 / Sab 14).
  Esa tabla se describe a sí misma como «cómo repartir 15/14/13/12/10/8 según la
  clase», es decir, un reparto sugerido, no una imposición; el reparto de la
  ficha usa los mismos seis números. **Lo doy por legal**, y lo hago constar
  porque es una diferencia real con la recomendación de la base y porque afecta
  a mis números: Des 14 en vez de 12 es lo que acaba dando `ca = 13` y no 11.
- **Ajuste de trasfondo.** Erudito permite ajustar `[Constitución, Inteligencia,
  Sabiduría]` (`trasfondos/trasfondos.yaml`, `pagina: {pdf: 184, libro: 182}`),
  y el reparto legal es *«+2 a una y +1 a otra, o +1 a cada una de las tres»*
  (`trasfondos.yaml → reparto_caracteristicas`). **+2 Int / +1 Con** encaja en
  ambas condiciones. ✔
- **Las cuatro mejoras.** Las cuatro citan
  `dotes/generales.yaml#Mejora de característica`
  (`pagina: {pdf: 209, libro: 207}`), cuyo texto es: *«Aumenta en 2 una
  puntuación de característica de tu elección, o aumenta dos en 1 cada una. No
  puede superar 20»*, con `prerrequisito: "nivel 4 o más"` y `repetible: true`.
  Las cuatro respetan las tres condiciones: son «+2 a una» (n4, n12, n16) o «+1 a
  dos» (n8); se toman en niveles ≥ 4; y **ninguna puntuación supera 20** (Int
  llega justo a 20 en el nivel 8 y no vuelve a subir, que es exactamente lo que
  cabría esperar de un jugador que sabe que ahí topa).
- **Los niveles en que se toman.** `clases/mago.yaml → progresion` pone
  «Mejora de característica» en los niveles **4, 8, 12 y 16** y en ningún otro.
  La ficha trae esas cuatro y solo esas. ✔ (El nivel 19 trae otra cosa: ver el
  hallazgo del final.)

**Derivación de cada modificador:**

| Característica | Puntuación final | `(p − 10) / 2` redondeado abajo | Fila de la tabla | Modificador |
|---|---|---|---|---|
| Fuerza | 8 | (8−10)/2 = −1 | `"8-9": -1` | **−1** |
| Destreza | 17 | (17−10)/2 = 3,5 → 3 | `"16-17": 3` | **+3** |
| Constitución | 16 | (16−10)/2 = 3 | `"16-17": 3` | **+3** |
| Inteligencia | 20 | (20−10)/2 = 5 | `20: 5` | **+5** |
| Sabiduría | 12 | (12−10)/2 = 1 | `"12-13": 1` | **+1** |
| Carisma | 10 | (10−10)/2 = 0 | `"10-11": 0` | **0** |

Los dos caminos (fórmula y tabla) coinciden en las seis.

El emparejamiento «Inteligencia» ↔ `int` y «Constitución» ↔ `con` (necesario para
leer el bloque `caracteristicas.final` de la ficha) lo declara
`reglas/caracteristicas.yaml`.

**Modificador de Constitución HISTÓRICO — dato imprescindible para los PG.**
A diferencia de una ficha de nivel 1, aquí el modificador de Constitución **ha
cambiado por el camino**, y eso importa (Paso 3):

| Tramo | Puntuación de Con | Modificador |
|---|---|---|
| niveles 1 – 11 | 14 (13 base + 1 de trasfondo) | **+2** |
| niveles 12 – 20 | 16 (+2 por la mejora del nivel 12) | **+3** |

**Bonificador por competencia (dato auxiliar, imprescindible para conjuros).**
Nivel 20 → **+6**, por dos fuentes que coinciden:
`clases/mago.yaml → progresion[n:20].pb = 6` y
`reglas/generacion_personaje.yaml → px_por_nivel.filas[nivel:20].pb = 6`
(tabla «Progreso de los personajes», pdf 43 / libro 41). El propio fichero de
reglas añade en `multiclase.bonificador_por_competencia` que se basa en el nivel
**total** del personaje; aquí clase única de nivel 20, así que coincide.

---

## Paso 1 — Inventario CERRADO de fuentes de efectos

Antes de calcular nada, cierro la lista de sitios de donde puede salir un
modificador, para poder afirmar que no me dejo ninguno.
`reglas/fuentes_de_efectos.yaml → fuentes` y `→ derivadas` declaran que solo
pueden conceder efectos: `especies/especies.yaml`, `clases/rasgos/*.yaml`,
`clases/subclases/*.yaml`, `dotes/*.yaml`, `trasfondos/*.yaml` y —derivados de
sus campos `ca` y `fuerza`— `equipo/armaduras.yaml`. Su bloque `excluidos`
declara uno a uno, con motivo, los demás ficheros de regla, incluido
`clases/mago.yaml` («tabla de progresión y atributos básicos; sus números son
columnas contrastadas»). Repaso las seis fuentes para esta ficha:

| Fuente | Qué le aplica a Fippen | ¿Modifica `pg_max`, `ca` o `velocidad`? |
|---|---|---|
| `especies/especies.yaml → Gnomo` (pdf 193 / libro 191) | Astucia gnoma · Linaje gnomo (Gnomo de los bosques) · Visión en la oscuridad 18 m | **No.** «Astucia gnoma» da ventaja en TdS de Int/Sab/Car. «Linaje gnomo» fija la aptitud mágica (Inteligencia) y, en el linaje de los bosques, da el truco *ilusión menor* y *hablar con los animales* siempre preparado. «Visión en la oscuridad» es un sentido. **Ninguno de los tres lleva bloque `efectos:`**: en todo ese fichero los únicos son el «Aguante enano» del Enano (línea 67, `pg_max op:add "nivel_total"`) y la «Forma grande» del Goliat (línea 94, `velocidad op:conditional`). Fippen no es ni Enano ni Goliat. |
| `clases/rasgos/mago.yaml` (los 8 rasgos) | Lanzamiento de conjuros (n1) · Adepto en rituales (n1) · Recuperación arcana (n1) · Académico (n2) · Memorizar conjuro (n5) · Maestría sobre conjuros (n18) · **Don épico (n19)** · Conjuros característicos (n20) | **No, ninguno**, y lo he comprobado leyendo los ocho `desc` enteros: hablan de trucos, libro de conjuros, espacios, pericia en una habilidad, y conjuros preparados sin gastar espacio. Ninguno menciona puntos de golpe, clase de armadura ni velocidad, y **ninguno lleva bloque `efectos:`** (el fichero entero no tiene ni uno). El de nivel 19 es la excepción interesante: no aporta nada **por sí mismo**, pero manda tomar una dote que sí podría aportar. Ver el hallazgo del final. |
| `clases/subclases/mago.yaml → Evocador` (pdf 148 / libro 146) | Experto en evocación (n3) · Truco potente (n3) · Esculpir conjuros (n6) · Evocación potenciada (n10) · Sobrecanalizar (n14) | **No.** Los cinco son de daño y de salvaciones contra conjuros. Ninguno lleva `efectos:`. Como contraste dentro del mismo fichero: la «Salvaguarda arcana» del **Abjurador** sí habla de PG («PG máximos iguales al doble de tu nivel de mago + tu modificador por Inteligencia»), pero son los PG **de la salvaguarda**, no los del personaje — y en todo caso Fippen es Evocador, no Abjurador. Los cinco rasgos del Evocador se han obtenido: `niveles_de_subclase: [3, 6, 10, 14]`, todos ≤ 20. |
| `dotes/origen.yaml → Iniciado en la magia` (pdf 203 / libro 201) | dos trucos y un conjuro de nivel 1 de la lista de mago, siempre preparado | **No.** El registro **no lleva** bloque `efectos:`. El único `efectos:` de ese fichero (línea 35) es el de **«Duro»** (`pg_max op:add "2 * nivel_total"`), que a nivel 20 valdría **+40 PG**. Fippen **no tiene «Duro»**: su trasfondo es Erudito, cuya dote es «Iniciado en la magia» (`trasfondos.yaml → Erudito.dote`). Es la trampa más cara de esta ficha y por eso la dejo escrita. |
| `dotes/generales.yaml` (4 registros con `efectos:`) | solo «Mejora de característica», que **no** lleva `efectos:` | **No.** Los cuatro con `efectos:` son *Atacante a la carga* (velocidad condicional), *Duelista defensivo* (ca condicional), *Combatiente con armadura media* (tope de mod. Des con armadura media) y *Maestro en armaduras pesadas* (`velocidad op:add "3"`). Fippen no tiene ninguna de las cuatro: sus cuatro mejoras son el registro «Mejora de característica», y ese solo mueve puntuaciones — ya contabilizadas en el Paso 0. |
| `dotes/don_epico.yaml` | **ninguna registrada en la ficha** | **No aplica**, y este es el punto delicado del informe: el rasgo de nivel 19 obliga a tomar una, dos de ellas tocarían mis valores (*Don de la fortaleza*: `pg_max op:add "40"`; *Don de la velocidad*: `velocidad op:add "9"`), y **la ficha no registra ninguna**. Derivo sin ella, porque no puedo inventar la elección de un jugador; lo reporto como hallazgo al final. |
| `dotes/estilo_de_combate.yaml` | ninguna | El Mago no obtiene estilo de combate en ningún nivel de su progresión, y la ficha no trae ninguno. Su único `efectos:` (línea 40) no le llega. |
| `trasfondos/trasfondos.yaml → Erudito` (pdf 184 / libro 182) | características, dote, habilidades, herramienta, equipo | **No.** El registro no lleva `efectos:`, y su propio campo `no_automatizado` dice que lo que concede son campos estructurados, «no prosa con mecánica escondida». |
| `equipo/armaduras.yaml` (fuente **derivada**) | **nada: no lleva armadura ni escudo** | Ver Paso 2. |

---

## Paso 2 — Comprobación de la condición «sin armadura»

Gobierna la CA y la penalización de velocidad, así que la compruebo aparte.

**El catálogo completo de armaduras** de la base es `equipo/armaduras.yaml`
(`pagina_pdf: 218`, `libro: 216`) y son 14 entradas:

- `armaduras_ligeras`: Armadura acolchada, Armadura de cuero, Armadura de cuero tachonado
- `armaduras_medias`: Armadura de pieles, Camisa de malla, Cota de escamas, Coraza, Media armadura
- `armaduras_pesadas`: Cota guarnecida, Cota de malla, Armadura de bandas, Armadura de placas
- `escudos`: Escudo (`ca: "+2"`)

**El equipo de Fippen**, uno por uno, con el fichero en el que vive cada pieza:

| Objeto de la ficha | Fichero de la base | ¿Es armadura o escudo? |
|---|---|---|
| Daga ×2 | `equipo/armas.yaml` | No, arma |
| Canalizador arcano (bastón) | `equipo/aventureros.yaml` («objeto ornamentado para canalizar magia arcana») | No, canalizador |
| Libro de conjuros | `equipo/aventureros.yaml → objetos_de_rasgo_de_clase` | No |
| Paquete de erudito | `equipo/aventureros.yaml` | No. Contenido declarado: «10 frascos de aceite, 10 hojas de pergamino, lámpara, libro, mochila, pluma, tinta y yesquero». Ninguna armadura dentro. |
| **Túnica** | `equipo/aventureros.yaml` | **No.** Es la única pieza que podría dar dudas por ser prenda. No figura en `equipo/armaduras.yaml`, no tiene campo `ca`, y su descripción es: «Tiene significado vocacional y ceremonial. Algunos eventos y lugares admiten solo a quien la vista con determinados colores o símbolos». Es ropa, no armadura. |
| Bastón | `equipo/armas.yaml` (armas sencillas, 1d6 contundente, versátil) | No, arma |
| Suministros de calígrafo | `equipo/herramientas.yaml` | No, herramienta |
| Libro (de historia) | `equipo/aventureros.yaml` | No |
| Pergamino (8 hojas) | `equipo/aventureros.yaml` | No |

**Conclusión: no lleva armadura de ningún tipo y no lleva escudo.**

Refuerzo independiente: el Mago **no tiene entrenamiento con ninguna armadura**
(`clases/mago.yaml → atributos_basicos.armaduras: []`), y la ficha lo refleja
con `competencias.armaduras: []`. Si se pusiera una, `equipo/armaduras.yaml →
reglas.sin_entrenamiento` dice que tendría desventaja en pruebas de Fue/Des y
**no podría lanzar conjuros** — o sea, la base misma escribe al Mago desde el
supuesto de ir sin armadura. La regla `reglas.solo_un_tipo` tampoco entra en
juego.

---

## Paso 3 — `pg_max`

Este es el valor con más historia de los cinco, y donde un personaje de nivel 20
se distingue de uno de nivel 1: **son dos reglas distintas más una tercera que
las corrige hacia atrás.**

### 3.1 · El nivel 1

`reglas/generacion_personaje.yaml → puntos_golpe.nivel_1`
(`pagina: {pdf: 42, libro: 40}`):

> `regla: "Máximo del dado de golpe + modificador por Constitución."`

**Dado de golpe:** `clases/mago.yaml → atributos_basicos.dado_golpe: d6`
(bloque `atributos_basicos.fuente: {pagina_pdf: 139, pagina_libro: 137}`).
**Máximo de un d6 = 6.** La ficha lo registra igual:
`pg_por_nivel[nivel: 1] = {metodo: maximo_dado, valor: 6}`.

### 3.2 · Los niveles 2 a 20

`reglas/generacion_personaje.yaml → puntos_golpe.niveles_siguientes_al_1`
(`pagina: {pdf: 44, libro: 42}`, sección «Subir de nivel, paso 2», `fidelidad:
literal`):

> «Cada vez que subas un nivel, obtendrás un dado de golpe adicional. Tira ese
> dado, suma tu modificador por Constitución al resultado y añade el total
> (mínimo de 1) a tus puntos de golpe máximos. En vez de tirar, puedes utilizar
> el valor establecido que se muestra en la tabla “Puntos de golpe establecidos
> por clase”.»

La ficha eligió, en los 19 niveles, el método `valor_establecido`. La tabla
`tabla_valores_establecidos` da para el Mago:
`{clases: [Hechicero, Mago], valor: 4}` → **4 por nivel**, sin tirar. Los 19
registros `pg_por_nivel` de la ficha traen ese 4, y los he contado uno a uno:
son exactamente los niveles 2 a 20, sin huecos ni repeticiones. ✔

El «mínimo de 1» del texto se refiere al **total** (dado + modificador), y aquí
nunca muerde: 4 + 2 = 6 y 4 + 3 = 7, ambos > 1.

### 3.3 · La regla que lo corrige hacia atrás — `aumento_de_constitucion`

Esta es la que hace que un nivel 20 no sea una suma acumulada ingenua.
`reglas/generacion_personaje.yaml → puntos_golpe.aumento_de_constitucion`
(`pagina: {pdf: 44, libro: 42}`, «Subir de nivel, paso 5», `fidelidad: literal`):

> «Cuando tu modificador por Constitución aumente en 1, tus puntos de golpe
> máximos también aumentarán en 1 por cada nivel que hayas alcanzado. Por
> ejemplo, si un personaje alcanza el nivel 8 y aumenta su puntuación de
> Constitución de 17 a 18, el modificador por Constitución pasará a ser de +4.
> Los puntos de golpe máximos del personaje aumentarán en 8, más los puntos de
> golpe obtenidos al alcanzar el nivel 8.»

**Le aplica a Fippen**, y no de forma teórica: su mejora del **nivel 12** sube
Constitución de 14 a 16, es decir, el modificador de **+2 a +3**. Por tanto los
11 niveles anteriores también se recalculan.

Consecuencia, que el propio registro enuncia en su nota: el término de
Constitución **no es historia acumulada**, es `nivel_total × mod_con_actual`;
solo el término del dado es historia.

### 3.4 · La aritmética, por los dos caminos

**Camino A — forma cerrada** (la que se deduce de `aumento_de_constitucion`):

```
    término del dado  =  máximo(d6) en el nivel 1  +  19 niveles × 4
                      =  6                          +  76
                      =  82

    término de Con    =  nivel_total × mod. Con actual
                      =  20         × 3
                      =  60

    pg_max            =  82  +  60  =  142
```

**Camino B — reconstrucción histórica, nivel a nivel** (para comprobar que la
forma cerrada no se ha comido nada):

| Tramo | Qué pasa | Acumulado |
|---|---|---|
| Nivel 1 | 6 (máx. d6) + 2 (mod. Con de entonces) = 8 | **8** |
| Niveles 2–11 (10 niveles) | 10 × (4 + 2) = 60 | **68** |
| Nivel 12 — PG del nivel | 4 + 2 (mod. **anterior**) = 6 | **74** |
| Nivel 12 — corrección retroactiva | +1 por cada nivel alcanzado = +12 | **86** |
| Niveles 13–20 (8 niveles) | 8 × (4 + 3) = 56 | **142** |

Los dos caminos dan **142**. ✔

*Sobre el orden dentro del nivel 12:* el ejemplo del manual dice «aumentarán en
8, **más** los puntos de golpe obtenidos al alcanzar el nivel 8», lo que podría
leerse como que el PG de ese nivel ya usa el modificador nuevo **y además** se
suma la corrección completa — lo que contaría dos veces ese nivel y daría 143.
Descarto esa lectura porque el propio registro cierra la puerta en su nota: el
término de Constitución es `nivel_total × mod_con`, y con 20 niveles a +3 son 60
exactos, no 61. Las dos frases del manual describen la misma cantidad desde dos
sitios; la forma cerrada es la que las concilia. **Doy 142 y dejo constancia de
que 143 es la lectura alternativa** que sale de aplicar el ejemplo al pie de la
letra sin la nota.

**Modificadores adicionales sobre `pg_max`: ninguno.** Del inventario del Paso 1:
el Gnomo no tiene «Aguante enano» (ese es del Enano: `pg_max +nivel_total`, que
a nivel 20 serían **+20**); la dote de origen es «Iniciado en la magia» y no
«Duro» (que sería **+40**); la subclase es Evocador y no Abjurador; y no hay
ninguna dote de don épico registrada (*Don de la fortaleza* sería **+40**).
Cuatro trampas caras, las cuatro esquivadas por lo que dice la ficha.

> **`pg_max = 142`**

---

## Paso 4 — `ca`

**Regla base.** El personaje no tiene **ningún** rasgo que redefina la CA: he
leído los ocho rasgos de mago, los cinco del Evocador, los tres del Gnomo y la
dote, y ninguno la menciona. (En la base sí existen cuatro rasgos así, y los he
mirado para poder descartarlos: «Defensa sin armadura» de Bárbaro y de Monje,
«Defensa sin armadura» del bardo Danzarín y «Resistencia dracónica» del
hechicero. Ninguno es de Mago, de Evocador ni de Gnomo.)

Por tanto la CA es la **CA por defecto sin armadura**, `10 + mod. Destreza`. Esa
regla vive en `reglas/efectos.yaml`, fichero que este encargo me prohíbe abrir;
el encargo indica darla por buena, y así lo hago. **No la anoto como hueco**: es
un hallazgo previo ya conocido, el mismo que declaró el calculista del Orco.

**Condición «sin armadura»:** comprobada en el Paso 2 — **se cumple**. Ninguna
de las 13 armaduras del catálogo, ni escudo.

**Aritmética:**

```
    ca = 10  +  mod. Destreza   (+ 0 por armadura: no lleva; + 0 por escudo: no lleva)
       = 10  +  3
       = 13
```

**«Armadura de mago», el punto que hay que argumentar.** Fippen lleva ese conjuro
**preparado** (`conjuros.preparados`), y su texto en `hechizos.json` dice:
*«Tocas a una criatura voluntaria que no lleva armadura. Hasta que el conjuro
termine, la CA base del objetivo es de 13 más su modificador por Destreza»*, con
`tiempo_lanzamiento: "Acción"` y `duracion: "8 horas"`. Si estuviera activo, la
CA sería 13 + 3 = **16**.

**No entra en el valor de la ficha**, por tres razones que declaro:

1. Es un efecto **con duración** que requiere **lanzarse** (una acción y un
   espacio de conjuro). Tener un conjuro *preparado* no es tenerlo *activo*: la
   ficha registra qué puede lanzar, no qué está lanzado.
2. `reglas/fuentes_de_efectos.yaml` cierra la lista de fuentes de efectos y
   **`hechizos.json` no está en ella** — ni en `fuentes`, ni en `derivadas`, ni
   en `pendientes`. Los conjuros no son, por declaración de la base, fuente de
   efectos permanentes sobre la ficha.
3. El vocabulario de la propia base distingue estos casos con `op: conditional`
   —lo he visto en «Forma grande» del Goliat, en «Atacante a la carga» y en
   «Duelista defensivo»—, cuyo `texto` dice explícitamente que **no es la
   velocidad/CA de la ficha**, sino un extra de una situación concreta. Un
   conjuro de 8 horas encaja en esa categoría.

Lo dejo escrito porque es la ambigüedad más plausible de esta ficha y porque, si
el motor diera **16**, no sería un error mío sino una decisión distinta sobre
qué es «la CA de la ficha».

> **`ca = 13`**

---

## Paso 5 — `velocidad`

**Valor base.** `especies/especies.yaml → especies[Gnomo].velocidad_m: 9`
(`pagina: {pdf: 193, libro: 191}`). El campo está declarado en metros
(`velocidad_m`), que es la unidad que pide el encargo.

**Modificadores, uno por uno:**

1. **Rasgos del Gnomo — NO aplican.** «Astucia gnoma» (ventaja en TdS mentales),
   «Linaje gnomo» (aptitud mágica + conjuros del linaje) y «Visión en la
   oscuridad 18 m». Ninguno toca la velocidad, ninguno lleva `efectos:`.
   → **+0 m.**
2. **Tamaño Pequeño — no penaliza.** El Gnomo es «Pequeño (90 cm–1,2 m)», pero su
   `velocidad_m` ya está declarada para esa especie (9 m, igual que Enano,
   Humano, Mediano y Orco). He buscado en `reglas/` y `equipo/` alguna regla que
   modifique la velocidad por tamaño y **no existe ninguna**. → **+0 m.**
3. **Rasgos de mago y de Evocador — NO aplican.** Ninguno de los 13 menciona la
   velocidad. El Mago no tiene un «Movimiento rápido» (Bárbaro, n5) ni un
   «Movimiento sin armadura» (Monje). → **+0 m.**
4. **Dote — NO aplica.** «Iniciado en la magia» no toca la velocidad. Las dotes
   de la base que sí lo hacen son «Maestro en armaduras pesadas»
   (`velocidad +3`, y exige armadura pesada), «Atacante a la carga»
   (`op: conditional`, solo al correr) y el don épico «Don de la velocidad»
   (`velocidad +9`) — ninguna registrada en esta ficha. → **+0 m.**
5. **Penalización de −3 m por Fuerza mínima de armadura — NO aplica.**
   `equipo/armaduras.yaml → reglas.fuerza`: *«Si la tabla indica una puntuación
   de Fuerza para un tipo de armadura, esta reduce 3 m la velocidad de quien la
   lleve, salvo que su Fuerza sea igual o superior a la indicada.»* Fippen no
   lleva armadura (Paso 2), así que no hay nada que penalizar. Merece la pena
   notarlo porque **aquí sí habría mordido**: su Fuerza es **8**, por debajo de
   los dos umbrales de la tabla (13 en Cota de malla, 15 en bandas y placas). Si
   este mago se pusiera una cota de malla —cosa que puede hacer, aunque sin
   entrenamiento— su velocidad bajaría a 6 m. No lo hace. → **−0 m.**
6. **Carga / sobrecarga — la base no la declara** para personajes (solo capacidad
   de carga de animales de tiro, en `equipo/aventureros.yaml`). Igual que anotó
   el calculista del Orco: es regla opcional del manual y no interviene en la
   velocidad canónica de una ficha; lo dejo constar porque busqué ahí antes de
   cerrar.

**Aritmética:**

```
    velocidad = base de especie  +  modificadores  −  penalización de armadura
              = 9 m              +  0             −  0
              = 9 m
```

> **`velocidad = 9 m`**

---

## Paso 6 — `cd_conjuros` y `bonif_ataque_conjuros`

**Fippen SÍ lanza conjuros**, y de la forma más completa que hay en la base:
`clases/mago.yaml` línea 20 → `lanzador: completo`, y línea 21 →
`aptitud_magica: Inteligencia`. Su rasgo «Lanzamiento de conjuros» de nivel 1
(`clases/rasgos/mago.yaml`, pdf 139 / libro 137) lo repite en prosa: *«Aptitud
mágica: Inteligencia»*.

**Las fórmulas.** `reglas/generacion_personaje.yaml → conjuros`
(`pagina: {pdf: 240, libro: 238}`, sección «Tiradas de salvación / Tiradas de
ataque»):

- `cd_salvacion.formula: "8 + modificador de aptitud mágica + bonificador por competencia"` (`base: 8`)
- `bonificador_ataque.formula: "modificador de aptitud mágica + bonificador por competencia"` (`base: 0`)

Y su `_nota_aptitud` remite a `clases/<clase>.yaml → aptitud_magica`, que es de
donde he sacado Inteligencia.

**Los dos términos:**

- modificador de aptitud mágica = **mod. Inteligencia = +5** (Int 20, Paso 0)
- bonificador por competencia = **+6** (nivel 20, Paso 0)

**Aritmética:**

```
    cd_conjuros           = 8  +  5  +  6  =  19
    bonif_ataque_conjuros =      5  +  6  =  11
```

**Las TRES fuentes de magia coinciden en Inteligencia — comprobado, porque si no
coincidieran el valor único sería ambiguo.** Fippen tiene magia por tres vías
distintas, y cada una fija su propia aptitud mágica:

| Vía | Qué concede | Aptitud mágica | Dónde lo dice |
|---|---|---|---|
| Clase Mago | trucos, libro, 25 conjuros preparados, espacios hasta nivel 9 | **Inteligencia** | `clases/mago.yaml → aptitud_magica` (y el `desc` del rasgo) |
| Linaje **Gnomo de los bosques** | truco *ilusión menor*; *hablar con los animales* siempre preparado | **elegida**: Inteligencia | `especies/especies.yaml → Gnomo`, rasgo «Linaje gnomo»: *«Inteligencia, Sabiduría o Carisma es tu aptitud mágica (elige al seleccionar el linaje)»*. La ficha registra la elección: `especie.rasgos_elegidos.aptitud_magica_linaje: Inteligencia` |
| Dote **Iniciado en la magia** | trucos *luz* y *reparar*; *identificar* siempre preparado | **elegida**: no registrada explícitamente | `dotes/origen.yaml → Iniciado en la magia`: *«aptitud mágica Inteligencia, Sabiduría o Carisma (a elección al tomar la dote)»* |

Las dos primeras son **Inteligencia** sin discusión. La tercera **no está
registrada en la ficha**: el bloque `dotes[]` solo trae la `ref` y el origen, sin
el campo de aptitud elegida. Lo doy por Inteligencia porque (a) la lista de
conjuros elegida es la de **mago** (los tres conjuros son de mago y el trasfondo
Erudito declara literalmente `dote: "Iniciado en la magia (mago)"`), y (b) es la
única elección que no crearía un segundo valor de CD en la misma ficha. Aun así
lo señalo abajo como hueco menor de registro.

**Consecuencia:** con las tres vías en Inteligencia, **un único par de valores
sirve para todos sus conjuros**: CD 19 y ataque +11. Si la elección de la dote
hubiera sido Carisma, sus tres conjuros de dote tendrían CD 8 + 0 + 6 = 14
mientras el resto seguiría en 19, y un campo escalar `cd_conjuros` no podría
representar la ficha. No es el caso, pero conviene que conste.

> **`cd_conjuros` = 19 · `bonif_ataque_conjuros` = +11**

---

## Valores derivados

| Valor | Resultado | Derivación | Regla citada |
|---|---|---|---|
| `pg_max` | **142** | (6 máx. d6 + 19×4 valor establecido) + 20 niveles × mod. Con (+3) = 82 + 60 | `reglas/generacion_personaje.yaml → puntos_golpe.nivel_1` (pdf 42 / libro 40), `→ niveles_siguientes_al_1` + `tabla_valores_establecidos` (pdf 44 / libro 42) y `→ aumento_de_constitucion` (pdf 44 / libro 42); dado en `clases/mago.yaml → atributos_basicos.dado_golpe: d6` (pdf 139 / libro 137) |
| `ca` | **13** | 10 + mod. Des (+3); sin armadura ✔, sin escudo ✔; ningún rasgo redefine la CA | CA por defecto sin armadura (vive en `reglas/efectos.yaml`, fichero vedado a este encargo, dada por buena); condición verificada contra `equipo/armaduras.yaml` (pdf 218 / libro 216) |
| `velocidad` | **9 m** | 9 m de especie, sin ningún modificador aplicable | `especies/especies.yaml → especies[Gnomo].velocidad_m` (pdf 193 / libro 191) |
| `cd_conjuros` | **19** | 8 + mod. Int (+5) + PB (+6) | `reglas/generacion_personaje.yaml → conjuros.cd_salvacion` (pdf 240 / libro 238); aptitud en `clases/mago.yaml → aptitud_magica` |
| `bonif_ataque_conjuros` | **+11** | mod. Int (+5) + PB (+6) | `reglas/generacion_personaje.yaml → conjuros.bonificador_ataque` (pdf 240 / libro 238) |

Valores auxiliares derivados por el camino, por si sirven de contraste:

| Auxiliar | Valor | Fuente |
|---|---|---|
| mod. Fuerza | −1 | Fue 8 |
| mod. Destreza | +3 | Des 17 |
| mod. Constitución | +3 | Con 16 (era +2 hasta el nivel 11) |
| mod. Inteligencia | +5 | Int 20 |
| mod. Sabiduría | +1 | Sab 12 |
| mod. Carisma | 0 | Car 10 |
| Bonificador por competencia | +6 | `clases/mago.yaml → progresion[n:20].pb` y `reglas/generacion_personaje.yaml → px_por_nivel[nivel:20].pb` (pdf 43 / libro 41) |
| Término del dado en los PG | 82 | 6 + 19×4 |
| Término de Constitución en los PG | 60 | 20 × 3 |

---

## Lo que NO se ha podido derivar de la base

### 1. El «Don épico» de nivel 19 no es una elección para la base — HALLAZGO

Es lo único que me ha hecho dudar de verdad, y tiene la misma forma que el
hallazgo mayor de este proyecto: **una regla transcrita y citada que ningún
número recoge.**

**La regla existe y está bien transcrita.** `clases/mago.yaml → progresion` pone
en el nivel 19: `rasgos: ["Don épico"]`. Y `clases/rasgos/mago.yaml → Don épico`
(`nivel: 19`, `pagina: {pdf: 141, libro: 139}`) dice:

> «Obtienes una dote de don épico (capítulo 5) u otra dote de tu elección para
> la que cumplas las condiciones. Se recomienda Don del recuerdo de conjuros.»

No es una rareza del Mago: **las doce clases** lo tienen en el nivel 19
(lo he comprobado en los doce ficheros `clases/*.yaml`).

**Las dotes que manda tomar sí tienen números, y grandes.**
`dotes/don_epico.yaml` trae las 12 con su página (pdf 212–213 / libro 210–211).
**Las doce** llevan `mejora_caracteristica: {cantidad: 1, maximo: 30, …}`, o sea
**+1 a una puntuación de característica, con tope 30 y no 20**. Y dos llevan
además bloque `efectos:` que caería de lleno sobre mis valores:

- **Don de la fortaleza**: `{objetivo: pg_max, op: add, formula: "40"}`
- **Don de la velocidad**: `{objetivo: velocidad, op: add, formula: "9"}`

**Pero la base no obliga a registrar la elección.**
`reglas/subida_de_nivel.yaml` es el fichero que declara qué se concede y qué se
elige al subir de nivel, y ahí «Don épico» **no aparece por ningún lado**:

- no está en `marcadores` (que solo lista «Mejora de característica»,
  «Rasgo de subclase» y el patrón «Subclase de \<clase\>»);
- no está en `elecciones`: el registro `mejora_caracteristica_o_dote` se declara
  a sí mismo como «medido: 51 apariciones, niveles 4, 6, 8, 10, 12, 14 y 16» —
  **el 19 no está en esa lista**.

Al no ser marcador, «Don épico» se comporta como un rasgo de clase normal con
texto propio, que es lo que es; y al no ser elección, nada pide al jugador (ni a
la skill `/subir-nivel`) que anote qué dote tomó.

**Y en esta ficha, efectivamente, no está anotada.** `dotes:` trae solo
«Iniciado en la magia» (del trasfondo), y `mejoras:` solo los niveles 4, 8, 12 y
16. Fippen ha llegado al nivel 20 sin la dote que el nivel 19 le concede.

**Qué he hecho con eso: nada, y por qué.** No puedo elegir por el jugador: de las
12 dotes, 10 no cambiarían ninguno de mis cinco valores (su +1 de característica
solo movería un modificador si la puntuación pasara de par a impar hacia arriba,
y en Fippen ninguna lo haría: Int 20→21 sigue dando +5, Des 17→18 daría +4 pero
solo si eligiera Destreza, Con 16→17 seguiría en +3), una daría **pg_max = 182**
y otra **velocidad = 18 m**. Derivo, por tanto, sobre lo que la ficha declara:
142 y 9 m.

**Lo que reporto** es que la base **no puede detectar la ausencia**: ningún campo
la exige, ninguna regla la enumera como elección pendiente, y por tanto cualquier
personaje de nivel 19 o 20, de cualquiera de las doce clases, saldrá con una
dote de menos sin que nada se ponga en rojo. Es exactamente el modo de fallo que
este encargo describe: la regla está en la prosa, citada y con su página, y
ningún número la recoge.

*(Añado un matiz por honestidad: no sé si el motor del proyecto trata «Don
épico» de alguna otra forma, porque no puedo leer su código. Lo que afirmo es lo
que se ve desde la base: el rasgo existe con su texto, las dotes existen con sus
efectos, y `subida_de_nivel.yaml` no conecta lo uno con lo otro.)*

### 2. La aptitud mágica elegida en «Iniciado en la magia» no se registra — hueco menor

La dote deja elegir entre Inteligencia, Sabiduría y Carisma, y la ficha no anota
la elección: el bloque `dotes[]` solo guarda `ref` y `origen`. Contrástese con el
linaje gnomo, donde la ficha **sí** tiene un campo para lo mismo
(`especie.rasgos_elegidos.aptitud_magica_linaje: Inteligencia`). En Fippen es
inocuo —todo apunta a Inteligencia— pero en un personaje cuya clase usara otra
aptitud, esa elección no registrada haría indeterminable la CD de los conjuros de
la dote. Lo anoto como hueco de **registro**, no de regla: la regla está bien
transcrita en `dotes/origen.yaml`.

### 3. Dos observaciones menores, ninguna bloqueante

1. **La velocidad base de las especies no trae `pagina` propia por campo.**
   `especies/especies.yaml` declara `velocidad_m: 9` dentro del registro Gnomo, y
   la página citable es la del registro entero (`pagina: {pdf: 193, libro: 191}`).
   Suficiente y sin ambigüedad; lo anoto solo para que conste el grano de la cita.
   (El calculista del Orco anotó lo mismo.)
2. **El reparto base de características no sigue la fila recomendada para el Mago.**
   Ver Paso 0: la ficha intercambia Destreza y Sabiduría respecto a
   `conjunto_estandar_por_clase.filas[clase: Mago]`. La tabla es una recomendación
   de reparto, no una restricción, y el multiconjunto de valores es el correcto,
   así que **no lo cuento como defecto**; lo dejo escrito porque es la razón de
   que `ca` valga 13 y no 11, y porque un verificador que compare contra la fila
   recomendada daría un falso positivo aquí.

---

*Informe escrito sin ejecutar ningún verificador, sin leer ninguna línea de
Python, sin abrir `reglas/efectos.yaml` y sin ver ningún valor calculado por el
motor para esta ficha ni para ninguna otra.*

---

## Veredicto

```veredicto
pg_max: 142
ca: 13
velocidad: 9
cd_conjuros: 19
bonif_ataque_conjuros: 11
```
