# Derivación a mano — `enano_clerigo_n5` (Doran Piedrafría)

**Agente E · «el calculista» — ronda 3 de estrés**
Fecha: 2026-09-06

---

## Cabecera

### Ficha

| | |
|---|---|
| Nombre | Doran Piedrafría |
| Especie | Enano (`especies/especies.yaml#Enano`) |
| Clase | Clérigo 5, Dominio de la Guerra |
| Trasfondo | Acólito |
| Nivel total | 5 |
| Puntuaciones finales | Fue 12 · Des 10 · Con 14 · Int 8 · Sab 18 · Car 15 |

### Método

Transcripción independiente. Todos los números de abajo salen de leer la base
canónica y hacer la aritmética a mano, paso a paso, **sin ejecutar ni leer
ninguna pieza del motor**. No es un segundo calculador: es una segunda lectura
de las mismas reglas por una vía distinta.

Datos de partida: la copia **cruda** de la ficha, sin bloque `calculado`, en
`/tmp/claude-0/-home-user-dnd/ccce6f54-5659-5d7c-89a3-15e0f610e8cf/scratchpad/crudos/enano_clerigo_n5.yaml`.

### Ficheros consultados (todos de la base)

- `reglas/generacion_personaje.yaml` — PG (nivel 1, niveles siguientes, aumento
  de Constitución), tabla de modificadores, tabla `px_por_nivel` (bonificador
  por competencia), fórmulas de CD y de ataque de conjuros
- `reglas/caracteristicas.yaml` — emparejamiento nombre ↔ abreviatura
- `reglas/fuentes_de_efectos.yaml` — para saber **dónde** puede haber efectos
  que toquen `pg_max`, `ca` o `velocidad`, y así poder afirmar que no me dejo
  ninguno
- `reglas/_ESQUEMA_efectos.md` — solo para confirmar qué es una `formula`
- `especies/especies.yaml` — registro Enano: velocidad y «Aguante enano»
- `clases/clerigo.yaml` — dado de golpe, aptitud mágica, tabla de progresión
- `clases/rasgos/clerigo.yaml` — rasgos de clérigo de niveles 1–5
- `clases/subclases/clerigo.yaml` — Dominio de la Guerra
- `equipo/armaduras.yaml` — Camisa de malla, Escudo y las reglas de la tabla
- `dotes/origen.yaml` — «Iniciado en la magia»
- `dotes/generales.yaml` — «Mejora de característica»
- `trasfondos/trasfondos.yaml` — Acólito

### Desviaciones cometidas

**Ninguna.** No he abierto `personajes/enano_clerigo_n5.yaml` ni ninguna otra
ficha, ni `personajes/_hallazgos/`, ni ningún informe previo de
`_verificacion/_aritmetica/` (a este directorio solo le he hecho `mkdir -p`
para poder escribir aquí, sin listar su contenido). No he leído `calculo.py`,
`efectos.py`, `reglas/efectos.yaml` ni ningún verificador, y no he ejecutado
ninguno. Los únicos comandos ejecutados han sido `cat`, `grep`, `sed` y `ls`
sobre ficheros de la base.

**Números nuestros vistos por accidente: ninguno.** No he visto en ningún
momento el bloque `calculado` de esta ficha ni de otra.

### Nota sobre el hallazgo ya conocido de la CA por defecto

No lo repito. Esta derivación además no lo necesita: el personaje lleva
armadura, así que su CA sale de la tabla de `equipo/armaduras.yaml`, no de la
CA por defecto de quien no lleva nada.

---

## 0. Preliminares: modificadores y bonificador por competencia

Estos tres números entran en casi todo lo demás, así que los derivo primero.

### 0.1 Modificadores por característica

> `reglas/generacion_personaje.yaml → metodos_generacion_caracteristicas.modificadores_por_puntuacion.formula`
> «(puntuación − 10) / 2, redondeando hacia abajo»
> (pág. pdf 40 / libro 38, según `metodos_generacion_caracteristicas.fuente`)

La misma entrada trae la `tabla` explícita, que uso como contraste:

| Característica | Puntuación final (ficha `caracteristicas.final`) | (p−10)/2 ↓ | Tabla | Mod. |
|---|---|---|---|---|
| Destreza | 10 | (10−10)/2 = 0 | `"10-11": 0` | **+0** |
| Constitución | 14 | (14−10)/2 = 2 | `"14-15": 2` | **+2** |
| Sabiduría | 18 | (18−10)/2 = 4 | `"18-19": 4` | **+4** |

Fórmula y tabla coinciden en los tres casos.

Comprobación aparte de que la puntuación final de Sabiduría es de verdad 18
(no la doy por buena solo porque la ficha la escriba):

- base 15 — conjunto estándar, `reglas/generacion_personaje.yaml →
  metodos_generacion_caracteristicas.conjunto_estandar.puntuaciones: [15, 14, 13, 12, 10, 8]`
- +2 por trasfondo — `trasfondos/trasfondos.yaml → Acólito.caracteristicas:
  [Inteligencia, Sabiduría, Carisma]`, y la regla de reparto está en
  `reglas/generacion_personaje.yaml →
  metodos_generacion_caracteristicas.ajuste_por_trasfondo` («aumenta una de
  las tres características del trasfondo en 2 y otra distinta en 1»)
- +1 por la mejora de nivel 4 — `dotes/generales.yaml → Mejora de característica`
  (pág. pdf 209 / libro 207), `mejora_caracteristica: {cantidad: 2, maximo: 20,
  entre: cualquiera}`; la ficha reparte +1 Sab / +1 Car, que es la variante
  «aumenta dos en 1 cada una» de la `descripcion`

15 + 2 + 1 = **18**, y 18 ≤ 20 (tope de `maximo: 20`). Correcto.

Constitución: base 14, sin ajuste de trasfondo (el Acólito no ofrece
Constitución) y sin tocar en la mejora de nivel 4 → **14 durante los cinco
niveles**. Esto importa mucho para los PG y lo retomo en el §1.4.

### 0.2 Bonificador por competencia (PB)

> `reglas/generacion_personaje.yaml → px_por_nivel.filas[nivel=5].pb = 3`
> (tabla «Progreso de los personajes», pág. pdf 43 / libro 41)

Contrastado con la tabla de la clase:

> `clases/clerigo.yaml → progresion[n=5].pb = 3`

Las dos fuentes dicen 3.

**PB = +3**

---

## 1. `pg_max` — puntos de golpe máximos

### 1.1 La regla, en dos piezas

La base separa —correctamente— el nivel 1 del resto:

> `reglas/generacion_personaje.yaml → puntos_golpe.nivel_1.regla`
> «Máximo del dado de golpe + modificador por Constitución.»
> (pág. pdf 42 / libro 40)

> `reglas/generacion_personaje.yaml → puntos_golpe.niveles_siguientes_al_1.literal`
> «Cada vez que subas un nivel, obtendrás un dado de golpe adicional. Tira ese
> dado, suma tu modificador por Constitución al resultado y añade el total
> (mínimo de 1) a tus puntos de golpe máximos. En vez de tirar, puedes utilizar
> el valor establecido que se muestra en la tabla "Puntos de golpe establecidos
> por clase".»
> (pág. pdf 44 / libro 42, sección «Subir de nivel, paso 2»)

Dado de golpe:

> `clases/clerigo.yaml → atributos_basicos.dado_golpe: d8` (pág. pdf 83 / libro 81)

Máximo del d8 = **8**.

Valor establecido de la clase:

> `reglas/generacion_personaje.yaml →
> puntos_golpe.niveles_siguientes_al_1.tabla_valores_establecidos.filas`
> `{clases: [Bardo, Brujo, Clérigo, Druida, Monje, Pícaro], valor: 5}`

Valor establecido de Clérigo = **5**.

### 1.2 Los cinco niveles, uno a uno

La ficha declara el método de cada nivel en `pg_por_nivel`. Verifico que cada
`valor` declarado es legítimo según la regla que la propia entrada cita, y
luego sumo. Leo `valor` como el resultado **del dado o de la tabla, sin el
modificador por Constitución** — porque el nivel 1 trae `valor: 8`, que es
exactamente el máximo del d8, y los niveles 2–4 traen `valor: 5`, que es
exactamente el valor establecido de Clérigo; si `valor` ya incluyera el +2 de
Constitución, ninguno de los dos cuadraría con su tabla.

| Nivel | Método declarado | `valor` | ¿Legítimo? | + mod. Con | Total del nivel |
|---|---|---|---|---|---|
| 1 | `maximo_dado` | 8 | Sí: máx. del d8 = 8 | +2 | 10 |
| 2 | `valor_establecido` | 5 | Sí: Clérigo = 5 en la tabla | +2 | 7 |
| 3 | `valor_establecido` | 5 | Sí: ídem | +2 | 7 |
| 4 | `valor_establecido` | 5 | Sí: ídem | +2 | 7 |
| 5 | `tirada` | 6 | Sí: 6 está en el rango 1–8 de un d8 | +2 | 8 |

Mínimo de 1: la regla dice que el mínimo es **del total** (dado + mod. Con), y
el propio fichero lo subraya con el comentario `# el MÍNIMO es del TOTAL (dado
+ mod), no del dado` en `puntos_golpe.niveles_siguientes_al_1.metodos[tirar].minimo`.
Aquí los totales de los niveles 2–5 son 7, 7, 7 y 8: ninguno queda por debajo
de 1, así que el mínimo no llega a morder.

Suma de los cinco niveles: 10 + 7 + 7 + 7 + 8 = **39**

### 1.3 El rasgo de especie: «Aguante enano»

> `especies/especies.yaml → especies[Enano].rasgos["Aguante enano"]`
> desc: «Tus PG máximos aumentan en 1, y en 1 más cada vez que subes de nivel.»
> efectos: `{objetivo: pg_max, op: add, formula: "nivel_total"}`
> (pág. pdf 192 / libro 190)

Dos lecturas posibles de la prosa:

- **(a)** +1 al obtener la especie (nivel 1) y +1 por cada subida posterior
  (niveles 2, 3, 4 y 5) → 1 + 4 = **5**.
- **(b)** +1 fijo *además* de +1 por cada nivel alcanzado, incluido el 1 → 6.

**Elijo la (a)**, y no por gusto: el propio registro declara la forma cerrada
`formula: "nivel_total"` junto a la prosa, y `nivel_total` = 5. La lectura (b)
daría 6 y contradiría la fórmula que la base escribe al lado. Además la (a) es
la lectura natural de «aumentan en 1, y en 1 más cada vez que subes de nivel»:
el primer +1 es el del nivel 1, no un sumando aparte.

`nivel_total` = 5 (`nivel_total: 5` en la ficha, y coherente con `clases[0].nivel: 5`
en una única clase).

Aporte de Aguante enano: **+5**

### 1.4 El término de Constitución, comprobado a la contra

La base avisa de que los PG máximos **no** son «la suma de lo que se ganó en
cada nivel» en cuanto la Constitución cambie:

> `reglas/generacion_personaje.yaml → puntos_golpe.aumento_de_constitucion.literal`
> «Cuando tu modificador por Constitución aumente en 1, tus puntos de golpe
> máximos también aumentarán en 1 por cada nivel que hayas alcanzado.»
> (pág. pdf 44 / libro 42, `_es_retroactivo: true`)

Aquí la Constitución **no cambia nunca**: 14 en la creación, sin ajuste de
trasfondo y sin tocar en la mejora de nivel 4 (que fue +1 Sab / +1 Car). Por
tanto mod. Con = +2 en los cinco niveles y el término retroactivo no se activa.

Rehago la cuenta con la forma cerrada, que es la que sobreviviría a un cambio
de Constitución, para ver si coincide con la suma nivel a nivel:

- Término de dados (historia acumulada): 8 + 5 + 5 + 5 + 6 = 29
- Término de Constitución: `nivel_total × mod_con` = 5 × 2 = 10
- Término de especie: 5

29 + 10 + 5 = **44**, y por la vía nivel a nivel 39 + 5 = **44**. Las dos vías
coinciden, como debe ser mientras la Constitución no se mueva.

### 1.5 ¿Falta algún otro efecto sobre `pg_max`?

Para poder afirmarlo, uso el manifiesto de fuentes de la propia base:

> `reglas/fuentes_de_efectos.yaml → fuentes` declara que los efectos solo
> pueden venir de `especies/especies.yaml` (rasgos), `clases/rasgos/*.yaml`,
> `clases/subclases/*.yaml`, `dotes/*.yaml` y `trasfondos/*.yaml`; y
> `→ derivadas` añade `equipo/armaduras.yaml` (que solo deriva `ca` y `velocidad`).

Repaso las que le tocan a este personaje:

- **Enano**: solo «Aguante enano» lleva `efectos:`; los otros tres rasgos
  (Afinidad con la piedra, Resistencia enana, Visión en la oscuridad) no tocan
  ninguna variable numérica.
- **Clérigo, rasgos de niveles 1–5** (`clases/rasgos/clerigo.yaml`):
  Lanzamiento de conjuros, Orden divina, Canalizar divinidad, Abrasar muertos
  vivientes. Ninguno lleva `efectos:` ni menciona PG máximos.
- **Dominio de la Guerra** (`clases/subclases/clerigo.yaml`): Conjuros del
  dominio, Golpe guiado, Sacerdote guerrero. Ninguno lleva `efectos:`.
- **Acólito** (`trasfondos/trasfondos.yaml`): sin `efectos:`; el registro
  incluso lo dice — `no_automatizado: "el trasfondo no tiene texto de rasgo…"`.
- **Iniciado en la magia** (`dotes/origen.yaml`): sin `efectos:`. La única dote
  de origen que toca `pg_max` es **Duro** (`2 * nivel_total`), y este personaje
  **no la tiene** (su única dote es Iniciado en la magia, y su única mejora de
  nivel 4 es Mejora de característica, que solo sube puntuaciones).

No queda ningún efecto sin contar.

### 1.6 Resultado

**pg_max = 44**

---

## 2. `ca` — clase de armadura

### 2.1 Qué lleva puesto

La ficha lista en `equipo`:

- `equipo/armaduras.yaml#Camisa de malla`
- `equipo/armaduras.yaml#Escudo`

> `equipo/armaduras.yaml → armaduras_medias.tabla`
> `{nombre: "Camisa de malla", ca: "13 + mod. Des (máx. 2)", fuerza: null, sigilo: null, peso_kg: 10, precio: "50 po"}`
> (págs. pdf 218-219 / libro 216, según `fuente`)

> `equipo/armaduras.yaml → escudos.tabla`
> `{nombre: Escudo, ca: "+2", fuerza: null, sigilo: null, peso_kg: 3, precio: "10 po"}`

### 2.2 ¿Tiene entrenamiento?

> `equipo/armaduras.yaml → reglas.entrenamiento`
> «Cualquiera puede ponerse una armadura o embrazar un escudo, pero solo quien
> tenga entrenamiento con ese tipo la usa de forma efectiva.»

> `equipo/armaduras.yaml → reglas.escudos`
> «Solo obtienes el bonificador a la CA de un escudo si tienes entrenamiento
> con escudos.»

La ficha declara en `competencias.armaduras`: Armaduras ligeras, Armaduras
medias y Escudos, todas con `origen: {clase: Clérigo}`. Contrastado con la
fuente:

> `clases/clerigo.yaml → atributos_basicos.armaduras: ["Armaduras ligeras", "Armaduras medias", Escudos]`

La Camisa de malla está en `armaduras_medias` → entrenado. El escudo →
entrenado. Así que **sí** se aplica el +2 del escudo y **no** aplica la
penalización de `reglas.sin_entrenamiento`.

También compruebo `reglas.solo_un_tipo` («no puede llevar puesta más de una
armadura ni embrazar más de un escudo a la vez»): una armadura y un escudo, sin
conflicto.

### 2.3 La cuenta

- Base de la Camisa de malla: **13**
- Modificador por Destreza, con el tope de la armadura media: mod. Des = **+0**;
  el tope es `(máx. 2)`, así que se aplica `min(0, 2) = 0` → **+0**
- Escudo: **+2**

13 + 0 + 2 = **15**

### 2.4 ¿Hay alguna otra fórmula de CA compitiendo?

`reglas/_ESQUEMA_efectos.md` (sección «Lo que este esquema todavía NO
representa») recuerda que cuando hay más de una CA base aplicable la ficha debe
elegir. Aquí no hay concurrencia: el clérigo no tiene ninguna «defensa sin
armadura», el Dominio de la Guerra no da ninguna fórmula de CA, y ninguna de
sus dotes toca `ca` (las que sí lo hacen en la base son Defensa de
`dotes/estilo_de_combate.yaml` y dos de `dotes/generales.yaml`, y no las
tiene). La única CA aplicable es la de la armadura que lleva.

### 2.5 Supuesto que hago explícito

La ficha cruda lista el equipo como **posesiones**; no hay ningún campo que
diga «puesto» o «equipado» —ni en la ficha ni en el vocabulario de la base—.
Doy por hecho que la camisa de malla va puesta y el escudo embrazado, que es lo
que hace que la CA sea 15. Si se leyera como «lo lleva en la mochila», la CA
sería la de sin armadura (10 + mod. Des = 10) y el escudo no contaría. Lo digo
porque el supuesto es mío, no de la base; ver el hallazgo H-3 más abajo.

### 2.6 Resultado

**ca = 15**

---

## 3. `velocidad` — en metros

> `especies/especies.yaml → especies[Enano].velocidad_m: 9`
> (registro Enano, pág. pdf 192 / libro 190)

Modificadores posibles, uno por uno:

- **Penalización por Fuerza de la armadura.**
  > `equipo/armaduras.yaml → reglas.fuerza`
  > «Si la tabla indica una puntuación de Fuerza para un tipo de armadura, esta
  > reduce 3 m la velocidad de quien la lleve, salvo que su Fuerza sea igual o
  > superior a la indicada.»

  La Camisa de malla trae `fuerza: null` — la tabla **no** indica puntuación de
  Fuerza para ella, así que la regla no se dispara. (Aunque se disparase, la
  Fuerza del personaje es 12; pero el caso no llega a plantearse.) En toda la
  tabla solo tienen `fuerza` no nula tres armaduras pesadas, y no lleva ninguna.

- **Rasgos.** Ninguno de los rasgos del Enano toca la velocidad; ninguno de los
  rasgos de clérigo de niveles 1–5 ni del Dominio de la Guerra la toca; el
  Acólito no da rasgos; ni «Iniciado en la magia» ni «Mejora de característica»
  llevan `efectos:` sobre `velocidad`. (Las que sí la tocan en la base —Elfo de
  los bosques, Goliat/Forma grande, Bárbaro, Explorador, Monje, Paladín, y las
  dotes Atacante a la carga, Veloz y Vigor sobrenatural— no son de este
  personaje.)

9 − 0 + 0 = **9**

### Resultado

**velocidad = 9 m**

*(Aviso de alcance: la base pone el número en el registro de especie, y no he
encontrado en los ficheros que puedo leer una frase general del tipo «la
velocidad del personaje es la de su especie». Si esa frase existe, vivirá en
`reglas/efectos.yaml`, que este encargo me prohíbe abrir — así que **no lo
apunto como hueco**, igual que la CA por defecto. El número, en cualquier caso,
es inequívoco: 9.)*

---

## 4. `cd_conjuros` — CD de salvación de sus conjuros

> `reglas/generacion_personaje.yaml → conjuros.cd_salvacion.formula`
> «8 + modificador de aptitud mágica + bonificador por competencia»
> (`conjuros.pagina: {pdf: 240, libro: 238}`, sección «Tiradas de salvación / Tiradas de ataque»)

Aptitud mágica de la clase:

> `clases/clerigo.yaml → aptitud_magica: Sabiduría`

confirmado por el propio rasgo:

> `clases/rasgos/clerigo.yaml → rasgos["Lanzamiento de conjuros"].desc`
> «… Aptitud mágica: Sabiduría. Canalizador mágico: un símbolo sagrado.»
> (pág. pdf 83 / libro 81)

y por el puntero que deja la propia regla:

> `reglas/generacion_personaje.yaml → conjuros._nota_aptitud`
> «La aptitud mágica de cada clase la declara su propio fichero, en
> `clases/<clase>.yaml → aptitud_magica`.»

Cuenta:

- 8 (`conjuros.cd_salvacion.base: 8`)
- + mod. Sabiduría = **+4** (§0.1)
- + PB = **+3** (§0.2)

8 + 4 + 3 = **15**

### Resultado

**cd_conjuros = 15**

*Contraste independiente:* el rasgo «Canalizar divinidad» de nivel 2 usa esta
CD como término ya conocido —«con salvación de Constitución CD igual a tu CD de
conjuros»— sin volver a definirla, lo que confirma que hay **una sola** CD de
conjuros para el personaje y que es la que acabo de derivar.

---

## 5. `bonif_ataque_conjuros` — bonificador de ataque con conjuros

> `reglas/generacion_personaje.yaml → conjuros.bonificador_ataque.formula`
> «modificador de aptitud mágica + bonificador por competencia»
> (`conjuros.pagina: {pdf: 240, libro: 238}`; `base: 0`)

- mod. Sabiduría = **+4**
- PB = **+3**

4 + 3 = **7**

### Resultado

**bonif_ataque_conjuros = +7**

---

## Valores derivados

| Valor | Resultado | De dónde sale, en una línea |
|---|---|---|
| `pg_max` | **44** | (8+5+5+5+6) dados/tabla + 5×(+2) Con + 5 Aguante enano |
| `ca` | **15** | 13 Camisa de malla + min(+0 Des, 2) + 2 Escudo |
| `velocidad` | **9 m** | Velocidad de Enano, sin ningún modificador aplicable |
| `cd_conjuros` | **15** | 8 + 4 (Sabiduría) + 3 (PB) |
| `bonif_ataque_conjuros` | **+7** | 4 (Sabiduría) + 3 (PB) |

Valores intermedios, por si sirven de contraste:

| Intermedio | Valor |
|---|---|
| mod. Fuerza | +1 |
| mod. Destreza | +0 |
| mod. Constitución | +2 |
| mod. Inteligencia | −1 |
| mod. Sabiduría | +4 |
| mod. Carisma | +2 |
| Bonificador por competencia | +3 |
| Dados de golpe | 5d8 |

**Los cinco valores se han podido derivar por completo desde la base.** No hay
ninguno que se quede sin número por falta de regla.

---

## Hallazgos

Ninguno de estos cambia los cinco números de arriba. Los apunto porque salieron
del camino.

### H-1 · La fórmula de CD/ataque de conjuros ya está en la base (cierre de un hallazgo previo)

Dos calculistas anteriores pararon aquí. Ya no hay dónde parar: la fórmula vive
en `reglas/generacion_personaje.yaml → conjuros`, con página (pdf 240 / libro
238) y con `_nota_aptitud` apuntando a `clases/<clase>.yaml → aptitud_magica`.
Lo dejo escrito para que la próxima tanda no lo cuente como hueco abierto: **no
lo es**.

### H-2 · `reglas/_ESQUEMA_efectos.md` está desactualizado sobre `velocidad`

La línea 97 del esquema dice, en su sección «Lo que este esquema todavía NO
representa»:

> «Es una tabla dispersa con decimales, que es el `ScaleValue` de Foundry […].
> Por eso `velocidad` no está en el vocabulario.»

Pero `velocidad` **sí** está hoy en el vocabulario, y con uso abundante:
`reglas/fuentes_de_efectos.yaml` la declara como objetivo derivado de
`equipo/armaduras.yaml` (`{campo: fuerza, objetivo: velocidad, op: add}`), y hay
efectos `objetivo: velocidad` en `especies/especies.yaml` (Goliat),
`clases/rasgos/barbaro.yaml`, `clases/rasgos/explorador.yaml`,
`clases/rasgos/monje.yaml`, `clases/subclases/paladin.yaml`,
`clases/subclases/monje.yaml`, `clases/subclases/explorador.yaml`,
`dotes/generales.yaml` y `dotes/don_epico.yaml`.

Es documentación que se quedó atrás, no una contradicción de datos —pero es
justo el tipo de frase que un lector futuro creería—. Sugerencia: reescribir
ese párrafo para que diga qué parte de `velocidad` sigue sin modelarse (el
escalado por nivel del Monje, que efectivamente se resuelve con `columna:
mov_sin_armadura_m` en `clases/rasgos/monje.yaml`) en vez de afirmar que la
variable no existe.

### H-3 · No hay forma de decir que una armadura va *puesta*

El `equipo` de la ficha es una lista de referencias con `origen`, sin ningún
campo de estado. La base tampoco tiene vocabulario para ello: `grep` de
`equipado` en `reglas/`, `equipo/` y `clases/` no devuelve nada. Y sin embargo
la distinción es cuantitativa: para este personaje son 15 de CA (con la malla
puesta y el escudo embrazado) frente a 10 (llevándolos encima). Ahora mismo eso
se resuelve por convención implícita —«si está en el equipo, se lleva puesto»—,
que es exactamente el tipo de regla que este proyecto quiere fuera del código.

El caso se agrava con `equipo/armaduras.yaml → reglas.solo_un_tipo` («no puede
llevar puesta más de una armadura ni embrazar más de un escudo a la vez»): esa
regla presupone que existe la noción de «puesta», pero la ficha no puede
expresarla. Una ficha con dos armaduras en el equipo —perfectamente legal como
posesión— no tendría manera de decir cuál lleva.

### H-4 · La ficha no registra la elección de «Orden divina» (rasgo obligatorio de nivel 1)

> `clases/rasgos/clerigo.yaml → rasgos["Orden divina"]` (nivel 1, pág. pdf 84 / libro 82)
> «Te consagras a una de estas dos funciones sacras, a tu elección: Protector
> (ganas competencia con armas marciales y entrenamiento con armaduras pesadas)
> o Taumaturgo (conoces un truco adicional de la lista de clérigo, y obtienes un
> bonificador igual a tu modificador de Sabiduría, mínimo +1, a las pruebas de
> Inteligencia (Conocimiento arcano y Religión))».

Es una elección obligatoria con consecuencias mecánicas, y en los datos crudos
no aparece: `decisiones` no la menciona, y las competencias declaradas no
delatan ninguna de las dos ramas —no hay armas marciales ni armaduras pesadas
(luego no es Protector), y los trucos de origen «clase» son exactamente 4, que
es lo que da la columna `trucos` de `clases/clerigo.yaml → progresion[n=5]` sin
el truco extra (luego tampoco parece Taumaturgo).

No afecta a ninguno de los cinco valores: el personaje viste armadura media,
que ya tiene por competencia de clase, y ninguna de las dos ramas toca PG, CA,
velocidad, CD ni ataque de conjuros. Pero es un rasgo de nivel 1 sin resolver
en la ficha.

### H-5 · La ficha no registra la aptitud mágica elegida para «Iniciado en la magia»

> `dotes/origen.yaml → dotes["Iniciado en la magia"]` (pág. pdf 203 / libro 201)
> «… aptitud mágica Inteligencia, Sabiduría o Carisma (a elección al tomar la dote).»

La dote trae su **propia** aptitud mágica, que puede no ser la de la clase. En
`decisiones` solo consta «Iniciado en la magia, lista de clérigo»; la aptitud
elegida no está. Aquí no cambia ningún número —los tres conjuros de la dote
(Piedad con los moribundos, Resistencia, Detectar el bien y el mal) no piden
tirada de salvación ni de ataque—, y el `cd_conjuros` de la ficha es el de la
clase (Sabiduría) en cualquier caso. Pero en otra combinación de dote y conjuros
esta laguna sí produciría un número equivocado, y en verde.

---

*Informe cerrado sin haber visto ningún valor calculado por el motor.*

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
pg_max: 44
ca: 15
velocidad: 9
cd_conjuros: 15
bonif_ataque_conjuros: 7
```
