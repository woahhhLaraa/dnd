# Sarv Escamagris (Dracónido · Monje 2) — derivación a mano, ciega

**Agente E · «el calculista» — ronda 3 de estrés**
Fecha: 2026-09-05

---

## Cabecera

**Ficha:** `draconido_monje_n2` — Sarv Escamagris. Dracónido (linaje Rojo),
trasfondo Ermitaño, Monje 2, sin subclase. Nivel total 2.

**Entrada:** exclusivamente los datos crudos de
`/tmp/claude-0/-home-user-dnd/ccce6f54-5659-5d7c-89a3-15e0f610e8cf/scratchpad/crudos/draconido_monje_n2.yaml`,
que no lleva bloque `calculado`.

**Método:** transcripción independiente. Cada número de abajo sale de leer la
base de reglas y aplicar la regla a mano, no de ejecutar ni de leer el motor.
Todo paso lleva su cita `fichero → campo` y, cuando el fichero la trae, la
página (`pagina: {pdf: N, libro: M}`).

### Ficheros de la base consultados

| Fichero | Para qué |
|---|---|
| `reglas/generacion_personaje.yaml` | modificadores por puntuación, ajuste de trasfondo, PG de nivel 1 y siguientes, tabla de valores establecidos, fórmula de CD de conjuros, PB por nivel |
| `clases/monje.yaml` | dado de golpe, competencias, `lanzador`, tabla de progresión (`pb`, `mov_sin_armadura_m`) |
| `clases/rasgos/monje.yaml` | Defensa sin armadura, Movimiento sin armadura, Concentración de monje |
| `clases/subclases/monje.yaml` | comprobar que ninguna subclase entra antes del nivel 3 |
| `especies/especies.yaml` | velocidad base y rasgos del Dracónido |
| `trasfondos/trasfondos.yaml` | Ermitaño: características ajustables, dote, equipo |
| `dotes/origen.yaml` | dote Sanador (¿concede conjuros o PG?) |
| `dotes/generales.yaml`, `dotes/estilo_de_combate.yaml`, `dotes/don_epico.yaml` | solo por `grep`, para enumerar qué efectos de `pg_max`/`ca`/`velocidad` existen en la base y descartarlos |
| `equipo/armaduras.yaml` | catálogo de armaduras y escudos, para comprobar la condición «sin armadura ni escudo» |
| `equipo/armas.yaml`, `equipo/aventureros.yaml`, `equipo/herramientas.yaml` | clasificar cada objeto del equipo y el contenido del paquete de explorador |
| `reglas/fuentes_de_efectos.yaml` | cerrar el universo de fuentes de efectos (ver desviaciones) |
| `clases/*.yaml` (los 12) | solo por `grep` de `lanzador`/`aptitud_magica`, para contrastar el patrón del Monje |

### Desviaciones del método — declaradas

1. **Leí `reglas/fuentes_de_efectos.yaml`.** No está en la lista de prohibidos
   (que nombra `reglas/efectos.yaml`, no este), pero es un fichero adyacente al
   motor y lo declaro igualmente. Lo usé solo para una cosa: cerrar la lista de
   sitios donde la base puede esconder un efecto sobre `pg_max`, `ca` o
   `velocidad` (`fuentes` → `especies/especies.yaml`, `clases/rasgos/*.yaml`,
   `clases/subclases/*.yaml`, `dotes/*.yaml`, `trasfondos/*.yaml`). No contiene
   ningún número de personaje ni ninguna fórmula: es un manifiesto de rutas.
2. **Ejecuté `ls /home/user/dnd/_verificacion/`** (solo nombres de fichero, sin
   abrir ninguno). No entré en `_aritmetica/` ni leí ningún informe previo.
3. **`grep` sobre `reglas/` con exclusión explícita.** Al buscar la regla
   general de CA lancé un `grep -rn` que abarcaba `reglas/`, filtrando con
   `grep -v` las líneas de `reglas/efectos.yaml` y `reglas/_ESQUEMA_efectos.md`
   antes de que llegaran a mí. Ninguna línea de esos dos ficheros apareció en la
   salida; lo dejo dicho porque el comando podría haberla mostrado.

**Lo que NO abrí:** `calculo.py`, `efectos.py`, `reglas/efectos.yaml`,
`reglas/_ESQUEMA_efectos.md`, ningún `verificar_*.py`, `validar.py`, `censo.py`,
`cobertura.py`, `generar_ficha.py`, `subir_nivel.py`, `buscar.py`, ningún
fichero de `personajes/` (ni el original de esta ficha ni ningún otro), ningún
fichero bajo `_verificacion/`, ni `FUENTES.md` / `CONTINUAR.md` / los `PLAN_*.md`
(documentos de proyecto que podrían traer ejemplos ya calculados).

**No he visto ningún número calculado por el proyecto para esta ficha ni para
ninguna otra.**

---

## Paso 0 — Puntuaciones finales y modificadores

Estos tres modificadores alimentan los cuatro apartados siguientes, así que los
derivo una vez aquí.

### 0.1 Puntuaciones finales

La ficha declara `caracteristicas.base` (conjunto estándar) y
`caracteristicas.ajuste_trasfondo` (`sab: 2`, `con: 1`). No me fío del bloque
`final`: lo rederivo.

- **Reparto base.** `reglas/generacion_personaje.yaml → conjunto_estandar_por_clase.filas`
  (`fuente: {pagina_pdf: 40, libro: 38, tabla: "Conjunto estándar por clase"}`),
  fila `Monje`: `fue: 12, des: 15, con: 13, int: 10, sab: 14, car: 8`.
  Coincide exactamente con `caracteristicas.base` de la ficha. ✔
- **Legalidad del ajuste.** `reglas/generacion_personaje.yaml →
  metodos_generacion_caracteristicas.ajuste_por_trasfondo`
  (`fuente: {pagina_pdf: 40, libro: 38}`): «aumenta una de las tres
  características del trasfondo en 2 y otra distinta en 1, o aumenta las tres en
  1. Ningún ajuste puede superar 20.»
  `trasfondos/trasfondos.yaml → trasfondos[Ermitaño].caracteristicas`
  (`pagina: {pdf: 183, libro: 181}`) = `[Constitución, Sabiduría, Carisma]`.
  El ajuste elegido (+2 Sab, +1 Con) toma dos características distintas de esas
  tres → **legal**. Ninguna supera 20. ✔

| Característica | Base | Ajuste | Final |
|---|---|---|---|
| Fuerza | 12 | — | **12** |
| Destreza | 15 | — | **15** |
| Constitución | 13 | +1 | **14** |
| Inteligencia | 10 | — | **10** |
| Sabiduría | 14 | +2 | **16** |
| Carisma | 8 | — | **8** |

Coincide con el bloque `final` de la ficha cruda. ✔

### 0.2 Modificadores

Regla: `reglas/generacion_personaje.yaml →
metodos_generacion_caracteristicas.modificadores_por_puntuacion.formula`
(`fuente: {pagina_pdf: 40, libro: 38}`) = «(puntuación − 10) / 2, redondeando
hacia abajo», con `tabla` de respaldo en el mismo campo.

- `mod_des` = ⌊(15 − 10)/2⌋ = ⌊2,5⌋ = **+2**  · tabla, entrada `"14-15": 2` ✔
- `mod_con` = ⌊(14 − 10)/2⌋ = **+2**  · tabla, entrada `"14-15": 2` ✔
- `mod_sab` = ⌊(16 − 10)/2⌋ = **+3**  · tabla, entrada `"16-17": 3` ✔

### 0.3 Bonificador por competencia

Dos fuentes concordantes, ambas para nivel total 2:

- `clases/monje.yaml → progresion`, fila `{n: 2, pb: 2, …}`
  (`fuente: {archivo: "Manual_del_Jugador_2024.pdf", pagina_pdf: 152}`,
  tabla «Rasgos de monje»).
- `reglas/generacion_personaje.yaml → px_por_nivel.filas`, fila
  `{nivel: 2, px: 300, pb: 2}` (`fuente: {pagina_pdf: 43, pagina_libro: 41,
  tabla: "Progreso de los personajes"}`).

**PB = +2.** (No interviene en los cuatro valores pedidos, pero sí en las CD del
apartado 4.)

---

## 1 · `pg_max` — Puntos de golpe máximos

### 1.1 Dado de golpe

`clases/monje.yaml → atributos_basicos.dado_golpe` = `d8`
(`atributos_basicos.fuente: {pagina_pdf: 151, pagina_libro: 149}`).

### 1.2 Nivel 1

`reglas/generacion_personaje.yaml → puntos_golpe.nivel_1.regla`
(`pagina: {pdf: 42, libro: 40}`): «Máximo del dado de golpe + modificador por
Constitución.»

- Máximo de un d8 = 8.
- 8 + `mod_con` (+2) = **10 PG**.

La ficha registra en `pg_por_nivel[0]`: `metodo: maximo_dado, valor: 8`, citando
`reglas/generacion_personaje.yaml → puntos_golpe.nivel_1`. Ese `8` es el término
del dado; el modificador de Constitución lo sumo yo desde la regla (ver la
ambigüedad tratada en 1.5).

### 1.3 Nivel 2

`reglas/generacion_personaje.yaml → puntos_golpe.niveles_siguientes_al_1`
(`pagina: {pdf: 44, libro: 42}`, sección «Subir de nivel, paso 2: Ajustar los
puntos de golpe y los dados de golpe», `fidelidad: literal`):

> «Cada vez que subas un nivel, obtendrás un dado de golpe adicional. Tira ese
> dado, suma tu modificador por Constitución al resultado y añade el total
> (mínimo de 1) a tus puntos de golpe máximos. En vez de tirar, puedes utilizar
> el valor establecido que se muestra en la tabla "Puntos de golpe establecidos
> por clase".»

La ficha eligió el método fijo — `decisiones[0]`: «PG: valor establecido (5) en
vez de tirar el d8», y `pg_por_nivel[1].metodo: valor_establecido`. Esa elección
es del jugador, no algo que yo pueda derivar; la tomo como dato de entrada, y la
propia base lo subraya: `…niveles_siguientes_al_1.metodos[valor_establecido].desc`
dice «Es una opción del jugador, no un promedio que la base pueda calcular por
su cuenta».

Valor de la tabla: `…niveles_siguientes_al_1.tabla_valores_establecidos.filas`,
fila `{clases: [Bardo, Brujo, Clérigo, Druida, Monje, Pícaro], valor: 5}` →
**Monje = 5**.

- 5 + `mod_con` (+2) = 7. Mínimo de 1 (`metodos[valor_establecido]`… el `minimo: 1`
  del método `tirar` se aplica al TOTAL, dado + mod): 7 ≥ 1, no muerde.
- **+7 PG.**

### 1.4 Efectos externos sobre `pg_max` — ninguno aplica

Enumerados por `grep` de `objetivo: pg_max` sobre las cinco familias de fuentes
que declara `reglas/fuentes_de_efectos.yaml → fuentes`:

| Efecto | Fichero | ¿Aplica? |
|---|---|---|
| «Aguante enano» (`+nivel_total`) | `especies/especies.yaml → especies[Enano].rasgos` | **No** — la especie es Dracónido |
| Dote «Duro» (`+2 * nivel_total`) | `dotes/origen.yaml → dotes[Duro].efectos` | **No** — la única dote de la ficha es Sanador |
| «Resistencia dracónica» (`+nivel_clase`) | `clases/subclases/hechicero.yaml` | **No** — es de subclase de hechicero, no del linaje dracónido |
| «Don del vigor irresistible» (`+40`) | `dotes/don_epico.yaml` | **No** — dote de nivel 19 |

Comprobado uno a uno el resto de fuentes del personaje:
- **Especie Dracónido** (`especies/especies.yaml`, `pagina: {pdf: 189, libro: 187}`):
  sus cinco rasgos —Linaje dracónico, Ataque de aliento, Resistencia al daño,
  Visión en la oscuridad, Vuelo dracónico (nivel 5)— no llevan bloque `efectos`
  ni mencionan PG máximos.
- **Rasgos de monje de niveles 1-2** (`clases/rasgos/monje.yaml`): Artes
  marciales, Defensa sin armadura, Concentración de monje, Metabolismo asombroso
  y Movimiento sin armadura. Solo «Metabolismo asombroso» habla de PG, y es
  **recuperación** puntual («recuperas una cantidad de puntos de golpe igual a
  tu nivel de monje más el resultado»), no un aumento del máximo.
- **Trasfondo Ermitaño** (`trasfondos/trasfondos.yaml`): sin bloque `efectos`;
  el propio registro declara `no_automatizado: "el trasfondo no tiene texto de
  rasgo…"`.
- **Dote Sanador** (`dotes/origen.yaml`, `pagina: {pdf: 204, libro: 202}`):
  médico de batalla y repetir tiradas de curación. Sin bloque `efectos`.
- **Subclase**: `null` (ver 4.2).

### 1.5 Ambigüedad tratada, y comprobación cruzada

**La duda:** en `pg_por_nivel`, ¿el campo `valor` es solo el término del dado, o
el total ya con Constitución sumada?

- *Lectura A (la que elijo):* `valor` es **solo el término del dado**. El
  `8` del nivel 1 es exactamente «máximo del d8» y el `5` del nivel 2 es
  exactamente la entrada de Monje en `tabla_valores_establecidos` — los dos
  números que las reglas citadas dan **sin** Constitución. Además las citas que
  la propia ficha adjunta apuntan a esos campos, no a un total.
  → pg_max = (8 + 5) + 2 × (+2) = 13 + 4 = **17**.
- *Lectura B (descartada):* `valor` sería el total. Entonces pg_max = 8 + 5 = 13
  y el modificador de Constitución no se habría aplicado nunca, lo que contradice
  el literal de ambas reglas («+ modificador por Constitución», «suma tu
  modificador por Constitución al resultado»). Un Monje con Con 14 no puede tener
  los mismos PG que uno con Con 10.

**Comprobación cruzada por la regla retroactiva.**
`reglas/generacion_personaje.yaml → puntos_golpe.aumento_de_constitucion`
(`pagina: {pdf: 44, libro: 42}`, `_es_retroactivo: true`): «Cuando tu modificador
por Constitución aumente en 1, tus puntos de golpe máximos también aumentarán en
1 por cada nivel que hayas alcanzado». Su `_nota_para_el_motor` da la forma
cerrada: el término de Constitución es `nivel_total × mod_con` y solo el término
del dado es historia acumulada.

- Término de dados: 8 (nivel 1) + 5 (nivel 2) = 13.
- Término de Constitución: `nivel_total × mod_con` = 2 × 2 = 4.
- Total = **17**.

Las dos vías coinciden, como debían: el ajuste de Constitución de esta ficha se
aplicó en la **creación** (`ajuste_trasfondo`), antes del nivel 1, así que
`mod_con` ha valido +2 en los dos niveles y no hay ninguna subida a mitad de
carrera que separe el modelo plano del retroactivo. Esta ficha, por tanto, **no
ejercita** el caso que la nota advierte; no sirve como prueba de esa regla.

### → `pg_max` = **17**

---

## 2 · `ca` — Clase de armadura

### 2.1 El rasgo que fija la base

`clases/rasgos/monje.yaml → rasgos[Defensa sin armadura]`
(`nivel: 1`, `pagina: {pdf: 151, libro: 149}`):

> «Mientras no lleves armadura ni portes un escudo, tu clase de armadura base es
> 10 + modificador de Destreza + modificador de Sabiduría.»

y su declaración estructurada, en el mismo registro, campo `efectos`:

    {objetivo: ca, op: base, formula: "10 + mod_des + mod_sab",
     requiere: [sin_armadura, sin_escudo], pagina: {pdf: 151, libro: 149}}

El personaje tiene el rasgo: `clases/monje.yaml → progresion`, fila `{n: 1, …,
rasgos: ["Artes marciales", "Defensa sin armadura"]}`, y su nivel de monje es 2.

### 2.2 Comprobación de la condición `[sin_armadura, sin_escudo]`

Esto es lo que hay que verificar de verdad, así que lo hago objeto a objeto
contra `equipo/armaduras.yaml` (`fuente: {paginas_pdf: "218-219"}`), cuyo
catálogo completo es: armaduras ligeras (acolchada, de cuero, de cuero
tachonado), medias (de pieles, camisa de malla, cota de escamas, coraza, media
armadura), pesadas (cota guarnecida, cota de malla, de bandas, de placas) y
`escudos` (Escudo, `ca: "+2"`).

| Objeto de `equipo` en la ficha | Qué es | Fichero donde lo encuentro | ¿Armadura o escudo? |
|---|---|---|---|
| Lanza | arma cuerpo a cuerpo sencilla | `equipo/armas.yaml` (`1d6 perforante`) | No |
| Daga ×5 | arma sencilla, ligera | `equipo/armas.yaml` (`1d4 perforante`) | No |
| Paquete de explorador | equipo de aventurero | `equipo/aventureros.yaml` | No |
| Bastón | arma sencilla | `equipo/armas.yaml` (`1d6 contundente`) | No |
| Útiles de herborista | herramienta | `equipo/herramientas.yaml` | No |
| Aceite ×3, Lámpara, Libro, Petate, Ropas de viaje | equipo de aventurero | `equipo/aventureros.yaml → tabla_peso_precio` | No |

**Contenido del paquete**, por si escondiera una armadura:
`equipo/aventureros.yaml → "Paquete de explorador"`: «Contiene: 10 antorchas,
cantimplora, cuerda, 2 frascos de aceite, mochila, petate, raciones para 10 días
y yesquero.» Ninguna armadura, ningún escudo.

Ojo con «Ropas de viaje»: aparece en `equipo/aventureros.yaml →
tabla_peso_precio` como equipo de aventurero (2 kg, 2 po), **no** en
`equipo/armaduras.yaml`. No es armadura.

Refuerzo coherente: la ficha declara `competencias.armaduras: []`, que es lo que
manda `clases/monje.yaml → atributos_basicos.armaduras: []` — el Monje no tiene
entrenamiento con ninguna armadura ni con escudos.

→ **La condición se cumple: ni armadura ni escudo.** El rasgo aplica.

### 2.3 Cálculo

    CA = 10 + mod_des + mod_sab
       = 10 + 2 + 3
       = 15

### 2.4 Otros efectos sobre `ca` — ninguno aplica

Por `grep` de `objetivo: ca` sobre las fuentes declaradas:
`clases/rasgos/barbaro.yaml` (Defensa sin armadura de bárbaro, otra clase),
`clases/subclases/bardo.yaml` (Danzarín, subclase ajena), `clases/subclases/
hechicero.yaml` (Resistencia dracónica, subclase ajena), `clases/subclases/
druida.yaml` y `clases/subclases/paladin.yaml` (condicionales de subclases
ajenas), `dotes/generales.yaml` (dotes que no tiene), y
`dotes/estilo_de_combate.yaml → Defensa` (`+1`, pero `requiere: [con_armadura]` —
doblemente inaplicable: no tiene la dote y no lleva armadura). Ninguno toca a
este personaje.

Tampoco entra en juego `reglas/generacion_personaje.yaml →
multiclase.clase_de_armadura` («si el personaje tiene varias formas de calcular
su CA… solo puede beneficiarse de una»): aquí solo hay una forma.

### 2.5 Hallazgo — la base no declara la CA por defecto sin armadura

**Este cálculo no lo necesita**, porque Defensa sin armadura declara una base
completa y propia. Pero al buscarla me encontré con que **la base no define en
ningún sitio la CA por defecto de una criatura sin armadura (10 + modificador de
Destreza)**.

Dónde lo busqué, sin encontrarlo:
- `equipo/armaduras.yaml → reglas`: solo `entrenamiento`, `sin_entrenamiento`,
  `escudos`, `solo_un_tipo`, `fuerza` y `sigilo`. La tabla da la CA **de cada
  armadura**, nunca la de no llevar ninguna.
- `reglas/generacion_personaje.yaml`: solo la mención de multiclase citada arriba.
- `reglas/habilidades.yaml`, `reglas/idiomas.yaml`, `reglas/prerrequisitos.yaml`,
  `reglas/subida_de_nivel.yaml`: nada.
- `grep -rn` de `"10 + "`, `"CA base"` y `"clase de armadura"` sobre `reglas/`,
  `equipo/`, `clases/`, `especies/`, `dotes/` y `trasfondos/`: los únicos
  aciertos son las cuatro fórmulas de defensa sin armadura (monje, bárbaro,
  bardo danzarín, hechicero dracónico), todas ellas bases de rasgo.

Consecuencia: un personaje sin armadura y **sin** rasgo de defensa sin armadura
—un mago con la túnica puesta, por ejemplo— no tiene de dónde derivar su CA con
esta base. Lo dejo escrito como hallazgo estructural; no bloquea esta ficha.

### → `ca` = **15**

---

## 3 · `velocidad` — en metros

### 3.1 Velocidad base de la especie

`especies/especies.yaml → especies[Dracónido].velocidad_m` = **9**
(`pagina: {pdf: 189, libro: 187}`; cabecera del fichero:
`fuente: {archivo: "Manual_del_Jugador_2024.pdf", capitulo: 4, paginas_pdf: "188-199"}`).

Ningún rasgo de Dracónido modifica la velocidad terrestre: «Vuelo dracónico»
concede velocidad **volando**, y además es de nivel 5 (`nivel: 5`) — el
personaje tiene 2.

### 3.2 Bonificador de Movimiento sin armadura

`clases/rasgos/monje.yaml → rasgos[Movimiento sin armadura]`
(`nivel: 2`, `pagina: {pdf: 152, libro: 150}`):

> «Tu velocidad aumenta en 3 m si no llevas armadura ni portas un escudo. Este
> bonificador aumenta con el nivel (columna "Movimiento sin armadura" de la
> tabla): +4,5 m en nivel 6, +6 m en nivel 10, +7,5 m en nivel 14, +9 m en nivel 18.»

    {objetivo: velocidad, op: add, columna: mov_sin_armadura_m,
     requiere: [sin_armadura, sin_escudo], pagina: {pdf: 152, libro: 150}}

Fíjese en que la cantidad **no** está en el texto del efecto: se lee de la
columna. El propio fichero lo advierte en un comentario junto al rasgo («El
escalado NO se copia aquí: se lee de la columna `mov_sin_armadura_m`»).

Valor de la columna a nivel de monje 2: `clases/monje.yaml → progresion`, fila
`{n: 2, pb: 2, artes_marciales: d6, puntos_concentracion: 2,
mov_sin_armadura_m: 3, rasgos: ["Concentración de monje", "Metabolismo
asombroso", "Movimiento sin armadura"]}` → **+3 m**.

Las dos lecturas (texto del rasgo y columna de la tabla) coinciden en 3 m: no hay
ambigüedad que resolver. El salto a 4,5 m no llega hasta el nivel 6.

El personaje tiene el rasgo: aparece en `rasgos` de esa misma fila de nivel 2.

### 3.3 Condición y penalizaciones

- `[sin_armadura, sin_escudo]`: **se cumple** — la comprobación objeto a objeto
  está en 2.2, y vale igual aquí.
- `equipo/armaduras.yaml → reglas.fuerza` («Si la tabla indica una puntuación de
  Fuerza para un tipo de armadura, esta reduce 3 m la velocidad de quien la
  lleve, salvo que su Fuerza sea igual o superior a la indicada»): **no aplica**,
  no lleva armadura de ningún tipo. (Aunque la llevara, solo cota de malla,
  bandas y placas indican puntuación de Fuerza.)
- Otros efectos sobre `velocidad` en la base (`grep objetivo: velocidad`):
  `especies/especies.yaml` (Goliat, Forma grande — otra especie, y condicional),
  `clases/rasgos/barbaro.yaml` y `clases/rasgos/explorador.yaml` (otras clases),
  `clases/subclases/{explorador,paladin,monje}.yaml` (rasgos de subclase; el del
  monje es `op: conditional` y de subclase, que este personaje no tiene),
  `dotes/generales.yaml` y `dotes/don_epico.yaml` (dotes que no tiene). **Ninguno
  aplica.**

### 3.4 Cálculo

    velocidad = 9 (Dracónido) + 3 (Movimiento sin armadura, nivel 2)
              = 12 m

### → `velocidad` = **12 m**

---

## 4 · `cd_conjuros` y `bonif_ataque_conjuros` — NO PROCEDE

**Sarv Escamagris no lanza conjuros.** No hay CD de conjuros ni bonificador de
ataque de conjuros que calcular. Lo justifico fuente por fuente, porque «no
procede» solo vale si se ha mirado en todas.

### 4.1 La clase

`clases/monje.yaml → lanzador` = **`ninguno`**.

Y, coherentemente, **`clases/monje.yaml` no tiene campo `aptitud_magica`**.
Contraste con el patrón del resto de clases (`grep` de `lanzador`/`aptitud_magica`
sobre `clases/*.yaml`):

| Clase | `lanzador` | `aptitud_magica` |
|---|---|---|
| Bardo, Clérigo, Druida, Hechicero, Mago | `completo` | Carisma / Sabiduría / Sabiduría / Carisma / Inteligencia |
| Explorador, Paladín | `medio` | Sabiduría / Carisma |
| Brujo | `pacto` | Carisma |
| **Bárbaro, Guerrero, Monje, Pícaro** | **`ninguno`** | **(no lo declaran)** |

Esto importa porque la fórmula que la base sí trae —
`reglas/generacion_personaje.yaml → conjuros` (`pagina: {pdf: 240, libro: 238}`,
sección «Tiradas de salvación / Tiradas de ataque»):

- `cd_salvacion.formula`: «8 + modificador de aptitud mágica + bonificador por competencia»
- `bonificador_ataque.formula`: «modificador de aptitud mágica + bonificador por competencia»

— tiene un término, «modificador de aptitud mágica», que en este personaje **no
existe**. El mismo campo dice de dónde debería salir
(`conjuros._nota_aptitud`: «La aptitud mágica de cada clase la declara su propio
fichero, en `clases/<clase>.yaml → aptitud_magica`»), y `clases/monje.yaml` no lo
declara. No es que falte el dato en la base: es que la regla **no tiene sujeto**
aquí.

*(Anoto de paso, por si sirve al contraste: esta fórmula está en la base desde
hoy mismo. El comentario que la precede en `reglas/generacion_personaje.yaml`
cuenta que vivía solo en `calculo.py` y que la destapó esta misma tanda de
«calculista». O sea que el hallazgo que el encargo me pone de ejemplo ya está
corregido; lo confirmo leyendo el campo, que ahora existe y es citable.)*

### 4.2 La subclase — no hay

`clases[0].subclase: null` en la ficha. Y no podría haberla:
`clases/monje.yaml → progresion`, fila `{n: 3, …, rasgos: ["Desviar ataques",
"Subclase de monje"]}` — la subclase de monje entra en el **nivel 3**, y el
personaje tiene 2.

Además, aunque la tuviera: de las cuatro subclases de
`clases/subclases/monje.yaml` (Guerrero de la Mano Abierta, de la Misericordia,
de la Sombra, de los Elementos), solo dos conceden magia —Guerrero de la Sombra
(«Artes sombrías»: truco *ilusión menor*, aptitud mágica Sabiduría) y Guerrero de
los Elementos («Manipular los elementos»: conjuro *elementalismo*, aptitud mágica
Sabiduría)— y ambas a partir de nivel 3.

### 4.3 La especie — no da conjuros

`especies/especies.yaml → especies[Dracónido].rasgos`: Linaje dracónico, Ataque
de aliento, Resistencia al daño, Visión en la oscuridad y Vuelo dracónico
(nivel 5). Ninguno concede trucos ni conjuros ni declara aptitud mágica.

Esto no es trivial: en el mismo fichero, Elfo («Linaje élfico»), Tiefling
(«Legado infernal», «Presencia sobrenatural»), Aasimar («Portador de luz») y
Gnomo («Linaje gnomo») **sí** conceden trucos y declaran aptitud mágica. El
Dracónido es de los que no.

### 4.4 El trasfondo y la dote — no dan conjuros

- `trasfondos/trasfondos.yaml → trasfondos[Ermitaño].dote` = **Sanador**.
- `dotes/origen.yaml → dotes[Sanador]` (`pagina: {pdf: 204, libro: 202}`):
  «Médico de batalla» (gastar un uso de útiles de sanador para que una criatura
  gaste y tire un dado de PG) y «Repetir tiradas de curación». **Ningún conjuro,
  ninguna aptitud mágica.**

Contraste dentro del mismo fichero: `dotes[Iniciado en la magia]` sí concede dos
trucos y un conjuro de nivel 1, y sí hace elegir aptitud mágica. Si el Ermitaño
diera esa dote, el cálculo procedería. No la da.

### 4.5 Dos CD que este personaje SÍ tiene — y que no son `cd_conjuros`

Las dejo escritas para que nadie las confunda con la CD de conjuros al contrastar:

- **Ataque de aliento** (`especies/especies.yaml → especies[Dracónido].rasgos`):
  «TdS de Destreza CD 8 + mod. Constitución + PB» = 8 + 2 + 2 = **12**.
- **Concentración de monje** (`clases/rasgos/monje.yaml → rasgos[Concentración de
  monje]`, `nivel: 2`, `pagina: {pdf: 151, libro: 149}`): «Cuando un rasgo de
  monje que usa puntos de concentración exige salvación, la CD es 8 + tu
  modificador de Sabiduría + tu bonificador por competencia» = 8 + 3 + 2 = **13**.
  A nivel 2 es una CD latente: los tres rasgos de puntos de concentración que
  tiene (Defensa paciente, Paso del viento, Ráfaga de golpes) no exigen salvación;
  la primera que la exige es Golpe aturdidor, de nivel 5.

Son CD de rasgo, con sus propios términos (Constitución en una, Sabiduría en la
otra), no la CD de conjuros de `reglas/generacion_personaje.yaml → conjuros`.

### → `cd_conjuros` y `bonif_ataque_conjuros`: **no aplican** (personaje no lanzador)

---

## Valores derivados

| Valor | Resultado | Derivación en una línea | Cita principal |
|---|---|---|---|
| `pg_max` | **17** | (8 máx. d8 + 5 valor establecido) + 2 niveles × mod_con +2 | `reglas/generacion_personaje.yaml → puntos_golpe.nivel_1` {pdf 42, libro 40} y `→ puntos_golpe.niveles_siguientes_al_1` {pdf 44, libro 42}; `clases/monje.yaml → atributos_basicos.dado_golpe` |
| `ca` | **15** | 10 + mod_des (+2) + mod_sab (+3), sin armadura ni escudo | `clases/rasgos/monje.yaml → rasgos[Defensa sin armadura]` {pdf 151, libro 149} |
| `velocidad` | **12 m** | 9 m (Dracónido) + 3 m (Movimiento sin armadura, nivel 2) | `especies/especies.yaml → especies[Dracónido].velocidad_m` {pdf 189, libro 187}; `clases/rasgos/monje.yaml → rasgos[Movimiento sin armadura]` {pdf 152, libro 150} + `clases/monje.yaml → progresion[n=2].mov_sin_armadura_m` |
| `cd_conjuros` | **no procede** | el Monje no lanza conjuros y ninguna otra fuente le da magia | `clases/monje.yaml → lanzador: ninguno` (y sin `aptitud_magica`) |
| `bonif_ataque_conjuros` | **no procede** | ídem | ídem |

**Intermedios** (por si el contraste los necesita):
mod_fue +1 · mod_des +2 · mod_con +2 · mod_int +0 · mod_sab +3 · mod_car −1 ·
PB +2 · dado de golpe d8 · dado de Artes marciales d6 · puntos de concentración 2.

## Lo que no he podido derivar

Nada de lo pedido se quedó sin derivar. El único hueco que encontré en la base
es colateral y está en **2.5**: no existe declarada en ningún fichero la CA por
defecto de una criatura sin armadura (10 + modificador de Destreza). No afecta a
esta ficha, porque Defensa sin armadura de monje declara una base propia y
completa, pero sí afectaría a cualquier personaje sin armadura que no tenga un
rasgo de defensa sin armadura.

---

## Veredicto

*Bloque añadido el 2026-09-08 (fase 2.0 del `PLAN_22`). Los números NO se han
tocado: se transcriben de la tabla final de este mismo informe, escrita antes,
y sin mirar lo que da el motor. Existe para que esta derivación se pueda
**volver a contrastar**: hasta hoy se comprobaba una vez, a ojo, el día que se
escribió, y nunca más — así que un motor que cambiara dejaba el informe viejo y
la ficha seguía diciendo «lo verificó un agente». Lo contrasta ahora
`verificar_personaje.verificar_veredicto` en cada pasada.*

```veredicto
pg_max: 17
ca: 15
velocidad: 12
cd_conjuros: no_procede
bonif_ataque_conjuros: no_procede
```
