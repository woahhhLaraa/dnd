# Vaelith Val'thraxis (dracónido hechicero 3) — cálculo a mano, a ciegas

**Agente:** E · «el calculista» — ronda 3 de estrés.
**Fecha:** 2026-09-05.
**Ficha:** `draconido_hechicero_n3`, leída **sin bloque `calculado`** desde la copia cruda
`/tmp/claude-0/-home-user-dnd/ccce6f54-5659-5d7c-89a3-15e0f610e8cf/scratchpad/crudos/draconido_hechicero_n3.yaml`.

## Método

Segunda transcripción independiente: cada uno de los cinco valores se deriva **sólo** de la base
(`reglas/`, `especies/`, `clases/`, `equipo/`, `dotes/`, `trasfondos/`), con cita de fichero, campo y
página del manual donde el fichero la trae. Ningún número de este informe procede del motor.

### Ficheros de la base consultados

| Fichero | Para qué |
|---|---|
| `reglas/generacion_personaje.yaml` | modificadores, bonificador por competencia, PG (nivel 1 y siguientes), fórmulas de conjuros, regla de CA en multiclase |
| `reglas/fuentes_de_efectos.yaml` | enumerar **qué ficheros pueden conceder efectos**, para que el barrido de fuentes fuera completo y no una lista de memoria |
| `especies/especies.yaml` | Dracónido: velocidad, rasgos |
| `clases/hechicero.yaml` | dado de golpe, aptitud mágica, PB de la tabla de clase |
| `clases/rasgos/hechicero.yaml` | Lanzamiento de conjuros (aptitud mágica), Hechicería innata |
| `clases/subclases/hechicero.yaml` | Hechicería Dracónica → Resistencia dracónica (PG y CA) |
| `equipo/armaduras.yaml` | CA de armaduras y escudo, penalizador de velocidad por Fuerza |
| `equipo/aventureros.yaml` | contenido del paquete de explorador de mazmorras, canalizador arcano |
| `dotes/origen.yaml` | Afortunado (y Duro, para descartarlo) |
| `trasfondos/trasfondos.yaml` | Comerciante |

### Desviaciones del método — declaradas

Nada de lo que sigue me dio un número de esta ficha, pero lo declaro entero en vez de esconderlo:

1. **Un `grep` recursivo desde la raíz tocó `personajes/`.** Buscando la fórmula de CA base lancé
   `grep -rn "10 + " --include=*.yaml --include=*.md .` con exclusiones y se me colaron **dos líneas**
   de `personajes/_hallazgos/`: `orco_barbaro.md:18` y `draconido_monje.md:10`. Ambas son prosa sobre la
   fórmula de CA del **bárbaro** y del **monje** (`10 + mod Des + mod Con`, `10 + mod Des + mod Sab`),
   de personajes que no son este. **No contienen ningún valor calculado**, ni de esas fichas ni de la mía,
   y no tocan la fórmula del hechicero. No abrí esos ficheros ni ninguno de `personajes/`; en particular
   **no abrí `personajes/draconido_hechicero_n3.yaml`**. Los `grep` posteriores ya iban acotados a los
   directorios de la base.
2. **Del mismo `grep`, dos líneas de `reglas/_ESQUEMA_efectos.md`** (11 y 13, el ejemplo del monje; y la 98,
   una nota que dice que la CA base de quien no lleva nada, `10 + mod_des`, «no tiene página»). Ese fichero
   **no** está en la lista de vetados —lo vetado es `reglas/efectos.yaml`—, pero es documentación del
   esquema del motor, así que no lo abrí: sólo vi esas líneas en la salida. Importa porque **coincide con un
   hallazgo al que llegué por mi cuenta** (§2, «lo que la base no declara»), al que llegué grepeando
   `reglas/` y `equipo/`, no por esa línea.
3. **Del mismo `grep`, dos líneas de `ANALISIS_REPOS.md`** (41-42): `lambda` de CA de bárbaro y monje de un
   análisis de **otros repositorios**, no de este motor. Sin números de esta ficha.
4. **Leí los bloques `efectos:` incrustados en los ficheros de la base** (p. ej. el de Resistencia dracónica).
   Están dentro de ficheros que el encargo autoriza expresamente y son datos, no código. Aun así **derivo de la
   prosa (`desc`) y uso el `efectos:` sólo como corroboración**, y digo en cada caso si coinciden.
5. **No** abrí `calculo.py`, `efectos.py`, `reglas/efectos.yaml`, ningún verificador, ni nada bajo
   `_verificacion/` (tampoco `_verificacion/_aritmetica/`, donde escribo). **No** ejecuté ningún verificador:
   todos los números de este informe están hechos a mano.
6. Durante el trabajo, `reglas/fuentes_de_efectos.yaml` **cambió en disco** (otro agente añadió la lista
   enumerada `ficheros:` bajo `pendientes`). No afecta a ninguna derivación: lo usé sólo para saber qué
   directorios pueden conceder efectos.

---

## Paso 0 — Insumos comunes

### 0.a Modificadores de característica

`reglas/generacion_personaje.yaml → metodos_generacion_caracteristicas.modificadores_por_puntuacion`
(línea 30; `fuente: {pagina_pdf: 40, libro: 38}` del bloque padre)
· fórmula: `"(puntuación - 10) / 2, redondeando hacia abajo"`, con tabla adjunta.

Características **finales** de la ficha (`caracteristicas.final`): fue 8, des 14, con 14, int 10, sab 12, car 17.
Las finales son coherentes con `base` + `ajuste_trasfondo` (+2 Car, +1 Con), y ambos ajustes caen dentro de
`trasfondos/trasfondos.yaml → Comerciante → caracteristicas: [Constitución, Inteligencia, Carisma]` (línea 57),
como exige `metodos_generacion_caracteristicas.ajuste_por_trasfondo`.

| Característica | Puntuación | Por fórmula | Por tabla | Modificador |
|---|---|---|---|---|
| Destreza | 14 | (14−10)/2 = 2 | `"14-15": 2` | **+2** |
| Constitución | 14 | (14−10)/2 = 2 | `"14-15": 2` | **+2** |
| Carisma | 17 | (17−10)/2 = 3,5 → 3 | `"16-17": 3` | **+3** |

Fórmula y tabla coinciden en los tres casos.

### 0.b Bonificador por competencia (PB)

`reglas/generacion_personaje.yaml → px_por_nivel.filas[nivel: 3].pb = 2`
(`fuente: {pagina_pdf: 43, pagina_libro: 41, tabla: "Progreso de los personajes"}`).
Corroborado en `clases/hechicero.yaml → progresion[n: 3].pb = 2` (línea 26).

La regla `multiclase.bonificador_por_competencia` («se basa en el nivel TOTAL») no cambia nada: clase única,
Hechicero 3 = nivel total 3.

**PB = +2.**

### 0.c ¿Lleva armadura o escudo? — No

Hace falta para la CA y para la velocidad, y se resuelve con la ficha cruda + `equipo/`:

- `competencias.armaduras: []` — sin entrenamiento con armadura alguna.
- El `equipo` de la ficha son: lanza, 2 dagas, canalizador arcano (cristal), paquete de explorador de
  mazmorras, herramientas de navegante, 2 bolsas y ropas de viaje. **Ninguno** es un registro de
  `equipo/armaduras.yaml` (ni de `armaduras_ligeras`, ni `medias`, ni `pesadas`, ni `escudos`).
- El paquete tampoco esconde una: `equipo/aventureros.yaml` línea 156 →
  «Contiene: abrojos, 10 antorchas, cantimplora, cuerda, 2 frascos de aceite, mochila, palanqueta,
  raciones para 10 días y yesquero».

Luego se cumplen las condiciones `sin_armadura` y `sin escudo`.

### 0.d Barrido de fuentes de efectos

Para no fiarme de mi memoria sobre qué puede modificar PG/CA/velocidad, tomé el universo de fuentes de
`reglas/fuentes_de_efectos.yaml → fuentes`: `especies/especies.yaml`, `clases/rasgos/*.yaml`,
`clases/subclases/*.yaml`, `dotes/*.yaml`, `trasfondos/*.yaml` (más `equipo/` como fuente derivada, en
`pendientes`). Barrido de lo que aplica a **este** personaje:

| Fuente | ¿Toca pg_max / ca / velocidad? |
|---|---|
| `especies/especies.yaml → Dracónido` | **No.** Sus cinco rasgos son Linaje dracónico, Ataque de aliento, Resistencia al daño, Visión en la oscuridad y Vuelo dracónico (nivel 5, y temporal). El único rasgo de especie con `pg_max` en toda la base es *Aguante enano*. |
| `clases/rasgos/hechicero.yaml` | **No.** El fichero entero (45 líneas) no tiene ni un bloque `efectos:`; ningún rasgo de hechicero base toca PG, CA ni velocidad. |
| `clases/subclases/hechicero.yaml → Hechicería Dracónica` | **Sí:** *Resistencia dracónica* (nivel 3) → PG y CA. *Alas de dragón* es de nivel 14. |
| `dotes/origen.yaml → Afortunado` | **No.** Puntos de suerte / ventaja / desventaja. (La dote de origen que sí da PG es *Duro*, y no la tiene.) |
| `trasfondos/trasfondos.yaml → Comerciante` | **No.** Sin texto de rasgo; sólo características, dote, habilidades, herramienta y equipo. |
| `equipo/` | **No.** Sin armadura ni escudo (§0.c). |

---

## 1 · `pg_max` — puntos de golpe máximos

**Regla A — nivel 1.**
`reglas/generacion_personaje.yaml → puntos_golpe.nivel_1` (línea 190), `pagina: {pdf: 42, libro: 40}`:
> «Máximo del dado de golpe + modificador por Constitución.»

Dado de golpe: `clases/hechicero.yaml → atributos_basicos.dado_golpe: d6` (línea 9,
`fuente: {pagina_pdf: 125, pagina_libro: 123}`). Máximo del d6 = **6**.

    Nivel 1 = 6 + (+2 Con) = 8

La ficha declara ese nivel como `metodo: maximo_dado, valor: 6`, que es el mismo 6 del dado.

**Regla B — niveles 2 y 3.**
`reglas/generacion_personaje.yaml → puntos_golpe.niveles_siguientes_al_1` (línea 199),
`pagina: {pdf: 44, libro: 42}`, sección «Subir de nivel, paso 2», `fidelidad: literal`:
> «Cada vez que subas un nivel, obtendrás un dado de golpe adicional. Tira ese dado, suma tu modificador por
> Constitución al resultado y añade el total (mínimo de 1) a tus puntos de golpe máximos. En vez de tirar,
> puedes utilizar el valor establecido que se muestra en la tabla "Puntos de golpe establecidos por clase".»

- **Nivel 2** — la ficha eligió `valor_establecido: 4`. Contrastado con
  `puntos_golpe.niveles_siguientes_al_1.tabla_valores_establecidos.filas` (línea 225):
  `{clases: [Hechicero, Mago], valor: 4}`. Correcto para Hechicero.
  → 4 + (+2) = **6** (≥ 1, se respeta el mínimo).
- **Nivel 3** — la ficha eligió `tirada`, resultado 5. Es un dato de la partida, no derivable; sólo compruebo
  que 5 es un resultado posible de un d6. → 5 + (+2) = **7** (≥ 1).

**Subtotal de clase: 8 + 6 + 7 = 21.**

*Comprobación por la forma cerrada.* `puntos_golpe.aumento_de_constitucion` (línea 228,
`pagina: {pdf: 44, libro: 42}`, `_es_retroactivo: true`) obliga a que el término de Constitución sea
`nivel_total × mod_con` y no una suma histórica. Aquí: dados 6 + 4 + 5 = 15, Constitución 3 × (+2) = 6,
total 15 + 6 = **21**. Coincide con la suma nivel a nivel, como tiene que pasar cuando el modificador
nunca ha cambiado — y no ha cambiado: la Constitución vale 14 desde la creación (13 de base +1 del
trasfondo, ambos en el mismo momento) y no hay mejora de característica hasta el nivel 4.

**Regla C — rasgo de subclase.**
`clases/subclases/hechicero.yaml → subclases[Hechicería Dracónica].rasgos[nivel: 3, "Resistencia dracónica"]`
(línea 46), `pagina: {pdf: 135, libro: 133}`:
> «Tus puntos de golpe máximos aumentan en 3, y en 1 más por cada nivel de hechicero que subas en el futuro.»

Se obtiene **al** nivel 3 (la subclase entra en `progresion[n: 3]` del hechicero y
`niveles_de_subclase: [3, 6, 14, 18]`), así que aún no hay ningún nivel «futuro»: **+3**.
El `efectos:` del mismo registro cierra la misma regla como `{objetivo: pg_max, op: add, formula: "nivel_clase"}`
= 3 a nivel de hechicero 3. **Prosa y efecto coinciden.**

    pg_max = 21 + 3 = 24

**`pg_max` = 24.**

---

## 2 · `ca` — clase de armadura

Sin armadura y sin escudo (§0.c), así que se activa la CA base del rasgo de subclase.

`clases/subclases/hechicero.yaml → Hechicería Dracónica → "Resistencia dracónica"` (línea 46),
`pagina: {pdf: 135, libro: 133}`:
> «Además, mientras no lleves armadura, tu CA base es igual a 10 + tu modificador por Destreza + tu
> modificador por Carisma.»

    ca = 10 + (+2 Des) + (+3 Car) = 15

El `efectos:` del mismo registro dice `{objetivo: ca, op: base, formula: "10 + mod_des + mod_car",
requiere: [sin_armadura]}`. **Prosa y efecto coinciden**, incluida la condición: el rasgo del hechicero
exige sólo `sin_armadura` (a diferencia del monje y del bardo danzarín, que además exigen `sin_escudo`).
Aquí da igual, porque tampoco hay escudo.

**Escudo:** `equipo/armaduras.yaml → escudos` da `+2`, pero (a) no lleva ninguno y (b)
`reglas.escudos`: «Solo obtienes el bonificador a la CA de un escudo si tienes entrenamiento con escudos»,
y `competencias.armaduras` está vacío. No suma nada.

**Concurrencia de fórmulas:** `reglas/generacion_personaje.yaml → multiclase.clase_de_armadura`
(«si el personaje tiene varias formas de calcular su CA… solo puede beneficiarse de una, a elegir»,
`fuente: {pagina_pdf: [46,47], libro: [44,45]}`). Aquí sólo hay **una** fórmula especial, la de
Resistencia dracónica, así que no hay elección que hacer.

**Lectura alternativa considerada y descartada:** la CA por defecto de quien no lleva armadura
(10 + mod. Des = 12). Se descarta porque el rasgo declara una CA **base** completa que la sustituye
(`op: base`, no `op: add`), y 15 > 12 en cualquier caso.

**`ca` = 15.**

### Lo que la base no declara (hallazgo colateral, no bloquea este número)

Busqué la **CA por defecto** —la de un personaje sin armadura y sin ningún rasgo especial— y **no está en
la base**. Dónde miré:

- `reglas/generacion_personaje.yaml`: sólo la regla de concurrencia de CA en multiclase; no la fórmula.
- `equipo/armaduras.yaml → reglas`: entrenamiento, sin entrenamiento, escudos, un solo tipo, Fuerza y
  sigilo. Da la CA **de cada armadura** y del escudo, nunca la de quien no lleva nada.
- `grep` de «clase de armadura», «CA base» y «sin armadura» por `reglas/`, `equipo/`, `clases/`,
  `especies/`, `dotes/` y `trasfondos/`: los únicos sitios donde aparece `10 + …` como CA base son
  **rasgos de clase o subclase** (bárbaro, monje, bardo danzarín, hechicero dracónico), cada uno con su
  página. Ninguno declara el caso general.

O sea: **la base sabe calcular la CA de un bárbaro, un monje, un bardo danzarín y un hechicero dracónico
descalzos, pero no la de un mago descalzo.** Para este personaje es indiferente —su rasgo trae la fórmula
entera—, pero es el mismo agujero que ya se destapó con la CD de conjuros: una regla que el motor debe de
tener cableada y que la base no puede citar. No puedo confirmar dónde vive porque `reglas/efectos.yaml` y
`calculo.py` están vetados por el método; el comentario que `reglas/fuentes_de_efectos.yaml` cita de la
cabecera de `reglas/efectos.yaml` («una regla cableada no se puede citar, no se puede validar y no se entera
de que hay una quinta», dicho **de las fórmulas de CA**) apunta a que allí está el vocabulario del motor, que
no es lo mismo que la regla del manual con su página. **Queda como hallazgo a verificar por quien sí pueda
abrir esos ficheros.**

---

## 3 · `velocidad`

`especies/especies.yaml → especies[Dracónido].velocidad_m: 9` (línea 25),
`pagina: {pdf: 189, libro: 187}`; el fichero declara `fuente: {paginas_pdf: "188-199"}` y
`verificado: {metodo: "vision-directa", cobertura: "10/10"}`.

Modificadores posibles, todos descartados con cita:

- **Clase y subclase:** `clases/rasgos/hechicero.yaml` no tiene ningún rasgo de velocidad (ni un solo
  `efectos:` en sus 45 líneas). En `clases/subclases/hechicero.yaml`, lo único de movimiento es
  *Alas de dragón* (**nivel 14**, y velocidad volando temporal de 18 m).
- **Especie:** *Vuelo dracónico* es de **nivel 5** («acción adicional… 10 minutos… 1 vez por descanso
  largo»): ni aplica a nivel 3 ni sería permanente ni sería velocidad en tierra.
- **Armadura:** `equipo/armaduras.yaml → reglas.fuerza` («reduce 3 m la velocidad… salvo que su Fuerza sea
  igual o superior a la indicada») sólo actúa sobre quien lleva una armadura con puntuación de Fuerza en la
  tabla — es decir, cota de malla, bandas o placas. No lleva armadura (§0.c). El −3 m **no** se aplica.
  *(Ojo: si algún día llevara una de esas armaduras, con Fuerza 8 sí se lo comería.)*
- **Dote:** *Afortunado* no toca la velocidad.

**`velocidad` = 9 m.**

---

## 4 · `cd_conjuros` — CD de salvación de sus conjuros

**Fórmula.** `reglas/generacion_personaje.yaml → conjuros.cd_salvacion.formula` (línea 269),
`conjuros.pagina: {pdf: 240, libro: 238}`, sección «Tiradas de salvación / Tiradas de ataque»:
> «8 + modificador de aptitud mágica + bonificador por competencia»

**Aptitud mágica.** `clases/hechicero.yaml → aptitud_magica: Carisma` (línea 21). Corroborado por el rasgo:
`clases/rasgos/hechicero.yaml → "Lanzamiento de conjuros"` (`pagina: {pdf: 125, libro: 123}`) termina con
«Aptitud mágica: Carisma». Y `conjuros._nota_aptitud` de `generacion_personaje.yaml` remite justamente ahí:
«la aptitud mágica de cada clase la declara su propio fichero, en `clases/<clase>.yaml → aptitud_magica`».

    cd_conjuros = 8 + (+3 Car) + (+2 PB) = 13

**`cd_conjuros` = 13.**

Dos avisos para que nadie confunda números vecinos:

- *Hechicería innata* (`clases/rasgos/hechicero.yaml`, nivel 1, `pagina: {pdf: 126, libro: 124}`) da
  «CD de salvación de tus conjuros de hechicero **+1**» durante 1 minuto, 2 usos por descanso largo. Es un
  **efecto temporal activable**, no la CD de la ficha: la CD base sigue siendo 13 (14 mientras esté activo).
- El **Ataque de aliento** del dracónido (`especies/especies.yaml → Dracónido → rasgos`) tiene **su propia**
  CD, «8 + mod. Constitución + PB» = 8 + 2 + 2 = **12**, y no es la CD de conjuros. Son dos números distintos
  que se parecen.

*Nota sobre el estado de la base:* el bloque `conjuros:` de `reglas/generacion_personaje.yaml` lleva un
comentario fechado hoy diciendo que la fórmula **acaba de entrar** en la base porque antes vivía sólo en
`calculo.py`. He derivado la CD del bloque tal como está hoy en la base; si la fecha importa para el
contraste, ahí está.

---

## 5 · `bonif_ataque_conjuros` — bonificador de ataque con conjuros

**Fórmula.** `reglas/generacion_personaje.yaml → conjuros.bonificador_ataque.formula` (línea 272),
misma `pagina: {pdf: 240, libro: 238}`:
> «modificador de aptitud mágica + bonificador por competencia»

Misma aptitud mágica (Carisma, §4) y mismo PB (+2, §0.b).

    bonif_ataque_conjuros = (+3 Car) + (+2 PB) = +5

**`bonif_ataque_conjuros` = +5.**

(La ficha tiene trucos y conjuros de tirada de ataque —*Rayo de escarcha*, *Rayo abrasador*— que usan este
bonificador; *Proyectil mágico* y *Manos ardientes* no hacen tirada de ataque. No cambia el número, sólo
señalo que el valor se usa de verdad.)

---

## Valores derivados

| Valor | Resultado | Derivación en una línea | Cita principal |
|---|---:|---|---|
| `pg_max` | **24** | (6 máx. d6 + 4 establecido + 5 tirado) + 3 niveles × (+2 Con) + 3 de Resistencia dracónica | `reglas/generacion_personaje.yaml → puntos_golpe` (pdf 42 y 44) + `clases/subclases/hechicero.yaml` (pdf 135) |
| `ca` | **15** | 10 + (+2 Des) + (+3 Car), sin armadura | `clases/subclases/hechicero.yaml → Hechicería Dracónica → Resistencia dracónica` (pdf 135, libro 133) |
| `velocidad` | **9 m** | velocidad de especie, sin ningún modificador aplicable a nivel 3 | `especies/especies.yaml → Dracónido → velocidad_m` (pdf 189, libro 187) |
| `cd_conjuros` | **13** | 8 + (+3 Car) + (+2 PB) | `reglas/generacion_personaje.yaml → conjuros.cd_salvacion` (pdf 240, libro 238) |
| `bonif_ataque_conjuros` | **+5** | (+3 Car) + (+2 PB) | `reglas/generacion_personaje.yaml → conjuros.bonificador_ataque` (pdf 240, libro 238) |

Insumos comunes: mod. Des **+2**, mod. Con **+2**, mod. Car **+3**, PB **+2**, nivel total **3**,
sin armadura ni escudo.

## Qué no he podido derivar

- **Nada de los cinco valores queda sin derivar.** Los cinco salen de la base con cita.
- **Dos datos son elecciones de partida, no reglas**, y los he tomado de la ficha cruda sin poder
  derivarlos: el `5` tirado en el d6 del nivel 3 y la elección de `valor_establecido` en el nivel 2. Lo
  único derivable ahí es que 5 es un resultado posible de un d6 y que el valor establecido del Hechicero
  es 4 — ambas cosas comprobadas.
- **Sí falta una regla en la base, aunque no bloquea este personaje:** la **CA por defecto de quien no lleva
  armadura** (`10 + mod. Des`) no está declarada en ningún fichero de la base (§2). Este hechicero no la
  necesita porque Resistencia dracónica trae la fórmula entera, pero un personaje sin rasgo especial de CA
  no tendría de dónde sacarla.

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
ca: 15
velocidad: 9
cd_conjuros: 13
bonif_ataque_conjuros: 5
```
