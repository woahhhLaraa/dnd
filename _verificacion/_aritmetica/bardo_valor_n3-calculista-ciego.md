# Recálculo ciego a mano — `bardo_valor_n3`

**Agente:** E · «el calculista» (ronda 3 de estrés)
**Fecha:** 2026-09-06
**Ficha:** Prueba Bardo 3 — Aasimar, Bardo 3 (Colegio del Valor), trasfondo Acólito
**Entrada usada:** `/tmp/claude-0/-home-user-dnd/ccce6f54-5659-5d7c-89a3-15e0f610e8cf/scratchpad/crudos/bardo_valor_n3.yaml`
(datos crudos, **sin** bloque `calculado`)

## Método

Segunda transcripción independiente: cada número sale de leer la regla en la
base canónica y hacer la aritmética a mano, no de ejecutar el motor. Ningún
número del proyecto se ha mirado antes de escribir el propio.

### Ficheros consultados (todos de la base, ninguno de código)

| Fichero | Para qué |
|---|---|
| `reglas/generacion_personaje.yaml` | modificadores por puntuación, PG nivel 1 y siguientes, tabla de valores establecidos, PB por nivel, fórmulas de CD y ataque de conjuros |
| `reglas/caracteristicas.yaml` | emparejamiento nombre ↔ abreviatura (`car` = Carisma, etc.) |
| `reglas/fuentes_de_efectos.yaml` | qué ficheros de la base pueden conceder efectos a un personaje (para saber dónde mirar y no dejarme una fuente) |
| `clases/bardo.yaml` | dado de golpe, aptitud mágica, tabla de progresión (PB de nivel 3), equipo inicial |
| `clases/rasgos/bardo.yaml` | rasgos de bardo de niveles 1–3 |
| `clases/subclases/bardo.yaml` | Colegio del Valor, rasgos de nivel 3 |
| `especies/especies.yaml` | Aasimar: velocidad y rasgos |
| `trasfondos/trasfondos.yaml` | Acólito: características, dote, habilidades, equipo |
| `dotes/origen.yaml` | «Iniciado en la magia» (la dote que concede el trasfondo) |
| `equipo/armaduras.yaml` | catálogo de armaduras, reglas de entrenamiento, escudos y penalización de velocidad por Fuerza |
| `equipo/aventureros.yaml` | contenido del «Paquete de artista» y comprobación de que ningún paquete lleva armadura ni escudo |

### Desviaciones cometidas

Ninguna. No he abierto `calculo.py`, `efectos.py`, `reglas/efectos.yaml`,
ningún verificador, ninguna ficha de `personajes/`, ni `personajes/_hallazgos/`,
ni he listado `_verificacion/_aritmetica/` (este fichero se ha escrito
directamente sobre su ruta). No he ejecutado ningún verificador; los únicos
comandos han sido `cat`, `grep`, `sed` y `ls` sobre ficheros de datos
permitidos. No he visto ningún número calculado por el proyecto para esta
ficha ni para ninguna otra.

Sí he leído `reglas/fuentes_de_efectos.yaml` (está en `reglas/` y no es
`efectos.yaml`). Lo he usado solo como mapa de *dónde buscar* efectos, no como
fuente de ningún número.

---

## Paso 0 — Insumos comunes

### 0.1 Modificadores de característica

Puntuaciones finales, de los datos crudos, campo `caracteristicas.final`:
`fue 10 · des 13 · con 14 · int 10 · sab 13 · car 15`.

Comprobación de que ese `final` es coherente con lo declarado: `base`
(car 15, con 14, des 13, sab 12, fue 10, int 8) + `ajuste_trasfondo`
(int +2, sab +1) → int 8+2 = 10 ✓, sab 12+1 = 13 ✓, el resto sin cambio ✓.
Las dos características ajustadas están entre las tres del trasfondo
(`trasfondos/trasfondos.yaml → trasfondos[Acólito].caracteristicas:
[Inteligencia, Sabiduría, Carisma]`) y el reparto +2/+1 es uno de los dos
permitidos (`reglas/generacion_personaje.yaml →
metodos_generacion_caracteristicas.ajuste_por_trasfondo`). En nivel 3 no hay
Mejora de característica (`clases/bardo.yaml → progresion`, n:4 es la primera).

Fórmula: `(puntuación − 10) / 2, redondeando hacia abajo`
— `reglas/generacion_personaje.yaml → metodos_generacion_caracteristicas.modificadores_por_puntuacion.formula`

| Característica | Puntuación | Cuenta | Mod. | Tabla del mismo campo |
|---|---|---|---|---|
| Fuerza | 10 | (10−10)/2 = 0 | **0** | «10-11»: 0 ✓ |
| Destreza | 13 | (13−10)/2 = 1,5 → 1 | **+1** | «12-13»: 1 ✓ |
| Constitución | 14 | (14−10)/2 = 2 | **+2** | «14-15»: 2 ✓ |
| Inteligencia | 10 | (10−10)/2 = 0 | **0** | «10-11»: 0 ✓ |
| Sabiduría | 13 | (13−10)/2 = 1,5 → 1 | **+1** | «12-13»: 1 ✓ |
| Carisma | 15 | (15−10)/2 = 2,5 → 2 | **+2** | «14-15»: 2 ✓ |

### 0.2 Bonificador por competencia

Nivel total 3 (`nivel_total: 3` en los datos crudos; una sola clase, Bardo 3).

- `clases/bardo.yaml → progresion`, fila `{n: 3, pb: 2, …}` → **PB = +2**
- `reglas/generacion_personaje.yaml → px_por_nivel.filas`, `{nivel: 3, px: 900, pb: 2}` → **PB = +2**

Las dos fuentes coinciden: **PB = +2**.

### 0.3 Barrido de fuentes de efectos (para no dejarme ninguna)

`reglas/fuentes_de_efectos.yaml` declara que lo que puede conceder algo
calculable a un personaje son: rasgos de especie, rasgos de clase, rasgos de
subclase, dotes, trasfondos, y —como fuente *derivada*— `equipo/armaduras.yaml`.
Recorro las seis para este personaje:

- **Especie (Aasimar)** — `especies/especies.yaml → especies[Aasimar].rasgos`:
  Manos curativas, Portador de luz, Resistencia celestial, Visión en la
  oscuridad, y Revelación celestial (nivel 3). Ninguno toca PG, CA ni velocidad
  de forma permanente. Detalle de Revelación celestial: la opción «Alas
  celestiales» da *velocidad volando igual a tu velocidad* durante 1 minuto,
  una vez por descanso largo → es una transformación temporal, no cambia la
  velocidad de la ficha (además es igual a ella, no la aumenta).
- **Rasgos de clase (Bardo 1–3)** — `clases/rasgos/bardo.yaml`: Inspiración
  bárdica (1), Lanzamiento de conjuros (1), Aprendiz de mucho (2), Pericia (2).
  Ninguno toca PG, CA ni velocidad.
- **Subclase (Colegio del Valor, nivel 3)** — ver §2.3 y §2.4: Entrenamiento
  marcial e Inspiración en combate. Se analizan abajo.
- **Dote** — `trasfondos/trasfondos.yaml → trasfondos[Acólito].dote:
  "Iniciado en la magia (clérigo)"`. Su texto en `dotes/origen.yaml` (pdf 203,
  libro 201) concede dos trucos y un conjuro de nivel 1 de la lista de clérigo.
  No toca PG, CA, velocidad, ni la CD/ataque de los conjuros *de bardo*.
  (Observación aparte en §6.)
- **Trasfondo (Acólito)** — `trasfondos/trasfondos.yaml`: no tiene texto de
  rasgo (`no_automatizado`); concede características, dote, habilidades,
  herramienta y equipo. Nada calculable más.
- **Equipo/armaduras** — ver §2.

---

## 1 · `pg_max`

**Regla del nivel 1** — `reglas/generacion_personaje.yaml → puntos_golpe.nivel_1.regla`
(pdf 42, libro 40): «Máximo del dado de golpe + modificador por Constitución.»

**Dado de golpe del Bardo** — `clases/bardo.yaml → atributos_basicos.dado_golpe: d8`.
Máximo de un d8 = **8**.

- Nivel 1: 8 + mod. Con (+2) = **10**

**Regla de los niveles siguientes** — `reglas/generacion_personaje.yaml →
puntos_golpe.niveles_siguientes_al_1.literal` (pdf 44, libro 42): «Cada vez que
subas un nivel, obtendrás un dado de golpe adicional. Tira ese dado, suma tu
modificador por Constitución al resultado y añade el total (mínimo de 1) a tus
puntos de golpe máximos. **En vez de tirar**, puedes utilizar el valor
establecido que se muestra en la tabla "Puntos de golpe establecidos por clase".»

Lectura: el valor establecido sustituye **la tirada del dado**, no el total; el
modificador por Constitución se sigue sumando. Dos razones, ambas de la base:
(a) la frase es «en vez de tirar», y la suma de Con es una oración aparte;
(b) la propia tabla lo confirma numéricamente — d12→7, d10→6, d8→5, d6→4 son
exactamente «media del dado redondeando arriba», sin rastro de ninguna
Constitución dentro.

**Valor establecido del Bardo** — `reglas/generacion_personaje.yaml →
puntos_golpe.niveles_siguientes_al_1.tabla_valores_establecidos.filas`,
fila `{clases: [Bardo, Brujo, Clérigo, Druida, Monje, Pícaro], valor: 5}` → **5**.
Coincide con lo que declaran los datos crudos en `pg_por_nivel` (niveles 2 y 3,
`metodo: valor_establecido`, `valor: 5`).

- Nivel 2: 5 + 2 = 7 (≥ 1, el mínimo no muerde) → **7**
- Nivel 3: 5 + 2 = 7 (≥ 1) → **7**

**Suma:** 10 + 7 + 7 = **24**

**Comprobación por la otra vía** (la que sugiere
`puntos_golpe.aumento_de_constitucion._nota_para_el_motor`: término de dado
acumulado + `nivel_total × mod_con`):
(8 + 5 + 5) + (3 × 2) = 18 + 6 = **24** ✓

**Efectos adicionales sobre PG:** ninguno. El único rasgo de la base que suma
PG máximos por especie es «Aguante enano» (`especies/especies.yaml →
especies[Enano]`), y este personaje es Aasimar. Ningún rasgo de bardo, de
Colegio del Valor, ni la dote «Iniciado en la magia» toca `pg_max`.

### → `pg_max = 24`

---

## 2 · `ca`

### 2.1 Equipo de la ficha, objeto a objeto

Los datos crudos traen **un único objeto** en `equipo`:

- `equipo/armaduras.yaml#Armadura de cuero tachonado`

Lo busco en el catálogo: `equipo/armaduras.yaml → armaduras_ligeras.tabla`,
registro `{nombre: "Armadura de cuero tachonado", ca: "12 + mod. Des",
fuerza: null, sigilo: null, peso_kg: 6.5, precio: "45 po"}` (fuente del fichero:
pdf 218, libro 216). El nombre casa exactamente. Es **armadura ligera** y su
fórmula **no lleva tope de Destreza** (los topes «(máx. 2)» solo aparecen en
`armaduras_medias`).

**No hay escudo** en la ficha, ni ningún otro objeto.

### 2.2 El paquete de `equipo/aventureros.yaml`

La ficha no lleva ningún paquete: `equipo` tiene un solo elemento, y el campo
`decisiones` de los datos crudos lo dice con todas las letras («el equipo
inicial vive como prosa en la base, así que esta ficha solo lleva armadura; el
inventario queda vacío a propósito», citando `clases/bardo.yaml →
atributos_basicos.equipo_inicial`).

Aun así compruebo qué habría dentro si se hubiera expandido, porque es lo que
la opción (a) del equipo inicial de bardo incluye: `equipo/aventureros.yaml`,
`"Paquete de artista": "Contiene: campana, cantimplora, 3 disfraces, espejo,
8 frascos de aceite, linterna de ojo de buey, mochila, petate, raciones para
9 días y yesquero."` → **ni armadura ni escudo**. Barrido el fichero entero
buscando «armadura» y «escudo»: los únicos aciertos son el «Símbolo sagrado»
(que puede ser un emblema *sobre* un escudo, no un escudo), la «Barda»
(armadura para monturas) y la regla general de vestir objetos. Ningún paquete
de `equipo/aventureros.yaml` concede CA. El resultado no cambiaría.

### 2.3 Entrenamiento (¿usa bien lo que lleva?)

`equipo/armaduras.yaml → reglas.entrenamiento`: «Cualquiera puede ponerse una
armadura o embrazar un escudo, pero solo quien tenga entrenamiento con ese tipo
la usa de forma efectiva.» Y `reglas.sin_entrenamiento`: sin entrenamiento hay
desventaja en pruebas de d20 de Fuerza o Destreza y no se pueden lanzar
conjuros — obsérvese que la penalización **no es un cambio de CA**.

Entrenamiento del personaje con armaduras:
- `competencias.armaduras` de los datos crudos: `Armaduras ligeras` (origen: clase Bardo),
  que casa con `clases/bardo.yaml → atributos_basicos.armaduras: ["Armaduras ligeras"]`.
- Además, `clases/subclases/bardo.yaml → Colegio del Valor → rasgo nivel 3
  "Entrenamiento marcial"` (pdf 69, libro 67): «Competencia con armas marciales
  y **entrenamiento con armaduras medias y escudos**.»

La armadura de cuero tachonado es **ligera** → entrenado por la clase ✓. Ni
desventaja ni bloqueo de conjuros.

El entrenamiento con escudos del Colegio del Valor **no aporta nada aquí**
porque no hay escudo en la ficha: `equipo/armaduras.yaml → reglas.escudos`
(«Solo obtienes el bonificador a la CA de un escudo si tienes entrenamiento con
escudos») necesita un escudo embrazado, y el catálogo pone el escudo en
`escudos.tabla` con `ca: "+2"` — un objeto que este personaje no tiene. Si
alguna vez lo comprara, sí lo usaría (+2, entrenado por la subclase); hoy no.
Lo mismo con las armaduras medias: puede llevarlas, pero no lleva ninguna.

### 2.4 El rasgo de nivel 3 que menciona la CA — y por qué lo descarto

`clases/subclases/bardo.yaml → Colegio del Valor → rasgo nivel 3
"Inspiración en combate"` (pdf 69, libro 67), texto entero:

> «Una criatura que tenga uno de tus dados de Inspiración bárdica puede usarlo
> para: **Defensa** (cuando un ataque la acierte, usa su reacción para tirar el
> dado y sumarlo a su CA contra ese ataque, pudiendo hacer que falle) u
> **Ofensiva** (justo después de acertar con una tirada de ataque, tira el dado
> y suma el resultado al daño).»

**Decisión: NO aporta al número permanente de CA de la ficha.** Cuatro razones,
todas del propio texto:

1. **Beneficiario equivocado.** El bonificador va a la CA de «una criatura que
   tenga uno de tus dados de Inspiración bárdica», es decir a **su** CA, no
   necesariamente a la del bardo. Inspiración bárdica se da «a otra criatura»
   (`clases/rasgos/bardo.yaml → "Inspiración bárdica"`, pdf 61, libro 59), así
   que el caso típico es que el número suba en la ficha de otro.
2. **Es reactivo y puntual.** Requiere que un ataque ya haya acertado, gastar
   la reacción, y solo vale «contra ese ataque».
3. **Es un dado, no un número.** Se tira el dado de Inspiración bárdica (d6 en
   nivel 3, `clases/bardo.yaml → progresion`, n:3, `dado: d6`): el valor es
   aleatorio entre +1 y +6, y no existe un número fijo que escribir.
4. **Se consume.** Gasta el dado, cuyos usos son limitados (mod. de Carisma por
   descanso largo).

La propia base lo clasifica igual: el registro `efectos` de ese rasgo lleva
`{objetivo: ca, op: conditional, texto: "Defensa: quien tenga un dado de
Inspiración bárdica puede gastarlo con su reacción para sumarlo a SU CA contra
un ataque concreto"}` — `op: conditional`, no `add` ni `base`. (Contrástese con
el otro rasgo de nivel 3 con CA en el mismo fichero, «Juego de pies
deslumbrante» del Colegio de la Danza, que sí lleva `op: base` con fórmula:
ese sí sería un cálculo permanente, pero es de otra subclase.)

El otro rasgo de nivel 3, «Entrenamiento marcial», tampoco aporta CA: concede
*entrenamiento*, que es un permiso, no un número (§2.3).

### 2.5 Cuenta

CA = 12 (base de la armadura de cuero tachonado) + mod. Des (+1) = **13**

Sin tope de Destreza que aplicar (armadura ligera), sin escudo, sin rasgo
permanente que modifique la CA. La CA por defecto sin armadura no interviene:
el personaje lleva armadura.

### → `ca = 13`

---

## 3 · `velocidad`

**Base de especie** — `especies/especies.yaml → especies[Aasimar].velocidad_m: 9`
(pdf 188, libro 186) → **9 m**.

**¿Penalización por armadura?** — `equipo/armaduras.yaml → reglas.fuerza`: «Si
la tabla indica una puntuación de Fuerza para un tipo de armadura, esta reduce
3 m la velocidad de quien la lleve, salvo que su Fuerza sea igual o superior a
la indicada.» El registro de la armadura de cuero tachonado tiene
`fuerza: null` → la tabla **no indica** puntuación de Fuerza → **no hay
reducción**. (La Fuerza 10 del personaje ni siquiera llega a evaluarse; solo
las armaduras pesadas «Cota de malla», «Armadura de bandas» y «Armadura de
placas» traen un valor en ese campo.)

**¿Algún rasgo?** Ninguno de los revisados en §0.3 modifica la velocidad
caminando de forma permanente:
- Aasimar «Revelación celestial» (nivel 3) → «Alas celestiales» da velocidad
  **volando** igual a tu velocidad, durante 1 minuto, 1 vez por descanso largo:
  temporal, y ni siquiera cambia el número.
- Bardo 1–3 y Colegio del Valor 3: nada sobre velocidad.
- Dote «Iniciado en la magia»: nada sobre velocidad.
- (El único rasgo de especie de la base que sube velocidad de forma
  condicionada es «Forma grande» de Goliat, marcado `op: conditional`; y el
  linaje «Elfo de los bosques» sube la base a 10,5 m. Ninguno aplica aquí.)

### → `velocidad = 9 m`

---

## 4 · `cd_conjuros`

**Fórmula** — `reglas/generacion_personaje.yaml → conjuros.cd_salvacion.formula`
(pdf 240, libro 238, sección «Tiradas de salvación / Tiradas de ataque»):
«8 + modificador de aptitud mágica + bonificador por competencia», con `base: 8`.

**Aptitud mágica** — `clases/bardo.yaml → aptitud_magica: Carisma`. Concuerda con
`clases/bardo.yaml → atributos_basicos.caracteristica_principal: Carisma` y con
`clases/rasgos/bardo.yaml → "Lanzamiento de conjuros"`: «Aptitud mágica: Carisma.»
Y `reglas/generacion_personaje.yaml → conjuros._nota_aptitud` confirma que la
aptitud se lee del fichero de la clase.

**Cuenta:**

    CD = 8 + mod. Car + PB
       = 8 + 2 + 2
       = 12

Un solo lanzador: el personaje es Bardo 3 puro, sin multiclase, así que no hay
que aplicar nada de `multiclase.lanzamiento_de_conjuros_multiclase`. El truco
*luz* del rasgo aasimar «Portador de luz» también usa Carisma, así que no
introduce una segunda CD distinta.

### → `cd_conjuros = 12`

---

## 5 · `bonif_ataque_conjuros`

**Fórmula** — `reglas/generacion_personaje.yaml → conjuros.bonificador_ataque.formula`
(misma página: pdf 240, libro 238): «modificador de aptitud mágica +
bonificador por competencia», con `base: 0`.

**Cuenta:**

    Ataque = mod. Car + PB
           = 2 + 2
           = +4

### → `bonif_ataque_conjuros = +4`

---

## 6 · Observaciones (no cambian los cinco números, pero conviene que consten)

1. **La armadura de la ficha no es la del equipo inicial declarado.**
   `clases/bardo.yaml → atributos_basicos.equipo_inicial.a` dice «**armadura de
   cuero**, 2 dagas, instrumento musical a elección, paquete de artista y 19 po».
   La ficha lleva «Armadura de cuero **tachonado**», que es otro registro del
   catálogo (`ca: "12 + mod. Des"`, 45 po) frente a la armadura de cuero a secas
   (`ca: "11 + mod. Des"`, 10 po). Derivo desde lo que la ficha declara llevar
   → CA 13. Si el objeto correcto fuera el de la opción (a), la CA sería
   11 + 1 = **12**. Dejo constancia de las dos lecturas y elijo la primera: el
   bloque `calculado` debe describir al personaje tal como su `equipo` lo viste,
   y arreglar la procedencia del objeto es un problema del generador, no de la
   aritmética. Además, la opción (a) tampoco se ha seguido en lo demás (faltan
   las 2 dagas, el instrumento, el paquete y las 19 po), cosa que el propio
   campo `decisiones` reconoce.
2. **La dote del trasfondo no está en la ficha.**
   `trasfondos/trasfondos.yaml → trasfondos[Acólito].dote` concede «Iniciado en
   la magia (clérigo)», y los datos crudos no traen ningún bloque `dotes` ni los
   dos trucos y el conjuro de nivel 1 que esa dote otorga
   (`dotes/origen.yaml`, pdf 203, libro 201). No afecta a ninguno de los cinco
   valores, pero es un hueco de los datos crudos.
3. **Competencia con armas marciales sin registrar.** «Entrenamiento marcial»
   (Colegio del Valor, nivel 3) concede competencia con armas marciales y
   entrenamiento con armaduras medias y escudos; `competencias.armas` de los
   datos crudos solo lista «Armas sencillas» (origen: clase) y
   `competencias.armaduras` solo «Armaduras ligeras». Tampoco afecta a los
   cinco valores —el personaje no lleva escudo ni armadura media— pero la ficha
   no refleja lo que la subclase le da.
4. **Nada quedó sin derivar.** Los cinco valores salen enteros de la base, con
   página. En particular, la fórmula de la CD de conjuros está donde el encargo
   avisaba (`reglas/generacion_personaje.yaml → conjuros`, pdf 240 / libro 238)
   y no ha hecho falta suponer nada.

---

## Valores derivados

| Valor | Resultado | Derivación en una línea | Cita principal |
|---|---|---|---|
| `pg_max` | **24** | (8 máx. d8 + 2) + (5 + 2) + (5 + 2); o 18 de dados + 3 × (+2) de Con | `reglas/generacion_personaje.yaml → puntos_golpe.nivel_1` y `.niveles_siguientes_al_1` (pdf 42/44) + `clases/bardo.yaml → atributos_basicos.dado_golpe` |
| `ca` | **13** | 12 (cuero tachonado, ligera, sin tope de Des) + 1 (mod. Des); sin escudo; «Inspiración en combate» descartada por situacional | `equipo/armaduras.yaml → armaduras_ligeras.tabla` (pdf 218 / libro 216) |
| `velocidad` | **9 m** | 9 m de Aasimar; la armadura no indica Fuerza → sin −3 m; ningún rasgo permanente | `especies/especies.yaml → especies[Aasimar].velocidad_m` (pdf 188 / libro 186) + `equipo/armaduras.yaml → reglas.fuerza` |
| `cd_conjuros` | **12** | 8 + 2 (mod. Car) + 2 (PB) | `reglas/generacion_personaje.yaml → conjuros.cd_salvacion.formula` (pdf 240 / libro 238) + `clases/bardo.yaml → aptitud_magica` |
| `bonif_ataque_conjuros` | **+4** | 2 (mod. Car) + 2 (PB) | `reglas/generacion_personaje.yaml → conjuros.bonificador_ataque.formula` (pdf 240 / libro 238) |

Insumos usados en varias filas: **mod. Des +1**, **mod. Con +2**, **mod. Car +2**
(`reglas/generacion_personaje.yaml → …modificadores_por_puntuacion`), **PB +2**
(`clases/bardo.yaml → progresion`, n:3, y `reglas/generacion_personaje.yaml →
px_por_nivel`, nivel 3).
