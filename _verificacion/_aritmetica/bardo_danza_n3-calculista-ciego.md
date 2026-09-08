# Cálculo ciego a mano — `bardo_danza_n3`

**Agente:** E · «el calculista» (ronda 3 de estrés)
**Fecha:** 2026-09-06
**Ficha (datos crudos, sin bloque `calculado`):**
`/tmp/claude-0/-home-user-dnd/ccce6f54-5659-5d7c-89a3-15e0f610e8cf/scratchpad/crudos/bardo_danza_n3.yaml`

## Método

Segunda transcripción independiente: cada uno de los cinco valores se deriva
leyendo **solo** la base canónica (`reglas/`, `especies/`, `clases/`,
`clases/rasgos/`, `clases/subclases/`, `equipo/`, `dotes/`, `trasfondos/`) y la
ficha cruda, sin ver ningún número producido por el motor. Cada paso lleva
fichero y campo exactos.

### Ficheros consultados

| Fichero | Para qué |
|---|---|
| `.../scratchpad/crudos/bardo_danza_n3.yaml` | datos crudos de la ficha |
| `reglas/generacion_personaje.yaml` | modificadores, PB, PG, CD y bonif. de ataque de conjuros, regla de CA múltiple |
| `reglas/caracteristicas.yaml` | emparejamiento nombre ↔ abreviatura (`car` = Carisma, etc.) |
| `reglas/subida_de_nivel.yaml` | qué concede cada nivel (marcadores, PG por elección) |
| `reglas/fuentes_de_efectos.yaml` | **universo cerrado** de ficheros que pueden conceder efectos: usado para comprobar que no me dejo ninguna fuente de CA / PG / velocidad |
| `clases/bardo.yaml` | dado de golpe, aptitud mágica, PB por nivel, progresión, equipo inicial |
| `clases/rasgos/bardo.yaml` | rasgos de bardo de niveles 1–3 |
| `clases/subclases/bardo.yaml` | Colegio de la Danza, rasgo de nivel 3 |
| `equipo/armaduras.yaml` | catálogo de armaduras y escudos, y sus reglas |
| `equipo/aventureros.yaml` | contenido de los paquetes (para descartar armadura/escudo escondidos) |
| `especies/especies.yaml` | Aasimar: velocidad y rasgos |
| `trasfondos/trasfondos.yaml` | Acólito |
| `dotes/origen.yaml` | dote «Iniciado en la magia» que concede el trasfondo |
| `dotes/generales.yaml`, `dotes/don_epico.yaml`, `dotes/estilo_de_combate.yaml` | barridos de §1, §2.6 y §3.2: descartar dotes que tocan `pg_max`, `ca` o `velocidad` |
| `clases/rasgos/{barbaro,monje,explorador}.yaml`, `clases/subclases/{hechicero,paladin,druida,monje,explorador}.yaml` | mismos barridos: confirmar que sus efectos son de otras clases |

### Desviaciones cometidas

- **Ninguna.** No he abierto `calculo.py`, `efectos.py`, `reglas/efectos.yaml`,
  ningún verificador (`validar.py`, `verificar_*.py`, `censo.py`, `cobertura.py`,
  `generar_ficha.py`, `subir_nivel.py`, `buscar.py`) ni nada bajo `_verificacion/`.
- No he abierto `personajes/` ni la he listado: no he visto ninguna ficha ni
  ningún `_hallazgos/`.
- No he listado `_verificacion/_aritmetica/`: he escrito este fichero
  directamente (`mkdir -p` + redirección).
- Sí he leído `reglas/fuentes_de_efectos.yaml`. No está vetado (está en
  `reglas/` y no es `efectos.yaml`) y **no contiene ningún número del
  personaje**: es el manifiesto de qué ficheros pueden llevar efectos. Lo
  declaro porque es el fichero más «cercano al motor» que he tocado; lo he
  usado solo para cerrar la lista de fuentes que debía revisar, no para
  calcular nada.
- No he abierto `reglas/_ESQUEMA_efectos.md`. Dos de sus líneas aparecieron
  como resultado de `grep`: la 13 (el ejemplo de «Defensa sin armadura» del
  monje) y la 97 (una nota de que `velocidad` está en el modelo). Ninguna
  contiene un número de este personaje. Lo declaro por transparencia.

---

## Paso 0 — Insumos comunes

### 0.1 Modificadores de característica

Ficha cruda → `caracteristicas.final`:
`fue 10 · des 13 · con 14 · int 10 · sab 13 · car 15`.

Regla: `reglas/generacion_personaje.yaml` →
`metodos_generacion_caracteristicas.modificadores_por_puntuacion.formula`
= *«(puntuación − 10) / 2, redondeando hacia abajo»*, con su `tabla` al lado
(mismo campo, clave `tabla`; fuente `pagina_pdf: 40, libro: 38`).

| Car. | Puntuación | Cuenta | Tabla | Mod. |
|---|---|---|---|---|
| Destreza | 13 | (13−10)/2 = 1,5 → 1 | `"12-13": 1` | **+1** |
| Constitución | 14 | (14−10)/2 = 2 | `"14-15": 2` | **+2** |
| Carisma | 15 | (15−10)/2 = 2,5 → 2 | `"14-15": 2` | **+2** |

(Fórmula y tabla coinciden en los tres casos.)
El emparejamiento `des`→Destreza, `con`→Constitución, `car`→Carisma está en
`reglas/caracteristicas.yaml` → `caracteristicas[].abrev`.

### 0.2 Bonificador por competencia (PB)

Nivel total 3 (ficha → `nivel_total: 3`; una sola clase, `clases[0].nivel: 3`,
así que no hay nada que sumar).

Dos declaraciones concordantes:
- `reglas/generacion_personaje.yaml` → `px_por_nivel.filas` → `{nivel: 3, px: 900, pb: 2}`
- `clases/bardo.yaml` → `progresion` → `{n: 3, pb: 2, …}`

**PB = +2.**

### 0.3 Universo de fuentes que hay que revisar

`reglas/fuentes_de_efectos.yaml` declara que solo pueden conceder efectos:
`especies/especies.yaml`, `clases/rasgos/*.yaml`, `clases/subclases/*.yaml`,
`dotes/*.yaml`, `trasfondos/*.yaml` (bloque `fuentes`) y, como fuente
*derivada*, `equipo/armaduras.yaml` (bloque `derivadas`, campos `ca → ca` y
`fuerza → velocidad`). El resto de `equipo/` y de `reglas/` está en
`excluidos` con su motivo. Lo que este personaje tiene de cada una:

- **Especie Aasimar** — `especies/especies.yaml` → `especies[Aasimar]`: cinco
  rasgos. Ninguno toca CA ni PG. Uno toca velocidad, pero solo de forma
  situacional (§3.3).
- **Rasgos de bardo niveles 1–3** — `clases/rasgos/bardo.yaml`: Inspiración
  bárdica, Lanzamiento de conjuros (n.1), Aprendiz de mucho, Pericia (n.2).
  Ninguno modifica CA, PG ni velocidad.
- **Subclase** — `clases/subclases/bardo.yaml` → Colegio de la Danza, nivel 3:
  «Juego de pies deslumbrante». **Sí toca la CA** (§2).
- **Trasfondo Acólito** — `trasfondos/trasfondos.yaml` → `trasfondos[Acólito]`:
  no tiene texto de rasgo (`no_automatizado`); concede la dote
  «Iniciado en la magia (clérigo)» (campo `dote`).
- **Dotes** — la ficha cruda **no lleva bloque `dotes`** (ver §6.2). Aunque lo
  llevara: `dotes/origen.yaml` → `"Iniciado en la magia"` solo concede trucos y
  un conjuro de nivel 1; no toca CA, PG ni velocidad.
- **Equipo** — un solo objeto (§2.1).

---

## 1 — `pg_max`

**Dado de golpe.** `clases/bardo.yaml` → `atributos_basicos.dado_golpe: d8`.

> Aviso de lectura: la columna `dado` de `clases/bardo.yaml → progresion`
> vale `d6` en los niveles 1–4, pero **no es el dado de golpe**: es el «Dado
> bárdico» de Inspiración bárdica, como declara
> `clases/rasgos/bardo.yaml → rasgos["Inspiración bárdica"].desc`
> («El dado cambia con el nivel (columna "Dado bárdico" …): d8 en nivel 5…»).
> El dado de golpe es el de `atributos_basicos`, **d8**.

**Nivel 1.** `reglas/generacion_personaje.yaml` → `puntos_golpe.nivel_1.regla`
= *«Máximo del dado de golpe + modificador por Constitución.»*
(`pagina: {pdf: 42, libro: 40}`). La ficha registra
`pg_por_nivel[0] = {metodo: maximo_dado, valor: 8}`, coherente con máximo de d8 = 8.

    8 (máx. d8) + 2 (mod. Con) = 10

**Niveles 2 y 3.** `reglas/generacion_personaje.yaml` →
`puntos_golpe.niveles_siguientes_al_1.literal` (`pagina: {pdf: 44, libro: 42}`)
= *«… suma tu modificador por Constitución al resultado y añade el total
(mínimo de 1) a tus puntos de golpe máximos. En vez de tirar, puedes utilizar
el valor establecido …»*. La ficha eligió `metodo: valor_establecido, valor: 5`
en ambos niveles; ese 5 es exactamente el de
`puntos_golpe.niveles_siguientes_al_1.tabla_valores_establecidos.filas` →
`{clases: [Bardo, Brujo, Clérigo, Druida, Monje, Pícaro], valor: 5}`.

    nivel 2:  5 + 2 = 7   (≥ 1, el mínimo del total no muerde)
    nivel 3:  5 + 2 = 7

**Suma.**

    10 + 7 + 7 = 24

**Comprobación por el otro camino**, el que describe
`puntos_golpe.aumento_de_constitucion._nota_para_el_motor`
(«el término de Constitución es `nivel_total × mod_con`»):

    término del dado:  8 + 5 + 5 = 18
    término de Con:    3 × (+2)  =  6
    total                          24   ✔ coincide

**Sumandos descartados.** Barrido de *todos* los efectos sobre `pg_max` que
existen en la base (grep de `objetivo: pg_max` sobre `especies/`, `clases/`,
`dotes/`, `trasfondos/`, `equipo/` y `reglas/`, excluido el fichero vetado):
son cuatro, y **ninguno** aplica a este personaje.

| Efecto | Dónde | Por qué no aplica |
|---|---|---|
| «Aguante enano» (`op: add`, `nivel_total`) | `especies/especies.yaml → especies[Enano].rasgos` | es **Aasimar**, no enano |
| «Resistencia dracónica» (`op: add`, `nivel_clase`) | `clases/subclases/hechicero.yaml` | no tiene niveles de hechicero |
| Dote «Duro» (`op: add`, `2 * nivel_total`) | `dotes/origen.yaml → dotes[Duro]` | no la tiene (§6.2) |
| Dote «Don de la fortaleza» (`op: add`, `40`) | `dotes/don_epico.yaml` | prerrequisito «nivel 19 o más» |

Ningún rasgo de bardo, ningún rasgo del Colegio de la Danza y ningún campo del
trasfondo Acólito toca los PG.

> ### `pg_max` = **24**

---

## 2 — `ca`

Hay dos vías candidatas. Las evalúo por separado y luego decido.

### 2.1 Inventario de la ficha, objeto a objeto

Ficha cruda → `equipo`: **un solo elemento**.

| # | `ref` de la ficha | ¿Está en `equipo/armaduras.yaml`? | Categoría | `ca` | `fuerza` |
|---|---|---|---|---|---|
| 1 | `equipo/armaduras.yaml#Armadura de cuero tachonado` | **Sí** | `armaduras_ligeras.tabla` | `"12 + mod. Des"` | `null` |

No hay ningún segundo objeto. En particular:
- **No hay escudo.** `equipo/armaduras.yaml → escudos.tabla` tiene un único
  registro, `Escudo` (`ca: "+2"`), y no aparece en la ficha.
- **No hay ningún paquete.** La ficha no referencia nada de
  `equipo/aventureros.yaml`. Lo he comprobado igualmente contra
  `equipo/aventureros.yaml → descripciones` (los 7 paquetes que lista
  `tabla_peso_precio`:
  artista, diplomático, erudito, explorador, explorador de mazmorras, ladrón,
  sacerdote): **ninguno contiene armadura ni escudo**; el de artista, que sería
  el del bardo según su equipo inicial, trae «campana, cantimplora, 3
  disfraces, espejo, 8 frascos de aceite, linterna de ojo de buey, mochila,
  petate, raciones para 9 días y yesquero». Coherente con que
  `reglas/fuentes_de_efectos.yaml → excluidos` clasifique
  `equipo/aventureros.yaml` como «no concede nada calculable».
- El único roce con la palabra «escudo» en `aventureros.yaml` es la
  descripción de `Símbolo sagrado` («emblema en tela o escudo»); no es un
  escudo del catálogo, y además la ficha tampoco lo lleva.

**Lectura que asumo, y que declaro:** la ficha no marca «equipada / puesta» en
los objetos de `equipo`; solo los lista. Leo que estar en `equipo` significa
*llevarla puesta* — es la única lectura con la que el campo significa algo, y
la entrada trae `origen: {clase: Bardo, nota: generado}`, es decir, es la
armadura que el personaje viste por su equipo inicial de clase. **Si en cambio
se leyera que la armadura está guardada y no puesta**, se cumpliría la
condición del rasgo y la CA saldría por la vía B — que, como se ve abajo, da
**el mismo 13**. La ambigüedad no cambia el número.

### 2.2 Vía A — la armadura

`equipo/armaduras.yaml` → `armaduras_ligeras.tabla` →
`{nombre: "Armadura de cuero tachonado", ca: "12 + mod. Des", fuerza: null,
sigilo: null}` (fuente del fichero: `pagina_pdf: 218, libro: 216`).

    CA = 12 + 1 (mod. Des) = 13

Sin tope de Destreza: el tope `(máx. 2)` solo aparece en las armaduras medias
de ese mismo fichero, no en las ligeras.

Entrenamiento: `equipo/armaduras.yaml → reglas.entrenamiento` exige
entrenamiento para usarla de forma efectiva; la ficha lo tiene
(`competencias.armaduras: [{categoria: "Armaduras ligeras", origen: {clase: Bardo}}]`,
que es lo que declara `clases/bardo.yaml → atributos_basicos.armaduras: ["Armaduras ligeras"]`).
Así que no se dispara `reglas.sin_entrenamiento`. En cualquier caso, esa
penalización es desventaja en pruebas y no poder lanzar conjuros: **no** habría
cambiado la CA.

### 2.3 Vía B — el rasgo de subclase

`clases/subclases/bardo.yaml` → `subclases[Colegio de la Danza]` →
`rasgos[nivel: 3, nombre: "Juego de pies deslumbrante"]`
(`pagina: {pdf: 66, libro: 64}`). Texto entero del `desc`, con la condición
subrayada:

> «**Mientras no lleves armadura ni escudo:** Virtuoso de la danza …;
> **Defensa sin armadura (CA base = 10 + mod. Destreza + mod. Carisma)**;
> Ataques ágiles …; Daño bárdico …»

El bloque `efectos` del mismo registro dice lo mismo en estructurado:
`{objetivo: ca, op: base, formula: "10 + mod_des + mod_car",
requiere: [sin_armadura, sin_escudo]}`.

Dos cosas que importan:

1. **`op: base` — FIJA la CA base, no suma.** No es «+2 a la CA»: sustituye el
   10 de partida por `10 + mod. Des + mod. Car`. Si se cumpliera, la CA sería
   `10 + 1 + 2 = 13`.
2. **La condición no se cumple.** `requiere: [sin_armadura, sin_escudo]`.
   Del §2.1: el personaje **sí lleva armadura** (Armadura de cuero tachonado,
   registro de `equipo/armaduras.yaml → armaduras_ligeras.tabla`). El requisito
   `sin_escudo` sí se cumple (no hay escudo), pero hacen falta los dos.

**→ La vía B queda descartada: el rasgo no aplica.**

### 2.4 Cuál se usa

Como solo queda **una** vía activa, la regla de conflicto ni siquiera llega a
morder. La cito igual porque es la que la base tiene escrita al respecto:

`reglas/generacion_personaje.yaml` → `multiclase.clase_de_armadura.regla`
(`fuente: {pagina_pdf: [46, 47], libro: [44, 45]}`):

> «Si el personaje tiene varias formas de calcular su CA (p. ej. Defensa sin
> armadura de monje y Resistencia dracónica de hechicero), solo puede
> beneficiarse de una, **a elegir**.»

Es decir: la base dice **«a elegir»**, *no* «la mayor». No he elegido por
tamaño en ningún momento; he descartado la vía B por incumplimiento de su
condición, no por ser menor o mayor.

(Salvedad honesta sobre esta cita: la regla vive bajo la clave `multiclase`,
y este personaje **no** es multiclase. Es la única declaración de la base sobre
concurrencia de vías de CA, y su enunciado es general —«Si el personaje tiene
varias formas de calcular su CA»—, así que la aplico como tal. Si alguien
sostiene que solo vale en multiclase, la base **no declararía** nada para el
caso monoclase; el resultado de esta ficha no cambia, porque aquí no hay
concurrencia.)

### 2.5 Coincidencia numérica — dicho en voz alta para que no engañe

Las dos vías dan **13**:

    vía A (armadura):  12 + 1           = 13
    vía B (rasgo):     10 + 1 + 2       = 13

Esto es una trampa perfecta para una verificación circular: un motor que
aplicase mal el rasgo —ignorando la condición «mientras no lleves armadura»—
sacaría **el mismo 13** y saldría en verde. El número correcto es 13 **por la
armadura**, no por el rasgo. Si alguna vez esta ficha cambia de armadura (o se
la quita), las dos vías dejan de coincidir y el error se haría visible.

### 2.6 Barrido de todos los demás efectos sobre `ca`

Grep de `objetivo: ca` sobre `especies/`, `clases/`, `dotes/`, `trasfondos/`,
`equipo/` y `reglas/` (excluido el fichero vetado). Además del rasgo del §2.3 y
de la fuente derivada `equipo/armaduras.yaml` del §2.2, la base tiene estos, y
**ninguno** aplica:

| Efecto | Dónde | Por qué no aplica |
|---|---|---|
| «Defensa sin armadura» de bárbaro (`op: base`, `10 + mod_des + mod_con`) | `clases/rasgos/barbaro.yaml` | no es bárbaro |
| «Defensa sin armadura» de monje (`op: base`, `10 + mod_des + mod_sab`) | `clases/rasgos/monje.yaml` | no es monje |
| «Resistencia dracónica» (`op: base`, `10 + mod_des + mod_car`, `requiere: [sin_armadura]`) | `clases/subclases/hechicero.yaml` | no es hechicero |
| «Inspiración en combate» (`op: conditional`) | `clases/subclases/bardo.yaml` → **Colegio del Valor** | su subclase es Colegio de la **Danza** |
| Rasgos `op: conditional` de druida y paladín | `clases/subclases/druida.yaml`, `…/paladin.yaml` | ni druida ni paladín; y son situacionales |
| Estilo de combate «Defensa» (`op: add`, `1`, `requiere: [con_armadura]`) | `dotes/estilo_de_combate.yaml` | **el bardo no obtiene Estilo de combate**: no aparece en `clases/bardo.yaml → progresion[].rasgos` en ningún nivel. Ojo: si lo tuviera, la CA sería 14 |
| «Duelista defensivo» (`op: conditional`) | `dotes/generales.yaml` | no tiene esa dote; y es una reacción situacional |
| «Maestro en armaduras medias» (`op: modifica_tope`) | `dotes/generales.yaml` | no tiene esa dote; y su armadura es ligera, sin tope |

**Sin escudo que sumar**: `equipo/armaduras.yaml → escudos.tabla` → `{nombre:
Escudo, ca: "+2"}` no está en el equipo de la ficha.

> ### `ca` = **13** (por la Armadura de cuero tachonado; el rasgo de subclase NO aplica)

---

## 3 — `velocidad`

### 3.1 Base de especie

`especies/especies.yaml` → `especies[Aasimar]` → `velocidad_m: 9`
(`pagina: {pdf: 188, libro: 186}`).

    velocidad = 9 m

### 3.2 Modificadores permanentes: ninguno

- **Armadura.** `equipo/armaduras.yaml → reglas.fuerza`: *«Si la tabla indica
  una puntuación de Fuerza para un tipo de armadura, esta reduce 3 m la
  velocidad de quien la lleve, salvo que su Fuerza sea igual o superior a la
  indicada.»* La Armadura de cuero tachonado tiene **`fuerza: null`** — la
  tabla no indica ninguna puntuación —, así que **no reduce**. (Las que sí la
  indican son las tres pesadas: `Cota de malla` 13, `Armadura de bandas` 15,
  `Armadura de placas` 15.) Esto es exactamente el efecto derivado
  `{campo: fuerza, objetivo: velocidad, op: add}` que declara
  `reglas/fuentes_de_efectos.yaml → derivadas`, y aquí sale vacío.
- **Rasgos de bardo 1–3** (`clases/rasgos/bardo.yaml`): ninguno toca la velocidad.
- **Colegio de la Danza nivel 3** (`clases/subclases/bardo.yaml`): «Juego de
  pies deslumbrante» no toca la velocidad. «Movimiento inspirador» sí habla de
  moverse, pero es de **nivel 6** — este personaje es de nivel 3 — y además es
  una reacción situacional.
- **Trasfondo / dote:** nada.

**Barrido completo** (grep de `objetivo: velocidad` sobre `especies/`,
`clases/`, `dotes/`, `trasfondos/`, `equipo/`, `reglas/`, excluido el fichero
vetado). Los efectos **permanentes** (`op: add`) de la base son seis, y
ninguno es de este personaje: «Movimiento rápido» de bárbaro n.5
(`clases/rasgos/barbaro.yaml`), «Errante» de explorador n.6
(`clases/rasgos/explorador.yaml`), «Movimiento sin armadura» de monje n.2
(`clases/rasgos/monje.yaml`), «Aura de celeridad» de paladín n.7
(`clases/subclases/paladin.yaml`) y las dotes «Veloz» (`dotes/generales.yaml`)
y «Don de la velocidad» (`dotes/don_epico.yaml`). Los demás son
`op: conditional`, es decir, situacionales por declaración de la propia base.
Es un bardo de nivel 3 sin dotes registradas: no tiene ninguno.

### 3.3 Descartado por SITUACIONAL (lo digo explícitamente)

`especies/especies.yaml → especies[Aasimar].rasgos["Revelación celestial"]`
(`nivel: 3`, que este personaje **sí** tiene) ofrece, entre sus tres opciones,
**Alas celestiales: «velocidad volando igual a tu velocidad»**.

**NO entra en el número de la ficha**, por dos motivos independientes:
1. Es **situacional**: «Acción adicional para transformarte **1 minuto, 1 vez
   por descanso largo**».
2. Aunque estuviera activa, es una **velocidad volando**, un modo de
   desplazamiento distinto; no altera la velocidad de caminar, que es lo que
   registra el campo `velocidad`.

(Mismo criterio que la base ya aplica a un caso gemelo: el rasgo «Forma grande»
del Goliat lleva `{objetivo: velocidad, op: conditional, texto: "+3 m mientras
dure Forma grande …, **no de forma permanente**"}` en
`especies/especies.yaml`.)

> **Observación al margen (asimetría de la base, no afecta a mi número).**
> «Forma grande» del Goliat sí lleva su bloque `efectos:` con
> `op: conditional`, y «Revelación celestial» del Aasimar **no lleva ninguno**:
> su mención de velocidad vive solo en la prosa del `desc`. Las dos son
> situacionales y las dos se descartan igual, pero solo una está marcada como
> tal en estructurado. Quien audite la cobertura de rasgos con efectos quizá
> quiera mirarlo.

> ### `velocidad` = **9 m**

---

## 4 — `cd_conjuros`

**Fórmula.** `reglas/generacion_personaje.yaml` → `conjuros.cd_salvacion.formula`
(`conjuros.pagina: {pdf: 240, libro: 238}`, `seccion: "Tiradas de salvación /
Tiradas de ataque"`):

> `"8 + modificador de aptitud mágica + bonificador por competencia"`  (`base: 8`)

**Aptitud mágica.** `conjuros._nota_aptitud` remite a
`clases/<clase>.yaml → aptitud_magica`; `clases/bardo.yaml` → `aptitud_magica: Carisma`
(y `atributos_basicos.caracteristica_principal: Carisma`, y
`clases/rasgos/bardo.yaml → rasgos["Lanzamiento de conjuros"].desc`:
«Aptitud mágica: Carisma»). Las tres declaraciones coinciden.

    CD = 8 + 2 (mod. Car) + 2 (PB) = 12

Nada de lo que tiene este personaje modifica la CD: ni los rasgos de bardo
1–3, ni «Juego de pies deslumbrante», ni el trasfondo. El rasgo aasimar
«Portador de luz» usa Carisma como aptitud mágica para el truco *luz*, misma
característica, así que no introduce una segunda CD distinta.

> ### `cd_conjuros` = **12**

---

## 5 — `bonif_ataque_conjuros`

**Fórmula.** `reglas/generacion_personaje.yaml` → `conjuros.bonificador_ataque.formula`
(misma `conjuros.pagina: {pdf: 240, libro: 238}`):

> `"modificador de aptitud mágica + bonificador por competencia"`  (`base: 0`)

Misma aptitud mágica que en §4 (Carisma, `clases/bardo.yaml → aptitud_magica`).

    bonif. ataque = 2 (mod. Car) + 2 (PB) = +4

Relación de sanidad con §4: `CD − bonif. ataque = 12 − 4 = 8`, que es el
`base: 8` de la fórmula de la CD. Consistente.

> ### `bonif_ataque_conjuros` = **+4**

---

## 6 — Lo que NO he podido derivar, y observaciones al margen

### 6.1 Todo lo pedido se pudo derivar

Los cinco valores salen de la base sin huecos. En particular, los dos avisos
del encargo se confirman:
- La fórmula de la CD **sí está** en la base
  (`reglas/generacion_personaje.yaml → conjuros.cd_salvacion`, con página).
  No es un hueco.
- La CA por defecto sin armadura (`10 + mod. Des`) **no me ha hecho falta**:
  este personaje lleva armadura, así que la CA sale de la tabla de armaduras.
  No he abierto el fichero que la declara (vetado).

### 6.2 Dos discrepancias en los DATOS CRUDOS (no en mis cuentas)

Las anoto porque las he visto derivando, no porque cambien mis números.

**(a) La armadura no es la del equipo inicial del bardo.** La entrada de
equipo trae `origen: {clase: Bardo, nota: generado}`, pero
`clases/bardo.yaml → atributos_basicos.equipo_inicial.a` dice
*«**armadura de cuero**, 2 dagas, instrumento musical a elección, paquete de
artista y 19 po»*. En `equipo/armaduras.yaml → armaduras_ligeras.tabla` esos
son **dos registros distintos**:

| Registro | `ca` | precio |
|---|---|---|
| `Armadura de cuero` | `"11 + mod. Des"` | 10 po |
| `Armadura de cuero tachonado` (la de la ficha) | `"12 + mod. Des"` | 45 po |

Si la armadura correcta fuese la de cuero a secas, la CA sería
`11 + 1 = **12**`, no 13. **Mi 13 se deriva de lo que la ficha cruda dice que
lleva puesto**, que es lo que se me pidió calcular; pero si alguien concluye
que el generador escogió mal la armadura, el valor que habría que corregir es
el dato crudo, y la CA pasaría a 12. Lo dejo dicho sin ajustar nada.

**(b) Falta la dote del trasfondo.** `trasfondos/trasfondos.yaml →
trasfondos[Acólito].dote` = «Iniciado en la magia (clérigo)», y la ficha cruda
**no tiene bloque `dotes`**. No afecta a ninguno de los cinco valores
(`dotes/origen.yaml → "Iniciado en la magia"` solo da dos trucos y un conjuro de
nivel 1, con su propia aptitud mágica a elegir), pero la ficha está incompleta
respecto de su trasfondo.

---

## Valores derivados

| Valor | Resultado | Derivación en una línea | Cita principal |
|---|---:|---|---|
| `pg_max` | **24** | (8 máx. d8 + 2) + (5 + 2) + (5 + 2) = 10 + 7 + 7 | `reglas/generacion_personaje.yaml → puntos_golpe.nivel_1` y `→ puntos_golpe.niveles_siguientes_al_1.tabla_valores_establecidos`; `clases/bardo.yaml → atributos_basicos.dado_golpe` |
| `ca` | **13** | 12 + 1 (mod. Des), por la armadura. El rasgo de subclase **no** aplica: lleva armadura | `equipo/armaduras.yaml → armaduras_ligeras.tabla["Armadura de cuero tachonado"]`; `clases/subclases/bardo.yaml → [Colegio de la Danza].rasgos[n.3]` |
| `velocidad` | **9 m** | velocidad de especie; la armadura no tiene requisito de Fuerza, así que no resta 3 m | `especies/especies.yaml → especies[Aasimar].velocidad_m`; `equipo/armaduras.yaml → reglas.fuerza` |
| `cd_conjuros` | **12** | 8 + 2 (mod. Car) + 2 (PB) | `reglas/generacion_personaje.yaml → conjuros.cd_salvacion.formula`; `clases/bardo.yaml → aptitud_magica` |
| `bonif_ataque_conjuros` | **+4** | 2 (mod. Car) + 2 (PB) | `reglas/generacion_personaje.yaml → conjuros.bonificador_ataque.formula` |

**Insumos:** mod. Des +1 · mod. Con +2 · mod. Car +2 · PB +2 · dado de golpe d8 ·
aptitud mágica Carisma.

**Descartado por situacional (no entra en la ficha):** Alas celestiales de
«Revelación celestial» del Aasimar (1 min, 1/descanso largo, y es velocidad
*volando*).
**Descartado por incumplimiento de condición:** «Defensa sin armadura» de
«Juego de pies deslumbrante» (requiere no llevar armadura ni escudo; lleva
Armadura de cuero tachonado). Da el mismo 13 por casualidad aritmética.

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
pg_max: 24
ca: 13
velocidad: 9
cd_conjuros: 12
bonif_ataque_conjuros: 4
```
