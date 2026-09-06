# Cálculo ciego a mano — Vurga Piedra-Tozuda (Bárbaro Berserker, nivel 20)

**Agente:** E · «el calculista» — ronda 3 de estrés
**Fecha:** 2026-09-06
**Ficha:** `barbaro_berserker_n20`

## Método

Transcripción independiente. He derivado a mano `pg_max`, `ca`, `velocidad` y
—cuando procediera— `cd_conjuros` / `bonif_ataque_conjuros` a partir de los
**datos crudos** de la ficha y de la **base canónica** (`reglas/`, `clases/`,
`especies/`, `trasfondos/`, `dotes/`, `equipo/`, `hechizos.json`), sin abrir
ninguna implementación ni ningún verificador, y sin haber visto ningún número
producido por el proyecto.

### Entrada

- `/tmp/claude-0/-home-user-dnd/ccce6f54-5659-5d7c-89a3-15e0f610e8cf/scratchpad/crudos/barbaro_berserker_n20.yaml`
  (ficha sin bloque `calculado`)

### Ficheros de la base consultados

| Fichero | Para qué |
|---|---|
| `reglas/generacion_personaje.yaml` | modificadores por puntuación; PG nivel 1; PG niveles siguientes; tabla de valores establecidos; retroactividad de Constitución; fórmula de CD de conjuros; tabla de PB |
| `reglas/caracteristicas.yaml` | emparejamiento nombre ↔ abreviatura (`con` = Constitución, etc.) |
| `reglas/subida_de_nivel.yaml` | qué concede la base al subir de nivel y qué elige el jugador |
| `clases/barbaro.yaml` | dado de golpe, `lanzador`, progresión (PB, rasgos por nivel), competencias, ausencia de `aptitud_magica` |
| `clases/rasgos/barbaro.yaml` | Defensa sin armadura, Movimiento rápido, Campeón primordial, Furia |
| `clases/subclases/barbaro.yaml` | Senda del Berserker (los cuatro rasgos) |
| `especies/especies.yaml` | Aasimar: `velocidad_m`, rasgos |
| `trasfondos/trasfondos.yaml` | Campesino: características y dote de origen |
| `dotes/origen.yaml` | Duro |
| `dotes/generales.yaml` | Veloz; «Mejora de característica» |
| `dotes/don_epico.yaml` | Don de la fortaleza |
| `equipo/armaduras.yaml` | Media armadura y reglas generales de armadura |
| `hechizos.json` | el truco *luz* (¿lleva ataque o salvación?) |

### Desviaciones cometidas

**Ninguna.** No he abierto `calculo.py`, `efectos.py`, `reglas/efectos.yaml`,
`validar.py`, `verificar_*.py`, `censo.py`, `cobertura.py`, `generar_ficha.py`,
`subir_nivel.py`, `buscar.py`, ningún fichero de `personajes/`, ni ningún otro
fichero de `_verificacion/`. No he listado el directorio en el que escribo
(`mkdir -p` + escritura directa). No he ejecutado ningún verificador; el único
código que he ejecutado es un `python3 -c` de tres líneas para *leer* un
registro de `hechizos.json`, sin calcular nada con él.

Doy por buena, por indicación del encargo, la CA por defecto sin armadura
(`10 + mod. Des`) declarada en el fichero vetado. En esta ficha no hace falta.

---

## 0. Valores previos que necesitan los cuatro apartados

### 0.1 Bonificador por competencia

- `clases/barbaro.yaml → progresion[n=20].pb` = **6**.
- Contrastado con `reglas/generacion_personaje.yaml → px_por_nivel` fila
  `{nivel: 20, px: 355000, pb: 6}`. Coinciden.

**PB = +6.**

### 0.2 Cadena de puntuaciones de característica

Fórmula del modificador: `reglas/generacion_personaje.yaml →
metodos_generacion_caracteristicas.modificadores_por_puntuacion.formula` =
«(puntuación − 10) / 2, redondeando hacia abajo».

Reconstrucción de la cadena, paso a paso:

| Paso | Cita | fue | des | con |
|---|---|---|---|---|
| Conjunto estándar (Bárbaro) | `reglas/generacion_personaje.yaml → conjunto_estandar_por_clase.filas[Bárbaro]` = fue 15, des 13, con 14 | 15 | 13 | 14 |
| Ajuste de trasfondo Campesino (+2/+1) | `trasfondos/trasfondos.yaml → Campesino.caracteristicas` = [Fuerza, Constitución, Sabiduría]; crudo `caracteristicas.ajuste_trasfondo` = fue +2, con +1 | 17 | 13 | 15 |
| Nivel 4 · dote Veloz (+1 Des) | `dotes/generales.yaml → Veloz.mejora_caracteristica` {cantidad 1, entre [Destreza, Constitución]} | 17 | **14** | 15 |
| Nivel 8 · Mejora de característica (+2 Fue) | `dotes/generales.yaml → "Mejora de característica"` {cantidad 2, máximo 20} | **19** | 14 | 15 |
| Nivel 12 · Mejora de característica (+2 Con) | ídem | 19 | 14 | **17** |
| Nivel 16 · Mejora de característica (+2 Con) | ídem | 19 | 14 | **19** |
| Nivel 19 · Don de la fortaleza (+1 Con) | `dotes/don_epico.yaml → "Don de la fortaleza".mejora_caracteristica` {cantidad 1, máximo 30} | 19 | 14 | **20** |
| Nivel 20 · **Campeón primordial** (+4 Fue y +4 Con, máx. 25) | `clases/rasgos/barbaro.yaml → rasgos["Campeón primordial"]`, nivel 20, pág. pdf 55 / libro 53 | **23** | 14 | **24** |

Comprobaciones de legitimidad:
- Las cuatro ranuras de «Mejora de característica» del Bárbaro son los niveles
  4, 8, 12 y 16 (`clases/barbaro.yaml → progresion`). La ficha gasta la de
  nivel 4 en la dote Veloz y las otras tres en subidas de +2. Cuadra.
- Prerrequisito de Veloz: «nivel 4 o más, Destreza o Constitución 13 o más».
  En el nivel 4 tenía Des 13. **Se cumple.**
- Prerrequisito de Don de la fortaleza: «nivel 19 o más». **Se cumple.**
- Ningún ASI supera el tope de 20 (`máximo: 20`): Con llega justo a 20.
- Campeón primordial tiene tope 25: Fue 23 ≤ 25, Con 24 ≤ 25. **Cabe.**

**Los siete pasos primeros coinciden exactamente con el bloque
`caracteristicas.final` del crudo (fue 19, con 20, des 14). El octavo no está
en él.** Ver §1.2.

Modificadores resultantes (con el octavo paso aplicado):

| Característica | Puntuación | Cálculo | Modificador |
|---|---|---|---|
| Fuerza | 23 | (23−10)/2 = 6,5 → 6 | **+6** |
| Destreza | 14 | (14−10)/2 = 2 | **+2** |
| Constitución | 24 | (24−10)/2 = 7 | **+7** |
| Carisma | 8 | (8−10)/2 = −1 | **−1** |

(La tabla `modificadores_por_puntuacion.tabla` de la base solo llega a 20; para
23 y 24 aplico la `formula` del mismo campo, que es la que la tabla tabula.)

---

## 1. `pg_max`

### 1.1 Los veinte niveles, uno a uno

**Regla del nivel 1** — `reglas/generacion_personaje.yaml →
puntos_golpe.nivel_1.regla` (pág. pdf 42 / libro 40): «Máximo del dado de golpe
+ modificador por Constitución».

**Regla de los niveles 2 a 20** — `reglas/generacion_personaje.yaml →
puntos_golpe.niveles_siguientes_al_1.literal` (pág. pdf 44 / libro 42):
«Tira ese dado, suma tu modificador por Constitución al resultado y añade el
total (mínimo de 1) a tus puntos de golpe máximos. En vez de tirar, puedes
utilizar el valor establecido que se muestra en la tabla…».

Dado de golpe del Bárbaro: `clases/barbaro.yaml →
atributos_basicos.dado_golpe` = **d12**.

Valor establecido del Bárbaro: `reglas/generacion_personaje.yaml →
puntos_golpe.niveles_siguientes_al_1.tabla_valores_establecidos.filas` →
`{clases: [Bárbaro], valor: 7}` = **7**.

Auditoría entrada por entrada de `pg_por_nivel` del crudo:

| Nivel(es) | `clase` | `metodo` | `valor` | Legitimidad |
|---|---|---|---|---|
| 1 | Bárbaro | `maximo_dado` | 12 | Máximo de un d12 = 12. **Legítimo.** |
| 2 – 20 (19 entradas) | Bárbaro | `valor_establecido` | 7 cada una | Tabla: Bárbaro = 7. **Legítimo en las 19.** |

Ninguna entrada usa el método `tirar`, así que no hay ninguna tirada que haya
que aceptar a ciegas ni ningún mínimo de 1 que aplicar. Hay exactamente una
entrada por nivel, del 1 al 20, sin huecos ni repeticiones, y todas de la misma
clase (no hay multiclase).

**El campo `valor` guarda solo el término del dado, no el del modificador.**
Se ve en el nivel 1: 12 es el máximo del d12 pelado, sin sumarle Constitución,
aunque la regla del nivel 1 sí manda sumarla. El término de Constitución va
aparte, por lo que dice el punto siguiente.

Suma del término del dado:

    nivel 1 .......... 12
    niveles 2–20 ..... 19 × 7 = 133
    ────────────────────────────────
    total dados ...... 145

### 1.2 El término de Constitución es retroactivo — y aquí la Constitución cambia cuatro veces

`reglas/generacion_personaje.yaml → puntos_golpe.aumento_de_constitucion`
(pág. pdf 44 / libro 42), `fidelidad: literal`:

> «Cuando tu modificador por Constitución aumente en 1, tus puntos de golpe
> máximos también aumentarán en 1 por cada nivel que hayas alcanzado.»

Y el propio campo `_nota_para_el_motor` del mismo bloque cierra la forma:

> «El término de Constitución es `nivel_total × mod_con` y se recalcula entero
> cuando el modificador sube; solo el término del dado es historia acumulada.»

He comprobado la equivalencia a mano con el ejemplo de la propia regla: si el
modificador pasa de +2 a +3 al alcanzar el nivel 12, la lectura incremental da
11 niveles a +2 (22) + el nivel 12 con el modificador viejo (2) + el bono
retroactivo de 1 por cada uno de los 12 niveles alcanzados (12) = 36 = 12 × 3.
Coincide con la forma cerrada. **Uso la forma cerrada.**

¿Cambia aquí la Constitución a mitad de camino? **Sí, cuatro veces:**

| Desde el nivel | Puntuación Con | Modificador | Causa |
|---|---|---|---|
| 1 | 15 | +2 | base 14 + 1 del trasfondo Campesino |
| 12 | 17 | +3 | Mejora de característica |
| 16 | 19 | +4 | Mejora de característica |
| 19 | 20 | +5 | Don de la fortaleza |
| 20 | 24 | **+7** | Campeón primordial (+4) |

Por la retroactividad, **los cuatro cambios intermedios no dejan rastro
propio**: solo cuenta el modificador final multiplicado por el nivel total.
(Un motor que sumase «lo ganado en cada nivel» y lo congelase daría 203 + bonos
= 283, que es la cifra equivocada que la propia nota de la base advierte.)

    término de Constitución = nivel_total × mod_con = 20 × 7 = 140

### 1.3 Los dos sumandos fijos de las dotes

**Duro** (dote de origen, concedida por el trasfondo Campesino —
`trasfondos/trasfondos.yaml → Campesino.dote: "Duro"`):
`dotes/origen.yaml → Duro.descripcion` (pág. pdf 203 / libro 201): «Tus PG
máximos aumentan en una cantidad igual al doble de tu nivel de personaje al
adquirir esta dote. A partir de entonces, cada vez que subas de nivel, tus PG
máximos aumentan 2 puntos adicionales.» Las dos mitades juntas equivalen a
`2 × nivel_total` en todo nivel posterior:

    Duro = 2 × 20 = +40

**Don de la fortaleza** (don épico de nivel 19 — `clases/rasgos/barbaro.yaml →
rasgos["Don épico"]`, nivel 19): `dotes/don_epico.yaml → "Don de la
fortaleza".descripcion` (pág. pdf 212 / libro 210): «Salud fortalecida: PG
máximos +40.» Sin condición ni duración:

    Don de la fortaleza = +40

La segunda mitad de esa dote («cada vez que recuperes PG, puedes recuperar PG
adicionales iguales a tu modificador por Constitución») es **curación
situacional, no máximo**: **descartada** del número de la ficha.

### 1.4 Lo que descarto y por qué

- **Furia implacable** (nivel 11): pone los PG «a una cantidad igual al doble de
  tu nivel de bárbaro» al caer a 0. Es un efecto de combate sobre los PG
  actuales, no sobre el máximo. **Situacional: fuera.**
- **Manos curativas** (Aasimar) y **Vitalidad del árbol** / PG temporales: no es
  la subclase de esta ficha, y los PG temporales nunca son máximo. **Fuera.**
- **Senda del Berserker**: ninguno de sus cuatro rasgos (Frenesí, Furia
  irracional, Represalia, Presencia intimidante) toca los PG. **Nada que sumar.**

### 1.5 Total

    dados ......................... 145
    Constitución (20 × +7) ........ 140
    Duro .......................... + 40
    Don de la fortaleza ........... + 40
    ─────────────────────────────────────
    pg_max ........................  365

### 1.6 La duda, y por qué elijo esta lectura

Las dos lecturas posibles son:

- **Lectura A — aplicar Campeón primordial (la que elijo): `pg_max = 365`.**
  El personaje tiene 20 niveles de Bárbaro, luego tiene el rasgo de nivel 20
  (`clases/barbaro.yaml → progresion[n=20].rasgos: ["Campeón primordial"]`), y
  su texto en `clases/rasgos/barbaro.yaml` dice, sin condición, sin duración,
  sin coste y sin recurso que gastar: «Tus puntuaciones de Fuerza y
  Constitución aumentan en 4, hasta un máximo de 25.» Es un aumento
  **permanente** de puntuación, exactamente igual de permanente que el +1 de
  Con del Don de la fortaleza, que la ficha sí ha contabilizado. Y la regla de
  retroactividad de PG está escrita en genérico («cuando tu modificador por
  Constitución aumente»), sin restringirse a dotes.

- **Lectura B — no aplicarlo: `pg_max = 325`** (145 + 20×5 + 40 + 40). Es lo
  que sale si se toma `caracteristicas.final` del crudo como cerrado e
  intocable: ese bloque da con 20 / fue 19, es decir, base + trasfondo +
  mejoras + dotes, **sin** el rasgo de clase de nivel 20.

**Elijo A** porque el encargo es derivar de la regla citada, no de un campo
intermedio de la ficha; y la regla de nivel 20 está en la base, con página, y
es incondicional. Lo digo con todas las letras porque tiene consecuencias más
allá de los PG: **si `caracteristicas.final` es el bloque del que se alimentan
los cálculos, Campeón primordial no está entrando en ninguna parte**, y eso
mueve `pg_max` en 40 puntos, el modificador de Fuerza de +4 a +6 y el de
Constitución de +5 a +7.

---

## 2. `ca`

### 2.1 Qué lleva puesto

`equipo` del crudo: una única entrada,
`equipo/armaduras.yaml#Media armadura`. **No hay escudo.**

`equipo/armaduras.yaml → armaduras_medias.tabla` →
`{nombre: "Media armadura", ca: "15 + mod. Des (máx. 2)", fuerza: null,
sigilo: Desventaja, peso_kg: 20, precio: "750 po"}`.

### 2.2 Derivación

    base de la armadura ................... 15
    mod. Des = +2, tope de la media ....... +2   (min(+2, 2) = +2)
    escudo ................................  0   (no lleva)
    ──────────────────────────────────────────
    ca ....................................  17

### 2.3 Lo que descarto y por qué

- **Defensa sin armadura** (`clases/rasgos/barbaro.yaml`, nivel 1, pág. pdf 53 /
  libro 51): «*Mientras no lleves armadura alguna*, tu clase de armadura base es
  10 + modificador de Destreza + modificador de Constitución». **La condición no
  se cumple: lleva Media armadura.** Fuera.
  Observación, no cambio: con Con 24 esa vía daría 10 + 2 + 7 = **19**, más que
  los 17 de la armadura. La regla de `reglas/generacion_personaje.yaml →
  multiclase.clase_de_armadura` («solo puede beneficiarse de una, a elegir»)
  permitiría escoger — pero solo si se quitara la armadura, y la ficha la lleva.
  El número de la ficha es 17.
- **Furia** no modifica la CA (da resistencia al daño, no CA). Fuera.
- **Media armadura** tiene `fuerza: null`: no hay requisito de Fuerza, así que
  no se activa la regla `reglas.fuerza`. Y la columna Sigilo (Desventaja) no es
  un número de CA.
- El bárbaro **sí es competente** con armaduras medias
  (`clases/barbaro.yaml → atributos_basicos.armaduras`), así que no se aplica
  `reglas.sin_entrenamiento`. En cualquier caso esa penalización tampoco toca la
  CA.

### 2.4 Un hueco menor que declaro

La entrada de `equipo` **no lleva ningún campo `equipada`/`llevada`**: solo
`ref` y `origen`. Interpreto «está en el equipo» = «la lleva puesta», que es la
única lectura que produce un número, y la que hace que la Media armadura llegue
a la ficha. Si la base pretende distinguir poseer de llevar, ese campo no
existe todavía.

---

## 3. `velocidad`

### 3.1 Base de especie

`especies/especies.yaml → Aasimar.velocidad_m` = **9 m**.

### 3.2 El rasgo de clase con condición

**Movimiento rápido** — `clases/barbaro.yaml → progresion[n=5].rasgos` lo
concede en el nivel 5; el texto está en `clases/rasgos/barbaro.yaml →
rasgos["Movimiento rápido"]` (pág. pdf 54 / libro 52):

> «Tu velocidad aumenta en 3 m **mientras no lleves armadura pesada**.»

La condición es *no pesada*, no *sin armadura*. El equipo es **Media
armadura**, que `equipo/armaduras.yaml` clasifica en `armaduras_medias`, no en
`armaduras_pesadas`. **La condición se cumple: +3 m.**

(El propio fichero lo subraya en su comentario: «mientras no lleves armadura
PESADA: con ligera o media lo conserva». Es la trampa del apartado y aquí no
salta.)

### 3.3 La dote

**Veloz** — `dotes/generales.yaml → Veloz.descripcion` (pág. pdf 211 / libro
209): «Aumento de velocidad: tu velocidad aumenta 3 m.» Sin condición ni
duración: permanente. **+3 m.**

### 3.4 Derivación

    base Aasimar ..................  9 m
    Movimiento rápido (nivel 5) ... +3 m   (no lleva armadura pesada ✓)
    Veloz (dote, nivel 4) ......... +3 m
    ───────────────────────────────────────
    velocidad ..................... 15 m

### 3.5 Lo que descarto y por qué

- **Revelación celestial → Alas celestiales** (Aasimar, nivel 3): da «velocidad
  volando igual a tu velocidad» durante 1 minuto, 1 vez por descanso largo. Es
  **situacional** *y además* es una velocidad de vuelo, no la velocidad a pie
  de la ficha. **Fuera por partida doble.**
- **Don de la velocidad** (`dotes/don_epico.yaml`, +9 m): esta ficha tomó **Don
  de la fortaleza**, no este. **No aplica.**
- **Regla de Fuerza de armadura** (`equipo/armaduras.yaml → reglas.fuerza`,
  −3 m): la Media armadura tiene `fuerza: null`. **No se activa.**
- **Salto instintivo** (nivel 7): mueve «hasta la mitad de tu velocidad» dentro
  de la acción adicional de furia. Consume velocidad, no la aumenta. **Fuera.**
- **Golpe brutal → Golpe ralentizador** reduce la velocidad *del objetivo*.
  **Fuera.**
- **Senda del Berserker**: ninguno de sus cuatro rasgos toca la velocidad.
- La velocidad **no** depende del modificador de Constitución, así que la duda
  de §1.6 no la afecta: 15 m en ambas lecturas.

---

## 4. `cd_conjuros` y `bonif_ataque_conjuros`

### NO PROCEDE. El personaje no es lanzador de conjuros.

Pruebas, en orden:

1. `clases/barbaro.yaml → lanzador: ninguno`. Es explícito.
2. `clases/barbaro.yaml` **no declara ningún campo `aptitud_magica`**, que es
   justo de donde `reglas/generacion_personaje.yaml → conjuros._nota_aptitud`
   dice que hay que sacarlo: «La aptitud mágica de cada clase la declara su
   propio fichero, en `clases/<clase>.yaml → aptitud_magica`». Sin aptitud
   mágica no hay ningún modificador que meter en la fórmula.
3. `clases/barbaro.yaml → columnas_extra: [furias, dano_furia, maestria_armas]`:
   la progresión del Bárbaro no tiene columnas `trucos`, `prep` ni `slots`.
4. **Senda del Berserker** no concede conjuros (a diferencia de Senda del
   Corazón Salvaje, que sí y que además declara «La Sabiduría es tu aptitud
   mágica» — no es esta subclase).
5. Ninguna de las tres dotes concede lanzamiento de conjuros (Duro, Veloz, Don
   de la fortaleza). La dote que lo haría, «Iniciado en la magia», no está aquí.
6. El propio rasgo **Furia** dice que mientras estás enfurecido «no puedes
   mantener la concentración ni lanzar conjuros».

Para que conste, la fórmula que **no** aplico está en
`reglas/generacion_personaje.yaml → conjuros` (pág. pdf 240 / libro 238):
`cd_salvacion` = «8 + modificador de aptitud mágica + bonificador por
competencia»; `bonificador_ataque` = «modificador de aptitud mágica +
bonificador por competencia». No es un hueco de la base: está declarada con
página. Lo que falta es el lanzador.

### El matiz que sí hay que nombrar: el truco de la especie

El Aasimar trae **Portador de luz** (`especies/especies.yaml → Aasimar.rasgos`):
«Conoces el truco *luz*. El Carisma es tu aptitud mágica para lanzarlo.» O sea:
este personaje **sí conoce un conjuro**, con aptitud mágica declarada, aunque su
clase no sea lanzadora.

¿Le hace falta una CD o un bonificador de ataque? **No.** He mirado el conjuro
en `hechizos.json`: *Luz*, nivel 0, `"tirada": "Directo"`, y su descripción
(«Tocas un objeto Grande o más pequeño que nadie lleve o vista…») **no pide
tirada de ataque ni tirada de salvación**. Ninguno de los dos valores llega a
usarse nunca.

Si aun así alguien quisiera anotarlos por el truco, saldrían:
`8 + (−1) + 6 = 13` y `(−1) + 6 = +5`. **No los propongo como valor de ficha**:
la fórmula del manual habla de la aptitud mágica del lanzador, y aquí no hay
rasgo de Lanzamiento de conjuros que la fije para el personaje, solo para un
truco concreto que no la gasta.

Y una advertencia para no confundir cosas: la CD «8 + mod. Carisma + PB» que
aparece en **Revelación celestial → Mortaja necrótica** (Aasimar) y la
«CD 8 + mod. Fuerza + PB» de **Presencia intimidante** (Berserker, nivel 14) son
**CD de rasgo**, no `cd_conjuros`. Coinciden en forma con la fórmula de conjuros
pero se calculan con otra característica y no deben escribirse en ese campo.

---

## Valores derivados

| Valor | Resultado | Derivación en una línea | Cita principal |
|---|---|---|---|
| `pg_max` | **365** | 12 (máx. d12) + 19×7 (valor establecido) + 20×(+7) (Con retroactiva) + 40 (Duro) + 40 (Don de la fortaleza) | `reglas/generacion_personaje.yaml → puntos_golpe.*`; `dotes/origen.yaml → Duro`; `dotes/don_epico.yaml → "Don de la fortaleza"`; `clases/rasgos/barbaro.yaml → "Campeón primordial"` |
| `pg_max` *(lectura alternativa B, sin Campeón primordial)* | *325* | 145 + 20×(+5) + 40 + 40 | ídem, tomando `caracteristicas.final` como cerrado |
| `ca` | **17** | 15 (Media armadura) + min(mod. Des +2, tope 2) + 0 (sin escudo) | `equipo/armaduras.yaml → armaduras_medias.tabla["Media armadura"]` |
| `velocidad` | **15 m** | 9 (Aasimar) + 3 (Movimiento rápido, no lleva pesada) + 3 (Veloz) | `especies/especies.yaml → Aasimar.velocidad_m`; `clases/rasgos/barbaro.yaml → "Movimiento rápido"`; `dotes/generales.yaml → Veloz` |
| `cd_conjuros` | **no procede** | el Bárbaro es `lanzador: ninguno` y no declara `aptitud_magica`; el único conjuro (truco *luz*, del Aasimar) no usa CD | `clases/barbaro.yaml → lanzador`; `hechizos.json → Luz.tirada = "Directo"` |
| `bonif_ataque_conjuros` | **no procede** | mismo motivo; *luz* tampoco pide tirada de ataque | ídem |

### Valores auxiliares usados (por si sirven de contraste)

| Valor | Resultado | Cita |
|---|---|---|
| Bonificador por competencia | +6 | `clases/barbaro.yaml → progresion[n=20].pb` (= `px_por_nivel[20].pb`) |
| mod. Fuerza | +6 (con Campeón primordial) / +4 (sin él) | §0.2 |
| mod. Destreza | +2 | §0.2 |
| mod. Constitución | +7 (con Campeón primordial) / +5 (sin él) | §0.2 |

---

## Lo que la base NO declara y he tenido que suplir

1. **`equipo[].equipada`** — no existe ningún campo que distinga «lo tengo» de
   «lo llevo puesto». Buscado en el crudo (`equipo`) y en
   `equipo/armaduras.yaml` (que sí declara `tiempo_equipar` y `reglas.solo_un_tipo`,
   pero no un campo de estado en la ficha). Interpretado como «puesta». Afecta a
   `ca` (17 con armadura) y, por rebote, a `velocidad` (la condición de
   Movimiento rápido) y a si Defensa sin armadura podría activarse.

2. **Modificadores por encima de 20** — `reglas/generacion_personaje.yaml →
   modificadores_por_puntuacion.tabla` se detiene en la fila `20: +5`, pero
   Campeón primordial y los dones épicos pueden llegar a 25 y 30. He usado la
   `formula` del mismo campo, que es la que la tabla tabula. No es un hueco de
   fondo, pero la tabla se queda corta para nivel 20.

3. **Campeón primordial y el bloque `caracteristicas`** — la base declara el
   rasgo con su texto y su página, pero la ficha no tiene ningún sitio donde ese
   +4/+4 pueda aterrizar: `caracteristicas` solo contempla `base`,
   `ajuste_trasfondo` y `final`, y `final` = base + trasfondo + mejoras + dotes.
   No es que falte la regla: falta el carril por el que un rasgo de clase mueva
   una puntuación. Es la causa de la doble lectura de §1.6.

---

## Apéndice · comprobación posterior sobre el punto 3

Escrito ya el informe, verifiqué el punto 3 en `reglas/fuentes_de_efectos.yaml`
(fichero de `reglas/` distinto de `efectos.yaml`, por tanto permitido). Confirma
lo que sospechaba y lo afila:

- `fuentes` incluye `{patron: "clases/rasgos/*.yaml", camino: [rasgos],
  que_es: "rasgos de clase"}`. Es decir, **Campeón primordial vive en un fichero
  que sí se recorre en busca de `efectos:`**. No es una fuente olvidada.
- Pero en `clases/rasgos/barbaro.yaml` **solo dos** de los diecinueve rasgos
  llevan bloque `efectos:` — «Defensa sin armadura» (línea 14) y «Movimiento
  rápido» (línea 53). **«Campeón primordial» (línea 102) no lo lleva.**

Así que el +4/+4 de nivel 20 está transcrito con su página y su texto, en el
sitio correcto, y aun así **no puede llegar a ningún cálculo**: ni por
`caracteristicas.final` (que solo suma trasfondo, mejoras y dotes) ni por el
manifiesto de efectos (que lo recorre pero no encuentra nada que recorrer).

Esto no cambia ninguno de mis números —los derivé de la regla, no del
manifiesto—, pero sí **explica** de dónde saldría la lectura B de §1.6, y
convierte la diferencia de 40 PG en un candidato a hallazgo real en vez de en
una discrepancia de criterio.

Nota de alcance, para no afirmar de más: no he leído `reglas/efectos.yaml`, así
que **no sé si el vocabulario del motor admite siquiera un `objetivo:` que sea
una puntuación de característica**. Si no lo admite, el hueco es más hondo que
una línea que falta: sería que la base no tiene forma de expresar «un rasgo de
clase sube una puntuación». Que alguien con permiso para abrir ese fichero lo
compruebe.
