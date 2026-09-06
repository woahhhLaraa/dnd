# Monje de los Elementos, nivel 20 — segunda transcripción a mano (agente E · «el calculista»)

**Ficha:** `Sen Aliento-de-Tormenta` — Aasimar, Monje 20 (Guerrero de los Elementos), trasfondo Acólito.
**Entrada usada:** `/tmp/claude-0/-home-user-dnd/ccce6f54-5659-5d7c-89a3-15e0f610e8cf/scratchpad/crudos/monje_elementos_n20.yaml` (datos crudos, sin bloque `calculado`).
**Fecha:** 2026-09-06.
**Ronda:** 3 de estrés.

## Método

Aritmética a mano, paso a paso, desde la base canónica. Cada término lleva **fichero y campo exactos**.
No se ha ejecutado ningún verificador ni motor de cálculo: los únicos comandos ejecutados han sido
`cat`, `sed`, `grep` y un `python3 -c` que solo hace `json.load` e imprime dos registros de
`hechizos.json` — lectura de datos, nunca cálculo.

### Ficheros consultados (todos permitidos)

| Fichero | Para qué |
|---|---|
| `reglas/generacion_personaje.yaml` | modificadores por puntuación, PG nivel 1, PG niveles siguientes, retroactividad de Constitución, tabla `px_por_nivel` (PB), fórmula de CD de conjuros |
| `reglas/caracteristicas.yaml` | emparejamiento nombre↔abreviatura (`des`, `sab`, `con`…) |
| `reglas/subida_de_nivel.yaml` | qué es un `valor_de_tabla` (columna dispersa por nivel) |
| `reglas/fuentes_de_efectos.yaml` | qué ficheros pueden conceder efectos, para no dejarme ninguna fuente sin mirar |
| `clases/monje.yaml` | dado de golpe, `lanzador`, tabla de progresión (columnas `pb` y `mov_sin_armadura_m`) |
| `clases/rasgos/monje.yaml` | Defensa sin armadura, Movimiento sin armadura, Concentración de monje, Cuerpo y mente |
| `clases/subclases/monje.yaml` | Guerrero de los Elementos: rasgos de niveles 3, 6, 11 y 17 |
| `especies/especies.yaml` | Aasimar: `velocidad_m` y rasgos |
| `trasfondos/trasfondos.yaml` | Acólito: características, dote concedida |
| `dotes/don_epico.yaml` | Don de la velocidad |
| `dotes/generales.yaml` | Mejora de característica (tope 20) |
| `dotes/origen.yaml` | Iniciado en la magia; y descartar «Duro» como fuente de PG |
| `equipo/armaduras.yaml` | reglas de armadura/escudo y penalizador de velocidad por Fuerza |
| `hechizos.json` | *Elementalismo* y *Luz*: si exigen salvación o tirada de ataque |

### Desviaciones cometidas

**Ninguna.** No he abierto `personajes/` (ni `monje_elementos_n20.yaml`, ni el otro monje de nivel 20,
ni `_hallazgos/`), ni `_verificacion/_aritmetica/` (he escrito este fichero directamente, sin listar el
directorio), ni `calculo.py`, `efectos.py`, `reglas/efectos.yaml`, ni ningún verificador. No he mirado
las skills `/personaje` ni `/subir-nivel`: describen lo que hace el motor, que es justo lo que no debo
saber. **No he visto ningún número del proyecto antes de escribir el mío.**

---

## 0. Insumos comunes

### 0.1 Bonificador por competencia (PB)

Nivel total 20.

- `clases/monje.yaml → progresion[n: 20].pb` = **6**
- `reglas/generacion_personaje.yaml → px_por_nivel[nivel: 20].pb` = **6** (tabla «Progreso de los personajes», pdf 43 / libro 41)

Las dos fuentes coinciden. **PB = +6.**

### 0.2 Modificadores por característica

Regla: `reglas/generacion_personaje.yaml → metodos_generacion_caracteristicas.modificadores_por_puntuacion.formula`
— *«(puntuación − 10) / 2, redondeando hacia abajo»* (pdf 40 / libro 38). La tabla adjunta del mismo
campo confirma cada caso hasta 20.

Puntuaciones del bloque `caracteristicas.final` de los crudos (fue 12, des 20, con 13, int 12, sab 19, car 8):

| Característica | Puntuación | Cuenta | Modificador |
|---|---|---|---|
| Destreza | 20 | (20−10)/2 = 5,0 → 5 | **+5** (tabla: `20: 5`) |
| Sabiduría | 19 | (19−10)/2 = 4,5 → 4 | **+4** (tabla: `"18-19": 4`) |
| Constitución | 13 | (13−10)/2 = 1,5 → 1 | **+1** (tabla: `"12-13": 1`) |

Comprobación de que el bloque `final` es coherente con los crudos (no es un número mío, es control de insumos):

- Destreza: 15 (`caracteristicas.base.des`) + 2 (`mejoras[nivel 4].sube.des`) + 2 (`mejoras[nivel 8].sube.des`) + 1 (`dotes[0].sube.des`, Don de la velocidad) = **20**. ✔
- Sabiduría: 14 (`base.sab`) + 1 (`ajuste_trasfondo.sab`) + 2 (`mejoras[nivel 12]`) + 2 (`mejoras[nivel 16]`) = **19**. ✔
- Constitución: 13 (`base.con`), sin ajustes. **Ver §1.2.**

El tope de 20 de `dotes/generales.yaml → dotes["Mejora de característica"].mejora_caracteristica.maximo` se
respeta (Des llega a 19 con las MC y sube a 20 con el don épico, cuyo tope propio es 30:
`dotes/don_epico.yaml → dotes["Don de la velocidad"].mejora_caracteristica.maximo: 30`).

---

## 1. `pg_max`

### 1.1 Dado de golpe y método por nivel

`clases/monje.yaml → atributos_basicos.dado_golpe` = **d8**.

He mirado los veinte niveles de `pg_por_nivel` **uno a uno**. Son dos métodos distintos:

- Nivel 1: `metodo: maximo_dado`, `valor: 8`.
- Niveles 2 a 20 (19 niveles): `metodo: valor_establecido`, `valor: 5` en los diecinueve. Ninguno usa `tirar`.

Ambos coinciden con la base:

- Nivel 1 → `reglas/generacion_personaje.yaml → puntos_golpe.nivel_1.regla`: *«Máximo del dado de golpe + modificador por Constitución»* (pdf 42 / libro 40). Máximo de un d8 = **8**. ✔
- Niveles 2-20 → `reglas/generacion_personaje.yaml → puntos_golpe.niveles_siguientes_al_1.tabla_valores_establecidos.filas`,
  fila `{clases: [Bardo, Brujo, Clérigo, Druida, Monje, Pícaro], valor: 5}` → **5** por nivel. ✔

El literal del mismo bloque (pdf 44 / libro 42) dice que el valor establecido **sustituye a la tirada del dado**,
y que el modificador por Constitución se suma aparte:
*«Tira ese dado, suma tu modificador por Constitución al resultado y añade el total (mínimo de 1)… En vez
de tirar, puedes utilizar el valor establecido…»*. Es decir, 5 es el término del dado, no el total del nivel.

Mínimo de 1: cada nivel aporta 5 + 1 = 6 ≥ 1. No se activa en ningún nivel.

### 1.2 La regla retroactiva de Constitución: ¿cambia aquí?

`reglas/generacion_personaje.yaml → puntos_golpe.aumento_de_constitucion` (pdf 44 / libro 42, `_es_retroactivo: true`):
*«Cuando tu modificador por Constitución aumente en 1, tus puntos de golpe máximos también aumentarán
en 1 por cada nivel que hayas alcanzado.»*

**Comprobado: la Constitución NO cambia en ningún momento de esta ficha.**

- `caracteristicas.base.con` = 13.
- `caracteristicas.ajuste_trasfondo` solo lleva `int: 2` y `sab: 1`. Además, Acólito solo permite ajustar
  Inteligencia, Sabiduría o Carisma (`trasfondos/trasfondos.yaml → trasfondos[Acólito].caracteristicas: [Inteligencia, Sabiduría, Carisma]`),
  así que la Constitución no podía subir por ahí.
- Las cuatro `mejoras` (niveles 4, 8, 12, 16) suben `des`, `des`, `sab`, `sab`. Ninguna toca `con`.
- La única dote, `dotes/don_epico.yaml#Don de la velocidad`, sube `des: 1`. No toca `con`.
- `caracteristicas.final.con` = 13. Igual que la base. ✔

Por tanto **mod. Con = +1 constante en los veinte niveles** y el término de Constitución es plano:
`nivel_total × mod_con`. No hay tramo que recalcular. (Si hubiera cambiado, el término correcto seguiría
siendo `20 × mod_con_final`, no una suma histórica; aquí ambas lecturas dan lo mismo.)

### 1.3 Fuentes externas de PG máximos

Recorridas todas las categorías que `reglas/fuentes_de_efectos.yaml → fuentes` declara como capaces de
conceder efectos, buscando `objetivo: pg_max` entre las que este personaje tiene:

- **Especie Aasimar** (`especies/especies.yaml → especies[Aasimar].rasgos`): Manos curativas, Portador de luz,
  Resistencia celestial, Visión en la oscuridad, Revelación celestial. **Ninguna toca `pg_max`.**
  (El único rasgo de especie con `objetivo: pg_max` de toda la base es «Aguante enano», del **Enano** — no aplica.)
- **Rasgos de monje** (`clases/rasgos/monje.yaml`): ninguno declara `objetivo: pg_max`. Metabolismo asombroso
  y Autorrestablecimiento **recuperan** PG, no suben el máximo.
- **Subclase Guerrero de los Elementos** (`clases/subclases/monje.yaml`): ninguno de sus cuatro rasgos toca `pg_max`.
- **Don épico tomado**: `dotes/don_epico.yaml → dotes["Don de la velocidad"].efectos` = `[{objetivo: velocidad, …}]`.
  **No toca `pg_max`.** El don épico que sí lo haría es «Don de la fortaleza» (`+40`, misma fichero, pdf 212),
  y **no es el que lleva esta ficha**. Descartado explícitamente.
- **Dote de origen**: el trasfondo Acólito concede «Iniciado en la magia (clérigo)»
  (`trasfondos/trasfondos.yaml → trasfondos[Acólito].dote`), que en `dotes/origen.yaml` no tiene `efectos`.
  La dote de origen que sube PG es «Duro» (`2 * nivel_total`), y **no la lleva**. Descartada explícitamente.

### 1.4 Cuenta

```
Término del dado
  nivel 1 ......................  8            (máximo del d8)
  niveles 2-20 .... 19 × 5 =  95            (valor establecido de Monje)
                              ----
                              103

Término de Constitución
  nivel_total × mod_con = 20 × (+1) =  20

  pg_max = 103 + 20 = 123
```

**`pg_max` = 123.**

Comprobación cruzada por el otro camino (sumando nivel a nivel, que aquí da lo mismo porque la Con no cambia):
nivel 1 = 8+1 = 9; niveles 2-20 = 19 × (5+1) = 114; 9 + 114 = **123**. ✔

---

## 2. `ca`

### 2.1 Qué fórmula aplica

`equipo` de la ficha = `[]` (lista vacía), y `competencias.armaduras` = `[]`, coherente con
`clases/monje.yaml → atributos_basicos.armaduras: []`. **No lleva armadura ni escudo.**
`equipo/armaduras.yaml → reglas.solo_un_tipo` / `reglas.escudos` no aportan nada aquí, y ninguna
armadura de esa tabla entra en el cálculo.

Con eso se cumple el requisito del rasgo de nivel 1:

`clases/rasgos/monje.yaml → rasgos["Defensa sin armadura"]` (nivel 1, pdf 151 / libro 149):
*«Mientras no lleves armadura ni portes un escudo, tu clase de armadura base es 10 + modificador de
Destreza + modificador de Sabiduría.»*
Su efecto declarado: `{objetivo: ca, op: base, formula: "10 + mod_des + mod_sab", requiere: [sin_armadura, sin_escudo]}`.

Es una fórmula **`base`**, no un `add`: sustituye a la CA por defecto sin armadura (`10 + mod. Des`), que
—según el aviso del encargo— está declarada en el fichero que tengo vetado. La doy por buena y no la uso,
porque Defensa sin armadura la reemplaza.

Repasadas las demás fuentes con `objetivo: ca` de este personaje: **ninguna otra**. La subclase Guerrero
de los Elementos no toca la CA en ningún nivel; el Aasimar tampoco; «Don de la velocidad» tampoco.

### 2.2 El punto donde dudo: «Cuerpo y mente» (rasgo de monje, nivel 20)

`clases/monje.yaml → progresion[n: 20].rasgos` = `["Cuerpo y mente"]`, y
`clases/rasgos/monje.yaml → rasgos["Cuerpo y mente"]` (nivel 20, pdf 153 / libro 151):
*«Tus puntuaciones de Destreza y Sabiduría aumentan en 4, hasta un máximo de 25.»*

Es un rasgo **permanente**, sin condición ni duración, y este personaje es Monje 20, así que lo tiene.
Toca las dos características de las que depende exactamente esta CA. Pero el bloque
`caracteristicas.final` de los crudos (des 20, sab 19) **no lo incluye**: se explica entero por
base + trasfondo + mejoras + dote (§0.2). Y el rasgo, a diferencia de «Defensa sin armadura» y
«Movimiento sin armadura», **no lleva bloque `efectos:`** en `clases/rasgos/monje.yaml`.

Escribo las **dos lecturas**, como pide el método:

**Lectura A — con las puntuaciones que los crudos declaran como `final`:**

```
CA = 10 + mod_des + mod_sab
   = 10 + (+5)   + (+4)
   = 19
```

**Lectura B — aplicando «Cuerpo y mente» tal como lo transcribe la base:**

```
Destreza  = 20 + 4 = 24   (tope 25, no se alcanza)   → mod = (24−10)/2 = 7
Sabiduría = 19 + 4 = 23   (tope 25, no se alcanza)   → mod = (23−10)/2 = 6,5 → 6
CA = 10 + (+7) + (+6) = 23
```

**Cuál elijo: la lectura B, CA = 23.** El encargo me pide el número derivado *de la regla citada*, y la
regla citada es un rasgo permanente de nivel 20 que la base transcribe con su página. Un monje de nivel 20
tiene Destreza 24 y Sabiduría 23; su CA es 23. La lectura A no es una regla, es el estado de un campo de
entrada al que le falta ese sumando.

**Pero lo digo con todas las letras, porque no quiero que se lea como aritmética cuando es de insumos:**
la diferencia de 4 puntos entre 19 y 23 **no es un error de suma**, es la ausencia de «Cuerpo y mente».
Si el motor produce 19, no ha sumado mal: no ha aplicado el rasgo, porque el rasgo no está expresado como
efecto y `caracteristicas.final` no lo trae. Dejo las dos en la tabla final para que quien compare vea
de cuál se trata. **Lo mismo vale para `caracteristicas.final` en sí: por la regla del manual debería ser
des 24 / sab 23.**

Este punto **no afecta ni a `pg_max` ni a `velocidad`**: «Cuerpo y mente» no toca Constitución ni velocidad.

### 2.3 Lo que descarto por situacional

Nada relevante para la CA: ningún rasgo de este personaje da bonificadores condicionales a la CA.
Reviso y descarto de todos modos, para que conste:

- **Defensa superior** (monje 18, `clases/rasgos/monje.yaml`): resistencia al daño gastando 3 puntos de
  concentración durante 1 minuto. Es **resistencia**, no CA, y además es situacional. **No entra.**
- **Desviar ataques** (monje 3): reduce el daño de un ataque que ya te ha acertado. No es CA. **No entra.**

---

## 3. `velocidad`

### 3.1 Base de especie

`especies/especies.yaml → especies[Aasimar].velocidad_m` = **9 m** (pdf 188 / libro 186).

### 3.2 Movimiento sin armadura (monje, nivel 2, escala con el nivel)

`clases/rasgos/monje.yaml → rasgos["Movimiento sin armadura"]` (nivel 2, pdf 152 / libro 150):
*«Tu velocidad aumenta en 3 m si no llevas armadura ni portas un escudo. Este bonificador aumenta con el
nivel (columna "Movimiento sin armadura" de la tabla): +4,5 m en nivel 6, +6 m en nivel 10, +7,5 m en
nivel 14, +9 m en nivel 18.»*
Efecto declarado: `{objetivo: velocidad, op: add, columna: mov_sin_armadura_m, requiere: [sin_armadura, sin_escudo]}`.

El propio rasgo remite a la columna, no copia la escala. Es un `valor_de_tabla` en el sentido de
`reglas/subida_de_nivel.yaml → concesiones.valor_de_tabla` («tabla dispersa por nivel»: hay que leer la
fila del nivel que toca, no la del tramo anterior).

Columna `mov_sin_armadura_m` de `clases/monje.yaml → progresion`, tramos completos:

| Niveles | `mov_sin_armadura_m` |
|---|---|
| 1 | 0 |
| 2-5 | 3 |
| 6-9 | 4,5 |
| 10-13 | 6 |
| 14-17 | **7,5** |
| 18-20 | **9** |

**El personaje es de nivel 20 → `progresion[n: 20].mov_sin_armadura_m` = 9.** No 7,5 (ese es el tramo
14-17) y no 6. Requisito `sin_armadura`/`sin_escudo`: se cumple (`equipo: []`). **+9 m.**

### 3.3 Don épico de nivel 19

`clases/monje.yaml → progresion[n: 19].rasgos` = `["Don épico"]`, y la ficha lo resuelve en
`dotes[0].ref` = `dotes/don_epico.yaml#Don de la velocidad` (`origen: {clase: Monje, rasgo: Don épico}`).

`dotes/don_epico.yaml → dotes["Don de la velocidad"]` (pdf 213 / libro 211): *«Celeridad: tu velocidad
aumenta 9 m.»* Efecto declarado: `{objetivo: velocidad, op: add, formula: "9"}`, con el comentario del
propio fichero: *«sin condición ni duración»*. Es **permanente**. **+9 m.**

(Su otra mitad, la mejora de característica `+1` a Destreza, ya está contada en §0.2 vía `dotes[0].sube.des`.)

### 3.4 Lo que descarto por situacional — explícito

- **«Paradigma elemental»**, rasgo de subclase de **nivel 17** de Guerrero de los Elementos
  (`clases/subclases/monje.yaml → subclases["Guerrero de los Elementos"].rasgos[nivel 17]`, pdf 157 / libro 155).
  Su efecto está declarado como **`op: conditional`**, con el texto:
  *«Paso destructivo: +6 m hasta el final del turno al usar Paso del viento, y solo mientras Armonía con
  los elementos esté activa»*. Doble condición (gastar un punto de concentración en Armonía con los
  elementos **y** usar Paso del viento) y duración de un turno. **NO entra en la velocidad de la ficha.**
  Este es el rasgo que el encargo señalaba como «puede tocar otro»: sí lo toca, pero solo en situación.
- **«Paso de los elementos»**, subclase nivel 11: velocidad **nadando y volando** iguales a tu velocidad,
  y solo mientras Armonía con los elementos esté activa. Es otro tipo de velocidad y es situacional.
  **NO entra.**
- **«Revelación celestial»** del Aasimar (nivel 3): la opción «Alas celestiales» da velocidad **volando**
  durante 1 minuto, 1 vez por descanso largo. Otro tipo de velocidad y situacional. **NO entra.**
- **Penalizador por Fuerza de armadura pesada** (`equipo/armaduras.yaml → reglas.fuerza`, −3 m):
  no lleva armadura. **No aplica.**
- **«Paso del viento»** (parte de Concentración de monje, nivel 2): permite correr como acción adicional;
  no aumenta la velocidad. **No entra.**

### 3.5 Cuenta

```
  base de especie (Aasimar) ...................  9,0 m
+ Movimiento sin armadura, nivel 20 ..........  +9,0 m
+ Don de la velocidad (Celeridad) ............  +9,0 m
                                               -------
  velocidad = 27,0 m
```

**`velocidad` = 27 m.**

Comprobación en pies (el manual original trabaja en pies de 5 en 5; 1,5 m = 5 pies):
30 + 30 + 30 = 90 pies = 27 m. ✔ Los decimales de la columna (4,5 y 7,5) no intervienen en el nivel 20,
pero los he mirado para asegurarme de no estar leyendo la fila equivocada.

---

## 4. `cd_conjuros` y `bonif_ataque_conjuros`

### 4.1 Conclusión: NO PROCEDE como valor de ficha

**El Monje no es una clase lanzadora y la base no le declara aptitud mágica.**

- `clases/monje.yaml → lanzador: ninguno`.
- `clases/monje.yaml` **no tiene campo `aptitud_magica`**. Comprobado sobre las doce clases: solo lo
  declaran Bardo (Carisma), Brujo (Carisma), Clérigo (Sabiduría), Druida (Sabiduría), Explorador
  (Sabiduría), Hechicero (Carisma), Mago (Inteligencia) y Paladín (Carisma). Bárbaro, Guerrero, Monje y
  Pícaro no.
- `clases/monje.yaml → columnas_extra` = `[artes_marciales, puntos_concentracion, mov_sin_armadura_m]`:
  **no hay columna de trucos, de conjuros preparados ni de espacios**. El personaje no tiene espacios de conjuro.

La fórmula existe y está en la base —`reglas/generacion_personaje.yaml → conjuros` (pdf 240 / libro 238):
`cd_salvacion.formula` = *«8 + modificador de aptitud mágica + bonificador por competencia»*,
`bonificador_ataque.formula` = *«modificador de aptitud mágica + bonificador por competencia»*—, y su
`_nota_aptitud` dice de dónde sale el término que falta: *«La aptitud mágica de cada clase la declara su
propio fichero, en `clases/<clase>.yaml → aptitud_magica`»*. Para el Monje **ese campo no existe**, así
que la fórmula no tiene con qué instanciarse a nivel de personaje. **No es un hueco de la base: es que la
clase no lanza conjuros.**

### 4.2 Pero este personaje sí conoce trucos — y aun así no sale ninguna CD

Tres fuentes le dan magia, cada una con **su propia** aptitud mágica, ninguna de clase:

1. **Especie**: `especies/especies.yaml → especies[Aasimar].rasgos["Portador de luz"]` — *«Conoces el truco
   luz. El **Carisma** es tu aptitud mágica para lanzarlo.»*
2. **Subclase**: `clases/subclases/monje.yaml → subclases["Guerrero de los Elementos"].rasgos[nivel 3]["Manipular los elementos"]`
   — *«Conoces el conjuro elementalismo. La **Sabiduría** es tu aptitud mágica para lanzarlo.»*
3. **Trasfondo**: `trasfondos/trasfondos.yaml → trasfondos[Acólito].dote` = «Iniciado en la magia (clérigo)»
   → `dotes/origen.yaml → dotes["Iniciado en la magia"]` (pdf 203 / libro 201): dos trucos y un conjuro de
   nivel 1 de la lista de clérigo, con *«aptitud mágica Inteligencia, Sabiduría o Carisma (a elección al
   tomar la dote)»*.

Dos observaciones:

- **Ninguno de los dos conjuros que la base le concede de forma nombrada exige salvación ni tirada de ataque.**
  `hechizos.json`: *Elementalismo* (`nivel: 0`, `tirada: "Directo"`) y *Luz* (`nivel: 0`, `tirada: "Directo"`).
  Con `tirada: Directo` no hay ni CD que superar ni bonificador de ataque que sumar.
- **No hay una aptitud mágica única del personaje**: serían Carisma para *luz* y Sabiduría para
  *elementalismo*. Un único campo `cd_conjuros` en la ficha **no podría decir la verdad**: o son dos
  números, o ninguno.

**Por eso no doy un valor.** Si alguien quisiera instanciar la fórmula de todos modos, estos serían los
números (los dejo etiquetados como hipotéticos, no como valores de la ficha):

| Aptitud hipotética | CD = 8 + mod + PB | Ataque = mod + PB |
|---|---|---|
| Sabiduría (sab 19, +4) | 8 + 4 + 6 = **18** | 4 + 6 = **+10** |
| Sabiduría con «Cuerpo y mente» (sab 23, +6) | 8 + 6 + 6 = **20** | 6 + 6 = **+12** |
| Carisma (car 8, −1) | 8 − 1 + 6 = **13** | −1 + 6 = **+5** |

### 4.3 Un número que se le parece pero NO es este

`clases/rasgos/monje.yaml → rasgos["Concentración de monje"]` (nivel 2, pdf 151 / libro 149) termina:
*«Cuando un rasgo de monje que usa puntos de concentración exige salvación, la CD es 8 + tu modificador de
Sabiduría + tu bonificador por competencia.»*

Con sab 19 eso da **8 + 4 + 6 = 18** (con «Cuerpo y mente», 8 + 6 + 6 = **20**). Es la CD de **Golpe
aturdidor**, de **Explosión elemental** y del resto de rasgos de concentración — **no es la CD de conjuros**,
aunque la aritmética sea idéntica. Lo anoto para que nadie lo confunda con `cd_conjuros` en la comparación.

---

## 5. Lo que no he podido derivar

- **`cd_conjuros` / `bonif_ataque_conjuros`**: no procede (§4). No es que falte el dato en la base: la
  fórmula está completa en `reglas/generacion_personaje.yaml → conjuros`, con página; lo que no existe es
  una aptitud mágica de personaje para este Monje. Lo busqué en `clases/monje.yaml` (`lanzador`,
  `aptitud_magica`, `columnas_extra`), en `clases/rasgos/monje.yaml`, en `clases/subclases/monje.yaml` y en
  `reglas/generacion_personaje.yaml`.
- **La ambigüedad de `caracteristicas.final` frente a «Cuerpo y mente»** (§2.2). No la resuelvo por mi
  cuenta: doy las dos y digo cuál defiendo (la B, CA 23). Lo busqué en `clases/rasgos/monje.yaml`
  (el rasgo está transcrito, con página, y **sin `efectos:`**) y en `reglas/subida_de_nivel.yaml`
  (`concesiones.rasgo_de_clase` lo concede como rasgo, pero el vocabulario de efectos que gobierna esto
  vive en `reglas/efectos.yaml`, que tengo vetado y no he abierto).

## 6. Observaciones de insumos (no son valores derivados)

Las dejo por escrito porque las he visto al recorrer la base, no porque me las hayan pedido:

1. **`caracteristicas.final` no incluye «Cuerpo y mente»** (monje 20: Des y Sab +4, tope 25). Por la regla
   citada debería ser des 24 / sab 23, y la CA subir de 19 a 23. Es el único punto donde mi cuenta y los
   crudos pueden separarse.
2. **El bloque `dotes` de los crudos no lista la dote del trasfondo.** Acólito concede «Iniciado en la
   magia (clérigo)» (`trasfondos/trasfondos.yaml → trasfondos[Acólito].dote`) y en `dotes` solo aparece
   «Don de la velocidad». No cambia ninguno de los tres números (esa dote no tiene `efectos` ni mejora de
   característica), pero es una ausencia.
3. **`decisiones[1]` dice «esta ficha solo lleva armadura»** mientras `equipo: []` está vacío. La frase
   parece una plantilla del generador; lo que cuenta para la CA y la velocidad es `equipo: []` (sin
   armadura ni escudo), que es lo que he usado.

---

## Valores derivados

| Valor | Derivado a mano | Cita principal |
|---|---|---|
| **`pg_max`** | **123** | `reglas/generacion_personaje.yaml → puntos_golpe.nivel_1` (8) + `puntos_golpe.niveles_siguientes_al_1.tabla_valores_establecidos` (19 × 5) + `puntos_golpe.aumento_de_constitucion` (20 × +1); `clases/monje.yaml → atributos_basicos.dado_golpe: d8` |
| **`ca`** | **23** *(lectura elegida)* | `clases/rasgos/monje.yaml → rasgos["Defensa sin armadura"]` (`10 + mod_des + mod_sab`) con Des 24 / Sab 23 tras `clases/rasgos/monje.yaml → rasgos["Cuerpo y mente"]` (nivel 20, +4/+4, tope 25) |
| **`ca`** | **19** *(lectura alternativa)* | La misma fórmula, con las puntuaciones tal cual figuran en `caracteristicas.final` de los crudos (des 20 → +5, sab 19 → +4). La diferencia de 4 es exactamente «Cuerpo y mente». |
| **`velocidad`** | **27 m** | `especies/especies.yaml → especies[Aasimar].velocidad_m` (9) + `clases/monje.yaml → progresion[n: 20].mov_sin_armadura_m` (9, vía `clases/rasgos/monje.yaml → rasgos["Movimiento sin armadura"]`) + `dotes/don_epico.yaml → dotes["Don de la velocidad"].efectos` (9) |
| **`cd_conjuros`** | **no procede** | `clases/monje.yaml → lanzador: ninguno`; sin `aptitud_magica`. Fórmula disponible en `reglas/generacion_personaje.yaml → conjuros.cd_salvacion` pero sin término de aptitud que instanciar |
| **`bonif_ataque_conjuros`** | **no procede** | Ídem, `reglas/generacion_personaje.yaml → conjuros.bonificador_ataque` |

### Insumos usados (para que se pueda auditar la cuenta sin rehacerla)

| Insumo | Valor | Cita |
|---|---|---|
| Nivel total | 20 | `nivel_total` de los crudos |
| PB | +6 | `clases/monje.yaml → progresion[n: 20].pb`; `reglas/generacion_personaje.yaml → px_por_nivel[20].pb` |
| Dado de golpe | d8 | `clases/monje.yaml → atributos_basicos.dado_golpe` |
| mod. Con | +1 (constante, sin cambios en 20 niveles) | Con 13, `modificadores_por_puntuacion` |
| mod. Des | +5 (crudos) / +7 (con «Cuerpo y mente») | Des 20 / 24 |
| mod. Sab | +4 (crudos) / +6 (con «Cuerpo y mente») | Sab 19 / 23 |
| Armadura y escudo | ninguno | `equipo: []` |
| Descartado por situacional | «Paradigma elemental» (subclase n17, +6 m), «Paso de los elementos» (n11, volar/nadar), «Revelación celestial» (Aasimar, volar), «Defensa superior» (n18, resistencia) | §2.3 y §3.4 |
