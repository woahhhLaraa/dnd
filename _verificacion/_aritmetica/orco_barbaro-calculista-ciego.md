# Derivación a mano — `orco_barbaro` (Grosh Colmillo Roto)

**Agente E · «el calculista» — ronda 3 de estrés**
Fecha: 2026-09-06

---

## Cabecera

### Ficha

| Campo | Valor (de los datos crudos) |
|---|---|
| Nombre | Grosh Colmillo Roto |
| Especie | Orco (`especies/especies.yaml#Orco`) |
| Clase | Bárbaro nivel 1, sin subclase |
| Nivel total | 1 |
| Trasfondo | Soldado (`trasfondos/trasfondos.yaml#Soldado`) |
| Dote | Atacante salvaje (de origen, por trasfondo) |
| Características finales | Fue 17 · Des 13 · Con 15 · Int 10 · Sab 12 · Car 8 |

### Método

Transcripción independiente. Cada número de este informe se ha derivado leyendo
**el texto de la regla** en los ficheros de la base y haciendo la aritmética a
mano, sin ejecutar nada y sin ver ningún valor calculado por el motor del
proyecto. La entrada ha sido exclusivamente la copia **cruda** de la ficha
(sin bloque `calculado`):

    /tmp/claude-0/-home-user-dnd/ccce6f54-5659-5d7c-89a3-15e0f610e8cf/scratchpad/crudos/orco_barbaro.yaml

### Ficheros consultados

| Fichero | Para qué |
|---|---|
| `clases/barbaro.yaml` | dado de golpe, `lanzador`, progresión (nivel de cada rasgo), competencias de armadura |
| `clases/rasgos/barbaro.yaml` | texto de «Defensa sin armadura», «Furia», «Maestría con armas», «Movimiento rápido» |
| `clases/subclases/barbaro.yaml` | comprobar que las subclases empiezan en nivel 3 (`niveles_de_subclase`) |
| `clases/_ESQUEMA_atributos_basicos.md` | confirmar la forma del campo `dado_golpe` (`d12` = «1d12 por nivel») |
| `especies/especies.yaml` | velocidad base y rasgos del Orco |
| `trasfondos/trasfondos.yaml` | Soldado: características ajustables, dote, equipo |
| `dotes/origen.yaml` | texto de «Atacante salvaje» (y contraste con «Duro», que sí toca `pg_max`) |
| `reglas/generacion_personaje.yaml` | tabla de modificadores, regla de PG de nivel 1, fórmulas de conjuros, `px_por_nivel` |
| `reglas/caracteristicas.yaml` | emparejamiento nombre ↔ abreviatura (`Constitución` ↔ `con`) |
| `reglas/fuentes_de_efectos.yaml` | qué ficheros de la base **pueden** conceder efectos (para no dejarme ninguno) |
| `reglas/subida_de_nivel.yaml` | qué concede la base al subir de nivel |
| `equipo/armaduras.yaml` | catálogo completo de armaduras y escudos; reglas de entrenamiento, Fuerza mínima y sigilo |
| `equipo/armas.yaml` | comprobar que las armas de la ficha son armas y no armadura |
| `equipo/aventureros.yaml` | contenido de «Paquete de explorador», «Ropas de viaje», «Aljaba», «Útiles de sanador» |

### Desviaciones cometidas — declaración honesta

**No he abierto ningún fichero prohibido.** Ni `calculo.py`, ni `efectos.py`,
ni `reglas/efectos.yaml`, ni ningún verificador, ni nada bajo `_verificacion/`
(salvo escribir este informe), ni `personajes/` (ni la ficha original, ni otras
fichas, ni `personajes/_hallazgos/`), ni `_verificacion/_aritmetica/`.

Cuatro matices que declaro por transparencia, ninguno de los cuales me ha
mostrado un número calculado de esta ficha:

1. **Bloques `efectos:` dentro de ficheros de la base permitidos.**
   `clases/rasgos/barbaro.yaml`, `especies/especies.yaml` y `dotes/origen.yaml`
   traen, junto al texto en prosa de algunos rasgos, un bloque `efectos:` con la
   fórmula ya formalizada. Están dentro de ficheros que el encargo permite
   expresamente y son **transcripción de la regla**, no valores de esta ficha.
   Aun así, para preservar la independencia he derivado **siempre desde el
   `desc` en prosa** y sólo después he mirado el `efectos:` como confirmación.
   En los tres casos coinciden; lo digo en cada apartado.

2. **`reglas/fuentes_de_efectos.yaml`.** Está en `reglas/` y no es
   `efectos.yaml`, así que es lectura permitida. Lo he usado para una cosa
   concreta y necesaria: saber de forma exhaustiva **qué ficheros de la base
   pueden conceder efectos**, y así poder afirmar con fundamento que no me dejo
   ninguna fuente. Sus comentarios hablan del motor y de fallos históricos del
   proyecto, pero no contienen ningún número de esta ficha.

3. **La cabecera de `reglas/generacion_personaje.yaml → conjuros`** menciona el
   propio mandato del calculista y a dos agentes anteriores que pararon en la
   fórmula de la CD de conjuros. Lo he leído porque venía pegado a la regla que
   necesitaba. No trae ningún valor de esta ficha.

4. **Listado de la raíz del proyecto** (`ls /home/user/dnd/`): he visto los
   *nombres* de los ficheros de código y de los planes, no su contenido.

**Hallazgo previo ya conocido, no lo cuento como nuevo:** la CA por defecto sin
armadura (`10 + mod. Destreza`) vive en `reglas/efectos.yaml`, fichero que este
encargo me prohíbe. La doy por buena tal como el encargo indica y no la anoto
como hueco de la base.

---

## Paso 0 — Modificadores de característica

Los cuatro valores dependen de los modificadores, así que los derivo primero.

**Regla.** `reglas/generacion_personaje.yaml → metodos_generacion_caracteristicas.modificadores_por_puntuacion`
(fuente del bloque: `pagina_pdf: 40`, `libro: 38`, cap. 2, «Paso 3: determinar
las puntuaciones de característica»):

> `formula: "(puntuación - 10) / 2, redondeando hacia abajo"`

El mismo bloque trae una `tabla:` explícita que uso como segunda comprobación.

**Qué puntuaciones uso: las finales.** El mismo fichero, en
`metodos_generacion_caracteristicas.ajuste_por_trasfondo`, dice que el ajuste del
trasfondo se aplica *«tras asignar las puntuaciones»*; por tanto los
modificadores se derivan del bloque `caracteristicas.final` de la ficha, no del
`base`. Comprobación de coherencia de esa suma (no es uno de mis cuatro valores,
pero sostiene los que sí lo son):

- `base` = Fue 15 / Des 13 / Con 14 / Int 10 / Sab 12 / Car 8 → coincide
  exactamente con la fila `{clase: Bárbaro, fue: 15, des: 13, con: 14, int: 10, sab: 12, car: 8}`
  de `reglas/generacion_personaje.yaml → conjunto_estandar_por_clase.filas`.
- `ajuste_trasfondo` = +2 Fue, +1 Con. El trasfondo Soldado permite ajustar
  `[Fuerza, Destreza, Constitución]`
  (`trasfondos/trasfondos.yaml → trasfondos[Soldado].caracteristicas`, pdf 187 /
  libro 185), y el reparto legal es *«+2 a una y +1 a otra, o +1 a cada una de
  las tres»* (`trasfondos.yaml → reparto_caracteristicas`). +2 Fue / +1 Con
  encaja. Ningún valor pasa de 20.
- `final` = 15+2 = **17** Fue; 13 Des; 14+1 = **15** Con; 10 Int; 12 Sab; 8 Car. ✔

**Derivación de cada modificador:**

| Característica | Puntuación final | `(p − 10) / 2` redondeado abajo | Fila de la tabla | Modificador |
|---|---|---|---|---|
| Fuerza | 17 | (17−10)/2 = 3,5 → 3 | `"16-17": 3` | **+3** |
| Destreza | 13 | (13−10)/2 = 1,5 → 1 | `"12-13": 1` | **+1** |
| Constitución | 15 | (15−10)/2 = 2,5 → 2 | `"14-15": 2` | **+2** |
| Inteligencia | 10 | (10−10)/2 = 0 | `"10-11": 0` | **0** |
| Sabiduría | 12 | (12−10)/2 = 1 | `"12-13": 1` | **+1** |
| Carisma | 8 | (8−10)/2 = −1 | `"8-9": -1` | **−1** |

Los dos caminos (fórmula y tabla) coinciden en las seis.

El emparejamiento «Constitución» ↔ `con` (necesario para leer el bloque
`caracteristicas.final` de la ficha) lo declara
`reglas/caracteristicas.yaml → caracteristicas[2]`:
`{nombre: "Constitución", abrev: "con", variable: "mod_con"}`.

**Bonificador por competencia (dato auxiliar).** Nivel 1 → **+2**, por dos
fuentes que coinciden: `clases/barbaro.yaml → progresion[n:1].pb = 2` y
`reglas/generacion_personaje.yaml → px_por_nivel.filas[nivel:1].pb = 2`
(tabla «Progreso de los personajes», pdf 43 / libro 41).

---

## Paso 1 — Inventario de fuentes de efectos que le tocan a Grosh

Antes de calcular nada, cierro la lista de sitios de donde puede salir un
modificador, para poder afirmar que no me dejo ninguno.
`reglas/fuentes_de_efectos.yaml → fuentes` y `→ derivadas` declaran que sólo
pueden conceder efectos: `especies/especies.yaml`, `clases/rasgos/*.yaml`,
`clases/subclases/*.yaml`, `dotes/*.yaml`, `trasfondos/*.yaml` y —derivados de
sus campos `ca` y `fuerza`— `equipo/armaduras.yaml`. Repaso los seis para esta
ficha:

| Fuente | Qué le aplica a Grosh | ¿Modifica `pg_max`, `ca` o `velocidad`? |
|---|---|---|
| `especies/especies.yaml → Orco` (pdf 197 / libro 195) | Aguante incansable · Descarga de adrenalina · Visión en la oscuridad 36 m | **No.** «Aguante incansable» *recupera* 1 PG al llegar a 0, no sube el máximo. «Descarga de adrenalina» da **PG temporales** iguales al PB, que no son PG máximos, y permite correr como acción adicional, que no cambia la velocidad. Ninguno de los tres lleva bloque `efectos:` (los únicos de ese fichero son los del Enano, línea 67, y el Goliat, línea 94). |
| `clases/rasgos/barbaro.yaml`, rasgos de nivel 1 | Defensa sin armadura · Furia · Maestría con armas | **Sí, uno:** «Defensa sin armadura» → `ca`. Ver Paso 3. «Furia» y «Maestría con armas» no tocan ninguno de los tres. |
| `clases/rasgos/barbaro.yaml`, rasgos de nivel > 1 | «Movimiento rápido» (nivel 5) toca `velocidad` | **No aplica: el personaje es nivel 1.** Ver Paso 4. |
| `clases/subclases/barbaro.yaml` | ninguno | `niveles_de_subclase: [3, 6, 10, 14]`, y la ficha trae `subclase: null` a nivel 1. Nada que aplicar. |
| `dotes/origen.yaml → Atacante salvaje` (pdf 203 / libro 201) | tirar dos veces los dados de daño una vez por turno | **No.** No lleva bloque `efectos:` (el único de ese fichero, línea 35, es el de la dote «Duro», que Grosh **no** tiene). |
| `trasfondos/trasfondos.yaml → Soldado` (pdf 187 / libro 185) | características, dote, habilidades, herramienta, equipo | **No.** El registro no lleva ningún bloque `efectos:`, y su propio campo `no_automatizado` dice que lo que concede son campos estructurados, «no prosa con mecánica escondida». |
| `equipo/armaduras.yaml` | **nada: no lleva armadura ni escudo** | Ver Paso 2. |

---

## Paso 2 — Comprobación de la condición «sin armadura»

Es la condición que gobierna la CA de este personaje, así que la compruebo
aparte y a conciencia.

**El catálogo completo de armaduras** de la base es
`equipo/armaduras.yaml` (pdf 218 / libro 216) y son 14 entradas:

- `armaduras_ligeras`: Armadura acolchada, Armadura de cuero, Armadura de cuero tachonado
- `armaduras_medias`: Armadura de pieles, Camisa de malla, Cota de escamas, Coraza, Media armadura
- `armaduras_pesadas`: Cota guarnecida, Cota de malla, Armadura de bandas, Armadura de placas
- `escudos`: Escudo (`ca: "+2"`)

**El equipo de Grosh**, uno por uno, con el fichero en el que vive cada pieza:

| Objeto de la ficha | Fichero de la base | ¿Es armadura o escudo? |
|---|---|---|
| Hacha a dos manos | `equipo/armas.yaml` (marciales, 1d12 cortante) | No, arma |
| Hacha de mano ×4 | `equipo/armas.yaml` (1d6 cortante, arrojadiza/ligera) | No, arma |
| Paquete de explorador | `equipo/aventureros.yaml` | No. Su contenido declarado: «10 antorchas, cantimplora, cuerda, 2 frascos de aceite, mochila, petate, raciones para 10 días y yesquero». Ninguna armadura dentro. |
| Lanza | `equipo/armas.yaml` (1d6 perforante) | No, arma |
| Arco corto | `equipo/armas.yaml` (1d6 perforante) | No, arma |
| Aljaba (20 flechas) | `equipo/aventureros.yaml` | No, contenedor de munición |
| Juego · Dados | `equipo/herramientas.yaml` | No, herramienta |
| Útiles de sanador | `equipo/aventureros.yaml` | No, equipo |
| Ropas de viaje | `equipo/aventureros.yaml` | **No.** Es la única pieza que podría dar dudas por ser prenda. No figura en `equipo/armaduras.yaml`, no tiene campo `ca`, y su descripción es «Prendas resistentes diseñadas para viajar por diversos entornos». Es ropa, no armadura. |

**Conclusión: no lleva armadura de ningún tipo y no lleva escudo.** La condición
del rasgo se cumple. Y la propia ficha lo registra como decisión explícita de
creación: `decisiones[]` → *«defensa sin armadura, sin escudo ni armadura
equipados»*, citando `clases/rasgos/barbaro.yaml → rasgo: Defensa sin armadura`.

*Nota lateral, sin efecto aquí:* Grosh **sí tiene** competencia con armaduras
ligeras, medias y escudos (`clases/barbaro.yaml → atributos_basicos.armaduras`),
o sea que podría llevarlas; simplemente no lo hace. La regla
`equipo/armaduras.yaml → reglas.solo_un_tipo` («no más de una armadura ni más de
un escudo a la vez») tampoco entra en juego.

---

## Paso 3 — Los cuatro valores

### 3.1 · `pg_max` — puntos de golpe máximos

**Regla aplicable.** `reglas/generacion_personaje.yaml → puntos_golpe.nivel_1`
(`pagina: {pdf: 42, libro: 40}`):

> `regla: "Máximo del dado de golpe + modificador por Constitución."`

Uso esta y no `puntos_golpe.niveles_siguientes_al_1` (pdf 44 / libro 42) porque
el personaje es de nivel 1 y no ha subido ningún nivel: no hay ningún dado que
tirar ni ningún «valor establecido» (7 para el Bárbaro) que aplicar. El propio
fichero avisa de que son «dos reglas distintas, en dos sitios».

**Dado de golpe.** `clases/barbaro.yaml → atributos_basicos.dado_golpe: d12`
(bloque `atributos_basicos.fuente: {pagina_pdf: 53, pagina_libro: 51}`).
Según `clases/_ESQUEMA_atributos_basicos.md` (regla 2), la forma `d12` significa
«1d12 por nivel», sin el 1 delante. **Máximo de un d12 = 12.**

**Modificador por Constitución.** Del Paso 0: Con 15 → **+2**.

**Aritmética:**

```
    pg_max = máximo del dado de golpe  +  mod. Constitución
           = 12                        +  2
           = 14
```

**Modificadores adicionales sobre `pg_max`: ninguno.** Del inventario del
Paso 1: el Orco no tiene un rasgo tipo «Aguante enano» (ese es del Enano,
`especies.yaml` línea 67, `pg_max op:add "nivel_total"`), y la dote de Grosh es
«Atacante salvaje», no «Duro» (esa sí lleva `pg_max op:add "2 * nivel_total"`,
`dotes/origen.yaml` línea 35). Es exactamente el par de trampas que este
personaje evita por poco: si el trasfondo hubiese sido Campesino, la dote sería
«Duro» y habría +2 PG.

> **`pg_max = 14`**

---

### 3.2 · `ca` — clase de armadura

**Regla aplicable.** `clases/rasgos/barbaro.yaml → rasgos[Defensa sin armadura]`,
nivel 1, `pagina: {pdf: 53, libro: 51}`. Texto literal del `desc`:

> «Mientras no lleves armadura alguna, tu clase de armadura base es 10 +
> modificador de Destreza + modificador de Constitución. Obtienes este beneficio
> aunque lleves un escudo.»

El bloque `efectos:` que ese mismo registro trae a continuación formaliza lo
mismo y confirma mi lectura del texto:
`{objetivo: ca, op: base, formula: "10 + mod_des + mod_con", requiere: [sin_armadura]}`.

**Condición.** `requiere: sin_armadura` — comprobada en el Paso 2: **se cumple**,
Grosh no lleva ninguna de las 13 armaduras del catálogo.

Obsérvese que la condición es `sin_armadura` **y no `sin_escudo`**: el texto del
manual dice expresamente «aunque lleves un escudo», de modo que el +2 de escudo
se sumaría *encima* si lo llevara. **Grosh no lleva escudo**, así que ese +2 no
entra. (El propio fichero anota en un comentario que el Monje sí exige no llevar
escudo — condición distinta que aquí no aplica.)

**Aritmética:**

```
    ca = 10  +  mod. Destreza  +  mod. Constitución   (+ 0 por escudo: no lleva)
       = 10  +  1              +  2
       = 13
```

**Las dos lecturas posibles, y por qué dan lo mismo.** El rasgo dice «tu clase de
armadura **base** es…» (`op: base`), lo que admite dos lecturas:

- **(a) Sustituye** la CA base por defecto sin armadura (`10 + mod. Des`, que el
  encargo me indica dar por buena) → 10 + 1 + 2 = **13**.
- **(b) Es una segunda forma de calcular la CA entre las que hay que elegir**,
  que es como lo plantea
  `reglas/generacion_personaje.yaml → multiclase.clase_de_armadura`: *«Si el
  personaje tiene varias formas de calcular su CA […] solo puede beneficiarse de
  una, a elegir»* → se elige la mayor entre 13 (rasgo) y 11 (`10 + 1` por
  defecto) → **13**.

**Elijo (a)**, porque es la que dice el texto del rasgo, que es la regla
específica; pero lo hago constar porque (b) es la lectura que exigiría un
personaje multiclase y aquí **ambas coinciden en 13**, así que la ambigüedad no
contamina este resultado.

**Modificadores adicionales sobre `ca`: ninguno.** No hay armadura ni escudo
(`equipo/armaduras.yaml` no aporta nada), ni rasgo de especie, trasfondo, dote o
subclase que toque la CA (Paso 1).

> **`ca = 13`**

---

### 3.3 · `velocidad`

**Valor base.** `especies/especies.yaml → especies[Orco].velocidad_m: 9`
(`pagina: {pdf: 197, libro: 195}`). El campo está declarado en metros
(`velocidad_m`), que es la unidad que pide el encargo.

**Modificadores, uno por uno:**

1. **«Movimiento rápido» (Bárbaro) — NO aplica, por nivel.**
   `clases/rasgos/barbaro.yaml → rasgos[Movimiento rápido]`, `nivel: 5`,
   `pagina: {pdf: 54, libro: 52}`: *«Tu velocidad aumenta en 3 m mientras no
   lleves armadura pesada»*
   (`efectos: {objetivo: velocidad, op: add, formula: "3", requiere: [sin_armadura_pesada]}`).

   Merece la pena ser explícito, porque aquí está la trampa: **su condición sí se
   cumple** —Grosh no lleva armadura pesada, ni de ninguna clase— pero **el
   rasgo todavía no se ha obtenido**. `clases/barbaro.yaml → progresion` lo sitúa
   en `{n: 5, … rasgos: ["Ataque adicional", "Movimiento rápido"]}`, y Grosh es
   nivel 1 (`clases[0].nivel: 1`, `nivel_total: 1`). Un rasgo cuya condición se
   cumple pero cuyo nivel no se ha alcanzado **no aporta nada**. → **+0 m.**

   (Ojo también a que la condición de este rasgo es `sin_armadura_pesada`, no
   `sin_armadura`: a nivel 5 el bárbaro conserva el +3 m con armadura ligera o
   media. Irrelevante aquí, pero lo anoto porque distingue este rasgo del del
   Monje.)

2. **Penalización de −3 m por Fuerza mínima de armadura — NO aplica.**
   `equipo/armaduras.yaml → reglas.fuerza`: *«Si la tabla indica una puntuación
   de Fuerza para un tipo de armadura, esta reduce 3 m la velocidad de quien la
   lleve, salvo que su Fuerza sea igual o superior a la indicada.»* Grosh no
   lleva armadura, así que no hay nada que penalizar. (Y aunque la llevara: los
   únicos umbrales de la tabla son Fuerza 13 —Cota de malla— y Fuerza 15
   —Armadura de bandas y de placas—, y su Fuerza es 17, por encima de ambos.)
   → **−0 m.**

3. **Rasgos del Orco — NO aplican.** Ninguno de los tres toca la velocidad.
   «Descarga de adrenalina» permite *correr* (la acción de correr) como acción
   adicional; eso es una acción, no un cambio de la velocidad. → **+0 m.**

4. **Trasfondo, dote, subclase — NO aplican.** Paso 1. → **+0 m.**

5. **Carga / sobrecarga — la base no la declara.** He buscado
   (`capacidad de carga`, `sobrecarga`) en `reglas/` y `equipo/`: lo único que
   sale es la capacidad de carga de los *animales de tiro*
   (`equipo/aventureros.yaml`), nada aplicable a un personaje. No es un hueco
   relevante: la carga es una regla opcional y no interviene en la velocidad
   canónica de una ficha.

**Aritmética:**

```
    velocidad = base de especie  + Movimiento rápido  − penalización de armadura
              = 9 m              + 0 (nivel 1)        − 0 (sin armadura)
              = 9 m
```

> **`velocidad = 9 m`**

---

### 3.4 · `cd_conjuros` y `bonif_ataque_conjuros` — **no proceden**

**Grosh no lanza conjuros.** Cuatro comprobaciones independientes, todas
negativas:

1. **La clase no es lanzadora.** `clases/barbaro.yaml` línea 20:
   `lanzador: ninguno`. Y —esto es lo decisivo para la fórmula— el fichero del
   Bárbaro **no tiene campo `aptitud_magica`**, a diferencia de las ocho clases
   que sí lo traen (`bardo.yaml: Carisma`, `clerigo.yaml: Sabiduría`,
   `mago.yaml: Inteligencia`, etc.). Sin aptitud mágica no hay término que meter
   en la fórmula.
2. **No hay subclase que lo conceda.** Las subclases de bárbaro empiezan en
   nivel 3 (`clases/subclases/barbaro.yaml → niveles_de_subclase: [3, 6, 10, 14]`)
   y la ficha trae `subclase: null`. (El caso «lanzador de subclase» existe en
   esta base —`clases/guerrero.yaml` y `clases/picaro.yaml` lo anotan para
   Caballero arcano y Ladrón arcano—, pero el Bárbaro no lo tiene en ninguna de
   sus cuatro subclases.)
3. **La especie no concede magia.** `especies/especies.yaml → Orco`: sus tres
   rasgos son Aguante incansable, Descarga de adrenalina y Visión en la
   oscuridad. Ninguno da trucos ni aptitud mágica, a diferencia de Aasimar
   («Portador de luz»), Elfo, Gnomo o Tiefling.
4. **La dote no concede magia.** El trasfondo Soldado otorga «Atacante salvaje»
   (`trasfondos.yaml → trasfondos[Soldado].dote`), no «Iniciado en la magia»
   —que es la dote de origen que sí daría trucos y aptitud mágica, y que llevan
   Acólito, Erudito y Guía—.

Como refuerzo, el propio rasgo «Furia» del Bárbaro
(`clases/rasgos/barbaro.yaml`, nivel 1) dice que mientras está enfurecido «no
puedes mantener la concentración ni lanzar conjuros»: la clase está escrita
desde el supuesto de que no lanza.

**Que conste que la fórmula sí existe en la base**, y podría aplicarla si el
personaje lanzara: `reglas/generacion_personaje.yaml → conjuros`
(`pagina: {pdf: 240, libro: 238}`, sección «Tiradas de salvación / Tiradas de
ataque»):

- `cd_salvacion.formula: "8 + modificador de aptitud mágica + bonificador por competencia"`
- `bonificador_ataque.formula: "modificador de aptitud mágica + bonificador por competencia"`

De los dos términos yo tengo el bonificador por competencia (+2, Paso 0), pero
**el modificador de aptitud mágica no existe para este personaje**: no es que
falte el dato en la base, es que la regla no le asigna ninguno. Por tanto los dos
valores no son «desconocidos» ni «0» — son **inaplicables**.

> **`cd_conjuros` = no procede · `bonif_ataque_conjuros` = no procede**

---

## Valores derivados

| Valor | Resultado | Derivación | Regla citada |
|---|---|---|---|
| `pg_max` | **14** | máx(d12) 12 + mod. Con (+2) | `reglas/generacion_personaje.yaml → puntos_golpe.nivel_1` (pdf 42 / libro 40) · dado en `clases/barbaro.yaml → atributos_basicos.dado_golpe` (pdf 53 / libro 51) |
| `ca` | **13** | 10 + mod. Des (+1) + mod. Con (+2); sin armadura ✔, sin escudo | `clases/rasgos/barbaro.yaml → rasgos[Defensa sin armadura]` (pdf 53 / libro 51); condición verificada contra `equipo/armaduras.yaml` (pdf 218 / libro 216) |
| `velocidad` | **9 m** | 9 m de especie, sin modificadores aplicables a nivel 1 | `especies/especies.yaml → especies[Orco].velocidad_m` (pdf 197 / libro 195); «Movimiento rápido» descartado por nivel (`clases/barbaro.yaml → progresion[n:5]`) |
| `cd_conjuros` | **no procede** | el personaje no lanza conjuros: sin aptitud mágica | `clases/barbaro.yaml → lanzador: ninguno` (y ausencia de `aptitud_magica`); fórmula en `reglas/generacion_personaje.yaml → conjuros.cd_salvacion` (pdf 240 / libro 238) |
| `bonif_ataque_conjuros` | **no procede** | ídem | ídem, `conjuros.bonificador_ataque` |

Valores auxiliares derivados por el camino, por si sirven de contraste:

| Auxiliar | Valor | Fuente |
|---|---|---|
| mod. Fuerza | +3 | Fue 17 |
| mod. Destreza | +1 | Des 13 |
| mod. Constitución | +2 | Con 15 |
| mod. Inteligencia | 0 | Int 10 |
| mod. Sabiduría | +1 | Sab 12 |
| mod. Carisma | −1 | Car 8 |
| Bonificador por competencia | +2 | `clases/barbaro.yaml → progresion[n:1].pb` y `reglas/generacion_personaje.yaml → px_por_nivel[nivel:1].pb` (pdf 43 / libro 41) |

---

## Lo que NO se ha podido derivar de la base

**Nada de lo encargado.** Los tres valores aplicables (`pg_max`, `ca`,
`velocidad`) salen enteros de reglas declaradas y citables, y los dos de
conjuros no proceden por una razón declarada en la base, no por un hueco en
ella.

En particular, y a diferencia de lo que informaron calculistas de tandas
anteriores según el propio aviso del encargo, **la fórmula de la CD de conjuros
y del bonificador de ataque de conjuros SÍ está hoy en la base**, en
`reglas/generacion_personaje.yaml → conjuros` con su página (pdf 240 / libro
238). Ese hueco está cerrado; lo dejo escrito como confirmación positiva, no
como hallazgo.

### Dos observaciones menores, ninguna bloqueante

1. **La velocidad base de las especies no trae `pagina` propia por campo.**
   `especies/especies.yaml` declara `velocidad_m: 9` dentro del registro Orco, y
   la página que puedo citar es la del registro entero
   (`pagina: {pdf: 197, libro: 195}`), no la del campo. Para esta derivación es
   suficiente y no genera ninguna ambigüedad: la velocidad de la especie aparece
   en la misma página del manual que el resto de su bloque. Lo anoto sólo para
   que conste el grano de la cita.

2. **La base no declara reglas de carga/sobrecarga para personajes.** Busqué
   `capacidad de carga` y `sobrecarga` en `reglas/` y `equipo/` y sólo hay
   capacidad de carga de animales de tiro (`equipo/aventureros.yaml`). Es una
   regla opcional del manual y no interviene en la velocidad canónica de una
   ficha, así que **no lo cuento como defecto**; lo dejo constar porque busqué
   ahí antes de dar la velocidad por cerrada.

---

*Informe escrito sin ejecutar ningún verificador, sin leer ninguna línea de
Python, sin abrir `reglas/efectos.yaml` y sin ver ningún valor calculado por el
motor para esta ficha ni para ninguna otra.*
