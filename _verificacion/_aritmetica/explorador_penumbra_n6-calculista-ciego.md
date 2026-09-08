# Kaelin Paso-en-Sombra — aritmética a mano (agente E · «el calculista», ciego)

## Cabecera

**Ficha:** Kaelin Paso-en-Sombra. Aasimar, Explorador 6 (Acechador en la Penumbra),
trasfondo Acólito. Nivel total 6.

**Datos de partida (única entrada usada):**
`/tmp/claude-0/-home-user-dnd/ccce6f54-5659-5d7c-89a3-15e0f610e8cf/scratchpad/crudos/explorador_penumbra_n6.yaml`
— datos crudos, SIN bloque `calculado`.

**Método.** Transcripción independiente. Cada número sale de leer la regla en la base
canónica y aplicarla a mano, escribiendo el paso intermedio y citando fichero y campo.
No se ha leído ni ejecutado nada del motor ni de sus verificadores, y no se ha visto
ningún número producido por el proyecto para esta ficha ni para ninguna otra.

**Ficheros consultados (todos de la base, todos permitidos):**

| Fichero | Para qué |
|---|---|
| `reglas/generacion_personaje.yaml` | tabla de modificadores, PG nivel 1 y siguientes, PB por nivel, fórmulas de conjuros |
| `reglas/caracteristicas.yaml` | emparejamiento nombre ↔ abreviatura (`sab` = Sabiduría, etc.) |
| `reglas/fuentes_de_efectos.yaml` | comprobación de exhaustividad: qué familias de ficheros pueden conceder efectos |
| `clases/explorador.yaml` | dado de golpe, aptitud mágica, tabla de progresión (PB y rasgos por nivel) |
| `clases/rasgos/explorador.yaml` | rasgos de clase 1–6, en particular «Errante» |
| `clases/subclases/explorador.yaml` | rasgos de Acechador en la Penumbra y sus niveles |
| `especies/especies.yaml` | velocidad base y rasgos del Aasimar |
| `trasfondos/trasfondos.yaml` | qué concede Acólito |
| `equipo/armaduras.yaml` | CA de Media armadura, categoría, regla de Fuerza y de escudos |
| `dotes/estilo_de_combate.yaml` | dote Defensa |
| `dotes/generales.yaml` | Mejora de característica; descarte de «Maestro en armaduras medias» |
| `dotes/origen.yaml` | «Iniciado en la magia», para descartar que toque estos cinco valores |

**Desviaciones cometidas:** ninguna. No se abrió `calculo.py`, `efectos.py`,
`reglas/efectos.yaml`, ningún `verificar_*.py`, `validar.py`, `censo.py`,
`cobertura.py`, `generar_ficha.py`, `subir_nivel.py`, `buscar.py`, ningún fichero de
`personajes/` ni ningún contenido de `_verificacion/`. Este documento se escribe dentro
de `_verificacion/_aritmetica/` (destino del encargo) sin haber leído nada de ese árbol:
solo se creó el directorio con `mkdir -p` y se escribió el fichero. No se ha visto por
accidente ningún número del proyecto.

---

## 0. Cantidades previas (se usan en varios apartados)

### 0.1 Modificadores de característica

Regla: `reglas/generacion_personaje.yaml → metodos_generacion_caracteristicas.modificadores_por_puntuacion`
— fórmula «(puntuación − 10) / 2, redondeando hacia abajo», con tabla explícita.
Nombres y abreviaturas: `reglas/caracteristicas.yaml → caracteristicas`.

Puntuaciones finales del crudo (`caracteristicas.final`), comprobadas contra su propia
cadena de origen (`base` + `ajuste_trasfondo` + `mejoras`):

| Característica | Base | Ajuste trasfondo | Mejora nivel 4 | Final | Modificador |
|---|---|---|---|---|---|
| Fuerza | 12 | — | — | 12 | **+1** (tabla, «12-13») |
| Destreza | 15 | — | +2 | 17 | **+3** (tabla, «16-17») |
| Constitución | 13 | — | — | 13 | **+1** (tabla, «12-13») |
| Inteligencia | 10 | +2 | — | 12 | **+1** (tabla, «12-13») |
| Sabiduría | 14 | +1 | — | 15 | **+2** (tabla, «14-15») |
| Carisma | 8 | — | — | 8 | **−1** (tabla, «8-9») |

La suma cuadra con el campo `caracteristicas.final` del crudo: 12 / 17 / 13 / 12 / 15 / 8.
La mejora de nivel 4 es `dotes/generales.yaml → Mejora de característica`
(`mejora_caracteristica: {cantidad: 2, maximo: 20}`); 15 + 2 = 17 ≤ 20, legal.

Los tres que usaré: **mod. Des = +3**, **mod. Con = +1**, **mod. Sab = +2**.

### 0.2 Bonificador por competencia

`reglas/generacion_personaje.yaml → px_por_nivel.filas`, fila `{nivel: 6, px: 14000, pb: 3}`.
Confirmado por segunda vía en `clases/explorador.yaml → progresion`, fila `{n: 6, pb: 3}`.
Personaje de una sola clase, nivel total 6.

**PB = +3.**

### 0.3 Qué rasgos están activos a nivel 6, y cuáles no

Rasgos de clase (`clases/explorador.yaml → progresion`, niveles 1 a 6):
Lanzamiento de conjuros, Enemigo predilecto, Maestría con armas (n.1); Estilo de combate,
Explorador hábil (n.2); Subclase (n.3); Mejora de característica (n.4); Ataque adicional
(n.5); **Errante** (n.6).

Rasgos de subclase: `clases/subclases/explorador.yaml → niveles_de_subclase: [3, 7, 11, 15]`.
A nivel 6 solo están activos los de nivel 3 del Acechador en la Penumbra:
Conjuros de acechador en la penumbra, **Emboscador pavoroso**, Visión en la umbra.
*Mente de hierro* es de nivel 7 y **no está activo**; *Oleada del acechador* (11) y
*Esquiva de las sombras* (15) tampoco.

De todos ellos, los únicos que tocan CA, velocidad o PG son «Errante» y la mitad
«Salto emboscador» de «Emboscador pavoroso». Se tratan en sus apartados.

**Comprobación de exhaustividad.** Según `reglas/fuentes_de_efectos.yaml`, lo que puede
conceder efectos son los ficheros de `clases/rasgos/`, `clases/subclases/`, `especies/`,
`dotes/`, `trasfondos/` y `equipo/armaduras.yaml` (esta última como fuente *derivada*).
Recorrí las seis familias buscando efectos sobre `ca`, `velocidad` y `pg_max`. Los que
existen y **no** aplican a este personaje, con el motivo:

- `clases/rasgos/barbaro.yaml` (CA sin armadura, Movimiento rápido), `clases/rasgos/monje.yaml`,
  `clases/subclases/bardo.yaml`, `clases/subclases/hechicero.yaml`, `clases/subclases/paladin.yaml`,
  `clases/subclases/druida.yaml`, `clases/subclases/monje.yaml` — otras clases/subclases.
- `especies/especies.yaml → Goliat, Forma grande` y `→ Enano, Aguante enano` — otra especie.
- `dotes/origen.yaml → Duro` (`pg_max += 2 × nivel_total`), `dotes/generales.yaml → Duelista
  defensivo`, `→ Maestro en armaduras medias`, `→ la dote de +3 m de velocidad`,
  `dotes/don_epico.yaml` — dotes que el personaje no tiene. El crudo declara exactamente
  dos entradas en `dotes` y `mejoras`: Defensa y Mejora de característica.
- `trasfondos/trasfondos.yaml` — ningún trasfondo declara `efectos:`; Acólito lleva
  `no_automatizado` diciendo que no tiene prosa con mecánica escondida.

**Anotación sobre el crudo, ajena a estos cinco números.** `trasfondos/trasfondos.yaml →
Acólito` declara `dote: "Iniciado en la magia (clérigo)"`, y esa dote **no aparece** en la
lista `dotes` del crudo. Leí `dotes/origen.yaml → Iniciado en la magia` para descartar que
alterase algo aquí: concede dos trucos y un conjuro de nivel 1 con aptitud mágica propia
(a elegir entre Int, Sab o Car), y no toca CA, velocidad, PG ni la CD de la clase. La
ausencia es un hueco de la ficha, no un cambio en ninguno de los cinco valores.

---

## 1. `pg_max`

**Reglas.**

- Dado de golpe: `clases/explorador.yaml → atributos_basicos.dado_golpe: d10`.
- Nivel 1: `reglas/generacion_personaje.yaml → puntos_golpe.nivel_1.regla` —
  «Máximo del dado de golpe + modificador por Constitución» (pdf 42, libro 40).
- Niveles siguientes: `reglas/generacion_personaje.yaml → puntos_golpe.niveles_siguientes_al_1.literal`
  (pdf 44, libro 42) — «Tira ese dado, suma tu modificador por Constitución al resultado y
  añade el total (mínimo de 1) a tus puntos de golpe máximos. En vez de tirar, puedes
  utilizar el valor establecido…».
- Valor establecido: misma sección, `tabla_valores_establecidos.filas` —
  `{clases: [Explorador, Guerrero, Paladín], valor: 6}`.

El crudo declara en `pg_por_nivel` exactamente esa elección: nivel 1 `metodo: maximo_dado,
valor: 10`; niveles 2 a 6 `metodo: valor_establecido, valor: 6`.

**Punto de duda, resuelto.** El «6» de la tabla, ¿es el sustituto del dado (y encima se
suma el mod. Con), o el total del nivel ya con todo dentro?

- *Lectura A (la que elijo):* sustituye **solo al dado**. El literal encadena «Tira ese
  dado, suma tu modificador por Constitución… En vez de **tirar**…»: lo que se reemplaza es
  el acto de tirar, no la suma posterior. Lo confirma
  `puntos_golpe.aumento_de_constitucion._nota_para_el_motor`, que describe el término de
  Constitución como `nivel_total × mod_con` — eso solo es cierto si el mod. Con entra en
  los seis niveles, también en los que usaron valor establecido.
- *Lectura B (descartada):* el 6 sería el total del nivel. Contradiría la nota anterior y
  dejaría la Constitución sin efecto retroactivo, que es justo lo que esa sección subraya.

**Derivación.**

```
Nivel 1 : máximo de d10 ......................... 10
Niveles 2-6 : 5 niveles × valor establecido 6 ... 30
Término de dado, acumulado ...................... 40

Término de Constitución : nivel_total × mod_con
                        = 6 × (+1) ............... +6

pg_max = 40 + 6 = 46
```

Comprobación por niveles (mismo resultado, otra ruta): 11 + 7 + 7 + 7 + 7 + 7 = 46.
Ningún nivel cae bajo el mínimo de 1 (el peor total aquí es 7).

Sin sumandos externos: la especie Aasimar no tiene nada como «Aguante enano», y el
personaje no lleva la dote «Duro» ni ninguna otra que declare efectos sobre `pg_max`.

> **`pg_max` = 46**

---

## 2. `ca`

**Equipo relevante.** El crudo lleva una sola pieza: `equipo/armaduras.yaml#Media armadura`.
**No lleva escudo** — `equipo` no tiene ninguna otra entrada, y
`equipo/armaduras.yaml → reglas.escudos` solo da el +2 a quien embrace uno.

**Trampa de nombre, resuelta.** «Media armadura» está en la tabla `armaduras_medias` de
`equipo/armaduras.yaml`: es armadura **media**, no pesada, pese a lo que sugiere el nombre.
Esto importa dos veces (aquí para el tope de Destreza, y en el apartado 3 para «Errante»).

**Reglas.**

- `equipo/armaduras.yaml → armaduras_medias.tabla`, fila
  `{nombre: "Media armadura", ca: "15 + mod. Des (máx. 2)", fuerza: null, sigilo: Desventaja}`
  (fuente del fichero: pdf 218, libro 216).
- `dotes/estilo_de_combate.yaml → Defensa` (pdf 211, libro 209): «Mientras lleves puesta una
  armadura ligera, media o pesada, recibes un bonificador de +1 a la clase de armadura».

**La condición de Defensa se cumple.** El crudo declara la dote en
`dotes: [{ref: dotes/estilo_de_combate.yaml#Defensa, origen: {clase: Explorador, rasgo: Estilo
de combate}}]`, coherente con `clases/rasgos/explorador.yaml → Estilo de combate` (nivel 2,
«Obtienes una dote de estilo de combate de tu elección»). Y el personaje lleva puesta
armadura media, que es una de las tres que el texto acepta. El texto **no** exige ir sin
escudo, así que no hay nada que descartar por ese lado.

**Tope de Destreza.** El mod. Des es +3, pero la armadura media lo limita a «máx. 2».
La única cosa de la base que sube ese tope a 3 es `dotes/generales.yaml → Maestro en
armaduras medias` (`op: modifica_tope, tope: mod_des, formula: "3"`), y **el personaje no
la tiene**: su única dote general es Mejora de característica. Por tanto el tope sigue en 2.

**Derivación.**

```
Base de Media armadura ..................... 15
Modificador por Destreza, topado:
    min(mod_des, 2) = min(+3, 2) ........... +2
Defensa (estilo de combate, con armadura) .. +1
Escudo ..................................... +0  (no lleva)

ca = 15 + 2 + 1 = 18
```

**Situacionales descartados explícitamente (NO entran en la CA de la ficha):** ninguno de
los rasgos activos a nivel 6 modifica la CA de forma permanente ni temporal. En concreto,
*Esquiva de las sombras* (subclase, **nivel 15**) da desventaja a un atacante con una
reacción, no CA, y además ni siquiera está activa a nivel 6.

> **`ca` = 18**

---

## 3. `velocidad`

**Reglas.**

- Base de especie: `especies/especies.yaml → Aasimar.velocidad_m: 9` (pdf 188, libro 186).
- `clases/rasgos/explorador.yaml → Errante` (nivel 6, pdf 106, libro 104):
  «Tu velocidad aumenta en 3 m **si no llevas armadura pesada**. Además obtienes una
  velocidad nadando y una velocidad trepando iguales a tu velocidad.»
- `equipo/armaduras.yaml → reglas.fuerza`: «Si la tabla indica una puntuación de Fuerza para
  un tipo de armadura, esta reduce 3 m la velocidad de quien la lleve, salvo que su Fuerza
  sea igual o superior a la indicada.»

**La condición de «Errante» se cumple.** El personaje tiene nivel 6 de explorador, así que
el rasgo está activo (`clases/explorador.yaml → progresion`, fila `n: 6`, `rasgos: ["Errante"]`).
Su única armadura, **Media armadura**, figura en `armaduras_medias` de `equipo/armaduras.yaml`
— es media, **no pesada** —, luego la condición «si no llevas armadura pesada» se satisface
y el +3 m entra. (Aquí es donde el nombre engaña: si uno lo leyera como «armadura pesada»,
perdería 3 m indebidamente.)

**Sin penalización por Fuerza.** La fila de Media armadura trae `fuerza: null`, es decir, la
tabla no indica puntuación de Fuerza para ella, así que la regla de los −3 m no se dispara.
La Fuerza 12 del personaje es irrelevante aquí (habría importado con Cota de malla 13 o
Bandas/Placas 15, que no lleva).

**Derivación.**

```
Velocidad de especie (Aasimar) ................. 9 m
Errante (nivel 6, sin armadura pesada) ......... +3 m

velocidad = 9 + 3 = 12 m
```

**Situacionales descartados explícitamente (NO entran en la velocidad de la ficha):**

1. **«Salto emboscador»**, mitad de *Emboscador pavoroso*
   (`clases/subclases/explorador.yaml → Acechador en la Penumbra`, nivel 3, pdf 108, libro 106):
   «al comienzo de tu primer turno de cada combate, tu velocidad aumenta en 3 m **hasta el
   final de ese turno**». Dura un turno y solo en el primero de cada combate: es un bono
   temporal, **no** parte del número permanente. Si entrase, daría 15 m — y sería un error.
2. **«Revelación celestial / Alas celestiales»** (`especies/especies.yaml → Aasimar`, nivel 3):
   transformación de **1 minuto, 1 vez por descanso largo**, y además concede velocidad
   **volando**, no velocidad a pie. Doblemente fuera: situacional y de otro tipo de velocidad.
3. **Velocidades nadando y trepando** que concede el propio «Errante»: son tipos de velocidad
   distintos, iguales a la velocidad (12 m cada una), y no alteran el número de velocidad
   a pie. El comentario del propio rasgo en la base dice que no se declaran.

> **`velocidad` = 12 m** (9 de especie + 3 de Errante)

---

## 4. `cd_conjuros`

**Reglas.**

- Fórmula: `reglas/generacion_personaje.yaml → conjuros.cd_salvacion.formula` (pdf 240,
  libro 238): «8 + modificador de aptitud mágica + bonificador por competencia», `base: 8`.
- Aptitud mágica: `clases/explorador.yaml → aptitud_magica: Sabiduría`. Lo repite
  `clases/rasgos/explorador.yaml → Lanzamiento de conjuros` («Aptitud mágica: Sabiduría»).
- Mod. Sab = +2 (apartado 0.1); PB = +3 (apartado 0.2).

**Derivación.**

```
Base .................................. 8
Modificador de aptitud mágica (Sab) ... +2
Bonificador por competencia ........... +3

cd_conjuros = 8 + 2 + 3 = 13
```

**Notas.** Una sola clase lanzadora, así que no interviene nada de
`generacion_personaje.yaml → multiclase.lanzamiento_de_conjuros_multiclase`. El estilo de
combate elegido fue Defensa, no *Guerrero druídico*, así que no hay una segunda vía de
lanzamiento por ese lado. La dote de trasfondo *Iniciado en la magia* (que la ficha no
declara, ver 0.3) tendría su propia aptitud mágica y no cambiaría esta CD.

> **`cd_conjuros` = 13**

---

## 5. `bonif_ataque_conjuros`

**Reglas.**

- Fórmula: `reglas/generacion_personaje.yaml → conjuros.bonificador_ataque.formula` (pdf 240,
  libro 238): «modificador de aptitud mágica + bonificador por competencia», `base: 0`.
- Aptitud mágica Sabiduría, mod. Sab = +2; PB = +3.

**Derivación.**

```
Base .................................. 0
Modificador de aptitud mágica (Sab) ... +2
Bonificador por competencia ........... +3

bonif_ataque_conjuros = 0 + 2 + 3 = +5
```

> **`bonif_ataque_conjuros` = +5**

---

## Valores derivados

| Valor | Resultado | Derivación en una línea | Cita principal |
|---|---|---|---|
| `pg_max` | **46** | (10 máx. d10 + 5×6 establecido) + 6 niveles × mod. Con +1 | `reglas/generacion_personaje.yaml → puntos_golpe.nivel_1` y `→ puntos_golpe.niveles_siguientes_al_1` (pdf 42 y 44); `clases/explorador.yaml → atributos_basicos.dado_golpe` |
| `ca` | **18** | 15 (Media armadura) + min(+3, 2) Des + 1 (Defensa) | `equipo/armaduras.yaml → armaduras_medias` (pdf 218); `dotes/estilo_de_combate.yaml → Defensa` (pdf 211) |
| `velocidad` | **12 m** | 9 (Aasimar) + 3 (Errante, sin armadura pesada) | `especies/especies.yaml → Aasimar.velocidad_m` (pdf 188); `clases/rasgos/explorador.yaml → Errante` (pdf 106) |
| `cd_conjuros` | **13** | 8 + 2 (mod. Sab) + 3 (PB) | `reglas/generacion_personaje.yaml → conjuros.cd_salvacion` (pdf 240); `clases/explorador.yaml → aptitud_magica` |
| `bonif_ataque_conjuros` | **+5** | 2 (mod. Sab) + 3 (PB) | `reglas/generacion_personaje.yaml → conjuros.bonificador_ataque` (pdf 240); `clases/explorador.yaml → aptitud_magica` |

Cantidades intermedias, por si sirven al contraste: mod. Fue +1, mod. Des +3, mod. Con +1,
mod. Int +1, mod. Sab +2, mod. Car −1, PB +3.

## Lo que no se pudo derivar

Nada de los cinco valores encargados quedó sin derivar: los cinco salen enteros de la base,
con página. No hubo que recurrir a la CA por defecto sin armadura (el personaje va con
armadura), ni hizo falta salir de los ficheros permitidos.

Dos observaciones que **no** son huecos de estos cinco números pero conviene que consten:

1. **Dote de trasfondo ausente en el crudo.** `trasfondos/trasfondos.yaml → Acólito` concede
   `dote: "Iniciado en la magia (clérigo)"` y la lista `dotes` del crudo no la incluye.
   No afecta a ninguno de los cinco valores (ver 0.3), pero la ficha está incompleta ahí.
2. **Unidades.** La base trabaja en metros (`velocidad_m`, «aumenta en 3 m»). El 12 de
   `velocidad` es metros; si el campo de la ficha esperase pies, el equivalente del manual
   sería 40 pies, pero la base no declara ninguna tabla de conversión y no la he supuesto.

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
pg_max: 46
ca: 18
velocidad: 12
cd_conjuros: 13
bonif_ataque_conjuros: 5
```
