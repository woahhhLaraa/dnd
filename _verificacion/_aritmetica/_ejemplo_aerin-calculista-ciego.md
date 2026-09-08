# Derivación a mano — `_ejemplo_aerin` (Aerin Vellamora)

**Agente E · «el calculista» — `PLAN_ESTRES.md`**
Fecha: 2026-09-08

---

## Cabecera

### Ficha

| Campo | Valor (de los datos crudos) |
|---|---|
| Nombre | Aerin Vellamora (prueba nivel 1) |
| Especie | Elfo (`especies/especies.yaml#Elfo`), `rasgos_elegidos: {}` |
| Clase | Brujo nivel 1, sin subclase |
| Nivel total | 1 |
| Trasfondo | Noble (`trasfondos/trasfondos.yaml#Noble`) |
| Dote | Habilidoso (de origen, por trasfondo) |
| Características finales | Fue 9 · Des 15 · Con 13 · Int 12 · Sab 10 · Car 16 |
| Armadura equipada | Armadura de cuero (`equipo/armaduras.yaml`), **sin escudo** |

### Método

Transcripción independiente. Cada número de este informe se ha derivado leyendo
**el texto de la regla** en los ficheros de la base y haciendo la aritmética a
mano, sin ejecutar nada y sin ver ningún valor calculado por el motor del
proyecto. La entrada ha sido exclusivamente la copia **cruda** de la ficha
(sin bloque `calculado`):

    /tmp/claude-0/-home-user-dnd/ccce6f54-5659-5d7c-89a3-15e0f610e8cf/scratchpad/crudos/_ejemplo_aerin.yaml

Aerin es el **único Brujo del repositorio** y ninguna ficha de Brujo tenía
lectura independiente hasta hoy. El Brujo usa el sistema de **pacto**
(`lanzador: pacto`), con reglas de espacios propias; el apartado 3.4 examina
expresamente si eso cambia la forma de calcular la CD y el bonificador de
ataque de conjuros respecto de las demás clases lanzadoras.

### Ficheros consultados

| Fichero | Para qué |
|---|---|
| `clases/brujo.yaml` | dado de golpe, `lanzador: pacto`, `aptitud_magica`, progresión (`pb`, `trucos`, `prep`, `espacios`), competencias de armadura |
| `clases/rasgos/brujo.yaml` | texto en prosa de «Invocaciones sobrenaturales» y «Magia del pacto», y de los rasgos de nivel > 1 que hubo que descartar |
| `clases/subclases/brujo.yaml` | comprobar que las subclases empiezan en nivel 3 (`niveles_de_subclase`) y que ninguna toca los cinco valores |
| `clases/_ESQUEMA_atributos_basicos.md` | confirmar la forma del campo `dado_golpe` (`d8` = «1d8 por nivel», sin el 1) |
| `clases/*.yaml` (solo las líneas `lanzador:` / `aptitud_magica:`) | situar `pacto` frente a `completo`, `medio` y `ninguno` |
| `especies/especies.yaml` | velocidad base y rasgos del Elfo; sus tres linajes; contraste con los dos únicos `efectos:` del fichero (Enano y Goliat) |
| `trasfondos/trasfondos.yaml` | Noble: características ajustables, dote, habilidades, equipo; y `reparto_caracteristicas` |
| `dotes/origen.yaml` | texto de «Habilidoso» (y contraste con «Duro», que sí toca `pg_max`) |
| `reglas/generacion_personaje.yaml` | tabla de modificadores, regla de PG de nivel 1, **fórmulas de CD y ataque de conjuros**, `px_por_nivel`, reglas de multiclase |
| `reglas/caracteristicas.yaml` | emparejamiento nombre ↔ abreviatura (`Carisma` ↔ `car`) |
| `reglas/fuentes_de_efectos.yaml` | qué ficheros de la base **pueden** conceder efectos, para cerrar el inventario |
| `equipo/armaduras.yaml` | catálogo completo; fórmula de CA de la Armadura de cuero; reglas de entrenamiento, Fuerza mínima y sigilo |
| `equipo/armas.yaml` | comprobar que la Daga es arma y no armadura |
| `equipo/aventureros.yaml` | contenido de «Canalizador arcano», «Libro» y «Paquete de erudito» |
| `_verificacion/_aritmetica/orco_barbaro-calculista-ciego.md` | **solo como modelo de formato**, indicado expresamente por el encargo; es de otro personaje (Bárbaro) y no comparte ningún número con este |

### Desviaciones cometidas — declaración honesta

**No he abierto ningún fichero prohibido de código.** Ni `calculo.py`, ni
`efectos.py`, ni ningún `validar*.py` / `verificar*.py`. No he abierto
`personajes/` (ni la ficha original de Aerin, ni ninguna otra). No he ejecutado
ningún verificador, ni `--calcular`, ni nada que devuelva un número ya
calculado.

Declaro cinco matices, ninguno de los cuales me ha mostrado un valor calculado
de esta ficha:

1. **Una línea de `reglas/efectos.yaml`, fichero prohibido, vista por
   accidente.** Al hacer un `grep` de `ca:` sobre los directorios permitidos
   para asegurarme de que ninguna otra fuente concede CA, el patrón encajó
   también en `reglas/efectos.yaml` y la salida me mostró **una sola línea**:
   `reglas/efectos.yaml:49:  ca:`. Es el nombre de una clave y su número de
   línea; **no vi ninguna fórmula, ningún valor ni ningún contexto**. Lo declaro
   igualmente porque la honestidad sobre la desviación vale más que una
   derivación aparentemente limpia. No ha influido en ningún paso: la CA de este
   personaje sale de `equipo/armaduras.yaml`, no de ahí.

2. **`_verificacion/_aritmetica/orco_barbaro-calculista-ciego.md`.** El encargo
   me manda expresamente leerlo como modelo de formato. Es de **otro
   personaje** (Grosh, Orco Bárbaro 1) y sus cinco valores (14 / 13 / 9 /
   no_procede / no_procede) no comparten derivación con los míos. La única
   coincidencia numérica —velocidad 9— sale de que ambas especies declaran
   `velocidad_m: 9` en el mismo fichero, cada una en su registro. **Ese informe
   tampoco es un valor del motor**: es otra derivación a mano.

3. **Bloques `efectos:` dentro de ficheros de la base permitidos.** He derivado
   **siempre desde el `desc` en prosa** y solo después he mirado el `efectos:`
   como confirmación. En el caso de Aerin la cuestión resulta ser vacua, y es un
   dato en sí: `clases/rasgos/brujo.yaml` tiene **cero** bloques `efectos:` y
   `clases/subclases/brujo.yaml` también **cero**; los únicos de
   `especies/especies.yaml` son los del Enano y el Goliat (ninguno es Elfo), y
   el único de `dotes/origen.yaml` es el de «Duro» (Aerin lleva «Habilidoso»).
   `trasfondos/trasfondos.yaml` no tiene ninguno. **No hay ni un solo bloque
   formalizado que aplique a este personaje**, así que las cinco derivaciones
   son al 100 % lectura de prosa y de tablas.

4. **`reglas/fuentes_de_efectos.yaml`.** Está en `reglas/` y no es
   `efectos.yaml`, luego es lectura permitida, y el encargo la pide
   expresamente. La he usado solo para cerrar el inventario del Paso 1. Sus
   comentarios hablan del motor y de fallos históricos del proyecto, pero no
   contienen ningún número de esta ficha.

5. **Listado de la raíz del proyecto** (`ls /home/user/dnd/`): he visto los
   *nombres* de los ficheros de código y de los planes, no su contenido.

**Hallazgo previo ya conocido, no lo cuento como nuevo:** la CA por defecto sin
armadura (`10 + mod. Destreza`) vive en `reglas/efectos.yaml`, que este encargo
me prohíbe. Aerin **lleva armadura**, así que esa fórmula no gobierna su CA;
solo aparece en el apartado 3.2 como término de comparación, y la doy por buena
tal como el encargo indica.

---

## Paso 0 — Modificadores de característica

Los cinco valores dependen de los modificadores, así que los derivo primero.

**Regla.** `reglas/generacion_personaje.yaml → metodos_generacion_caracteristicas.modificadores_por_puntuacion`
(fuente del bloque: `pagina_pdf: 40`, `libro: 38`, cap. 2, «Paso 3: determinar
las puntuaciones de característica»):

> `formula: "(puntuación - 10) / 2, redondeando hacia abajo"`

El mismo bloque trae una `tabla:` explícita que uso como segunda comprobación.

**Qué puntuaciones uso: las finales.** El mismo fichero, en
`metodos_generacion_caracteristicas.ajuste_por_trasfondo`, dice que el ajuste
del trasfondo se aplica *«Tras asignar las puntuaciones»*; por tanto los
modificadores se derivan del bloque `caracteristicas.final` de la ficha, no del
`base`. Comprobación de coherencia de esa suma:

- `base` = Fue 8 / Des 15 / Con 13 / Int 12 / Sab 10 / Car 14. El método
  declarado es `conjunto_estandar`, y
  `reglas/generacion_personaje.yaml → metodos_generacion_caracteristicas.conjunto_estandar.puntuaciones`
  es `[15, 14, 13, 12, 10, 8]`. El multiconjunto de la ficha
  {8, 15, 13, 12, 10, 14} **es exactamente ese**. ✔
  *(Observación, no defecto: la fila recomendada para Brujo en
  `conjunto_estandar_por_clase.filas` es `{fue: 8, des: 14, con: 13, int: 12,
  sab: 10, car: 15}`, o sea con Des y Car intercambiados respecto de la ficha.
  Esa tabla se describe como «Cómo repartir 15/14/13/12/10/8 según la clase»
  —una recomendación—, no como una restricción, y el conjunto estándar no
  obliga a un reparto concreto. Anoto abajo que la elección de la ficha no
  cambia ningún modificador: 14+2 = 16 y 15+2 = 17 dan **ambos +3**.)*
- `ajuste_trasfondo` = +2 Car, +1 Fue. El trasfondo Noble permite ajustar
  `[Fuerza, Inteligencia, Carisma]`
  (`trasfondos/trasfondos.yaml → trasfondos[Noble].caracteristicas`, pdf 186 /
  libro 184), y el reparto legal es *«+2 a una y +1 a otra, o +1 a cada una de
  las tres»* (`trasfondos.yaml → reparto_caracteristicas`). +2 Car / +1 Fue
  encaja: ambas están en la terna y son distintas. Ningún valor pasa de 20.
- `final` = 8+1 = **9** Fue; 15 Des; 13 Con; 12 Int; 10 Sab; 14+2 = **16** Car. ✔

**Derivación de cada modificador:**

| Característica | Puntuación final | `(p − 10) / 2` redondeado abajo | Fila de la tabla | Modificador |
|---|---|---|---|---|
| Fuerza | 9 | (9−10)/2 = −0,5 → **−1** | `"8-9": -1` | **−1** |
| Destreza | 15 | (15−10)/2 = 2,5 → 2 | `"14-15": 2` | **+2** |
| Constitución | 13 | (13−10)/2 = 1,5 → 1 | `"12-13": 1` | **+1** |
| Inteligencia | 12 | (12−10)/2 = 1 | `"12-13": 1` | **+1** |
| Sabiduría | 10 | (10−10)/2 = 0 | `"10-11": 0` | **0** |
| Carisma | 16 | (16−10)/2 = 3 | `"16-17": 3` | **+3** |

Los dos caminos (fórmula y tabla) coinciden en las seis. Atención al redondeo de
Fuerza: «redondeando hacia abajo» sobre −0,5 da **−1**, no 0; la tabla lo
confirma con la fila `"8-9": -1`. (No interviene en ninguno de mis cinco
valores, pero lo dejo derivado por completitud del Paso 0.)

El emparejamiento «Carisma» ↔ `car` (necesario para leer el bloque
`caracteristicas.final` de la ficha) lo declara
`reglas/caracteristicas.yaml → caracteristicas[5]`:
`{nombre: "Carisma", abrev: "car", variable: "mod_car"}`.

**Bonificador por competencia (dato auxiliar, y esta vez sí entra en dos de los
cinco valores).** Nivel 1 → **+2**, por dos fuentes que coinciden:
`clases/brujo.yaml → progresion[n:1].pb = 2` y
`reglas/generacion_personaje.yaml → px_por_nivel.filas[nivel:1].pb = 2`
(tabla «Progreso de los personajes», pdf 43 / libro 41). El personaje es de una
sola clase, así que la regla `multiclase.bonificador_por_competencia` («se basa
en el nivel TOTAL») no cambia nada: nivel de clase = nivel total = 1.

---

## Paso 1 — Inventario CERRADO de fuentes de efectos

Antes de calcular nada, cierro la lista de sitios de donde puede salir un
modificador, para poder afirmar con fundamento que no me dejo ninguno.
`reglas/fuentes_de_efectos.yaml → fuentes` declara cinco patrones que pueden
llevar bloques `efectos:` —`especies/especies.yaml`, `clases/rasgos/*.yaml`,
`clases/subclases/*.yaml`, `dotes/*.yaml` y `trasfondos/*.yaml`— y
`→ derivadas` añade una sexta, `equipo/armaduras.yaml`, cuyos efectos no se
escriben sino que se **derivan de sus campos `ca` y `fuerza`**. Su bloque
`excluidos` declara uno a uno, con motivo, los demás ficheros de regla
(incluido `clases/brujo.yaml`, «tabla de progresión y atributos básicos; sus
números son columnas […], no efectos»), de modo que la lista de seis es
exhaustiva.

Repaso las seis para esta ficha:

| Fuente | Qué le aplica a Aerin | ¿Modifica `pg_max`, `ca`, `velocidad`, `cd_conjuros` o `bonif_ataque_conjuros`? |
|---|---|---|
| `especies/especies.yaml → Elfo` (pdf 191 / libro 189) | Linaje élfico · Linaje feérico · Sentidos agudos · Trance · Visión en la oscuridad 18 m | **Aporta la velocidad base (9 m) y nada más.** Ninguno de los cinco rasgos lleva bloque `efectos:` — los dos únicos del fichero son el «Aguante enano» del Enano (línea 67) y la «Forma grande» del Goliat (líneas 94-97). «Linaje feérico» es ventaja en TdS; «Sentidos agudos», una competencia; «Trance», descanso; «Visión en la oscuridad», sentido. **«Linaje élfico» merece examen aparte: ver Paso 2.** |
| `clases/rasgos/brujo.yaml`, rasgos de nivel 1 | Invocaciones sobrenaturales · Magia del pacto | **Uno, y solo para conjuros:** «Magia del pacto» declara la aptitud mágica (ver 3.4). Ninguno toca `pg_max`, `ca` ni `velocidad`. |
| `clases/rasgos/brujo.yaml`, rasgos de nivel > 1 | Astucia mágica (2), Contactar patrón (9), los cuatro Arcanum místico (11/13/15/17), Don épico (19), Maestro sobrenatural (20) | **No aplica: el personaje es nivel 1.** Y, leídos uno a uno, ninguno tocaría los cinco valores ni aun teniéndolos: todos hablan de recuperar o lanzar conjuros. **En particular, «Maestro sobrenatural» (nivel 20) NO sube ninguna puntuación de característica** —solo hace que Astucia mágica recupere todos los espacios en vez de la mitad—, así que la trampa de nivel 20 que el encargo menciona para otras dos clases **no existe en el Brujo**. Lo compruebo explícitamente porque era justo lo que se buscaba. |
| `clases/subclases/brujo.yaml` | ninguno | `niveles_de_subclase: [3, 6, 10, 14]` y la ficha trae `subclase: null` a nivel 1. Además el fichero no contiene **ningún** bloque `efectos:`. |
| `dotes/origen.yaml → Habilidoso` (pdf 203 / libro 201) | *«Ganas competencia en cualquier combinación de tres habilidades o herramientas que elijas.»* | **No.** Solo competencias. No lleva bloque `efectos:`; el único del fichero (línea 35) es el de «Duro», que Aerin **no** tiene. |
| `trasfondos/trasfondos.yaml → Noble` (pdf 186 / libro 184) | características, dote, habilidades, herramienta, equipo | **Solo vía características** (ya incorporadas en el Paso 0). El registro no lleva `efectos:`, y su propio campo `no_automatizado` dice que lo que concede son campos estructurados, «no prosa con mecánica escondida». |
| `equipo/armaduras.yaml` (derivada) | **Armadura de cuero**, ligera | **Sí: gobierna la `ca`.** Ver Paso 3 y 3.2. Su campo `fuerza` es `null`, luego no toca la velocidad. |

Fuera de esas seis, nada más puede conceder efectos. Las tres piezas de equipo
restantes de Aerin viven en ficheros que `fuentes_de_efectos.yaml → excluidos`
declara sin efectos por motivo escrito: `equipo/armas.yaml` (la Daga) y
`equipo/aventureros.yaml` (Canalizador arcano, Libro, Paquete de erudito).

---

## Paso 2 — Dos condiciones que hay que comprobar aparte

### 2.1 · El linaje élfico no está elegido — y es lo único que podría mover la velocidad

`especies/especies.yaml → Elfo`, rasgo **«Linaje élfico»** (pdf 191 / libro 189):

> «Elige un linaje. Obtienes su beneficio de nivel 1 y aprendes un conjuro a los
> niveles 3 y 5, siempre preparado, lanzable 1 vez sin gastar espacio por
> descanso largo. Inteligencia, Sabiduría o Carisma es tu aptitud mágica (elige
> al seleccionar el linaje).»

Los tres linajes y su beneficio de nivel 1, del mismo registro:

| Linaje | `nivel_1` | ¿Toca alguno de mis cinco valores? |
|---|---|---|
| Alto elfo | «Truco prestidigitación (sustituible por otro truco de mago tras descanso largo)» | No |
| Drow | «Visión en la oscuridad aumenta a 36 m; truco luces danzantes» | No |
| **Elfo de los bosques** | **«Velocidad aumenta a 10,5 m**; truco saber druídico» | **Sí: `velocidad`** |

**La ficha trae `especie.rasgos_elegidos: {}`, vacío.** No hay linaje elegido.
Por tanto **no se aplica ningún beneficio de linaje**, y en particular no se
aplica el «Velocidad aumenta a 10,5 m» del Elfo de los bosques. La velocidad se
queda en la base de la especie.

Lo hago constar como **la única bifurcación real de esta derivación** (ver
apartado 3.3 y la sección final «Lo que NO se ha podido derivar»): si algún día
esa ficha declara `Elfo de los bosques`, su velocidad pasa a **10,5** y este
informe deja de valer para ese campo. Con los datos crudos tal como están, el
número es 9.

*Nota lateral que apunta en la misma dirección:* la ficha lleva
`Prestidigitación` entre sus trucos, que es a la vez uno de los dos trucos
recomendados al Brujo por «Magia del pacto» **y** el beneficio de nivel 1 del
Alto elfo. Como los trucos de la ficha son exactamente 2 —«Descarga
sobrenatural» y «Prestidigitación»— y `clases/brujo.yaml → progresion[n:1].trucos`
concede precisamente 2, los dos se explican enteros por la clase y no queda
ninguno atribuible a un linaje. Es coherente con que no haya linaje elegido.

### 2.2 · Sí lleva armadura: qué armadura y si tiene entrenamiento

Es la condición que gobierna la CA, así que la compruebo a conciencia. **El
catálogo completo** de `equipo/armaduras.yaml` (pdf 218 / libro 216) son 13
entradas: 3 ligeras (Armadura acolchada, Armadura de cuero, Armadura de cuero
tachonado), 5 medias, 4 pesadas y el Escudo.

**El equipo de Aerin**, uno por uno:

| Objeto de la ficha | Fichero de la base | ¿Es armadura o escudo? |
|---|---|---|
| **Armadura de cuero** | `equipo/armaduras.yaml → armaduras_ligeras` | **Sí, armadura ligera.** `ca: "11 + mod. Des"`, `fuerza: null`, `sigilo: null`, 5 kg, 10 po |
| Daga | `equipo/armas.yaml` (1d4 perforante, arrojadiza/ligera/sutil) | No, arma |
| Canalizador arcano (orbe) | `equipo/aventureros.yaml` | No. Su descripción: «Objeto de la tabla "Canalizadores arcanos", ornamentado para canalizar magia arcana. Brujos, hechiceros o magos pueden usarlo como canalizador mágico.» Sin campo `ca` |
| Libro (de conocimiento oculto) | `equipo/aventureros.yaml` | No, objeto (2,5 kg, 25 po) |
| Paquete de erudito | `equipo/aventureros.yaml` | No. Contenido declarado: «10 frascos de aceite, 10 hojas de pergamino, lámpara, libro, mochila, pluma, tinta y yesquero». Ninguna armadura dentro |

**Conclusiones:**

- **Lleva exactamente una armadura y ningún escudo.** La regla
  `equipo/armaduras.yaml → reglas.solo_un_tipo` («no más de una armadura ni más
  de un escudo a la vez») se cumple trivialmente.
- **Tiene entrenamiento con ella.** `clases/brujo.yaml → atributos_basicos.armaduras: ["Armaduras ligeras"]`,
  y la ficha lo registra en `competencias.armaduras`. Luego no entra
  `reglas.sin_entrenamiento` (que además impone desventaja y prohibición de
  lanzar conjuros, pero **no** cambiaría la CA).
- **No hay `+2` de escudo.** No lo lleva, y de llevarlo tampoco lo obtendría:
  `reglas.escudos` exige entrenamiento con escudos, que el Brujo no tiene.

---

## Paso 3 — Los cinco valores

### 3.1 · `pg_max` — puntos de golpe máximos

**Regla aplicable.** `reglas/generacion_personaje.yaml → puntos_golpe.nivel_1`
(`pagina: {pdf: 42, libro: 40}`):

> `regla: "Máximo del dado de golpe + modificador por Constitución."`

Uso esta y no `puntos_golpe.niveles_siguientes_al_1` (pdf 44 / libro 42) porque
el personaje es de nivel 1 y no ha subido ningún nivel: no hay ningún dado que
tirar, ni «valor establecido» que aplicar (para el Brujo sería 5, fila
`{clases: [Bardo, Brujo, Clérigo, Druida, Monje, Pícaro], valor: 5}`). El propio
fichero avisa de que son «dos reglas distintas, en dos sitios».

Tampoco entra `puntos_golpe.aumento_de_constitucion` (pdf 44 / libro 42): no ha
habido ningún aumento del modificador por Constitución posterior a la creación.

**Dado de golpe.** `clases/brujo.yaml → atributos_basicos.dado_golpe: d8`
(bloque `atributos_basicos.fuente: {pagina_pdf: 71, pagina_libro: 69}`).
Según `clases/_ESQUEMA_atributos_basicos.md` (regla 2), la forma `d8` significa
«1d8 por nivel», sin el 1 delante. **Máximo de un d8 = 8.**

**Modificador por Constitución.** Del Paso 0: Con 13 → **+1**.

**Aritmética:**

```
    pg_max = máximo del dado de golpe  +  mod. Constitución
           = 8                         +  1
           = 9
```

**Modificadores adicionales sobre `pg_max`: ninguno.** Del inventario del
Paso 1: el Elfo no tiene «Aguante enano» (ese es del Enano,
`especies.yaml` línea 67, `pg_max op:add "nivel_total"`), y la dote de Aerin es
«Habilidoso», no «Duro» (esa sí lleva `pg_max op:add "2 * nivel_total"`,
`dotes/origen.yaml` línea 35). Ningún rasgo de Brujo de nivel 1 toca los PG, ni
lo haría ninguno de nivel superior. El Brujo tampoco tiene un análogo del
«Aguante» de otras clases.

*(Que conste el contraste con los PG temporales, que no son PG máximos: ningún
rasgo de Aerin concede siquiera de esos a nivel 1; el que existe en la clase,
«Resiliencia celestial», es de la subclase Patrón Celestial a nivel 10.)*

> **`pg_max = 9`**

---

### 3.2 · `ca` — clase de armadura

**Regla aplicable.** `equipo/armaduras.yaml → armaduras_ligeras.tabla`
(`fuente: {pagina_pdf: 218, libro: 216}`), registro **Armadura de cuero**:

> `{nombre: "Armadura de cuero", ca: "11 + mod. Des", fuerza: null, sigilo: null, peso_kg: 5, precio: "10 po"}`

La CA es una **fórmula escrita en el propio campo `ca`** de la tabla; no hay
prosa aparte que derivar, porque este fichero declara su `fidelidad:
"estructurado"` («tabla de datos: CA, fuerza mínima, sigilo, peso, precio»).
Tampoco hay bloque `efectos:` que pudiera contaminar la lectura: como declara
`reglas/fuentes_de_efectos.yaml → derivadas`, los efectos de este fichero **se
derivan del campo `ca`**, y escribir un `efectos:` al lado sería duplicar el
dato. Aquí, pues, la fórmula del campo *es* el texto de la regla.

**Sin tope de Destreza.** Es una diferencia que conviene comprobar y no dar por
supuesta: las cinco armaduras **medias** del catálogo escriben su fórmula como
`"NN + mod. Des (máx. 2)"`, y las cuatro **pesadas** dan un número pelado sin
término de Destreza. Las tres **ligeras** —la de Aerin entre ellas— escriben
`"11 + mod. Des"` / `"12 + mod. Des"` sin tope alguno. Su mod. Des es +2, que
ni siquiera alcanzaría el tope de las medias, pero la ausencia de tope queda
comprobada y no supuesta.

**Condiciones.** Del Paso 2.2: lleva la armadura, tiene entrenamiento con
armaduras ligeras, y no lleva escudo.

**Aritmética:**

```
    ca = 11 (base de la Armadura de cuero)  +  mod. Destreza   (+ 0 por escudo: no lleva)
       = 11                                 +  2
       = 13
```

**Sobre la regla de «varias formas de calcular la CA».**
`reglas/generacion_personaje.yaml → multiclase.clase_de_armadura` dice: *«Si el
personaje tiene varias formas de calcular su CA […] solo puede beneficiarse de
una, a elegir.»* Aerin tiene dos candidatas:

- **(a) Armadura de cuero:** 11 + mod. Des (+2) = **13**.
- **(b) CA por defecto sin armadura,** `10 + mod. Destreza` = 10 + 2 = **12**.
  (Esa fórmula por defecto vive en `reglas/efectos.yaml`, que el encargo me
  prohíbe abrir; la doy por buena tal como el encargo indica, y solo la uso como
  término de comparación.)

Se elige la mayor: **13**. Y la elección es además la natural, porque la (b)
solo se aplica *sin* armadura y Aerin lleva una. Las dos vías coinciden en 13,
así que la ambigüedad no contamina el resultado.

**El Brujo no tiene rasgo de CA.** Lo compruebo explícitamente porque es el
lugar donde otras clases meten una tercera fórmula: `clases/rasgos/brujo.yaml`
tiene diez rasgos y **ninguno** es una «Defensa sin armadura» ni equivalente;
tampoco hay nada así en las cuatro subclases (`clases/subclases/brujo.yaml`), y
de todas formas empiezan en nivel 3. Ni la especie, ni el trasfondo, ni la dote
tocan la CA (Paso 1).

> **`ca = 13`**

---

### 3.3 · `velocidad`

**Valor base.** `especies/especies.yaml → especies[Elfo].velocidad_m: 9`
(`pagina: {pdf: 191, libro: 189}`). El campo está declarado en metros
(`velocidad_m`), que es la unidad que pide el encargo.

**Modificadores, uno por uno:**

1. **«Elfo de los bosques» (linaje élfico) — NO aplica, por falta de elección.**
   Es el único modificador de velocidad al alcance de este personaje:
   `especies.yaml → Elfo.linajes[Elfo de los bosques].nivel_1` =
   «Velocidad aumenta a 10,5 m». Pero la ficha trae `rasgos_elegidos: {}`
   (Paso 2.1): **no hay linaje elegido**, luego no hay beneficio de linaje que
   aplicar. Obsérvese además que el texto dice «aumenta **a** 10,5 m», no
   «aumenta **en**»: sería una sustitución del valor, no una suma — irrelevante
   aquí, pero lo anoto porque distingue esta redacción de la del Goliat
   («aumenta **en** 3 m»). → **9 m se mantiene.**

2. **Penalización de −3 m por Fuerza mínima de armadura — NO aplica.**
   `equipo/armaduras.yaml → reglas.fuerza`: *«Si la tabla indica una puntuación
   de Fuerza para un tipo de armadura, esta reduce 3 m la velocidad de quien la
   lleve, salvo que su Fuerza sea igual o superior a la indicada.»* La Armadura
   de cuero declara **`fuerza: null`**: la tabla no indica ninguna puntuación
   para ella, luego no hay nada que penalizar. Merece un segundo de atención
   porque la Fuerza de Aerin es 9, muy baja, y esta es la trampa evidente: los
   **únicos** umbrales de todo el catálogo son Fuerza 13 (Cota de malla) y
   Fuerza 15 (Armadura de bandas y de placas), las tres **pesadas**, y ninguna
   armadura ligera ni media tiene umbral. Su armadura no está entre ellas.
   → **−0 m.**

3. **Rasgos de clase — NO aplican.** El Brujo no tiene ningún rasgo de
   velocidad en toda su progresión (`clases/rasgos/brujo.yaml`, los diez
   rasgos), ni a nivel 1 ni a ningún otro. No hay aquí un equivalente del
   «Movimiento rápido» del Bárbaro o del Monje.

4. **Trasfondo, dote, subclase, resto de rasgos de especie — NO aplican.**
   Paso 1. En particular ninguno de los otros cuatro rasgos del Elfo toca la
   velocidad. → **+0 m.**

5. **Carga / sobrecarga — la base no la declara.** Busqué en `reglas/` y
   `equipo/`: lo único que hay es la capacidad de carga de vehículos y animales
   de tiro (`equipo/aventureros.yaml`), nada aplicable a un personaje. Es una
   regla opcional del manual y no interviene en la velocidad canónica de una
   ficha; no lo cuento como defecto, pero dejo constancia de que miré ahí antes
   de cerrar el número. (El rasgo «Constitución poderosa» del Goliat sí menciona
   la capacidad de carga, lo que confirma que el concepto existe en el juego
   aunque su regla no esté transcrita.)

**Aritmética:**

```
    velocidad = base de especie  + linaje élfico     − penalización de armadura
              = 9 m              + 0 (sin elegir)    − 0 (cuero: fuerza null)
              = 9 m
```

> **`velocidad = 9 m`** — con la salvedad declarada del linaje sin elegir.

---

### 3.4 · `cd_conjuros` y `bonif_ataque_conjuros` — **sí proceden**

Este es el apartado que el encargo señalaba: hay que mirar con cuidado si
`lanzador: pacto` y la aptitud mágica del Brujo funcionan como los de las demás
clases o no.

**Aerin sí lanza conjuros.** Cuatro comprobaciones independientes, todas
positivas:

1. **La clase es lanzadora.** `clases/brujo.yaml` línea 20:
   `lanzador: pacto`, con el comentario «sistema propio: espacios todos del
   mismo nivel». Y línea 21: **`aptitud_magica: Carisma`**.
2. **El rasgo existe y es de nivel 1.**
   `clases/brujo.yaml → progresion[n:1].rasgos` incluye **«Magia del pacto»**
   (junto a «Invocaciones sobrenaturales»), y
   `clases/rasgos/brujo.yaml → rasgos[Magia del pacto]` lo declara `nivel: 1`,
   `pagina: {pdf: 71, libro: 69}`. Su `desc` en prosa termina diciendo, literal:

   > «**Aptitud mágica: Carisma.** Canalizador mágico: un canalizador arcano.»

   *(Derivo desde este `desc` en prosa; el campo `aptitud_magica: Carisma` de
   `clases/brujo.yaml` es la segunda fuente que lo confirma, y coincide. No hay
   bloque `efectos:` en este rasgo — ni en ninguno del fichero — así que no hay
   fórmula formalizada de la que estuviera copiando.)*
3. **La ficha ejerce el rasgo.** Trae 2 trucos («Descarga sobrenatural»,
   «Prestidigitación») y 2 conjuros preparados de nivel 1 («Hechizar persona»,
   «Maleficio»), que es exactamente lo que concede
   `clases/brujo.yaml → progresion[n:1]`: `trucos: 2`, `prep: 2`. Y coincide con
   la prosa de «Magia del pacto», que recomienda esos cuatro por su nombre.
4. **No hace falta buscar la magia en otro sitio.** La especie podría aportarla
   («Linaje élfico» concede aptitud mágica a elegir entre Int/Sab/Car), pero el
   linaje no está elegido (Paso 2.1); y la dote es «Habilidoso», no «Iniciado en
   la magia». No importa: la clase ya la da, y es una sola clase, así que no hay
   que decidir entre aptitudes.

**Ahora la pregunta del encargo: ¿el sistema de pacto cambia la fórmula?**

La forma de `lanzador` en la base tiene cuatro valores, que he contrastado
leyendo esa línea en las doce clases:

| `lanzador` | Clases | `aptitud_magica` |
|---|---|---|
| `completo` | Bardo, Clérigo, Druida, Hechicero, Mago | sí (Car / Sab / Sab / Car / Int) |
| `medio` | Explorador («solo hasta espacios de nivel 5»), Paladín | sí (Sab / Car) |
| **`pacto`** | **Brujo** | **sí (Carisma)** |
| `ninguno` | Bárbaro, Guerrero, Monje, Pícaro | **no** (el campo no existe) |

Lo decisivo es la última columna: **`pacto` está del mismo lado de la raya que
`completo` y `medio`** —tiene `aptitud_magica`— y del lado opuesto a `ninguno`.

Y la fórmula no consulta `lanzador` en ningún punto.
`reglas/generacion_personaje.yaml → conjuros` (`pagina: {pdf: 240, libro: 238}`,
sección «Tiradas de salvación / Tiradas de ataque»):

- `cd_salvacion.formula: "8 + modificador de aptitud mágica + bonificador por competencia"` (`base: 8`)
- `bonificador_ataque.formula: "modificador de aptitud mágica + bonificador por competencia"` (`base: 0`)
- `_nota_aptitud`: *«La aptitud mágica de cada clase la declara su propio
  fichero, en `clases/<clase>.yaml → aptitud_magica`. Aquí solo vive la fórmula
  que la combina con el bonificador por competencia.»*

Los dos términos son **el modificador de aptitud mágica** y **el bonificador por
competencia**. Ni uno ni otro depende del tipo de lanzador. La `_nota_aptitud`
lo dice de forma explícita: el único dato que la fórmula toma de la clase es
`aptitud_magica`, y el Brujo lo tiene.

**Qué es, entonces, lo que el pacto sí cambia.** Leyendo la prosa de «Magia del
pacto» (`clases/rasgos/brujo.yaml`, pdf 71 / libro 69), lo propio del sistema
son **los espacios**, y solo ellos:

> «Espacios de conjuro: los de la columna "Espacios de conjuro" de la tabla
> Rasgos de brujo (1 en nivel 1, hasta 4 en nivel 17+), **todos del mismo nivel**
> indicado en la columna "Nivel de los espacios" (sube hasta nivel 5 en nivel
> 9+); **se recuperan tras un descanso corto o largo**.»

Es decir: cuántos espacios hay, de qué nivel son todos ellos, y cada cuánto se
recuperan. Nada de eso entra en la CD ni en el bonificador de ataque. Lo
confirma, desde el otro extremo del manual, la regla de multiclase
`reglas/generacion_personaje.yaml → multiclase.lanzamiento_de_conjuros_multiclase.magia_del_pacto`,
que trata la Magia del pacto como un **depósito de espacios paralelo** que se
combina con los espacios normales, sin decir una palabra de CD ni de ataque —
y que `calculo_nivel_para_tabla`, la regla que sí trocea a los lanzadores por
tipo (completo / mitad / un tercio), **ni siquiera menciona al brujo**, porque
sus espacios no van a esa tabla. La distinción `pacto` vive entera en el terreno
de los espacios.

*(Aerin es de una sola clase, así que ninguna regla de multiclase se le aplica;
las cito solo como evidencia de dónde la base sitúa la diferencia del pacto.)*

**Aritmética.** Aptitud mágica = Carisma → mod. Car = **+3** (Paso 0).
Bonificador por competencia a nivel 1 = **+2** (Paso 0).

```
    cd_conjuros           = 8  +  mod. aptitud mágica (Carisma)  +  bonif. competencia
                          = 8  +  3                              +  2
                          = 13

    bonif_ataque_conjuros =      mod. aptitud mágica (Carisma)   +  bonif. competencia
                          =      3                               +  2
                          = 5
```

**Comprobación de sentido.** La diferencia entre ambos es exactamente 8, que es
la `base:` declarada de la CD; y el truco «Descarga sobrenatural» que la ficha
lleva es precisamente un ataque de conjuro, de modo que el segundo valor no es
ocioso para este personaje. Además, ningún rasgo del Brujo de nivel 1 modifica
la CD ni el ataque de conjuros (las que llevan CD propias en esta clase son
capacidades de subclase, y empiezan en nivel 3).

> **`cd_conjuros = 13` · `bonif_ataque_conjuros = 5`**

---

## Valores derivados

| Valor | Resultado | Derivación | Regla citada |
|---|---|---|---|
| `pg_max` | **9** | máx(d8) 8 + mod. Con (+1) | `reglas/generacion_personaje.yaml → puntos_golpe.nivel_1` (pdf 42 / libro 40) · dado en `clases/brujo.yaml → atributos_basicos.dado_golpe` (pdf 71 / libro 69) |
| `ca` | **13** | 11 (Armadura de cuero) + mod. Des (+2); sin tope de Des, con entrenamiento ✔, sin escudo | `equipo/armaduras.yaml → armaduras_ligeras[Armadura de cuero].ca` (pdf 218 / libro 216); entrenamiento por `clases/brujo.yaml → atributos_basicos.armaduras` |
| `velocidad` | **9 m** | 9 m de especie; linaje élfico sin elegir; cuero con `fuerza: null` | `especies/especies.yaml → especies[Elfo].velocidad_m` (pdf 191 / libro 189); «Elfo de los bosques» descartado por `rasgos_elegidos: {}`; `equipo/armaduras.yaml → reglas.fuerza` no aplica |
| `cd_conjuros` | **13** | 8 + mod. Car (+3) + PB (+2) | `reglas/generacion_personaje.yaml → conjuros.cd_salvacion` (pdf 240 / libro 238); aptitud por `clases/rasgos/brujo.yaml → rasgos[Magia del pacto]` (pdf 71 / libro 69) y `clases/brujo.yaml → aptitud_magica` |
| `bonif_ataque_conjuros` | **5** | mod. Car (+3) + PB (+2) | `reglas/generacion_personaje.yaml → conjuros.bonificador_ataque` (pdf 240 / libro 238); ídem aptitud |

Valores auxiliares derivados por el camino, por si sirven de contraste:

| Auxiliar | Valor | Fuente |
|---|---|---|
| mod. Fuerza | −1 | Fue 9 |
| mod. Destreza | +2 | Des 15 |
| mod. Constitución | +1 | Con 13 |
| mod. Inteligencia | +1 | Int 12 |
| mod. Sabiduría | 0 | Sab 10 |
| mod. Carisma | +3 | Car 16 |
| Bonificador por competencia | +2 | `clases/brujo.yaml → progresion[n:1].pb` y `reglas/generacion_personaje.yaml → px_por_nivel[nivel:1].pb` (pdf 43 / libro 41) |
| Aptitud mágica | Carisma | `clases/brujo.yaml → aptitud_magica` y prosa de «Magia del pacto» |

---

## Lo que NO se ha podido derivar de la base

**Nada de lo encargado queda sin derivar.** Los cinco valores salen enteros de
reglas declaradas y citables, y los dos de conjuros **sí proceden**, con la
fórmula presente y paginada en `reglas/generacion_personaje.yaml → conjuros`
(pdf 240 / libro 238). Confirmo por tanto, desde una clase distinta de las de
rondas anteriores, que ese hueco histórico está cerrado.

Ahora bien, hay **un hueco real** y **tres observaciones**:

### Hueco real — el linaje élfico obligatorio no está elegido en la ficha

`especies/especies.yaml → Elfo` declara el rasgo «Linaje élfico» con
`desc: "Elige un linaje…"`, sin `nivel:`, es decir **de nivel 1 y obligatorio**;
los tres linajes están enumerados en `Elfo.linajes` con su beneficio de nivel 1.
La ficha trae `especie.rasgos_elegidos: {}`.

Es un hueco de la **ficha**, no de la base —la base declara el rasgo, la
elección y las tres opciones con su mecánica—, pero **toca directamente uno de
mis cinco valores**, y por eso lo destaco en vez de dejarlo en nota al pie:

- Con la ficha tal como está: **velocidad = 9**. Es lo que pongo en el veredicto,
  porque es lo único que los datos crudos sostienen.
- La lectura alternativa: si la elección omitida fuera **«Elfo de los bosques»**,
  la velocidad sería **10,5**. Los otros dos linajes (Alto elfo, Drow) la dejan
  en 9.

Dicho de otro modo: dos de los tres linajes posibles dan 9 y uno da 10,5, y la
ficha no dice cuál es. **Elijo 9** porque un beneficio que no se ha elegido no se
obtiene, igual que un rasgo cuyo nivel no se ha alcanzado no aporta nada. Pero
el número no es tan firme como los otros cuatro, y conviene que quien mantenga
la ficha cierre esa elección.

*Un matiz que refuerza la elección de 9, aunque no la demuestra:* los dos trucos
de la ficha se explican enteros por la clase (Paso 2.1), y los tres linajes
conceden **cada uno un truco** de nivel 1 (prestidigitación / luces danzantes /
saber druídico). Si hubiera un linaje elegido y aplicado, cabría esperar un
tercer truco en la ficha. No lo hay. Es coherente con que, en efecto, no haya
linaje.

### Observación 1 — el Brujo no tiene ni un solo bloque `efectos:`

`clases/rasgos/brujo.yaml` (diez rasgos) y `clases/subclases/brujo.yaml` (cuatro
subclases) contienen **cero** bloques `efectos:`. Para esta derivación es
correcto: ninguno de sus rasgos toca `pg_max`, `ca` ni `velocidad`, y las
fórmulas de conjuros no viven en los rasgos sino en
`reglas/generacion_personaje.yaml`. Lo anoto porque significa que, a diferencia
del Bárbaro o del Monje, en el Brujo **no hay una segunda lectura formalizada
contra la que contrastar la prosa**: este informe es la única transcripción
independiente que existe para la clase. No es un defecto que haya que arreglar
añadiendo `efectos:` vacíos; es una razón para que esta derivación se conserve.

### Observación 2 — comprobé la trampa de nivel 20 y en el Brujo no está

El encargo advierte de dos rasgos de nivel 20 que subían puntuaciones de
característica y vivían solo en la prosa. Revisé el equivalente del Brujo,
**«Maestro sobrenatural»** (`clases/rasgos/brujo.yaml`, nivel 20, pdf 73 / libro
71): *«Cuando empleas tu rasgo Astucia mágica, recuperas todos los espacios de
conjuro gastados de Magia del pacto (en vez de solo la mitad).»* **No sube
ninguna puntuación** ni toca ninguno de los cinco valores. Repasé por lo mismo
los otros ocho rasgos de nivel > 1 del Brujo: todos hablan de recuperar o lanzar
conjuros. **La clase está limpia de ese modo de fallo.** Lo dejo escrito como
confirmación positiva, no como hallazgo.

### Observación 3 — tres discrepancias de la ficha ajenas a mis cinco valores

Las vi al recorrer la base y las anoto por si sirven, dejando claro que
**ninguna cambia ninguno de los cinco números**:

1. **La dote «Habilidoso» no tiene reflejo en las competencias.**
   `dotes/origen.yaml → Habilidoso` (pdf 203 / libro 201) concede «competencia
   en cualquier combinación de **tres** habilidades o herramientas». La ficha
   lista cuatro habilidades, todas con origen declarado (2 de clase, 2 de
   trasfondo), `herramientas: []`, y ninguna atribuida a la dote. Faltan las
   tres. *(Nota: el trasfondo Noble también concede una herramienta —«elige un
   tipo de juego»— que tampoco aparece.)*
2. **El equipo inicial no cuadra con la opción A declarada.**
   `clases/brujo.yaml → atributos_basicos.equipo_inicial.a` es «armadura de
   cuero, **hoz**, **2 dagas**, canalizador arcano (orbe), libro (de
   conocimiento oculto), paquete de erudito **y 15 po**». La ficha trae la
   armadura, **1** daga, el canalizador, el libro y el paquete: falta la hoz,
   falta una daga y faltan las 15 po. Tampoco figura el equipo del trasfondo
   Noble (`equipo_a`: juego, perfume, ropas de calidad, 29 po). Sin efecto sobre
   la CA, porque la pieza que la gobierna —la armadura de cuero— sí está.
3. **El reparto del conjunto estándar no sigue la fila recomendada.** Detallado
   en el Paso 0: la ficha intercambia Des y Car respecto de
   `conjunto_estandar_por_clase.filas[Brujo]`. Es **legal** (el conjunto
   estándar fija las seis puntuaciones, no su asignación, y esa tabla se
   presenta como recomendación de reparto) y, además, **da el mismo modificador
   de Carisma**: 14+2 = 16 y 15+2 = 17 caen los dos en la fila `"16-17": 3`. Es
   decir: la CD y el bonificador de ataque de conjuros salen 13 y 5 con
   cualquiera de los dos repartos.

---

*Informe escrito sin ejecutar ningún verificador, sin leer ninguna línea de
Python, sin abrir `personajes/`, sin abrir `reglas/efectos.yaml` (salvo la línea
suelta declarada arriba, que no contenía ninguna fórmula) y sin ver ningún valor
calculado por el motor para esta ficha ni para ninguna otra.*

---

## Veredicto

```veredicto
pg_max: 9
ca: 13
velocidad: 9
cd_conjuros: 13
bonif_ataque_conjuros: 5
```
