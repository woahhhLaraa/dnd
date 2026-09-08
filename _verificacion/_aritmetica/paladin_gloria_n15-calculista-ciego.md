# Ilanna Vela-de-Gloria — Paladín 15 (Juramento de Gloria)
## Cálculo a mano, a ciegas · agente E «el calculista» · ronda 3 de estrés

---

## Cabecera

**Ficha.** `Ilanna Vela-de-Gloria`, nivel total 15, Aasimar, trasfondo Acólito,
Paladín 15 con subclase *Juramento de Gloria*.
Datos crudos leídos de
`/tmp/claude-0/-home-user-dnd/ccce6f54-5659-5d7c-89a3-15e0f610e8cf/scratchpad/crudos/paladin_gloria_n15.yaml`
(sin bloque `calculado`).

**Método.** Segunda transcripción independiente. Cada número de este documento
sale de leer la regla en la base canónica y hacer la aritmética a mano, con cita
de fichero y campo. No se ha ejecutado ningún motor ni verificador: `python3` se
usó **sólo** como lector de YAML (`yaml.safe_load` + `print`) para imprimir
registros concretos de `dotes/generales.yaml` y `dotes/origen.yaml`, que son
ficheros largos; ninguna operación aritmética la hizo el ordenador.

**Ficheros consultados** (todos dentro de lo permitido):

| Fichero | Para qué |
|---|---|
| `reglas/generacion_personaje.yaml` | tabla de modificadores, PG nivel 1 y siguientes, PB por nivel, fórmulas de conjuros, ajuste por trasfondo |
| `reglas/caracteristicas.yaml` | emparejamiento nombre ↔ abreviatura (`car` = Carisma, etc.) |
| `reglas/subida_de_nivel.yaml` | qué concede cada nivel y qué elige el jugador |
| `reglas/fuentes_de_efectos.yaml` | **manifiesto de dónde puede haber efectos**, usado como lista de comprobación de cobertura (no aporta ningún número) |
| `clases/paladin.yaml` | dado de golpe, aptitud mágica, PB y rasgos del nivel 15 |
| `clases/rasgos/paladin.yaml` | los 14 rasgos de clase hasta nivel 15 |
| `clases/subclases/paladin.yaml` | rasgos del Juramento de Gloria (niveles 3, 7, 15) |
| `especies/especies.yaml` | Aasimar: velocidad y rasgos |
| `trasfondos/trasfondos.yaml` | Acólito |
| `equipo/armaduras.yaml` | Media armadura y las reglas de armadura |
| `dotes/generales.yaml` | las tres dotes generales |
| `dotes/origen.yaml`, `dotes/estilo_de_combate.yaml` | descartes razonados (ver §6) |

**Desviaciones cometidas.** Ninguna. No se abrió `calculo.py`, `efectos.py`,
`reglas/efectos.yaml`, ningún verificador, ningún fichero de `personajes/` ni
ningún otro fichero de `_verificacion/`. **No he visto ningún número del
proyecto para estos cinco valores antes de escribir los míos.** El directorio
`_verificacion/_aritmetica/` no se listó ni se leyó: se creó con `mkdir -p` y se
escribió directamente en él.

Dos cosas se dan por buenas según el propio encargo, sin contarlas como hallazgo:
la CA por defecto sin armadura vive en el fichero vetado (aquí es irrelevante:
la ficha lleva armadura), y la fórmula de la CD sí está en la base, en
`reglas/generacion_personaje.yaml → conjuros`.

---

## §0 · Insumos comunes

### 0.1 · Comprobación de `caracteristicas.final`

Regla del ajuste de trasfondo:
`reglas/generacion_personaje.yaml → metodos_generacion_caracteristicas.ajuste_por_trasfondo`
(«aumenta una de las tres características del trasfondo en 2 y otra distinta en 1,
o aumenta las tres en 1. Ningún ajuste puede superar 20»), pdf 40 / libro 38.

Las tres dotes de la ficha son las de los niveles 4, 8 y 12 —los tres marcadores
«Mejora de característica» de `clases/paladin.yaml → progresion` para un paladín
de nivel 15 (n:4, n:8, n:12; el de n:16 aún no se ha alcanzado)— y cada una
declara su propio `mejora_caracteristica` en `dotes/generales.yaml`:

| Dote | `mejora_caracteristica.entre` | `sube:` de la ficha | ¿coherente? |
|---|---|---|---|
| Atacante a la carga (pdf 205) | Fuerza, Destreza | `des: 1` | sí |
| Duelista defensivo (pdf 206) | Destreza | `des: 1` | sí |
| Maestro en armaduras medias (pdf 208) | Fuerza, Destreza | `des: 1` | sí |

Suma a mano:

| Carac. | base | + trasfondo | + dotes | = calculado | `final` de la ficha | ¿cuadra? |
|---|---|---|---|---|---|---|
| Fue | 15 | +2 | — | **17** | 17 | sí |
| Des | 13 | — | +1+1+1 = +3 | **16** | 16 | sí |
| Con | 12 | — | — | **12** | 12 | sí |
| Int | 8 | — | — | **8** | 8 | sí |
| Sab | 10 | — | — | **10** | 10 | sí |
| Car | 14 | +1 | — | **15** | 15 | sí |

`caracteristicas.final` **cuadra en las seis**. (Sobre la *legalidad* del `+2` a
Fuerza, ver §7.1: cuadra la aritmética, no la regla.)

### 0.2 · Modificadores

Tabla: `reglas/generacion_personaje.yaml → metodos_generacion_caracteristicas.modificadores_por_puntuacion.tabla`,
pdf 40 / libro 38 (fórmula: `(puntuación − 10) / 2, redondeando hacia abajo`).

- Fue 17 → rango `16-17` → **+3**
- **Des 16 → rango `16-17` → +3**
- **Con 12 → rango `12-13` → +1**
- Int 8 → rango `8-9` → −1
- Sab 10 → rango `10-11` → 0
- **Car 15 → rango `14-15` → +2**

### 0.3 · Bonificador por competencia

Dos fuentes independientes de la base, y coinciden:

- `clases/paladin.yaml → progresion`, fila `{n: 15, pb: 5, …}`
- `reglas/generacion_personaje.yaml → px_por_nivel.filas`, fila `{nivel: 15, px: 165000, pb: 5}` (pdf 43 / libro 41)

**PB = 5.**

---

## §1 · `pg_max`

**Nivel 1.** `reglas/generacion_personaje.yaml → puntos_golpe.nivel_1`
(pdf 42 / libro 40): «Máximo del dado de golpe + modificador por Constitución».
Dado de golpe del paladín: `clases/paladin.yaml → atributos_basicos.dado_golpe: d10`
(pdf 159 / libro 157). Máximo del d10 = 10.

    Nivel 1 = 10 + mod_con = 10 + 1 = 11

(La ficha registra `pg_por_nivel[0].valor: 10` con método `maximo_dado`: ese 10
es el dado, el `+1` de Constitución lo pone la regla aparte.)

**Niveles 2 a 15.** `reglas/generacion_personaje.yaml →
puntos_golpe.niveles_siguientes_al_1` (pdf 44 / libro 42), literal: «Tira ese
dado, suma tu modificador por Constitución al resultado y añade el total
(mínimo de 1)… En vez de tirar, puedes utilizar el valor establecido».
El valor establecido **sustituye a la tirada, no al modificador**.
Tabla `tabla_valores_establecidos.filas`: `{clases: [Explorador, Guerrero, Paladín], valor: 6}`.

Los 14 niveles del 2 al 15 de la ficha declaran los tres `metodo: valor_establecido`,
`valor: 6`, con esa misma cita.

    Cada nivel 2..15 = 6 + mod_con = 6 + 1 = 7   (≥ 1, el mínimo no muerde)
    14 niveles × 7 = 98

**Total.**

    pg_max = 11 + 98 = 109

**Comprobación por la vía que pide el `_nota_para_el_motor`** del mismo campo
(«El término de Constitución es `nivel_total × mod_con` … solo el término del
dado es historia acumulada»):

    dado nivel 1 .................. 10
    valores establecidos 2..15 .... 14 × 6 = 84
    Constitución .................. 15 × (+1) = 15
    -------------------------------------------
    pg_max ........................ 10 + 84 + 15 = 109

Las dos vías coinciden: **109**.

**Regla retroactiva de Constitución** (`puntos_golpe.aumento_de_constitucion`,
pdf 44 / libro 42): **no aplica**. Ninguna de las tres dotes sube Constitución
(las tres declaran `sube: {des: 1}`), y el trasfondo no la toca; Con vale 12 desde
el nivel 1 hasta el 15 y su modificador nunca cambió. Es justo el caso en que el
modelo plano y el correcto dan el mismo número, así que este 109 **no discrimina**
entre un motor que aplique bien la retroactividad y uno que no.

**Sin aportaciones externas a los PG.** Recorridas todas las fuentes de efectos
que le tocan a esta ficha (§6), ninguna toca `pg_max`: el Aasimar no tiene el
«Aguante enano» del Enano ni la «Resistencia dracónica» del Hechicero, ninguna de
las tres dotes generales lleva efecto sobre `pg_max`, y las dos dotes de la base
que sí lo llevan (`dotes/origen.yaml` → Duro, `dotes/don_epico.yaml` → Bendición
del Bastión) no están en la ficha.

> **`pg_max` = 109**

---

## §2 · `ca`

**Armadura equipada.** `equipo` de la ficha: un único elemento,
`equipo/armaduras.yaml#Media armadura`. **No hay escudo** en la ficha, así que el
`+2` del escudo (`equipo/armaduras.yaml → escudos.tabla`) no entra.

**Fórmula base de la armadura.** `equipo/armaduras.yaml → armaduras_medias.tabla`
(pdf 218 / libro 216): `{nombre: "Media armadura", ca: "15 + mod. Des (máx. 2)", …}`.

Es decir: **base 15, más el modificador por Destreza, topado en 2.**

**El tope cambia.** `dotes/generales.yaml → Maestro en armaduras medias`
(pdf 208 / libro 206), descripción literal del bloque *Portador diestro*:

> «mientras lleves armadura media, sumas **3 (en vez de 2)** a tu CA por Destreza
> si tu puntuación de Destreza es 16 o más»

Esta dote **no suma nada a la CA**: cambia el «(máx. 2)» que la Media armadura
impone al modificador por Destreza. Las dos condiciones se cumplen:

- lleva armadura media (Media armadura, §arriba) ✔
- Destreza 16 ≥ 16 ✔ (§0.1)

**Aritmética.**

    mod_des = +3            (Des 16, §0.2)
    tope    = 3             (por Maestro en armaduras medias, en vez del 2 de la armadura)
    ca = 15 + min(+3, 3) = 15 + 3 = 18

**Dos lecturas posibles de la frase, y aquí convergen.** «Sumas 3 (en vez de 2)»
puede leerse como *«el tope pasa de 2 a 3»* → `15 + min(3, 3) = 18`, o como
*«sumas exactamente 3»* → `15 + 3 = 18`. **Con Des 16 dan el mismo número**, así
que este valor no distingue entre ambas. Elijo la primera (tope) porque es la que
respeta la forma de la fórmula de la armadura y la única que se generaliza —con
Des 18, mod +4, la lectura de tope daría 18 y la de suma fija también 18, pero con
Des 20, mod +5, ambas seguirían dando 18; la diferencia sólo aparecería con Des 14
(mod +2): tope → 17, suma fija → 18, y ahí el propio manual aclara que con Destreza
inferior a 16 la dote no se nota. La lectura de tope es la coherente con esa frase.

**Descartes explícitos** (efectos que tocan `ca` pero **no** entran en el número de la ficha):

1. **Defensa gloriosa**, rasgo de nivel 15 del Juramento de Gloria
   (`clases/subclases/paladin.yaml`, pdf 164 / libro 162): «**Reacción** cuando una
   tirada de ataque os acierta… sumas un bonificador a la CA del objetivo igual a
   tu modificador por Carisma (mínimo +1)… **Usos iguales a tu modificador por
   Carisma**». Es una **reacción con usos limitados y objetivo variable** (puede ser
   ella o un aliado a 3 m): no es CA permanente. **NO entra.** Si entrara, sumaría
   +2 y daría 20 — no es la CA de la ficha.
2. **Duelista defensivo**, dote de nivel 8 (`dotes/generales.yaml`, pdf 206 /
   libro 204): «si empuñas un arma sutil y otra criatura te acierta cuerpo a cuerpo,
   **reacción** para sumar tu bonificador por competencia a tu CA». Reacción,
   condicionada a un arma sutil que además la ficha no lleva (`equipo` sólo tiene la
   armadura). **NO entra.** Si entrara, sumaría +5.
3. **Atacante a la carga** no toca la CA en absoluto.

> **`ca` = 18** (Media armadura 15 + Des +3, con el tope subido a 3 por Maestro en armaduras medias; sin escudo)

---

## §3 · `velocidad`

**Base de especie.** `especies/especies.yaml → especies[Aasimar].velocidad_m: 9`
(pdf 188 / libro 186). **9 m.**

**Aumento permanente.** `clases/subclases/paladin.yaml → Juramento de Gloria →
rasgos[nivel: 7] "Aura de celeridad"` (pdf 164 / libro 162):

> «**Tu velocidad aumenta en 3 m.** Además, siempre que un aliado entre en tu Aura
> de protección por primera vez en un turno o comience su turno dentro de ella, su
> velocidad aumenta en 3 m hasta el final de su próximo turno.»

La **primera frase** no tiene condición, ni duración, ni usos: es la velocidad del
paladín, y se calcula. La segunda es sobre la velocidad de **otra criatura** y
depende de dónde esté: se cita, no se agrega. El personaje es Paladín 15 ≥ 7, así
que el rasgo está activo.

    velocidad = 9 + 3 = 12 m

**Penalización por armadura: no aplica.** `equipo/armaduras.yaml → reglas.fuerza`:
«Si la tabla indica una puntuación de Fuerza para un tipo de armadura, esta reduce
3 m la velocidad de quien la lleve, salvo que su Fuerza sea igual o superior a la
indicada». La fila de **Media armadura** trae `fuerza: null` — la tabla no indica
puntuación de Fuerza, así que **no hay −3 m**. (Aunque la hubiera, Fue 17 la
superaría con holgura en las tres armaduras que la piden: 13, 15 y 15.)

**Descartes explícitos** (efectos que tocan `velocidad` pero **no** entran):

1. **Atacante a la carga**, dote de nivel 4 (`dotes/generales.yaml`, pdf 205 /
   libro 203), bloque *Carrera mejorada*: «**al correr**, tu velocidad aumenta 3 m
   **para esa acción**». Es un extra de **una acción concreta** (la de correr), no la
   velocidad de la ficha. **NO entra.** Si entrara, daría 15 m.
2. **Atleta sin parangón**, rasgo de nivel 3 del Juramento de Gloria (pdf 164 /
   libro 162): acción adicional, gasta Canalizar divinidad, dura **1 hora**, y lo que
   aumenta son **los saltos** («aumentar en 3 m la distancia de tus saltos»), no la
   velocidad. **NO entra** por partida doble: es temporal y ni siquiera es velocidad.
3. **Revelación celestial** del Aasimar (nivel 3, pdf 188 / libro 186): «Acción
   adicional para transformarte **1 minuto, 1 vez por descanso largo**»; la opción
   *Alas celestiales* da una **velocidad volando** igual a la velocidad. Temporal, con
   usos, y además es un modo de desplazamiento distinto. **NO entra.**
4. La dote **Veloz** (`dotes/generales.yaml`, pdf 211) sí daría un `+3 m`
   permanente, pero **no está en esta ficha**.

> **`velocidad` = 12 m**

---

## §4 · `cd_conjuros`

**Fórmula.** `reglas/generacion_personaje.yaml → conjuros.cd_salvacion`
(pdf 240 / libro 238, sección «Tiradas de salvación / Tiradas de ataque»):

    CD = 8 + modificador de aptitud mágica + bonificador por competencia

**Aptitud mágica.** `clases/paladin.yaml → aptitud_magica: Carisma`
(confirmado en `clases/rasgos/paladin.yaml → "Lanzamiento de conjuros"`, nivel 1,
pdf 159 / libro 157: «Aptitud mágica: Carisma»). El emparejamiento `car` = Carisma
está en `reglas/caracteristicas.yaml`.

**Aritmética.**

    mod_car = +2   (Car 15, §0.2)
    PB      = 5    (nivel 15, §0.3)
    cd_conjuros = 8 + 2 + 5 = 15

Clase única: no hay reparto multiclase que aplicar
(`reglas/generacion_personaje.yaml → multiclase.lanzamiento_de_conjuros_multiclase`
sólo entra «si se tiene por más de una» clase).

> **`cd_conjuros` = 15**

---

## §5 · `bonif_ataque_conjuros`

**Fórmula.** `reglas/generacion_personaje.yaml → conjuros.bonificador_ataque`
(misma página, pdf 240 / libro 238):

    bonificador de ataque = modificador de aptitud mágica + bonificador por competencia

**Aritmética.** Misma aptitud mágica (Carisma) y mismo PB que en §4:

    bonif_ataque_conjuros = +2 + 5 = +7

> **`bonif_ataque_conjuros` = +7**

---

## §6 · Cobertura: dónde busqué efectos, y qué encontré

Para no dejarme una fuente, recorrí el manifiesto
`reglas/fuentes_de_efectos.yaml → fuentes` / `derivadas` y visité **todas** las que
le tocan a esta ficha:

| Fuente declarada | Registro de esta ficha | ¿Toca pg_max / ca / velocidad? |
|---|---|---|
| `especies/especies.yaml` | Aasimar, 5 rasgos | no (Revelación celestial: descartada, §3) |
| `clases/rasgos/paladin.yaml` | los 14 rasgos hasta nivel 15 | **ninguno**: Imponer las manos, Lanzamiento de conjuros, Maestría con armas, Castigo de paladín, Estilo de combate, Canalizar divinidad, Ataque adicional, Corcel fiel, Aura de protección, Abjurar de los enemigos, Aura de coraje, Golpes radiantes, Toque reparador |
| `clases/subclases/paladin.yaml` | Juramento de Gloria, rasgos de nivel 3, 7 y 15 | **velocidad +3 m** (Aura de celeridad, permanente) y **ca condicional** (Defensa gloriosa, descartada) |
| `dotes/*.yaml` | las 3 dotes generales | **ca: tope de Des a 3**; los otros dos efectos son condicionales |
| `trasfondos/trasfondos.yaml` | Acólito | ningún `efectos:` en todo el fichero (comprobado: 0 apariciones) |
| `equipo/armaduras.yaml` (derivada) | Media armadura | **ca base 15 + Des (máx. 2)**; `fuerza: null` → sin −3 m |

---

## §7 · Lo que no cuadra en los datos crudos (no cambia mis cinco números)

### 7.1 · El `+2` de Fuerza no lo puede dar el trasfondo Acólito

`trasfondos/trasfondos.yaml → Acólito` (pdf 180 / libro 178) declara
`caracteristicas: [Inteligencia, Sabiduría, Carisma]`.
La ficha aplica `ajuste_trasfondo: {fue: 2, car: 1}`.

La regla (`reglas/generacion_personaje.yaml →
metodos_generacion_caracteristicas.ajuste_por_trasfondo`) dice «aumenta **una de
las tres características del trasfondo** en 2 y otra distinta en 1». **Fuerza no es
una de las tres del Acólito.** El `car: 1` sí es legal; el `fue: 2` no.

Efecto sobre mis cinco valores: **ninguno**. Fuerza no entra en `pg_max`, ni en la
`ca` (Media armadura no pide Fuerza), ni en la `velocidad`, ni en las dos fórmulas
de conjuros. Lo anoto porque el enunciado pedía comprobar `caracteristicas.final`:
la **suma** cuadra, la **legalidad del sumando** no.

### 7.2 · La ficha dice `opcion: A` pero no lleva lo que da la opción A

`equipo[0].origen` es `{clase: Paladín, opcion: A}`, y
`clases/paladin.yaml → atributos_basicos.equipo_inicial.a` es «**cota de malla,
escudo**, espada larga, 6 jabalinas, símbolo sagrado, paquete de sacerdote y 9 po».
Lo que la ficha equipa es **Media armadura**, que no aparece en esa opción, y no
lleva escudo.

El bloque `decisiones` de la ficha explica que el equipo inicial vive como prosa y
que por eso «esta ficha solo lleva armadura», pero eso justifica *no llevar el
resto*, no *llevar una armadura distinta*.

**He calculado con lo que la ficha declara equipado** (Media armadura, sin escudo)
→ 18. Curiosidad que conviene decir en voz alta para que nadie la use como
confirmación: **la opción A literal daría también 18** (Cota de malla `ca: 16`, fija,
sin modificador por Destreza, más `+2` de escudo). Es una coincidencia numérica; los
dos caminos son distintos y sólo uno está declarado en la ficha.

### 7.3 · Falta el Estilo de combate del nivel 2, y falta la dote de trasfondo

- `clases/paladin.yaml → progresion[n:2].rasgos` incluye **«Estilo de combate»**, que
  según `clases/rasgos/paladin.yaml` (pdf 160 / libro 158) «obtienes una dote de
  estilo de combate de tu elección». La ficha **no declara ninguna**
  (`dotes` sólo trae las tres generales; `mejoras: []`).
  Importa para la CA: si esa dote fuera **Defensa**
  (`dotes/estilo_de_combate.yaml`, pdf 211 / libro 209: «+1 a la clase de armadura»
  mientras lleves armadura ligera, media o pesada), la CA sería **19**, no 18.
  Como la ficha no la declara, **calculo 18**; si el motor la hubiera supuesto,
  discreparíamos por esa razón y no por aritmética.
- `trasfondos/trasfondos.yaml → Acólito` concede la dote **«Iniciado en la magia
  (clérigo)»**, que tampoco figura en `dotes`. Comprobado en `dotes/origen.yaml`
  (pdf 203 / libro 201): **no altera ninguno de mis cinco valores** — da trucos y un
  conjuro de nivel 1 con aptitud mágica propia elegible, que no cambia la CD de
  conjuros del paladín.

### 7.4 · Reparto del conjunto estándar

La ficha reparte 15/14/13/12/10/8 como Fue 15, Car 14, Des 13, Con 12, Sab 10, Int 8;
la tabla `conjunto_estandar_por_clase` de `reglas/generacion_personaje.yaml`
(pdf 40) sugiere para Paladín Fue 15, Des 10, Con 13, Int 8, Sab 12, Car 14.
El conjunto de seis valores es el correcto y el propio bloque `decisiones` declara
la heurística; lo dejo como **nota, no como error**.

---

## Valores derivados

| Valor | Resultado | Derivación en una línea | Cita principal |
|---|---|---|---|
| `pg_max` | **109** | `10` (máx. d10) + `14 × 6` (valor establecido) + `15 × (+1)` (Con) | `reglas/generacion_personaje.yaml → puntos_golpe.nivel_1` (pdf 42) y `→ puntos_golpe.niveles_siguientes_al_1` (pdf 44); `clases/paladin.yaml → atributos_basicos.dado_golpe` |
| `ca` | **18** | `15` (Media armadura) + `min(mod_des +3, tope 3)`; sin escudo | `equipo/armaduras.yaml → armaduras_medias.tabla` (pdf 218) + `dotes/generales.yaml → Maestro en armaduras medias` (pdf 208) |
| `velocidad` | **12 m** | `9 m` (Aasimar) + `3 m` (Aura de celeridad, nivel 7); sin penalización de armadura | `especies/especies.yaml → Aasimar.velocidad_m` (pdf 188) + `clases/subclases/paladin.yaml → Juramento de Gloria → rasgos[nivel:7]` (pdf 164) |
| `cd_conjuros` | **15** | `8 + mod_car (+2) + PB (5)` | `reglas/generacion_personaje.yaml → conjuros.cd_salvacion` (pdf 240) + `clases/paladin.yaml → aptitud_magica` |
| `bonif_ataque_conjuros` | **+7** | `mod_car (+2) + PB (5)` | `reglas/generacion_personaje.yaml → conjuros.bonificador_ataque` (pdf 240) |

### Descartes que sostienen estos números

| Efecto | Fuente | Por qué NO entra | Qué habría dado |
|---|---|---|---|
| Defensa gloriosa | subclase, nivel 15 (pdf 164) | reacción, usos limitados, objetivo variable | ca 20 |
| Parada (Duelista defensivo) | dote nivel 8 (pdf 206) | reacción, y exige arma sutil que no lleva | ca 23 |
| Carrera mejorada (Atacante a la carga) | dote nivel 4 (pdf 205) | sólo durante la acción de correr | velocidad 15 m |
| Atleta sin parangón | subclase, nivel 3 (pdf 164) | 1 hora, gasta Canalizar divinidad, y aumenta **saltos**, no velocidad | — |
| Revelación celestial (Alas celestiales) | Aasimar, nivel 3 (pdf 188) | 1 minuto, 1 vez por descanso largo, y es velocidad **volando** | — |

### Nada quedó sin derivar

Los cinco valores salen enteros de la base: no hay ningún hueco que impida
calcularlos. Los dos avisos del encargo se cumplieron tal cual —la fórmula de la CD
**sí** está en `reglas/generacion_personaje.yaml → conjuros`, con página (pdf 240 /
libro 238), y la CA sin armadura no hizo falta porque la ficha lleva armadura—.

Lo único que la base **no** permite resolver son las **elecciones que la ficha no
declara**, y no son cálculo sino datos que faltan: el Estilo de combate del nivel 2
(§7.3) es el único que podría mover uno de mis cinco números, y lo movería de 18 a
19 en la CA **sólo si** esa elección fuera *Defensa*. Con lo declarado, 18.

---

*Escrito sin ver ningún número del proyecto para esta ficha. Ningún paso se ajustó
para cuadrar con nada.*

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
pg_max: 109
ca: 18
velocidad: 12
cd_conjuros: 15
bonif_ataque_conjuros: 7
```
