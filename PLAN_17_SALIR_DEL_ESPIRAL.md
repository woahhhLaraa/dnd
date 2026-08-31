# PLAN 17 — Salir del espiral de verificadores

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

### ⬜ C5 · Rellenar las fuentes que faltan — **el grueso, exige el manual**

El trabajo de contenido, una vez C1-C4 hacen que sea imposible dejarlo a
medias:

| Fuente | Registros | Estado |
|---|---|---|
| `dotes/*.yaml` | 75 (54 con «+1 característica») | 0 con `efectos:` |
| `clases/subclases/*.yaml` | 241 rasgos en 46 ficheros | 2 ficheros hechos |
| `trasfondos/trasfondos.yaml` | 16 | sin revisar |
| `clases/rasgos/*.yaml` | 158 (70 «suenan» numéricos) | 7 efectos declarados |

⚠️ **Ese «70» es una heurística mía, no un hallazgo.** Muchos son falsos
positivos: su número vive en la columna de `progresion`, que ya está
contrastada por `verificar_srd.py`. Solo C2 dirá cuántos son de verdad,
porque obliga a mirarlos uno a uno. **No lo trates como 63 agujeros.**

---

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

## 7. Orden de ejecución

C1 y C2 **antes** que C5, y no al revés: rellenar 120 registros a mano sin que
el sistema exija el campo es garantizar que el 121 se quede fuera.

```
1. ✅ C1  _ORIGENES → descubrimiento + manifiesto   (hecho 2026-08-31)
2. ✅ C4  `conditional` en el vocabulario           (hecho 2026-08-31)
3. ✅ C3  mejora de característica por dote         (hecho 2026-08-31)
4. ⬜ C5  rellenar: dotes → subclases → trasfondos  (el grueso, ~semanas)
5. ⬜ C2  `efectos:` obligatorio + `no_automatizado`
6. ⬜ Borrados de §5 (falta FODA_..._OBSOLETO.md)
```

**C2 se movió detrás de C5, y el plan original se equivocaba.** Decía que
dejar la base en rojo con ~500 registros sin declarar «es el éxito, no el
fracaso». En un proyecto de una sola persona eso es meses de rojo permanente
durante los cuales **no se distingue una rotura nueva de la deuda conocida**,
que es justo la señal que hace falta mientras se rellena. Primero se rellena,
después se cierra la puerta.

El paso 3 dejará la base en rojo con ~400 registros sin declarar. **Eso es el
éxito, no el fracaso**: es la primera vez que el proyecto ve el tamaño real de
lo que no sabe.

---

## 8. Criterio de cierre

El plan está hecho cuando las cuatro cosas son ciertas a la vez:

1. Crear `clases/subclases/_prueba.yaml` hace fallar a `efectos.py` (C1).
2. Quitar `efectos:` de cualquier rasgo hace fallar a `validar.py` (C2).
3. La tabla invertida de §0 está del derecho: correcta en verde, rota en rojo,
   para `Duro` (nivel 1) y para `Actor` (nivel 4) (C3).
4. `generar_ficha.py --barrido --exhaustivo` sigue en 240/240 **y** el barrido
   varía la dote elegida en vez de coger siempre «Mejora de característica»,
   que es la única de las 75 que el esquema sabía expresar y por eso 240 fichas
   verdes nunca tocaron el caso que rompe.

---

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
