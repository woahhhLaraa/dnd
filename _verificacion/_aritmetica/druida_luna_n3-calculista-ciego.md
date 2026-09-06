# Cálculo a mano — `druida_luna_n3` (agente E · «el calculista», ronda 3 de estrés)

## Cabecera

**Ficha calculada:** `Prueba Druida 3` — Aasimar, Druida 3 (Círculo de la Luna), trasfondo Acólito.
**Fuente de los datos crudos:** `/tmp/claude-0/-home-user-dnd/ccce6f54-5659-5d7c-89a3-15e0f610e8cf/scratchpad/crudos/druida_luna_n3.yaml` (ficha SIN bloque `calculado`).
**Fecha:** 2026-09-06.

### Método

Segunda transcripción independiente. Cada número de abajo se deriva **a mano** desde las
reglas y tablas de la base canónica, citando fichero y campo exactos. No se ha ejecutado
ningún verificador ni motor de cálculo, ni se ha leído código Python, ni se ha consultado
ninguna ficha ya calculada. Si un número coincide con el del motor, es coincidencia de dos
lecturas independientes; si no coincide, hay que mirar las dos.

### Ficheros consultados (todos leídos, ninguno ejecutado)

| Fichero | Para qué |
|---|---|
| `reglas/generacion_personaje.yaml` | modificadores por puntuación; PG nivel 1 y siguientes; tabla de valores establecidos; fórmula de CD y de bonificador de ataque de conjuros; tabla «Progreso de los personajes» (PB) |
| `reglas/caracteristicas.yaml` | emparejamiento nombre ↔ abreviatura (`sab` = Sabiduría, etc.) |
| `clases/druida.yaml` | dado de golpe, aptitud mágica, entrenamiento con armaduras, PB por nivel de clase |
| `clases/rasgos/druida.yaml` | rasgos de druida de niveles 1-3 (¿alguno toca CA, velocidad o PG?) |
| `clases/subclases/druida.yaml` | Círculo de la Luna, rasgos de nivel 3 — en especial «Formas del círculo» |
| `especies/especies.yaml` | Aasimar: velocidad base y rasgos (¿alguno toca CA, velocidad o PG?) |
| `trasfondos/trasfondos.yaml` | Acólito: características, dote de origen |
| `dotes/origen.yaml` | «Iniciado en la magia», la dote que concede el trasfondo |
| `equipo/armaduras.yaml` | catálogo: CA de la armadura llevada, requisito de Fuerza, y el bloque `reglas` |
| `equipo/aventureros.yaml` | contenido de los paquetes (por si un paquete escondiera armadura o escudo) |
| `reglas/fuentes_de_efectos.yaml` | comprobación final de que no queda ninguna fuente de efectos sin mirar |

### Desviaciones cometidas

**Ninguna.** No se han abierto `calculo.py`, `efectos.py`, `reglas/efectos.yaml`, ningún
verificador (`validar.py`, `verificar_*.py`, `censo.py`, `cobertura.py`, `generar_ficha.py`,
`subir_nivel.py`, `buscar.py`) ni nada bajo `_verificacion/`. No se ha abierto
`personajes/druida_luna_n3.yaml`, ninguna otra ficha de `personajes/`, ni
`personajes/_hallazgos/`. `_verificacion/_aritmetica/` no se ha listado: este fichero se ha
escrito directamente en su ruta. No se ha visto ningún número calculado por el motor antes de
escribir los de abajo.

**Una cosa que sí debo declarar, aunque sea menor.** Al terminar el informe corrí
`git status --porcelain` en la raíz para comprobar que no había tocado nada bajo `personajes/`,
y su salida me mostró —sin yo pedirlo— que en `_verificacion/_aritmetica/` existe además un
fichero `bardo_valor_n3-calculista-ciego.md`, de otro agente de esta misma ronda. **Vi el
nombre, no el contenido: no lo he abierto.** Además es de otra ficha (un bardo), así que no
contiene ningún número de este druida. Lo digo porque el mandato me pedía no listar ese
directorio ni siquiera de refilón, y esta comprobación de higiene acabó haciéndolo de rebote.
Los cinco números de abajo ya estaban escritos y guardados cuando ocurrió.

Dos apuntes sobre los avisos recibidos, para que no se lean como hallazgos:

- La CA por defecto sin armadura (`10 + mod. Des`) está declarada en un fichero vetado
  (`reglas/efectos.yaml`). **No hace falta aquí**: el personaje lleva armadura, así que la CA
  sale de la tabla de `equipo/armaduras.yaml`. No la he usado.
- La fórmula de la CD de conjuros **sí está en la base**, en
  `reglas/generacion_personaje.yaml → conjuros.cd_salvacion.formula` (pdf 240 / libro 238).
  La cito abajo. No es un hueco.

---

## Paso 0 — Materiales comunes: modificadores y bonificador por competencia

### 0.1 Modificadores por característica

Puntuaciones finales, de la ficha cruda (`caracteristicas.final`):
`fue 12`, `des 13`, `con 14`, `int 12`, `sab 16`, `car 8`.

Regla — `reglas/generacion_personaje.yaml → metodos_generacion_caracteristicas.modificadores_por_puntuacion`:

> `formula: "(puntuación - 10) / 2, redondeando hacia abajo"`

y su tabla, en el mismo campo (`…modificadores_por_puntuacion.tabla`): `"12-13": 1`,
`"14-15": 2`, `"16-17": 3`, `"8-9": -1`.

Aplicando la fórmula y contrastando con la tabla (coinciden):

| Característica | Puntuación | Cuenta | Modificador | Fila de la tabla |
|---|---|---|---|---|
| Fuerza (`fue`) | 12 | (12−10)/2 = 1 | **+1** | `"12-13": 1` |
| Destreza (`des`) | 13 | (13−10)/2 = 1,5 → 1 | **+1** | `"12-13": 1` |
| Constitución (`con`) | 14 | (14−10)/2 = 2 | **+2** | `"14-15": 2` |
| Inteligencia (`int`) | 12 | (12−10)/2 = 1 | **+1** | `"12-13": 1` |
| Sabiduría (`sab`) | 16 | (16−10)/2 = 3 | **+3** | `"16-17": 3` |
| Carisma (`car`) | 8 | (8−10)/2 = −1 | **−1** | `"8-9": -1` |

(El emparejamiento abreviatura ↔ nombre —`sab` = Sabiduría, `des` = Destreza…— está declarado
en `reglas/caracteristicas.yaml → caracteristicas`.)

### 0.2 Bonificador por competencia (PB)

Nivel total del personaje: 3 (`nivel_total: 3` en la ficha cruda; una sola clase, Druida 3).

Regla — `reglas/generacion_personaje.yaml → px_por_nivel` (tabla «Progreso de los personajes»,
pdf 43 / libro 41), fila `{nivel: 3, px: 900, pb: 2}` → **PB = +2**.

Confirmación redundante en el fichero de clase: `clases/druida.yaml → progresion`, fila
`{n: 3, pb: 2, …}` → **PB = +2**. Las dos fuentes coinciden.

Y el criterio de que el PB va por nivel TOTAL, no por nivel de una clase, está en
`reglas/generacion_personaje.yaml → multiclase.bonificador_por_competencia.regla`. Aquí es
indiferente (clase única), pero lo dejo citado.

---

## 1 · `pg_max` — Puntos de golpe máximos

### 1.1 Dado de golpe

`clases/druida.yaml → atributos_basicos.dado_golpe: d8`. Máximo del dado = **8**.

### 1.2 Nivel 1

Regla — `reglas/generacion_personaje.yaml → puntos_golpe.nivel_1.regla` (pdf 42 / libro 40):

> «Máximo del dado de golpe + modificador por Constitución.»

→ 8 + (+2) = **10**.

La ficha cruda declara para el nivel 1 `metodo: maximo_dado`, `valor: 8` con esa misma cita
(`pg_por_nivel[0].cita`), es decir, el 8 es el término del dado, sin Constitución. Coincide.

### 1.3 Niveles 2 y 3

Regla — `reglas/generacion_personaje.yaml → puntos_golpe.niveles_siguientes_al_1.literal`
(pdf 44 / libro 42, «Subir de nivel, paso 2»):

> «Cada vez que subas un nivel, obtendrás un dado de golpe adicional. Tira ese dado, suma tu
> modificador por Constitución al resultado y añade el total (mínimo de 1) a tus puntos de
> golpe máximos. En vez de tirar, puedes utilizar el valor establecido…»

La ficha declara `metodo: valor_establecido` en los niveles 2 y 3. Valor establecido para
Druida — `reglas/generacion_personaje.yaml → puntos_golpe.niveles_siguientes_al_1.tabla_valores_establecidos.filas`,
fila `{clases: [Bardo, Brujo, Clérigo, Druida, Monje, Pícaro], valor: 5}` → **5** por nivel.

- Nivel 2: 5 + (+2) = **7** (≥ 1, el mínimo del total no muerde).
- Nivel 3: 5 + (+2) = **7** (ídem).

### 1.4 Suma y comprobación por la vía del término de Constitución

    pg_max = 10 (nivel 1) + 7 (nivel 2) + 7 (nivel 3) = 24

Comprobación por la otra vía, la que describe
`reglas/generacion_personaje.yaml → puntos_golpe.aumento_de_constitucion._nota_para_el_motor`
(«el término de Constitución es `nivel_total × mod_con`»):

    términos de dado : 8 + 5 + 5            = 18
    término de Con   : 3 niveles × (+2)     =  6
    total                                    = 24

Las dos vías dan lo mismo. (`aumento_de_constitucion` no llega a aplicarse: el modificador por
Constitución de este personaje nunca sube — la única mejora posible sería la del nivel 4, que
este personaje aún no tiene.)

### 1.5 Descartes explícitos (nada más suma PG)

- **Especie Aasimar**: `especies/especies.yaml → especies[Aasimar].rasgos` — Manos curativas,
  Portador de luz, Resistencia celestial, Visión en la oscuridad, Revelación celestial.
  Ninguno toca los PG máximos. (El único rasgo de especie de toda la base que suma PG máximos
  es «Aguante enano» del Enano, `especies[Enano].rasgos`, y esta ficha no es Enano.)
- **Rasgos de druida 1-3** (`clases/rasgos/druida.yaml`): Lanzamiento de conjuros, Druídico,
  Orden primigenia, Compañero salvaje, Forma salvaje. Forma salvaje da **PG temporales**
  iguales al nivel de druida, no PG máximos: no suma aquí.
- **Círculo de la Luna, nivel 3** (`clases/subclases/druida.yaml`): «Formas del círculo» da
  «Puntos de golpe temporales (obtienes el triple de tu nivel de druida)». **Temporales, y solo
  al usar Forma salvaje**: no son `pg_max`.
- **Dote de trasfondo**: Acólito concede «Iniciado en la magia (clérigo)»
  (`trasfondos/trasfondos.yaml → trasfondos[Acólito].dote`); la dote
  (`dotes/origen.yaml → «Iniciado en la magia»`) solo da trucos y un conjuro. Cero PG.

> ### **`pg_max` = 24**

---

## 2 · `ca` — Clase de armadura

### 2.1 Equipo de la ficha, objeto a objeto

La ficha cruda trae **un solo objeto** en `equipo`:

    - ref: equipo/armaduras.yaml#Armadura de cuero tachonado

y una decisión declarada (`decisiones[1]`) que explica por qué el inventario está vacío: «el
equipo inicial vive como prosa en la base, así que esta ficha solo lleva armadura». No hay
paquete, no hay escudo, no hay ningún otro objeto.

**Comprobación de paquetes (aunque no haya ninguno en la ficha):** los siete paquetes de
`equipo/aventureros.yaml` (líneas 54-60 de la tabla, y su desglose en el bloque de contenidos,
líneas 152-158) son Paquete de artista, de diplomático, de erudito, de explorador, de
explorador de mazmorras, de ladrón y de sacerdote. **Ninguno de los siete contiene armadura ni
escudo** — lo más cercano es «túnica» (paquete de sacerdote), que no está en
`equipo/armaduras.yaml`. Así que aunque la ficha llevara el «paquete de explorador» que
`clases/druida.yaml → atributos_basicos.equipo_inicial.a` menciona en prosa, no cambiaría la
CA. Descarte cerrado.

### 2.2 La armadura en el catálogo

`equipo/armaduras.yaml → armaduras_ligeras.tabla`:

    - {nombre: "Armadura de cuero tachonado", ca: "12 + mod. Des", fuerza: null,
       sigilo: null, peso_kg: 6.5, precio: "45 po"}

Es **armadura ligera** (está en el bloque `armaduras_ligeras`), su fórmula de CA es
`12 + mod. Des` y **no tiene tope al modificador de Destreza** (los topes «(máx. 2)» solo
aparecen en `armaduras_medias`).

### 2.3 ¿Tiene entrenamiento con lo que lleva?

Regla — `equipo/armaduras.yaml → reglas.entrenamiento`:

> «Cualquiera puede ponerse una armadura o embrazar un escudo, pero solo quien tenga
> entrenamiento con ese tipo la usa de forma efectiva.»

La ficha declara (`competencias.armaduras`): `Armaduras ligeras` (origen: clase Druida) y
`Escudos` (origen: clase Druida). Concuerda con
`clases/druida.yaml → atributos_basicos.armaduras: ["Armaduras ligeras", Escudos]`.

La armadura de cuero tachonado es ligera → **sí tiene entrenamiento**. No aplica
`equipo/armaduras.yaml → reglas.sin_entrenamiento` (que impondría desventaja en pruebas de
Fuerza/Destreza e impediría lanzar conjuros).

Nota lateral: el druida podría haber obtenido entrenamiento con armaduras medias por «Orden
primigenia → Guardián» (`clases/rasgos/druida.yaml`, nivel 1), pero la ficha no lo declara en
`competencias.armaduras` y, además, no lleva armadura media. Irrelevante aquí.

`equipo/armaduras.yaml → reglas.escudos` («solo obtienes el bonificador a la CA de un escudo si
tienes entrenamiento con escudos»): **no aplica**, la ficha no lleva escudo. Tiene la
competencia, pero no el objeto. **Sin objeto no hay +2.**

`equipo/armaduras.yaml → reglas.solo_un_tipo`: trivialmente cumplido, una sola armadura.

### 2.4 El rasgo de subclase que menciona la CA — y por qué NO suma

`clases/subclases/druida.yaml → subclases[Círculo de la Luna].rasgos`, nivel 3,
**«Formas del círculo»**, texto completo:

> «Al usar Forma salvaje: Valor de desafío (máximo igual a tu nivel de druida dividido entre 3,
> redondeando abajo); **Clase de armadura (tu CA pasa a ser 13 + mod. Sabiduría si es superior a
> la de la bestia)**; Puntos de golpe temporales (obtienes el triple de tu nivel de druida).»

y su efecto declarado, en el mismo rasgo:

    efectos:
      - {objetivo: ca, op: conditional,
         texto: "En Forma salvaje, la CA pasa a ser 13 + mod. Sabiduría si es superior a la de
                 la bestia adoptada", pagina: {pdf: 99, libro: 97}}

**Decisión: NO aporta al número permanente de la ficha. La CA de la ficha se calcula sin él.**

Tres razones, todas del propio texto:

1. **El rasgo está encabezado por «Al usar Forma salvaje»**: todo lo que sigue —los tres
   términos, incluido el de CA— solo existe mientras el personaje está transformado en bestia.
   No es una forma alternativa de calcular la CA del druida en su cuerpo.
2. **La comparación es contra la CA de la bestia, no contra la del druida**: «si es superior a
   la de la bestia». El número al que sustituye es el de la criatura adoptada. En forma normal
   no hay bestia contra la que comparar, así que la cláusula ni siquiera es evaluable.
3. **La propia base lo marca como condicional**: `op: conditional` en el bloque `efectos`, no
   `base` ni `add`.

Si se sumara, saldría `13 + 3 = 16` en vez de 13, un error de +3 en la ficha de un personaje que
está de pie en su propio cuerpo. Ese descarte es parte del resultado.

(Y aunque se quisiera contar, `reglas/generacion_personaje.yaml → multiclase.clase_de_armadura`
recuerda que con varias formas de calcular la CA solo puede beneficiarse de una, a elegir; no
se acumulan.)

### 2.5 Otros descartes de CA

- **Aasimar** (`especies/especies.yaml → especies[Aasimar]`): ninguno de sus cinco rasgos
  menciona la clase de armadura.
- **Rasgos de druida 1-3** (`clases/rasgos/druida.yaml`): ninguno menciona la clase de armadura.
- **Acólito / «Iniciado en la magia»**: nada de CA.
- **Conjuros preparados** (`escudo`, `piel robliza`…): no hay ninguno así en la lista, y de
  haberlo sería un efecto de duración, no CA permanente.

### 2.6 Cuenta

    ca = 12 (armadura de cuero tachonado) + 1 (mod. Des, de Destreza 13)
       = 13

> ### **`ca` = 13**

---

## 3 · `velocidad`

### 3.1 Velocidad base, por especie

`especies/especies.yaml → especies[Aasimar].velocidad_m: 9` (pdf 188 / libro 186) → **9 m**.

No hay en `reglas/` ninguna otra declaración de velocidad base; la velocidad la fija la especie
y ninguna otra cosa la toca en esta ficha.

### 3.2 ¿Hay penalización por Fuerza insuficiente?

Regla — `equipo/armaduras.yaml → reglas.fuerza`:

> «Si la tabla indica una puntuación de Fuerza para un tipo de armadura, esta reduce 3 m la
> velocidad de quien la lleve, salvo que su Fuerza sea igual o superior a la indicada.»

Objeto a objeto, contra el catálogo:

| Objeto de la ficha | Bloque del catálogo | Campo `fuerza` | ¿Penaliza? |
|---|---|---|---|
| Armadura de cuero tachonado | `armaduras_ligeras.tabla` | **`null`** | **No** |

`fuerza: null` significa que la tabla **no indica ninguna puntuación de Fuerza** para esta
armadura, así que la condición de la regla no se dispara. De hecho, en todo
`equipo/armaduras.yaml` solo tres entradas traen requisito de Fuerza, y las tres son pesadas:
Cota de malla (`fuerza: 13`), Armadura de bandas (`fuerza: 15`) y Armadura de placas
(`fuerza: 15`). Este personaje, con Fuerza 12, quedaría por debajo de las tres —perdería 3 m—,
pero **no lleva ninguna de ellas**: lleva cuero tachonado. Sin penalización.

### 3.3 Otros descartes de velocidad

- **Aasimar**: «Revelación celestial» (nivel 3) ofrece «Alas celestiales (velocidad volando
  igual a tu velocidad)», pero es una transformación de 1 minuto, 1 vez por descanso largo, y
  además es velocidad **volando**, no la velocidad caminando de la ficha. No suma.
- **Formas del círculo / Forma salvaje**: la velocidad en forma de bestia es la de la bestia;
  el motor no modela bestias y la ficha registra al personaje en su cuerpo.
- Comparación útil para ver que el descarte es del mismo tipo que uno ya sellado en la base:
  `especies/especies.yaml → especies[Goliat].rasgos → «Forma grande»` declara explícitamente
  `{objetivo: velocidad, op: conditional, texto: "+3 m mientras dure Forma grande …, no de
  forma permanente"}`. Mismo criterio, aplicado aquí a Revelación celestial.

> ### **`velocidad` = 9 m**

---

## 4 · `cd_conjuros` — CD de salvación de conjuros

### 4.1 Aptitud mágica de la clase

`clases/druida.yaml → aptitud_magica: Sabiduría`. (Confirmado también en
`clases/rasgos/druida.yaml → «Lanzamiento de conjuros»`, nivel 1: «Aptitud mágica: Sabiduría».)

Sabiduría 16 → modificador **+3** (paso 0.1).

### 4.2 Fórmula

`reglas/generacion_personaje.yaml → conjuros.cd_salvacion` (pdf 240 / libro 238, sección
«Tiradas de salvación / Tiradas de ataque»):

    cd_salvacion:
      formula: "8 + modificador de aptitud mágica + bonificador por competencia"
      base: 8

Y `reglas/generacion_personaje.yaml → conjuros._nota_aptitud` remite, para la aptitud, a
`clases/<clase>.yaml → aptitud_magica`, que es lo que he usado.

### 4.3 Cuenta

    cd_conjuros = 8 + 3 (mod. Sabiduría) + 2 (PB de nivel 3)
                = 13

Descartes: la única otra fuente de magia del personaje sería la dote «Iniciado en la magia
(clérigo)» del trasfondo Acólito, cuya aptitud mágica se elige aparte
(`dotes/origen.yaml → «Iniciado en la magia»`); afectaría solo a los conjuros de esa dote, no a
la CD de druida de la ficha. Además, la ficha cruda **no declara ningún bloque de dotes**, así
que ni siquiera hay una elección de aptitud registrada que consultar.

> ### **`cd_conjuros` = 13**

---

## 5 · `bonif_ataque_conjuros` — Bonificador de ataque con conjuros

### 5.1 Fórmula

`reglas/generacion_personaje.yaml → conjuros.bonificador_ataque` (misma página: pdf 240 /
libro 238):

    bonificador_ataque:
      formula: "modificador de aptitud mágica + bonificador por competencia"
      base: 0

### 5.2 Cuenta

    bonif_ataque_conjuros = 3 (mod. Sabiduría, aptitud mágica de Druida) + 2 (PB de nivel 3)
                          = +5

Comprobación cruzada de coherencia con el paso 4: `cd_conjuros − bonif_ataque_conjuros` debe dar
exactamente 8, la `base` de `cd_salvacion`. 13 − 5 = 8. Cuadra.

> ### **`bonif_ataque_conjuros` = +5**

---

## Valores derivados

| Valor | Resultado | Derivación en una línea | Cita principal |
|---|---:|---|---|
| `pg_max` | **24** | (8 + 5 + 5) del dado + 3 niveles × (+2) por Constitución | `reglas/generacion_personaje.yaml → puntos_golpe.nivel_1` y `→ puntos_golpe.niveles_siguientes_al_1.tabla_valores_establecidos` |
| `ca` | **13** | 12 (cuero tachonado) + 1 (mod. Des) | `equipo/armaduras.yaml → armaduras_ligeras.tabla["Armadura de cuero tachonado"].ca` |
| `velocidad` | **9 m** | 9 m de especie, sin penalización de Fuerza (`fuerza: null`) | `especies/especies.yaml → especies[Aasimar].velocidad_m` y `equipo/armaduras.yaml → reglas.fuerza` |
| `cd_conjuros` | **13** | 8 + 3 (Sabiduría) + 2 (PB) | `reglas/generacion_personaje.yaml → conjuros.cd_salvacion.formula` |
| `bonif_ataque_conjuros` | **+5** | 3 (Sabiduría) + 2 (PB) | `reglas/generacion_personaje.yaml → conjuros.bonificador_ataque.formula` |

Materiales intermedios, por si hay que localizar una discrepancia:
mod. Fue **+1** · mod. Des **+1** · mod. Con **+2** · mod. Int **+1** · mod. Sab **+3** ·
mod. Car **−1** · PB **+2** · dado de golpe **d8** · aptitud mágica **Sabiduría**.

---

## Comprobación de cobertura: ¿me he dejado alguna fuente?

Para no fiarme de mi propio recorrido, contrasto los ficheros que he mirado contra el
manifiesto `reglas/fuentes_de_efectos.yaml`, que declara qué ficheros de la base pueden
conceder algo calculable al personaje. Son seis patrones, y los seis quedan cubiertos:

| Fuente declarada en el manifiesto | Qué toca en esta ficha | ¿Mirado? |
|---|---|---|
| `especies/especies.yaml` → `[especies, rasgos]` | Aasimar: 5 rasgos | Sí (§1.5, §2.5, §3.3) |
| `clases/rasgos/*.yaml` → `[rasgos]` | `druida.yaml`: rasgos de niveles 1-3 | Sí (§1.5, §2.5) |
| `clases/subclases/*.yaml` → `[subclases, rasgos]` | `druida.yaml` → Círculo de la Luna, nivel 3 | Sí (§2.4, el descarte razonado) |
| `dotes/*.yaml` → `[dotes]` | ninguna: la ficha cruda **no declara bloque `dotes`** | Sí (§1.5, §4.3) |
| `trasfondos/*.yaml` → `[trasfondos]` | Acólito: sin campo `efectos`, y su propio `no_automatizado` dice que no esconde mecánica en prosa | Sí |
| `equipo/armaduras.yaml` (categoría `derivadas`) | armadura de cuero tachonado | Sí (§2.2, §3.2) |

Vale la pena señalar que la entrada `derivadas` del manifiesto describe exactamente los dos
efectos que he calculado a mano desde esa tabla, y ninguno más:

    campos:
      - {campo: ca,     objetivo: ca,        op: "base|add"}
      - {campo: fuerza, objetivo: velocidad, op: add}

El campo `ca` de la armadura llevada (`"12 + mod. Des"`) es el que uso en §2.6; el campo
`fuerza` (`null` en cuero tachonado) es el que no dispara nada en §3.2. Coinciden en qué
campos son relevantes, que es lo único que este contraste puede confirmar — los números los
he sacado yo de la tabla, no de aquí.

Los ficheros que el manifiesto marca como **no fuente de efectos** incluyen `clases/druida.yaml`
(«tabla de progresión y atributos básicos») y `equipo/aventureros.yaml` («peso y precio, no
concede nada calculable»). Los he leído igualmente: el primero por el dado de golpe, la aptitud
mágica, el PB y el entrenamiento con armaduras —datos que uso como entrada, no como efectos—, y
el segundo para cerrar el descarte de paquetes de §2.1.

## Lo que NO se ha podido derivar de la base

**Nada de los cinco valores.** Los cinco se derivan enteros de ficheros de la base, con página
del manual en la cita. En particular, y a diferencia de lo que dejó escrito una ronda anterior
(ver el comentario de cabecera del bloque `conjuros` de
`reglas/generacion_personaje.yaml`), la fórmula de la CD de salvación y la del bonificador de
ataque **ya están en la base** y ya no obligan a parar.

Dos observaciones menores, que no son huecos de estos cinco valores pero conviene dejar
anotadas por si sirven a otro agente:

1. **La CA por defecto sin armadura no la he podido leer**, porque su única declaración está en
   `reglas/efectos.yaml`, que este mandato me veta. No me ha hecho falta —el personaje lleva
   armadura y la CA sale de `equipo/armaduras.yaml`—, pero dejo constancia de que **fuera de ese
   fichero vetado la base no repite `10 + mod. Des` en ningún sitio que yo haya podido leer**:
   ni en `reglas/generacion_personaje.yaml`, ni en `equipo/armaduras.yaml`, ni en las clases.
2. **La ficha cruda no declara la dote de origen del trasfondo.** Acólito concede «Iniciado en
   la magia (clérigo)» (`trasfondos/trasfondos.yaml → trasfondos[Acólito].dote`) y la ficha no
   tiene bloque `dotes`. No afecta a ninguno de los cinco valores —esa dote solo da trucos y un
   conjuro—, pero es una ausencia en los datos crudos, no una elección que yo haya podido leer.

## Lecturas dudosas y cuál elijo

Solo ha habido una, y la resuelvo en el apartado 2.4: **«Formas del círculo» (Círculo de la
Luna, nivel 3) y su cláusula «tu CA pasa a ser 13 + mod. Sabiduría»**.

- *Lectura A (la que elijo)*: es CA **solo en Forma salvaje**, sustituye la CA de la **bestia**
  y solo si la mejora. No entra en la ficha. → `ca` = 13.
- *Lectura B (la que descarto)*: es una forma alternativa de calcular la CA del druida, al modo
  de «Defensa sin armadura». → daría `ca` = max(13, 13 + 3) = 16.

**Elijo A** porque el rasgo se abre literalmente con «Al usar Forma salvaje:» y porque la
comparación explícita es «si es superior a la de **la bestia**» — sin bestia adoptada la
cláusula no tiene término contra el que compararse. La lectura B exigiría ignorar las dos
primeras palabras del rasgo.
