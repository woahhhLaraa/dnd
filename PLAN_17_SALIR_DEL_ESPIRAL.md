# PLAN 17 — Salir del espiral de verificadores

> **Estado (2026-08-31): C1, C3 y C4 hechas.** Los puntos que quedaban
> abiertos (C2, C5, C6) están **absorbidos en `PLAN_18_REVISION_COMPLETA.md`**,
> que es el documento de trabajo hacia delante y trae las cifras remedidas.
> Este fichero se conserva por lo que no está en ninguna otra parte: la
> investigación sobre Foundry dnd5e y DiceCloud (§1) y el diagnóstico del
> espiral (§2).

> Escrito el **2026-08-31**, tras leer el código real de Foundry dnd5e y
> DiceCloud (clonados, no sus README). Todas las cifras de este documento
> están **medidas** con los comandos que se citan al lado. Si vuelves y no
> cuadran, la base ha cambiado y el plan también.
>
> **Motivo:** en tres fases distintas (14, 15, 16) se cerró trabajo dejando
> huecos que nadie sabía que existían, y la respuesta a cada hueco fue
> escribir otro verificador. Este plan **no añade un verificador más**: quita
> la causa por la que aparecen.

---

## 0. El problema, en una frase

`efectos.py` no aplica los efectos de **54 de 75 dotes** ni de **46 de 48
subclases**, y nada en la base lo detecta. Peor: el verificador **rechaza la
ficha correcta y aprueba la rota**.

Reproducción, con una ficha de nivel 1 (`personajes/_ejemplo_aerin.yaml`):

| Ficha | `verificar_personaje.py` |
|---|---|
| Toma `Duro` (dote de origen, «+2 PG por nivel») y **aplica** el +2 | ❌ *«recalculado da 9»* — la rechaza |
| Toma `Duro` y **no** aplica el +2 (los PG quedan mal) | ✅ **0 problemas** |

Lo mismo con `Actor` (+1 Carisma) sobre `draconido_hechicero_n4.yaml`: la
ficha correcta da error, la rota pasa en verde con la CD, el ataque y la CA
un punto por debajo.

---

## 1. Qué hacen los proyectos maduros (investigación, 2026-08-31)

### 1.1 Foundry dnd5e — no automatiza casi nada, y lo dice

Es la implementación de D&D 5e más usada que existe, con equipo a tiempo
completo. Medido sobre su contenido SRD 2024 (`packs/_source/classes24/`):

```
registros de clase/subclase 2024:            332
  con Active Effects (automatizado):          76   (23 %)
  sin effects (solo texto):                  256   (77 %)
```

**No resolvieron el espiral automatizando todo. Lo resolvieron no
intentándolo.** Y la frontera no queda implícita: **380 registros** llevan una
`<section class="secret">Foundry Note</section>` dentro del propio dato,
diciendo qué hace el sistema y qué tiene que hacer la persona. Textual, de
`grappler.yml`:

> *«Foundry Note. The Advantage is not automated.»*

Eso es lo que aquí no existe: **una forma de decir "esto no se calcula" que no
sea el silencio.**

### 1.2 Foundry — una taxonomía cerrada de 9 tipos, y un único camino

`module/documents/advancement/`:

```
ability-score-improvement · hit-points · item-choice · item-grant
modify-item · scale-value · size · subclass · trait
```

Lo decisivo para nuestro agujero: **una dote que sube una característica usa
el MISMO mecanismo que la mejora de nivel 4.** De `grappler.yml`:

```yaml
advancement:
  - type: AbilityScoreImprovement
    configuration:
      cap: 1
      points: 1
      locked: [con, int, wis, cha]   # solo Fue/Des elegibles
effects: []                          # ← la dote NO usa Active Effects
```

No hay un camino «efecto de dote» separado del camino «mejora de nivel». Por
eso **no se puede olvidar conectar uno de los dos**: es el mismo.

### 1.3 Foundry — cero tests

`package.json`, sección `scripts`, íntegra: `build`, `lint`, `watch`. **No hay
suite de tests, ni validadores de datos, ni pruebas por mutación.** Su
verificación es `eslint .` más cientos de miles de personas jugando.

> **Lectura honesta, y por qué NO copiamos esto:** Foundry sustituye
> verificación por uso masivo. Este proyecto tiene una usuaria. Sus 3666
> valores contrastados y sus 149 mutaciones **son el sustituto correcto** de
> los usuarios que no tiene. Lo que hay que copiar de Foundry es la
> **arquitectura**, no la ausencia de pruebas.

### 1.4 DiceCloud — la operación que nos falta

`app/imports/api/properties/Effects.ts`, vocabulario completo:

```
base · add · mul · min · max · set
advantage · disadvantage · passiveAdd · fail · conditional
```

El nuestro (`reglas/efectos.yaml`) tiene los **seis primeros**. Falta el que
resuelve el espiral, y su comentario en el código fuente lo explica:

```ts
// Conditional benefits store just uncomputed text
text: { type: String, ... }
```

**`conditional` es un efecto declarado que guarda texto y no se calcula.** Es
el equivalente estructurado de la «Foundry Note».

Su agregador (`getAggregatorResult.js`) son **30 líneas** y es idéntico al
nuestro en orden y semántica. No hay nada que copiar ahí: ya lo tenemos bien.

---

## 2. El diagnóstico: repetimos el error que ya habíamos diagnosticado

La cabecera de `reglas/efectos.yaml` dice, con todas las letras:

> *«`calculo.py` tenía las fórmulas de "Defensa sin armadura" como `lambda` de
> Python, y por eso conocía 2 de las 4 que hay en la base (se le escapaban las
> de SUBCLASE). Una regla cableada no se puede citar, no se puede validar y no
> se entera de que hay una quinta.»*

Y doce líneas más abajo, en `efectos.py`:

```python
_ORIGENES = (
    ("especies/especies.yaml", ...),
    ("clases/rasgos/barbaro.yaml", ...),      # ← 12 rutas literales
    ...
    ("clases/subclases/bardo.yaml", ...),     # ← 2 de 48 subclases
    ("clases/subclases/hechicero.yaml", ...),
)                                              # ← 0 de 4 ficheros de dotes
```

**`_ORIGENES` es `_CA_SIN_ARMADURA` otra vez, un nivel más arriba.** Se
sustituyó un diccionario cableado de *fórmulas* por una tupla cableada de
*rutas*. Conoce 2 de las 48 subclases y **no se entera de que hay una tercera**
— exactamente la frase que la propia base escribió para condenar el patrón.

Ese es el motor del espiral. Mientras la cobertura sea una lista escrita a
mano, cada fuente nueva es un hueco futuro, y cada hueco pide su verificador.

---

## 3. Decisión de fondo: **NO se rehace la matemática**

Ofreciste rehacerla desde cero. Medido, no hace falta, y sería tirar lo único
que está bien diseñado:

- El vocabulario cerrado (`reglas/efectos.yaml`: 12 variables, 6 operaciones,
  4 condiciones, todo con página citada) es **el modelo de DiceCloud, bien
  implementado**.
- El agregador de `efectos.py` coincide con el de DiceCloud en orden y
  semántica.
- `mutaciones_efectos.py` da 26/26 y `mutaciones_pg.py` 13/13: el motor está
  probado donde se usa.

**El motor es correcto. Lo que está mal es a cuántos ficheros se le deja
mirar.** El trabajo es de fontanería y de relleno de datos, no de rediseño.

---

## 4. CAMBIOS

### ✅ C1 · `_ORIGENES` deja de ser una lista escrita a mano — **HECHA (2026-08-31)**

`efectos.py`. Sustituir la tupla literal por **descubrimiento + manifiesto**:

1. Descubrir por glob todos los ficheros de regla:
   `especies/*.yaml`, `clases/rasgos/*.yaml`, `clases/subclases/*.yaml`,
   `dotes/*.yaml`, `trasfondos/*.yaml`.
2. Un manifiesto (`reglas/fuentes_de_efectos.yaml`) declara para cada patrón
   la ruta de descenso (`("subclases","rasgos")`, etc.).
3. **Un fichero descubierto que el manifiesto no sepa recorrer es un ERROR**,
   no un salto silencioso. `ErrorDeEfectos`, como ya hace con
   `origen de efectos inexistente`.

**Criterio de cierre — CORREGIDO al implementarlo.** Este plan decía que
añadir `clases/subclases/_prueba.yaml` debía **fallar**. Es al revés, y el
comportamiento real es mejor: un fichero de subclase nuevo **lo recoge el
patrón solo**, sin tocar nada. Lo que falla es un fichero de regla que
**ningún patrón sepa recorrer** y que no esté declarado como excluido —
probado con `reglas/_prueba_c1.yaml`, que lanza `ErrorDeEfectos` nombrándolo.

**Resultado medido:** de **15 fuentes cableadas a 30 descubiertas**.

### ⬜ C2 · `efectos:` obligatorio en todo rasgo — **REORDENADA: va DESPUÉS de C5**

Es la «Foundry Note» de §1.1, estructurada. Todo registro con `desc`/
`descripcion` en las fuentes de C1 debe declarar una de estas dos cosas:

```yaml
# a) tiene efecto calculable
efectos:
  - {operacion: add, variable: pg_max, cantidad: "2 * nivel_total",
     pagina: {pdf: 206, libro: 204}}

# b) no lo tiene, y se dice POR QUÉ
efectos: []
no_automatizado: "ventaja en pruebas de Carisma para suplantar: no es un
                  número que la ficha calcule"   # pdf 204 = libro 202
```

Lo que desaparece es la tercera opción actual: **el campo ausente**, que hoy
es indistinguible de «se nos olvidó».

`validar.py` exige el campo. No exige adivinar semántica con expresiones
regulares — solo que **alguien ya haya decidido y escrito** de qué lado cae.

> Esto es exactamente la doctrina que la base ya aplica en
> `verificar_chequeos.py` con `# TOLERADO:` — una rama silenciosa o avisa, o se
> declara. Aquí es lo mismo para los rasgos.

### ✅ C3 · La dote que sube una característica — **HECHA (2026-08-31)**

Copiar el modelo de `grappler.yml` (§1.2). Hoy `personajes/_ESQUEMA.md` exige
`final = base + ajuste_trasfondo + mejoras`, y una dote **no tiene dónde
entrar** — de ahí el caso `Actor`. Pasa a:

```
final = base + ajuste_trasfondo + Σ(mejoras) + Σ(mejoras de dote)
```

donde la dote declara su incremento con la misma forma que la mejora de nivel
4 (`sube: {car: 1}`, con `cap: 1` y las características bloqueadas cuando el
manual las bloquea). **Un solo camino, no dos.**

**Criterio de cierre — CUMPLIDO.** La tabla de §0 está del derecho:

| Ficha | Antes | Ahora |
|---|---|---|
| `Duro` (nivel 1) con su +2 PG — CORRECTA | ❌ | ✅ |
| `Duro` con el +2 perdido — ROTA | ✅ | ❌ |
| `Actor` (nivel 4) con su +1 Car — CORRECTA | ❌ | ✅ |
| `Actor` con el +1 perdido — ROTA | ✅ | ❌ |

**Cómo se hizo sin transcribir nada nuevo:** se ESTRUCTURÓ la prosa ya citada
y se exigió **ida y vuelta 54/54 exacta** (el método de la Fase 15). El
chequeo permanente es `validar_mejoras_de_dote()`, y salta en los dos
sentidos: prosa sin estructura, y estructura sin prosa.

**Lo que la ida y vuelta evitó:** los **12 dones épicos dicen «máx. 30»**, no
20. Suponer 20 habría inventado una regla para 12 dotes.

**Defecto encontrado en los datos propios:** `draconido_hechicero_n4.yaml`
tomaba `Lanzador ritual` (+1 a Int/Sab/Car) y no aplicaba el +1 — Carisma 17,
CD 13, ataque +5, CA 15 donde debía ser 18/14/+6/16. Corregido.

### ✅ C4 · Ampliar el vocabulario con `conditional` — **HECHA (2026-08-31)**

`reglas/efectos.yaml`. Añadir la operación de DiceCloud que falta, para los
efectos reales pero no numéricos (ventaja, resistencia, competencia). Guarda
texto y página; **no entra en el agregador**. Sin esto, C2 obliga a marcar
como «no automatizado» cosas que sí son efectos, solo que no aritméticos.

### ⬜ C5 · Declarar los efectos que faltan — **MEDIDO el 2026-08-31: son 21, no 528**

**Corrección importante a este mismo plan.** La versión anterior hablaba de
«~528 registros» y de «semanas». Esa cifra era la de C2 (que TODO registro
declare algo), no la del trabajo funcional. Medido contra la realidad:

```
variables calculables en reglas/efectos.yaml:  ca · pg_max · velocidad   (3)
```

Un efecto **solo puede tocar esas tres**. Así que el hueco funcional no son
todos los rasgos: son los que mencionan una de las tres en su texto **ya
transcrito y citado** y no la declaran. Contados con `efectos.origenes()`:

| Variable | Candidatos sin declarar |
|---|---|
| `velocidad` | 10 |
| `ca` | 6 |
| `pg_max` | 5 |
| **Total** | **21** |

**Y casi todos se pueden cerrar sin abrir el manual**, porque su texto ya está
transcrito con su página. Clasificados leyendo esos textos:

**C5-a · Declarables hoy, vocabulario actual (~4)**
| Rasgo | Texto citado | Efecto |
|---|---|---|
| `Veloz` (dote) | «tu velocidad aumenta 3 m» | `velocidad +3`, sin condición |
| `Defensa` (estilo) | «mientras lleves armadura ligera, media o pesada, +1 a la CA» | `ca +1`, `requiere: [con_armadura]` |
| `Don de la fortaleza` | «PG máximos +40» | `pg_max +40` |
| `Movimiento rápido`* | «velocidad aumenta 3 m mientras no lleves armadura pesada» | ver C5-b |

**C5-b · Falta vocabulario: la condición «sin armadura pesada» (2)**
`Movimiento rápido` (Bárbaro) y `Errante` (Explorador) condicionan a **no
llevar armadura PESADA**, y las condiciones actuales solo distinguen
`sin_armadura` / `con_armadura`. No es lo mismo: un bárbaro con armadura media
sí conserva el bonificador. Hay que añadir la condición al vocabulario cerrado
antes de declararlos; inventarse `sin_armadura` sería falsear la regla.

**C5-c · Modelo insuficiente, y es un hallazgo (1)**
`Maestro en armaduras medias`: «sumas **3 (en vez de 2)** a tu CA por Destreza
si tu Destreza es 16 o más». Eso no es `add` ni `set` sobre `ca`: **cambia un
parámetro de la fórmula de la armadura** (el tope de Destreza). El modelo
actual —base/add/mul/min/max/set sobre una variable— no lo expresa. Es el
equivalente al `ModifyItem` de Foundry. Decidir si se modela o se declara
`no_automatizado`; no forzarlo.

**C5-d · Situacionales → `conditional` o `no_automatizado` (~14)**
`Puntería certera` (velocidad 0 tras usar el rasgo), `Atacante a la carga`
(+3 m solo al correr), `Duelista defensivo` (reacción, +PB a la CA),
`Forma grande` (10 minutos), `Aura de celeridad`, `Defensa gloriosa`,
`Inspiración en combate`… Son efectos ciertos y citados que el motor **no
debe** calcular. Con C4 ya hay dónde ponerlos.

**Método, el mismo que funcionó en C3:** derivar de la prosa ya citada y
exigir ida y vuelta. **Nada de esto necesita el PDF** salvo que el texto
transcrito resulte ambiguo, y entonces se marca y se pregunta (regla 3).

**Criterio de cierre:** los 21 candidatos, a cero. El chequeo que los cuenta
es el de C6.

---

### ⬜ C6 · Las cuatro listas escritas a mano que quedan

La regla inviolable 6 nació de cinco casos; el sexto apareció al medir C5:

| Lista | Qué se le escapa | Arreglo |
|---|---|---|
| `validar._PROMESAS` | **vigila `ca` y `pg_max`, no `velocidad`** — por eso los 10 rasgos de velocidad pasaron desapercibidos | derivarla de las variables `calculada` del vocabulario, no escribirla |
| `verificar_chequeos.FUENTES` | audita 3 de las 6 que declara (las otras 3 ponen su lógica en `main()`) | descubrir por glob y no filtrar por nombre de función |
| `verificar_srd.MAPA` | `pb`, `forma_salvaje`, `mov_sin_armadura_m` sin contraste externo | exigir que toda columna esté mapeada o declarada como no contrastable |
| `verificar_foundry.MODULOS` | categorías de dato sin contrastar | ídem |

`_PROMESAS` es el más urgente y el más barato: es literalmente la lista que
tenía que haber avisado de los 10 huecos de velocidad, y su contenido correcto
**ya está** en `reglas/efectos.yaml`.

## 5. ELIMINAR

| Qué | Por qué |
|---|---|
| **El `verificar_cobertura_efectos.py` que propuse el 2026-08-31** | **No llegar a escribirlo.** Era el espiral otra vez: auditar con expresiones regulares lo que ya existe, en vez de impedir que vuelva a pasar. C1+C2 lo dejan sin trabajo que hacer |
| `FODA_2026-08-19_OBSOLETO.md` (14 KB) | El propio `CONTINUAR.md` avisa: *«⛔ está archivado… manda hacer fases ya cerradas. No lo uses para decidir.»* Un documento que hay que avisar de no leer es un documento que ya está en el historial de git |
| `clases/subclases/_borrador_mapa.yaml` | Se declara *«BORRADOR NO VERIFICADO… No usar para crear personajes»*, y **ningún script lo lee** (comprobado). Con C1 pasaría a ser descubierto por glob y a exigir `efectos:`, así que estorba activamente |
| La rama muerta de `verificar_chequeos.py` que reescribe la línea base | Si un cambio cierra una rama silenciosa y abre otra, `if cerradas:` guarda la huella **con la nueva dentro** y devuelve 1; la siguiente ejecución sale verde sin que nadie arregle nada. Quitar esa reescritura automática |

### Lo que NO se borra, aunque lo parezca

- `_origen_hechizos.csv` (304 KB): es la procedencia documentada de
  `hechizos.json` y lo citan `verificar_foundry.py` y `FUENTES.md`. Es
  historia, no lastre.
- `verificar_documentos.py`: es el más «meta» de todos y aun así **cazó el
  fallo real** de esta revisión (`foundry: 3020 → None`) y una inyección de
  prueba. Se queda.

---

## 6. DEJAR ESTAR (no tocar)

Esto es lo bueno del proyecto y el espiral no es excusa para desmontarlo:

| Qué | Por qué se queda |
|---|---|
| `verificar_srd.py` + `verificar_foundry.py` (3666 valores, 0 discrepancias) | Es el sustituto de los usuarios que Foundry tiene y tú no. Probado: detecta y sale con código 1 |
| Las 10 suites de mutación (149/149) | Sin ellas, «0 errores» no significa nada. Es lo que da derecho a fiarse del resto |
| `reglas/efectos.yaml` — el vocabulario cerrado | Es el modelo de DiceCloud bien hecho. Solo se le añade `conditional` (C4) |
| `pg_por_nivel` como historia por nivel | Correcto y sutil: hace que la regla retroactiva de Constitución salga sola |
| La disciplina de citar página en cada dato | Es lo que distingue esta base de todas las demás. No se relaja para ir más rápido |
| `validar.py` — chequeos de transcripción | Aburridos y valiosos. No son la causa del espiral |

---

## 7. Orden de ejecución — **revisado el 2026-08-31 tras medir C5**

```
✅ C1  _ORIGENES → descubrimiento + manifiesto        (hecho)
✅ C4  `conditional` en el vocabulario                (hecho)
✅ C3  mejora de característica por dote · 54/54      (hecho)
⬜ C6a `_PROMESAS` derivada del vocabulario           (~1 h, y es la que falló)
⬜ C5a declarar los ~4 inequívocos                    (~2 h, sin manual)
⬜ C5b condición «sin armadura pesada» + los 2 rasgos (~2 h, sin manual)
⬜ C5d los ~14 situacionales como `conditional`       (~medio día, sin manual)
⬜ C5c decidir qué hacer con `Maestro en armaduras medias`
⬜ C6b las otras 3 listas escritas a mano
⬜ C2  `efectos:` obligatorio                          (al final, no antes)
```

**Lo que cambia respecto a la versión anterior de este plan:** C5 pasa de
«semanas y hace falta el manual» a **un día de trabajo sin abrir el PDF**,
porque el texto ya está transcrito y citado y las variables calculables son
tres. La lectura del manual queda solo para los casos en que la transcripción
resulte ambigua.

**C6a va primero** por una razón concreta: es la lista que tenía que haber
avisado de los 10 huecos de velocidad y no lo hizo. Arreglarla antes de
rellenar significa que el propio chequeo te dice cuándo has terminado, en vez
de tener que fiarte de una lista que yo escribí a mano hoy.

## 8. Criterio de cierre

El plan está hecho cuando las cinco cosas son ciertas a la vez:

1. ✅ Un fichero de regla que ningún patrón sepa recorrer hace fallar a
   `efectos.py` (C1, probado con `reglas/_prueba_c1.yaml`).
2. ✅ La tabla de §0 está del derecho para `Duro` y para `Actor` (C3).
3. ⬜ **Los 21 candidatos de C5 están a cero**, y el chequeo que los cuenta
   deriva su lista de variables del vocabulario, no de una tupla (C6a).
4. ⬜ Ninguna de las listas escritas a mano de C6 sigue siéndolo.
5. ⬜ Quitar `efectos:` de cualquier rasgo hace fallar a `validar.py` (C2).

Y en todo momento, sin excepción: `validar.py` a 0 errores, las 17 fichas y el
barrido 240/240 en verde, y los contrastes externos en 646 + 3020.

## 9. Sobre copiar código

Dijiste que copiar está bien y que el proyecto es 100 % personal. Dos notas:

- **Legalmente**, con uso personal no hay problema. La GPL-3.0 de DiceCloud
  obliga al **distribuir**, no al usar en privado; Foundry dnd5e es MIT, que
  solo pide conservar el aviso de copyright.
- **Prácticamente, no hay casi nada que copiar.** DiceCloud es TypeScript sobre
  Meteor/MongoDB y Foundry es JavaScript sobre su propio runtime; esto es
  Python sobre YAML. Lo aprovechable son **una lista de 11 palabras** (las
  operaciones), **una lista de 9** (los tipos de *advancement*) y **un
  agregador de 30 líneas que ya tienes escrito y probado**. El valor de esos
  repos era el diseño, y el diseño ya está en este documento.

---

## 10. Lo que este plan NO promete

No promete que no vuelva a aparecer un hueco. Promete que **la clase concreta
de hueco que ha aparecido tres veces —una fuente de reglas que el motor no
mira— deja de ser posible**, porque la cobertura pasa de ser una lista escrita
a mano a ser una comprobación de la propia base.

Las fuentes de regla de D&D 2024 son un conjunto cerrado y pequeño: especies,
rasgos de clase, subclases, dotes, trasfondos. Cinco. No «las que vayan
apareciendo». Por eso esto termina.
